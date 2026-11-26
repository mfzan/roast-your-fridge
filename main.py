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


def main() -> int:
    line = ROAST.strip()
    if len(line) > MAX_CHARS:
        print(
            f"error: roast line is {len(line)} characters, "
            f"over the {MAX_CHARS}-character limit",
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")

    # The grader collects outputs as another user, so the file must be
    # world-readable. (Never chmod the output directory itself.)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
