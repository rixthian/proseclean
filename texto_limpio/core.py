"""Core cleaning rules.

Every rule is plain data, so it is easy to read, audit and extend.
The cleaner never rewrites wording: it removes hidden characters and
normalises typography, and it only *flags* style patterns for a human.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# --- Invisible characters: always removed -----------------------------------
INVISIBLES = (
    "​‌‍⁠﻿­"            # zero-width, BOM, soft hyphen
    "⁡⁢⁣⁤"                        # invisible math operators
    "ㅤﾠ⠀"                              # blank filler glyphs
    "‪‫‬‭‮"                  # bidi embeddings / overrides
    "⁦⁧⁨⁩"                        # bidi isolates
)
EXOTIC_SPACES = (
    "         "
    "     　"
)
TAG_CHARS = re.compile("[\U000e0000-\U000e007f]")        # Unicode "tag" smuggling block
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# --- Typography: normalised at the "standard" level -------------------------
TYPOGRAPHY = {
    "‘": "'", "’": "'", "ʼ": "'", "ʹ": "'",
    "“": '"', "”": '"', "″": '"',
    "…": "...", "‥": "..",
    "‐": "-", "‑": "-", "‒": "-", "−": "-",
    "ﬁ": "fi", "ﬂ": "fl",
}

# --- Chat residue: removed ---------------------------------------------------
RESIDUE = [
    ("citation brackets", re.compile(r"【[^】]*】")),
    ("oai_citation", re.compile(r"\(?\boai_citation[^)\s]*\)?")),
    ("utm_source=chatgpt", re.compile(r"[?&]utm_source=chatgpt\.com")),
    ("<think> block", re.compile(r"<think>.*?</think>", re.S)),
    ("chat template token", re.compile(r"<\|[^|>]{1,40}\|>")),
]

# --- Style patterns: flagged only, never rewritten ---------------------------
FLAGGED_PHRASES = [
    r"cabe destacar", r"es importante (?:señalar|destacar|notar)",
    r"en el panorama (?:actual|de)", r"un testimonio de", r"se adentra en",
    r"tapiz de", r"sin lugar a dudas",
    r"it is important to note", r"\bdelve\b", r"\btapestry\b",
    r"in today's", r"navigating the", r"\[Your Name\]", r"\[Tu nombre\]",
]
DASHES = "—–"  # flagged: in Spanish the dialogue dash is legitimate

_MOJIBAKE = re.compile(
    "(?:â€[\u0080-ÿ‘-›Œ-™]?"
    "|Ã[\u0080-¿‘-™])+"
)


@dataclass
class Report:
    changes: dict[str, int] = field(default_factory=dict)
    flags: dict[str, int] = field(default_factory=dict)

    def _add(self, key: str, n: int) -> None:
        if n:
            self.changes[key] = self.changes.get(key, 0) + n

    @property
    def clean(self) -> bool:
        return not self.changes and not self.flags


def _repair_mojibake(match: re.Match) -> str:
    try:
        return match.group(0).encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return match.group(0)


def clean(text: str, level: str = "standard") -> tuple[str, Report]:
    """Return ``(cleaned_text, report)``. ``level`` is ``light`` or ``standard``."""
    if level not in ("light", "standard"):
        raise ValueError("level must be 'light' or 'standard'")
    rep = Report()

    fixed = _MOJIBAKE.sub(_repair_mojibake, text)
    if fixed != text:
        rep._add("garbled characters repaired", 1)
        text = fixed

    rep._add("invisible characters removed", sum(text.count(c) for c in INVISIBLES))
    text = text.translate({ord(c): None for c in INVISIBLES})

    rep._add("hidden tag characters removed", len(TAG_CHARS.findall(text)))
    text = TAG_CHARS.sub("", text)

    rep._add("exotic spaces normalised", sum(text.count(c) for c in EXOTIC_SPACES))
    text = text.translate({ord(c): " " for c in EXOTIC_SPACES})

    rep._add("control characters removed", len(CONTROL_CHARS.findall(text)))
    text = CONTROL_CHARS.sub("", text)

    for name, pattern in RESIDUE:
        text, n = pattern.subn("", text)
        rep._add(f"chat residue: {name}", n)

    if level == "standard":
        for src, dst in TYPOGRAPHY.items():
            n = text.count(src)
            if n:
                rep._add(f"typography: U+{ord(src):04X} -> {dst!r}", n)
                text = text.replace(src, dst)

    dashes = sum(text.count(c) for c in DASHES)
    if dashes:
        rep.flags["long dashes (review by hand)"] = dashes
    for pattern in FLAGGED_PHRASES:
        n = len(re.findall(pattern, text, flags=re.I))
        if n:
            rep.flags[f"typical phrase: {pattern}"] = n
    if any(unicodedata.category(c) in ("Cf", "Co") for c in text):
        rep.flags["other invisible or private-use characters"] = 1

    return text, rep
