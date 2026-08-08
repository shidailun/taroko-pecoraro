# -*- coding: utf-8 -*-
"""Snapshot / diff verified.js and modern_map.js. Each file's OWN indentation."""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, "site")
OUT = os.path.dirname(os.path.abspath(__file__))


def verif():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), m.group(2))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def mapp():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:t.index("\n};", a) + 2], re.M))


def dump(tag):
    for n, f in (("verif", verif), ("map", mapp)):
        d = f()
        io.open(os.path.join(OUT, "%s_%s.txt" % (n, tag)), "w",
                encoding="utf-8").write(
            "\n".join("%s\t%s" % (k, d[k]) for k in sorted(d)))
        print("%s %s: %d" % (tag, n, len(d)))


def diff(tag):
    for n, f in (("VERIF", verif), ("MAP", mapp)):
        old = dict(l.split("\t") for l in io.open(
            os.path.join(OUT, "%s_%s.txt" % (n.lower()[:5], tag)),
            encoding="utf-8").read().splitlines() if l)
        new = f()
        lost = sorted(set(old) - set(new))
        got = sorted(set(new) - set(old))
        ch = sorted(k for k in set(old) & set(new) if old[k] != new[k])
        print("%-6s %d -> %d  lost=%s new=%s changed=%s"
              % (n, len(old), len(new), lost[:8], got[:8],
                 [(k, old[k], new[k]) for k in ch[:8]]))


if __name__ == "__main__":
    (dump if sys.argv[1] == "dump" else diff)(sys.argv[2])
