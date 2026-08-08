# -*- coding: utf-8 -*-
"""[batch 232 probe] Generalise batch 231's instrument: a pale token of his that
is really TWO modern words typed as one.

No token-keyed test can ever see `ka sayang` -- attestation, the gloss files and
the analyser all ask about single words. Batch 231 found two of these by hand
(`kasayang`, `isoka`) after b57 had pinned one to his own letters for years.
This asks the question over the whole pale list at once.

The test, per pale token, at every split point:
  1. both halves are >= 2 letters
  2. both halves modernise to words in attested_modern.json  (dark end to end)
  3. HE writes each half standing alone in his own book
  4. the SPLIT bigram occurs in the ILRDF parquets
  5. the JOINED string occurs ZERO times there
  6. he does not CARD the joined token   (batch 231's card exclusion)

Prints survivors only.
"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join("tools", "orthography", "logs"))
import dom231 as D                                              # noqa: E402

CACHE = os.path.join(".scratch", "b232", "dom.json")
if os.path.exists(CACHE):
    DOM = json.load(io.open(CACHE, encoding="utf-8"))
else:
    DOM = D.measure()
    json.dump(DOM, io.open(CACHE, "w", encoding="utf-8"))

MM = D.modern_map()
VER = D.verified()
AM = D.sources()[0]
CNT = D.his_tokens()
HEADS = D.his_headwords()

PALE = set(DOM["unv"])
print("pale values %d   his tokens %d" % (len(PALE), len(CNT)))


def modern(w):
    """The app's chain, minus WORD_OVERRIDES (which no map read can see)."""
    k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
    return MM.get(k) or D.char_rules(k)


# --- reverse the pale VALUES to his own tokens (batch 219)
his_pale = sorted(t for t in CNT if modern(t) in PALE)
print("his tokens rendering pale: %d" % len(his_pale))


def bigrams():
    c1, c2 = collections.Counter(), collections.Counter()
    if not os.path.isdir(D.PARQUET_ROOT):
        return None, None
    import pyarrow.parquet as pq
    for d in sorted(glob.glob(os.path.join(D.PARQUET_ROOT, "*", "Truku"))):
        col = ("formosan" if "ithuan_formosan_text" in d.replace("\\", "/")
               else "transcript")
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            try:
                t = pq.read_table(fp, columns=[col])
            except Exception:
                continue
            for s in t.column(col).to_pylist():
                ws = re.findall(r"[A-Za-z']+", (s or "").lower())
                c1.update(ws)
                c2.update(" ".join(p) for p in zip(ws, ws[1:]))
    return c1, c2


U, B = bigrams()
if U is None:
    print("parquets not mounted -- skip")
    sys.exit(0)
print("parquet unigrams %d  bigrams %d" % (len(U), len(B)))

rows = []
for t in his_pale:
    if t in HEADS:
        continue
    joined = modern(t)
    if B.get(joined) or U.get(joined):
        continue                       # the joined string is a real word there
    for i in range(2, len(t) - 1):
        a, b = t[:i], t[i:]
        ma, mb = modern(a), modern(b)
        if ma not in AM or mb not in AM:
            continue
        if not (CNT.get(a) and CNT.get(b)):
            continue
        bg = B.get("%s %s" % (ma, mb), 0)
        if bg < 1:
            continue
        rows.append((bg, t, "%s %s" % (ma, mb), joined,
                     CNT.get(a), CNT.get(b), CNT.get(t),
                     VER.get(ma), VER.get(mb), DOM["unv"].get(joined, 0)))

rows.sort(reverse=True)
print("\n%d candidates" % len(rows))
print("%-14s %-18s %-12s %6s %6s %5s %4s %4s %4s %4s"
      % ("his", "split", "joined", "pq", "hisA", "hisB", "his", "cA", "cB",
         "pale"))
for r in rows:
    print("%-14s %-18s %-12s %6d %6d %5d %4d %4s %4s %4d"
          % (r[1], r[2], r[3], r[0], r[4], r[5], r[6], r[7], r[8], r[9]))
