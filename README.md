# texto-limpio

**Keep your prose yours.** A small, free, offline tool that removes hidden characters and chat residue from your writing, and flags typical AI phrasing so *you* decide what stays.

No dependencies. One Python package. Your original file is never touched.

---

## Why this exists

Text copied through chat tools and editors can carry invisible baggage: zero-width characters, odd spaces, hidden Unicode tag characters, broken accents (`â€™`), citation leftovers and template tokens. None of it is visible to a reader, but all of it travels with your manuscript, your blog post or your newsletter.

Authors deserve to know exactly what is inside their own text. This tool shows you, fixes the mechanical problems, and leaves every creative decision to you.

## What it does

| Kind | Examples | Action |
|---|---|---|
| Invisible characters | zero-width spaces, BOM, soft hyphen, bidirectional overrides, blank filler glyphs | **Removed** |
| Hidden tag characters | Unicode block `U+E0000–E007F` | **Removed** |
| Exotic spaces | narrow no-break space, em space, ideographic space | **Normalised** to a plain space |
| Garbled text | `â€™`, `Ã©` (mojibake) | **Repaired**, only the damaged fragment |
| Chat residue | `【…】` citations, `oai_citation`, `utm_source=chatgpt.com`, `<think>` blocks, `<\|…\|>` tokens | **Removed** |
| Typography *(standard level)* | curly quotes, `…`, odd hyphens, `ﬁ` ligatures | **Normalised** |
| Long dashes | `—` `–` | **Flagged only**: in Spanish and many literary styles they are legitimate |
| Typical phrases | "cabe destacar", "it is important to note", "delve", "tapestry" | **Flagged only**, never rewritten |

**Design rule:** the tool never rewrites your wording. Style is a human decision.

## Install and use

```bash
git clone https://github.com/<your-user>/texto-limpio.git
cd texto-limpio
python3 -m texto_limpio examples/sample.md
```

```
examples/sample.md
  fixed   invisible characters removed: 1
  fixed   typography: U+201C -> '"': 1
  fixed   typography: U+201D -> '"': 1
  fixed   typography: U+2026 -> '...': 1
  review  long dashes (review by hand): 1
  review  typical phrase: cabe destacar: 1
  wrote   examples/sample.clean.md
```

Options:

```
--level light       invisible characters only (keeps your typography)
--level standard    default: also normalises typography
--report-only       show the report, write nothing
--check             exit 1 if a file needs cleaning (for CI or pre-commit)
```

Use it as a library:

```python
from texto_limpio import clean

text, report = clean(open("chapter1.md", encoding="utf-8").read())
print(report.changes, report.flags)
```

## Use it as a Claude skill

The folder [`skills/texto-limpio`](skills/texto-limpio/SKILL.md) contains a ready-made skill. It tells Claude to run this cleaner before delivering any final text, review the flagged phrases *with you*, and keep your own voice.

## Honest limits

- It removes hidden characters and visible tics. It **cannot detect or remove statistical watermarks** (for example SynthID-style signals woven into word choice).
- It does **not** protect your work from being copied or used to train AI models. For that, look at licensing and opt-out tools.
- It is deliberately **not** a detector-evasion tool. There is no mass-rewrite mode.

## Credits

The categories of hidden characters and chat residue are informed by the public documentation of [Olib-AI/llm-cleanup](https://github.com/Olib-AI/llm-cleanup) (MIT), a Rust tool that also handles `.docx`, PDF and metadata. If you need those formats, use it. This project is an independent, minimal Python implementation focused on plain text and Markdown.

## Roadmap

- `.docx` support
- Pre-commit hook
- Configurable phrase lists per language

## License

MIT. See [LICENSE](LICENSE).
