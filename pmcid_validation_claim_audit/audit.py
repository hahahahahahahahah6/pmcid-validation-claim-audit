"""Inspect documentation and Python syntax without executing repository code."""
import argparse
import ast
import json
import os
from pathlib import Path
import re
import sys

from .phrases import YES, NO, GENERIC


def normalize(text):
    return ' '.join(text.lower().replace("n't", ' not').replace('-', ' ').split())


def claims(text):
    text = normalize(text)
    found = []
    for phrases in (NO, YES):
        hit = False
        for phrase in sorted(phrases, key=lambda p: (-len(p), p)):
            pattern = r'(?<!\w)' + re.escape(phrase) + r'(?!\w)'
            text, count = re.subn(pattern, lambda m: ' ' * len(m.group()), text)
            hit = hit or count > 0
        found.append(hit)
    return found[1], found[0]


def prose(text):
    output = []
    active = None
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if active is None:
            if marker:
                active = marker.group(1)
                output.append('')
            else:
                output.append(line)
        elif marker and marker.group(1)[0] == active[0] and len(marker.group(1)) >= len(active) and not line[marker.end():].strip():
            active = None
    return '\n'.join(output)


def evidence(source):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return False
    imports = {}
    definitions = set()
    bindings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.asname or alias.name.split('.')[0]] = alias.name
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            for alias in node.names:
                if alias.name != '*':
                    imports[alias.asname or alias.name] = node.module + '.' + alias.name
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)):
            targets = [node.target]
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            targets = [item.optional_vars for item in node.items if item.optional_vars]
        for target in targets:
            bindings.update(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
    shadows = definitions | bindings
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id not in shadows:
            route = imports.get(func.id, '')
            name = route.rsplit('.', 1)[-1]
            if name not in definitions and (route == 'idutils.is_pmcid' or ('.' in route and name in GENERIC)):
                return True
        elif isinstance(func, ast.Attribute) and func.attr not in definitions:
            base = func.value
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and base.id in imports and base.id in shadows:
                continue
            if func.attr in GENERIC:
                return True
            if (func.attr == 'is_pmcid' and isinstance(func.value, ast.Name)
                    and imports.get(func.value.id) == 'idutils' and func.value.id not in shadows):
                return True
    return False


def audit(root, ignore=()):
    root = Path(root)
    if root.is_symlink() or not root.is_dir() or not os.access(root, os.R_OK | os.X_OK):
        raise OSError('invalid or unreadable directory: ' + str(root))
    positive = negative = production = testing = False
    documents, sources = [], []
    def raise_error(error):
        raise error
    def ignored(path):
        return any(path.startswith(prefix) for prefix in ignore)
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=raise_error):
        base = Path(directory)
        dirs[:] = sorted(d for d in dirs if not (base / d).is_symlink() and not ignored((base / d).relative_to(root).as_posix()))
        for name in sorted(files):
            path = base / name
            rel = path.relative_to(root)
            if path.is_symlink() or ignored(rel.as_posix()):
                continue
            parts = rel.parts
            if (len(parts) == 1 and name == 'README.md') or (name.endswith('.md') and 'docs' in parts[:-1]):
                documents.append(rel.as_posix())
                for paragraph in re.split(r'\n\s*\n', prose(path.read_text(encoding='utf-8'))):
                    yes, no = claims(paragraph)
                    positive = positive or yes
                    negative = negative or no
            elif name.endswith('.py'):
                sources.append(rel.as_posix())
                if any(p in ('fixtures', 'docs', 'examples') for p in parts[:-1]):
                    continue
                is_test = 'tests' in parts[:-1] or name.startswith('test_') or name.endswith('_test.py')
                found = evidence(path.read_text(encoding='utf-8'))
                if is_test:
                    testing = testing or found
                else:
                    production = production or found
    findings = []
    if positive and not production:
        findings.append({'id': 'documented-pmcid-validation-claim-false', 'severity': 'MEDIUM' if testing else 'HIGH', 'message': 'Evidence occurs only in tests.' if testing else 'No production evidence found.'})
    if negative and production:
        findings.append({'id': 'documented-no-pmcid-validation-claim-false', 'severity': 'HIGH', 'message': 'Production evidence contradicts the negative claim.'})
    return {'findings': findings, 'production_evidence': production, 'test_evidence': testing, 'documents': documents, 'source_files': sources}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(1, self.prog + ': error: ' + message + '\n')


def main(argv=None):
    parser = Parser(prog='pmcid-validation-claim-audit')
    parser.add_argument('--version', action='version', version='0.1.0')
    sub = parser.add_subparsers(dest='command', required=True, parser_class=Parser)
    command = sub.add_parser('audit')
    command.add_argument('repo', nargs='?', default='.')
    command.add_argument('--json', action='store_true')
    command.add_argument('--verbose', action='store_true')
    command.add_argument('--ignore', action='append', default=[])
    command.add_argument('--fail-on', choices=('high', 'medium'), default='high')
    args = parser.parse_args(argv)
    try:
        result = audit(args.repo, args.ignore)
    except (OSError, UnicodeError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for item in result['findings']:
            print(item['severity'] + ' ' + item['id'] + ': ' + item['message'])
        if not result['findings']:
            print('PASS')
        if args.verbose:
            print('Documents: ' + str(len(result['documents'])) + '; Python files: ' + str(len(result['source_files'])))
    return 2 if any(item['severity'] == 'HIGH' or args.fail_on == 'medium' for item in result['findings']) else 0
