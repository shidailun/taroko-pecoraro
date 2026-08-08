# -*- coding: utf-8 -*-
"""Price the seam the SNOXEL ruling opened.

The fingerprint: a pale value whose card's Chinese contains a RARE character
that some LISTED register word carries, and that word sits within 2 edits of the
pale value. `sneuhir` scored exactly that against `snuher` on 妒 (43 carriers,
distance 2), while a string search on his 嫉妒 returned only the hkrig family.

Gates, both needed, or the output is batch 221's noise:
  - the character has at most CARRIER_MAX carriers (妒 43; 子 887, 為 1569)
  - the listed word is within EDIT_MAX of the pale value
Reports a count and the rows. Verdict lines only."""
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
O = "tools/orthography/"
CARRIER_MAX = 120
EDIT_MAX = 2

AM = set(json.load(io.open(O + "attested_modern.json", encoding="utf-8")))
AG = json.load(io.open(O + "attested_gloss.json", encoding="utf-8"))
BG = json.load(io.open(O + "bible_gloss.json", encoding="utf-8"))
PALE = json.load(io.open(".scratch/b230/pale_zh.json", encoding="utf-8"))

STOP = set("的了是不在有人和一二三個他她我你們也就都很之與或等這那")


def L(x):
    return [] if x is None else (x if isinstance(x, list) else [x])


def gl(w):
    return L(AG.get(w)) + L(BG.get(w))


CAR = {}
for w in sorted(set(AG) | set(BG)):
    for s in gl(w):
        for ch in set(s):
            CAR.setdefault(ch, []).append(w)


def ed(a, b, cap):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    p = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        c = [i]
        for j, cb in enumerate(b, 1):
            c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (ca != cb)))
        p = c
    return p[-1]


# batch 218: strip his apparatus from BOTH sides before scoring a gloss.
# The character 根 in "…的詞根" is metalinguistic, not meaning; so are his
# affix labels, his part-of-speech notes and his own class markers.
META = [
    "的詞根", "詞根", "前綴詞", "前綴", "後綴", "中綴", "省略字", "擬聲詞",
    "代名詞所有格", "代名詞", "助詞", "語助詞", "指示", "進行貌標記",
    "慣用語", "植物名", "動物名", "人名", "男名", "女名", "地名",
    "是「", "」的", "為「",
]


def strip_meta(s):
    for m in META:
        s = s.replace(m, "")
    return s


rows = []
for val, meta in sorted(PALE.items()):
    zh = strip_meta(meta.get("zh") or "")
    best = None
    for ch in set(zh):
        if ch in STOP or not ("一" <= ch <= "鿿"):
            continue
        cs = CAR.get(ch) or []
        if not cs or len(cs) > CARRIER_MAX:
            continue
        for w in cs:
            if w not in AM or w == val:
                continue
            d = ed(val, w, EDIT_MAX)
            if d <= EDIT_MAX and (best is None or d < best[0]):
                best = (d, w, ch, len(cs))
    if best:
        rows.append((best[0], val, best[1], best[2], best[3],
                     meta["n"], meta["hw"]))

rows.sort()
print("pale types %d   rows passing both gates: %d  (carriers<=%d, edits<=%d)"
      % (len(PALE), len(rows), CARRIER_MAX, EDIT_MAX))
for d, val, w, ch, nc, n, hw in rows:
    g = "/".join(gl(w))[:34]
    print("  %-13s -> %-13s d=%d  %s(%d carriers)  %-10s x%-2d  %s"
          % (val, w, d, ch, nc, hw[:10], n, g))
