# -*- coding: utf-8 -*-
"""For the nine rows the first run called HEALED: are they seen now, or not?

Serial, one log at a time (batch 217): a contended run under-renders and an
absence it cannot see reads as a healing.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

WATCH = ['dom232.py', 'dom235.py', 'dom236.py', 'dom237.py', 'dom238.py',
         'dom239.py', 'dom241.py', 'dom58.py']
MAP, META = S.load_map(), set(hw for hw, _ in S.meta_rows())
for f in WATCH:
    _, txt, rc = S.run(f)
    seen = set()
    for line in S.failures(txt):
        head, _ = S.sig(line)
        seen.add(head)
    mine = [k for k in S.LEDGER if k[0] == f]
    for k in sorted(mine):
        if k[1] not in seen:
            print("UNSEEN  %-12s %s" % (f, k[1][:120]))
            print("        absorbed=%s" % (k in S.ABSORBED))
    print("== %-12s rc=%d  %d failure lines, %d ledger rows"
          % (f, rc, len(seen), len(mine)))
