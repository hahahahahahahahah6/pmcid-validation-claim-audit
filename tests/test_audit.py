import contextlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest

from pmcid_validation_claim_audit.audit import audit, claims, evidence, main, prose
from pmcid_validation_claim_audit.phrases import YES, NO, GENERIC


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(set(YES)), len(set(NO)), len(set(GENERIC))), (50, 24, 24))
        for phrase in YES:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase), (True, False))
        for phrase in NO:
            with self.subTest(phrase=phrase):
                self.assertEqual(claims(phrase), (False, True))
        for text, expected in [('documented pmcid validation claim false', (True, False)), ('pmcid validation claim audit', (True, False)), ('documented no pmcid validation claim false', (False, True)), ("doesn't validate-pmcid", (False, True)), ('invalid pmcidly', (False, False))]:
            self.assertEqual(claims(text), expected)
        self.assertEqual(claims(prose('```\nvalidate pmcid\n```\n`pmcid check`')), (True, False))
        self.assertEqual(claims(prose('~~~\nvalidate pmcid\n~~~')), (False, False))

    def test_evidence_routes(self):
        valid = ['import idutils\nidutils.is_pmcid(x)', 'import idutils as iu\niu.is_pmcid(x)', 'from idutils import is_pmcid\nis_pmcid(x)', 'from idutils import is_pmcid as pm\npm(x)', 'obj = factory()\nobj.pmcid_checker(x)']
        for name in GENERIC:
            valid += ['obj.' + name + '(x)', 'from custom import ' + name + ' as route\nroute(x)']
        for source in valid:
            with self.subTest(source=source): self.assertTrue(evidence(source))
        invalid = ['import idutils', 'is_pmcid(x)', 'obj.is_pmcid(x)', 'validate_pmcid(x)', 'pmcid(x)', 'obj.pmcid(x)', 'obj.to_url(x)', 'obj.pmcid_regexp(x)', 'idutils.to_url(x, "pmcid")', 'idutils.normalize_pid(x, "pmcid")', 'idutils.normalize_pmcid(x)', 'idutils.detect_identifier_schemes(x)', 'idutils.pmcid_regexp.match(x)', 'idutils.pmcid_regexp.search(x)', 'validators.pmcid(x)', 'stdnum.pmcid.validate(x)', 'pmcid.validate(x)', 're.match("PMC", x)', 'x.startswith("PMC")', 'x.isdigit()', 'len(x)', 'requests.get(x)', 'subprocess.run(x)', '"validate pmcid"', 'from idutils import *\nis_pmcid(x)', 'import idutils.is_pmcid\nidutils.is_pmcid(x)', 'import idutils as iu\niu = other\niu.is_pmcid(x)', 'import idutils as iu\nwith other as iu:\n iu.is_pmcid(x)', 'from idutils import is_pmcid as p\ndef p(x): pass\np(x)', 'def validate_pmcid(x): pass\nobj.validate_pmcid(x)', 'def broken(:']
        for name in ('is_pmid is_doi is_handle is_ark is_urn is_istc is_cstr is_ror is_openalex is_viaf is_wikidata is_gnd is_hal is_swh is_rrid is_arxiv is_ean is_email is_url is_orcid is_isni is_isbn is_isbn10 is_isbn13 is_issn').split():
            invalid.append('import idutils\nidutils.' + name + '(x)')
        for source in invalid:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_pattern_boundaries(self):
        pattern = re.compile(r'PMC\d+$', flags=re.I)
        for value in ['PMC1234567', 'pmc1234567', 'Pmc1234567', 'PMC1', 'PMC0', 'PMC0000001', 'PMC' + '1' * 40, 'PMC1234567\n']:
            with self.subTest(value=value): self.assertIsInstance(pattern.match(value), re.Match)
        for value in ['PMCID:PMC1234567', 'PMC:1234567', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC1234567/', 'PMC1234567/', 'PMC1234567\n\n', 'PMC1234567\r', 'PMC1234567\r\n', 'PMC 123', ' PMC1', 'PMC1 ', 'PMC1\t', 'PMC1x', 'PMC', '123', 'PMC-1', 'PMC_1', 'PMC1.1', 'PMC1\n2', 'PMC1\u00a0', '', 'garbage']:
            with self.subTest(value=value): self.assertIsNone(pattern.match(value))
        for value in [123, None, b'PMC1']:
            with self.subTest(value=value):
                with self.assertRaises(TypeError): pattern.match(value)

    def test_findings_and_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'README.md').write_text('validate pmcid')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
            (root/'tests').mkdir()
            (root/'tests/test_route.py').write_text('import idutils\nidutils.is_pmcid(x)')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'MEDIUM')
            (root/'src.py').write_text('import idutils\nidutils.is_pmcid(x)')
            self.assertEqual(audit(root)['findings'], [])
            (root/'README.md').write_text('does not validate pmcid')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'HIGH')
            (root/'src.py').unlink()
            self.assertEqual(audit(root)['findings'], [])
            (root/'fixtures').mkdir()
            (root/'fixtures/x.py').write_text('import idutils\nidutils.is_pmcid(x)')
            (root/'docs').mkdir()
            (root/'docs/a.md').write_text('validate pmcid')
            self.assertEqual(audit(root)['findings'][0]['severity'], 'MEDIUM')
            self.assertEqual(audit(root, ['tests', 'docs'])['findings'], [])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'README.md').write_text('validate pmcid')
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(['audit', tmp, '--json']), 2)
            self.assertEqual(json.loads(out.getvalue())['findings'][0]['severity'], 'HIGH')
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exc: main(['bad'])
            self.assertEqual(exc.exception.code, 1)
            with contextlib.redirect_stderr(io.StringIO()): self.assertEqual(main(['audit', tmp + '/missing']), 1)

    def test_self_audit(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(claims(prose((root/'README.md').read_text())), (False, False))
        self.assertEqual(audit(root)['findings'], [])


if __name__ == '__main__':
    unittest.main()
