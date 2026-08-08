# -*- coding: utf-8 -*-
"""Negative control for logs/dom228.py. One measurement, replayed.

Every assertion is tampered with in turn and required to FAIL; two untouched or
irrelevant cases are required to PASS. A log that cannot fail is a list of
excuses (batch 209); a log that fails on anything is just as useless.
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
    "dom228", os.path.join(ROOT, "tools", "orthography", "logs", "dom228.py"))
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)

print("measuring once ...")
DOM = D.measure()
REAL = dict(measure=D.measure, modern_map=D.modern_map, verified=D.verified,
            register=D.register, char_rules=D.char_rules,
            audio_ids=D.audio_ids, entries_text=D.entries_text)
CONST = dict((k, getattr(D, k)) for k in
             ("FLOOR", "DENOM", "AUDIO_IDS", "RULED", "HIS", "BASE_WORD",
              "BASE_GLOSS", "SENTENCE", "STEM_FORMS", "HH_FLOOR", "HH_AN_FLOOR",
              "NO_RIVAL_PARSE", "RIVAL_CHARS", "OTHER_ROOT", "FURNITURE"))
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
    print("%-50s -> %s%s" % (name,
                             ("refused: " + out[0][5:62]) if out else "passed",
                             "" if ok else "   <<< BAD"))
    results.append(ok)


AM0, AG0 = REAL["register"]()

# 1, 2 -- positive controls
run("UNTOUCHED", False)
run("an unrelated word goes pale", False,
    dom=lambda d: (d["seen"].update(zzz=2), d["unv"].update(zzz=2), d)[-1])

# 3 -- the ruling comes back out of verified.js
run("hhtran leaves verified.js", True,
    verified=lambda: {k: v for k, v in REAL["verified"]().items() if k != "hhtran"})

# 4 -- ... or renders pale anyway (the DOM is the authority, not the table)
run("hhtran renders pale on the page", True,
    dom=lambda d: (d["unv"].update(hhtran=1), d)[-1])

# 5 -- it is still the sole blocker: the pair was not actually bought
run("hhtran still sole-blocks a pair", True,
    dom=lambda d: (d["sole"].update(hhtran=1), d)[-1])

# 6 -- FURNITURE trap: dark, but in no sentence, so it bought nothing
run("hhtran is in no .truku box", True,
    dom=lambda d: (d["inTruku"].pop("hhtran", None), d)[-1])

# 7 -- the map drifts to another spelling
run("map sends xxtlan somewhere else", True,
    modern_map=lambda: dict(REAL["modern_map"](), xxtlan="hhtur"))

# 8 -- the char rules stop producing it unaided
run("charRules no longer gives hhtran", True, char_rules=lambda w: "hhtur")

# 9 -- his sentence changed under the ruling (a transcription edit)
run("his Psmuk sentence was edited", True,
    SENTENCE="Pnsmuk ko daxa ktinox lex xxtlaN mo bgixol")

# 10 -- the gloss that ruled it is gone
run("htran loses 阻擋", True,
    register=lambda: (AM0, dict(AG0, htran=["塞住"])))

# 11 -- the bare stem loses forms
run("the htr- stem loses htrun", True,
    register=lambda: (AM0 - {"htrun"}, AG0))

# 12 -- the hh- population collapses below the floor the argument was made on
run("hh- population falls below 120", True, HH_FLOOR=999)

# 13 -- batch 224's slot test stops holding
run("hh-...-an is spelled for no other stem", True, HH_AN_FLOOR=999)

# 14 -- a rival parse appears: hh- + tran becomes readable
run("a rival parse `tran` is listed", True,
    register=lambda: (AM0 | {"tran"}, AG0))

# 15 -- a rival root for his meaning appears
run("a register word gains 屏障", True,
    register=lambda: (AM0 | {"zzzq"}, dict(AG0, zzzq=["屏障"])))

# 16 -- the other 阻擋 root leaves; the different-root half needs re-arguing
run("bbaat leaves the register", True,
    register=lambda: (AM0 - {"bbaat"}, AG0))

# 17 -- the seam re-prices: a furniture redup starts blocking a pair
run("ggar starts blocking a pair", True,
    dom=lambda d: (d["sole"].update(ggar=1), d)[-1])

# 18 -- the audio wiring moved
run("an audio id was minted", True, AUDIO_IDS=5133)

# 19 -- the metric fell back to where batch 227 left it
run("the pair count falls to 5331", True, FLOOR=5333)

print("\n%d of %d control cases behaved correctly" % (sum(results), len(results)))
sys.exit(0 if all(results) else 1)
