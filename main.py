#!/usr/bin/env python3
"""Roast Your Fridge: one-line roast writer.

Writes a single roast line about a fridge's crisper drawer to
``<OUTPUT_DIR>/entry.txt``. The line is the whole entry: nothing else
is written to the file, and the program refuses to run if the line
would break the competition's 200-character limit.
"""

import os
import stat
import sys

os.umask(0o022)

MAX_CHARS = 200

ROAST = (
    "My fridge's crisper drawer is where vegetables go to file for "
    "witness protection \u2014 nobody has seen a carrot come out alive."
)

# World-readable file: the grader collects outputs as another user.
FILE_MODE = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH


def validate_line(line: str) -> str:
    """Trim the line and enforce the competition's character limit."""
    cleaned = line.strip()
    if not cleaned:
        raise ValueError("roast line is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            f"roast line is {len(cleaned)} characters, "
            f"over the {MAX_CHARS}-character limit"
        )
    if "\n" in cleaned:
        raise ValueError("roast line must be a single line")
    return cleaned


def write_entry(line: str, output_dir: str) -> str:
    """Write the single roast line to entry.txt and return its path."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    # The grader collects outputs as another user, so the file must be
    # world-readable. (Never chmod the output directory itself.)
    os.chmod(path, FILE_MODE)
    return path


def main() -> int:
    try:
        line = validate_line(ROAST)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    write_entry(line, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
