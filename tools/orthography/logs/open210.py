# -*- coding: utf-8 -*-
"""The blockers with no written refusal: his raw spelling, and his own family.

`blockers.py` ranks 92 sole-blocker types, but nearly all carry a refusal from an
earlier batch — re-deriving those is the thing the notes exist to prevent. These
five are the ones `batch-log.md` has never named.

For each: the headword it sits under, his raw token, what the map does with it,
and every OTHER form on the same card with its own map value and attestation.
The family is the cheapest question on the page — a card whose other slots are
all dark convicts a head that keeps its own letters, and acquits one that does
not (batch 199).
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
s = open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
t = open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
O = "tools/orthography/"
ATT = set(json.load(open(H + O + "attested_modern.json", encoding="utf-8")))
GL = json.load(open(H + O + "attested_gloss.json", encoding="utf-8"))
SPK = json.load(open(H + O + "spoken_truku.json", encoding="utf-8"))

TARGETS = sys.argv[1:] or ["sapi", "embuyan", "mtmagu", "tqriyan", "tnqriyan", "smuwan"]
TOK = re.compile(r"[A-Za-zÀ-ÿ'\u2019\"]+")


def key(w):
    return w.lower().replace('"', "'").replace("\u2019", "'")


def mapped(w):
    return MAP.get(key(w), "")


def state(w):
    """What the page will do with this token, and whether anyone else says it."""
    m = mapped(w)
    v = m or w.lower()
    return "%-14s -> %-14s %s spoken=%-4d %s" % (
        w, m or "(char rules)", "ATTESTED" if v in ATT else "pale    ",
        SPK.get(v, 0), " / ".join(GL.get(v, []))[:38])


def forms(e):
    out = [("HEAD", e.get("hw", ""))]
    for sub in e.get("subs") or []:
        out.append(("sub", sub.get("form", "")))
    return out


for target in TARGETS:
    print("\n=== %s" % target)
    hit = False
    for e in E:
        blob = json.dumps(e, ensure_ascii=False)
        if not re.search(r"\b" + target + r"\b", blob, re.I):
            continue
        hit = True
        print("  card %-14s %s" % (e.get("hw", ""), (e.get("zh") or "")[:44]))
        # where the token actually occurs, and under what gloss
        for node, where in ([(e, "card")] +
                            [(x, "sub " + (x.get("form") or "")) for x in e.get("subs") or []]):
            if re.search(r"\b" + target + r"\b", (node.get("form") or ""), re.I):
                print("    FORM  %-22s %s" % (node.get("form"), (node.get("zh") or "")[:40]))
            for ex in node.get("examples") or []:
                if re.search(r"\b" + target + r"\b", ex.get("t") or "", re.I):
                    raw = [w for w in TOK.findall(ex["t"]) if w.lower() == target.lower()]
                    print("    §     %s" % (ex["t"])[:76])
                    print("    中     %s" % ((ex.get("zh") or "")[:56]))
                    for w in raw[:1]:
                        print("    tok   %s" % state(w))
        print("    -- the family on this card:")
        for kind, f in forms(e):
            if not f:
                continue
            for w in TOK.findall(f)[:2]:
                print("      %-5s %s" % (kind, state(w)))
    if not hit:
        print("  not found in entries.js as a whole word")
