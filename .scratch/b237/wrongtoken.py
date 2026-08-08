# -*- coding: utf-8 -*-
"""Does a refusal's stated reason describe the token it is refusing?

Batch 231 named this fault: `dom219.py:233` refused `isuka` because "蓋住 is
spuy", and the 蓋住 belonged to `Lmobong` -- a different word in the same
sentence. Batch 236 hit it again from the other side: `shmqan`'s refusal opens
"his GMALYEQ card is headed 詞根不明", which is his note about the HEADWORD,
while the token being refused is `sxmqan` inside the example.

This is NOT `logs/premise231.py`, which swept ABSENCE claims and closed the
class at zero. That asked whether a premise was TRUE. This asks whether it is
about the right word, which a true premise can fail.

The filter is self-selecting. A Han run in a refusal is either a register gloss
it is citing (`首領 is bukung`) or a quote of HIS gloss. A register gloss will
not appear on his card; a quote of his will. So: flag a run that appears
SOMEWHERE on his card but NOWHERE in the scope the refused token actually sits
in. A hit is a place to READ -- the verdict can be sound over a wrong premise
(batches 232, 235), so this proposes nothing.

    python .scratch/b237/wrongtoken.py
"""
import collections
import glob
import importlib
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.join("tools", "orthography", "logs"))
sys.stdout.reconfigure(encoding="utf-8")
HAN = re.compile(r"[一-鿿＀-￯]{2,}")
TOK = re.compile(r"[A-Za-zÇçÀ-ſ'\"]+")


def entries():
    s = io.open("site/entries.js", encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open("site/modern_map.js", encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def char_rules(w):
    w = re.sub(r"[’ʼ\"ʔ]", "'", w).lower()
    return w.replace("ł", "l").replace("ç", "x") \
            .replace("o", "u").replace("l", "r").replace("x", "h")


MM = modern_map()


def value(tok):
    k = re.sub(r"[’ʼ\"ʔ]", "'", tok).lower()
    return MM.get(k) or char_rules(k)


# --- his book, indexed by (value -> list of (card, scope-gloss, card-gloss))
E = entries()
SCOPE = collections.defaultdict(list)


def add(val, card, own, whole):
    SCOPE[val].append((card, own, whole))


def card_text(e):
    """Every Chinese on this card, at any depth."""
    out = [str(e.get("zh") or "")]
    for x in (e.get("examples") or []):
        out.append(str(x.get("zh") or ""))
    for sb in (e.get("subs") or []):
        out.extend(card_text(sb))
    return " ".join(out)


def walk(e, card, whole):
    hw = (e.get("hw") or e.get("form") or "").strip()
    if hw:
        # a headword or sub-form NAME: its own gloss is the card/sub gloss
        for w in TOK.findall(hw):
            add(value(w), card, str(e.get("zh") or ""), whole)
    for x in (e.get("examples") or []):
        zh = str(x.get("zh") or "")
        for w in TOK.findall(str(x.get("t") or "")):
            add(value(w), card, zh, whole)
    for sb in (e.get("subs") or []):
        walk(sb, card, whole)


for e in E:
    walk(e, (e.get("hw") or "").strip(), card_text(e))

# --- every REFUSED dict in the record
REF = {}
for p in sorted(glob.glob(os.path.join("tools", "orthography", "logs",
                                       "dom2*.py"))):
    name = os.path.basename(p)[:-3]
    try:
        m = importlib.import_module(name)
    except Exception as exc:
        print("  (skip %s: %s)" % (name, str(exc)[:50]))
        continue
    for var in ("REFUSED", "REFUSALS"):
        d = getattr(m, var, None)
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, str):
                    REF.setdefault(k, []).append((name, v))

print("%d refusals over %d values" % (sum(len(v) for v in REF.values()),
                                      len(REF)))

flagged = 0
for val in sorted(REF):
    scopes = SCOPE.get(val, [])
    if not scopes:
        continue
    for log, why in REF[val]:
        for run in set(HAN.findall(why)):
            on_card = [s for s in scopes if run in s[2]]
            in_scope = [s for s in scopes if run in s[1]]
            if on_card and not in_scope:
                flagged += 1
                print("\n  %-9s %-10s quotes %s" % (log, val, run))
                print("    on his [%s] card, but NOT in the scope the token "
                      "sits in" % on_card[0][0])
                print("    token's own gloss: %s" % (on_card[0][1][:70]
                                                     or "(none)"))
print("\n%d flagged" % flagged)
