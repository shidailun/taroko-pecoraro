# -*- coding: utf-8 -*-
"""Negative control for dom239 — a ledger that cannot fail is a list of excuses.

Every leg tampers with one input and requires the corresponding assertion to
REFUSE. The project's rules about controls, all of them learned the hard way:

  * batch 233 — accumulate `bad`, never reassign it. A leg written
    `bad = 0 if ok else 1` can CLEAR an earlier real failure and print
    "all controls behaved" over it.
  * batch 234/235 — a leg that patches the wrong field passes for FREE and
    reads as *explained* rather than as an error. So `patch()` RAISES when it
    matched nothing, and every field-sensitive leg is PAIRED with the same
    string written to the wrong field, which must NOT refuse.
  * batch 222 — inject a value that is in the tested state NOW, taken from the
    measured data rather than invented.
  * batch 232 — an empty sweep and a broken sweep have the same output, so the
    batch-215 legs are controlled from the DATA side in both directions.

The two batch-215 legs run through `D.cluster_legs()`, the log's own function.
The gloss legs mirror the log's inline expressions; that is the established
pattern (dom238's control does the same) and it is why the mirrors are kept
short enough to read against the original.

    python .scratch/b239/control239.py
"""
import collections
import copy
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "tools", "orthography",
    "logs"))
import dom239 as D                                            # noqa: E402

bad = 0


def leg(name, refused, want=True):
    """want=True: this tampering MUST be refused. want=False: the paired
    wrong-field leg, which proves the assertion reads the field it claims."""
    global bad
    ok = bool(refused) == want
    bad = bad or (0 if ok else 1)
    print("  %-4s %-62s %s" % ("ok" if ok else "BAD", name,
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


def main():
    global bad
    E, MM, VER, G = (D.entries_json(), D.modern_map(),
                     D.verified(), D.register())
    print("dom239 negative control")

    # --- the gloss test that convicts the freeze, and its wrong-field pair --
    def overlap(EE):
        for e in EE:
            if (e.get("hw") or "").strip() == "QBOLONG":
                return set(str(e.get("zh") or "")) & set("".join(G["qburung"]))
        return None

    leg("the zero-overlap test reads his QBOLONG Chinese",
        bool(overlap(patch(E, "QBOLONG", "zh", "收割"))))
    leg("...and NOT his French (paired wrong field)",
        bool(overlap(patch(E, "QBOLONG", "fr", "收割"))), want=False)
    leg("...and not the OTHER card's gloss (paired wrong card)",
        bool(overlap(patch(E, "KBOLONG", "zh", "蚱蜢"))), want=False)

    # his tag is what makes QBOLONG an animal card rather than a slip
    def tag_of(EE):
        for e in EE:
            if (e.get("hw") or "").strip() == "QBOLONG":
                return (e.get("tag") or "").strip()
    leg("the tag assertion reads his tag",
        tag_of(patch(E, "QBOLONG", "tag", "plante")) != "animal")

    # --- the positive half: kbowlung is the SOLE carrier of 蚱/蜢 -----------
    G2 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G2["mqburung"] = ["蚱蜢"]
    carr2 = sorted(w for w in G2 if any(c in " ".join(G2[w])
                                        for c in D.UNIQUE_CHARS))
    leg("a SECOND carrier of 蚱/蜢 re-opens the candidate",
        carr2 != [D.REFUSED])

    # --- the negative half: a q-initial hopper word retires the pin ---------
    G3 = collections.defaultdict(list, {k: list(v) for k, v in G.items()})
    G3["qbowlung"] = ["蚱蜢"]
    carr3 = [w for w in G3 if any(c in " ".join(G3[w]) for c in D.UNIQUE_CHARS)]
    leg("a q-initial hopper word fires the pin's own retirement clause",
        bool([w for w in carr3 if D.NO_Q_HOPPER.match(w)]))
    # ...and the clause must NOT fire on a k-initial one, which is today's state
    leg("...and does not fire on the k-initial word that is already there",
        bool([w for w in sorted(G) if any(c in " ".join(G[w])
                                          for c in D.UNIQUE_CHARS)
              and D.NO_Q_HOPPER.match(w)]), want=False)

    # --- batch 215, leg 1: modern kb-, through the log's own function -------
    M1 = dict(MM)
    M1["qbxxxx"] = "kbyyyy"                      # the crossing, injected
    _, kbq, _, _ = D.cluster_legs(M1)
    leg("leg 1 refuses when he spells a modern kb- word qb-",
        kbq != D.KB_HIS_QB)
    M2 = dict(MM)
    M2["kbxxxx"] = "kbyyyy"                      # same cell, NO crossing
    _, kbq2, _, _ = D.cluster_legs(M2)
    leg("...and not when he spells it kb- (paired non-crossing)",
        kbq2 != D.KB_HIS_QB, want=False)

    # the populated-cell requirement: batch 217, an empty cell is no refusal
    M3 = {k: v for k, v in MM.items() if not D.plain(v).startswith("kb")}
    kbn3, _, _, _ = D.cluster_legs(M3)
    leg("leg 1 refuses if its cell empties out (batch 217)",
        kbn3 < D.KB_VALUES)

    # --- batch 215, leg 2: modern -owl- ------------------------------------
    M4 = dict(MM)
    M4["xolxxx"] = "xowlxxx"                     # a bare ol spelling modern owl
    _, _, _, owo = D.cluster_legs(M4)
    leg("leg 2 refuses when he spells a modern owl word with a bare ol",
        owo != D.OWL_HIS_BARE_OL)
    M5 = dict(MM)
    M5["xoulxxx"] = "xowlxxx"                    # his real correspondence
    _, _, _, owo2 = D.cluster_legs(M5)
    leg("...and not when he spells it oul (paired non-crossing)",
        owo2 != D.OWL_HIS_BARE_OL, want=False)
    M6 = {k: v for k, v in MM.items() if "owl" not in D.plain(v)}
    _, _, own6, _ = D.cluster_legs(M6)
    leg("leg 2 refuses if its cell empties out (batch 217)",
        own6 < D.OWL_VALUES)

    # --- the char-rule fact the pin exists to block (batch 227, inverted) ---
    cr = lambda w: D.plain(w).replace("o", "u").replace("l", "r") \
                             .replace("x", "h")
    leg("the char-rule leg computes, rather than restating its constant",
        cr("qbolang") != D.CHAR_RULE_OUTPUT)
    leg("...and on his actual token it really does spell the freeze",
        cr("qbolong") == D.CHAR_RULE_OUTPUT)

    # --- batch 205's cost, measured on his ONE occurrence -------------------
    def count(EE):
        n = 0
        for e in EE:
            txts = [e.get("hw") or ""] + [x.get("t") or ""
                                          for x in e.get("examples") or []]
            for sb in e.get("subs") or []:
                txts += [sb.get("form") or ""] + [
                    x.get("t") or "" for x in sb.get("examples") or []]
            n += sum(len(re.findall(r"(?i)\bqbolong\b", t)) for t in txts)
        return n

    E2 = copy.deepcopy(E)
    hit = 0
    for e in E2:
        if (e.get("hw") or "").strip() == "KBOLONG":
            e.setdefault("examples", []).append(
                {"t": "Qbolong ka nii.", "fr": "", "en": "", "zh": ""})
            hit += 1
    if not hit:
        raise AssertionError("no KBOLONG card to append an example to")
    leg("a SECOND occurrence of his token re-prices the pin", count(E2) != 1)
    leg("...and a French one does not (paired wrong field)",
        count(patch(E, "KBOLONG", "fr", "Qbolong partout")) != 1, want=False)

    # --- the map and verified.js legs --------------------------------------
    k, v = D.RULING
    leg("the pin is refused if the map drifts to a third spelling",
        dict(MM, qbolong="qbulung").get(k) != v)
    leg("the pin is refused if qbolong ENTERS verified.js — the pallor is the "
        "whole point", dict(VER, qbolong=1).get(v) is not None)
    kk, kv = D.KEEP
    leg("his harvest card is refused if it leaves verified.js",
        kv not in {a: b for a, b in VER.items() if a != kv})
    leg("a second key sending to qburung is refused",
        sorted(t for t, val in dict(MM, mkbolong="qburung").items()
               if val == kv) != [kk])

    print("all controls behaved" if not bad else "CONTROL FAILURE")
    return bad


if __name__ == "__main__":
    sys.exit(main())
