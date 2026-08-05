# Pecoraro Taroko — 4-language Truku dictionary

Digitization of Ferdinando Pecoraro MEP's *Essai de dictionnaire taroko-français*
(SECMI, Paris, 1977). Original is Truku (Taroko) → French; we add English +
Traditional Chinese (translated from the French, draft pending native review).

- Live: https://pecoraro-taroko.netlify.app (Netlify project `pecoraro-taroko`, site_id `d6e80a1c-405b-4bf9-8977-3630174261c6`)
- All 398 pages digitized: 1,967 root entries, 2,948 sub-forms, 5,436 examples.

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
- **A card head that is dark for the wrong reason licenses nothing beside it**
  (batch 199). His TABE `-un`/`-i` slots looked like clean gaps beside a dark
  `tbiyan` — which is glossed 下來, not 犁. Six wrong words in one ruling. Run the
  gloss test on the neighbour you are leaning on, BEFORE writing the value.
- **A pale slot beside three dark ones is the cheapest question on the page**
  (batch 199, the instrument that cleared 99%). His card is a paradigm, so ask
  what every other slot on it says, not what the analyser can say about the word.
- **A label is not an argument**, and **a cognate explains a word but never spells
  one**.
- **A wrong-looking gloss is a question, not a verdict** — the paradigm answers it.
- **An attestation test over pale words is circular** (batch 204). Pale MEANS not
  in `attested_modern`, so re-asking it returns 0 of 37 across the top seven
  cards. The only non-circular question is the meaning test: does a DIFFERENT,
  attested word spell his? For RNGUT 懷孕 it is `mshjil` and for SNOXEL 嫉妒 it is
  `hkrig` — different roots, so there is no respelling to find and the pallor is
  correct.
- **A lexeme modern Truku replaced is NOT a settled class** (batch 204). The four
  classes share one property: attestation is a test they cannot SIT. An obsolete
  verb can sit it and fails it. Naming a fifth class there is the bulk clearance
  already priced and rejected twice.
- **A modern homophone is not a freeze** (batch 204). `sgsapat` 姦淫 (2× parquet,
  1× Bible) acquits his SAPAT 放蕩 head, which the register also lists as 舖床:
  both roots are real. But the acquitted head still cannot license its family,
  because it is dark on the OTHER one.
- **Two independent supporters must agree**; unanimity over one item is not
  unanimity.
- **A pin comes down when evidence overturns it, not when the rule tires**, and a
  pin naming one cause must be retired when a second cause appears.
- **Overriding evidence costs more than filling a hole.** Prefer the fix that adds.
- **The map is never evidence about colour; only the DOM is.** `WORD_OVERRIDES` is
  invisible to the generated map. Any tool asking "is this still green?" must
  consult the whole chain (`respellable()` reads three tables).
- **Decide slot by slot when a homophone exists**, not once for the root.
- **`CITE_SPELL` cannot split a homograph he carded TWICE** (batch 205). The
  `naru`/`nalu` fix worked on an asymmetry — one sense had a headword, the
  other only sentences. DIMA heads 竹子 AND 已經, QALO heads 梳子 AND 豬油, and in
  both his example sentences are the sense the map already renders. A remap
  would paint four correct sentences wrong to fix three heads. Leave them.
- **Score a gloss filter against HIS gloss, never a pairing file's abbreviation
  of it** (batch 205). `omnibus_gloss_pairs.json` carries 腳掌 for LAMIL, which
  shares no character with `ramil` 拖鞋 and flagged a freeze. His own entry reads
  腳掌／鞋底－（引申＝）鞋子 and his family is `Mklamil` 穿鞋子. No freeze.
- **A freeze detector needs an OUTSIDE voice to propose the alternative**
  (batch 206). Run over the whole book with no pairing file, the gloss test
  flags 827 of 2,420 dark headwords — synonym pairs, not freezes (`tama` 父親
  vs 上帝). Adding a shape-search second leg leaves 156, still noise, because
  both legs are then the same test wearing a hat. `logs/freezesweep.py` keeps
  the negative result reproducible; don't rebuild it.
- **Two gloss-verified sources disagreeing is a freeze detector** (batch 205).
  Where the map value's register gloss shares no character with his and a
  second source's value does, the span is dark AND wrong. 29 of 413 flagged;
  most were the same root inflected, and only 2 survived the different-root
  test. Run it on any new pairing file before treating the file as absorbed.
- **Same root in two dialects is not a licence to merge two cards.**
- **A sibling is only a sibling if it is the same card.** A ruled form one slot
  over licenses its neighbour — but check which headword it comes off first:
  `pngraq` is his Png'laq off NG'LAQ 愚蠢, not G'LAQ 拿取 (batch 198).
- **Bucket the pale before working it** (batch 198): root attested-and-glossed /
  root listed-unglossed / no analysis. That prices the seam. It does not rule
  anything — `HAND_RULED` will darken any value put in it, so the pricing has to
  come first or the metric decides the spelling.
- **The analyser cannot see reduplication.** `inf.roots()` has no rule for it, so
  every CC-/VV- form reports no root. That is a fact about the analyser, not a
  verdict about the word — strip the doubled onset by hand before believing it.
- **His own parenthetical is testimony that two spellings are one word** (batch
  200). Where he writes `X (Y)`, `X (vl. Y)`, `X (Y ?)` and the map sends the two
  to different values of which exactly ONE is dark, the pale side should render
  what the dark side renders — a consistency fix, not a new attestation claim.
  **The dark side still has to pass the gloss test**: 7 of 17 were refused because
  the dark value is dark on a homograph, and following it would spread a freeze.
- **Search his own book, not only the register.** `nilit` looked like an override
  of `mirit` 山羊 until the count came in: he writes `milit` 15× and `nilit` 2×.
  His own text spelled it. Same instrument proved `dbsnawan` an ethnonym —
  `dSbnawan ni dTroko` stands it beside the Truku.
- **A char-rule contradiction inside one root is a bug, not a variant** (batch
  201, three of them: `mp'yax`→`mpyah` beside `iyax`, `upsk'la`→`upskra` beside
  `skla`, and the DLUT crossing). Where `l→r` or `x→h` fires on one slot of a card
  whose other slots keep the letter, the char rule has overreached — check the
  siblings before believing the fallback.
- **A diacritic can be the whole distinction** (batch 201). His `ç` vs `x` is what
  separates KOYOç 雨 from KOYOX 女人—妻子; `plain()` strips it downstream, so a
  sweep keyed on shape will cross the two cards. The gained/LOST assertion is what
  catches it — `koyox → quyux` broke the 女人 card and was reverted.
- **A single gloss row is not the register's answer; the family is** (batch 200).
- **A refusal that names one blocker dies when that blocker is removed** (batch
  202). `naru` was refused three times for one reason — "a token-keyed map cannot
  split them" — and his `nalu` really is two words (好 in seven sentences, 代替 on
  his own headword). `CITE_SPELL` in `app.js` fires only where `noLink === true`,
  which is every render of a form as a NAME and no render of running text. A
  citation entry can only REFUSE the map's value, never assert a new one, so a
  wrong seam costs a pale headword and not a dark wrong word. That asymmetry is
  the licence; do not use the hook to assert.
- **A settled class is a fourth kind of answer**, beside ruled, refused and
  pending (batch 203). Where a word is pale because the register has no reason to
  carry it — a wild species, a name, a loan, an onomatopoeion, a bare affix —
  the fix is to name the class, not to hunt harder. Ask which of the four it is
  BEFORE pricing a respelling: `klulu` was refused twice as a spelling and is
  correct as a class.
- **A multi-letter affix article scores its MODERN prefix** (batch 203). `mpa`
  scores 0 and `emp` scores 689; the zero is the tier-W schwa showing up as a
  lookup miss, not evidence against his card. `HAND_AFFIX` names the string to
  count.
- **Census per TOKEN, never per headword** (batch 203). A multi-word head like
  WA"LO 蜜蜂 has no single map key, so a headword-keyed census reported eight
  already-dark cards as green.
- **A sentence-corpus gloss is not the headword's gloss** (batch 203). `bgiya`
  appears in 都是專捕虎頭蜂人 but its own row reads 打緯線; `srcing` is the 虎頭蜂.
- **Two supporters must be INDEPENDENT, not the same test twice** (batch 203).
  Closest-string alone proposed a Japanese surname for a given name; his own
  `(m)`/`(f)` tag checked against the register's 男名/女名 refused nine of fifteen.
- **Ask the scan before you blame the language** (batch 202). His French `m`
  renders n-like at page resolution. Crop the disputed glyph and a known `n` and
  a known `m` **from the same line** at 6×, and count legs.
  `damat`'s only row reads 恢復原狀, which would have refused `pdmati`; the five
  family members are all 菜餚/配菜 and his card agrees with them.

## Target

- **The metric is deliverable sentence pairs** — examples whose every Truku span
  is dark, over 5,429. **Currently 97.90%** (5,315). Not token share. A pair is
  what an MT session can consume; a token percentage is not.
- **Rank by SOLE blockers, not by occurrences** (batch 200). One pale word can
  hold a whole example hostage; 216 of the 227 blocked pairs were blocked by a
  single type. The occurrence ranking spends effort where the pairs are already
  lost. The 2-or-more-pair tier is now exhausted — ruled or refused in writing.
- **Every blocker tier is now closed** (batch 201). The sole-blocker tier went to
  zero open, and the 2-blocker tier behind it — 10 clusters, no recurring word
  pair — is ruled or refused item by item. The 130 pairs still blocked are held by
  words with a written refusal, so the next gain has to come from new evidence,
  not from re-ranking what is already priced.
- **French in a Truku field is not a pair, and was inflating the metric.** Six
  example rows have a `t` identical to their `fr` — his AN (3) card demonstrates
  the circumfix that way (`Paro = Grand; Knplaan = Grandeur`). `metaLine()` in
  `app.js` renders those with no spans at all, which drops them from the
  denominator because the metric reads the DOM. **Five of the six had been
  counted DELIVERABLE**: French sentences scoring as Truku pairs. The test is
  `t == fr` modulo punctuation — it finds exactly six, no near misses, because no
  real sentence equals its own translation. Denominator 5,435 → **5,429**.
- **A zero-span row is a transcription question, not just an exclusion** (batch
  207). The exclusion list ran to eight, not the six `t == fr` rows — and reading
  the other two found one real defect. His PARU example `Ini kparo ka muxeng na!`
  had `fr = "Son…"` because the French runs over the page break, and page 214's
  leadin carried `…nez n'est pas grand.` as a row of its own with
  `t = "… (suite de la page précédente)"` where the Truku should be. One sentence
  filed as two. The other, `Mluxai § Est ce qu'il en aurait pris l'habitude`, is
  **his** omission — the scan at 1.8× shows the § followed directly by French, so
  the empty `t` is the faithful record and stays. Examples 5,437 → **5,436**;
  denominator unchanged at 5,429, because a French `t` renders no spans either
  way. Check the exclusion COUNT against the rule that predicts it. The orphan
  row was not inert: **a French `t` field is a Truku field to the generator**, and
  the census had mapped his page-break marker's *page* to `pagi` (tier R).
- **A transcription slip can land on an attested word** (batch 208). His
  `ln'xlax` was read as `lm'xlax`, which char-rules to `lmhlah` — a word the
  register lists. Dark, correctly spelled, wrong sentence: the homograph-freeze
  shape arriving through the scan instead of through the map, and invisible to
  every colour metric because the span was already dark. Crop the glyph with a
  known `m` **from the same line** at 3× and count legs. The correct reading cost
  nothing — `lnhlah` came back code 2 off the same root.
- **The apparatus is not the sentence** (batch 208). The page marks his editorial
  notes `.meta-abbr` and the superseded word `.w-orig`; the colour metric ignores
  both, correctly, because neither is a Truku claim. Anything harvesting
  `.truku` textContent ships them as Truku — `Mapa brunguy (porter la hotte)`
  went out as a training pair. Scope span queries to `.truku` too: unscoped they
  count 700 gloss spans in 256 rows, so a pale name in the FRENCH blocks a row
  whose Truku is entirely dark.
- **A span and a word are not the same unit, in either direction** (batch 208).
  One span can hold two words (`Mpaso` renders `Empaa su`), one hyphenated word
  can hold two spans (`Empa-laqi`). Any check comparing rendered text against the
  token list has to break both sides into pieces first.
- **The gained/LOST check must match the file's own indentation** (batch 207).
  `verified.js` writes keys with two leading spaces, `modern_map.js` with none —
  so `^  "(.+?)":` over the map reports every change as no change. It reported a
  clean diff while the map had lost an entry.
- **A homograph freeze paints dark AND wrong** — a raw token mapped onto a
  same-shaped modern word with an unrelated gloss. Batch 201 found **seven**,
  including his KOYOç 雨 head frozen onto `kuyuh` 女人. They are invisible to every
  colour metric, because the span is already dark. Only the gloss test finds them.
- **100% dark is unreachable**, and is the wrong gate to set. Three classes can
  never clear by evidence: grammatical-morpheme cards (MPA 前綴 is a prefix, not
  a word), tier-J loans, and names no register lists.
- **Tier-J loans go dark via `loan_population.json`**, consumed in
  `build_verified.py` as of batch 172. Attestation is not a test a Japanese loan
  can fail — it is one it cannot sit, since no Truku wordlist will ever hold
  `abura` 油 or `budosyu` 葡萄酒.
- **A word settled by CLASS gets its own colour** (batch 196): names, loans and —
  since batch 201 — onomatopoeia (`HAND_ONOM`, read off his own gloss) emit code
  **16** and render `w-mod w-cls`, a deeper brown. The class is
  ADDITIVE — the span keeps `w-mod`, so every harness selecting on `w-mod` still
  counts it dark. Batch 202 added the fourth, `HAND_SPECIES`, closed at seven in
  batch 203: his
  KLULU is 爬牆虎, the Virginia creeper he pressed into service for the grapevine
  the Taroko did not have, and a wordlist of everyday speech will not hold wild
  flora. **Price the seam before opening a class** — 512 single-word headwords on
  his thematic lists, only 24 not dark, of which five are species. A class, not a
  door. Emitting them as code 1 said *a source lists this*, and none
  does.

- **A hand-ruled name goes in `HAND_NAMES`** (`inflection.py`), never in
  `name_population.json` — that file is regenerated by `build_modern_map.py` and
  hand edits vanish on the next map build (batch 197). **A hand-ruled loan goes in
  `HAND_LOANS`** for the same reason; `loan_population.json` is regenerated too
  (batch 199). The generator reads his `tag` for the loan verdict and cannot see
  one he wrote into a gloss.
- **A manual entry of the form `X → X+C` corrupts the strip rule** (batch 199).
  `psilin → psiling` produced `psiling → psilingg` and `mpsiling → empsilingg`:
  the rule strips the final consonant, finds the manual value, re-appends. Pin
  both shapes. The gained/LOST check is what catches it.

## Testing and measurement

- **Run the suite with `python tools/orthography/suite.py`** (site served at
  :8765, ~4 min). It runs every `logs/dom*.py` and `freeze2*.py` and adjudicates
  what they report against a ledger keyed on the exact failure line. Green reads
  `54 logs — 23 clean, 181 superseded, 0 REGRESSIONS`.
- **A frozen measurement is not a test until something adjudicates its
  failures** (batch 209). The logs are records of what a batch measured; the
  project moves under them, so failures accumulate that are not regressions. 181
  of them had, and the sweep before had reported zero by reading a stale
  `verified.js`. **Never edit a log to make it pass** — that destroys the only
  evidence anything moved. The supersession goes in the ledger, naming the batch
  that overturned the pin.
- **A supersession must re-assert the reason, not excuse the failure** (batch
  209). `dark` re-checks that the word is dark AND alone; `map` re-reads
  `modern_map.js` so a drift to a third spelling still fails; `meta` re-derives
  batch 207's metalinguistic test from `entries.js`. And **run the negative
  control** — 13 tampered lines fed to `adjudicate()` — because a ledger that
  cannot fail is a list of excuses.
- **A pinned occurrence count is a snapshot of a growing book** (batch 209). All
  eight count drifts were increases, from later pages and from map arrivals.
  Assert a floor, never equality; a count that FALLS is the news.
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
- `.claude/notes/batch-log.md` — batches 136–204: the name register, the pale
  census, per-batch adjudications and their DOM measurements.
- `.claude/notes/app-behaviour.md` — browse/search index, paradigm slot cards,
  display-time typography, crossref collapse, in full.

## Deploy

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6   # project: pecoraro-taroko
```
