# Pecoraro Taroko — 4-language Truku dictionary

Digitization of Ferdinando Pecoraro MEP's *Essai de dictionnaire taroko-français*
(SECMI, Paris, 1977). Original is Truku (Taroko) → French; we add English +
Traditional Chinese (translated from the French, draft pending native review).

- Live: https://pecoraro-taroko.netlify.app (Netlify project `pecoraro-taroko`, site_id `d6e80a1c-405b-4bf9-8977-3630174261c6`)
- All 398 pages digitized: 1,967 root entries, 2,948 sub-forms, 5,437 examples.

## Layout

- `scans/full/page_NNN.png` — page renders of the source PDF scan. The PDF's OCR
  layer is bad; entries were transcribed by reading the page images.
- `data/batch_*.json` — per-batch transcription+translation source files, merged
  by `tools/build_entries.py` into `site/entries.js`.
- `site/` — static app, no build step. Deploy this dir.
  - `entries.js` — ALL dictionary data (`window.ENTRIES`); source of truth
  - `index.html`, `style.css`, `app.js` — search + entry cards, ⓘ about sheet,
    ⚙ language-toggle sheet (fr/en/zh checkboxes → localStorage
    `taroko_pecoraro_langs_v1`; Truku always shown). Accepts `?q=` deep link.

## Entry data shape (entries.js)

```js
{ hw, tag: "(R)", crossRef?, paradigm?, truncated?, fr, en, zh,
  examples: [{ t, fr, en, zh }],
  subs: [{ form, paradigm?, fr, en, zh, examples: [...] }] }
```

`(R)` = racine/root as marked by Pecoraro; `°` lines = verb paradigm; `§` = example.

**Source data in `entries.js` is never modernized.** His spelling is the record;
the modern spelling is display-only, applied at render time by the ⚙ toggle. The
same principle governs `tidy()`: `entries.js` keeps the book's own punctuation.

## Hard invariants

- **Never run glosses through `modernize()`.** The char-rule fallback turns French
  "Palissade" into "Parissade". `mtext` covers Truku fields only.
- **Don't flatten `entries.js`** to match the flat `FORMS` index. The `(R)` marks
  and the nesting are Pecoraro's own judgments about what shares a root.
- **Don't expand the char rules** (`o→u`, `l→r`, `x→h`) without re-deriving from
  `Truku_Omnibus.xlsx`. `i→y` and `q↔k` were excluded deliberately.
- **A generated page must never read like a page he wrote.** Slot cards carry
  "Pecoraro does not define this form; he only lists it", italic gloss, dashed tag.
- **Pale is not a backlog to clear.** It is the honest mark on a respelling no
  modern source has confirmed. Two proposals to clear it in bulk were priced and
  rejected — see `.claude/notes/app-behaviour.md`.
- **Don't reinstate `#alpha-row`.** A–Z is the 🔤 sheet button.

## Deciding a spelling — the method rules

These were each learned by breaking something. Evidence for every one is in
`.claude/notes/map-history.md` and `.claude/notes/batch-log.md`.

- **The gloss of the candidate must match the gloss of the entry it renders in.**
  A shape hit plus high frequency is not evidence — `bitaq` was 321× and wrong.
- **Search from the meaning, not from the letter.** Ask the omnibus which modern
  word carries his Chinese, rather than deciding a letter and hoping a word exists.
- **The family is evidence in both directions.** A family that already agrees
  convicts a head that keeps its own letters; it also acquits.
- **An attested value can still be a wrong value.** Attestation tests cannot catch
  this; only the gloss can.
- **A label is not an argument**, and **a cognate explains a word but never spells
  one**.
- **A wrong-looking gloss is a question, not a verdict** — the paradigm answers it.
- **Two independent supporters must agree**; unanimity over one item is not
  unanimity.
- **A pin comes down when evidence overturns it, not when the rule tires**, and a
  pin naming one cause must be retired when a second cause appears.
- **Overriding evidence costs more than filling a hole.** Prefer the fix that adds.
- **The map is never evidence about colour; only the DOM is.** `WORD_OVERRIDES` is
  invisible to the generated map. Any tool asking "is this still green?" must
  consult the whole chain (`respellable()` reads three tables).
- **Decide slot by slot when a homophone exists**, not once for the root.
- **Same root in two dialects is not a licence to merge two cards.**

## Target

- **The metric is deliverable sentence pairs** — examples whose every Truku span
  is dark, over 5,435. **Currently 94.81%** (5,153). Not token share. A pair is
  what an MT session can consume; a token percentage is not.
- **100% dark is unreachable**, and is the wrong gate to set. Three classes can
  never clear by evidence: grammatical-morpheme cards (MPA 前綴 is a prefix, not
  a word), tier-J loans, and names no register lists.
- **Tier-J loans go dark via `loan_population.json`**, consumed in
  `build_verified.py` as of batch 172. Attestation is not a test a Japanese loan
  can fail — it is one it cannot sit, since no Truku wordlist will ever hold
  `abura` 油 or `budosyu` 葡萄酒.
- **A word settled by CLASS gets its own colour** (batch 196): names and loans
  emit code **16** and render `w-mod w-cls`, a deeper brown. The class is
  ADDITIVE — the span keeps `w-mod`, so every harness selecting on `w-mod` still
  counts it dark. Emitting them as code 1 said *a source lists this*, and none
  does.

- **A hand-ruled name goes in `HAND_NAMES`** (`inflection.py`), never in
  `name_population.json` — that file is regenerated by `build_modern_map.py` and
  hand edits vanish on the next map build (batch 197).

## Testing and measurement

- **Measure from the DOM, not from the map.** Assert against rendered cards.
- **Rank the pale by occurrence, not only by pair.** `blockers.py` ranks by
  sentence pairs, so a word spent on headwords and crossrefs never reaches it —
  the biggest pale word on the page (`treura`, 13) was invisible to it.
- **A green span is not a pale one.** Green means no map entry fired; the fix is
  a map entry, which is itself a spelling claim, not a warrant in `verified.js`.
- **A test that cannot see a colour reports it as an absence** — check the harness
  before believing a null result.
- **Assert the replacement COUNT** on any sweep, or you will unhook the audio.
- **Read a bad row as a diagnosis**, and don't diagnose a missing file from a
  truncated `ls`.
- **An empty candidate list is not a refusal.**
- **A greedy algorithm over an unordered input is a sample, not a rule.**
- Verifying crossref behaviour needs two taps: first shows the gloss preview,
  second opens the entry (`app.js:1272–1276`). A single `.click()` moves nothing.

### Keep the session's context lean

Autocompaction mid-investigation loses the evidence chain an adjudication is
built on. Every rule below exists to stop that.

- **Never print full card bodies, full diffs, or per-row output.** Redirect to a
  scratch file and read the tail.
- **A census run prints the summary line only** — dark / pale / green / total /
  cards / errors. No leaderboards unless they were asked for.
- **Don't re-derive a standing finding**; `grep .claude/notes/batch-log.md` for
  it. The refusals and the pins are already written down.

## Where the detail lives

Read these with the Read tool when you need the evidence behind a rule. They are
NOT loaded at session start, deliberately.

- `.claude/notes/map-history.md` — the modern-spelling map, batches 14–47: tier
  definitions, the idtrap and mirror sweeps, per-class decisions, generator
  invariants.
- `.claude/notes/batch-log.md` — batches 136–170: the name register, the pale
  census, per-batch adjudications and their DOM measurements.
- `.claude/notes/app-behaviour.md` — browse/search index, paradigm slot cards,
  display-time typography, crossref collapse, in full.

## Deploy

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6   # project: pecoraro-taroko
```
