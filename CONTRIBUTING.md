# Contributing

Thank you for helping authors keep their text clean.

## Ground rules

1. **Never rewrite wording automatically.** Hidden characters and typography may be fixed. Word choice and style may only be flagged.
2. **No detector-evasion features.** ProseClean is text hygiene, not disguise.
3. **No dependencies and no network access.**
4. **Every rule needs a test.**

## Set up

```bash
git clone https://github.com/rixthian/proseclean.git
cd proseclean
python3 -m unittest discover -s tests -v
```

Python 3.11 or newer.

## Adding a rule

All rules live in [`proseclean/core.py`](proseclean/core.py) as plain data:

- `INVISIBLES`, `EXOTIC_SPACES`: characters removed or normalised.
- `TYPOGRAPHY`: replacements applied at the `standard` level.
- `RESIDUE`: patterns of chat leftovers that are removed.
- `FLAGGED_PHRASES`: patterns that are reported but never changed.

Add the rule, add a test in `tests/test_core.py`, update `CHANGELOG.md`, and open a pull request describing the real-world text that motivated it.

## Reporting a bug

Open an issue with a **small** text sample that reproduces it. Please do not paste private manuscripts.
