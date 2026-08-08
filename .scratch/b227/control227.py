# -*- coding: utf-8 -*-
"""Negative control for logs/dom227.py.

A frozen measurement that cannot fail is a list of excuses (batch 209), so every
assertion in dom227 is tampered with in turn and required to FAIL -- and two
untouched/irrelevant cases are required to PASS, because a log that fails on
anything is just as useless.

The DOM is measured ONCE and replayed, so the whole control costs one page load.
"""
import contextlib
import copy
import importlib.util
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location(
    "dom227", os.path.join(ROOT, "tools", "orthography", "logs", "dom227.py"))
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)

print("measuring once ...")
DOM = D.measure()
REAL = dict(measure=D.measure, modern_map=D.modern_map, verified=D.verified,
            register=D.register, sources=D.sources, char_rules=D.char_rules,
            audio_ids=D.audio_ids)
CONST = dict((k, getattr(D, k)) for k in
             ("FLOOR", "DENOM", "AUDIO_IDS", "RULED", "FREEZE", "FREEZE_GLOSS",
              "CARD", "REFUSED", "REFUSED_INTRUKU", "OTHER_ROOT", "OTHER_CHAR"))
results = []


def run(name, expect_fail, dom=None, **patch):
    for k, v in REAL.items():
        setattr(D, k, v)
    for k, v in CONST.items():
        setattr(D, k, v)
    d = copy.deepcopy(DOM) if dom is None else dom(copy.deepcopy(DOM))
    D.measure = lambda: d
    for k, v in patch.items():
        setattr(D, k, v)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = D.main()
    out = [l for l in buf.getvalue().splitlines() if l.startswith("FAIL")]
    ok = bool(rc) == expect_fail
    print("%-52s -> %s%s" % (name,
                             ("refused: " + out[0][5:63]) if out else "passed",
                             "" if ok else "   <<< BAD"))
    results.append(ok)


def paled(w):
    """Move a word out of the pale dict, i.e. it has gone DARK on the page."""
    def f(d):
        d["unv"].pop(w, None)
        return d
    return f


# 1 -- untouched. The log must pass as it stands.
run("UNTOUCHED (positive control)", False)

# 2 -- an unrelated word going pale must NOT fail this log
run("an unrelated word goes pale (positive control)", False,
    dom=lambda d: (d["seen"].update(zzz=3), d["unv"].update(zzz=3), d)[-1])

# 3 -- the ruling leaves the map
run("map drops s'mul -> smul", True,
    modern_map=lambda: dict(REAL["modern_map"](), **{"s'mul": "samul"}))

# 4 -- the freeze is reinstated as some other key's value
run("some key sends to smur again", True,
    modern_map=lambda: dict(REAL["modern_map"](), zzz="smur"))

# 5 -- smur back in verified.js: a key is emitting it
run("smur re-enters verified.js", True,
    verified=lambda: dict(REAL["verified"](), smur=1))

# 6 -- the pin stops being load-bearing
run("charRules no longer spells the freeze", True,
    char_rules=lambda w: "smul")

# 7 -- a card value goes dark: the consistency fix has become a claim
run("smamul renders dark on the page", True, dom=paled("smamul"))

# 8 -- and the same thing seen from verified.js
run("smul enters verified.js", True,
    verified=lambda: dict(REAL["verified"](), smul=1))

# 9 -- FURNITURE: the ruling turns out to touch a sentence after all
run("smul appears inside a .truku box", True,
    dom=lambda d: (d["inTruku"].update(smul=1), d)[-1])

# 10 -- the freeze account: smur gains his character
run("smur's register gloss gains 抱", True,
    register=lambda: (REAL["register"]()[0],
                      dict(REAL["register"]()[1], smur=["濕冷", "抱著"])))

# 11 -- the freeze account: smur clears the >= 2 bar
run("smur gains a second source", True,
    sources=lambda: dict(REAL["sources"](), **{"bible_gloss.json": {"smur": 1}}))

# 12 -- batch 221's refusal is overturned without being cited
run("snmul enters verified.js (221's refusal)", True,
    verified=lambda: dict(REAL["verified"](), snmul=1))

# 13 -- the positive half of the refusal is gone
run("kmeabuh loses 抱", True,
    register=lambda: (REAL["register"]()[0] - {"kmeabuh"}, REAL["register"]()[1]))

# 14 -- the NEGATIVE half: a word of HIS shape is listed
run("a word of his shape is listed (samul)", True,
    register=lambda: (REAL["register"]()[0] | {"samul"}, REAL["register"]()[1]))

# 15 -- the audio wiring moved
run("an audio id was minted", True, AUDIO_IDS=5133)

# 16 -- the metric fell
run("the pair count falls below the floor", True, FLOOR=5332)

print("\n%d of %d control cases behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
