# -*- coding: utf-8 -*-
"""Look for the batch-166 error again, everywhere else in the map.

The S"LU bug scored itself DARK. `seelug` and `smeelug` are listed modern words,
so rule 1 verified them at sight; the census cannot see that class of error at
all, because a wrong spelling that happens to be somebody else's right spelling
is indistinguishable from a right one by counting. Only a reader finds it. This
is the instrument that tells a reader where to look.

Two independent signals, and neither works alone.

**Rarity.** The map makes ~5,500 respellings out of ~570 distinct letter
correspondences, and the common ones are the whole system: o>u 882 times, l>r
811, x>h 643, ->e 418, '>- 381. Canonicalise BOTH sides through the classes the
map actually swaps and most respellings collapse to distance 0 — they said the
same thing in two alphabets. What survives is a respelling that changed the word
rather than its spelling. `s'lu` -> `seelug` sits at distance 3.

Rarity alone is not evidence. 57 rows score >= 3 and 56 are lexical swaps he
licenses himself — `tabe` -> `sakur` 犁 with his own note 同義詞＝SAKOL, `tbako`
-> `lumak`, `sengse` -> `mtgsa`, `daloas` -> `dowras`. He is not misspelling
those; he is naming a different word for the same thing, which is what a
dictionary does.

**Disagreement.** `_agrees` asks whether the modern word means what he says the
word means. Alone this is noise too: it fires 519 times across the map on plain
homonymy and on glosses written a century and a language apart.

**Together** they cut 266 rows to 34, and 34 is a number a person can read. The
audit of 2026-08-03 read all 34 and cleared 33 of them:

  P"lu -> peelug        his own example gloss ends （在同一條路上）. He derived
                        "at the same moment" from the road himself.
  Skdolox -> sdrux      KDOLOX is 牆—整齊排列的堆疊 and `qdrux` is 石牆; his
                        直／真誠／誠實 is the figurative half of one root, which
                        his own Mskdoloç prints as 正直的、排列整齊的.
  mpaxei -> empaahiyi   `hiyi` is flesh AND fruit, so 會有瘦肉 and 將結成果實
                        are one word.
  daloas -> dowras      cited 人名 because the cliff word is also a man's name.
  x'lyeq -> hgliq       毀約 is 撕裂 applied to an agreement.

The one that did not clear is `Mpolo`, and it is not fixable here. p. 222 carries
TWO subs spelled Mpolo: 發起者／模仿者, which is `purug`, and 患風濕、痛風的人
with the example `mpolo kana papaq mo!` 我的腳滿是風濕. The second is a different
word. The map is keyed on the raw TOKEN, so both get one spelling and no map
entry can separate them; it needs a per-card override or a speaker. Recorded, not
patched.

**So: no map errors found.** That is the finding, and it is worth as much as a
find would have been. Re-run this after any batch that adds unusual mappings; the
rows it prints are the only place the census is blind.
"""
import sys
import io
import json
import re
import os

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
os.chdir(H)
sys.path.insert(0, H)
from inflection import Inflection  # noqa: E402

# The classes the map swaps as a matter of course. Two spellings that differ
# only inside these are the same word written twice, not a respelling.
CLASS = {}
for grp, tag in (("ouwöò", "U"), ("lr", "R"), ("xhç", "H"),
                 ("eiy", "I"), ("kqp", "K"), ("dj", "J"), ("tc", "C"),
                 ("äa", "A")):
    for ch in grp:
        CLASS[ch] = tag
DROP = "'’\"- "


def canon(s):
    return "".join(CLASS.get(c, c) for c in s.lower() if c not in DROP)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def txt(g):
    return [str(x.get("zh") or "") if isinstance(x, dict) else str(x)
            for x in (g if isinstance(g, (list, set, tuple)) else [g])]


def main():
    lex = set(json.load(io.open("attested_modern.json", encoding="utf-8")))
    src = io.open(os.path.join(H, "..", "..", "site", "modern_map.js"),
                  encoding="utf-8").read()
    mp = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]*)"', src))
    inf = Inflection(lex, mp)

    # Self-test on the pair that motivated the tool. It is no longer in the map
    # -- batch 166 fixed it -- so it is asserted here from the historical record.
    d = lev(canon("s'lu"), canon("seelug"))
    if d < 2:
        print("SELF-TEST FAILED: s'lu -> seelug scores %d, "
              "the classes have been widened until the bug is invisible" % d)
        return 1

    dist = {}
    rows = []
    for k, v in mp.items():
        if not v or k.lower() == v.lower():
            continue
        n = lev(canon(k), canon(v))
        dist[n] = dist.get(n, 0) + 1
        if n < 2 or v not in lex:
            continue
        g, his = inf.gl.get(v), inf._his(v, slots_only=True)
        if not g or not his or inf._agrees(his, v):
            continue
        rows.append((n, k, v, "／".join(txt(g))[:22], "／".join(txt(his))[:44]))

    print("respellings by distance, once both sides are canonicalised:")
    for n in sorted(dist):
        print("   %d  %5d%s" % (n, dist[n], "   <- the map's own system" if not n else ""))
    print()
    print("irregular AND the modern gloss disagrees with his: %d rows" % len(rows))
    print("(2026-08-03: 34 rows, all read, 33 cleared, `mpolo` recorded above.)")
    print()
    for r in sorted(rows, reverse=True):
        print("%d %-13s -> %-13s %-24s %s" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
