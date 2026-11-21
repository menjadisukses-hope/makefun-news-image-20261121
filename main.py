#!/usr/bin/env python3
"""Entrypoint for the News Image 21 Nov 2026 entry.

The grader runs this file. Its whole job is to take the finished front
page (news.png, which lives beside this script in the repository) and
place a copy at the fixed location the grader reads: /output/entry.png.
Only the Python standard library is used.
"""

import shutil
from pathlib import Path

OUTPUT_DIR = Path("/output")
OUTPUT_NAME = "entry.png"
SOURCE_NAME = "news.png"


def produce_entry() -> Path:
    """Copy the front page next to this script into /output/entry.png."""
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        raise SystemExit(f"missing source image: {source}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / OUTPUT_NAME
    shutil.copyfile(source, target)
    return target


def main() -> None:
    written = produce_entry()
    size = written.stat().st_size
    print(f"Wrote {written} ({size} bytes) from {SOURCE_NAME}")


if __name__ == "__main__":
    main()
