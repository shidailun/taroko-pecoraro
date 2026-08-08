# -*- coding: utf-8 -*-
"""Join the DOM's pale values to HIS Chinese, from entries.js.

The DOM cannot supply the gloss cheaply -- `.gloss` carries a `中` chip and the
card's zh is spread over head, sub-form and example. So the pale VALUES come from
the DOM (the only honest source for colour) and the Chinese is joined offline by
running his tokens through the same three tables the app reads."""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
PALE = json.load(io.open(".scratch/b230/pale.json", encoding="utf-8"))
t = io.open("site/modern_map.js", encoding="utf-8").read()
_a = t.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[_a:t.index("\n};", _a) + 2], re.M))
ent = io.open("site/entries.js", encoding="utf-8").read()
E = json.loads(ent[ent.index("["):ent.rindex("]") + 1])


def wordkey(w):
    return re.sub(r'[’ʼ"ʔ]', "'", w.lower()).replace("ł", "l")


def char_rules(w):
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


def value(tok):
    k = wordkey(tok.strip("°§.,;:!?()[]«»\"'"))
    return MM.get(k) or char_rules(k)


out = {}


def scan(node, zhs, hw):
    """collect (value -> the zh of the smallest unit the token sits in)"""
    mine = list(zhs)
    if node.get("zh"):
        mine = mine + [node["zh"]]
    for key in ("hw", "form", "t", "paradigm"):
        v = node.get(key)
        for s in ([v] if isinstance(v, str) else (v or []) if isinstance(v, list) else []):
            for tok in re.findall(r"[A-Za-z'\"’ʼ]+", s or ""):
                val = value(tok)
                if val in PALE:
                    d = out.setdefault(val, {"hw": hw, "n": PALE[val]["n"],
                                             "zh": [], "toks": set()})
                    d["toks"].add(tok)
                    for z in mine:
                        if z not in d["zh"]:
                            d["zh"].append(z)
    for x in (node.get("examples") or []):
        scan(x, mine, hw)
    for s in (node.get("subs") or []):
        scan(s, mine, hw)


for e in E:
    scan(e, [], e.get("hw"))

for v in out.values():
    v["toks"] = sorted(v["toks"])
    v["zh"] = " ".join(v["zh"])[:160]
json.dump(out, io.open(".scratch/b230/pale_zh.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("pale types %d   joined to his Chinese %d   unjoined %s"
      % (len(PALE), len(out), sorted(set(PALE) - set(out))[:12]))
