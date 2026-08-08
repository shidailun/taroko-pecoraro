# -*- coding: utf-8 -*-
"""Two of HIS cards, one map value, disagreeing glosses — freezes that ship.

Batch 238 measured this class to price a cost (244 modern types over 520 cards)
and never asked the question the class exists to answer. Batch 239 found one by
hand: his QBOLONG 蚱蜢 and his KBOLONG 收割 both landed on `qburung` 收割, so the
grasshopper card rendered dark and wrong.

twice211 asks this of the SAME headword carded twice. This asks it of two
DIFFERENT headwords colliding on one value, which is the larger class and the
one batch 239's find sits in. The outside voice is the same and is his own act
(batch 206): he wrote two cards because he judged them two words, so where the
register glosses the shared value and that gloss agrees with one card and shares
nothing with the other, the other card is dark and wrong.

Rules built in, each one a written finding:
  * batch 218 — strip metalinguistic apparatus from BOTH sides before scoring.
  * batch 232 — the stoplist is DERIVED from the register's own gloss character
    frequencies, and its depth is set where the derivation reproduces every
    character the project has already named as noise. Not hand-picked.
  * batch 221/230 — a shared COMMON character is not agreement; gate on carrier
    rarity.
  * batch 225 — a name-only register gloss does not convict a dark value.
  * batch 200 — the family is the register's answer, so a value with no gloss
    row at all is reported as unjudgeable, never scored as disagreement.
  * batch 230 — report what will not join; never drop it silently.

Ranked by whether the value renders inside a `.truku` box, because a freeze
there SHIPS as a training pair (batch 208), while one on furniture is merely
wrong on the page.

    python .scratch/b240/collide.py
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = "C:/dev/formosan/seediq/taroko-pecoraro/"
ORTH = ROOT + "tools/orthography/"

CJK = re.compile(r"[\u4e00-\u9fff]")
# batch 218: his apparatus and the register's, stripped from both sides
META = re.compile(r"（[^）]*）|\([^)]*\)|的詞根|詞根|引申|註[：:][^；;。]*|"
                  r"人名|男名|女名|地名|等等|之類|泛稱|統稱|的樣子|的情況")


def entries():
    s = io.open(ROOT + "site/entries.js", encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open(ROOT + "site/modern_map.js", encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(ROOT + "site/verified.js", encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def register():
    G = collections.defaultdict(list)
    for p in ("attested_gloss.json", "bible_gloss.json"):
        f = ORTH + p
        if not os.path.exists(f):
            continue
        for k, v in json.load(io.open(f, encoding="utf-8")).items():
            G[k] += [str(x) for x in (v if isinstance(v, list) else [v])]
    return G


def word_key(w):
    """app.js wordKey(), verbatim (batch 219)."""
    return re.sub(r"[’ʼ\"ʔ]", "'", w).lower()


def char_rules(w):
    w = re.sub(r"[’ʼ\"ʔ]", "'", w)
    return (w.replace("ł", "l").replace("ç", "x").lower()
             .replace("o", "u").replace("l", "r").replace("x", "h"))


def value(tok, MM):
    return MM.get(word_key(tok)) or char_rules(tok)


def strip_meta(s):
    return "".join(CJK.findall(META.sub("", s or "")))


def build_stoplist(G, want):
    """batch 232: derive it, and set the depth by what it must reproduce."""
    c = collections.Counter()
    for gl in G.values():
        c.update(set(strip_meta(" ".join(gl))))
    ranked = [ch for ch, _ in c.most_common()]
    for depth in range(10, 120):
        if set(want) <= set(ranked[:depth]):
            return set(ranked[:depth]), depth
    return set(ranked[:30]), 30


def main():
    E, MM, VER, G = entries(), modern_map(), verified(), register()
    # the noise characters the project has already NAMED, in writing
    NAMED = "著子一人為的不是有我你"
    STOP, DEPTH = build_stoplist(G, NAMED)
    carriers = collections.Counter()
    for w, gl in G.items():
        for ch in set(strip_meta(" ".join(gl))):
            carriers[ch] += 1

    # ---- his cards, keyed by the map value their HEADWORD renders as -------
    by_val = collections.defaultdict(list)
    for e in E:
        hw = (e.get("hw") or "").strip()
        zh = strip_meta(str(e.get("zh") or ""))
        if not hw or " " in hw or not zh:          # batch 203: census per token
            continue
        by_val[value(hw, MM)].append((hw, zh))

    rows, unjudgeable = [], []
    for val, cards in sorted(by_val.items()):
        if len(cards) < 2:
            continue
        seen = {}
        for hw, zh in cards:                        # collapse identical glosses
            seen.setdefault(zh, hw)
        if len(seen) < 2:
            continue                                # his cards AGREE — fine
        reg = strip_meta(" ".join(G.get(val, [])))
        if not reg:
            unjudgeable.append((val, sorted(seen.values())))
            continue
        # which card does the register's own gloss agree with?
        scored = []
        for zh, hw in sorted(seen.items()):
            share = {c for c in (set(zh) & set(reg))
                     if c not in STOP and carriers[c] <= 120}
            scored.append((hw, zh, sorted(share)))
        agree = [s for s in scored if s[2]]
        disagree = [s for s in scored if not s[2]]
        if agree and disagree:
            rows.append((val, reg, agree, disagree))

    print("map values serving 2+ of his single-word cards: %d"
          % sum(1 for v, c in by_val.items() if len(c) > 1))
    print("stoplist depth %d (reproduces every named noise character)" % DEPTH)
    print("unjudgeable — the register glosses the value nowhere: %d"
          % len(unjudgeable))
    print("FLAGGED — register agrees with one card, shares nothing with the "
          "other: %d\n" % len(rows))
    for val, reg, agree, disagree in rows:
        print("  %-14s register %s" % (val, reg[:26]))
        for hw, zh, sh in agree:
            print("      served  %-12s %s   (on %s)" % (hw, zh[:20],
                                                        "".join(sh)))
        for hw, zh, _ in disagree:
            print("      ORPHAN  %-12s %s" % (hw, zh[:20]))
    here = os.path.dirname(os.path.abspath(__file__))
    with io.open(os.path.join(here, "flagged.json"), "w",
                 encoding="utf-8") as fh:
        json.dump({"rows": [[r[0], r[1], r[2], r[3]] for r in rows],
                   "unjudgeable": unjudgeable}, fh, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
