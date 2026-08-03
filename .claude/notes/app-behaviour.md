# App behaviour: browse, slots, typography — full findings

<!-- Moved out of CLAUDE.md 2026-08-03 to keep the always-loaded file small. Content is verbatim; nothing was deleted. -->

## Browse and search (2026-07-28)

Pecoraro's root organization is the storage shape; `FORMS` in `app.js` is a second
index over it giving all 4,914 forms (1,967 headwords + 2,947 sub-forms) their own
alphabetical slot. In a letter listing a root renders as a full entry card and a
sub-form as a one-line cross-reference stub (form → root + first enabled gloss)
that opens the root on tap. Don't flatten `entries.js` to match — the `(R)` marks
and the nesting are Pecoraro's own judgments about what shares a root.

Every form carries both spellings (`key` original / `mkey` modern), and `INDEX`
carries `mhw`/`mforms`/`mtext` alongside `hw`/`forms`/`text`, all built through the
same `modernize()` path the display uses. Consequences:

- Search matches either orthography whichever way the ⚙ toggle is set (`hbuy` finds
  XBUI, `qpah` finds K'PAX). Ranked: headword prefix → sub-form prefix → full text.
- `mtext` covers Truku fields only. Never run the glosses through `modernize()` —
  its character-rule fallback turns French "Palissade" into "Parissade".
- Letters bucket and sort by the spelling on screen, so the A–Z row itself differs
  by mode: modern gains H and J (DIMA→JIMA, d→j before i) and keeps a 4-form X row
  (map `id` tier). It is recomputed on toggle, not cached. **Modern used to lose O
  as well, and that was a defect** (fixed 2026-08-01): o→u is a rule about his
  vowel, not about the topic marker, which modern Truku writes `o` — so the modern
  O row now exists and holds exactly one card, his own O particle entry. See
  `WORD_OVERRIDES` in app.js.
- Toggling while browsing follows the words, not the letter (X → H), via
  `rerender()`; calling `render()` there would turn the listing into a search.
- A–Z is the 🔤 sheet button, shown on the cover and in results alike. The strip
  the pre-redesign code built along the bottom of the cover is gone for good: it
  was an opaque band across the "FERDINANDO PECORARO MEP" byline, and it was
  unreachable from a listing. Don't reinstate `#alpha-row`.

## Paradigm slots — a page for a form he only LISTED (2026-08-02)

`FORMS` covers headwords and sub-forms, which is everything he filed. It is not
everything he *wrote*: his `°` lines name 1,045 further types (1,028 of them
unambiguously one entry's), and those had no page, so a reader meeting `kgusi` in
a sentence had nowhere to go. **998 of them are now generated cards**, merged into
the A–Z listing (5,023 rows → **6,021**) and linked from every sentence and every
`°` line that uses the token. `SLOTS` / `SLOT_KEY` in app.js, built lazily like
`buildConc`.

- **The label is read off the POSITION, not the suffix.** His five-cell `°` lines
  are AF, citation root, imperative, LF, PF, in that order — measured **380/380**
  for `-an` at cell 4 and 380/381 for `-un/-on` at cell 5 (`parslot4.py`). The lone
  exception, `Pskingal ° Mpskingal, pskingal, pskngali, pskngalan, pskngalu`, is
  his own truncation and still reads right positionally. That is what rescues the
  syncopated tokens (`d'si`, `pai`) a suffix table can never reach; `SLOT_SUF` is
  the fallback for lines that are not five cells, and where neither works the card
  says "form of X" and claims nothing. Measured on screen: 346 imperative, 337
  patient focus, 190 locative focus, 102 actor focus, 16 citation, **7 unlabelled**.
- **A `°` line is cut into CELLS, not into words** (`cells()` in app.js). A token
  inside brackets is his *second spelling of the same slot* — `plqe (pl'qe)` — and
  `.?.` is a slot he could not fill, which has to open an empty cell or everything
  after it shifts left. Reading by token made both of those into new slots, so
  `Mploq, ploq, plqe (pl'qe), plqan (pl'qan), plqon (pl'qon)` counted eight and
  forfeited the positional read entirely: 321 five-token lines against **381**
  five-cell ones, and the invariant is *stronger* on the wider basis, not weaker.
  Unlabelled cards fell 33 → 7.
- **It is marked as generated, in the text and in the type.** Every card carries
  "Pecoraro does not define this form; he only lists it" in both languages, the
  gloss is italic (`.gloss.morph`), and the tag is dashed rather than solid. A
  page we built must never read like a page he wrote.
- **The examples are the concordance, not new data.** `CONC_IDX[s.key]` already
  answers "where else in the book does this exact token occur?" — 278 slot pages
  carry at least one, 584 sentences in all (`slotex.py`). The other 720 say so
  plainly rather than rendering an empty card.
- **`lookupWord()` always wins.** A form with an entry of its own is not this
  index's business, and the test is `lookupWord()` rather than membership of
  `FORMS`, because his bracketed aliases reach an entry through a slot `FORMS`
  does not hold. On KGUS's line that leaves exactly `kgusi` and `kgusun` generated
  — `kgusan` is his own sub-form and keeps its crossref.
- **A slot link opens on ONE tap**, unlike a crossref. The two-tap pattern exists
  to show a gloss before navigating, and a slot has no gloss to show; its whole
  card is the one line of morphology the preview would have carried.
- **`data-slot` must NOT go on the card's `<article>`.** With it there, the click
  handler's `closest()` walks up from any tap inside the page — including a
  crossref in a borrowed sentence — and re-opens the same page. The selector names
  only the two things that carry it (`.slot-link`, `.entry.idx-slot`), and the
  `.slot-parent` branch is checked *above* it or the root link is swallowed.
- `currentFirst` is now the merged `{k, f}` / `{k, s}` row, not a `FORMS` record,
  because the first thing under a letter can be a slot; `rerender()` dispatches on
  `.f`. Slot records and FORMS records both have `.entry` and `.key`, so they
  cannot be told apart by duck-typing — don't try.
- `slotMatches("")` returns `[]`, so the whole-dictionary census is untouched:
  `?q=%CC%81` still gives **1,967 cards / 895 concordance lists / 22,190 rows**
  (`kgus4.py`), 0 page errors. `slotdom.py` is the feature's own check.

**The `-an`/`-un`-as-evidence proposal, priced and rejected (2026-08-02).** Giving
the LF/PF slots of a dark root a `verified` entry sounds like it should move the
dark ratio and does not: **+114 occurrences → 94.3843%**, or 94.5013% with the
imperatives, both *below* the line-mate rule's 94.7982% and all three short of 95%,
which needs +388 of the 2,579 pale occurrences. `palemake.py` decomposes the
DOM-measured pale census and says why: **861 of the 1,453 pale types are `(other)`**
— no derivable suffix slot at all — carrying 1,585 occurrences, and the heaviest
pale words (`liwis` 38, `mikat` 33, `ingay` 24, `lauken` 22, `nta` 20, `lubyaq` 20)
are not paradigm slots. Turning every pale word dark gives 99.928%, so the ceiling
is real; the route to it is that bucket, not the paradigm. Its `roots()` deliberately
over-generates (each of `aeiou`, plus the `m-`/`-m-` readings) so the small answer is
a genuine ceiling and not an artifact of the stemming.

**"He used it in a sentence, so make it dark" — priced and rejected too
(2026-08-02).** It is the one rule that clears the bar: 292 pale types / 767
occurrences → **95.8529%**. It is still wrong, because it answers a different
question. `build_verified.py`'s two levels both assert something about the
**modern** spelling — that the exact string is one of the 40,760 types in
`attested_modern.json`, or that it is a regular inflection of a listed root whose
modern gloss agrees with his Chinese. A sentence in the 1977 book attests **his**
spelling; it cannot confirm ours. `sktama` (11 occurrences, the fourth-heaviest
such word) is the standing counter-example — he uses it, and nothing in the modern
lexicon glosses 先父. Pale is not a backlog to be cleared; it is the honest mark on
a respelling no modern source has confirmed.

## Display-time typography (2026-07-28)

`tidy()` in `app.js` normalizes punctuation and capitalization at render time, by
language — `entries.js` keeps the book's own text, exactly like the spelling
toggle. Pecoraro's habits were inconsistent (`ka iso ! T'mlong` beside
`ka isu, mkla`), and 3,901 of his 5,437 example sentences have no final stop at
all. Rules: Latin text gets flush punctuation, one space after `,;:`, a capital
at each sentence start (an abbreviation list keeps `nb.` / `vr.` / `e.g.`
mid-sentence), his two-dot ellipsis `..` → `…`, dangling trailing dashes dropped,
and a final `.` when the line ends in a word; **French** additionally takes a
narrow no-break space before `;:!?»` — after a word only, so his `(??)` query
marks stay together; **Chinese** takes full-width punctuation and brackets
(converted as a pair, judged by what is inside), loses spaces only between two
Chinese characters (`參見 QDALAN` keeps its space), and ends in `。`. Truku
example lines run through the Latin path. Headwords, sub-forms and `°` paradigm
lines are NOT tidied — they are words and form lists, not sentences.

One-line contexts (A–Z stubs, the hover/tap word preview) show a single gloss and
pick **EN → 中 → FR**, not the fr/en/zh order a full entry uses: French is the
source language, and picking it first made a letter listing look like an
untranslated French dictionary. (There are no French-only definitions in the
data — every gloss has all three — but 273 entries (13.9%) have no definition in
any language, because Pecoraro left them blank himself.)

`collapsed()` drops the bracket when a bracketed form's spellings converge in
modern Truku — `L'NGLONG (LNGLONG)` is LNGLUNG twice — and keeps it when they
stay apart (`Pklilu (Plilu ?)`). `FORMS_MOD` is filtered to match, or the merged
alias would set a second identical row in the letter listing; `FORMS_ORIG` is
not, since in Pecoraro's spelling they are two spellings and both earn a slot.

The same convergence happens inside a **root tag**, where his brackets are his
second try at the word, and `collapsed()` never sees it: it guards the form field,
and `variants()` splits on `()=?` but not on his dash, so `(TNG'I – T'NGI)` reaches
it as one string. `collapseTagBrackets()` (modern mode only) therefore works bracket
by bracket, dropping a segment that has no word in it, that is the headword again,
or that is a spelling of a word the bracket already listed — and dropping the whole
bracket when nothing is left. Of two converging segments it keeps the one that says
more, measured with the `=` and `?` removed, so GILA's `(= TGILA ? - Vr. TGILA)`
still says *variante* rather than becoming a bare `(= TGILA?)`. Measured over all
443 root-mark tags in the real DOM: 14 brackets distinguishing a word from itself
before, 0 after, and the 13 word types that stopped rendering are all the headword
repeating itself beside a `→` cross-ref that still names it. Pecoraro mode is
untouched — there `(TNG'I – T'NGI)` really is two spellings on the page.

Most of the 164 tags this changed lost only a letterless segment: `(=? - = TAMA?)`
became `(= TAMA?)`. That is the existing rule about his bare uncertainty (a bracket
whose whole content is `= ? .` is already dropped, since the √ implies it) finally
reaching the same thing inside a dash list.

**A `crossRef` arrow can point at its own headword, and there the collapse is the
wrong fix (2026-07-30).** Found while checking that batch 22's `dxeyaq` entry made
D'XYAQ's `(vl. DXEYAQ)` tag collapse — it did, to a bare √, but the same card carried
a second line reading `√ → THIYAQ`. `xref.py` counts the class: of 124 `crossRef`
fields, **26 have a target that modernizes to the card's own headword**, which is the
map *working* — his doublet converged. The tag path drops that remainder, so the
reflex is to drop the arrow too.

`xref2.py` shows why that would be wrong: **24 of the 26 targets head their own
entry.** A tag alternative is this entry's second try and navigates nowhere; a
`crossRef` is a link, and in modern mode the two cards render the *same* headword —
which is precisely when the reader most needs to be told they are two entries.
Collapsing would delete the only thing joining them. So the arrow keeps its link and
its `data-ref`, and prints **his** spelling instead of repeating the headword
(`.xref-his`, italic, muted): `GHAK → G'XAP`, not `GHAK → GHAK`. Pecoraro mode is
untouched — there the arrow already shows his form natively, so the class must not
appear at all.

Two residues, both left alone deliberately. `TQ'NAI → TKNAI` names no entry, so its
arrow is genuinely vacuous — but showing his `TKNAI` still says more than `TQNAY`,
and the link was dead before this too. And `KBIYAN → GBIYAN` still repeats, because
*his* spelling of the target already equals the modern one; nothing in the display can
distinguish two cards whose both spellings coincide.

Verifying this needs the real interaction: **first tap on a crossref-link shows the
gloss preview, a second tap opens the entry** (app.js:1272–1276). A single
`.click()` moves nothing, and reading that as a dead link is a test bug, not a page
bug — `xrefclick2.py` taps twice and lands on the target card for all five sampled
arrows.

