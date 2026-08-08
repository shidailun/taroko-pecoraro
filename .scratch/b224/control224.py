# -*- coding: utf-8 -*-
"""Negative control for dom224.py -- a log that cannot fail is a list of excuses.

Each case injects a state the log is supposed to catch and requires a FAIL. The
values are picked from the run just done, not from the notes (batch 222).
"""
import importlib.util
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location(
    "dom224", os.path.join(ROOT, "tools", "orthography", "logs", "dom224.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

REAL = dict(verified=m.verified, modern_map=m.modern_map, register=m.register,
            audio_ids=m.audio_ids, entries_text=m.entries_text, JS=m.JS)


def restore():
    for k, v in REAL.items():
        setattr(m, k, v)


def run(name, expect_fail):
    rc = m.main()
    ok = (rc != 0) if expect_fail else (rc == 0)
    # say what actually happened: a tampered case must be REFUSED, and the
    # untouched case must PASS. One word for both reads as proof of nothing.
    got = "refused" if rc != 0 else "passed"
    print("%-46s -> %s (%s)\n" % (name, got, "good" if ok else "BAD"))
    restore()
    return ok


results = []

# 1 -- the ruling dropped out of verified.js: the value goes pale again
m.verified = lambda: {k: v for k, v in REAL["verified"]().items()
                      if k != "graka"}
results.append(run("graka dropped from verified.js", True))

# 2 -- the map respelled the card without redoing the gloss argument
m.modern_map = lambda: dict(REAL["modern_map"](), glaqa="graqa")
results.append(run("map drifts glaqa -> graqa", True))

# 3 -- the form whose OWN gloss carries the character loses it
def _noglos():
    am, ag = REAL["register"]()
    ag = dict(ag)
    ag["grkaan"] = ["埋伏"]           # 監視 removed; the gloss test's basis gone
    return am, ag
m.register = _noglos
results.append(run("grkaan loses 監視 from its gloss", True))

# 4 -- the negative half of the refusal: an -i form of the stem arrives
def _arrived():
    am, ag = REAL["register"]()
    return set(am) | {"psnmai"}, ag
m.register = _arrived
results.append(run("register gains psnmai (re-opens refusal)", True))

# 5 -- the trap's gloss changes, so the account of WHY it was refused dies
def _notrap():
    am, ag = REAL["register"]()
    ag = dict(ag)
    ag["raka"] = ["埋伏"]
    return am, ag
m.register = _notrap
results.append(run("raka stops being a personal name", True))

# 6 -- an audio id lost. No audio work is permitted until there is a voice.
m.audio_ids = lambda: set(list(REAL["audio_ids"]())[:-1])
results.append(run("one audio id lost", True))

# 7 -- FURNITURE: the value turns up inside a .truku box after all
m.JS = REAL["JS"].replace("return {tot:",
                          "inTruku['graka'] = 1; return {tot:")
results.append(run("graka appears in a .truku span", True))

# 8 -- positive control: untouched, must pass
results.append(run("UNTOUCHED (positive control)", False))

print("%d of %d control cases behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
