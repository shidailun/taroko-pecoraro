# -*- coding: utf-8 -*-
"""Negative control for dom238 — a ledger that cannot fail is a list of excuses.

Every leg tampers with one input and requires the corresponding assertion to
REFUSE. Three project rules shape it:

  * batch 233 — accumulate `bad`, never reassign it. A leg written
    `bad = 0 if ok else 1` can CLEAR an earlier real failure and print
    "all controls behaved" over it.
  * batch 234/235 — a leg that patches the wrong field passes for FREE and
    reads as *explained* rather than as an error. So `patch()` RAISES when it
    matched nothing, and every field-sensitive leg is PAIRED with the same
    string written to the wrong field, which must NOT refuse.
  * batch 222 — inject a value that is in the tested state NOW, taken from the
    measured data rather than invented.

    python .scratch/b238/control238.py
"""
import collections
import copy
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools", "orthography",
    "logs"))
import dom238 as D                                            # noqa: E402

bad = 0


def leg(name, refused, want=True):
    """want=True: this tampering MUST be refused. want=False: it must NOT be
    (the paired wrong-field leg, which proves the assertion reads its field)."""
    global bad
    ok = bool(refused) == want
    bad = bad or (0 if ok else 1)
    print("  %-4s %-58s %s" % ("ok" if ok else "BAD", name,
                               "refused" if refused else "passed"))


def patch(E, hw, field, value, sub=None):
    """Write `value` into one card's field. RAISES if it matched no card --
    batch 235: a patcher that silently matches nothing makes its leg free."""
    E = copy.deepcopy(E)
    hit = 0
    for e in E:
        if (e.get("hw") or "").strip() != hw:
            continue
        if sub is None:
            e[field] = value
            hit += 1
        else:
            for sb in e.get("subs") or []:
                if (sb.get("form") or "").strip() == sub:
                    sb[field] = value
                    hit += 1
    if not hit:
        raise AssertionError("patch matched no card: %s %s %s" % (hw, sub, field))
    return E


def main():
    global bad
    E, MM, VER, G = (D.entries_json(), D.modern_map(),
                     D.verified(), D.register())

    print("dom238 negative control")

    # --- the UNIT-vs-CARD measurement, and its paired wrong-field leg ------
    SUB, CARD = D.PAREN_SUB, D.PAREN_CARD

    def unit_share(EE):
        for e in EE:
            if (e.get("hw") or "").strip() == CARD:
                for sb in e.get("subs") or []:
                    if (sb.get("form") or "").strip() == SUB:
                        return len(set("咀嚼") & set(str(sb.get("zh") or "")))
        return None

    def card_share(EE):
        for e in EE:
            if (e.get("hw") or "").strip() == CARD:
                return len(set("咀嚼") & set(str(e.get("zh") or "")))
        return None

    leg("UNIT share reads the sub-form gloss",
        unit_share(patch(E, CARD, "zh", "無關的詞義", sub=SUB)) != D.UNIT_SHARE)
    leg("...and NOT the card gloss (paired wrong field)",
        unit_share(patch(E, CARD, "zh", "咀嚼")) != D.UNIT_SHARE, want=False)
    leg("CARD share reads the headword gloss",
        card_share(patch(E, CARD, "zh", "咀嚼")) != D.CARD_SHARE)
    leg("...and NOT the sub-form gloss (paired wrong field)",
        card_share(patch(E, CARD, "zh", "咀嚼", sub=SUB)) != D.CARD_SHARE,
        want=False)

    # --- his TAPAK example glosses, and the wrong-field pair ---------------
    def his_examples(EE):
        ex = []
        for e in EE:
            if (e.get("hw") or "").strip() == "TAPAK":
                for sb in e.get("subs") or []:
                    ex += [str(x.get("zh") or "")
                           for x in sb.get("examples") or []]
        return all(any(h in z for z in ex) for h in D.HIS_EXAMPLES)

    blanked = copy.deepcopy(E)
    hit = 0
    for e in blanked:
        if (e.get("hw") or "").strip() == "TAPAK":
            for sb in e.get("subs") or []:
                for x in sb.get("examples") or []:
                    x["zh"] = "無關"
                    hit += 1
    if not hit:
        raise AssertionError("no TAPAK example to blank")
    leg("his TAPAK example glosses are read", not his_examples(blanked))
    leg("...and not his French (paired wrong field)",
        not his_examples(patch(E, "TAPAK", "fr", "拍手 游泳")), want=False)

    # --- the register legs: all sources, batch 233 -------------------------
    G2 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G2["tpaqi"] = ["無關"]
    carr = [w for w, gl in G2.items() if D.UNIQUE_CHAR in " ".join(gl)]
    leg("tpaqi's own gloss is what carries 拍手", carr != ["tpaqi"])

    G3 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G3["mtapaq"] = ["平的。拍手"]
    carr3 = [w for w, gl in G3.items() if D.UNIQUE_CHAR in " ".join(gl)]
    leg("a SECOND carrier of 拍手 breaks the uniqueness claim",
        sorted(carr3) != ["tpaqi"])

    G4 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G4["bsqani"] = ["咀嚼"]          # a bs[eq]- key acquiring his sense
    hits = [w for w in G4 if D.NO_BSQ.match(w)
            and any(s in " ".join(G4[w]) for s in D.NO_SENSE_B)]
    leg("the negative half re-opens when a bs[eq]- key gains 咀嚼", bool(hits))

    G5 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G5["bsekan"] = ["咀嚼"]
    leg("the ABSENT pin fires when bsekan enters the register",
        any(w in G5 for w in D.ABSENT))

    # --- the sweep: does it SEE, or is it merely empty? (batch 232) --------
    # No browser here, so the pale list is synthetic. `sweep()` takes it as an
    # ARGUMENT precisely so its logic can be controlled without the DOM; the
    # live log feeds it the real list from `measure()` (batch 219/230). These
    # legs are about whether the instrument can SEE, not about what is pale.
    back = dict(MM)
    back["bsqan"] = "bsekan"
    rec, _ = D.sweep(E, back, {"bsekan"}, G)
    leg("POSITIVE: backing the ruling out recovers bsekan -> pskan",
        any(r[0] == "bsekan" and r[1] == "pskan" for r in rec))

    blind = collections.defaultdict(list)
    rec2, _ = D.sweep(E, back, {"bsekan"}, blind)
    leg("...and with an EMPTY register it cannot",
        not any(r[0] == "bsekan" for r in rec2))

    # An empty sweep and a broken sweep have the same output (batch 232), so
    # assert the PAIR: the two runs above differ, which is what distinguishes
    # "found nothing" from "cannot see".
    leg("...so 'found nothing' and 'cannot see' are distinguishable",
        bool(rec) != bool(rec2))

    # The rarity gate is load-bearing -- but only measurably so over a set with
    # rivals to cut. Over the one-value set above, gated and ungated return the
    # same row, so that leg would have passed for free (batch 234). Use a loose
    # OFFLINE proxy for pallor here: every map value absent from verified.js.
    # It is not the DOM's pale list and is not claimed to be -- the question is
    # whether the gate cuts, not what is pale today.
    PROXY = {v for v in MM.values() if v not in VER}
    leg("the proxy pale set is big enough to have rivals to cut",
        len(PROXY) > 100)
    gated, _ = D.sweep(E, MM, PROXY, G)
    keep = D.RARE
    D.RARE = 10 ** 9
    flood, _ = D.sweep(E, MM, PROXY, G)
    D.RARE = keep
    leg("the rarity gate is load-bearing (ungated the sweep floods)",
        len(flood) > 3 * max(1, len(gated)))
    print("       gate: %d rows gated, %d ungated" % (len(gated), len(flood)))

    # the unjoinable half must be REPORTED, never silently dropped (batch 230)
    _, unj = D.sweep(E, MM, {"a-value-no-unit-of-his-reaches"}, G)
    leg("a pale value no unit reaches is REPORTED, not dropped",
        unj == ["a-value-no-unit-of-his-reaches"])

    # --- the furniture claim: a value ALREADY inTruku==0 is a free pass ----
    # batch 234: injecting something that is already in the tested state
    # changes no count. Assert the pairing explicitly rather than trusting it.
    leg("a value already at inTruku==0 would pass the delta leg for free",
        D.DELTA["tapaq"][2] == 0, want=True)

    # --- the map legs ------------------------------------------------------
    leg("the ruling is refused if the map drifts to a third spelling",
        dict(MM, tapak="tapaqq").get("tapak") != D.RULINGS["tapak"])
    leg("the ruling is refused if its target leaves verified.js",
        D.RULINGS["tapak"] not in {k: v for k, v in VER.items()
                                   if k != "tapaq"})

    print("all controls behaved" if not bad else "CONTROL FAILURE")
    return bad


if __name__ == "__main__":
    sys.exit(main())
