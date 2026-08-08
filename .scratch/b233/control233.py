# -*- coding: utf-8 -*-
"""Negative control for `logs/dom233.py`. A pin that cannot fail is not a pin.

Every assertion in the log is moved and required to refuse -- the metric both
ways, the ruling itself in all three files it touches, the argument beside it,
his own page, the gloss test on the family, the neighbourhood, the DOM collapse,
and the whole tag-furniture class. Two legs are the ones worth reading:

  * the neighbourhood pin is a FLOOR (batch 209), so the control has to show it
    discriminating: a register word arriving one edit away and carrying a
    character of HIS gloss refuses, one glossed 跳躍 does not, and `psranaq`
    LEAVING refuses. Three legs, not one;
  * the collapse is asserted as a DELETION, so the control puts the span back --
    both as a pale `PSAANAQ` and as a DARK one -- and both must refuse. A log
    written to wait for `w-mod` would pass the second.

    python .scratch/b233/control233.py            # site served at :8765
"""
import contextlib
import copy
import importlib.util
import io as _io
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom233", "tools/orthography/logs/dom233.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

# ---- capture the real world once -----------------------------------------
_D = M.measure()
_ENT = M.entries_json()
_MM = M.modern_map()
_MAN = M.manual_map()
_VER = M.verified()
_SRC = M.sources()
_CR = M.char_rules

BASE = dict(
    measure=lambda: copy.deepcopy(_D),
    entries_json=lambda: copy.deepcopy(_ENT),
    modern_map=lambda: dict(_MM),
    manual_map=lambda: dict(_MAN),
    verified=lambda: dict(_VER),
    sources=lambda: copy.deepcopy(_SRC),
    char_rules=_CR,
)
PINS = dict((k, getattr(M, k)) for k in
            ("FLOOR", "DENOM", "AUDIO_IDS", "SOLE_PAIRS", "SOLE_TYPES",
             "RULED", "RULED_TO", "HIS_CARD", "MODERN_CARD", "HIS_TAG",
             "HIS_ZH", "HIS_OCCURRENCES", "FAMILY", "NEAR", "NEIGHBOUR",
             "NEIGHBOUR_FAMILY", "CHARRULE_ID", "TAGS", "TAGS_RENDERED",
             "VARIANT_BESIDE_ROOT", "TAG_DARK", "TAG_PALE", "TAG_GREEN",
             "TAG_TRUKU", "SHAPES", "B225_GREEN"))
bad = 0


def run(**patch):
    for k, v in BASE.items():
        setattr(M, k, v)
    for k, v in PINS.items():
        setattr(M, k, v)
    for k, v in patch.items():
        setattr(M, k, v)
    M.fails[:] = []
    with contextlib.redirect_stdout(_io.StringIO()):
        M.main()
    return list(M.fails)


def case(name, must_refuse, **patch):
    global bad
    fs = run(**patch)
    ok = bool(fs) == must_refuse
    if not ok:
        bad = 1
    print("%-4s %-56s %s" % ("ok" if ok else "BAD", name,
                             (fs[0] if fs else "explained")[:70]))
    return fs


def D(**over):
    d = copy.deepcopy(_D)
    d.update(over)
    return lambda: d


def MAP(**over):
    m = dict(_MM)
    for k, v in over.items():
        if v is None:
            m.pop(k, None)
        else:
            m[k] = v
    return lambda: m


print("== the world as it is")
case("the real book explains itself", False)

print("\n== the metric")
case("pairs FELL below the floor", True, measure=D(ok=_D["ok"] - 1))
case("pairs rose (a gain is not a failure)", False,
     measure=D(ok=_D["ok"] + 1))
case("the denominator moved", True, measure=D(tot=_D["tot"] - 1))
case("an audio id was minted", True, AUDIO_IDS=M.AUDIO_IDS - 1)
case("a sole blocker was gained", True,
     measure=D(sole=dict(_D["sole"], zzz=9)), SOLE_TYPES=len(_D["sole"]))

print("\n== the ruling, in all three files")
case("the map reverted to his own letters", True,
     modern_map=MAP(psaanaq="psaanaq"))
case("the map drifted to a third spelling", True,
     modern_map=MAP(psaanaq="pseanaq"))
case("the map entry was deleted", True, modern_map=MAP(psaanaq=None))
case("manual_map.json lost the ruling", True,
     manual_map=lambda: dict((k, v) for k, v in _MAN.items()
                             if k != "psaanaq"))
case("the argument beside it was deleted", True,
     manual_map=lambda: dict((k, v) for k, v in _MAN.items()
                             if not k.startswith("_psaanaq")))
case("the argument was reduced to a label", True,
     manual_map=lambda: dict(
         (k, ("his own parenthetical. [b233]" if k.startswith("_psaanaq")
              else v)) for k, v in _MAN.items()))
case("the argument stopped citing batch 212 (the scan)", True,
     manual_map=lambda: dict(
         (k, (v.replace("batch 212", "obviously") if k.startswith("_psaanaq")
              else v)) for k, v in _MAN.items()))
case("the VALUE went pale in verified.js", True,
     verified=lambda: dict((k, v) for k, v in _VER.items() if k != "pseanak"))

print("\n== his own page")


def ent(fn):
    def f():
        e = copy.deepcopy(_ENT)
        for x in e:
            fn(x)
        return e
    return f


case("his tag was rewritten", True,
     entries_json=ent(lambda x: x.__setitem__("tag", "(PSAANAQ)")
                      if x.get("hw") == "PSAANAK" else None))
case("his Chinese was rewritten", True,
     entries_json=ent(lambda x: x.__setitem__("zh", "分開。")
                      if x.get("hw") == "PSAANAK" else None))
case("a SECOND occurrence of his string appeared", True,
     entries_json=ent(lambda x: x.__setitem__("fr", str(x.get("fr")) + " PSAANAQ")
                      if x.get("hw") == "PSANYAQ" else None))

print("\n== the gloss test")


def src(fn):
    def f():
        s = copy.deepcopy(_SRC)
        fn(s)
        return s
    return f


case("seanak lost the 視 his 歧視 was ruled on", True,
     sources=src(lambda s: s[1].__setitem__("seanak", ["分開"])))
# NB the log reads all THREE gloss sources, so patching attested_gloss alone
# leaves bible_gloss carrying 隔開 and the leg passes for the wrong reason.
case("ptgeanak lost the 隔 his 隔離 was ruled on", True,
     sources=src(lambda s: [d.__setitem__("ptgeanak", ["分開"])
                            for d in (s[1], s[2], s[3])]))
case("the VALUE left attested_modern", True,
     sources=src(lambda s: s[0].discard("pseanak")))
case("the tag's dark neighbour lost its 禁忌 family", True,
     sources=src(lambda s: [s[1].__setitem__(w, ["女人陰部"])
                            for w in ("gmpsaniq", "ppsaniq")]))

print("\n== the neighbourhood -- a FLOOR, so three legs")
case("his string became listed after all", True,
     sources=src(lambda s: s[1].__setitem__("psaanaq", ["歧視"])))
case("psranaq LEFT the neighbourhood", True,
     sources=src(lambda s: (s[0].discard("psranaq"),
                            s[1].pop("psranaq", None))))
rv = case("a NEW neighbour carries a character of his gloss", True,
          sources=src(lambda s: (s[0].add("psaanak"),
                                 s[1].__setitem__("psaanak", ["歧視他人"]))))
if rv:
    ok = "different-root test" in rv[0]
    bad = bad or (0 if ok else 1)   # never CLEAR an earlier failure
    print("%-4s %-56s %s" % ("ok" if ok else "BAD",
                             "...and it refuses with the RIVAL message",
                             rv[0][:70]))
case("a new neighbour glossed 跳躍 is not news", False,
     sources=src(lambda s: (s[0].add("psaanak"),
                            s[1].__setitem__("psaanak", ["跳躍"]))))
case("charRules started spelling his string itself", True,
     char_rules=lambda w: "pseanak" if w == "psaanaq" else _CR(w))

print("\n== the collapse, asserted as a DELETION")
CARD = [t for t in _D["tags"] if t[0] == "PSEANAK"]
OTHER = [t for t in _D["tags"] if t[0] != "PSEANAK"]


def tags(rows):
    d = copy.deepcopy(_D)
    d["tags"] = rows
    return lambda: d


case("the parenthetical is printed again, PALE", True,
     measure=tags(OTHER + [["PSEANAK", "(PSAANAQ?) (= PSANIQ?)",
                            [["PSAANAQ", "w-unv", False]] + CARD[-1][2]]]))
case("...and printed again DARK -- a w-mod probe would pass this", True,
     measure=tags(OTHER + [["PSEANAK", "(PSAANAQ?) (= PSANIQ?)",
                            [["PSAANAQ", "w-mod", False]] + CARD[-1][2]]]))
case("his string renders anywhere else in the book", True,
     measure=D(seen=dict(_D["seen"], psaanaq=1),
               unv=dict(_D["unv"], psaanaq=1)))
case("the card stopped rendering as PSEANAK (batch 226's case trap)", True,
     measure=tags(OTHER))

print("\n== the class")
case("a tag span moved inside a .truku box", True,
     measure=tags(OTHER + [[c[0], c[1], [[s[0], s[1], True] for s in c[2]]]
                           for c in CARD]))
case("a tag span went pale", True,
     measure=tags(OTHER + [[c[0], c[1], [[s[0], "w-unv", s[2]] for s in c[2]]]
                           for c in CARD]))
case("one of batch 225's five gained his root mark", True,
     entries_json=ent(lambda x: x.__setitem__("tag", "(SILAP ?) (R.)")
                      if x.get("hw") == "SLAP" else None))
case("a rendered tag count moved", True, TAGS_RENDERED=M.TAGS_RENDERED - 1)
case("the variant-shape count moved", True,
     VARIANT_BESIDE_ROOT=M.VARIANT_BESIDE_ROOT + 1)
case("the shape split changed", True, SHAPES=dict(M.SHAPES, variant=1))

print("\n%s" % ("all controls behaved" if not bad
                else "SOMETHING BEHAVED BADLY"))
sys.exit(bad)
