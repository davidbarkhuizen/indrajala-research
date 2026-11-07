#!/usr/bin/env python3
"""Builds an arXiv source package for a released document, from its release tag.

    scripts/arxiv_package.py TAG SOURCE.tex OUT_DIR [--literature ../indrajala-literature] [--compare RELEASED.pdf]

1. The source is taken from the tag (``git show TAG:SOURCE.tex``), never from the working tree, and the
   bibliographies as they were then: ``extra.bib`` at the tag, and ``library.bib`` at indrajala-literature's
   last commit before the tag's commit time. So the package is the released text, not today's.
2. Comments are stripped: a whole-line comment goes; a trailing comment keeps its ``%`` (which joins
   the line to the next) and loses the text after it. A ``%`` escaped as ``\\%`` is text.
3. The stripped source is built with ``pdflatex``, ``bibtex``, ``pdflatex`` twice, in an empty directory,
   to make its ``.bbl``.
4. **The package** (``NAME.tex`` and ``NAME.bbl``) is then built alone, in another empty directory,
   with ``pdflatex`` twice and no ``bibtex``, as arXiv will; any undefined reference or citation, or a
   LaTeX error, fails it.
5. With ``--compare``, the package's PDF text (``pdftotext``) must equal the released PDF's, word for
   word; the first difference is shown otherwise.

Writes ``OUT_DIR/NAME.tar.gz`` (the package), ``OUT_DIR/NAME.pdf`` (what it builds) and
``OUT_DIR/NAME.sha256``; the package is byte-reproducible (no timestamps or owners in it). OUT_DIR must
not exist (nothing is overwritten).
"""

from __future__ import annotations

import argparse
import difflib
import gzip
import hashlib
import re
import subprocess
import sys
import tarfile
from pathlib import Path


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def git(*args: str, repo: Path = Path(".")) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def strip_comments(tex: str) -> str:
    out = []
    for line in tex.splitlines():
        cut = None
        i = 0
        while i < len(line):
            if line[i] == "\\":
                i += 2
                continue
            if line[i] == "%":
                cut = i
                break
            i += 1
        if cut is None:
            out.append(line)
        elif line[:cut].strip() == "":
            continue  # a whole-line comment: its newline was eaten anyway
        else:
            out.append(line[: cut + 1])
    return "\n".join(out) + "\n"


def latex(name: str, cwd: Path) -> None:
    result = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"], cwd, check=False)
    if result.returncode:
        sys.exit(f"pdflatex failed in {cwd}:\n" + result.stdout[-3000:])


def words(pdf: Path) -> list[str]:
    text = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    return text.split()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tag")
    parser.add_argument("source", help="the .tex file's path in the repository")
    parser.add_argument("out", type=Path)
    parser.add_argument("--literature", type=Path, default=Path("../indrajala-literature"))
    parser.add_argument("--compare", type=Path, help="the released PDF, whose text the package must reproduce")
    args = parser.parse_args()

    args.out = args.out.resolve()
    if args.out.exists():
        sys.exit(f"{args.out} exists; choose a new directory")
    name = Path(args.source).stem
    build, alone = args.out / "build", args.out / "alone"
    build.mkdir(parents=True)
    alone.mkdir()

    when = git("log", "-1", "--format=%cI", args.tag).strip()
    lit_rev = git("rev-list", "-1", "--before=" + when, "HEAD", repo=args.literature).strip()
    (build / "library.bib").write_text(git("show", f"{lit_rev}:library.bib", repo=args.literature))
    (build / "extra.bib").write_text(git("show", f"{args.tag}:extra.bib"))
    tex = strip_comments(git("show", f"{args.tag}:{args.source}"))
    (build / f"{name}.tex").write_text(tex)
    print(f"{name}: {args.tag} ({when}), indrajala-literature {lit_rev[:7]}")

    latex(name, build)
    bib = run(["bibtex", name], build, check=False)
    if bib.returncode > 1:  # 1 is warnings only; they're shown, and --compare judges the result
        sys.exit("bibtex:\n" + bib.stdout)
    for line in bib.stdout.splitlines():
        if line.startswith("Warning--"):
            print("bibtex " + line)
    latex(name, build)

    (alone / f"{name}.tex").write_text(tex)
    (alone / f"{name}.bbl").write_text((build / f"{name}.bbl").read_text())
    latex(name, alone)
    latex(name, alone)
    log = (alone / f"{name}.log").read_text(errors="replace")
    if re.search(r"There were undefined (references|citations)|Citation .* undefined|Reference .* undefined", log):
        sys.exit(f"{alone / name}.log: undefined references or citations")
    if "Rerun to get" in log:
        sys.exit(f"{alone / name}.log: still asks for a rerun after two passes")

    package = args.out / f"{name}.tar.gz"
    with open(package, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for f in (f"{name}.tex", f"{name}.bbl"):
                info = tar.gettarinfo(alone / f, arcname=f)
                info.mtime, info.uid, info.gid, info.uname, info.gname, info.mode = 0, 0, 0, "", "", 0o644
                with open(alone / f, "rb") as fh:
                    tar.addfile(info, fh)
    pdf = args.out / f"{name}.pdf"
    pdf.write_bytes((alone / f"{name}.pdf").read_bytes())
    sums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in (package, pdf))
    (args.out / f"{name}.sha256").write_text(sums)
    pages = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", str(pdf)], args.out).stdout)
    print(f"{package}: {package.stat().st_size} bytes; {pdf.name}: {pages.group(1) if pages else '?'} pages")

    if args.compare:
        ours, theirs = words(pdf), words(args.compare)
        if ours != theirs:
            diff = difflib.unified_diff(theirs, ours, "released", "package", n=8, lineterm="")
            print("\n".join(list(diff)[:60]))
            sys.exit(f"the package's text differs from {args.compare}")
        print(f"text equal to {args.compare}: {len(ours)} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
