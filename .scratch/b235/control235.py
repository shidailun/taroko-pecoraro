# -*- coding: utf-8 -*-
"""Negative control for `logs/dom235.py`. A pin that cannot fail is not a pin.

Every assertion is moved and required to refuse. The legs worth reading are the
ones where this log could have passed for the wrong reason:

  * **a control leg that patches the wrong field passes for FREE** (batch 234).
    The rarity leg and the `nalong` hapax count are measured off his Truku `t`
    fields, so each is moved by writing `t` AND paired with the same string
    written to `fr`, which must NOT refuse. Every patch that edits an existing
    card asserts it matched something (`hit()`), so a patch that reaches no
    field is a BAD rather than an explanation.
  * **the register legs must read all three gloss files** (batch 230). Removing
    `sgsapat` from `attested_modern` must not explain anything, because it is
    bible-only and that is exactly where the refusal read it. This is the leg
    that caught the log's own bug before it shipped.
  * **the split sweep's zero has to be told apart from a blind sweep** (batch
    232), so a pale-side join must refuse while the same join all-dark must not,
    and emptying the sequence list must trip the positive control BY NAME. The
    injected pair is taken from the book's own all-dark joins, not invented, so
    the leg cannot pass because the word happened not to be listed.
  * **a control that can clear its own earlier failure proves nothing** (batch
    233): `bad = bad or 1`, never `0 if ok else 1`.

    python .scratch/b235/control235.py            # site served at :8765
"""
import contextlib
import copy
import importlib.util
import io as _io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom235", "tools/orthography/logs/dom235.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

# ---- capture the real world once -----------------------------------------
_D = M.measure()
_ENT = M.entries_json()
_MM = M.modern_map()
_VER = M.verified()
_SRC = M.sources()

BASE = dict(
    measure=lambda: copy.deepcopy(_D),
    entries_json=lambda: copy.deepcopy(_ENT),
    modern_map=lambda: dict(_MM),
    verified=lambda: dict(_VER),
    sources=lambda: copy.deepcopy(_SRC),
)
PINS = dict((k, getattr(M, k)) for k in
            ("FLOOR", "DENOM", "AUDIO_IDS", "SOLE_TYPES", "SOLE_PAIRS",
             "TWO_TYPE", "THREE_PLUS", "TWO_CLUSTERS", "RARE_MAX",
             "RARE_FLOOR", "NO_MAP_KEY", "HIS", "VAL", "HIS_N", "CARD",
             "CARD_VAL", "HIS2", "VAL2", "CARD2", "SUB2", "RIVALS",
             "LICK_FAMILY", "LICK_SLOTS", "SPLIT_BOXES", "JOIN_PALE",
             "JOIN_ANY_FLOOR"))
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
    try:
        fs = run(**patch)
        note = fs[0] if fs else "explained"
        ok = bool(fs) == must_refuse
        if ok and want:
            ok = any(want in f for f in fs)
    except Exception as e:                     # a patch that reached nothing
        fs, ok, note = [], False, "PATCH %s" % e
    if not ok:
        bad = bad or 1                         # never CLEAR an earlier failure
    print("%-4s %-54s %s" % ("ok" if ok else "BAD", name, note[:66]))
    return fs


# ---- patchers -------------------------------------------------------------
def D(**over):
    d = copy.deepcopy(_D)
    d.update(over)
    return lambda: d


def DSEQ(extra):
    def f():
        d = copy.deepcopy(_D)
        d["seq"] = d["seq"] + [extra]
        return d
    return f


def DBLOCK(add=(), drop=None):
    def f():
        d = copy.deepcopy(_D)
        b = [x for x in d["blocked"]
             if drop is None or sorted(x) != sorted(drop)]
        if drop is not None and len(b) == len(d["blocked"]):
            raise RuntimeError("no blocked row matched %s" % (drop,))
        d["blocked"] = b + [list(x) for x in add]
        return d
    return f


def MAP(**over):
    m = dict(_MM)
    for k, v in over.items():
        m.pop(k, None) if v is None else m.__setitem__(k, v)
    return lambda: m


def VER(**over):
    v = dict(_VER)
    for k, x in over.items():
        v.pop(k, None) if x is None else v.__setitem__(k, x)
    return lambda: v


def SRC(fn):
    def f():
        s = copy.deepcopy(_SRC)
        fn(s)
        return s
    return f


def ENT(fn):
    def f():
        e = copy.deepcopy(_ENT)
        fn(e)
        return e
    return f


def hit(n, what):
    """a patch that matched nothing is a BAD, not an explanation (batch 234)."""
    if not n:
        raise RuntimeError("patch matched no %s" % what)
    return n


def card(e, hw):
    return [x for x in e if (x.get("hw") or "").lower() == hw.lower()]


def edit_card(hw, **fields):
    def fn(e):
        for x in hit(card(e, hw), hw):
            x.update(fields)
    return ENT(fn)


def drop_card(hw):
    def fn(e):
        hit(card(e, hw), hw)
        e[:] = [x for x in e if (x.get("hw") or "").lower() != hw.lower()]
    return ENT(fn)


def add_card(text, where="t"):
    def fn(e):
        e.append({"hw": "ZZCONTROL", "tag": "(R)", "fr": "", "zh": "",
                  "examples": [{"t": text if where == "t" else "",
                                "fr": text if where == "fr" else ""}],
                  "subs": []})
    return ENT(fn)


def rare_blob():
    """his own rare sole-blocker tokens, ready to be made frequent. Excludes
    the two words §3 and §4 count, so those legs stay measurable."""
    C = M.counts(_ENT)
    inv = {}
    for k, v in _MM.items():
        inv.setdefault(v, []).append(k)
    sole = set(x[0] for x in _D["blocked"] if len(x) == 1)
    toks = [h for w in sole for h in inv.get(w, ())
            if 0 < C.get(h, 0) <= M.RARE_MAX and h not in (M.HIS, M.HIS2)]
    return " ".join(hit(toks, "rare blocker token") * 3)


def listed_join():
    """an adjacent span pair the book ALREADY joins into a listed word. Taken
    from the data so the injection cannot pass for being unlisted."""
    att = _SRC[0]
    for sp in _D["seq"]:
        for i in range(len(sp) - 1):
            a, b = sp[i][0], sp[i + 1][0]
            if " " in a or " " in b or not a or not b:
                continue
            j = re.sub(r"[^a-z']", "", a + b)
            if len(j) >= 4 and j in att:
                return a, b
    raise RuntimeError("no listed join in the book to inject")


BLOB = rare_blob()
JA, JB = listed_join()
print("injection stock: %d rare tokens | join %s+%s\n"
      % (len(BLOB.split()) // 3, JA, JB))

print("--- 1. the shape of the loss")
case("the metric falls below the floor", True, "FLOOR", measure=D(ok=5345))
case("the denominator moves", True, "denominator", measure=D(tot=5430))
case("a pair blocked by THREE types appears", True, "THREE or more",
     measure=DBLOCK(add=[["zza", "zzb", "zzc"]]))
case("a two-type cluster heals", True, "left the book",
     measure=DBLOCK(drop=["snuk", "thiy"]))
case("a NEW sole blocker appears", True, "sole-blocker types",
     measure=DBLOCK(add=[["zzznewsole"]]))

print("--- 2. rarity, and the field the leg actually measures")
case("his rare tokens become frequent (written to `t`)", True,
     "Rarity was pinned", entries_json=add_card(BLOB, "t"))
case("...the same blob written to `fr` must NOT move it", False,
     entries_json=add_card(BLOB, "fr"))
case("a sole blocker no map key reaches", True, "no map key reaches",
     measure=DBLOCK(add=[["zzunmapped"]]), SOLE_TYPES=68, SOLE_PAIRS=80)

print("--- 3. narung")
case("narung goes DARK", True, "is DARK now", verified=VER(narung=1))
case("his nalong is remapped", True, "maps to", modern_map=MAP(nalong="zzz"))
case("a second nalong in his TEXT", True, "occurs 2 times",
     entries_json=add_card("nalong", "t"))
case("...a second nalong in his FRENCH must NOT move it", False,
     entries_json=add_card("nalong", "fr"))
case("the MALONG card loses its ivory note", True, "ivory note",
     entries_json=edit_card("malong", fr="Décoration (?)."))
case("his MALONG head goes pale", True, "no longer dark",
     verified=VER(marung=None))
case("a 象牙 word arrives in the register", True, "glosses a word 象牙",
     sources=SRC(lambda s: s[2].__setitem__("zzivory", ["象牙圓片"])))
case("a word 2 edits from narung takes the sense", True, "within two edits",
     sources=SRC(lambda s: s[1].__setitem__("arung", ["穿山甲", "裝飾品"])))
case("...a FAR word with the same sense must NOT", False,
     sources=SRC(lambda s: s[1].__setitem__("qmpahan", ["裝飾品"])))

print("--- 4. kahui")
case("the KAXOI card is gone", True, "card is gone",
     entries_json=drop_card("KAXOI"))
case("the Mkaxoi sub-form is gone", True, "sub-form is gone",
     entries_json=edit_card("KAXOI", subs=[]))
case("kahui goes DARK", True, "no longer pale", verified=VER(kahui=1))
case("a 妓 word arrives in the register", True, "glosses a word 妓",
     sources=SRC(lambda s: s[3].__setitem__("zzwhore", ["妓女"])))
case("a word 1 edit from kahui is listed", True, "within one edit",
     sources=SRC(lambda s: s[0].add("kahuy")))
case("a 淫 rival loses its gloss", True, "lost its gloss",
     sources=SRC(lambda s: [d.pop("sgsapat", None) for d in s[1:]]))
case("...dropping it from attested_modern only must NOT", False,
     sources=SRC(lambda s: s[0].discard("sgsapat")))

print("--- 5. shkun")
case("the shik family leaves the register", True, "has lost",
     sources=SRC(lambda s: [s[0].discard("shik")]
                 + [d.pop("shik", None) for d in s[1:]]))
case("the register spells shkun", True, "suffixed slot",
     sources=SRC(lambda s: s[0].add("shkun")))
case("...an unrelated new listed word must NOT", False,
     sources=SRC(lambda s: s[0].add("zznewword")))

print("--- 6. the split sweep")
case("an adjacent PALE-side join is listed", True, "join into a listed word",
     measure=DSEQ([[JA, 0], [JB, 1]]))
case("...the same join all DARK must NOT", False,
     measure=DSEQ([[JA, 1], [JB, 1]]))
case("the positive control collapses", True, "positive control",
     measure=D(seq=[]), SPLIT_BOXES=0)

print("\n%s" % ("all controls behaved" if not bad
                else "BAD: a control did not behave"))
sys.exit(bad)
