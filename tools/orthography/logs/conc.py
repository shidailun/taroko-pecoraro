# -*- coding: utf-8 -*-
"""Every ILRDF corpus sentence containing a word, with its Mandarin.

build_parquet_gloss.py refuses the phrase rows on principle: splitting one
Chinese translation across several Truku words is a guess, and a gate reading a
shared Han character cannot tell which half it matched. That refusal is about
AUTOMATION. A human reading four sentences that all contain `mnalu` and all say
代替 in the Chinese is not splitting anything — the word is being identified by
its contexts, which is how a field linguist identifies one.

So this prints and never writes. Nothing it shows enters lex, seen, or a gloss
table; it is evidence for a ruling that a person makes.

    python tools/orthography/logs/conc.py mnalu msska
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = "C:/dev/ILRDF/datasets"
STRIP = re.compile(r"[^A-Za-z']")
MAX = 8


def main():
    import pyarrow.parquet as pq
    words = [w.lower() for w in sys.argv[1:] if not w.startswith("--")]
    hits = {w: [] for w in words}
    seen = {w: set() for w in words}
    for d in sorted(glob.glob(os.path.join(ROOT, "*", "Truku"))):
        p = d.replace("\\", "/")
        tc, gc = (("formosan", "mandarin") if "ithuan_formosan_text" in p
                  else ("transcript", "translation"))
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            t = pq.read_table(fp, columns=[tc, gc])
            for a, b in zip(t.column(tc).to_pylist(), t.column(gc).to_pylist()):
                if not a:
                    continue
                toks = {STRIP.sub("", x).lower() for x in str(a).split()}
                for w in words:
                    if w in toks and str(a) not in seen[w]:
                        seen[w].add(str(a))
                        hits[w].append((str(a).strip(), str(b or "").strip()))
    for w in words:
        h = hits[w]
        print(u"\n%s — %d corpus sentence%s"
              % (w, len(h), "" if len(h) == 1 else "s"))
        for a, b in h[:MAX]:
            print(u"   %s" % a[:110])
            print(u"      %s" % b[:110])
        if len(h) > MAX:
            print(u"   … %d more" % (len(h) - MAX))


if __name__ == "__main__":
    main()
