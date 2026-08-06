# -*- coding: utf-8 -*-
"""Search from the MEANING, not from the letter.

`look.py` did this off `omni.pkl`, a local cache built from the omnibus
spreadsheet that is not in the repo and is no longer on this disk. The distilled
register is: `attested_gloss.json` is 32,208 modern words with their Chinese,
and `spoken_truku.json` counts them in speech.

    python meaning.py 禮服 盛裝            # which modern word carries his Chinese?
    python meaning.py 禮服 --near tbiran   # ...and how close is it to his shape?

Ranked by shape distance to `--near` when given, else by how often the word is
actually spoken. The gloss printed is the register's own, so it can be scored
against HIS gloss rather than against a pairing file's abbreviation of it
(batch 205). A hit here is a candidate, never a ruling: the gloss of the
candidate still has to match the gloss of the entry it would render in.
"""
import difflib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"
GLOSS = json.load(open(H + "attested_gloss.json", encoding="utf-8"))
SPK = json.load(open(H + "spoken_truku.json", encoding="utf-8"))

args = [a for a in sys.argv[1:] if not a.startswith("--")]
near = None
if "--near" in sys.argv:
    near = sys.argv[sys.argv.index("--near") + 1]
    args = [a for a in args if a != near]
if not args:
    print(__doc__)
    raise SystemExit

hits = []
for w, gs in GLOSS.items():
    g = " / ".join(gs)
    if any(a in g for a in args):
        d = difflib.SequenceMatcher(None, near, w).ratio() if near else 0.0
        hits.append((d, SPK.get(w, 0), w, g))

hits.sort(key=lambda h: (-h[0], -h[1], h[2]))
print("%d attested words carry %s" % (len(hits), "/".join(args)))
for d, n, w, g in hits[:25]:
    print("  %-18s shape %.2f  spoken %-5d %s" % (w, d, n, g[:64]))
