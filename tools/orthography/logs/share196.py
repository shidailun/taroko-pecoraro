# -*- coding: utf-8 -*-
"""How often does rule 2 verify a word on a character that carries no meaning?

Batch 171 pinned `pdrut` pale and left an instruction on the pin: if this ever
goes dark, check that it did so on a gloss and not on another `id` freeze. It is
dark now, at code 2, and the character the two glosses share is 去 — his EXAMPLE
sentence 我沒時間去請人磨小米 against the e-dictionary's 輾過去 for `drut`. Not a
freeze; something the pin did not anticipate. His own word gloss for the slot,
使人碾磨;請人碾磨, agrees with the root on nothing at all.

So: is that one word, or a rung? This walks every code-2 value, asks the
analyser for the character it agreed on, and reports the distribution — plus,
for each value, whether that character reaches it ONLY through a sentence-shaped
string of his. Summary lines only.

    python tools/orthography/logs/share196.py
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from inflection import Inflection            # noqa: E402

lex = set(json.load(io.open(os.path.join(HERE, "attested_modern.json"),
                            encoding="utf-8")))
m = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
mp = json.loads(m[a:m.index("\n};", a) + 2])
inf = Inflection(lex, mp)

v = io.open(os.path.join(ROOT, "site", "verified.js"), encoding="utf-8").read()
codes = dict((w, int(c)) for w, c in re.findall(r'^  "(.+?)": (\d+),', v, re.M))
two = sorted(w for w, c in codes.items() if c == 2)

# A word gloss of his is a gloss; a clause translation is a sentence. The proxy
# is his own punctuation plus length — the sentences all end in 。？! and run
# long, the glosses are 碾磨 / 使人碾磨;請人碾磨.
SENT = re.compile(r"[，。？！,?!]")


def sentence(s):
    return len(s) >= 9 and bool(SENT.search(s[:-1]))


by_char = {}
only_sent = []
for w in two:
    r = inf.regular(w)
    if not r:
        continue
    ch = r[4]
    by_char[ch] = by_char.get(ch, 0) + 1
    holds = [h for h in inf._his(w) if ch in h]
    if holds and all(sentence(h) for h in holds):
        only_sent.append((w, ch))

print("code-2 values: %d; analysable now: %d" % (len(two), sum(by_char.values())))
print("distinct agreement characters: %d" % len(by_char))
print("agreed ONLY through a sentence-shaped string of his: %d" % len(only_sent))
top = sorted(by_char.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
print("commonest characters: " + "  ".join("%s %d" % t for t in top))
sc = {}
for w, ch in only_sent:
    sc[ch] = sc.get(ch, 0) + 1
print("sentence-only, by character: "
      + "  ".join("%s %d" % t for t in
                  sorted(sc.items(), key=lambda kv: (-kv[1], kv[0]))[:14]))
json.dump({"only_sent": only_sent},
          io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "share196.json"), "w", encoding="utf-8",
                  newline="\n"), ensure_ascii=False)
