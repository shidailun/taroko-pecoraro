# -*- coding: utf-8 -*-
"""The nine unworked no-root blockers: his side, and what the register says.

For each: the card it sits on, his French + Chinese, the blocked sentence, how
the map produces the value (manual pin / char rules / identity), and whether
roots() reaches anything at all. Verdict lines only -- never a card body.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORTH = os.path.join(ROOT, "tools", "orthography")
sys.path.insert(0, ORTH)

WORDS = sys.argv[1:] or ["kaon", "qntqdan", "nagui", "smllu", "iniku",
                         "mman", "pkkah", "uru", "rqili"]

AM = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"), encoding="utf-8")))
AG = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"), encoding="utf-8"))
MAN = json.load(io.open(os.path.join(ORTH, "manual_map.json"), encoding="utf-8"))

t = io.open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))

ent = io.open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
ENT = json.loads(ent[ent.index("["):ent.rindex("]") + 1])


def char_rules(w):
    return w.replace("o", "u").replace("l", "r").replace("x", "h")


def wordkey(w):
    return re.sub(r'[’ʼ"ʔ]', "'", w.lower()).replace("ł", "l")


def gl(w):
    g = AG.get(w) or []
    g = g if isinstance(g, list) else [g]
    return "/".join(g)[:40]


# his tokens for each value
HIS = {}
for k, v in MM.items():
    HIS.setdefault(v, set()).add(k)


def toks(s):
    return re.findall(r"[^\s,.;:!?()\[\]«»\"]+", s or "")


def find(val):
    """cards where one of his tokens rendering to `val` occurs"""
    out = []
    for e in ENT:
        blob = json.dumps(e, ensure_ascii=False)
        for tok in set(toks(blob.replace('"', " "))):
            k = wordkey(tok.strip("°§"))
            if (MM.get(k) or char_rules(k)) == val:
                out.append((e, tok.strip("°§")))
                break
    return out


for w in WORDS:
    print("\n=== %s ===" % w)
    hs = sorted(HIS.get(w, set()))
    print("  map keys -> it: %s | manual: %s | attested: %s %s"
          % (" ".join(hs) or "(none)",
             " ".join("%s=%s" % (k, MAN[k]) for k in hs if k in MAN) or "-",
             w in AM, gl(w) or ""))
    for k in hs:
        print("    charRules(%s) = %s%s" % (k, char_rules(k),
                                            "  <- map is redundant" if char_rules(k) == w else ""))
    try:
        import inflection as inf
        r = inf.roots(w)
        print("  roots(%s): %s" % (w, r[:3] if r else "level 0"))
    except Exception as e:
        print("  roots failed: %s" % e)
    for e, tok in find(w)[:2]:
        print("  card %-12s %s | %s" % (e.get("hw"), (e.get("fr") or "")[:40],
                                        (e.get("zh") or "")[:22]))
        blob = json.dumps(e, ensure_ascii=False)
        for m in re.finditer(r'"t": "([^"]*)"', blob):
            if tok.lower() in m.group(1).lower():
                i = blob.index(m.group(0))
                fr = re.search(r'"fr": "([^"]*)"', blob[i:])
                zh = re.search(r'"zh": "([^"]*)"', blob[i:])
                print("    S %s" % m.group(1)[:74])
                print("      fr %s" % ((fr.group(1) if fr else "")[:60]))
                print("      zh %s" % ((zh.group(1) if zh else "")[:34]))
                break
