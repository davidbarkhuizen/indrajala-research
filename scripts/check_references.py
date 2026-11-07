#!/usr/bin/env python3
"""Checks that every reference a document cites exists as cited.

For each key the built document cites (its .aux), the entry is read from the bibliographies
(indrajala-literature's library.bib and extra.bib) and looked up:

- a DOI: Crossref's record for it;
- an arXiv ID (``arXiv:NNNN.NNNNN`` in ``note``, ``eprint`` or ``journal``): arXiv's record for it;
- a URL: the page answers;
- neither: a Crossref bibliographic search on the title and first author.

A record matches when its title equals the entry's (letters and digits, case and accents aside, or a
close match of at least 0.9 for subtitles and punctuation; a record's trailing "(Technical Report)" or
the like is dropped) and the entry's first author's surname is
among the record's authors. Each entry gets one verdict: ``ok``, ``MISMATCH`` (found, but not as cited),
``MISSING`` (the identifier doesn't resolve), or ``manual`` (no identifier and no match by search: a
book, say, to be checked by hand). The exit status is 1 when any entry is MISMATCH or MISSING.

Our own entries (keys starting ``barkhuizen-``) are listed, not looked up.

    scripts/check_references.py papers/learning-transducers-with-proof.aux [more .aux files]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

USER_AGENT = "indrajala-research-reference-check/1.0"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_ID = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})", re.I)
TRAILER = re.compile(r"\s*\((technical report|extended version|full version|long version)\)\s*$", re.I)
LATEX_ACCENT = re.compile(r"\\[\"'`^~=.uvHckrb]\s*\{?\\?([A-Za-z])\}?")


def plain(text: str) -> str:
    """Letters and digits only, lower case, accents and LaTeX markup removed."""
    text = LATEX_ACCENT.sub(r"\1", text)
    text = re.sub(r"\\(DJ|dj)", "dj", text)
    text = re.sub(r"\\[A-Za-z]+", " ", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", text.lower())


def read_bib(paths: list[Path]) -> dict[str, dict[str, str]]:
    """The entries of the .bib files, by key, each a dict of lower-case field names (and ``type``)."""
    entries: dict[str, dict[str, str]] = {}
    for path in paths:
        text = path.read_text()
        for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
            start, depth, i = m.end(), 1, m.end()
            while depth and i < len(text):
                depth += {"{": 1, "}": -1}.get(text[i], 0)
                i += 1
            fields = {"type": m.group(1).lower()}
            body = text[start : i - 1]
            for f in re.finditer(r"(\w+)\s*=\s*", body):
                j, value = f.end(), ""
                if body[j] == "{":
                    depth, k = 1, j + 1
                    while depth:
                        depth += {"{": 1, "}": -1}.get(body[k], 0)
                        k += 1
                    value = body[j + 1 : k - 1]
                elif body[j] == '"':
                    value = body[j + 1 : body.index('"', j + 1)]
                else:
                    value = re.match(r"[^,\n]*", body[j:]).group(0)  # type: ignore[union-attr]
                fields.setdefault(f.group(1).lower(), re.sub(r"\s+", " ", value).strip())
            entries[m.group(2)] = fields
    return entries


def cited_keys(aux: Path) -> list[str]:
    keys: set[str] = set()
    for line in aux.read_text().splitlines():
        if line.startswith("\\citation{"):
            keys.update(k.strip() for k in line[len("\\citation{") : -1].split(","))
    return sorted(keys)


def fetch(url: str) -> bytes:
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if attempt == 3:
                raise
        except urllib.error.URLError:
            if attempt == 3:
                raise
        time.sleep(3 * (attempt + 1))
    raise AssertionError


def crossref_doi(doi: str) -> tuple[str, list[str]]:
    msg = json.loads(fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    return " ".join(msg.get("title", [""])), [a.get("family", a.get("name", "")) for a in msg.get("author", [])]


def crossref_search(title: str, author: str) -> list[tuple[str, list[str]]]:
    q = urllib.parse.urlencode({"query.bibliographic": title, "query.author": author, "rows": 5})
    items = json.loads(fetch("https://api.crossref.org/works?" + q))["message"]["items"]
    return [(" ".join(i.get("title", [""])), [a.get("family", "") for a in i.get("author", [])]) for i in items]


def arxiv(arxiv_id: str) -> tuple[str, list[str]] | None:
    feed = ET.fromstring(fetch("https://export.arxiv.org/api/query?id_list=" + arxiv_id))
    entry = feed.find(ATOM + "entry")
    if entry is None or entry.find(ATOM + "title") is None:
        return None
    title = entry.findtext(ATOM + "title", "")
    names = [a.findtext(ATOM + "name", "") for a in entry.findall(ATOM + "author")]
    return title, [n.split()[-1] if n.split() else n for n in names]


def first_surname(author_field: str) -> str:
    first = re.split(r"\s+and\s+", author_field)[0]
    return first.split(",")[0] if "," in first else first.split()[-1]


def matches(entry: dict[str, str], title: str, surnames: list[str]) -> tuple[bool, str]:
    want, got = plain(entry.get("title", "")), plain(TRAILER.sub("", title))
    ratio = 1.0 if want == got else difflib.SequenceMatcher(None, want, got).ratio()
    surname = plain(first_surname(entry.get("author", "")))
    author_ok = any(surname and (surname in plain(s) or plain(s) in surname) for s in surnames if plain(s))
    if ratio >= 0.9 and author_ok:
        return True, ""
    why = []
    if ratio < 0.9:
        why.append(f"title {ratio:.2f}: {title!r}")
    if not author_ok:
        why.append(f"{first_surname(entry.get('author', ''))!r} not among {surnames[:6]}")
    return False, "; ".join(why)


def check(key: str, entry: dict[str, str]) -> tuple[str, str]:
    if key.startswith("barkhuizen-"):
        return "own", entry.get("doi", entry.get("howpublished", ""))
    if "doi" in entry:
        try:
            title, names = crossref_doi(entry["doi"])
        except urllib.error.HTTPError:
            return "MISSING", "doi " + entry["doi"]
        ok, why = matches(entry, title, names)
        return ("ok", "doi " + entry["doi"]) if ok else ("MISMATCH", "doi " + entry["doi"] + ": " + why)
    m = ARXIV_ID.search(" ".join(entry.get(f, "") for f in ("note", "eprint", "journal")))
    if m:
        record = arxiv(m.group(1))
        time.sleep(3)  # arXiv's API asks for one request every three seconds
        if record is None:
            return "MISSING", "arXiv " + m.group(1)
        ok, why = matches(entry, *record)
        return ("ok", "arXiv " + m.group(1)) if ok else ("MISMATCH", "arXiv " + m.group(1) + ": " + why)
    if "url" in entry:
        try:
            fetch(entry["url"])
        except urllib.error.URLError as e:
            return "MISSING", f"url {entry['url']}: {e}"
        return "ok", "url " + entry["url"] + " (answers; title not compared)"
    for title, names in crossref_search(entry.get("title", ""), first_surname(entry.get("author", ""))):
        if matches(entry, title, names)[0]:
            return "ok", "found by search: " + title
    return "manual", "no identifier, no match by search"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("aux", nargs="+", type=Path, help="the built documents' .aux files")
    parser.add_argument("--literature", type=Path, default=Path("../indrajala-literature"))
    args = parser.parse_args()
    bib = read_bib([args.literature / "library.bib", Path("extra.bib")])
    keys = sorted({k for aux in args.aux for k in cited_keys(aux)})
    counts: dict[str, int] = {}
    for key in keys:
        if key not in bib:
            verdict, detail = "MISSING", "not in the bibliographies"
        else:
            verdict, detail = check(key, bib[key])
        counts[verdict] = counts.get(verdict, 0) + 1
        print(f"{verdict:8} {key}: {detail}", flush=True)
    print(f"{len(keys)} cited: " + ", ".join(f"{n} {v}" for v, n in sorted(counts.items())))
    return 1 if counts.get("MISMATCH") or counts.get("MISSING") else 0


if __name__ == "__main__":
    sys.exit(main())
