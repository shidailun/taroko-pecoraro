# -*- coding: utf-8 -*-
"""Reverse `hhtran` / `kakuh` to his tokens, and show the cards they sit on."""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
SITE = os.path.join(ROOT, "site")
WANT = sys.argv[1:] or ["hhtran", "kakuh", "kkakuh"]

t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))


def char_rules(w):
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])

AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))


def g(w):
    x = AG.get(w) or []
    x = x if isinstance(x, list) else [x]
    return "/".join(x)[:60] or ("(listed, no gloss)" if w in AM else "NOT LISTED")


def toks(txt):
    return re.findall(r"[A-Za-zçüö’ʼ\"'ʔł]+", txt or "")


for v in WANT:
    keys = sorted(k for k, m in MM.items() if m == v)
    print("\n=== %-8s <- map keys %s" % (v, keys or "(none)"))
    print("    base gloss: %s" % g(v))
    seen = set()

    def scan(e, hw, path):
        for fld in ("hw",):
            pass
        for x in (e.get("examples") or []):
            for w in toks(x.get("t")):
                lw = w.lower()
                if (MM.get(re.sub("[’ʼ\"ʔ]", "'", lw)) == v
                        or (lw not in MM and char_rules(lw) == v)):
                    k = (hw, x.get("t"))
                    if k in seen:
                        continue
                    seen.add(k)
                    print("  [%s] %s" % (hw, (x.get("t") or "")[:78]))
                    print("       中 %s" % (x.get("zh") or "")[:60])
                    print("       fr %s" % (x.get("fr") or "")[:70])
        for sb in (e.get("subs") or []):
            scan(sb, hw, path)

    for e in E:
        hw = e.get("hw") or "?"
        if any((MM.get(re.sub("[’ʼ\"ʔ]", "'", w.lower())) == v)
               or (w.lower() not in MM and char_rules(w.lower()) == v)
               for w in toks(hw)):
            print("  HEADWORD %s  %s | %s" % (hw, (e.get("zh") or "")[:34],
                                              (e.get("fr") or "")[:40]))
        scan(e, hw, "")
        for sb in (e.get("subs") or []):
            f = sb.get("form") or ""
            if any((MM.get(re.sub("[’ʼ\"ʔ]", "'", w.lower())) == v)
                   or (w.lower() not in MM and char_rules(w.lower()) == v)
                   for w in toks(f)):
                print("  SUB %-14s under %-10s %s | %s"
                      % (f, hw, (sb.get("zh") or "")[:30], (sb.get("fr") or "")[:36]))
