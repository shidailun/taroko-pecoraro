# -*- coding: utf-8 -*-
"""Print the exact LEDGER key `suite.py` will compute for each failure line.

Writing a ledger key by hand from a log's format strings is how a row silently
matches nothing; ask the adjudicator's own `sig()` instead. Serial, because a
contended run under-renders (batch 217).

    python .scratch/b241/keys.py dom217.py dom230.py ...
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

for name in sys.argv[1:]:
    f, txt, rc = S.run(name)
    for line in S.failures(txt):
        head, got = S.sig(line)
        print("--- %s  rc=%d" % (f, rc))
        print("LINE %s" % line)
        print("HEAD %r" % head)
        print("GOT  %r" % got)
        print()
