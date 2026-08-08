# -*- coding: utf-8 -*-
"""Batch 231 — re-measure the ABSENCE claims the written refusals rest on.

Batch 227's rule, run mechanically: a refusal can rest on a premise that later
goes false, and repairing the premise is not overturning the verdict. Batch 230
found two rulings that way BY HAND — batch 201's "試探 returns 0 register rows"
(it returns 4) and batch 68's "no bare form is attested" (five are).

Both premises are the same shape: an assertion that some WORD is not in the
register. That is mechanically checkable.

THE INSTRUMENT HAS TO BIND THE TOKEN TO THE CLAIM. A sentence-level "does this
sentence contain a negation" test returns 734 tokens, nearly all of them the
word the sentence names as PRESENT ("his 嫉妒 is `hkrig`, a different root, so
there is nothing to respell"). The token must be the grammatical subject of the
absence, or the object of a "no ___". Anchored that way the same corpus returns
a list short enough to read.

Prints verdicts only, never card bodies."""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ORTH = "tools/orthography"

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                           encoding="utf-8")))
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
BG = json.load(io.open(os.path.join(ORTH, "bible_gloss.json"), encoding="utf-8"))

T = r"`([a-z'’\"]{3,20})`"
LIST = r"(?:[,\s]+(?:and |or |nor )?%s)*" % T          # `a`, `b` and `c`
GAP = r"[^`.]{0,40}?"                                  # no other token between

# The token is the SUBJECT of the absence.
SUBJ = re.compile(
    T + LIST + GAP +
    r"(?:is|are|was|were|remains?|stays?)\s+(?:both\s+|all\s+|still\s+)?"
    r"(?:not\s+(?:listed|attested|in\b|a\s+listed)|unlisted|unattested|"
    r"absent|empty|nowhere)", re.I)
# The token is the OBJECT of an existential negation.
OBJ = re.compile(
    r"(?:there\s+is\s+no|there\s+are\s+no|has\s+no|have\s+no|carries\s+no|"
    r"lists?\s+no|spells?\s+no|knows?\s+no|contains?\s+no|and\s+no|,\s*no|"
    r"^no|\bno)\s+" + GAP + T, re.I)

FILES = (glob.glob(".claude/notes/*.md") + glob.glob(ORTH + "/logs/*.py")
         + ["CLAUDE.md"])


def sentences(text):
    for para in re.split(r"\n\s*\n", text):
        s = " ".join(para.split())
        for sent in re.split(r"(?<=[.!?])\s+", s):
            yield sent


def listed(w):
    if w in AG:
        return "attested_gloss", AG[w]
    if w in BG:
        return "bible_gloss", BG[w]
    if w in AM:
        return "attested_modern", []
    return None, None


hits, claims, scanned = {}, 0, 0
for path in FILES:
    text = io.open(path, encoding="utf-8", errors="replace").read()
    for sent in sentences(text):
        scanned += 1
        toks = set()
        for rx in (SUBJ, OBJ):
            for m in rx.finditer(sent):
                toks |= set(g for g in m.groups() if g)
        if not toks:
            continue
        claims += 1
        for t in toks:
            where, gloss = listed(t)
            if where:
                hits.setdefault(t, (os.path.basename(path), where, gloss, sent))

print("sentences %d   anchored absence claims %d   tokens now LISTED %d"
      % (scanned, claims, len(hits)))
print()
for t in sorted(hits):
    path, where, gloss, sent = hits[t]
    if isinstance(gloss, str):
        gloss = [gloss]
    print("%-14s %-16s %-15s %s" % (t, where, path,
                                    ";".join(gloss)[:34] or "(no gloss)"))
io.open(".scratch/b231/premise.txt", "w", encoding="utf-8").write(
    "\n\n".join("%s [%s] %s\n%s" % (t, hits[t][1], hits[t][0], hits[t][3])
                for t in sorted(hits)))
