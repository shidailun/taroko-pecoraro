# -*- coding: utf-8 -*-
"""Negative control for dom241 — a ledger that cannot fail is a list of excuses.

Every leg tampers with ONE input and requires the corresponding assertion to
REFUSE. The rules this project learned the hard way, each applied here:

  * batch 233 — accumulate `bad`, never reassign it. `bad = 0 if ok else 1`
    can CLEAR an earlier real failure and print "all controls behaved" over it.
  * batch 234/235 — a leg that patches the wrong field passes for FREE and
    reads as *explained*. So `patch()` RAISES when it matched no card, and every
    field-sensitive leg is PAIRED with the same string written to a field the
    assertion does not read, which must NOT refuse.
  * batch 233 — a gloss leg must patch EVERY source. `D.register()` merges
    `attested_gloss.json` and `bible_gloss.json`, so tampering the merged dict
    covers both by construction.
  * batch 222 — inject a value that is in the tested state NOW, taken from the
    measured data rather than invented.
  * batch 229 — the audio-id leg is a SWAP, not a drop: re-minting holds the
    count, so a count assertion cannot see it and only the BY-NAME pin can.
  * batch 232 — an empty sweep and a broken sweep have the same output, so the
    browser leg is controlled in BOTH directions: a needle that is really there
    must be found, and one that is not must come back None.

The legs drive `D.checks()`, which is the same function `main()` runs — a
control that re-implements the assertion proves nothing about the assertion.

    python .scratch/b241/control241.py        # site served at :8765
"""
import collections
import copy
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography", "logs"))
import dom241 as D                                              # noqa: E402

bad = 0
BASE = {}


def leg(name, refused, want=True):
    """want=True: this tampering MUST be refused. want=False: the paired leg,
    which proves the assertion reads the input it claims to read."""
    global bad
    ok = bool(refused) == want
    bad = bad or (0 if ok else 1)
    print("  %-4s %-66s %s" % ("ok" if ok else "BAD", name,
                               "refused" if refused else "passed"))


def run(**kw):
    """Run every data-side assertion over a tampered copy of the inputs and
    return the failure list."""
    a = dict(BASE)
    a.update(kw)
    fs, _ = D.checks(a["E"], a["MM"], a["VER"], a["G"], a["A"], a["raw"])
    return fs


def hit(fs, needle):
    """Did the assertion we are aiming at refuse — not merely SOME assertion?
    A leg that fires the wrong check is the field-patching fault one level up."""
    return [f for f in fs if needle in f]


def patch(E, hw, field, value, sub=None, ex=None):
    """Write `value` into one card. RAISES when it matched nothing — batch 235:
    a patcher that silently matches no card makes its leg free."""
    E = copy.deepcopy(E)
    n = 0
    for e in E:
        if (e.get("hw") or "").strip() != hw:
            continue
        if ex is not None:
            for x in e.get("examples") or []:
                if ex in (x.get("t") or "") or ex in (x.get("fr") or ""):
                    x[field] = value
                    n += 1
        elif sub is not None:
            for sb in e.get("subs") or []:
                if (sb.get("form") or "").strip() == sub:
                    sb[field] = value
                    n += 1
        else:
            e[field] = value
            n += 1
    if not n:
        raise AssertionError("patch matched nothing: %s %s %s %s"
                             % (hw, sub, ex, field))
    return E


def patch_ex(E, needle, field, value):
    """Patch the one example row whose Truku `t` carries `needle`."""
    E = copy.deepcopy(E)
    n = 0
    for e in E:
        boxes = list(e.get("examples") or [])
        for sb in e.get("subs") or []:
            boxes += list(sb.get("examples") or [])
        for x in boxes:
            if needle in (x.get("t") or ""):
                x[field] = value
                n += 1
    if not n:
        raise AssertionError("patch_ex matched no example: %r" % needle)
    return E


def gloss(G, **kw):
    G2 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    for k, v in kw.items():
        G2[k] = list(v) if isinstance(v, (list, tuple)) else [v]
    return G2


def main():
    global bad
    E = D.entries_json()
    BASE.update(E=E, MM=D.modern_map(), VER=D.verified(), G=D.register(),
                A=D.attested(), raw=D.entries_raw())
    print("dom241 negative control")

    # ---- the untampered baseline: nothing may be failing already ----------
    leg("the untampered inputs pass (the baseline the legs move from)",
        run(), want=False)

    # ---- 1. the transcription ----------------------------------------------
    #  reverting the correction must fire BOTH the sentence check and the hapax
    E_back = patch_ex(E, "ini na txey ka smuk", "t",
                      "Mxnuk bi ka qouni, ini na txey ka snuk")
    leg("reverting the slip fires the corrected-sentence assertion",
        hit(run(E=E_back), "corrected sentence"))
    leg("...and the hapax count with it (batch 213)",
        hit(run(E=E_back), "occurs 1 times in his Truku"))
    #  PAIRED: the same string written to the FRENCH field. `count()` walks his
    #  Truku fields only, so this must NOT move it — the batch-234 fault made
    #  mechanical.
    E_fr = patch_ex(E, "ini na txey ka smuk", "fr", "les clous snuk pas")
    leg("...and NOT when `snuk` is written to his French (paired wrong field)",
        hit(run(E=E_fr), "occurs 1 times in his Truku"), want=False)

    #  his SMUK card is what closes the scan question (batch 235)
    leg("his SMUK card losing its tag refuses",
        hit(run(E=patch(E, "SMUK", "tag", "(R.?)")), "SMUK tag"))
    leg("his SMUK card losing a sub-form refuses",
        hit(run(E=patch(E, "SMUK", "subs", [])), "sub-forms"))
    leg("...and his ENGLISH gloss is not read for it (paired wrong field)",
        hit(run(E=patch(E, "SMUK", "en", "zzz")), "SMUK"), want=False)

    #  batch 229: an id is a URL, and the count cannot see a re-mint
    swapped = BASE["raw"].replace(D.STALE_ID, "ex_zzz_reminted")
    leg("SWAPPING the stale audio id refuses (a drop would move the count too)",
        hit(run(raw=swapped), "audio id"))
    leg("...and the id COUNT cannot see the swap — which is why the pin is "
        "by NAME", hit(run(raw=swapped), "attached ids"), want=False)

    #  dom230's refusal of `snuk`, both halves
    leg("samu losing 釘子 refuses (dom230's positive half)",
        hit(run(G=gloss(BASE["G"], samu=["搬運"])), "dom230 refused"))
    leg("a listed word spelling `snuk` refuses (dom230's negative half)",
        hit(run(A=BASE["A"] | {"snuku"}), "listed word now spells"))

    # ---- 2. the two refusals cited -----------------------------------------
    #  these read files on disk, so they are exercised by the baseline; what is
    #  controlled is the 牢 fact dom230 owns and this batch only re-aims
    leg("a SECOND carrier of 牢 refuses — dom230's fact is a measurement",
        hit(run(G=gloss(BASE["G"], zzhkan=["牢固"])), "carriers of 牢"))
    leg("...and a carrier of a character the pin does not name does not "
        "(paired)", hit(run(G=gloss(BASE["G"], zzhkan=["關住"])),
                        "carriers of 牢"), want=False)

    # ---- 3. what rules it ---------------------------------------------------
    leg("reverting the map to his own letters refuses",
        hit(run(MM=dict(BASE["MM"], txey="txey")), "MAP txey"))
    leg("a SECOND token rendering `thiy` refuses — the cost argument rests on "
        "there being one", hit(run(MM=dict(BASE["MM"], zztxey="thiy")),
                               "keys sending to thiy"))
    leg("`thiy` leaving verified.js refuses",
        hit(run(VER={k: v for k, v in BASE["VER"].items() if k != "thiy"}),
            "left verified.js"))
    leg("a sibling of his TOXOI card going pale refuses (batch 199)",
        hit(run(VER={k: v for k, v in BASE["VER"].items() if k != "thiyan"}),
            "thiyan left verified.js"))
    leg("a sibling of his TOXOI card MOVING refuses",
        hit(run(MM=dict(BASE["MM"], txeyan="zzz")), "TOXOI family moved"))
    leg("the orphaned `snuk` entry acquiring a value refuses",
        hit(run(MM=dict(BASE["MM"], snuk="samu")), "orphaned map entry"))

    #  batch 224: the stem-whole test
    leg("a listed form that spells the stem whole going missing refuses",
        hit(run(A=BASE["A"] - {"kmthiyun"}), "spelling the stem whole"))
    leg("`thiy` BECOMING listed refuses — the HAND_RULED entry would be "
        "redundant", hit(run(A=BASE["A"] | {"thiy"}), "in attested_modern"))

    #  batch 221/233: the gloss legs, over the merged register
    leg("thiyan losing 和…在一起 refuses (batch 221)",
        hit(run(G=gloss(BASE["G"], thiyan=["遠的"])), "register row thiyan"))
    leg("kmthiyun losing 和…一起 refuses — the SECOND row (batch 200)",
        hit(run(G=gloss(BASE["G"], kmthiyun=["遠的"])),
            "register row kmthiyun"))
    leg("...and a neighbouring key does not (paired wrong key)",
        hit(run(G=gloss(BASE["G"], kmthiyunn=["遠的"])),
            "register row kmthiyun,"), want=False)

    #  batch 229: the negative half is a property of the CARRIERS
    leg("a carrier off a DIFFERENT root spelling his stem re-opens the ruling",
        hit(run(G=gloss(BASE["G"], zzthiy=["陪伴"])), "carriers spelling his "
                                                     "stem"))
    leg("...and one off a different root that does NOT spell his stem does "
        "not (paired)", hit(run(G=gloss(BASE["G"], zzqnay=["陪伴"])),
                            "carriers spelling his stem"), want=False)

    #  the incidental finding
    leg("the register's `smuk` losing 金鋼樹 refuses",
        hit(run(G=gloss(BASE["G"], smuk=["釘子"])), "register row smuk"))

    # ---- 4. the browser leg, controlled in BOTH directions (batch 232) ------
    #  A sweep that finds nothing and one that cannot see look identical. The
    #  sentence finder is asserted positively by the log itself; here it is
    #  asserted NEGATIVELY — a needle no box carries must come back None, or
    #  `sent is not None` was never informative.
    old = D.SENT
    try:
        D.SENT = "zzzz no box carries this zzzz"
        blind = D.measure()
    finally:
        D.SENT = old
    leg("a needle no box carries comes back None — so `sent is not None` is "
        "a measurement", blind["sent"] is None)
    leg("...and the same run still counts the book, so it is not simply "
        "broken", blind["tot"] != D.DENOM, want=False)

    print("all controls behaved" if not bad else "CONTROL FAILURE")
    return bad


if __name__ == "__main__":
    sys.exit(main())
