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
    character the project has already named as noise. Not hand-picked. Measured
    here it is INERT (41 rows at every depth), because the rarity gate below is
    strictly stronger; that is stated rather than left implied, and the
    derivation now returns depth 0 when it FAILS instead of a plausible 30.
  * batch 221/230 — a shared COMMON character is not agreement; gate on carrier
    rarity.
  * batch 225 — a name-only register gloss does not convict a dark value.
  * batch 200 — the family is the register's answer, so a value with no gloss
    row at all is reported as unjudgeable, never scored as disagreement.
  * batch 230 — report what will not join; never drop it silently.

Ranked by whether the value renders inside a `.truku` box, because a freeze
there SHIPS as a training pair (batch 208), while one on furniture is merely
wrong on the page.

THE RESULT IS NEGATIVE AND IS KEPT AS ONE — the standing of `freezesweep.py`,
`tail221.py` and `premise231.py`. Over the whole book the sweep flags 41 rows
and rules NONE of them. Every row falls in a class already closed in writing:

  20  the SAME headword carded twice — batch 205 refuses the remap (a
      token-keyed map cannot split two senses of one string, and a remap paints
      his correct sentences wrong), and batch 222 measured the whole queue at
      **0 pale**, so it moves the metric by zero in any case.
  15  his OWN cross-reference or variant note — 參見, 見, 「會不會是…的變體」,
      「syn. = SAKOL」, 「更正確的寫法」. His two cards are one word and he says
      so on the page; there is no disagreement to adjudicate.
   4  tier-J loans, and they are CORRECT: his BALAS 礫石 (バラス), KASI 餅乾
      (菓子), XANA 花, XAYA 汽車 (ハイヤー) collide with native `balas`,
      `kasi`, `hana`, `haya`. Batch 204 — a modern homophone is not a freeze.
   2  leftovers, both refused by naming the form whose OWN gloss carries his
      character (batch 221):
        `tucing`  his TOTING 鐵鎚 beside TÖTING 掉落. `wordKey()` keeps the
                  diaeresis (batch 219), so the map COULD split them — and must
                  not: `tmucing` 敲打、鎚 is built on that root and carries his
                  hammer. Both senses are the register's.
        `qnilaw`  his KNILAO / QNILAO 豬食. `tmqnilaw` 煮豬食的人 and
                  `smqnilaw` 很需要豬食 carry his gloss verbatim.

So batch 239's `qbolong`/`kbolong` freeze was the only one of its shape in
1,967 entries. What makes that a finding rather than an empty sweep is the
positive control (batch 232, controlled from the DATA side): fed the pre-239
map this instrument recovers `qburung` with orphan QBOLONG unaided, and fed a
blinded register it recovers nothing. `dom240.py` keeps it live — it fires when
a NEW collision appears that none of the four classes accounts for.

    python tools/orthography/logs/collide240.py
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
    """batch 232: derive it, and set the depth by what it must reproduce.

    Returns (stoplist, depth), and depth 0 means the derivation FAILED to
    reproduce every character it was asked for. The first draft of this
    returned `ranked[:30], 30` in that case, which is the shape batch 233
    warns about one level down: a fallback that hands back a plausible number
    cannot be told from a derivation that worked. It was firing — 我 sits at
    rank 368 of 2,780 and 你 at 300, so no depth in range reproduced the list,
    and the printed line "depth 30 (reproduces every named noise character)"
    was false. dom240's own control caught it.
    """
    c = collections.Counter()
    for gl in G.values():
        c.update(set(strip_meta(" ".join(gl))))
    ranked = [ch for ch, _ in c.most_common()]
    for depth in range(10, 120):
        if set(want) <= set(ranked[:depth]):
            return set(ranked[:depth]), depth
    return set(ranked[:30]), 0


# his own words for "these two cards are one word" -- 參見/見/變體/syn./同義詞,
# plus the grammatical descriptions that are not glosses at all (batch 218, one
# level up: a whole gloss can BE apparatus).
XREF = re.compile(r"見|參見|前綴|後綴|所有格|人稱|虛詞|變體|寫法|僅見|之意|"
                  r"syn\.|同義詞")


def bare(h):
    return re.sub(r"[^a-z]", "", word_key(h))


def classify(rows, E):
    """Sort every flagged row into a class already closed in writing.

    Returns (Counter, leftovers). A row reaching LEFTOVER is the news: it is a
    collision no standing refusal covers, and it is what dom240 asserts on.
    """
    card = collections.defaultdict(list)
    for e in E:
        card[(e.get("hw") or "").strip()].append(e)
    cnt, left = collections.Counter(), []
    for val, reg, agree, dis in rows:
        heads = {h for h, _, _ in agree} | {h for h, _, _ in dis}
        orphans = [h for h, _, _ in dis]
        prose = " ".join(t for h in heads for e in card[h]
                         for t in ((e.get("tag") or ""), (e.get("fr") or ""),
                                   (e.get("zh") or "")))
        if any("emprunt" in (e.get("tag") or "")
               for h in orphans for e in card[h]):
            k = "tier-J loan, and correct (batch 204)"
        elif XREF.search(prose):
            k = "his own cross-ref / variant note"
        elif len({bare(h) for h in heads}) == 1:
            k = "same headword carded twice (batch 205/222)"
        else:
            k = "LEFTOVER"
            left.append((val, sorted(heads)))
        cnt[k] += 1
    return cnt, left


# the two leftovers, both refused above; a THIRD is what dom240 fires on
KNOWN_LEFTOVERS = [["KNILAO", "QNILAO"], ["TOTING", "TÖTING"]]


# The noise characters the project has already NAMED, in writing — restricted
# to the ones named over the REGISTER's glosses (batch 218's 的詞根 scoring,
# batch 221's 著/子/一/人 tail rows, batch 232's own derivation). 我 and 你 are
# deliberately NOT here: they are batch 221's noise from 我的 / 你們的, which
# are SENTENCE glosses, and the register's definitions barely use pronouns —
# 我 ranks 368th of 2,780 characters and 你 300th, so requiring them would set
# the cut past 300 and strip the whole vocabulary the test scores on.
NAMED = "著子一人為的不是有"

# What the stoplist is WORTH here, measured as batch 232 requires: nothing.
# Withdrawn entirely the sweep flags 41 rows; at depth 30 it flags 41; at the
# derived depth 37 it flags 41. The rarity gate (carriers <= 120) is strictly
# stronger than any frequency cut — a character in the top 37 by document
# frequency has hundreds of carriers and is already gone. The stoplist is kept
# because it costs nothing and because a later change could make it
# load-bearing; STOPLIST_IS_INERT is the pin that would notice.
STOPLIST_IS_INERT = True


def stoplist_at(G, depth):
    """the same derivation, cut at a depth the caller names -- how dom240
    measures what the stoplist is WORTH (batch 232)."""
    c = collections.Counter()
    for gl in G.values():
        c.update(set(strip_meta(" ".join(gl))))
    return set(ch for ch, _ in c.most_common()[:depth])


def sweep(E, MM, G, depth=None):
    """The whole instrument, over inputs supplied by the caller.

    Taking E/MM/G as arguments rather than reading them is what lets dom240
    control this from the DATA side in both directions (batch 232): fed the
    pre-239 map it must recover QBOLONG, and fed a blinded register it must
    recover nothing. An empty sweep and a broken sweep have the same output.

    `depth` overrides the derived cut; dom240 uses it to measure what the
    stoplist is worth, which here is nothing.

    Returns (colliding, depth, unjudgeable, rows).
    """
    if depth is None:
        STOP, DEPTH = build_stoplist(G, NAMED)
    else:
        STOP, DEPTH = stoplist_at(G, depth), depth
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

    colliding = sum(1 for v, c in by_val.items() if len(c) > 1)
    return colliding, DEPTH, unjudgeable, rows


def main():
    E, MM, VER, G = entries(), modern_map(), verified(), register()
    colliding, DEPTH, unjudgeable, rows = sweep(E, MM, G)

    print("map values serving 2+ of his single-word cards: %d" % colliding)
    print("stoplist depth %d (reproduces every named noise character)" % DEPTH)
    print("unjudgeable — the register glosses the value nowhere: %d"
          % len(unjudgeable))
    print("FLAGGED — register agrees with one card, shares nothing with the "
          "other: %d" % len(rows))
    cnt, left = classify(rows, E)
    for k, v in cnt.most_common():
        print("    %-42s %d" % (k, v))
    print("  leftovers (each refused in the docstring): %s"
          % ", ".join("/".join(h) for _, h in left))
    news = [h for _, h in left if h not in KNOWN_LEFTOVERS]
    print("  NEW, unclassified: %s" % (news or "none — the sweep is closed"))
    print()
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
