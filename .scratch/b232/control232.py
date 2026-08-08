# -*- coding: utf-8 -*-
"""Negative control for `logs/dom232.py`.

A log that cannot fail is a list of excuses (batch 209). dom232 asserts a HELD
metric, a repaired refusal and three sweeps that all came back empty -- and an
empty sweep is exactly the shape a BROKEN sweep has. So every assertion is
tampered with here and required to refuse, the emptiness ones twice: once by
moving the pin, once by moving the DATA under it.

The expensive halves (the browser measurement, the parquets) are taken once and
memoised, so the ~35 re-runs of `main()` cost one page load between them.

    python .scratch/b232/control232.py
"""
import contextlib
import copy
import importlib.util
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

# --- memoise the slow reads -------------------------------------------------
_D = M.measure()
_C = {False: M.corpus(False), True: M.corpus(True)}
_S = M.sources()
_E = M.entries_json()
_T = M.his_tokens()
_MM = M.modern_map()
_A = M.audio_ids()

BASE = dict(measure=lambda: copy.deepcopy(_D),
            corpus=lambda with_zh=False: copy.deepcopy(_C[with_zh]),
            sources=lambda: copy.deepcopy(_S),
            entries_json=lambda: copy.deepcopy(_E),
            his_tokens=lambda: dict(_T),
            modern_map=lambda: dict(_MM),
            audio_ids=lambda: list(_A))
PINS = dict((k, getattr(M, k)) for k in
            ("FLOOR", "DENOM", "AUDIO_IDS", "SOLE_PAIRS", "SOLE_TYPES",
             "HIS_CARDS", "BICYCLE_NOTE", "ICE_ROOT", "ICE_FAMILY_MIN",
             "HIS_GAQAT", "HIS_GAKAT", "GAQAT_ICE", "GAQAT_BIKE", "CITED",
             "JOIN_PALE", "JOIN_CONTROL", "JOIN_ALL_DARK", "CORPUS_ROWS",
             "SENT_PROPOSALS", "SENT_LIVE", "SENT_TRAP", "SPELL_SHAPES",
             "SPELL_LIVE", "STOP_N", "STOP_MUST"))
bad = 0


def run(**patch):
    """Run dom232's main() under a patch; return its FAIL lines."""
    for k, v in BASE.items():
        setattr(M, k, v)
    for k, v in PINS.items():
        setattr(M, k, v)
    for k, v in patch.items():
        setattr(M, k, v)
    M.fails[:] = []
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        M.main()
    return list(M.fails)


def check(name, must_refuse, **patch):
    global bad
    fs = run(**patch)
    good = bool(fs) == must_refuse
    if not good:
        bad = 1
    print("%-4s %-58s %s" % ("ok" if good else "BAD", name,
                             (fs[0] if fs else "explained")[:80]))


def tamper(fn):
    """Return a callable producing a mutated copy of one memoised read."""
    def w():
        return fn()
    return w


# --- positive control: untouched, dom232 is green ---------------------------
check("untouched -- every assertion EXPLAINED", False)


# === the metric =============================================================
def moved(**kw):
    d = copy.deepcopy(_D)
    for k, v in kw.items():
        d[k] = v
    return lambda: d


check("the metric FELL by one pair", True, measure=moved(ok=_D["ok"] - 1))
check("the metric ROSE by one pair", True, measure=moved(ok=_D["ok"] + 1))
check("the denominator moved", True, measure=moved(tot=_D["tot"] + 1))
check("an audio id was minted", True,
      audio_ids=lambda: list(_A) + ["ex_new"])
check("an audio id was dropped", True, audio_ids=lambda: list(_A)[:-1])

_sole = dict(_D["sole"])
check("a sole blocker was cleared", True,
      measure=moved(sole=dict((k, v) for k, v in _sole.items()
                              if k != "mqlaq")))
check("a sole blocker gained a pair", True,
      measure=moved(sole=dict(_sole, mqlaq=_sole.get("mqlaq", 0) + 1)))


# === GAQAT: the refusal =====================================================
check("the map now sends gaqat -> gakat", True,
      modern_map=lambda: dict(_MM, gaqat="gakat"))
check("gaqat stopped rendering pale", True,
      measure=moved(unv=dict((k, v) for k, v in _D["unv"].items()
                             if k != "gaqat")))
check("gakat stopped rendering dark", True,
      measure=moved(seen=dict((k, v) for k, v in _D["seen"].items()
                              if k != "gakat")))
check("gaqat's sole-blocked pairs moved", True,
      measure=moved(sole=dict(_sole, gaqat=1)))


def ent_less(hw, key, sub):
    e = copy.deepcopy(_E)
    for x in e:
        if x.get("hw") == hw and isinstance(x.get(key), str):
            x[key] = x[key].replace(sub, "")
        if x.get("hw") == hw:
            for ex in (x.get("examples") or []):
                if isinstance(ex.get("zh"), str):
                    ex["zh"] = ex["zh"].replace(sub, "")
    return lambda: e


check("his GAKAT card lost the posture gloss", True,
      entries_json=ent_less("GAKAT", "zh", "蹲"))
check("his GAQAT card lost the ice gloss", True,
      entries_json=ent_less("GAQAT", "zh", "冰"))
check("his GAKAT example lost the bicycle etymology", True,
      entries_json=ent_less("GAKAT", "zzz", M.BICYCLE_NOTE))


def src(mut):
    s = copy.deepcopy(_S)
    mut(s)
    return lambda: s


check("the register's gakat stopped being a posture root", True,
      sources=src(lambda s: (s[1].pop("gakat", None), s[3].pop("gakat", None))))
check("the huda ice family fell away", True,
      sources=src(lambda s: [d.pop(w, None) for d in (s[1], s[2], s[3])
                             for w in list(d) if M.ICE_ROOT in w]))
# THE NEWS: the negative half is a regex, so a gaqat-shaped 冰 must re-open it
check("a gaqat-shaped word entered the register glossed 冰", True,
      sources=src(lambda s: s[1].__setitem__("gaqat", ["冰塊"])))
check("...and at one edit, not zero", True,
      sources=src(lambda s: s[1].__setitem__("gaqit", ["冰柱"])))
check("...but a gaqat-shaped word glossed something ELSE is not news", False,
      sources=src(lambda s: s[1].__setitem__("gaqit", ["跳躍"])))

check("his gaqat count moved", True,
      his_tokens=lambda: dict(_T, gaqat=_T.get("gaqat", 0) + 1))
check("his gakat count moved", True,
      his_tokens=lambda: dict(_T, gakat=99))
check("the sense split moved -- an ice token became a bicycle", True,
      GAQAT_ICE=1)
check("the refusal this batch repairs left dom214.py", True,
      CITED=(("dom214.py", "a sentence dom214 does not contain"),))


# === sweep 1: the join sweep ================================================
check("the join sweep's own pin says it found one", True, JOIN_PALE=1)
check("the positive control names a join it cannot recover", True,
      JOIN_CONTROL=("kasayang", "isoka", "xnotaword"))
check("the widened sweep's dark-row count moved", True, JOIN_ALL_DARK=7)
# and the DATA leg: an empty corpus makes every join sweep return nothing, so
# a pin asserting 0 would pass on a broken instrument. The control leg is what
# refuses -- it can no longer find kasayang either.
check("the parquets returned no rows at all", True,
      corpus=lambda with_zh=False: ([] if with_zh else []))
# parquets UNPLUGGED is a skip, not a pass: corpus() returns None
check("the parquets are unmounted -- sweeps 1 and 2 SKIP, nothing claimed",
      False, corpus=lambda with_zh=False: None)


# === sweep 2: the sentence sweep ============================================
check("the sentence sweep's proposal count moved", True, SENT_PROPOSALS=12)
check("the corpus row floor was breached", True, CORPUS_ROWS=10 ** 7)
check("the sweep can no longer see batch 231's written refusal", True,
      SENT_TRAP=("yianu", "xyamu"))
check("the sweep can no longer see its one adjudicable row", True,
      SENT_PROPOSALS=13, sources=src(
          lambda s: s[0].discard("gakat") if isinstance(s[0], set)
          else s[0].pop("gakat", None)))


# === sweep 4: the spellchecker ==============================================
check("the spellcheck shape count moved", True, SPELL_SHAPES=39)
check("a shape survived the gloss test", True, SPELL_LIVE=1)
# the DERIVED stoplist: too shallow and the apparatus comes back as evidence
check("the stoplist was cut above the characters the record named", True,
      STOP_N=10)
check("the stoplist demands a character the register does not lead with", True,
      STOP_MUST=set("的人是著子一龘"))
# ...and too deep is news too: at 300 characters the stoplist eats real meaning
check("...while the pinned depth 30 still reproduces all six", False, STOP_N=30)

print("\n%s" % ("all controls behaved" if not bad
                else "SOMETHING BEHAVED BADLY"))
sys.exit(bad)
