# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-23

### Added
- Removal of invisible characters, hidden Unicode tag characters and control characters.
- Normalisation of exotic spaces.
- Targeted repair of garbled text (mojibake) without touching neighbouring text.
- Removal of chat residue: citation brackets, `oai_citation`, `utm_source=chatgpt.com`, `<think>` blocks, template tokens.
- Typography normalisation at the `standard` level.
- Review flags for long dashes and typical AI phrasing (never rewritten).
- Command line interface with `--level`, `--report-only` and `--check`.
- Python API: `proseclean.clean`.
- Claude skill in `skills/proseclean`.
- Test suite and continuous integration.
