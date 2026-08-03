# MT hand-off — annotated sentences and wordlist

Generated from the **rendered page**, not from the maps. Colour is the confidence
signal and it is only real in the DOM: `WORD_OVERRIDES` is invisible to
`modern_map.js`, so anything that asks a table instead of the page gets a
different answer. Regenerate with `scratchpad/mtexport.py` against a local server
on `site/` at port 8765.

## The three states

| status | class | means |
|---|---|---|
| `confirmed` | `w-mod` | a modern source — the Truku dictionary or the spoken corpus — **has this word**. Safe to train on. |
| `unconfirmed` | `w-unv` | a curated table **proposed** this respelling and no modern source confirms it. Usually regular morphology a 38,685-type dictionary simply does not list. Not wrong; not evidence. |
| `unmapped` | `w-raw` | no table knew the word; the blind character rules (`o→u`, `l→r`, `x→h`) ran and nothing vouched for the result. |

**A sentence is `deliverable` when every Truku span in it is confirmed.** That is
the same test behind the project metric, so this export and the metric agree by
construction: **4,951 deliverable**.

## Files

- **`mt_deliverable.tsv`** — the 4,951 fully-confirmed pairs, `truku ⇥ zh ⇥ en ⇥ fr ⇥ headword`.
  This is the file to train or translate from.
- **`mt_sentences.jsonl`** — all 5,437 examples, one JSON object per line, with
  `deliverable`, per-token `tokens[{w,c}]` (`c` = `d`/`p`/`g`), and the
  `unconfirmed` / `unmapped` token lists broken out. Use this to see *why* a
  sentence is blocked.
- **`mt_wordlist.tsv`** — 4,674 word types with status, total occurrences, and how
  many of those occurrences sit inside a deliverable sentence.

## Two things to know before using it

**`truku_pecoraro` is not token-aligned with `truku_modern`.** Modern mode joins
proclitics he spaced (`Ti malu` → `tgmalu`), so the two spellings of one sentence
have different token counts. The `tokens` array describes the MODERN string only.

**487 sentences are blocked, and 462 of them by a single word type.** The
bottleneck is narrow, not diffuse — the top 30 blocking types alone would free 81
pairs. If the MT session hits a sentence it wants that is blocked, the
`unconfirmed` list names exactly what is holding it.

**Source spelling is never modernized in the data.** Pecoraro's spelling is the
record; the modern spelling is display-only, applied at render time. That is why
this export is taken from the DOM.
