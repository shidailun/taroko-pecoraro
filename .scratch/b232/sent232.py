# -*- coding: utf-8 -*-
"""[batch 232 probe] The parallel corpus, read as SENTENCES.

Batch 183 read the parquets' Mandarin column for rows whose Truku side is one
word (8,875 of them) and refused the phrase rows in writing: `baga bubu`
母親的雙手 would gloss `baga` 手 and 母親 with equal confidence, and a shared
character cannot tell which half it matched. That reason is about building a
WORD -> GLOSS file, and it is right.

It is not a reason against this question, which never attributes a gloss to a
word: take HIS example sentence and ITS Chinese, find corpus sentences whose
Chinese overlaps his, and ask which Truku word in them is close in SHAPE to his
pale token. Sentence against sentence is apples to apples, and it reaches the
cards a word-level test cannot -- the eleven he could not gloss himself.

A hit is a PROPOSAL, never a ruling: the gloss of the candidate still has to
match the gloss of the entry it renders in.

    python .scratch/b232/sent232.py
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

HAN = re.compile(r"[一-鿿]")
MM = D.modern_map()
AM, AG, BG, PG = D.sources()
DOM = json.load(io.open(".scratch/b232/dom.json", encoding="utf-8"))
PALE = set(DOM["unv"])


def modern(w):
    k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
    return MM.get(k) or D.char_rules(k)


# ---------------------------------------------------------------- his side
TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
his_rows = []                     # (hw, his token, pale value, zh, sentence)


def walk(e, hw):
    for x in (e.get("examples") or []):
        t, zh = x.get("t") or "", x.get("zh") or ""
        if not t or not zh or not HAN.search(zh):
            continue
        for w in TOK.findall(t):
            v = modern(w)
            if v in PALE:
                his_rows.append((hw, w.lower(), v, zh, t))
    for sb in (e.get("subs") or []):
        walk(sb, hw)


for e in D.entries_json():
    walk(e, e.get("hw") or "")

print("his pale example rows: %d  distinct values: %d"
      % (len(his_rows), len(set(r[2] for r in his_rows))))


# ------------------------------------------------------------ corpus side
def corpus():
    out = []
    for d in sorted(glob.glob(os.path.join(D.PARQUET_ROOT, "*", "Truku"))):
        p = d.replace("\\", "/")
        tc, gc = ("formosan", "mandarin") if "ithuan_formosan_text" in p \
            else ("transcript", "translation")
        import pyarrow.parquet as pq
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            try:
                t = pq.read_table(fp, columns=[tc, gc])
            except Exception:
                continue
            for tr, zh in zip(t.column(tc).to_pylist(), t.column(gc).to_pylist()):
                if tr and zh and HAN.search(zh):
                    out.append((re.findall(r"[A-Za-z']+", tr.lower()),
                                set(HAN.findall(zh)), tr, zh))
    return out


if not os.path.isdir(D.PARQUET_ROOT):
    print("parquets not mounted -- skip")
    sys.exit(0)
C = corpus()
print("corpus sentence pairs with Chinese: %d" % len(C))

# index by Han character so we only score sentences that can possibly overlap
byhan = collections.defaultdict(list)
for i, (ws, hs, tr, zh) in enumerate(C):
    for h in hs:
        byhan[h].append(i)

rows = []
for hw, tok, val, zh, sent in his_rows:
    hs = set(HAN.findall(zh))
    if len(hs) < 2:
        continue
    cand = collections.Counter()
    for h in hs:
        for i in byhan.get(h, ()):
            cand[i] += 1
    best = None
    for i, sh in cand.items():
        if sh < 2:
            continue
        ws, chs, tr, czh = C[i]
        # CONTAINMENT, not Jaccard: his example glosses are long sentences and
        # the corpus rows are often single words, so a union denominator would
        # score a perfect sense match as 0.1 and throw it away.
        j = sh / float(min(len(hs), len(chs)))
        if j < 0.60:
            continue
        for w in ws:
            if w == val or w in PALE:
                continue
            if w not in AM:
                continue
            e = D.ed(val, w)
            if e > 2 or e >= max(2, len(val) - 2):
                continue
            sc = (j, -e)
            if best is None or sc > best[0]:
                best = (sc, hw, tok, val, w, e, round(j, 2), czh, zh)
    if best:
        rows.append(best)

rows.sort(reverse=True)
seen = set()
print("\n%d proposals (best per row, deduped by value+candidate)" % len(rows))
for sc, hw, tok, val, w, e, j, czh, zh in rows:
    if (val, w) in seen:
        continue
    seen.add((val, w))
    g = (D.gl(AG, w) or D.gl(BG, w) or D.gl(PG, w) or ["-"])[0]
    print("%-10s %-12s %-12s -> %-12s ed=%d j=%.2f | %s | his: %s"
          % (hw[:10], tok[:12], val[:12], w[:12], e, j, str(g)[:24], zh[:28]))
