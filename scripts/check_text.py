#!/usr/bin/env python3
"""Checks a built PDF's text for what must never reach a reader: a draft note, a to-do, an assistant's remark.

The PDF's text comes from ``pdftotext``. A line is flagged when it holds a draft note as the papers'
``\\draftnote`` prints it (``[Draft:``), ``TODO``, ``FIXME``, ``XXX``, a ``??`` left by an undefined
reference, or a phrase an assistant says to its user rather than a paper to its reader. The exit status
is 1 when any line is flagged.

    scripts/check_text.py papers/learning-transducers-with-proof.pdf [more PDFs]
"""

from __future__ import annotations

import re
import subprocess
import sys

FLAGS = [
    r"\[Draft:",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bXXX\b",
    r"\?\?",
    r"\bas an AI\b",
    r"\blanguage model,? I\b",
    r"\bI hope this helps\b",
    r"\bwould you like me to\b",
    r"\blet me know if\b",
    r"\bhere is (a|an|the) (revised|updated|summary|draft)\b",
    r"\bcertainly[,!]",
    r"\bsure[,!] here\b",
    r"\bI'?d be happy to\b",
    r"\bknowledge cutoff\b",
]
PATTERN = re.compile("|".join(FLAGS), re.I)


def main() -> int:
    flagged = 0
    for pdf in sys.argv[1:]:
        text = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
        hits = [(n, line.strip()) for n, line in enumerate(text.splitlines(), 1) if PATTERN.search(line)]
        for n, line in hits:
            print(f"{pdf}:{n}: {line}")
        print(f"{pdf}: {len(hits)} flagged")
        flagged += len(hits)
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
