# -*- coding: utf-8 -*-
"""Negative controls for logs/dom236.py.

A frozen measurement that cannot fail is a list of excuses, so every assertion
in dom236 is fed a state in which it MUST refuse. Three house rules apply
(batches 233-235) and each is enforced mechanically here, not by reading:

* **Accumulate.** `bad = bad or ...`, never `bad = 0 if ok else 1` -- a leg that
  can clear an earlier leg's failure proves nothing (batch 233).
* **A patch that reaches nothing must RAISE.** `patch_card()` and `patch_val()`
  both throw when they matched no card / no key, so a leg cannot pass because
  the injection went nowhere (batch 235).
* **Pair every field-sensitive leg with the WRONG field**, which must NOT
  refuse. That is what proves the right one reached the measurement -- batch
  234 found three legs that had patched the wrong field and passed for free.

The DOM is measured ONCE and doctored in memory; a browser per case would take
half an hour and measure the same page.

    python .scratch/b236/control236.py          (site served at :8765)
"""
import copy
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography", "logs"))

import dom236 as M                                        # noqa: E402

BASE = {}          # filled by main(): the real DOM read, and the real files


class NoHit(Exception):
    """A patch that matched nothing. Raised, never returned -- an injection
    that goes nowhere makes its leg pass for free."""


def patch_card(E, hw, field, fn):
    """Rewrite one field of one card. Raises if no card carries that hw."""
    E = copy.deepcopy(E)
    n = 0
    for e in E:
        if (e.get("hw") or "") == hw:
            e[field] = fn(e.get(field))
            n += 1
    if not n:
        raise NoHit("no card %r to patch %r on" % (hw, field))
    return E


def patch_val(D, k, v):
    """Set a key that must already exist. Raises otherwise."""
    D = dict(D)
    if k not in D:
        raise NoHit("%r is not in the table" % k)
    if v is None:
        del D[k]
    else:
        D[k] = v
    return D


def add_gloss(S, w, g, which=1):
    """which: 1 attested_gloss, 2 bible_gloss, 3 parquet_gloss."""
    S = (set(S[0]), dict(S[1]), dict(S[2]), dict(S[3]))
    S[which][w] = [g] if which == 1 else g
    return S


def run(**over):
    """Run dom236's assertions over a doctored world. Returns the fail list."""
    keep = {}
    for k in ("measure", "modern_map", "verified", "sources", "entries_json",
              "pq_freq"):
        keep[k] = getattr(M, k)
    try:
        for k, v in over.items():
            setattr(M, k, (lambda val: (lambda *a, **kw: val))(v))
        M.fails = []
        buf, sys.stdout = sys.stdout, io.StringIO()
        try:
            M.main()
        finally:
            sys.stdout = buf
        return list(M.fails)
    finally:
        for k, v in keep.items():
            setattr(M, k, v)


CASES = []


def case(name, expect_fail, **over):
    CASES.append((name, expect_fail, over))


def main():
    print("measuring the page once ...")
    BASE["d"] = M.measure()
    BASE["mm"] = M.modern_map()
    BASE["ver"] = M.verified()
    BASE["S"] = M.sources()
    BASE["E"] = M.entries_json()
    BASE["pq"] = M.pq_freq()
    d, mm, ver, S, E, pq = (BASE["d"], BASE["mm"], BASE["ver"], BASE["S"],
                            BASE["E"], BASE["pq"])

    base_fails = run(measure=d, modern_map=mm, verified=ver, sources=S,
                     entries_json=E, pq_freq=pq)
    bad = 0
    if base_fails:
        bad = 1
        print("BAD  the undoctored state already fails: %s" % base_fails[:2])
    else:
        print("ok   undoctored: 0 failures")

    # ---- §1 towmuk: the gloss-arrival test, in EACH of the three files -----
    for which, nm in ((1, "attested_gloss"), (2, "bible_gloss"),
                      (3, "parquet_gloss")):
        case("towmuk glossed in %s" % nm, True,
             sources=add_gloss(S, "towmuk", "首領；負責人", which))
    # ... and the wrong WORD: the same gloss on a neighbour must explain nothing
    case("the same gloss on a different word", False,
         sources=add_gloss(S, "towmuk_not_a_word", "首領；負責人", 1))

    # ---- §1 the rivals: the different-root refusal must stay re-readable ---
    def blank(w, txt="人名（男）"):
        """Strip a word's gloss from ALL THREE files. Batch 233: a gloss leg
        that patches one of them passes for the wrong reason -- and this
        control found that out the hard way, having first blanked `thowlang`
        in bible_gloss alone while attested_gloss kept 王、領袖或頭目."""
        out = [set(S[0]), dict(S[1]), dict(S[2]), dict(S[3])]
        n = 0
        for i in (1, 2, 3):
            if w in out[i]:
                out[i][w] = [txt] if i == 1 else txt
                n += 1
        if not n:
            raise NoHit("%r is glossed in no file to blank" % w)
        return tuple(out)

    case("bukung loses 首長 in all three files", True, sources=blank("bukung"))
    case("thowlang loses 領 in all three files", True,
         sources=blank("thowlang"))
    # ...and the single-file version must NOT refuse. `thowlang` is glossed in
    # attested AND bible, so blanking one leaves the register saying 領 -- the
    # zero-from-one-file rule (batch 230) made visible as a control.
    case("thowlang blanked in bible_gloss ONLY", False,
         sources=(S[0], S[1], patch_val(S[2], "thowlang", "人名（男）"), S[3]))
    # wrong FILE: bukung is attested-gloss-only, so blanking a bible row it
    # does not have must not refuse
    case("bukung blanked in the file it is not in", False,
         sources=(S[0], S[1], dict(S[2], bukung="人名"), S[3]))

    # ---- §1 the map / verified / attestation legs -------------------------
    case("teumuk sent elsewhere", True,
         modern_map=patch_val(mm, "teumuk", "thowlang"))
    case("towmuk not verified", True, verified=patch_val(ver, "towmuk", None))
    case("towmuk verified at 16 not 1", True,
         verified=patch_val(ver, "towmuk", 16))
    case("towmuk out of attested_modern", True,
         sources=(S[0] - {"towmuk"}, S[1], S[2], S[3]))
    case("the single corpus row gone", True,
         pq_freq=patch_val(pq, "towmuk", 0))
    # wrong KEY: dropping a neighbour's count must explain nothing
    case("a different word's count dropped", False,
         pq_freq=patch_val(pq, "thlangan", 0))

    # ---- §1 the tag: his loan mark, and the WRONG CARD / WRONG FIELD pair --
    case("his TEUMUK tag gains `emprunt`", True,
         entries_json=patch_card(E, "TEUMUK", "tag",
                                 lambda t: t + " [emprunt jap.]"))
    case("`emprunt` written to a DIFFERENT card's tag", False,
         entries_json=patch_card(E, "TXOULANG", "tag",
                                 lambda t: t + " [emprunt jap.]"))
    case("`emprunt` written to TEUMUK's fr, not its tag", False,
         entries_json=patch_card(E, "TEUMUK", "fr",
                                 lambda t: t + " [emprunt jap.]"))

    # ---- §2 his prose, and the wrong-field twin ---------------------------
    case("his note loses `japonais`", True,
         entries_json=patch_card(E, "TXOULANG", "fr",
                                 lambda t: t.replace("japonais", "chinois")))
    case("the same edit made to `zh` instead of `fr`", False,
         entries_json=patch_card(E, "TXOULANG", "zh",
                                 lambda t: t.replace("日本", "中國")))
    case("his TEUXU loan tag gone", True,
         entries_json=patch_card(E, "TEUXU", "tag", lambda t: "(R)"))

    # ---- §2 the orthographic half, stated against itself ------------------
    # A rival on the REGULAR correspondence would have to be weighed. Each of
    # the four shapes is injected into a different table, because a rival
    # arriving in any one of them is news.
    case("tumuk turns up attested", True,
         sources=(S[0] | {"tumuk"}, S[1], S[2], S[3]))
    case("tomuk turns up glossed 首領", True,
         sources=add_gloss(S, "tomuk", "首領", 2))
    case("tmuk turns up in the parquets", True,
         pq_freq=dict(pq, tmuk=9))
    # ...and a shape that is NOT a rival must explain nothing
    case("an unrelated shape turns up attested", False,
         sources=(S[0] | {"zzzmuk"}, S[1], S[2], S[3]))
    # the correspondence counts are measurements, so move them
    case("the regular eu -> u correspondence collapses", True,
         modern_map=dict((k, ("qowlit" if k.startswith("qeulit") else v))
                         for k, v in mm.items()
                         if not (k.startswith("xeul") or k.startswith("mxeul")
                                 or k.startswith("psxeul"))))
    case("qeulit stops answering ow", True,
         modern_map=patch_val(mm, "qeulit", "qulit"))
    # wrong KEY: moving a French eu-word must not disturb the count, which is
    # what proves EU_NOT is doing its job rather than the floor being slack
    case("a FRENCH eu-word moves", False,
         modern_map=patch_val(mm, "grandeur", "grandeur"))
    case("thowlang's 552 tokens collapse", True,
         pq_freq=patch_val(pq, "thowlang", 40))

    # ---- §3 the card, slot by slot ----------------------------------------
    case("the head reverts to thulang", True,
         modern_map=patch_val(mm, "txoulang", "thulang"))
    case("the oblique reverts", True,
         modern_map=patch_val(mm, "txlangan", "thulangan"))
    case("thulang acquires a gloss", True,
         sources=add_gloss(S, "thulang", "首領", 2))
    case("thlangan's gloss stops naming its head", True,
         sources=(S[0], S[1], patch_val(S[2], "thlangan", "主"), S[3]))
    case("empathulang turns up attested", True,
         sources=(S[0] | {"empathulang"}, S[1], S[2], S[3]))
    # the HELD slots: batch 197's pride reading dragged off its stem
    case("stxoulang dragged onto the head's stem", True,
         modern_map=patch_val(mm, "stxoulang", "sthowlang"))
    case("msthulang leaves HAND_RULED (goes pale)", True,
         verified=patch_val(ver, "msthulang", None))

    # ---- §0 the shape of the loss -----------------------------------------
    d3 = copy.deepcopy(d)
    d3["blocked"].append(["aaa", "bbb", "ccc"])
    d3["ok"] -= 1
    case("a THREE-type blocked row appears", True, measure=d3)
    d2 = copy.deepcopy(d)
    d2["blocked"].append(["aaa", "bbb"])
    d2["ok"] -= 1
    case("a FIFTH two-type cluster appears", True, measure=d2)
    dm = copy.deepcopy(d)
    dm["ok"] -= 1
    case("the metric falls by one", True, measure=dm)

    # ---- §4 colour: taken from the measured data, not invented ------------
    dp = copy.deepcopy(d)
    dp["wide"]["towmuk"] = [1, 1]
    case("towmuk renders a PALE span", True, measure=dp)
    dt = copy.deepcopy(d)
    dt["truku"]["thlangan"] = [2, 1]
    case("a TXOULANG value goes pale inside .truku", True, measure=dt)
    dn = copy.deepcopy(d)
    del dn["truku"]["towmuk"]
    case("towmuk renders in no .truku box", True, measure=dn)
    df = copy.deepcopy(d)
    df["wide"]["thulang"] = [3, 0]
    case("the frozen value renders again", True, measure=df)
    # a DARK injection where the assertion wants "absent" -- batch 233: the
    # probe must not pass just because the span is brown
    db = copy.deepcopy(d)
    db["wide"]["empathulang"] = [1, 0]
    case("the dropped value renders DARK", True, measure=db)

    # ---- run them ---------------------------------------------------------
    for name, want, over in CASES:
        full = dict(measure=d, modern_map=mm, verified=ver, sources=S,
                    entries_json=E, pq_freq=pq)
        full.update(over)
        try:
            fs = run(**full)
        except NoHit as e:
            bad = bad or 1
            print("BAD  %-46s injection hit nothing: %s" % (name, e))
            continue
        got = bool(fs)
        ok = (got == want)
        bad = bad or (0 if ok else 1)
        print("%-4s %-46s %s%s"
              % ("ok" if ok else "BAD", name,
                 "refused" if got else "no refusal",
                 "" if ok else "   <-- expected %s"
                 % ("a refusal" if want else "no refusal")))

    # a patcher that cannot raise is not a guard: prove it raises
    try:
        patch_card(E, "NO_SUCH_CARD", "tag", lambda t: t)
        bad = 1
        print("BAD  patch_card accepted a card that does not exist")
    except NoHit:
        print("ok   patch_card raises on a card that does not exist")
    try:
        patch_val(mm, "no_such_key", "x")
        bad = 1
        print("BAD  patch_val accepted a key that does not exist")
    except NoHit:
        print("ok   patch_val raises on a key that does not exist")

    print("\n%d case(s) + 2 guards | %s"
          % (len(CASES), "all controls behaved" if not bad
             else "SOMETHING DID NOT BEHAVE"))
    return bad


if __name__ == "__main__":
    sys.exit(main())
