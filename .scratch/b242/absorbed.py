    # [batch 242] A raw COUNT assertion healed without its subject moving --
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
    # rows are kept rather than retired.
    ('dom236.py',
     'FAIL the map has # keys, pinned #: this batch moved three VALUES and no '
     'key'),
    ('dom237.py',
     'FAIL the map has # keys, pinned #: batch # changes no spelling at all'),
    ('dom238.py',
     'FAIL MAP keys #, pinned #'),
    ('dom239.py',
     'FAIL MAP keys #, pinned #'),
    ('dom241.py',
     'FAIL MAP keys #, pinned #'),
    # [batch 242] Re-keyed, not retired. Both lines carry a LIST inside the
    # message, so clearing a cluster changes the key rather than silencing the
    # assertion -- which is exactly what batch 241 said this shape was for ("a
    # NEW row of this shape re-keys and is reported"). Batch 242 cleared
    # `tbasyaq+tibasyaq` and `dmtbasyaq+dmtsapat`, so both messages re-key and
    # their successors are in the batch-242 block above, carrying the new
    # lists. The old keys can only fire again if the rulings revert.
    ('dom235.py',
     'FAIL a two-type cluster this batch pinned has left the book '
     '(snuk+thiy): batch # confirmed all four as refusals, so one healing is '
     'news'),
    ('dom236.py',
     "FAIL the two-type seam moved: # rows, [('dmtbasyaq', 'dmtsapat'), "
     "('krikut', 'nrikut'), ('tbasyaq', 'tibasyaq')]. Batch # confirmed all "
     'four refusals; a NEW row of this shape is a pair the sole-blocker '
     'ranking cannot see.'),
    # [batch 242] The assertion did not RUN. dom232 prints `parquets not
    # mounted -- sweeps 1 and 2 SKIPPED`, which is batch 232's own rule working
    # (an absent source must skip, not bank its emptiness as a zero) -- and a
    # sweep that does not run emits no failure line, which reads on screen
    # exactly like a pin retiring. An absence the instrument cannot see is not
    # a healing. The row stays live in LEDGER for whenever the parquets are
    # mounted again.
    ('dom232.py',
     'FAIL the sentence sweep returned # proposals, expected #'),
    # [batch 242] Batch 226's mechanism once more, on the log batch 230 added
    # to the class: `dom58.py:12` reads its *before* map from `git show
    # HEAD:site/modern_map.js`. Batch 238 ruled `bsqan -> pskan`, and once that
    # went into HEAD the log's before and after agree, so no HOLD row for the
    # old `bsekan` is generated at all. Note this healed BEFORE batch 242
    # touched anything -- it is the commit of b43895b, not this batch's work.
    ('dom58.py',
     'BROWN bsqan bsekan missing on ["QAN]'),
