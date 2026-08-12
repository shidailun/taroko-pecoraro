# -*- coding: utf-8 -*-
"""Emit the batch-242 ABSORBED additions, keyed from the real healed set."""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

WATCH = ['dom232.py', 'dom235.py', 'dom236.py', 'dom237.py', 'dom238.py',
         'dom239.py', 'dom241.py', 'dom58.py']
seen = set()
for f in WATCH:
    _, txt, _rc = S.run(f)
    for line in S.failures(txt):
        seen.add((f, S.sig(line)[0]))
healed = sorted(k for k in set(S.LEDGER) - seen - S.ABSORBED if k[0] in WATCH)


def pystr(s, ind):
    words, out, cur = s.split(" "), [], ""
    for w in words:
        cand = cur + w + " "
        if cur and len(repr(cand)) + ind > 79:
            out.append(cur)
            cur = w + " "
        else:
            cur = cand
    if cur:
        out.append(cur)
    out[-1] = out[-1].rstrip(" ")
    return ("\n" + " " * ind).join(repr(c) for c in out if c)


COUNT = ('dom236.py', 'dom237.py', 'dom238.py', 'dom239.py', 'dom241.py')
G = {}
for f, h in healed:
    if 'keys' in h and 'pinned' in h:
        g = 'count'
    elif f == 'dom58.py':
        g = 'head'
    elif 'sentence sweep' in h:
        g = 'skip'
    else:
        g = 'rekey'
    G.setdefault(g, []).append((f, h))

C = {
 'count': """    # [batch 242] A raw COUNT assertion healed without its subject moving --
    # the arithmetic refilled the hole, and the reason each row records is still
    # literally true. Batch 241's transcription fix dropped the DEAD `snuk` key
    # and left the map at 7370 against a pin of 7371, which is what these five
    # rows explain. Batch 242 added exactly ONE key, `sloweq` (the SLOWEQ head
    # had no map entry at all, which is why it rendered GREEN), and the map is
    # back at 7371. `snuk` is still gone -- `MAP.get("snuk")` is None -- so
    # nothing these rows assert has been undone; a key count simply cannot tell
    # "the lost key came back" from "a different key arrived". Batch 241 noted
    # that dom241's ORPHAN check has an escape hatch its raw count "does not
    # have"; this is the raw count's own blind spot, and it is the reason the
    # rows are kept rather than retired.""",
 'rekey': """    # [batch 242] Re-keyed, not retired. Both lines carry a LIST inside the
    # message, so clearing a cluster changes the key rather than silencing the
    # assertion -- which is exactly what batch 241 said this shape was for ("a
    # NEW row of this shape re-keys and is reported"). Batch 242 cleared
    # `tbasyaq+tibasyaq` and `dmtbasyaq+dmtsapat`, so both messages re-key and
    # their successors are in the batch-242 block above, carrying the new
    # lists. The old keys can only fire again if the rulings revert.""",
 'skip': """    # [batch 242] The assertion did not RUN. dom232 prints `parquets not
    # mounted -- sweeps 1 and 2 SKIPPED`, which is batch 232's own rule working
    # (an absent source must skip, not bank its emptiness as a zero) -- and a
    # sweep that does not run emits no failure line, which reads on screen
    # exactly like a pin retiring. An absence the instrument cannot see is not
    # a healing. The row stays live in LEDGER for whenever the parquets are
    # mounted again.""",
 'head': """    # [batch 242] Batch 226's mechanism once more, on the log batch 230 added
    # to the class: `dom58.py:12` reads its *before* map from `git show
    # HEAD:site/modern_map.js`. Batch 238 ruled `bsqan -> pskan`, and once that
    # went into HEAD the log's before and after agree, so no HOLD row for the
    # old `bsekan` is generated at all. Note this healed BEFORE batch 242
    # touched anything -- it is the commit of b43895b, not this batch's work.""",
}

out = []
for g in ('count', 'rekey', 'skip', 'head'):
    out.append(C[g])
    for f, h in G.get(g, []):
        out.append("    (%r,\n     %s)," % (f, pystr(h, 5)))
io.open(os.path.join(ROOT, ".scratch", "b242", "absorbed.py"), "w",
        encoding="utf-8").write("\n".join(out) + "\n")
print("healed %d, grouped %s" % (len(healed),
                                 {k: len(v) for k, v in G.items()}))
