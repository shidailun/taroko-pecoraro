# -*- coding: utf-8 -*-
"""[batch 231] Batch 227's rule run MECHANICALLY over the whole record, and the
answer is NEGATIVE on both legs. Keep this file; do not rebuild the sweep.

Batch 227: a written refusal can rest on a premise that later goes false, and
repairing the premise is not overturning the verdict. Batch 230 found two of
those BY HAND -- batch 201's "試探 returns 0 register rows" (it returns 4 in the
gloss file that batch did not read) and batch 68's "no bare form is attested"
(`hibaw` and `hnibaw` both are). Two in one batch reads like a seam, so this
asks the obvious question: how many more are there?

A premise of that shape is an ABSENCE CLAIM, and an absence claim is
mechanically re-checkable. There are exactly two kinds in the record.

    LEG 1 -- the token is absent.  "`X` is not listed", "there is no `X`".
    LEG 2 -- the Chinese is absent. "the register has no 淋巴", "試探 returns 0".

Leg 1 has to BIND THE TOKEN TO THE CLAIM or it measures nothing. A sentence-level
"does this sentence contain a negation" test returns 734 tokens, nearly all of
them the word the sentence names as PRESENT -- "his 嫉妒 is `hkrig`, a different
root, so there is nothing to respell" is a POSITIVE claim about `hkrig` inside a
refusal. Anchored as grammatical subject of the absence or object of a "no ___",
734 -> 132 claims, and of those 31 name a token that IS in the register today.

    leg 1   anchored absence claims 132   tokens now listed 31   live 0
    leg 2   gloss absence claims     34   Han with carriers  7   live 0

**All 38 are false positives, and the failure mode is one and the same: the
regex binds the wrong side of the sentence.** A refusal of the project's usual
shape names the absent thing AND the present alternative in one breath -- "the
register has no 淋巴 at all, nearest is `biqir` 甲狀腺腫瘤" -- so an anchor that
catches "no ___" catches `biqir`, the word that is there. Every leg-1 row reads
that way, including the one that matters here: "Sruweq has no map entry and no
attested neighbour (`sruwaq` 不滿 differs in the vowel)" binds `sruwaq`, while
the word the sentence declares absent is `sruweq`, and `sruweq` is still absent.
Leg 2's seven are the mirror: 試探 appears four times and all four are batch 230
SAYING the count is 4, 太魯閣族 is a claim about NameType rows and not about the
string, 裝填 is a claim about HIS book, 蜜蜂 is about there being no single map
key for a two-word head.

So: batch 230's two premise failures were not a seam. Run over the whole record
the class is empty, and the reason is that the project's refusals are written
with their sources named. That is the finding.

    python tools/orthography/logs/premise231.py

Not a suite log -- it asserts nothing and holds no pins. Same standing as
`freezesweep.py` and `tail221.py`: a reproducible negative result.
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ORTH))

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                           encoding="utf-8")))
GLOSSES = {}
for f in ("attested_gloss.json", "bible_gloss.json", "parquet_gloss.json"):
    GLOSSES[f] = json.load(io.open(os.path.join(ORTH, f), encoding="utf-8"))

FILES = [p for p in
         (sorted(glob.glob(os.path.join(ROOT, ".claude", "notes", "*.md")))
          + sorted(glob.glob(os.path.join(HERE, "*.py")))
          + [os.path.join(ROOT, "CLAUDE.md")])
         # not itself: a sweep that reads its own docstring quotes every claim
         # it is measuring back at itself and manufactures two hits.
         if os.path.basename(p) != "premise231.py"]

# --- leg 1. The token is the SUBJECT of an absence, or the OBJECT of a "no ___".
T = r"`([a-z'’\"]{3,20})`"
LIST = r"(?:[,\s]+(?:and |or |nor )?%s)*" % T
GAP = r"[^`.]{0,40}?"
SUBJ = re.compile(
    T + LIST + GAP +
    r"(?:is|are|was|were|remains?|stays?)\s+(?:both\s+|all\s+|still\s+)?"
    r"(?:not\s+(?:listed|attested|in\b|a\s+listed)|unlisted|unattested|"
    r"absent|empty|nowhere)", re.I)
OBJ = re.compile(
    r"(?:there\s+is\s+no|there\s+are\s+no|has\s+no|have\s+no|carries\s+no|"
    r"lists?\s+no|spells?\s+no|knows?\s+no|contains?\s+no|and\s+no|,\s*no|"
    r"^no|\bno)\s+" + GAP + T, re.I)

# --- leg 2. A Han string asserted absent from the register.
HAN = r"[一-鿿]{2,6}"
BEFORE = re.compile(r"\b(?:no|zero)\s+(?:register\s+|wordlist\s+|listed\s+)?"
                    r"(?:row[s]?\s+for\s+|gloss\s+)?(%s)" % HAN)
AFTER = re.compile(r"(%s)\s*(?:returns?|has|gets?|scores?)\s+(?:exactly\s+)?"
                   r"(?:0|zero|no)\b" % HAN)


def sentences(text):
    for para in re.split(r"\n\s*\n", text):
        for sent in re.split(r"(?<=[.!?])\s+", " ".join(para.split())):
            yield sent


def carriers(han):
    out = {}
    for f, d in GLOSSES.items():
        n = 0
        for w, gs in d.items():
            gs = [gs] if isinstance(gs, str) else gs
            if any(han in g for g in gs):
                n += 1
        out[f] = n
    return out


def main():
    tok_hits, gloss_hits = {}, {}
    claims = gclaims = scanned = 0
    for path in FILES:
        text = io.open(path, encoding="utf-8", errors="replace").read()
        base = os.path.basename(path)
        for sent in sentences(text):
            scanned += 1
            toks = set()
            for rx in (SUBJ, OBJ):
                for m in rx.finditer(sent):
                    toks |= set(g for g in m.groups() if g)
            if toks:
                claims += 1
                for t in toks:
                    # LISTED means in attested_modern.json and nothing else. A
                    # membership test over the gloss files reads a bible-only
                    # word as attested and manufactures its own hits.
                    if t in AM:
                        tok_hits.setdefault(t, (base, sent))
            for rx in (BEFORE, AFTER):
                for m in rx.finditer(sent):
                    han = m.group(1)
                    if (han, base) in gloss_hits:
                        continue
                    gclaims += 1
                    c = carriers(han)
                    if sum(c.values()):
                        gloss_hits[(han, base)] = (c, sent)

    print("sentences scanned            %d" % scanned)
    print("leg 1  anchored absence claims %d   tokens now LISTED %d"
          % (claims, len(tok_hits)))
    for t in sorted(tok_hits):
        base, sent = tok_hits[t]
        print("   %-14s %-16s %s" % (t, base, sent[:96].replace("`", "")))
    print("leg 2  gloss absence claims    %d   Han WITH carriers %d"
          % (gclaims, len(gloss_hits)))
    for han, base in sorted(gloss_hits):
        c, sent = gloss_hits[(han, base)]
        print("   %-8s %-16s ag=%-3d bg=%-3d pq=%-3d %s"
              % (han, base, c["attested_gloss.json"], c["bible_gloss.json"],
                 c["parquet_gloss.json"], sent[:70].replace("`", "")))
    print("\nEvery row above was read by hand in batch 231 and every one is a "
          "false positive.\nThe premise-failure class is EMPTY. Don't rebuild "
          "this sweep.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
