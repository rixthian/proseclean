---
name: texto-limpio
description: Clean hidden characters and chat residue from an author's text and flag typical AI phrasing for review, without rewriting the author's voice. Use before delivering any final article, story or chapter.
---

# texto-limpio

Goal: leave the author's text with zero hidden marks and no AI tics, keeping their human voice.

## When to use
Before delivering any final article, story, chapter or post. Also when asked to "clean this", "remove watermarks" or "remove AI traces".

## Steps
1. Save the final text to a `.md` or `.txt` file. Work on a copy, never the original.
2. Run `python3 -m texto_limpio FILE` from the repository root (add `--level light` to keep typography, `--report-only` to write nothing).
3. Read the report. **Fixed** items are mechanical. **Review** items (long dashes, typical phrases) are never changed automatically: go through them one by one with the author. In Spanish the dialogue dash is legitimate.
4. When rewriting a flagged phrase, use the author's own voice, never generic prose.
5. Deliver the clean text with a short plain-language report: what was removed and what is left to decide.

## Limits (say them honestly)
- Cannot detect or remove statistical watermarks such as SynthID.
- Does not protect a text from being copied or used for AI training.
- No detector-evasion or mass-rewrite mode. This is text hygiene, not disguise.
