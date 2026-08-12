# -*- coding: utf-8 -*-
"""Negative control on the 68 batch-242 ledger rows.

A ledger that cannot fail is a list of excuses (batch 209). Every row must
(a) accept the real failure line against the live tables, and (b) REFUSE when
the thing it re-asserts is taken away. Kind decides what "taken away" means:
a row keyed on the map is tampered by moving the map value, a row keyed on an
absence is tampered by giving it a colour to see.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

NEW = eval("{" + io.open(os.path.join(ROOT, ".scratch", "b242", "block.py"),
                         encoding="utf-8").read() + "}")
MAP = S.load_map()
META = set(hw for hw, _ in S.meta_rows())

txt = io.open(os.path.join(ROOT, ".scratch", "b242", "keys.txt"),
              encoding="utf-8").read().splitlines()
cur, lines = None, []
for l in txt:
    if l.startswith("--- "):
        cur = l[4:].split()[0]
    elif l.startswith("LINE "):
        lines.append((cur, l[5:]))

bad = 0
kinds = {}
for f, line in lines:
    key = (f, S.sig(line)[0])
    if key not in NEW:
        continue
    kind, arg, _why = NEW[key]
    kinds[kind] = kinds.get(kind, 0) + 1

    # (a) the row accepts the real line against the live tables
    rec, err = S.adjudicate(f, line, MAP, META)
    if err:
        print("BAD  live line refused: %s %s\n     %s" % (f, key[1][:70], err))
        bad = 1

    # (b) and refuses when its subject is taken away
    tam_map, tam_line = dict(MAP), line
    if kind == "map":
        tok = re.match(r"BROWN (\S+) (\S+) missing on \[(.+?)\]",
                       key[1]).group(1)
        tam_map[tok] = "ZZZ"
    elif kind in ("ruled", "shape", "grew", "floor"):
        tok = arg[1] if kind in ("shape", "grew") else arg[0]
        if kind == "floor":
            tok = arg[1]
        tam_map[tok] = "ZZZ"
    elif kind == "absent":
        tam_line = line.replace("got {}", "got {'dark': 1}")
        if tam_line == line:
            print("BAD  absent-row tamper matched nothing: %s" % key[1][:70])
            bad = 1
    else:
        print("BAD  no tamper defined for kind %r" % kind)
        bad = 1
        continue
    rec, err = S.adjudicate(f, tam_line, tam_map, META)
    if not err:
        print("BAD  tampered %-6s NOT refused: %s %s" % (kind, f, key[1][:70]))
        bad = 1

# (c) a control that can clear its own earlier failure proves nothing
#     (batch 233) -- `bad` accumulates, never assigns.
# (d) and a leg that patches the wrong field passes for free (batch 234):
#     tampering a token no row names must NOT refuse anything.
free = dict(MAP)
free["zzz_not_a_token"] = "ZZZ"
clean = 0
for f, line in lines:
    key = (f, S.sig(line)[0])
    if key not in NEW:
        continue
    _rec, err = S.adjudicate(f, line, free, META)
    if err:
        print("BAD  irrelevant tamper refused %s %s" % (f, key[1][:60]))
        bad = 1
    clean += 1
print("rows exercised %d over kinds %s" % (clean, kinds))
print("CONTROLS %s" % ("BAD" if bad else "all behaved"))
sys.exit(bad)
