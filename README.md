# Documentation claim audit

An offline audit tool compares documented pubmed-central-identifier claims with calls found in Python source. It parses source without executing it and does not establish whether a record exists.

## Usage

```sh
pmcid-validation-claim-audit audit .
pmcid-validation-claim-audit audit . --json --fail-on medium --ignore vendor/
pmcid-validation-claim-audit --version
python3 -m pmcid_validation_claim_audit audit .
```

The optional path defaults to the current directory. The repeatable ignore option excludes path prefixes. JSON provides findings and scanned paths; verbose output includes counts. Exit status is 0 for a pass, 2 when a finding meets the threshold, and 1 for usage or I/O errors. The default threshold is high; medium also fails on test-only evidence.

## Findings

```
documented-pmcid-validation-claim-false
documented-no-pmcid-validation-claim-false
```

A positive claim without production evidence is high severity, or medium when evidence appears only in tests. A negative claim contradicted by production evidence is high severity. A negative claim without source passes. The scan considers the root README and Markdown under directories named docs, excludes fenced blocks, and treats inline code as prose. It scans Python files statically, excluding symlinks and fixture, example and documentation source from production evidence. Aliases are resolved within a module, with locally shadowed names excluded.

## Evidence

A call to the following library route, or an imported or attribute call with a listed generic name, establishes evidence. A bare name without a resolved import does not. The library returns a match object or None, interpreted by truthiness; it uses the case-insensitive pattern shown below. It never looks up a record.

```text
idutils.is_pmcid
pmcid_regexp = re.compile(r"PMC\d+$", flags=re.I)
validate_pmcid
validates_pmcid
validating_pmcid
pmcid_validation
pmcid_validator
validate_pubmed_central_id
validates_pubmed_central_id
pubmed_central_id_validation
pubmed_central_id_validator
check_pmcid
pmcid_check
pmcid_checker
verify_pmcid
pmcid_verification
is_valid_pmcid
pmcid_is_valid
pmcid_validity
validate_pmcid_format
pmcid_format_validation
pmcid_validation_check
check_pubmed_central_id
pubmed_central_id_check
verify_pubmed_central_id
pubmed_central_id_verification
```

## Matched phrases

```
validate pmcid
validates pmcid
validating pmcid
pmcid validation
pmcid validations
pmcid validator
pmcid validation check
pmcid check
check pmcid
verify pmcid
pmcid verification
pmcid is valid
pmcid is invalid
valid pmcid
invalid pmcid
pmcid validity
pmcid format validation
validate pmcid format
pmcid length validation
pmcid character validation
is valid pmcid
is pmcid valid
pmcid validation library
pmcid validation function
pmcid validation tool
checks pmcid
checking pmcid
verifies pmcid
verifying pmcid
validate pubmed central id
validates pubmed central id
validating pubmed central id
pubmed central id validation
pubmed central id validations
pubmed central id validator
pubmed central id validation check
pubmed central id check
check pubmed central id
verify pubmed central id
pubmed central id verification
pubmed central id is valid
pubmed central id is invalid
valid pubmed central id
invalid pubmed central id
pubmed central id validity
pubmed central id format validation
validate pubmed central id format
is valid pubmed central id
is pubmed central id valid
pubmed central id validation library
no pmcid validation
does not validate pmcid
no pmcid validator
no pmcid validation check
does not support pmcid validation
without pmcid validation
pmcid validation not supported
pmcid validation not available
cannot validate pmcid
cannot check pmcid
does not check pmcid
no pmcid check
does not verify pmcid
no pmcid verification
pmcid validation not implemented
does not validate pmcid format
no pubmed central id validation
does not validate pubmed central id
no pubmed central id validator
pubmed central id validation not supported
cannot validate pubmed central id
does not verify pubmed central id
no pubmed central id verification
pubmed central id validation not implemented
```

Bare terms alone are not claims:

```
pmcid
pubmed central id
pubmed central
pmc.ncbi.nlm.nih.gov
identifier
digits
prefix
suffix
```

## Phrase hazards

```text
validate pmcid
```

The bare phrase above can describe a manual runbook step.

```text
pmcid validation
```

The bare phrase above can describe a roadmap feature.

```text
pmcid validator
```

The bare phrase above can describe a hosted web page.

```text
pmcid check
```

The bare phrase above can describe a field-presence lint rule.

```text
check pmcid
```

The bare phrase above can describe a manual runbook step.

```text
verify pmcid
```

The bare phrase above can describe a visual account confirmation.

```text
pmcid validation check
```

The bare phrase above can describe a field-presence check.

```text
valid pmcid
```

The bare phrase above can appear as example output.

```text
pmcid is valid
```

The bare phrase above can appear as example error text.

```text
pmcid is invalid
```

The bare phrase above can name a configuration flag or column.

```text
pmcid validity
```

The bare phrase above can describe a format without code.

```text
pmcid format validation
```

The bare phrase above can describe a shape-only check.

```text
validate pmcid format
```

The bare phrase above can name a specification section.

```text
validate pubmed central id
```

The bare phrase above can describe a manual runbook step.

```text
pubmed central id validation
```

The bare phrase above can describe a manual runbook step.

```text
check pubmed central id
```

The bare phrase above can describe a manual runbook step.

```text
verify pubmed central id
```

The bare phrase above can name a specification section.

```text
pubmed central id check
```

The bare phrase above can name a reference-data checklist item.

```text
pubmed central id validation check
```

The bare phrase above can describe a result from an external platform.

```text
pubmed central id validator
```

The bare phrase above alone names a string without judging it.

```text
pmcid
```

The bare phrase above alone does not claim a judgement.

```text
pubmed central id
```

The bare phrase above alone does not claim a judgement.

```text
pubmed central
```

The bare phrase above alone does not claim a judgement.

```text
pmc.ncbi.nlm.nih.gov
```

The bare phrase above alone does not claim a judgement.

```text
identifier
```

The bare phrase above alone does not claim a judgement.

```text
digits
```

The bare phrase above alone does not claim a judgement.

```text
prefix
```

The bare phrase above alone does not claim a judgement.

```text
suffix
```

The bare phrase above alone does not claim a judgement.

## Limitations

The library ships no normalisation route for this identifier.

A conversion call builds a resolver address and never judges a string.

A network fetch asks a service for a record and never judges a string.

A direct pattern match is a shape check, not a library judgement.

A Handle call judges a wider namespace and is not recognised.

A DOI call judges a digital object identifier string and is not recognised.

An arXiv call judges a preprint identifier string and is not recognised.

A PMID call judges a bare integer string and is not recognised.

The validators package does not provide the relevant route.

The stdnum package does not provide the relevant route.

Strings, comments, imports and bare references do not establish a call.

Syntax errors prevent source evidence.

Calls split across modules do not combine into evidence.

A subprocess invocation does not count.

Roadmap, changelog and TODO prose can produce claims without implemented code.

The library does not establish registration of any string.

There is no check digit: any all-digit suffix passes.

There is no length limit: a thirty digit suffix passes.

There is no range check: zero passes.

A trailing space fails the shape check.

A trailing newline passes the shape check.

An embedded newline fails the shape check.

A leading space fails the shape check.

A scheme prefix is not accepted: PMCID:PMC1234567 is rejected.

A trailing slash fails: PMC1234567/ is rejected.

An empty string fails the shape check.

Lowercase letters pass: pmc1234567 is accepted.

A resolver form is not accepted: https://pmc.ncbi.nlm.nih.gov/articles/PMC1234567/ is rejected.

A single-character slip in the digits still passes the shape check.

Leading zeroes pass: PMC0000001 is accepted.

A conversion call builds an address from invalid input without judging it.

Non-string input raises TypeError instead of judging.

A single digit passes: PMC1 is accepted.

Two trailing newlines and a trailing carriage return fail the shape check. The scheme classifier returns possible schemes rather than a validity judgement. Direct pattern calls, digit and prefix checks, and unrelated identifier predicates do not count as evidence. The audit is a static heuristic; it cannot establish execution or correctness of a generic call.

## Differentiation

This tool does not cover fetching a PubMed Central record over the network (the fetch family); reading a string out of text or a document (the extraction family); checking whether a string is a well-formed digital object identifier string (the doi family); checking whether a string is a well-formed handle-system string (the handle family); checking whether a string is a well-formed archival resource key (the ark family); checking whether a string is a well-formed uniform resource name (the urn family); checking whether a string is a well-formed preprint identifier string (the arxiv family); checking whether a string is a well-formed bare decimal integer string (the pmid family); checking whether a string is a well-formed text-content string (the istc family); checking whether a string is a well-formed science-resource string (the cstr family); checking whether a string is a well-formed research-organisation string (the ror family); checking whether a string is a well-formed openalex string (the openalex family); checking whether a string is a well-formed authority-file string (the viaf family); checking whether a string is a well-formed wikidata string (the wikidata family); checking whether a string is a well-formed authority record string (the gnd family); checking whether a string is a well-formed archive string (the hal family); checking whether a string is a well-formed software-heritage string (the swh family); checking whether a string is a well-formed research-resource string (the rrid family); checking whether a string is a well-formed six-letter classification string (the cfi family); checking whether a creditor-reference string is well-formed (the creditor-reference family); reading a classification string out of a document (the classification-code-extraction family); looking a string up by its classification code (the classification-code-lookup family); assigning a new classification code to a string (the classification-code-assignment family). The remaining neighbours use the standard wordings (each "checking whether a ... string is well-formed (the ... family)" or the matching action wording): checking whether input is checked at all (the generic validation family), checking whether a book number passes the ISBN-10 / ISBN-13 check digit (the ISBN-validation family), checking whether a serial number passes the ISSN check digit (the ISSN-validation family), checking whether a bank account number passes the IBAN check digit (the IBAN-validation family), checking whether a universally unique identifier string is well-formed (the UUID-validation family), checking whether a version string is a well-formed semantic version (the semver-validation family), checking whether a hardware address string is well-formed (the MAC-address-validation family), checking whether a business identifier code string is well-formed (the BIC-validation family), checking whether a cron-expression string is well-formed (the cron-expression-validation family), turning a cron-expression string into a human-readable sentence (the cron-expression-description family), checking whether anything runs on a schedule (the scheduled-execution family), checking whether a date string is well-formed (the date-validation family), checking whether a call times out (the timeout family), checking whether a payment is processed (the payment-processing family), reading a card number out of a document (the credit-card-extraction family), checking whether a user is authenticated (the auth family), hashing a password (the password-hashing family), generating a password (the password-generation family), encrypting a PDF (the PDF-encryption family), sending an email (the email-sending family), sending a text message (the SMS-sending family), reading data out of a document (the document-extraction family), scanning a barcode (the barcode-scanning family), checking whether an email address is well-formed (the email-validation family), checking whether a phone number is well-formed (the phone-validation family), checking whether a password is strong (the password-strength family), checking whether a document matches a JSON Schema (the JSON-Schema-validation family), checking whether a card number is well-formed (the credit-card-validation family), checking whether a domain name is well-formed (the domain-validation family), checking whether a URL is well-formed (the URL-validation family), checking whether an IP address is well-formed (the IP-validation family), parsing JSON (the JSON-parsing family), matching a regular expression (the regex family), parsing a URL (the URL-parsing family), fetching a URL (the URL-fetching family), resolving a domain name (the DNS family), generating a barcode (the barcode-generation family), reading an account number out of a document (the account-extraction family), reading a vehicle identification number out of a document (the VIN-extraction family), decoding a vehicle identification number (the VIN-decoding family), looking up a vehicle identification number's history (the VIN-history-lookup family), checking whether a hex color string is well-formed (the hex-color-validation family), checking whether a researcher identifier string is well-formed (the ORCID-validation family), checking whether a name identifier string is well-formed (the ISNI-validation family), checking whether a chemical registry number string is well-formed (the CASRN-validation family), checking whether a stock-exchange identifier string is well-formed (the SEDOL-validation family), checking whether a securities identifier string is well-formed (the ISIN-validation family), looking up a securities identifier's record (the ISIN-record-query family), reading a securities identifier out of a document (the ISIN-extraction family), checking whether a security identifier string is well-formed (the CUSIP-validation family — a CUSIP is a 9-character security identifier with a mod-10 check digit, and judging one says nothing about a PMCID), checking whether a device identifier string is well-formed (the IMEI-validation family), checking whether a mobile equipment identifier string is well-formed (the MEID-validation family), checking whether a legacy mobile equipment identifier string is well-formed (the ESN-validation family), checking whether a music number string is well-formed (the ISMN-validation family), checking whether an audiovisual number string is well-formed (the ISAN-validation family), checking whether a release identifier string is well-formed (the GRid-validation family), checking whether a barcode number string is well-formed (the EAN-validation family), checking whether a serial number string is well-formed (the generic-serial-number family), checking whether a financial instrument identifier string is well-formed (the FIGI-validation family), looking up a financial instrument identifier's record (the FIGI-record-query family), reading a financial instrument identifier out of a document (the FIGI-extraction family), checking whether a recording code string is well-formed (the ISRC-validation family), checking whether an Ethereum address string is well-formed (the Ethereum-address-validation family), checking whether a Binance Smart Chain address string is well-formed (the Binance-Smart-Chain-address-validation family), checking whether a Tron address string is well-formed (the Tron-address-validation family), checking whether a Litecoin address string is well-formed (the Litecoin-address-validation family), checking whether a Dogecoin address string is well-formed (the Dogecoin-address-validation family), checking whether a bitcoin address string is well-formed (the bitcoin-address-validation family), checking whether a transaction hash string is well-formed (the transaction-hash-validation family), checking whether a private key string is well-formed (the private-key- validation family), looking up a balance or transactions on a block explorer (the block-explorer family), generating an address (the address-generation family), reading an address out of a document (the address-extraction family), confirming receipt of a payment (the payment-receipt family), reading a spreadsheet (the spreadsheet-reading family), generating a spreadsheet (the spreadsheet-generation family), reading a Word document (the Word-reading family), generating a Word document (the Word-generation family), reading a presentation (the presentation-reading family), generating a presentation (the presentation-generation family), extracting text from a PDF (the PDF-extraction family), generating a PDF (the PDF-generation family), merging PDFs (the PDF-merging family), splitting a PDF (the PDF-splitting family), rotating a PDF (the PDF-rotation family), filling a PDF form (the PDF-form-filling family), watermarking a PDF (the PDF-watermarking family), redacting a PDF (the PDF-redaction family), compressing a PDF (the PDF-compression family), annotating a PDF (the PDF-annotation family), extracting a table (the table-extraction family), reading text from an image (the OCR family), extracting data from a document (the document-data-extraction family), signing a document electronically (the e-signature family), recording a screen (the screen-recording family), generating a video (the video-generation family), generating a QR code (the QR-generation family), generating a barcode (the barcode-generation family), scanning a barcode (the barcode-scanning family), mixing audio (the audio-mixing family), generating audio (the audio-generation family), editing audio (the audio-editing family), separating audio sources (the audio-source-separation family), recognising speech (the speech-recognition family), synthesising speech (the speech-synthesis family), reducing noise (the noise-reduction family), generating music (the music-generation family), transcribing music (the music-transcription family), checking whether a chemical identifier string is well-formed (the InChI family), checking whether a chemical notation string is well-formed (the SMILES family), checking whether a European Community number string is well-formed (the EC-number family), checking whether a United Nations transport number string is well-formed (the UN-transport-number family), looking up a compound in PubChem (the PubChem-query family), checking whether a chemical structure is well-formed (the chemical-structure- validation family), checking whether any other chemical identifier string is well-formed (the other-chemical-identifiers family), reading a container number out of a shipping document (the container-number-reading family), looking up a carrier registration by container number (the carrier-registry family), checking whether a shipowner code is registered (the BIC- shipowner-code family), checking whether a container size-type code is well-formed (the container-size-type family), generating a new container number (the container-number-generation family), checking whether a container number string is well-formed (the ISO-6346-validation family), fetching a library's record from a registry over the network (the library-record-fetching family), registering a new library identifier with an agency (the library-identifier-registration family), cataloguing a library collection or reading a MARC record (the cataloguing family), looking a library up in OCLC or WorldCat (the OCLC-WorldCat family), listing the agencies that issue library identifiers (the library-agency-listing family), checking whether a library-identifier string is well-formed (the ISIL-validation family), checking whether a ship-number string is well-formed (the IMO-validation family), checking whether a maritime mobile identity string is well-formed (the MMSI-validation family), checking whether a hull identification number string is well-formed (the HIN-validation family), checking whether a European vessel number string is well-formed (the ENI-validation family), looking a vessel up in a ship registry (the vessel-registry-lookup family), tracking a vessel by AIS (the AIS-tracking family), looking a ship up by name (the ship-name-lookup family), checking whether a subscriber-identity string is well-formed (the IMSI-validation family), looking a tax identifier up in the EU VIES registry over the network (the VIES-lookup family — a registry query, not a string judgement), looking up the tax rate for a country (the VAT-rate-lookup family), computing tax amounts on an invoice (the tax-calculation family), generating an invoice document (the invoice-generation family), checking whether a tax-identifier string is well-formed (the VATIN-validation family — a VATIN is a country code plus a country-specific identifier, and judging one says nothing about a PMCID), checking whether a SEPA structured creditor reference string is well-formed (the SEPA-creditor- reference family — an RF reference judged by the ISO 11649 check, a different identifier from a PMCID), reading an unstructured invoice or payment reference out of a document (the invoice-reference-extraction family), looking a payment up by its creditor reference (the payment-lookup family — a registry query, not a string judgement), generating a new creditor reference (the creditor-reference-generation family — minting a fresh string never judges an existing one), checking whether a classification code string is well-formed (the financial-instrument- classification family — a six-letter ISO 10962 code judged by a classification table, and judging one says nothing about a PMCID), checking whether a digital object identifier string is well-formed (the digital-object-identifier family — a "10."-prefixed registrant code plus a slash plus a suffix, and judging one says nothing about a PMCID).
