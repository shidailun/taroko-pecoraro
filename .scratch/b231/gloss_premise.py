# -*- coding: utf-8 -*-
"""Batch 231, leg 2 — the GLOSS-side absence claims.

Leg 1 asked whether a word the record calls unlisted is listed today: seven
candidates, all seven false positives of a different kind (absent from
verified.js, absent from SYN, absent from HIS book, absent from the cache). The
register-absence premise class has no live row.

But that is not the shape that failed in batch 230. Batch 201 refused the SPUNG
card because 試探 "returns 0 register rows" — a claim about a Chinese GLOSS, not
about a Truku token, and false because it had searched one gloss file of three.
That shape is checkable too: harvest every sentence that asserts a Han string is
absent from the register, and count its carriers across all three gloss files.

Prints verdicts only."""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ORTH = "tools/orthography"

GLOSSES = {}
for f in ("attested_gloss.json", "bible_gloss.json", "parquet_gloss.json"):
    d = json.load(io.open(os.path.join(ORTH, f), encoding="utf-8"))
    GLOSSES[f] = d

HAN = r"[一-鿿]{2,6}"
# The absence phrases the record uses about a gloss, with the Han string on
# either side: "no 斑鳩 at all", "試探 returns 0", "there is no 溢滿 in it",
# "zero rows for 犁田", "the register has no 淋巴".
BEFORE = re.compile(r"\b(?:no|zero)\s+(?:register\s+|wordlist\s+|listed\s+)?"
                    r"(?:row[s]?\s+for\s+|gloss\s+)?(%s)" % HAN)
AFTER = re.compile(r"(%s)\s*(?:returns?|has|gets?|scores?)\s+(?:exactly\s+)?"
                   r"(?:0|zero|no)\b" % HAN)
FILES = (glob.glob(".claude/notes/*.md") + glob.glob(ORTH + "/logs/*.py")
         + ["CLAUDE.md"])


def carriers(han):
    """Every register word whose own gloss contains this Han string."""
    out = {}
    for f, d in GLOSSES.items():
        n = 0
        for w, gs in d.items():
            gs = [gs] if isinstance(gs, str) else gs
            if any(han in g for g in gs):
                n += 1
        out[f] = n
    return out


hits, seen = [], set()
for path in FILES:
    text = io.open(path, encoding="utf-8", errors="replace").read()
    for para in re.split(r"\n\s*\n", text):
        for sent in re.split(r"(?<=[.!?])\s+", " ".join(para.split())):
            for rx in (BEFORE, AFTER):
                for m in rx.finditer(sent):
                    han = m.group(1)
                    key = (han, os.path.basename(path))
                    if key in seen:
                        continue
                    seen.add(key)
                    hits.append((han, os.path.basename(path), sent))

print("gloss-absence claims harvested:", len(hits))
live = []
for han, path, sent in hits:
    c = carriers(han)
    tot = sum(c.values())
    if tot:
        live.append((tot, han, path, c, sent))
print("claims whose Han string HAS carriers today:", len(live))
print()
for tot, han, path, c, sent in sorted(live, reverse=True):
    print("%-8s %-16s ag=%-4d bg=%-3d pq=%-4d" % (
        han, path, c["attested_gloss.json"], c["bible_gloss.json"],
        c["parquet_gloss.json"]))
    print("    " + sent[:190].replace("`", ""))
