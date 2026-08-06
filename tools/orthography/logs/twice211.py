# -*- coding: utf-8 -*-
"""Headwords he carded TWICE, where one map value has to serve both senses.

The LIDIL find (batch 211) is a shape, not an accident: where he wrote the same
headword on two cards with unrelated glosses, the token-keyed map can carry only
ONE value, so at most one of the two cards is rendered by a word that means what
the card says. If the register glosses that value and it shares no character with
the OTHER card's Chinese, that card is dark and wrong — a homograph freeze no
colour metric can see.

This is a much narrower question than the batch 206 whole-book gloss sweep, which
flagged 827 of 2,420 dark headwords and was noise. Here the duplication is HIS
OWN act: he carded the word twice because he judged it two words. That is the
outside voice batch 206 said a freeze detector needs, and it costs nothing to
ask, because the class is enumerable and small.

A flag is a QUESTION, not a verdict. Two cards by the same hand can gloss one
sense two ways (batch 200: a single gloss row is not the register's answer), and
his prose restates. What earns a ruling is a DIFFERENT attested word carrying the
other card's meaning — which is what `rijig` 柄（刀;鋤） was for LIDIL 工具的柄.
"""
import json
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
O = H + "tools/orthography/"

s = open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
t = open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
VER = dict(re.findall(r'^  "(.+?)": (\d+),?$',
                      open(H + "site/verified.js", encoding="utf-8").read(), re.M))
GL = json.load(open(O + "attested_gloss.json", encoding="utf-8"))
SPK = json.load(open(O + "spoken_truku.json", encoding="utf-8"))

CJK = re.compile(r"[\u4e00-\u9fff]")
TOK = re.compile(r"[A-Za-zÀ-ÿ'\u2019\"]+")


def key(w):
    return w.lower().replace('"', "'").replace("\u2019", "'")


def chars(zh):
    return set(CJK.findall(zh or ""))


# group cards by the headword token he wrote
byhw = defaultdict(list)
for i, e in enumerate(E):
    hw = e.get("hw") or ""
    toks = TOK.findall(hw)
    if len(toks) != 1:
        continue                      # multi-word heads have no single map key
    byhw[key(toks[0])].append((i, e))

dups = {k: v for k, v in byhw.items() if len(v) > 1}
print("headwords he carded more than once: %d" % len(dups))

flagged = []
for k in sorted(dups):
    cards = dups[k]
    val = MAP.get(k)
    if not val:
        continue                      # green: no claim to be wrong about
    if val not in VER:
        continue                      # pale: already saying "unconfirmed"
    reg = chars(" ".join(GL.get(val, [])))
    if not reg:
        continue                      # the register does not gloss the value
    scored = [(i, e, chars(e.get("zh")) & reg) for i, e in cards]
    served = [x for x in scored if x[2]]
    unserved = [x for x in scored if not x[2] and chars(x[1].get("zh"))]
    if served and unserved:
        flagged.append((k, val, served, unserved))

print("of those, dark values whose register gloss serves one card and not the "
      "other: %d\n" % len(flagged))


def outside_voice(zh, exclude, k):
    """Which DIFFERENT attested word carries the orphan card's meaning?

    The batch 204 test. An attestation question over the flagged value is
    circular — it is dark, that is the premise — so the only non-circular one is
    whether some OTHER word means what the orphan card says. Two shared
    characters, because one is his prose style (`人` in 太魯閣人 matched a 人名
    gloss and proposed a man's name for his millet card).

    Ranked by shape distance to HIS token first: a freeze that can be split
    looks like `lidil` -> `rijig`, one letter off the value already there, and a
    synonym on the other side of the language is a different claim entirely.
    """
    want = chars(zh)
    if len(want) < 2:
        return []
    out = []
    for w, gs in GL.items():
        if w == exclude or not SPK.get(w):
            continue
        sh = chars(" ".join(gs)) & want
        if len(sh) >= 2:
            near = len(set(w) & set(k)) / float(max(len(w), len(k)))
            out.append((round(near, 2), SPK[w], w, " / ".join(gs)[:26]))
    out.sort(key=lambda x: (-x[0], -x[1]))
    return out[:2]


for k, val, served, unserved in flagged:
    print("%-12s -> %-12s code %-3s spoken %-4d  %s"
          % (k, val, VER.get(val, "-"), SPK.get(val, 0),
             " / ".join(GL.get(val, []))[:34]))
    for i, e, sh in served:
        print("    serves   card %-5d %s" % (i, (e.get("zh") or "")[:38]))
    for i, e, sh in unserved:
        print("    ORPHAN   card %-5d %s" % (i, (e.get("zh") or "")[:38]))
        for near, n, w, g in outside_voice(e.get("zh"), val, k):
            print("      voice  %-12s shape %.2f spoken %-5d %s" % (w, near, n, g))
