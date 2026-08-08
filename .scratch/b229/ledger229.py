# -*- coding: utf-8 -*-
"""Negative control for batch 229's three new LEDGER rows. A supersession that
cannot fail is an excuse (batch 209), so each row is fed its real failure line
and then tampered versions, and every tamper must be REFUSED.

    python .scratch/b229/ledger229.py
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S  # noqa: E402

MAP = S.load_map()
META = set(hw for hw, _ in S.meta_rows())

CASES = [
    # (log, failure line, MAP override, expect explained?)
    # --- dom166: the count grew because batch 229 ruled sml'lu onto it
    ("dom166.py", "GAIN smalu: want 16 dark, got {'dark': 17}", None, True),
    ("dom166.py", "GAIN smalu: want 16 dark, got {'dark': 16}", None, True),
    ("dom166.py", "GAIN smalu: want 16 dark, got {'dark': 15}", None, False),
    ("dom166.py", "GAIN smalu: want 16 dark, got {'dark': 17, 'pale': 1}", None, False),
    ("dom166.py", "GAIN smalu: want 16 dark, got {}", None, False),
    # --- dom58: the freeze revert, and the identity ruled beside it
    ("dom58.py", "BROWN n'gui nguy missing on [SLAP]  green there: []", None, True),
    ("dom58.py", "BROWN n'gui nguy missing on [SLAP]  green there: []",
     {"n'gui": "nguy"}, False),        # the freeze put back
    ("dom58.py", "BROWN n'gui nguy missing on [SLAP]  green there: []",
     {"n'gui": "ngeuyan"}, False),     # drifted onto the slot that must not move
    ("dom58.py", "BROWN nagui nagui missing on [SLAP]  green there: []", None, True),
    ("dom58.py", "BROWN nagui nagui missing on [SLAP]  green there: []",
     {"nagui": "nagui"}, False),       # the identity claim back
    # a line no row covers must stay uncovered
    ("dom58.py", "BROWN nagwi ngeuyan missing on [SLAP]  green there: []", None, False),
]

bad = 0
for log, line, over, want in CASES:
    m = dict(MAP)
    if over:
        m.update(over)
    rec, why = S.adjudicate(log, line, m, META)
    got = bool(rec) and not why
    mark = "ok " if got == want else "BAD"
    if got != want:
        bad += 1
    print("%s %-56s -> %s   %s" % (mark, line[:56],
                                   "explained" if got else "REFUSED", why[:52]))

print("\n%d cases, %d wrong" % (len(CASES), bad))
sys.exit(1 if bad else 0)
