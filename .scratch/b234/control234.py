# -*- coding: utf-8 -*-
"""Negative control for `logs/dom234.py`. A pin that cannot fail is not a pin.

Every assertion is moved and required to refuse. Four legs are the ones worth
reading, because each is a place this log could have passed for the wrong
reason:

  * **the e-dictionary legs must DISCRIMINATE.** `ASKED_HITS == 0` and the
    never-asked containment would both be satisfied by an instrument that had
    simply stopped being consulted, so the control asks a value and returns a
    MISS (must not refuse) as well as a HIT (must refuse), and adds a pale value
    nobody ever asked (must refuse);
  * **the negative half of the refusal is a property, not a list** (batch 229),
    so a new 口水 carrier that does NOT take a `k-` must not be news, while one
    that does must be — and with the register-has-stopped-being-silent message;
  * **the standing test has to fire on a DELETION as well as on an arrival.**
    Injecting a blocker nobody has written about refuses; injecting one that
    already carries a written refusal does not; and stripping THIS batch's own
    refusal out of the record puts `kyuqan` back on the unworked list, which is
    what makes the log part of the record it reads;
  * **a control that can clear its own earlier failure proves nothing** (batch
    233), so every message check is `bad = bad or ...`, never `0 if ok else 1`.

    python .scratch/b234/control234.py            # site served at :8765
"""
import contextlib
import copy
import importlib.util
import io as _io
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom234", "tools/orthography/logs/dom234.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

# ---- capture the real world once -----------------------------------------
_D = M.measure()
_ENT = M.entries_json()
_MM = M.modern_map()
_VER = M.verified()
_SRC = M.sources()
_ED = M.edictionary()
_REC = M.record()

BASE = dict(
    measure=lambda: copy.deepcopy(_D),
    entries_json=lambda: copy.deepcopy(_ENT),
    modern_map=lambda: dict(_MM),
    verified=lambda: dict(_VER),
    sources=lambda: copy.deepcopy(_SRC),
    edictionary=lambda: dict(_ED),
    record=lambda: copy.deepcopy(_REC),
)
PINS = dict((k, getattr(M, k)) for k in
            ("FLOOR", "DENOM", "AUDIO_IDS", "SOLE_TYPES", "ASKED_HITS",
             "NEVER_ASKED", "FRENCH", "TFR_ROWS", "HIS", "VAL",
             "HIS_OCCURRENCES", "SIB", "SIB_VAL", "ROOT", "ROOT_ZH",
             "SLOT_SISTERS", "RIVAL", "RIVAL_ZH", "UNWORKED"))
bad = 0


def run(**patch):
    for k, v in list(BASE.items()) + list(PINS.items()):
        setattr(M, k, v)
    for k, v in patch.items():
        setattr(M, k, v)
    M.fails[:] = []
    with contextlib.redirect_stdout(_io.StringIO()):
        M.main()
    return list(M.fails)


def case(name, must_refuse, want=None, **patch):
    global bad
    fs = run(**patch)
    ok = bool(fs) == must_refuse
    if ok and want:
        ok = any(want in f for f in fs)
    if not ok:
        bad = bad or 1            # never CLEAR an earlier failure
    print("%-4s %-58s %s" % ("ok" if ok else "BAD", name,
                             (fs[0] if fs else "explained")[:66]))
    return fs


def D(**over):
    d = copy.deepcopy(_D)
    d.update(over)
    return lambda: d


def MAP(**over):
    m = dict(_MM)
    for k, v in over.items():
        m.pop(k, None) if v is None else m.__setitem__(k, v)
    return lambda: m


def ED(**over):
    e = dict(_ED)
    for k, v in over.items():
        e.pop(k, None) if v == "unask" else e.__setitem__(k, v)
    return lambda: e


def SRC(fn):
    def f():
        s = copy.deepcopy(_SRC)
        fn(s)
        return s
    return f


def ENT(fn):
    def f():
        e = copy.deepcopy(_ENT)
        for x in e:
            fn(x)
        return e
    return f


print("== the world as it is")
case("the real book explains itself", False)

print("\n== the metric")
case("pairs FELL below the floor", True, measure=D(ok=_D["ok"] - 1))
case("pairs rose (a gain is not a failure)", False, measure=D(ok=_D["ok"] + 1))
case("the denominator moved", True, measure=D(tot=_D["tot"] - 1))
case("an audio id was minted", True, AUDIO_IDS=M.AUDIO_IDS - 1)
case("a sole-blocker type was gained", True,
     measure=D(sole=dict(_D["sole"], zzzsole=1)), SOLE_TYPES=M.SOLE_TYPES)

print("\n== 1. the e-dictionary at the pale -- it must DISCRIMINATE")
case("a pale value came back LISTED", True, "re-opened",
     edictionary=ED(mqlaq=[{"word": "mqlaq"}]))
case("a never-asked value was asked and MISSED (not news)", False,
     edictionary=ED(shkun=None))
case("a never-asked value was asked and HIT", True, "re-opened",
     edictionary=ED(shkun=[{"word": "shkun"}]))
case("a value already asked was UN-asked", True, "never asked",
     edictionary=ED(**{"ayuq": "unask"}))
case("a new pale map value nobody ever asked appeared", True, "never asked",
     modern_map=MAP(zzztok="zzzval"))
case("a pale value went dark (a ruling is not a failure)", False,
     verified=lambda: dict(_VER, mqlaq=1))

print("\n== 3. the French leakage is INERT, which is the whole claim")
case("a French map value renders as a span", True, "no longer inert",
     measure=D(seen=dict(_D["seen"], grand=1), unv=dict(_D["unv"], grand=1)))
case("a French map value left the map", True, "changed shape",
     modern_map=MAP(grand=None))
case("his t == fr demonstration rows were re-filed", True, "t == fr rows",
     entries_json=ENT(lambda x: [ex.__setitem__("fr", "Grandeur.")
                                 for sb in (x.get("subs") or [])
                                 for ex in (sb.get("examples") or [])]
                      if x.get("hw") == "AN" else None))

print("\n== 2. the refusal -- both halves")
case("the map reverted to his own letters", True, modern_map=MAP(kyoqan=None))
case("the map drifted to a third spelling", True,
     modern_map=MAP(kyoqan="ktuyuqan"))
case("someone spelled it his sibling's way", True,
     modern_map=MAP(kyoqan="tuyuqan"))
case("the VALUE went DARK -- the refusal is overturned", True,
     "It was refused because", verified=lambda: dict(_VER, kyuqan=1))
case("his row stopped being a blocked pair", True, "sole blocker",
     measure=D(sole=dict((k, v) for k, v in _D["sole"].items()
                         if k != "kyuqan")))
case("a SECOND occurrence of his hapax appeared", True, "a second reading",
     entries_json=ENT(lambda x: [ex.__setitem__("t", str(ex.get("t")) + " kyoqan")
                                 for sb in (x.get("subs") or [])
                                 for ex in (sb.get("examples") or [])]
                      if x.get("hw") == "TUYOQ" else None))
case("his Tyoqan stopped glossing as a crachat", True, "crachat",
     entries_json=ENT(lambda x: [s.__setitem__("fr", "Salive.")
                                 for s in (x.get("subs") or [])
                                 if (s.get("form") or "").lower() == M.SIB]
                      if x.get("hw") == "TUYOQ" else None))
case("the dark sibling went pale", True, "positive half",
     verified=lambda: dict((k, v) for k, v in _VER.items() if k != "tuyuqan"))
case("the root lost its 痰", True,
     sources=SRC(lambda s: [d.__setitem__("tuyuq", ["口"])
                            for d in (s[1], s[2], s[3])]))
case("the k...an slot stopped being spelled for other stems", True,
     "empty candidate list",
     sources=SRC(lambda s: [s[0].discard(w) for w in M.SLOT_SISTERS]))
case("a 口水 word arrived that does NOT take a k- (not news)", False,
     sources=SRC(lambda s: (s[0].add("tmuyuq"),
                            s[1].__setitem__("tmuyuq", ["吐口水"]))))
case("a 口水 word arrived that DOES take a k-", True, "stopped being silent",
     sources=SRC(lambda s: (s[0].add("ktuyuqan"),
                            s[1].__setitem__("ktuyuqan", ["滿臉口水"]))))
case("the tuyuq family left the 口水 carriers", True, "positive half",
     sources=SRC(lambda s: [d.pop(w, None) for d in (s[1], s[2], s[3])
                            for w in list(d) if w.startswith("tuyuq")]))
case("khalus lost the 沾滿唾液 the rival root is named on", True,
     sources=SRC(lambda s: [d.__setitem__("khalus", ["口水"])
                            for d in (s[1], s[2], s[3])]))

print("\n== 4. the standing test, on an arrival AND on a deletion")
case("a blocker nobody has written about appeared", True,
     "no refusal-shaped sentence",
     measure=D(sole=dict(_D["sole"], zzzqan=1)),
     SOLE_TYPES=len(_D["sole"]) + 1)
case("a blocker that already carries a refusal appeared", False,
     measure=D(sole=dict(_D["sole"], snoxel=1)),
     SOLE_TYPES=len(_D["sole"]) + 1)
case("THIS batch's refusal was struck from the record", True,
     "no refusal-shaped sentence",
     record=lambda: [(n, [ln for ln in L
                          if "kyuqan" not in ln.lower()
                          and "kyoqan" not in ln.lower()])
                     for n, L in _REC])
case("the record was emptied entirely", True, "no refusal-shaped sentence",
     record=lambda: [])

print("\n%s" % ("all controls behaved" if not bad else "SOMETHING BEHAVED BADLY"))
sys.exit(bad)
