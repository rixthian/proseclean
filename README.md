<p align="center">
  <img src="assets/banner.svg" alt="ProseClean: manuscript hygiene for authors" width="100%">
</p>

<p align="center">
  <a href="https://github.com/rixthian/proseclean/actions/workflows/ci.yml"><img src="https://github.com/rixthian/proseclean/actions/workflows/ci.yml/badge.svg" alt="tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-c9953c.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776ab.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/dependencies-none-2ea44f.svg" alt="No dependencies">
  <img src="https://img.shields.io/badge/runs-offline-1e293b.svg" alt="Runs offline">
</p>

<p align="center">
  <b>Keep your prose yours.</b><br>
  A small, free, offline tool that removes hidden characters and chat residue from your writing,<br>
  and flags typical AI phrasing so <i>you</i> decide what stays.
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#what-it-cleans">What it cleans</a> ·
  <a href="#use-it-as-a-library">Library</a> ·
  <a href="#use-it-as-a-claude-skill">Claude skill</a> ·
  <a href="#faq">FAQ</a>
</p>

---

## Why ProseClean

Text that passes through chat tools, web editors and copy-paste can pick up invisible baggage: zero-width characters, odd spaces, hidden Unicode tag characters, broken accents (`â€™`), citation leftovers and template tokens. A reader never sees any of it, but all of it travels with your manuscript, your blog post or your newsletter.

Authors deserve to know exactly what is inside their own text. ProseClean shows you, fixes the mechanical problems, and leaves every creative decision to you.

| Principle | What it means |
|---|---|
| **Never rewrites your words** | Style is a human decision. Wording is only ever *flagged*. |
| **Original is sacred** | Output goes to a new `.clean` file. Your source is never modified. |
| **Transparent** | Every change is counted and reported. |
| **Zero dependencies** | Pure Python standard library. Nothing to install, nothing phoning home. |
| **Offline and deterministic** | Same input, same output, no network. |

## Quick start

```bash
git clone https://github.com/rixthian/proseclean.git
cd proseclean
python3 -m proseclean examples/sample.md
```

```text
examples/sample.md
  fixed   invisible characters removed: 1
  fixed   typography: U+201C -> '"': 1
  fixed   typography: U+201D -> '"': 1
  fixed   typography: U+2026 -> '...': 1
  review  long dashes (review by hand): 1
  review  typical phrase: cabe destacar: 1
  wrote   examples/sample.clean.md
```

Or install the `proseclean` command:

```bash
pip install .
proseclean chapter1.md chapter2.md
```

### Options

| Flag | Effect |
|---|---|
| `--level light` | Invisible characters and residue only. Keeps your typography. |
| `--level standard` | Default. Also normalises typography (curly quotes, ellipsis, odd hyphens). |
| `--report-only` | Show the report, write nothing. |
| `--check` | Exit with code `1` if any file needs cleaning. Made for CI and pre-commit. |

## What it cleans

| Category | Examples | Action |
|---|---|---|
| Invisible characters | zero-width spaces, BOM, soft hyphen, bidirectional overrides, blank filler glyphs | **Removed** |
| Hidden tag characters | Unicode block `U+E0000–E007F` | **Removed** |
| Exotic spaces | narrow no-break space, em space, ideographic space | **Normalised** to a plain space |
| Garbled text | `â€™`, `Ã©` (mojibake) | **Repaired**, only the damaged fragment |
| Chat residue | `【…】` citations, `oai_citation`, `utm_source=chatgpt.com`, `<think>` blocks, `<\|…\|>` tokens | **Removed** |
| Typography *(standard)* | curly quotes, `…`, odd hyphens, `ﬁ` ligatures | **Normalised** |
| Long dashes | `—` `–` | **Flagged only**: legitimate in Spanish dialogue and many literary styles |
| Typical phrases | "cabe destacar", "it is important to note", "delve", "tapestry" | **Flagged only**, never rewritten |

## Use it as a library

```python
from proseclean import clean

text, report = clean(open("chapter1.md", encoding="utf-8").read())
print(report.changes)   # what was fixed
print(report.flags)     # what is left for you to review
```

## Use it as a Claude skill

[`skills/proseclean`](skills/proseclean/SKILL.md) is a ready-made skill. It tells Claude to run the cleaner before delivering any final text, to walk through flagged phrases *with you*, and to keep your own voice.

## Honest limits

ProseClean does one job and says plainly what it does not do.

- It removes hidden characters and visible tics. It **cannot detect or remove statistical watermarks** (for example signals woven into word choice).
- It does **not** protect your work from being copied or used to train AI models. For that, look at licensing and opt-out tools.
- It is deliberately **not** a detector-evasion tool. There is no mass-rewrite mode.

## FAQ

**Will it change my writing?**
No. It removes characters you cannot see and normalises typography. Anything about word choice is only flagged.

**Why are long dashes only flagged?**
In Spanish the dialogue dash is part of correct punctuation, and many authors use dashes deliberately. You decide.

**Does it work on Word or PDF files?**
Not yet. It handles plain text and Markdown. For `.docx`, PDF and metadata, see the project credited below.

**Is anything sent over the network?**
No. It never opens a connection.

## Project

| | |
|---|---|
| [CHANGELOG](CHANGELOG.md) | What changed in each release |
| [CONTRIBUTING](CONTRIBUTING.md) | How to propose changes and add rules |
| [SECURITY](SECURITY.md) | How to report a problem privately |

## Roadmap

- [ ] `.docx` support
- [ ] Pre-commit hook
- [ ] Configurable phrase lists per language

## Credits

The categories of hidden characters and chat residue are informed by the public documentation of [Olib-AI/llm-cleanup](https://github.com/Olib-AI/llm-cleanup) (MIT), a Rust tool that also handles `.docx`, PDF and metadata. If you need those formats today, use it. ProseClean is an independent, minimal Python implementation focused on plain text and Markdown.

## License

[MIT](LICENSE)
