# -*- coding: utf-8 -*-
"""Search HIS book (batch 200's rule), and ask the register about a candidate.

  python his.py --tok k'aon            how often does he write it, and where
  python his.py --hw KAON              headwords matching a regex, with glosses
  python his.py --reg klaun            is the candidate listed, and glossed what
  python his.py --corr "'" l           his mark vs a modern letter: how does the
                                       map actually pair them, over the whole map
Summary lines only.
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
t = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))
ent = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
ENT = json.loads(ent[ent.index("["):ent.rindex("]") + 1])
BLOB = json.dumps(ENT, ensure_ascii=False)


def gl(w):
    g = AG.get(w) or []
    g = g if isinstance(g, list) else [g]
    return "/".join(g)[:52]


mode, arg = sys.argv[1], sys.argv[2]

if mode == "--tok":
    n = len(re.findall(r"(?<![A-Za-zÀ-ÿ'\"])%s(?![A-Za-zÀ-ÿ'\"])" % re.escape(arg),
                       BLOB, re.I))
    print("%s: %d occurrence(s) in the book" % (arg, n))
    for e in ENT:
        s = json.dumps(e, ensure_ascii=False)
        if re.search(r"(?<![A-Za-zÀ-ÿ'\"])%s(?![A-Za-zÀ-ÿ'\"])" % re.escape(arg), s, re.I):
            print("  %-12s %s | %s" % (e.get("hw"), (e.get("fr") or "")[:38],
                                       (e.get("zh") or "")[:20]))

elif mode == "--hw":
    for e in ENT:
        if re.search(arg, e.get("hw") or "", re.I):
            print("  %-14s %-34s %s" % (e.get("hw"), (e.get("fr") or "")[:34],
                                        (e.get("zh") or "")[:24]))

elif mode == "--reg":
    for w in sys.argv[2:]:
        print("  %-14s listed=%-5s %s" % (w, w in AM, gl(w) or "(no gloss)"))

elif mode == "--corr":
    # how does the map pair his mark against a modern letter, book-wide?
    mark, letter = sys.argv[2], sys.argv[3]
    c = collections.Counter()
    ex = collections.defaultdict(list)
    for k, v in MM.items():
        if mark in k and len(k) == len(v):
            for i, ch in enumerate(k):
                if ch == mark and i < len(v):
                    c[v[i]] += 1
                    if len(ex[v[i]]) < 3:
                        ex[v[i]].append("%s>%s" % (k, v))
    tot = sum(c.values())
    print("his %r at the same index, over %d same-length map pairs:" % (mark, tot))
    for ch, n in c.most_common(8):
        print("  -> %-3s %4d (%4.1f%%)  %s" % (ch, n, 100.0 * n / max(tot, 1),
                                               " ".join(ex[ch])))
