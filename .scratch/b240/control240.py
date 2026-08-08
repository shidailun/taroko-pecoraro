# -*- coding: utf-8 -*-
"""Negative control for dom240 — a test that cannot fail is a list of excuses.

Every leg tampers with one input and requires the corresponding assertion to
REFUSE. The project's rules about controls, each learned the hard way:

  * batch 233 — accumulate `bad`, never reassign it. A leg written
    `bad = 0 if ok else 1` can CLEAR an earlier real failure and print
    "all controls behaved" over it.
  * batch 234/235 — a leg that patches the wrong field passes for FREE and
    reads as *explained* rather than as an error. So `patch()` RAISES when it
    matched no card, and every field-sensitive leg is PAIRED with the same
    string written to a field the assertion does not read, which must NOT
    refuse.
  * batch 222 — inject a value that is in the tested state NOW, taken from the
    measured data rather than invented.
  * batch 232 — an empty sweep and a broken sweep have the same output, so the
    instrument is controlled from the DATA side in BOTH directions. dom240
    carries those two legs itself; what is controlled here is that they can
    still fail.

Tampering `G` covers both gloss files at once — `register()` merges
`attested_gloss.json` and `bible_gloss.json` before returning — which is the
batch-233 requirement that a gloss leg patch every source, met by construction.

    python .scratch/b240/control240.py
"""
import collections
import copy
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
LOGS = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools", "orthography",
    "logs")
sys.path.insert(0, LOGS)
import collide240 as C                                          # noqa: E402
import dom240 as D                                              # noqa: E402

bad = 0


def leg(name, refused, want=True):
    """want=True: this tampering MUST be refused. want=False: the paired leg,
    which proves the assertion reads the input it claims to read."""
    global bad
    ok = bool(refused) == want
    bad = bad or (0 if ok else 1)
    print("  %-4s %-64s %s" % ("ok" if ok else "BAD", name,
                               "refused" if refused else "passed"))


def patch(E, hw, field, value):
    """Write `value` into one card's field. RAISES if it matched no card --
    batch 235: a patcher that silently matches nothing makes its leg free."""
    E = copy.deepcopy(E)
    hit = 0
    for e in E:
        if (e.get("hw") or "").strip() == hw:
            e[field] = value
            hit += 1
    if not hit:
        raise AssertionError("patch matched no card: %s %s" % (hw, field))
    return E


def gloss(G, **kw):
    G2 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    for k, v in kw.items():
        G2[k] = list(v) if isinstance(v, (list, tuple)) else [v]
    return G2


def news_of(E, MM, G):
    _, _, _, rows = C.sweep(E, MM, G)
    _, left = C.classify(rows, E)
    return [h for _, h in left if h not in C.KNOWN_LEFTOVERS]


def classes_of(E, MM, G):
    _, _, _, rows = C.sweep(E, MM, G)
    cnt, left = C.classify(rows, E)
    return cnt, sorted(h for _, h in left), len(rows)


def main():
    global bad
    E, MM, G = C.entries(), C.modern_map(), C.register()
    print("dom240 negative control")

    # --- the load-bearing assertion: a NEW collision must be reported -------
    pre = {k: v for k, v in MM.items() if k != D.PIN[0]}
    leg("a new collision fires the NEW-unclassified assertion",
        news_of(E, pre, G) != [])
    leg("...and today's map does not (paired untampered)",
        news_of(E, MM, G) != [], want=False)

    # --- the classification, class by class ---------------------------------
    #  his tag is what makes a row a loan; the fr field is not read for it
    cnt, left, n = classes_of(patch(E, "TOTING", "tag", "[emprunt jap./chin.]"),
                              MM, G)
    leg("the loan class reads his TAG",
        cnt.get("tier-J loan, and correct (batch 204)")
        != D.CLASSES["tier-J loan, and correct (batch 204)"])
    cnt2, _, _ = classes_of(patch(E, "TOTING", "en", "[emprunt jap./chin.]"),
                            MM, G)
    leg("...and not his English (paired wrong field)",
        cnt2.get("tier-J loan, and correct (batch 204)")
        != D.CLASSES["tier-J loan, and correct (batch 204)"], want=False)

    #  his own cross-reference note is read off tag/fr/zh. The string has to be
    #  one XREF actually names -- the first draft injected the French "voir
    #  KNILAO", which the regex does not carry, and the leg passed for free
    #  (batch 234). Taken from the measured data instead: `syn. =` is his own
    #  notation, and is what classifies one of the fifteen real cross-ref rows.
    cnt3, left3, _ = classes_of(patch(E, "QNILAO", "fr", "syn. = KNILAO"),
                                MM, G)
    leg("a cross-reference note reclassifies a leftover",
        left3 != sorted(C.KNOWN_LEFTOVERS))
    leg("...and the LEFTOVER count moves with it",
        cnt3.get("LEFTOVER") != D.CLASSES["LEFTOVER"])

    #  batch 218's metalinguistic strip is load-bearing on the gloss side
    G_meta = gloss(G, tucing=["（掉下來）"])
    leg("stripping his parenthesised apparatus is what scores the gloss",
        any("掉下來" in g for g in G_meta["tucing"])
        and not C.strip_meta(" ".join(G_meta["tucing"])))

    # --- section 1: the two refusals, positive half and negative half -------
    leg("the tucing leg reads its own gloss row",
        not any(D.TUCING[1] in g for g in gloss(G, tucing=["搬運"])["tucing"]))
    leg("...and not a neighbouring word's (paired wrong key)",
        not any(D.TUCING[1] in g
                for g in gloss(G, tmucing=["搬運"]).get("tucing", [])),
        want=False)
    leg("the hammer leg refuses when tmucing loses its 鎚",
        not any(D.HAMMER[1] in g
                for g in gloss(G, tmucing=["敲打"])["tmucing"]))
    G2 = gloss(G, pucing=["鐵鎚"])
    leg("a SECOND carrier of 鎚/槌 re-opens the row — a rival root",
        D.carriers(G2, D.HAMMER_CHARS) != [D.HAMMER[0]])
    G3 = gloss(G, pucing=["敲打"])
    leg("...and a carrier of a character the pin does not name does not "
        "(paired)", D.carriers(G3, D.HAMMER_CHARS) != [D.HAMMER[0]],
        want=False)
    G4 = gloss(G, mhuma=["豬食"])
    leg("a 豬食 carrier off another root re-opens the qnilaw row",
        sorted(D.carriers(G4, [D.PIGFOOD_CHARS])) != sorted(D.PIGFOOD))
    leg("...and the stem-whole leg catches it by shape too",
        not all(x.lstrip("stgpm").startswith(D.QNILAW[0])
                for x in D.carriers(G4, [D.PIGFOOD_CHARS])))

    # --- section 2: controlling dom240's own two controls -------------------
    leg("the positive control fails if the pre-239 map stops colliding",
        news_of(E, dict(pre, qbolong="qbulung"), G) == [D.RECOVERS], want=False)
    leg("the blinded control fails if the sweep can score without a register",
        bool(C.sweep(E, MM, collections.defaultdict(list))[3]), want=False)
    #  ...and the blinded leg must be blind to the INJECTED freeze too, or it
    #  is passing because today's map is clean rather than because it is blind
    leg("the blinded sweep cannot see even the pre-239 freeze",
        bool(C.sweep(E, pre, collections.defaultdict(list))[3]), want=False)
    leg("the blinded sweep reports its collisions as unjudgeable, never as "
        "agreement (batch 200)",
        len(C.sweep(E, MM, collections.defaultdict(list))[2]) >= D.FLAGGED)

    # --- the pins themselves ------------------------------------------------
    #  a character the register does not carry AT ALL: the derivation cannot
    #  reproduce it, and must say so with depth 0 rather than handing back a
    #  plausible number. This leg is what caught the silent fallback.
    leg("the depth pin refuses a derivation that CANNOT reproduce its list",
        C.build_stoplist(G, C.NAMED + "麤")[1] != D.DEPTH)
    leg("...and the failure is signalled as 0, not as a plausible depth",
        C.build_stoplist(G, C.NAMED + "麤")[1] == 0)
    #  and one it does carry, but deeper than the cut
    leg("the depth pin moves when a deeper named character is required",
        C.build_stoplist(G, C.NAMED + "給")[1] != D.DEPTH)
    leg("...to the rank of that character (55), not to a fallback",
        C.build_stoplist(G, C.NAMED + "給")[1] == 55)
    #  the inertness claim: it must be falsifiable from the data side
    leg("the inertness pin is a measurement, not a restatement",
        len({len(C.sweep(E, MM, G, depth=x)[3]) for x in (10, 30, 37)}) != 1,
        want=False)
    leg("the universe pin reads the map",
        C.sweep(E, dict(MM, toting="zzzzz"), G)[0] != D.COLLIDING)

    print("all controls behaved" if not bad else "CONTROL FAILURE")
    return bad


if __name__ == "__main__":
    sys.exit(main())
