#!/usr/bin/env python3
"""Convert `pdftotext -layout` output of a bylaws PDF into line-per-clause Markdown.

Output conventions (what the diff/merge tooling relies on):
  # <Document title>
  ## Article N – Title
  ### Sec. N. Title          (section heading; body follows on its own line)
  one paragraph, list item, or proviso per line; blank line between blocks.

Heuristic, not magic: every import must be reviewed against the source.
Usage: bylaws2md.py raw.txt --title "..." [--source URL] [--adopted "..."] > bylaws.md
"""
import argparse
import re
import sys

ARTICLE = re.compile(r"^(?i:article)\s+([IVXLC]+|\d+)\s*[–—:.-]?\s*(.*)$")
SECTION = re.compile(r"^(Sec\.|(?i:section))\s+(\d+[A-Za-z]?)\.?\s+(.*)$")
ITEM = re.compile(r"^(\([a-z0-9]{1,4}\)|[a-z]\)|\d+\.)\s+")
PAGENUM = re.compile(r"^\s*\d{1,3}\s*$")
END_MARK = re.compile(r"^\s*#{3}\s*$")
SENTENCE_END = re.compile(r"[.:;”\"]$")


def section_title(rest):
    """Split 'Classes of Membership. There shall...' into (title, body) if it looks titled."""
    m = re.match(r"^([A-Z][^.]{0,60}?)\.\s+(.*)$", rest)
    if m and len(m.group(1).split()) <= 6:
        return m.group(1), m.group(2)
    return None, rest


def blocks(lines):
    """Yield logical blocks (joined paragraphs) from layout text."""
    cur = []
    prev_blank = False
    for raw in lines:
        line = raw.replace("\f", "").rstrip()
        if END_MARK.match(line):
            break
        if PAGENUM.match(line) and line.strip():
            continue  # page footer; may sit mid-paragraph
        text = line.strip()
        if not text:
            prev_blank = True
            continue
        starts_new = bool(ARTICLE.match(text) or SECTION.match(text) or ITEM.match(text)
                          or re.match(r"^Provisos?:?$", text))
        heading_done = len(cur) == 1 and ARTICLE.match(cur[0])
        if cur and (starts_new or heading_done or (prev_blank and SENTENCE_END.search(cur[-1]))):
            yield join(cur)
            cur = []
        cur.append(text)
        prev_blank = False
    if cur:
        yield join(cur)


def join(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p if out.endswith("-") and not out.endswith(" -") else out + " " + p
    return re.sub(r"\s+", " ", out)


# Abbreviations whose trailing period does not end a sentence.
ABBREV = re.compile(r"(?:\b(?:Sec|Art|Arts|No|Nos|St|Mr|Mrs|Ms|Dr|Inc|Co|Comm|vs|v|etc|e\.g|i\.e)|\b[A-Z]\.[A-Z])\.$")


def split_sentences(par):
    """One sentence per line. Markdown renders consecutive lines as one paragraph,
    so this changes nothing visually but lets git merge edits to different sentences."""
    out, start = [], 0
    for m in re.finditer(r"[.?!][”\"]?\s+(?=[A-Z“\"(])", par):
        head = par[start:m.start() + 1]
        if ABBREV.search(head):
            continue
        out.append(par[start:m.end()].rstrip())
        start = m.end()
    out.append(par[start:])
    return "\n".join(s for s in out if s)


def convert(lines, title):
    out = [f"# {title}", ""]
    started = False
    for b in blocks(lines):
        a = ARTICLE.match(b)
        if a:
            started = True
            name = a.group(2).strip()
            out += [f"## Article {a.group(1)}" + (f" – {name}" if name else ""), ""]
            continue
        if not started:
            continue  # cover/title lines before Article I
        if re.match(r"^Provisos?:?$", b):
            out += ["## Provisos", ""]
            continue
        s = SECTION.match(b)
        if s:
            t, body = section_title(s.group(3))
            out += [f"### Sec. {s.group(2)}." + (f" {t}" if t else ""), ""]
            if body:
                out += [split_sentences(body), ""]
            continue
        out += [b if ITEM.match(b) and len(b) < 200 else split_sentences(b), ""]
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--title", required=True)
    ap.add_argument("--source", default="")
    ap.add_argument("--adopted", default="")
    a = ap.parse_args()
    with open(a.raw, encoding="utf-8") as f:
        body = convert(f.read().splitlines(), a.title)
    fm = ["---", f"title: {a.title}"]
    if a.source:
        fm.append(f"source: {a.source}")
    if a.adopted:
        fm.append(f"adopted: {a.adopted}")
    fm.append("---")
    sys.stdout.write("\n".join(fm) + "\n\n" + body)
