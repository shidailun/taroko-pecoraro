# -*- coding: utf-8 -*-
"""Negative control for dom225.py.

Each case injects a state the log is supposed to catch and requires a FAIL. The
injected values are picked from the run just done, not from the notes -- a
control keyed on the notes proves nothing and reads as proof (batch 222).
"""
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location(
    "dom225", os.path.join(ROOT, "tools", "orthography", "logs", "dom225.py"))
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
    got = "refused" if rc != 0 else "passed"
    print("%-52s -> %s (%s)\n" % (name, got, "good" if ok else "BAD"))
    restore()
    return ok


results = []

# 1 -- the freeze reinstated: a key sends to the dog name again
m.modern_map = lambda: dict(REAL["modern_map"](), kubwi="kubuy")
results.append(run("kubwi drifts back to kubuy (the freeze)", True))

# 2 -- the stem drops out of verified.js, so the head goes pale
m.verified = lambda: {k: v for k, v in REAL["verified"]().items() if k != "kbuyu"}
results.append(run("kbuyu dropped from verified.js", True))

# 3 -- the listed gloss this ruling cites is gone
def _noglos():
    am, ag = REAL["register"]()
    ag = dict(ag)
    ag["kbuyu"] = ["打獵"]                    # 草叢 removed
    return am, ag
m.register = _noglos
results.append(run("kbuyu loses 草叢 from its gloss", True))

# 4 -- the root stops being listed: regular('pkbuyu') can no longer derive it
def _unlisted():
    am, ag = REAL["register"]()
    return set(am) - {"kbuyu"}, ag
m.register = _unlisted
results.append(run("kbuyu no longer listed in the register", True))

# 5 -- the consistency fix turns into a CLAIM by entering verified.js
m.verified = lambda: dict(REAL["verified"](), knbuyu=1)
results.append(run("knbuyu entered verified.js (pale -> a claim)", True))

# 6 -- the negative half: an unreduplicated kn- form arrives
def _arrived():
    am, ag = REAL["register"]()
    return set(am) | {"knbuyu"}, ag
m.register = _arrived
results.append(run("register gains knbuyu (re-opens the refusal)", True))

# 7 -- the trap acquires his meaning, which would re-open the ruling
def _trapmoves():
    am, ag = REAL["register"]()
    ag = dict(ag)
    ag["kubuy"] = ["狗名", "遮蔽"]
    return am, ag
m.register = _trapmoves
results.append(run("kubuy gains 遮蔽 (the freeze account dies)", True))

# 8 -- collapsed() stops dropping the bracket, so the head renders twice
m.JS = REAL["JS"].replace("return {tot:", "seen['kbuyu'] = 2; return {tot:")
results.append(run("kbuyu renders twice (bracket not collapsed)", True))

# 9 -- FURNITURE: the value turns up inside a .truku box after all
m.JS = REAL["JS"].replace("return {tot:", "inTruku['kbuyu'] = 1; return {tot:")
results.append(run("kbuyu appears in a .truku span (0-pair claim)", True))

# 10 -- an audio id lost. No audio work until the text is at 100 and there is
# a voice; an id is a URL and a re-minted one unhooks a paid-for clip.
m.audio_ids = lambda: set(list(REAL["audio_ids"]())[:-1])
results.append(run("one audio id lost", True))

# 11 -- positive control: untouched, must pass
results.append(run("UNTOUCHED (positive control)", False))

print("%d of %d control cases behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
