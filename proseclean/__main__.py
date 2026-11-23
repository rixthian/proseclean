"""Command line interface: ``python -m proseclean FILE [options]``."""
from __future__ import annotations

import argparse
import pathlib
import sys

from . import __version__
from .core import clean


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="proseclean",
        description="Remove hidden characters and chat residue from text files. "
        "The original file is never modified.",
    )
    p.add_argument("files", nargs="+", type=pathlib.Path)
    p.add_argument("--level", choices=("light", "standard"), default="standard",
                   help="light = invisible characters only; standard also normalises typography")
    p.add_argument("--report-only", action="store_true", help="show the report, write nothing")
    p.add_argument("--check", action="store_true",
                   help="exit with code 1 if any file needs cleaning (useful in CI)")
    p.add_argument("--version", action="version", version=__version__)
    args = p.parse_args(argv)

    dirty = False
    for path in args.files:
        original = path.read_text(encoding="utf-8")
        cleaned, rep = clean(original, args.level)
        print(f"\n{path}")
        for k, v in rep.changes.items():
            print(f"  fixed   {k}: {v}")
        for k, v in rep.flags.items():
            print(f"  review  {k}: {v}")
        if rep.clean:
            print("  nothing found")
        if cleaned != original:
            dirty = True
            if not (args.report_only or args.check):
                out = path.with_name(f"{path.stem}.clean{path.suffix}")
                out.write_text(cleaned, encoding="utf-8")
                print(f"  wrote   {out}")
    return 1 if (args.check and dirty) else 0


if __name__ == "__main__":
    sys.exit(main())
