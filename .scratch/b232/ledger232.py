# -*- coding: utf-8 -*-
"""Control for batch 232's absorption of two `kasayang` ledger rows.

Committing batch 231 healed the row in dom63 and dom67 and NOT in dom57. That
split has to be asserted, not just explained in a comment: a row absorbed for
the wrong reason is a failure nobody will ever see again. So --

  * both healed rows stay in LEDGER and are subtracted in ABSORBED;
  * dom57's row is in LEDGER and NOT in ABSORBED, because it is that log's own
    TARGET (`b57.py:127`) rather than a HEAD-relative HOLD, and can only heal if
    the map reverts;
  * all three still REFUSE if the map drifts, is reverted, or loses the entry.

    python .scratch/b232/ledger232.py
"""
import importlib.util
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("suite", "tools/orthography/suite.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

REAL = S.load_map()
META = set(hw for hw, _ in S.meta_rows())
KAS = "BROWN kasayang kasayang missing on [SLIYU]"
bad = 0


def say(good, name, detail=""):
    global bad
    if not good:
        bad = 1
    print("%-4s %-58s %s" % ("ok" if good else "BAD", name, detail[:74]))


def check(name, must_refuse, log, line, mp):
    _, why = S.adjudicate(log, line, mp, META)
    say(bool(why) == must_refuse, name, why or "explained")


def less(d, *keys):
    d = dict(d)
    for k in keys:
        d.pop(k, None)
    return d


# --- the split itself
for log, absorbed in (("dom57.py", False), ("dom63.py", True), ("dom67.py", True)):
    k = (log, KAS)
    say(k in S.LEDGER, "%s kasayang is in LEDGER" % log[:6],
        str(S.LEDGER.get(k)))
    say((k in S.ABSORBED) == absorbed,
        "%s kasayang absorbed=%s as its role requires" % (log[:6], absorbed),
        "TARGET in b57.py" if not absorbed else "HOLD off git HEAD")

# --- the reason, read off the files rather than trusted
b57 = open("tools/orthography/logs/b57.py", encoding="utf-8").read()
say('"kasayang"' in b57, "dom57's row is a TARGET: b57.py writes the pin")
for log in ("b63.py", "b67.py"):
    src = open("tools/orthography/logs/%s" % log, encoding="utf-8").read()
    say("kasayang" not in src,
        "dom%s's row is NOT a target: %s never names it" % (log[1:3], log))
import subprocess  # noqa: E402
head = subprocess.run(["git", "show", "HEAD:site/modern_map.js"],
                      capture_output=True, text=True, encoding="utf-8").stdout
# NB do NOT strip spaces to normalise here: the value IS two words, and
# `replace(" ", "")` turns the ruling back into the join it replaced.
say('"kasayang":"ka sayang"' in head,
    "HEAD carries the ruling, which is what re-baselined the two HOLDs")

# --- and every one of the three still refuses a map that moves
for log in ("dom57.py", "dom63.py", "dom67.py"):
    check("%s -- real map, EXPLAINED" % log[:6], False, log, KAS, REAL)
    check("%s -- ruling drifts" % log[:6], True, log, KAS,
          dict(REAL, kasayang="ka sayangg"))
    check("%s -- reverted to his own letters" % log[:6], True, log, KAS,
          dict(REAL, kasayang="kasayang"))
    check("%s -- map entry deleted" % log[:6], True, log, KAS,
          less(REAL, "kasayang"))

# --- absorption must not swallow a row that is still failing
say(("dom57.py", KAS) not in S.ABSORBED,
    "the live row was not absorbed along with its twins")

print("\n%s" % ("all controls behaved" if not bad
                else "SOMETHING BEHAVED BADLY"))
sys.exit(bad)
