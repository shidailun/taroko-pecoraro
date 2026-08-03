# Pecoraro Taroko — 4-language Truku dictionary

Digitization of Ferdinando Pecoraro MEP's *Essai de dictionnaire taroko-français*
(SECMI, Paris, 1977). Original is Truku (Taroko) → French; we add English +
Traditional Chinese (translated from the French, draft pending native review).

- Live: https://pecoraro-taroko.netlify.app (Netlify project `pecoraro-taroko`, site_id `d6e80a1c-405b-4bf9-8977-3630174261c6`; renamed from `taroko-pecoraro` 2026-07-18)
- Full dictionary: all 398 pages digitized (body + loanwords/animals-plants/names
  appendices), 1967 root entries, 2947 sub-forms, 5438 examples.

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

## Entry data shape (entries.js)

```js
{ hw, tag: "(R)", crossRef?, paradigm?, truncated?, fr, en, zh,
  examples: [{ t, fr, en, zh }],
  subs: [{ form, paradigm?, fr, en, zh, examples: [...] }] }
```

`(R)` = racine/root as marked by Pecoraro; `°` lines = verb paradigm; `§` = example.
Pecoraro's orthography is idiosyncratic (x = today's h, o = u, etc.). Source data
in `entries.js` is never modernized. As of 2026-07-19, the app has a display-only
modern-spelling toggle (⚙ settings sheet) applying three cross-checked character
rules (o→u, l→r, x→h — derived from `Truku_Omnibus.xlsx`, see `tools/orthography/`);
weaker/inconsistent patterns (i→y, q↔k) were deliberately excluded. Don't expand
the rule set without re-deriving from the omnibus corpus.

2026-07-19 word-level modern map: blanket rules corrupt words that are already
valid modern Truku (malu→maru, do→du, lukus→rukus), so conversion is now
word-by-word. `site/modern_map.js` (generated by
`tools/orthography/build_modern_map.py`, 6,730 tokens of which 4,854 actually
change the spelling) maps corpus tokens to
modern spellings; lookup order in `modernize()` is
WORD_OVERRIDES → MODERN_MAP → `charRules()`. Map tiers:
- **id** (1,071) — original spelling already attested in the omnibus; left unchanged
  (also protects loanwords like `lemon` from the char rules). "Unchanged" means
  his capitals and apostrophes, not his diacritics — `norm()` ignores those, so
  the tier used to hand back `däxa` for `däxa`.

  **An identity claim is not a no-op — it blocks `charRules()`.** Where the char
  rules were already going to be right, mapping a token to itself is strictly worse
  than having no entry: it suppresses a correct l→r/o→u/x→h and turns a would-be
  green guess into a brown claim. That makes this tier the one place a *homonym* is
  actively harmful, and `idtrap.py` asks the narrow question it can be wrong about —
  the token still holds an l/o/x, the char-ruled form is attested speech, and the
  char-ruled form's gloss agrees with the entry while the identity's does not. Six
  hits in 1,095 (batch 17): KALAT 天空 was claiming `kalat` 鳳梨 when it is `karat`
  天氣 520× — and his own QALAT 鳳梨 entry was *already* mapped to `kalat`, so the
  map had his q-word and his k-word on the same target; LBAGAN 夏季 was claiming a
  spelling that occurs nowhere in speech against `rbagan` 187×; BILAT 耳朵 was
  claiming `bilat` while its own sub already said `sbirat`.

  **The whole class is measurable, and it is mostly not a defect** (batch 23,
  `idsweep.py`). Of 2,048 identity claims across the map, **1,203 are inert** —
  `crule(k) == k`, so they suppress nothing and are comments in the wrong file, the
  same finding as the four `sl'xq*` nulls. Of the **845 live** ones: 23 are name
  freezes (tier N's business), **279 RIGHT** (the claimed form is attested speech, so
  the block is earning its place), **526 BLIND** (both forms 0×, no evidence either
  way — the claim is a guess but so is the char rule), and **17 WRONG**: claimed form
  0× while the form it blocks IS said.
  **WRONG is a suspicion, not a verdict** — the attested form can be a different word
  that `charRules()` happens to produce. Reading the glosses killed 12 of the 17, and
  two of those would have printed a wrong word in brown: `mlabang` 寬闊的 would have
  become `rabang` 42× 較多, and `mdaling` 近的 would have become `mdaring`, from
  `daring` 呻吟聲. So the sweep's real yield was ~2 of 17, and the ratio is the point:
  a shape-only test over this tier proposes eight wrong changes for every right one.
- **M** (897 of 941 keys) — hand-curated, gloss-verified (`tools/orthography/manual_map.json`).
  Sometimes **his own tag names the modern spelling**: SPU is tagged
  `(SPU" - SPUG) (R)`, and his sub-forms Spgan / Snpgan / Pnspgan / Sspgan all
  keep that g — only Spu, Smpu and Pspu dropped it. Modern `smpug` is 95× in
  speech and `spug` 20×, glossed 數. The bracket in a tag is his own second
  spelling, so when it is the *fuller* one it is direct evidence, not a guess.
  An identity entry here is a verdict ("no modern form found") reached at a
  particular time and may be overturned later: `sueq` → `sueq` became
  `sueq` → `suwiq` once the whole family turned up attested (suwiq 倒掉,
  psuwiq 使倒掉, smuwiq 倒).
  A key here is inert if the token is in `OVERRIDE_KEYS`, because the generator
  skips those (app.js resolves them first, in `WORD_OVERRIDES`) — six `dui`-family
  entries were written and silently ignored before that was noticed. `WORD_OVERRIDES`
  is invisible to the generated map, so the map is never evidence about colour;
  only the DOM is. That cuts both ways, and the second direction cost a batch:
  a scan that reads the map to decide what is still green will offer up words that
  have been brown all along. Eight of the twenty entries in batch 14 were the KLUI
  family, re-derived from the corpus and written down before it turned out that
  `WORD_OVERRIDES` already carried all eight, with the same values. Any tool that
  asks "is this green?" has to consult the whole chain, not the map.

  Systematizing the SPU find: **all 1,850 root tags scanned** for a bracketed
  variant that is a near-shape of the headword (`tagvar.py`) gives 49 pairs, of
  which 11 had a variant the corpus resolves while the headword stayed green.
  That vein produced TUIL (his tag says `(TUWIL ?)`, and `tmtuwil` 專捕鰻魚 /
  `ptuwil` 養鰻魚 / `gmtuwil` 專挑鰻魚 prove the stem — the omnibus even glosses
  bare `tuwil` 人名（男）, which is his own note that it nicknames tall thin young
  men), TMAMuX → `tmeemux` 交配 (modern `mux` is glossed "為「tmeemux 交配」的
  詞根"), SA'GUL → `seegul` 綁住 beside his already-mapped MA'GUL → `mgul`,
  GQANI → `glqani` 拿去出草, and DUX → `dux` (a no-change verdict: `kndux` 厚 6×,
  `mkndux` 厚的 5×, `mkdux` 5× all keep it). The rest of the 11 have variants that
  are only rule output — `tatu`, `psuqih`, `snkrawah`, `bubao`, `klulus` are all
  0-attested — and a rule output is not evidence, so they stay green.

  Two homonym scares in that batch, both checked before acting and both wrong:
  `xili` → `hili` looked like a trap because his XILI is 用手指指人 while `hili`
  is 最小的、老么 — but `hili` has a second sense, 誣賴, carried by `dmhili`
  誣賴的人 and `emphili` 會誣賴, which is exactly pointing the finger at someone.
  And `g'loq` → `gluq` looked wrong because `gluq` is glossed 污垢, until his own
  XG'LOQ 出鞘－拔出 turned out to be modern `hmgluq` 抽;拔. His X'LI 倒入, on the
  other hand, is a *different entry* the shape-scan conflated with XILI, and it
  stays green.

  Batch 15 found two homonyms that were **real**, and both had been sitting in the
  map as confident brown claims. A wrong entry here is worse than green: green says
  "guessed", brown says "verified", and these said the latter about the wrong word.
  His **BETAQ** 刺 was mapped to `bitaq`, which is 直到；連 — and `bitaq` is 321× in
  speech, so the wrong answer was also the best-attested one, which is precisely how
  it survived. 刺 is `beytaq` (spk 6), his METAQ is `meytaq` 注射 (spk 52), and his
  PBETAQ was `pbitaq` 把…劃到 for what is `pbeytaq` 被打針. His own two sentences
  (給你的孩子打針, 把耶穌釘在木頭上) say so plainly. His **MESA** was mapped to
  `msa` 說, but all six of its occurrences are the asking sense (B'SO 無論你去要什麼,
  PESA 我要去乞討食物 / 我來向你要火柴, UMAL 你要求的錢數) — it is `meysa` 要, 82×.
  The lesson is that a shape hit plus high frequency is not evidence; **the gloss of
  the candidate has to match the gloss of the entry it will render in**, and for
  these two nobody had checked. Suffixed forms can still be genuinely shared: his
  `btaqan` 打針, `btaqi`, `bntaqan`, `btaqun` were all already right, because the
  btaq- stem really is common to 刺 and 直到.

  Batch 16 found a third, the same way: **Q'TOL** 肥的－粗的－胖的－肥胖的 was
  mapped to `qtul`, which is 砍 — to chop — and its SQ'TOL to `sqtul` 已砍. The
  word is `qthur` 肥胖 (spk 45), `qqthur` 很肥胖, `mqthur`, `pqthur` 讓…粗（胖）.
  Three of these in two batches, all long-standing, is enough to call it a class
  rather than an accident, and none was found by looking for it — they turned up
  while working the green tail nearby. `claimaudit.py` is the systematic version:
  for every brown claim whose asserted word has a gloss, flag it when that gloss
  shares nothing with the entry's **and** some other attested near-shape does.
  Condition two is what makes it usable — `meytaq` 注射 against an entry glossed
  刺 shares no character and is still right, so "no overlap" alone flags hundreds
  of good entries; it was the existence of `beytaq` 刺 that made `bitaq` 直到 stand
  out.

  Batch 15 closed the **teetu** family, where the map was contradicting
  itself: `st'to`/`sta'to` → `steetu` and `knta'to` → `knteetu` (the long vowel)
  sat beside `ta'to` → `tatu`, `tma'to` → `tmatu` and `knt'to` → `knttu`, all three
  0-attested. Modern has `teetu` 切豬;切菜;切斷藤, `tmeetu` 切、剁 (spk 5) for his
  TMA'TO, `pteetu` 立碑 for his PT"TO 豎立, `knteetu` 一直 for his KNTA'TO
  不停地－頻繁地 — the same long-vowel correspondence as SA'GUL → `seegul`. **When
  one branch of a family is already spelled a way the others are not, the
  disagreement is the finding**; a family should never carry two stems.

  Batch 16 got its other two families from the inverse of that: one slot already
  right while the rest of the family sat green. **DLMUT** 熱忱－熱心－勤奮 was green
  in every slot except `kndlmutan` → `kndrmtan` 勤勞, so the answer was already in
  the map — the root is `drumut` with the u syncopated, and `mdrumut` 很勤勞 is
  **137×** in speech, `kdrumut` 30×. **K'KAX** 踩－踐踏 was green in all eight slots
  with only `knkaxan` mapped, to `knqahan` — right except for a dropped l. Modern is
  `qlqah` 踏, and the paradigm lines up slot for slot (`qmlqah` 8×, `qlqahan` 3×,
  `qlqahi` 2×). His k→q and x→h are ordinary; what is new is that **the elision mark
  in `k'kax` is standing for the l** of `qlqah`, not for a vowel — the first case of
  `'` covering a consonant rather than a syncopated vowel. A single already-mapped
  slot in an otherwise green family is therefore worth checking before any corpus
  search: it is either the answer or, as with `knqahan`, one letter from it.

  Batch 17 pushed that to its limit with **LAWAX** 打開－釋放, where *twelve* derived
  slots were already mapped with modern r — `rmawah`, `rwahi`, `rwahan`, `rwahun`,
  `mrawah`, `prawah`, `mprawah`, `wahan`, `wahi` — and the **headword** was still
  claiming `lawax`, which is 瘦. `rawah` 打開蓋子 20×. Three siblings were wrong the
  same way: `llawax` claimed `lrawah`, a cluster Truku does not have, where his Ll-
  is modern rr- by his own MLLAWA→`mrrawa` and PLLAWA→`prrawa`; `tlawax` and
  `mptlawax` were 0-attested identities keeping an x the rest of the family drops.
  Fixing `llawax` made the projection tier hand back `pllawax` → `prrawah` on its
  own, which is the tier working as designed. IYAX was the same shape: the whole 來
  family takes h (`miyah`, `yahi`, `yahan`, `yahun`, `nyahan`, `smiyah`) but
  `p'iyax`/`mp'iyax` kept the x beside their own attested `pyahi`/`pyahan`/`pyahun`.
  So the check is not "does the family disagree with itself" but **which member is
  outnumbered** — and the headword carries no extra authority, because it is the
  slot most likely to be a bare root that happens to collide with another word.

  **The one defect the map SHAPE cannot express.** `modernize()` takes a bare token
  (app.js:105, and the comment at :160 says as much); there is no per-entry hook,
  not even in WORD_OVERRIDES. So when two entries share a headword and want
  different modern words, one of them must render wrong. Two instances: IYAX is
  `iyah` 來 179× in one entry and `iyax` 間隙 115× in the other; LAWA is `rawa` 背簍
  44× in one and the calling stem `lawa` in another — proven by `mlawa` 打；招呼 79×,
  `plawa` 呼叫 9×, `splawa` 呼叫 16×, not by the bare 14× in speech, which is the
  woman's name. Both keep the identity, because it is a *true* claim for one entry
  of each pair; blocking them to green would only move the wrongness and lose a
  correct reading as well. Do not re-litigate these two without changing the lookup
  signature first. Batch 18 found a third and a fourth: **NGALI** is `ngari` 剩餘 31×
  as a headword but `ngali` 拿! in ANGAL's imperative and three example sentences, and
  **ULAE** is two entries, `ulay` 溫泉 4× and `uray` 餓 10×. Both keep the reading that
  serves more slots, which for ULAE means the hot-spring card now displays URAY.

  **Ask the LAWAX question mechanically: which families argue with themselves?**
  `famsplit.py` walks every entry's owned forms and, per char rule, partitions them
  into the ones whose value took the modern letter and the ones whose value kept his —
  95 families split, 85 with a minority of ≤4, which `famsplit2.py` then rebuilds the
  majority's way and prices against speech. That is the batch-18 vein, and it is the
  largest single one so far. Its own false positive is documented in the script: a
  word with two l's where only one folds (T'LO's `mt'lol` → `mtrul` 32× 三十 is right).
  Twice the **minority was the correct side, and the gloss said so** — APIX 壓 had four
  h-forms outvoting three x-forms, but `apih` is 扁嘴 with zero speech while `pixan`
  用…壓住 is 3×; PXAAL 用扁擔挑運 had four `phr-` forms, all glossed 氣喘 (asthma), against
  `mhaal` 扛 8×. So the majority is only a tie-breaker: **the member whose gloss
  matches the entry wins however few of them there are.**

  **The mirror image, and the bigger vein: the green straggler.** `famsplit.py` only
  compared *mapped* forms, so it was blind to the case that matters more. A green form
  is not silent — it is rendered through `charRules()`, which applies l→r, x→h and o→u
  unconditionally. So in any family whose mapped members **decline** a rule, every
  green member containing that letter is displayed with the correction the family has
  already rejected, and *there is no way to say "leave this letter alone" except to
  make the claim.* `famgreen.py` asks exactly that and finds **51 families** —
  BALAE (`balay` 1219×, nineteen l-keeping members, and KNSBLAYAN rendering
  KNSBRAYAN), MALU 好 568×, KLAWA 356×, MAXAL 十 348×, SILING 詢問 252×, TALANG 跑 154×,
  XEULING 狗 398×. Its proposal is not invention: modernize with every *other* rule and
  leave the disputed letter, which is what the family's own adjudicated members say.
  Note a token hit on two rules (`pnnaxal`, where MAXAL declines both l→r and x→h)
  needs the per-rule proposals intersected, not applied one at a time.

  **PXAAL: search the syncopated shape, not only the full one.** I blocked its four
  suffixed slots as unchoosable — `phaali`, `phali`, `phalan`, `phalun`, `haalan`,
  `phaalan` are all 0, the `ttuun` situation — and unblocked them in the same batch
  when `famgreen.py`, run for a different reason, printed `phlun` **4×**; `phlan` is in
  an omnibus sentence as well ("Btakan o snalu djima phlan qsiya" = 竹筒是打水用, the
  carrying-instrument sense of his own P'XLAN slot). The two questions were one
  question: the stem is `haal`, so **`mhaal`'s final letter IS the root l** — which
  syncopation and whether the l survives have a single answer, and it was inside the
  8× attestation I had already read as evidence about the stem alone. `phli`, `phlan`,
  `phlun`, `phlaan`: x is h, the elision mark is the syncopated a, the l is a root
  consonant l→r must not touch.

  **Batch 19 applied the green straggler in breadth: 112 proposals over 48 families,
  98 accepted.** The strong end decides it on real data (BALAE 1219×, MALU 568×,
  XEULING 398×, KLAWA 356×, MAXAL 348×, SILING 252×, TALANG 154×, and two proposals
  attested outright — `slhbnan` 1×, `lwaqun` 9×); the weak end (SB'LÖS, SWIWIL,
  BTULUK, DLUT, TG'LA, L'LU, XG'LYEQ, M'LUX, SNUGUL) decides it on internal
  consistency alone, every member 0×. That is a thinner claim than usual, and worth
  stating plainly: **the alternative to a thin claim here is not "no claim", it is the
  green rendering, and that one is positively contradicted by the family.** Four
  families were *better* than the tool's proposal, and each is a pattern already in
  this file rather than a one-off:

  - **GALUP 連接 — the entry proves it itself.** Two of its slots are written twice
    under the *same* gloss, once with p and once with k: 使結合 has both `Pgalup` and
    `pgaluk`, 作為橋樑的人 has both `Mpgaluk` and `mpgalup`. Every k-form is attested
    (`galuk` 衣扣, `gmaluk` 接續, `mgaluk` 要連接), every p-form is 0. This is XOLIT's
    t/d doublet again with p/k — but here the doubling is **inside one entry under one
    gloss, which is proof rather than inference**. Six forms took k, not a keep-l
    identity, and the keep-l identity would have claimed a word that does not exist.
  - **XDIYAL / TDIYAL — check for a letter no char rule reaches.** The family also
    folds d→j, so the keep-l proposal would still have rendered HDYALAN and TDYALAN.
    `hjyalan` 找到了 and `hjyali` 找到 are in the omnibus; the TDIYAL forms are all 0,
    but his own already-mapped `tnjyalan` 4× proves the syncopated `tjyal-` shape with
    the j. Same lesson as LADING → `rajing` (l→r *plus* d→j) in batch 18: a keep-letter
    identity is only right if every *other* difference is a char rule.
  - **DAOLYAQ 眼睛 `pdlyeqon` — a char-rule verdict is positional.** The family
    declines o→u because `dowriq` 264× keeps the o **of its root**; `pdlyeqon`'s o is
    in the **suffix** `-on`, where his -on = modern -un is systematic. A family-level
    verdict cannot be carried to a letter in a different morpheme. Left green, where
    it renders PDRYEQUN with the suffix right. Same class as T'LO's two-l false
    positive.
  - **K'LAE 硬的－昂貴的 — a fifth per-token conflict, and the family wants the rule.**
    Modern 硬/貴 is `mkray` 40×, *with* r, so the green PKRAY is already correct and
    the proposal was reading the neighbouring K'LA 知道 family's evidence. `k'lae` is
    both K'LAE's headword and a sub of K'LA, and `occ.py` shows eleven of its twelve
    occurrences are "ini mo k'lae" = 我不知道 — the twelfth being the K'LAE headword
    itself. As with ULAE and NGALI: **the headword is the slot that loses.**

  Also dropped: KLUULUS (2/1 is too thin, both members 0, and his own note calls it a
  reduplication of ULUS whose reflex `murus` takes r), and `tnblxan`, where **the
  author flags the root himself** — BALAX's gloss reads
  "（詞根＝BALAX 新近的、新的？－BULAX？＝新的？－BOLOX＝分離？）". Keeping the x follows
  BOLOX's `burux` 單獨; the 長子／新生兒 senses fit BALAX 新 → `barah`, which takes h.
  When he writes the uncertainty into the entry, that is the `ttuun` situation stated
  out loud — leave it green rather than pick a side he would not.

  `dom19.py` is generated *from the batch data* rather than hand-written, because 98
  changes cannot be transcribed into assertions without miscopying one, and a
  miscopied expectation is the failure that teaches nothing. Both of its initial
  failures were bad expectations in the test: it computed a card's modern headword as
  `MAP[hw] or charRules(hw)`, which is wrong for a **bracketed** headword
  (`M'LUX (M'LUç)` — `modernize()` takes a bare token, and the JS comparison keeps
  only the first word) and wrong for any headword living in **`WORD_OVERRIDES`**,
  which is invisible to `modern_map.js` — `klui` renders `kluwi`, not the char-rule
  `krui`. Any tool that computes what the page will show has to merge WORD_OVERRIDES
  in, exactly as `respellable()` does.

  **Batch 20 — his doubled initial consonant is a SYNCOPATED REDUPLICATION, and
  batch 18 read it as a letter.** Batch 18 mapped `lludan` (his plural of LUDAN 長者)
  to `rrudan` by applying l→r to both letters, and `llodoç` to `rrudux`. Both targets
  occur **0×** anywhere. The defect is not the letter, it is the morphology: modern
  Truku writes the plural/distributive as a copy of the root's first syllable **minus
  its vowel**, so 老人們 is `rdrudan` 68×. His convention is to double the initial
  instead — same word, same morphology, a different orthographic convention, which is
  respelling and belongs in the map. The vein is the most basic vocabulary in the
  book: `llaqe`→`lqlaqi` 210× 孩子們, `lludan`→`rdrudan` 68×, `ssamat`→`smsamat` 41×,
  `kkoyox`→`kykuyuh` 36× 女性們, `llutut`→`ltlutut` 28× 親戚們, `ssik`→`sksik` 18× 掃把,
  `pparo`→`prparu` 16×, `ggaya`→`gygaya` 12× 各個法律, and 15 more.

  Five of the 24 are **already in the map under another of his own spellings of the
  same slot** — the strongest form this evidence takes, since he wrote the slot twice
  and only one spelling was ever adjudicated: `lqlaqe`→`lqlaqi`, `ldludan`→`rdrudan`,
  `pkpakao`→`pkpakaw`, `mlmilit`→`mrmirit`, `qxqaxol`→`qhqahur`. His own labels say the
  two spellings are one slot — `Lqlaqe (vl. llaqe)`, `Lludan (vl. Ldludan)`,
  `Pkpakao (ppakao)`, `Kkoyox (var. Kikoyox)` — which is also how `kikoyox` came in.
  The 0× targets are not on air either: each has an omnibus gloss that his own example
  sentence confirms. `bbagun` is "Malu bi bbagun ka btakan so" 你的大竹子很容易劈開 and
  `bgbagun` is 剝開; `llubwi` is 玉米袋／紙袋 and `lblubuy` is 布袋; `ppotox` is
  橋樑都損壞了 and `ptputuh` is 斷了.

  **Two restrictions matter more than the fixes.**
  - **A doubled initial is not always a reduplication.** mm-, pp-, tt-, ss- are live
    modern *prefixes* — `mmiyah` 即將到來 is prospective, `ppais` "for the enemy" — so
    the syncopated shape has to be **attested** before this says anything at all.
    `redup3.py` asks the corpus for any attested word ending in the root instead of
    generating a shape, and the other 81 doubled values have **no** reduplication:
    there the answer is silence. And the bare root is never the fallback — `ssapax`
    房子全都 is not `sapah`, one house.
  - **Modern marks the human plural with `d-`**: `dseejiq` 288× 人們, `dsnaw` 53×. So
    his `sseejiq` and `ssnaw` stay as they are. Swapping his reduplication for a
    different *morpheme* is lexical substitution, not respelling. (`snsnaw` 2× exists
    but is glossed 為男人爭, a verb — not the plural.)

  Rejected with the reason kept: `ppongo` (his "nouer" against the perfective
  `pnpungu` 做繩結) and `ssapat` (his "débauche intense" against `spsapat` 撕裂而堆積).

  **The propagation is where this batch nearly broke something, and it is the same
  restriction one level down.** `ssik`→`sksik` correctly pulled `mssik`, `ssikan`,
  `ssikun`, `sssik` through the projection tier — `msksik` 4× and `ssksik` 掃地的工具,
  which is *his own gloss for `sssik`*, both attested. But it also pulled
  **`Skkoyox` 亡妻 → `skykuyuh`**, and that is wrong: there the doubled k is `sk-`
  'the late' meeting a k-initial root (`skbaki` 過逝的岳父 is the same shape), it is
  singular, and it was being handed KOYOX's plural. Pinned to `skkuyuh` / `nskkuyuh`.
  **A tier that carries a corrected head into its relatives carries the correction's
  scope with it — check the relatives for the case the restriction was written for.**

  `dom20.py` is generated from the **map diff** rather than from the proposal file,
  which is what caught it: 34 keys applied but 39 moved. It also fixed a coverage hole
  `dom19.py` had — `own` scanned only form/paradigm slots, but most of these plurals
  live in his **example sentences**, which are modernized identically. Adding
  `examples[].t` took the check from 19 cards to 77 (92 brown, 83 banned-form
  assertions, 0 failures). 27 of the 39 are corrections of an *earlier claim*, so the
  banned form is not a char-rule rendering but a wrong brown word this file previously
  shipped — `rrudan`, `rrudux`, `hhuling`. Those bans are the batch.

  **Batch 21 — the name tier, seeded from the tag we already wrote (2026-07-30).**
  75 map changes from two edits, both described under tiers L and N below: eight
  `llm_map` values that had matched a name onto a real word were dropped, and tier N
  is now seeded from `name (m)`/`name (f)` rather than from capitalisation
  statistics (76 → 143 names). `dom21.py` verifies from the map diff as dom20 does,
  and adds the assertions the change could have *broken* rather than only the ones
  it makes: KULAS must still render KURAS and LABAI RABAY (tier S, attested 24× and
  42× — the freeze must not outrank attestation), and QAYO must still render KAYU
  (that llm value was right, and the name sharing the token cannot win). 101 cards,
  102 brown, 55 banned-form assertions, 0 failures. Almost every banned form here is
  a char-rule rendering rather than a previous brown claim, because these names were
  **green** — the page was displaying guesses at men's names.

  This started from `ndiyan`, the one `null` in `lexical_map.json` with no note. It
  is the n- possessive of the `name (m)` DIYAN, not of the common noun 白天 →
  `jiyan` 44×, making it the sixth per-token conflict (after IYAX, LAWA, NGALI,
  ULAE, K'LAE) and the first resolved at a *derived* form. Auditing the other eight
  nulls by measurement — delete all nine, regenerate, diff — showed only five
  suppress anything at all (`biri`, `ndiyan`, `stbako`, `ttuon`, `ttuun`); **the
  four `sl'xq*` blocks are inert.** A block that suppresses nothing is not a
  decision, it is a comment in the wrong file.

  **Batch 22 — `vl.` is *vel*, and only some of the time is it a spelling
  (2026-07-30).** His own tooltip glosses the abbreviation `vl|vel — ou / or`, so it
  announces an *alternative* and nothing more. Which kind of alternative depends
  entirely on the slot it sits in, and that is what decides whether the pair is
  evidence:

  - in a **form** slot (headword, sub-form, paradigm, tag) it is reliably one slot
    written twice — `Tklean (vl.Tkliyan)`, `BOLONG (vr. KBOLONG)` — so the two sides
    are two spellings of one word and each side's map value is a claim about the
    other;
  - in an **example** it labels an alternative *phrasing*: `Uxai ko mb'so (vl. uxai
    ko ka mb'so)` differs by a particle, not a letter. Worse, even at one token per
    side it can pair two different WORDS — M'LUX's `Ini ! (vl. Adi !)` puts `ini`
    2617× beside `adi`→`aji` 1323×, two words for "not". So an example-position pair
    is admissible only when the two sides share a consonant skeleton.

  `vlpair2.py` reads every slot with the head taken positionally (the last token
  before the labelled bracket, the field's own head when the bracket opens it).
  Result: 36 pairs, and **52 of the 66 example-position labels dropped as wording
  rather than spelling** — the vein is far thinner than it looks, and without the
  skeleton gate the sweep proposes `ka` (26,777×) and `da` (3,834×) as headwords and
  calls every clause variant a conflict. The productive class is the **12
  tag-position labels**, which vlpair.py had reported as "(unparsed)" because in a
  tag the label *is* the whole field and there is nothing to its left. The method
  checks itself on `BUKOX (vr. BOQOX)`, where both members already map to `bukuh`.

  Six keys changed, and the largest was a family contradicting itself: `kbolong`,
  `qbolong`, `kmbolong` and `mkbolong` all resolved on **`burung`** — with r — while
  `bolong` claimed *itself* and `mbolong` claimed `mbulung`, both keeping the l. An
  identity claim blocks charRules, so `bolong` was the idtrap pattern at 0×
  attestation, and the omnibus settles the root outright: `qburung` 收割, `qmburung`,
  `qbrungun`, `qnbrungan`. Also `bwixol` `bwihur` (0×) → `bgihur` (211×), his own
  `(vr.BGIXOL)`; `kbiyan`/`skbiyan`, where KBIYAN's entry is nothing but a
  cross-reference — 「＝GBIYAN之變體＝傍晚－晚間。見GBIYAN」 — and `gbiyan` is 115×
  against `kbiyan` 0×; and `dxeyaq` → `thiyaq`, the labelled twin of `d'xyaq` 43×.
  `dom22.py` asserts the six plus the seven neighbours the fix could have dragged off
  their root: 21 cards, 25 brown, 10 banned-form, 0 failures.

  Seven rejected, because **a label is not an argument**: DIMA/DDIMA (`jima` 71× and
  `djima` 179× are both attested — d- is the collective, two forms not two
  spellings), KLAWAI/TLAWAI (54× and 28×, both real), BU/SBU (his own note says BU
  never appears in this form), GNAMA/NAMA (g- prefix), GILA/TGILA (耽擱、逗留 vs 酵母
  — unrelated, and his "(=TGILA 之詞根?)" is his own doubt), G'LEQ/LEQE (轉動 vs 歪的,
  both 0×, his tag a chain of question marks).

  **Batch 23 — the idtrap sweep: 17 suspects, 12 killed by the dictionary
  (2026-07-30).** The census is in the **id** tier above; what matters for method is
  how the 17 WRONG candidates were settled, because 12 of them were rejected and two
  of the rejections were saves. Two kinds of evidence did all the work, and neither is
  the shape of the word:

  - **the family.** LAMU, LAWA and SALU keep their l with heavy attestation —
    `lmamu` 29×, `mlawa` 79× / `lawa` 14×, `smalu` 44× / `smlaan` 30× — so `lmuan`,
    `plwaan` and `slui` at 0× are RIGHT claims and the 1× r-forms beside them are
    other words. `mkalang` belongs to `alang` 部落 1052×. This is the same test that
    convicted `bolong`, run in the other direction: a family that already agrees is
    evidence either way.
  - **the gloss, searched from the meaning.** `idcheck.py` takes his Chinese and asks
    the omnibus which modern word carries it, rather than deciding a letter and hoping
    a word exists. 寬闊 came back `garang` with a whole paradigm (`garang` 河川寬闊,
    `mggarang` 像…寬闊的一樣, `sggarang` 沿著寬闊, `kgarang`, `sknegarang`,
    `tmnegarang`) — which **confirmed GALANG and killed MLABANG in the same query**,
    because `labang` 3× is itself glossed 寬 while `rabang` 42× is 較多. 癢 came back
    as the root `krak` (`mrkrak` 8×, `mkrak` 6×), so nothing shaped q?aq glosses it
    and `qraq` 2× is some other word; 近 came back `dalih` 45× with no `mdalih` at
    all, so MDALING has nowhere to move and `mdaring` belongs to `daring` 呻吟聲.

  **GALANG is the batch: nine of the ten keys.** His 延展——蔓延——氾濫 is `garang`, and
  the family had already committed to r five times (`gmarang` 22×, `mkgarang` 14×,
  `ggarang`, `mpgarang`, `pgarang`) while eight members claimed themselves at 0× —
  `bolong` again, a head keeping its letters against its own relatives. The
  complication is a **genuine l homophone, "make an implement"**: `glangan` 做了樹梯,
  `glangi` 做箭尾鉤, `glangun` 做刀銷, `glngani` 幫…做鉤, `mgalang` 種植. So every slot
  was decided on its own gloss, not on the root — and that is what settled the one
  slot with attestation on the l side: his **Mgalang 蔓延的——散開的——攤開的** is
  `mgarang` 9× 要耙開日曬的 (raked out to sun-dry), not `mgalang` 2× 種植. 耙開 "rake
  apart" is the verb of his 散布——分散 throughout, so `grangi` 4×, `grangun` 2×,
  `grangan` 1×, `grngani`. `pglangi`/`pglangan`/`pglangun` are 0× on both sides and
  were taken on paradigm regularity alone: `pgalang` → `pgarang` was already mapped,
  so leaving the imperatives on l would have made one sub-form contradict its own
  head — the half-brown card. Tenth key: **`pulut` → `purut`** 16× 山麻雀（飛禽名） for
  his 雀鳥（燕雀類小鳥）, where the l form `pulut` is 陰蒂, unrelated and unattested.

  **Batch 24 — the mirror sweep, and his elision mark as a defeater (2026-07-30).**
  An identity claim only *withholds* a fix; a mapping is worse when it is wrong,
  because it changes what the reader sees. `revsweep.py` ran the idtrap test in the
  other direction — a non-identity mapping whose key is attested speech but whose
  value is 0× — and **the map is healthy: 36 of 4,681, or 0.8%**, nearly all stray
  o→u / ai→ay corpus tokens. `spoken_truku.json` is a corpus of *modern* texts, so a
  token in it is by definition current spelling, which is what makes that test sharp.

  Three of the 36 were real **homographs printing a different word in brown**:
  `pspui` (his 使…煮 against `pspi` 使…做夢), `lqloq` 墨 (against `rqruq` 沙啞聲), and
  the TLOONG suffixed forms (against `tlngun` 摸). TLOONG also has an **ablaut split**
  that has to be respected slot by slot: -an/-un take the long stem (`tleengan` 93×,
  and the omnibus has `ptleengan` 使坐), while -i keeps the short one (`tlngi` 3×,
  `ptlngi` 2×). `klangan` was deliberately **not** retargeted to `tleengan` — the
  consonant skeleton differs (k vs t), so respelling it `qlangan` preserves his
  variant where substituting would erase it, the `_sogi` failure mode.
  **QALO is a seventh per-token conflict**: 梳子 wants `kalu` and 豬油 wants `qalu`
  食油 5×, and MODERN_MAP is token-keyed so only one can be served. The comb entry is
  explicitly a pointer (`參見 KALO`, and `kalo` → `kalu` already), so the token went to
  `qalu` and the comb sense reaches its spelling through its own crossRef.

  **The DOM check found a defect the map could not see.** LQLOQ still printed RQRUQ
  after `lqloq` was mapped, because `tkey()` **keeps the apostrophe** — his tag spells
  it `Lq'loq`, which is a different key. `markvar.py` swept the class: **9 mark-bearing
  tokens disagree with their mark-free twin**, and the mark is not automatically noise
  — **four of the nine are deliberate**, the mark being the only thing separating two
  words (`k'lae` 了解 / `klae` 硬·昂貴; `wa'lo` `walu` 28× 蜜蜂 / `walo` `waru` 脖子;
  `p'alex` ALEX 使人厭煩 / `palex` `parih` 43× 小鋤頭; `ta'to` `teetu` 切菜 / TATO, a
  personal name with no gloss at all). The other four were fixed, one of them running
  the **opposite** way — bare `qtol` was the wrong twin: DUDUX reads
  「Kingal pusu qouni o, qtol ka pusu」一棵樹，底部粗大, which is `qthur` 45× 肥胖 and
  not `qtul` 1× 砍, and the whole Q'TOL family was already on `qthur`.

  Method note: **the "gone" assertion in the DOM checks was too crude.** It banned a
  string from the whole card, but QALO carries `crossRef: "KALO"`, so KALU on that card
  is the pointer working, not a stale value. `dom24c.py` now subtracts everything the
  card's own tokens legitimately render to before banning anything — 76 cards,
  103 brown, 90 banned-form, 0 failures.

  **Batch 25 — the `lyeq` vein: three half-brown cards (2026-07-30).** His `<lyeq>`
  transcribes what the modern orthography writes **-liq-** (or **-riq-** where the
  liquid is his l-for-r), and the map had **already applied that correspondence in 14
  keys** — `xglyeqan`→`hgliqan`, `slyeqan`→`sliqan` 14×, `mblyeqan`→`mbliqan`,
  `qndlyeqan`→`qndriqan` 4×, `galyeq`→`galiq` 46× 布料. What was left was a 17-key
  residue plus a green tail, arranged as **three half-brown cards**: the GALANG defect
  again, a head keeping its letters while its own relatives had moved.

  The class evidence is one-sided in a way that is worth recording, because it is what
  licenses the blind slots: **of ~70 candidate forms, not one spelling containing
  `lyeq` is attested anywhere** — 0× in speech and absent from the omnibus — while the
  liq/riq twin is attested wherever there is a witness at all. A blind slot here is not
  a coin flip; it moves from a spelling that is definitely not modern to one that is at
  least well formed.

  - **S'LYEQ 浪費；違犯；揮霍 → `seeliq`** is the headline, and it came from searching
    the omnibus by his gloss. His **Sm'lyeq 浪費；濫用；違犯** is `smeeliq` **67× 浪費**,
    an exact match — and it was pointing at `smliq` 2× 破壞, a real but far rarer word.
    The family carries the **same long/short ablaut as TLOONG**: `seeliq` 7× 破壞 and
    `smeeliq` 67× take the long stem, `sliqan` 14×, `sliqi` 3× and `snliqan` 2× 破壞的
    the short one, so bare forms and suffixed forms had to be mapped differently.
  - **XG'LYEQ 撕裂（用於布、紙、樹皮…）→ `hgliq`**, whose whole paradigm is in the
    dictionary: `hgliq` 3×, `hmgliq` 3× 撕開, `hgliqi` 2× 撕開, `mhgliq` 裂開,
    `hgliqan` 撕裂了, `hgliqun` 要…撕裂, `hnegliq` 撕裂的, `thhgliq` 同時都撕開. Two
    slots were decided against each other on the same principle: `txg'lyeq` → `thgliq`
    keeps his skeleton rather than taking the geminate `thhgliq`, while `xnglyeq` →
    `hnegliq` **does** take the dictionary form, because there the only difference is
    the schwa his transcription never writes (h-n-g-l is unpronounceable as it stands).
  - **BLAEQ 享受——幸福** was already right in its *ae* half — `msblaiq` 41× 祝福；福氣,
    `smblaiq` 38×, `tblaiq` 12× 很享受, `psblaiq` 11×, `sblaiq` 4× 因…幸福 — and the
    **ae class as a whole is clean, 0 defects in 64 keys**. Only its five `blyeq` slots
    were stranded, and the syncopated stem they need is attested (`psbliqan` 2×,
    `sbliqi` 6× 幸福).
  - **QDOLYAQ 逃跑** (`qduriq` 52×) and **DAOLYAQ 眼睛** (`dowriq` 264×) were green
    tails rather than defects, but the same syncope: `pqdriqi` 2× and `pqdriqun` 1× are
    attested, and `qndlyeqan`→`qndriqan` 4× was already in the map, which is what
    licenses the DAOLYAQ parallels at 0×.

  Left green on purpose: **`x'lyeq`** (X'LYEQ 撕裂的——撕碎的, 參見 XG'LYEQ 意義相同 — but
  his form has no g, and modern has only `hgliq`, so mapping it would substitute a
  different word for his variant, the `klangan`/`_sogi` decision again); `gn'lyeq`, for
  which no gn- form of the root is attested either way; and `g'lyeq` / `lyeq`, which are
  root citations inside a `(R. = …)` tag rather than words. `gmalyeq` → `gmaliq` 5×
  出草（殺人）was left as it stands: his GMALYEQ has no gloss at all (「詞根不明」), so the
  shape is all there is, and `galyeq`→`galiq` proves the correspondence for that root.
  32 keys; `dom25.py` 75 cards, 129 brown, 129 banned-form, 0 failures.

  **Batch 26 — generalize the `lyeq` find into a test, and it returns the biggest defect
  in the book (2026-07-30).** `lyeq` was not a wrong word, it was a **letter sequence the
  orthography never writes**, and that is mechanically detectable without knowing any
  Truku: build the character n-gram inventory of the whole modern lexicon (38,687 types,
  2/3/4-grams, word-boundary aware with `^`/`$`), then flag every map VALUE containing an
  n-gram that occurs **nowhere** in it. `seqsweep.py` returns **1,172 values in 739
  distinct sequences**, grouped by the offending sequence so the output is classes rather
  than singletons. An impossible n-gram is far stronger evidence than an unattested word:
  a word can be 0× because it is rare, but a trigram 0× across 38,687 types is 0× because
  the orthography forbids it.

  Its largest class is **`^mp`, and it is a prefix spelling**. Modern writes the
  future/agentive as `emp-` — **1,651 types / 2,251 spoken tokens** — against `mp-` at
  **8 types / 13 tokens**, so the map was printing ~100 brown forms beginning with a
  cluster that occurs 13 times in 277k tokens of speech. The affected words are the most
  basic vocabulary in the book: 老師 `emptgsa`, 二十 `empusal`, 七 `empitu`, 讀書
  `empatas`, 洗 `embahu`, 煮 `empshada`. It is the same finding as batch 25 one morpheme
  further out — his transcription does not write the schwa, word-internally *or*
  word-initially.

  **Three decisions define the scope, and each was made against my first instinct.**

  - **Not a general rule.** The per-token guard ("value 0×, `e`+value attested") is
    initial-agnostic and looks equally safe anywhere, so `eprefix.py` measured what a
    general rule would catch: **144 fires**, and the non-`mp` remainder is unsafe —
    `glani` → *eglani* (a word batch 24 had just settled), `duk` → *eduk* 門扇, `lixan`
    → *erihan*, singleton initials where the e-form is a coincidental different word.
    That is exactly the blanket rule this file warns about, arriving disguised as a guard.
  - **It stops at the labials, and that is phonology rather than luck.** `mbcheck.py`
    priced every m-initial: `emn` **0** types against `mn` 1,215, `ems` **0** against
    1,096, `emk` 5 against 920, `emg` 1 against 667, `emt` 15 against 520. The written
    schwa appears only before **p** and **b** — where the cluster needs breaking — which
    is why `mb-` (201 types / 1,011 tokens against 8 / 9) belongs in the same pass even
    though it is a **different morpheme** (stative m- on a b-root, `m`+`biyax`) and does
    not inherit the `mp-` argument. It had to be measured separately to be admitted.
  - **Not `manual_map.json`.** Freezing 140 stems by hand would silently override any
    *future* stem fix — precisely what batch 25 had just done for `lyeq`. A generator
    post-pass composes instead: it rewrites whatever the stem tiers produce, so a later
    correction to the stem still lands. Hooked in after the tier-V twin pass, which is
    why the tier's 140 are drawn **from** other tiers (P 99, T 15, R 14, M 6, E 4, G 1,
    V 1) rather than added to the map — mapped stays 6,733 while *changing* goes
    4,697 → 4,732.

  **The guard is deliberately more conservative than the class.** Attested is attested,
  the id-tier principle: `mpgeeguy` 偷竊者, `mpplaq` and `mputuh` 斷掉 stay, and so does
  `mblaiq` at 5× even though `emblaiq` is 43×. 57 of the 140 fired on the omnibus alone
  with 0 spoken support, and every one has a gloss confirming the reading (`embukaw`
  駝背, `empdanga` 要照顧, `empsinaw` 釀酒的人). Two values keep an **x** — `empxal` 再一次
  8× and `emptgxal` 要做伙伴 — which is not a defect: modern Truku writes x in 793 spoken
  types (`jiyax` 749×, `dxgal` 662×, `maxal` 348×), so x→h is a *word-by-word* question,
  never a blanket one.

  `dom26.py` derives its assertions from the map diff, and its load-bearing half is the
  set the tier must **not** have touched — every value still beginning `mp-`/`mb-` after
  the run, asserted unchanged on its own card. If the guard were reading the class
  instead of the token, those are the words that would have moved. 334 cards, 426 brown,
  326 banned-form, **0 failures**.

  **The green count, measured from the DOM for the first time (`greendom.py`).** The map
  cannot answer this question — `WORD_OVERRIDES` lives in `app.js` and is invisible to
  it, and `metaAbbr`/`FORM_PROSE` grey words before `respellable()` is ever asked — so
  the count comes from walking all 24 letters of the A–Z listing in modern mode, where
  every root renders as a full card, and counting the spans the page actually painted.
  Across **5,094 cards**: **49,558 brown / 1,504 green occurrences (97.1%)** and
  **9,806 brown / 862 green types (91.9%)**. The tail is now genuinely flat — the
  commonest green word on the entire site occurs **19** times, and nothing exceeds 20.
  Four of the top fifty (`de`, `cuntractiun`, `ra`, `I`) are not Truku at all: French
  residue and the `contraction :=` parse bug, which are data repairs rather than
  spelling work.

  **Batch 27 — the blind half of the same vein (2026-07-30).** Batch 26's guard skipped
  every `mp-`/`mb-` value with no attested `emp-`/`emb-` twin, so re-running `seqsweep.py`
  after it still flagged `^mpa` (20), `^mpk` (20) and `^mpt` (10) — 164 values where
  neither spelling has a witness. A blind slot is the batch-25 case: the choice is not
  between a right answer and a wrong one but between a form that is **definitely not
  modern** and one that at least could be. Two measurements settle it.

  - **The class is all but exceptionless.** Of the 8 `mp-`-initial types in all 38,687
    modern types, **7 also have an `emp-` twin**; the one that does not is `mpotoh` 2×,
    unglossed. Writing `mp-` word-initially is, in modern Truku, essentially not done.
  - **The one real ambiguity does not arise.** `mp` is two things: the prefix `emp-` with
    the schwa unwritten, *or* plain m- on a **p-initial root** (`mputuh` 斷掉 = m+`putuh`),
    where modern really does write `mp-` and there is no schwa to add. `mpblind2.py` asked
    the corpus which reading each of the 149 blind values takes — strip `mp` and test the
    stem, versus strip only `m` and test the p-initial remainder. **100 leave a directly
    attested stem** (`nanak` 600×, `iya` 572×, `piya` 515×, `baki` 488×) and **0** take the
    m-on-a-p-root reading. The shape explains why: that reading needs a VOWEL after `mp`,
    and these are overwhelmingly `mp`+consonant.

  For the 49 with no witness on either reading, `mpblind3.py` asked a weaker question that
  still discriminates — is the initial the e-form would have one modern Truku writes at
  all? **`empa-` is a real prefix**: 50 types / 166 spoken tokens (`empatas` 100× 在…讀書)
  against **0** `mpa-` types, which settles 22 of the 49 at a stroke. Every dark value's
  e-form four-gram is attested with 17–455 types **except `mpyah`**, where `empy-` is 0×,
  and it is the one value the branch correctly refuses.

  So tier W gained a second branch, `class`: no twin required, but the e-form's four-letter
  initial must appear in the lexicon (a `LICIT` counter over `attested | spoken`). The first
  run leaked into two frozen populations — `mpa`→`empa` and `mpsq'lol`→`empsqlul` are tier
  **N** names, `mbosi` and `mpasimpu` tier **J** loans — a reminder that a shape-driven rule
  fires on shape alone and must be told which populations are not its business. Adding N and
  J to the existing X exclusion fixed all four and nothing else. **W 140 → 301**; mapped
  6,733 unchanged, changing 4,732 → **4,772**; map diff `added 0 removed 0 changed 161`. The
  tier only ever prepends `e`, never re-decides a stem, so pre-existing stem defects it
  passes over (`mbubao`'s `ao` for modern `aw`, `mpax`'s `x`) are neither created nor
  worsened. `dom27.py`: 174 cards, 213 brown, 203 banned-form, **0 failures**.

  **Batch 28 — `^knq`, where the fix is not a prefix but an infix (2026-07-30).** The next
  named class in the sweep, 12 keys, and the sweep is right for a reason worth writing down:
  `knq` is **0 of 38,687 types**, and more than that, there is **not one `kn-` form on a
  q-initial root anywhere in the modern lexicon**. His words are unambiguously that shape —
  `Knqalas` 喜樂的強烈程度, `Knqalox` 黑暗的強烈程度, `Knqdlyeqan` 逃跑的程度 — the degree
  nominalizer `kn-`, which modern writes freely on every other consonant (`kncilux` 熱的程度,
  `kndahang` 小氣的程度, 45 of the 65 words glossed 程度 begin `kn-`).

  What modern does instead is put the **`-n-` inside the root**: `qaras` 喜樂 → `qnaras` 17×,
  `qduriq` 逃 → `qndriqan` 4× 逃跑, `qlqah` 踏 → `qnlqahan` 2× 被…踩踏, `qnquan` 25×
  過失；過錯；錯誤. So `kn-` is not a prefix that fails to attach to q — the same morpheme
  simply surfaces as an infix there, and `qn-` is 181 types / 949 tokens.

  **Four of the twelve were manual entries I had written myself** — `knkax` → *knqlqah*,
  `knkaxan` → *knqlqahan*, `knqdolyaq` → *knqduriq*, `knqt'lan` → *knqthuran*: right stem,
  wrong prefix shape, kn+q formed by analogy with kn+everything-else. The stems were right
  because they were read off the glosses; the shape was wrong because it was never asked of
  the corpus. That is the argument for the sweep in one line — it audits the half of a
  decision that gloss evidence cannot see.

  Targets were chosen word by word, not by rule. A mechanical `knq` → `qn` gets **8 of 11**:
  it mangles `knqnqoan` (his form already carries the infix, so modern is `qnquan`, and he
  flagged it "(?)" himself), it misses that `knq'mi`'s apostrophe marks the root vowel of
  `qumi` 仔細找及觀察 15× rather than a bare `qmi`, and it would invent *`qnalux` over the
  attested `qngqalux` 黑的樣子. **`knkax` is settled by a whole paradigm**: his separate root
  K'KAX (`kmkax`, `k'kax`, `kkaxe`, `kkaxan`, `kkaxon`) was already mapped form for form onto
  modern QLQAH (`qmlqah`, `qlqah`, `qlqahi`, `qlqahan`, `qlqahun`), which makes KNKAX the same
  root's `-n-` form and `qnlqah`/`qnlqahan` its two members. `dom28.py` asserts that paradigm
  unmoved alongside the twelve: 16 cards, 24 brown, 24 banned-form, **0 failures**.

  **Batch 29 — the sweep has no more classes, so work the identity claims (2026-07-30).**
  After 28 the largest named class left is 6 keys, so the method changes: rank the sweep's
  **identity claims** — values where the map says "his spelling is already modern" about a
  string the modern lexicon cannot write — by occurrences and work down. That is the worst
  state available to a word: brown, and claiming to have been verified. Green would at least
  be honest. 23 keys went in by hand, and every one of them was **already brown**, so the
  load-bearing assertion in `dom29.py` is the banned-form one, not the new spelling.

  Two veins came out of the top of the list.

  **A dropped initial q.** He does *not* drop q as a rule — prepending q to every 0× map value
  rescues **21 of 2,925**, which is noise, and the hypothesis was rejected on that number. But
  several of the 21 are basic vocabulary, and the tell is that the map **already had the
  q-form for a sibling in the same family**: `qbxni` → `qbhni` 306× 鳥 while bare `bxni` →
  *`bhni`* 0×; `kbaxang` → `qbahang` 89× 聽 while bare `baxang` → *`bahang`* 0×; `kpoling` →
  `qpuring` 40× 一群 while `poling` → *`puring`* 0×; `klxangi` → `qlhangi` 10× while
  `klxangan` → *`klhangan`* 0×. The defect is intra-family inconsistency, which is why the fix
  is a list (7 keys, plus `ntaan` → `qntaan` 70× and `taon` → `qtaun` 24×) and not a rule —
  the same family's `taan` 106×, `mita` 47×, `tai` 154×, `ita` 162× are attested as they stand
  and must not move.

  **`d` → `j` before `y`, in the DAYAW 幫助 root only.** `dy` is not impossible — the pronouns
  `dyami` 4× and `dyamu` 3× keep their d, and `dy` is 21 modern types — so a blanket rule would
  wreck them. His own paradigm settles the scope: DAYAO gives Dmayao / dayao / dyagi / dyagan /
  dyagun, and modern has `dmayaw` 126×, `dayaw` 5×, `jyagi` 53×, `jyagan` 6×, `jyagun` 15×.
  d survives before a and turns to j before y **inside one paradigm**; `jy` is 70 types / 126
  tokens. Eight keys, including `radyo` → `rajyu` 3× (the ラジオ loan).

  Then plain gloss matches the map had never been asked for: **`pnax` → `pnaah` 187× 自；從**
  (`paah` 591×) is the commonest word in the sweep; his WIT 累 root is modern **UWIT**
  (`uwit` 5×, `meuwit` 33× 很累, `keuwit` 3×, `smeuwit` 使牽累他人); his DUK 關閉 is **`eduk`**
  4× 門扇 (`mduk` 6×, `seeduk`, `peeduk`), and `nduk` 門關著 is `enduk` 門；橫隔膜. **This
  reverses a batch-26 judgement** that had filed `duk` → *eduk* as an unsafe coincidence.
  `mdup` / `ndup` / `duka` were left alone on purpose: modern has no p-final form of the root
  at all (`ndup`, `mdup`, `endup`, `edup` all 0× — `dupan` 獵場 is the other DUP root), and his
  own note says NDUP is NDUK with the final P surfacing as K, so rewriting his variant to the
  k-form is a lexical substitution, which belongs on screen in tier X and not silently here.
  **`mdup` was overturned in batch 158, and the measurement is what overturned it.** `-dup$` is
  0 words and `-duk$` is 96, which argues for the respelling rather than against it: a
  substitution is when his WORD is gone and a different one carries the sense, and here the
  root, the prefix and the sense are identical while one consonant differs — a consonant he
  documents as alternating. Batch 19's GALUP family had already taken six p-forms to k on his
  own doubled spelling; the two rulings contradicted each other until 158. `ndup` and `duka`
  stand: bare `duk` is unlisted, so they fail the K-twin gate.

  **The generator's own propagation had to be swept too**, and that is the transferable lesson:
  four derived forms came along that nobody typed. Two were fine (`penduk` off the attested
  `enduk`; `ndjyamu`, where `^ndj` is 0× but `^dj` is only 8 types, so the absence is what a
  tiny population predicts). Two were defects, and both were batch 28 repeating itself — the
  `-n-` goes *inside* the root and the q stays initial: `knklxangan` → *`knqlhangan`* carries
  the banned `^knq` and had to be pinned to `qnlhangan` 1×, and `nbaxang` → *`nqbahang`* has no
  bad n-gram at all but is 0× where `qnbahang` is 13×. **A hand batch must be re-swept after
  the rebuild, not before**: the n-gram test caught the first, but only the frequency check
  caught the second. Net: impossible values 1,141 → 1,125, identity claims among them 405 →
  394, **0 newly impossible**. `dom29.py` asserts the 23 plus the already-correct half of each
  family (`qbxni`, `kbaxang`, `kpoling`, `klxangi`, `dayao`, `dmayao`, `dyami`, `dyamo`,
  `taan`, `mita`, `tai`, `ita`, `mduk`) unmoved: 265 cards, 331 brown, 145 banned-form,
  **0 failures**.

  Deferred: **`xal` 14×**, where his own headword note says the bare form is never attested
  (從未見過此簡單形式) and the family is well attested with x (`pxal` 147×, `knxalan` 52×) but
  `^xa` is 0× — a candidate for removal-to-green rather than invention.

  **Batch 30 — `di`/`ti` are almost not written in modern Truku (2026-07-30).** Found the
  batch-29 way: `mtdiyal` was an identity claim sitting **next to `dmtdiyal` → `dmtjiyal`**,
  which the map already spelled right. d→j and t→c before i were already in the discovery list
  above, so the only real question was how much of the corpus still carries the unconverted
  form, and the counts settle it —

  | | types | tokens | | types | tokens |
  |---|---|---|---|---|---|
  | `di` | 4 | 10 | `ji` | 707 | 7,870 |
  | `ti` | 9 | 70 | `ci` | 985 | 2,062 |

  and the residue is loans and names (`dabidi`, `seediq`, `uting`, `kati`, `ciyating`). That is
  the tier-W shape of evidence: the correspondence is near-exceptionless. **It was still not
  applied wholesale**, because the blind half is where the guesses die. Ten went in
  twin-attested (his form 0×, the j/c form real): `padyaq` → `pajiq` 178× 蔬菜 (`mgpajiq` 85×
  菜像…一樣), `mpadyaq` → `empajiq` 12×, `mtdiyal` → `mtjiyal` 6×, `xliti` → `hriji` 留住
  against his XOLIT 我沒有挽留, `lutyaq` → `ruciq` 51× 罪, `mlutyaq` → `mruciq` 23× 髒,
  `slutyaq` → `sruciq` 4×, `pkngati` → `pkngaci` 8×, and the two names `tiwas` → `ciwas` 18×
  and `tiwang` → `ciwang` 28×. Eight more are blind derivatives of those same two stems, where
  nothing moves but the stem the corpus just confirmed.

  **Three of the blind half were lexical substitutions wearing a spelling defect's clothes**,
  and only a gloss search found that out: `kdiyong` 虎頭蜂 is not *`kjiyung`* — modern writes
  `srcing`; `qadi` 蜘蛛網 is not *`qaji`* — 蜘蛛 is `krubaw`; `mslidil` 歪斜 is not *`msrijil`*
  — 歪 is `mriqi`/`kapih`. The XETI 遺產 family (`xtiyan`, `xtiyun`, `xntiyan`) was held for
  the same reason: I had assumed `hci-`, and 留下 turns out to be `hnici` 38× / `hmici` 11× /
  `mhici` 2×, which does not syncopate. **A near-exceptionless correspondence still cannot tell
  you the word is the same word** — that is the one thing the n-gram sweep and the twin test
  both share as a blind spot, and the gloss is the only thing that sees it. `dom30.py` asserts
  all eight exclusions unmoved alongside the 18: 50 cards, 64 brown, 51 banned-form,
  **0 failures**. Impossible values 1,125 → 1,114, identity claims 394 → 391.

  **Batch 31 — past the classes, the gloss search is the only method left (2026-07-30).**
  The identity-claim list stops being a class after `di`/`ti`; it is unrelated words. So
  sixteen were looked up **by their Chinese gloss**, and three families came back.

  **SUIL 偶爾 → SUWIL, where he printed the answer himself.** His headword reads
  `MSUIL (MSUWIL)`, and modern has `msuwil` 16× and `suwil` 7× 有時候（偶爾）. The variant was
  sitting in the entry and no tier ever read it.

  **NUGUL → NEGUL, and this one is why gloss beats shape.** His root carries two senses —
  細繩／繫繩／連結／線, and 跟隨 through SNUGUL — and modern carries both on one stem: `negul`
  6×, `enegul` 綁著, `sgnegul` 只靠…繩子, `tmnegul` 曾專編…繩子 for the cord sense; `snegul`
  35× 跟隨, `msnegul` 7×, `smnegul` 7×, `empsnegul` 1×, `psnegul` 是跟隨 for the other. Eight
  of his forms moved, seven witnessed directly. A shape test would have had nothing to say
  about `u` → `e` in a stressed root vowel; the glosses made it a single lookup.

  Plus **`snkaxa` → `sngkaxa`**, whose modern gloss is the one word 前天.

  **Searched and refused, which is the other half of the yield:** `msnoxel` 嫉妒 (the modern
  root is `hkrig` — `shkrig`, `sphkrig`, `skhkrig`), `tknayun` 同伴 (`gxal`), `denki` 電
  (電燈 is `samaw` 254×), `sktama` 先父 (**nothing** in the modern lexicon glosses 先父). Those
  are lexical substitutions, which declare themselves on screen in tier X and are not the map's
  business. And **`ppxal` was exonerated rather than fixed**: `pxal` 147× 一次 is itself
  attested — modern Truku writes x — so his reduplication is an ordinary blind, not a wrong
  claim. `dom31.py` asserts all of those unmoved: 43 cards, 65 brown, 44 banned-form,
  **0 failures**. Impossible values 1,114 → 1,103, identity claims 391 → 380.

  **`ts` → `c` is NOT a class — tested and rejected.** It looks like one, since modern `c` is
  /ts/ and 1,230 types carry it, and `tsmanan` 破曉/清晨 pairs with a `csmanan` glossed 清晨.
  But **modern Truku writes `ts` too** — 48 types / 74 tokens (`emptsamat` 18×, `tsasaw` 6×,
  `ptsani` 4×, `tsongan` 4×) — and of the 27 map values containing `ts`, three are attested
  **with** the `ts` (`tssagan`, `tsgasut`, `tsasao`) while **every single c-twin is 0×**. The
  correspondence that made `di`/`ti` safe is exactly absent here. Anything in the TS'APAT /
  TSLABANG / TSDAXAL families needs individual gloss evidence, not the sequence.

  **`tools/orthography/../tmp/glossmatch.py` (not in the repo) mechanises the batch-29-to-31
  loop** so it stops being sixteen hand lookups per batch: for every impossible value it takes
  his headword-level gloss (never an example sentence — those describe a whole clause and match
  anything), finds every modern word whose gloss overlaps, and scores the pair on **both** axes,
  gloss overlap × shape distance. Neither alone is usable: gloss-only proposes lexical
  substitutions, shape-only walks into the raki/laqi trap. 151 of the 1,103 have a candidate
  scoring on both. Top of that list, adjudicated but **not yet applied**: `kn'udus` → `kneudus`
  54× 生命 (his apostrophe is the modern `e`, cf. `meudus` 67×), `knstmaan` → `kntmaan` 3× 信仰,
  `msspong` → `mspung` 7× 摔角, `kptoxan` → `kmptuhan` 6× 寡婦, `iing` → `iying` 尋找
  (`miying` 135×), `knqlinut` → `qngqrinut` (the batch-28 infix again, parallel to `qngqalux`),
  and `tl'xlax` → the `hurah` 鬆開 family, which is one of the split families left open by
  batch 23. The four PAIS forms it scores highly (`ppais`, `dpais`, `pnpais`, `mapais`) are a
  **false positive worth remembering**: the gloss is 敵人 and the candidate is bare `pais` 126×,
  which is the root and not the form — high on both axes, still wrong.

  **Batch 32 — the first batch glossmatch picked (2026-07-30).** Eleven keys, all one
  signature: *the map already spells a sibling on the stem the modern way, and these were
  left behind.* **KUDUS 生命** is the clean case — the map writes `keudus` in five places
  (`kkudus`→`kkeudus`, `mpk'udus`→`empkeudus`, `pk'udus`→`pkeudus`, `pnk'udus`→`pnkeudus`,
  and his own bracket variant `knoudus`→`kneudus`), so **his apostrophe IS the modern `e`**,
  and the three keys that kept the bare `u` (`kn'udus`, `mk'udus`, `mkudus`) were simply
  missed. `kneudus` is 54× 生命, his gloss exactly. Same shape elsewhere: `knstmaan` →
  `kntmaan` 3× 信仰; `msspong` → `mspung` 7× 摔角 (his 彼此較量 is the reciprocal, and the
  lexicon writes `sspung` but never `mssp-`); `knqlinut` → `qngqrinut`; and `pxlnasan` →
  `phrnasan`, which wrote `hl` where **all nine** of its siblings write `hr`.

  **`kptoxan` and `knptoxan` both → `kmptuhan`.** Two keys, one value, deliberately: both
  gloss 寡婦－鰥夫 identically and modern has exactly one word for it, `kmptuhan` 6×. He
  printed the same word twice; `kmnptuhan` and `knptuhan` are both 0×.

  **Word-initial `ii` is not written in modern Truku** — `iing` → `iying` 尋找 (`miying`
  135×) and `iita` → `jiita` 4× 我們. But it is **two words, not a rule**, and the refusal is
  the finding: `miing` 53× 找 is itself attested, so `miing`→`miing` stands, and the whole
  LIING family (`lmiing` 3× 藏起來) is the *other* root, hiding. `dom32.py` asserts those
  plus the batch-30 ITA forms and the three glossmatch proposed that the gloss check killed
  (`psnmaan` — 準備 is `psramal` 70×, a different root; `tkgabal`; `tsmanan`): 61 cards,
  77 brown, 28 banned-form, **0 failures**. Impossible values 1,103 → 1,094, identity claims
  380 → 377, and the post-rebuild re-sweep found **0 newly impossible and 0 derived forms
  moved** — the batch-29 propagation check, now routine.

  **The green count, measured in the DOM at last (2026-07-30).** `render()` bails to the
  cover when the box is empty, but `norm()` strips combining marks — so `?q=%CC%81` survives
  `trim()`, normalizes to `""`, and `filter()` returns **every** entry. All 1,967 cards on
  one page: **637 green types / 1,090 occurrences, 2.4% of the displayed words**; brown
  6,133 / 43,491 (97.6%). The static count over `entries.js` says 776 / 6,602 / 13.1% and is
  **wrong by ~5,500 occurrences** — its top is his French metadata (`r` 2767×, `name` 540×,
  `emprunt`/`jap`/`chin` 242× each), which `metaAbbr` / `TAG_PROSE` / `FORM_PROSE` intercept
  before `respellable()` is ever asked. Count green in the DOM or don't quote a number.
  **Batch 33 — L'XLAX, and the one thing an attestation test can never catch (2026-07-30).**
  A split family left open by batch 23: the map wrote his one root **five ways** — `lxlax`,
  `mrxrax`, `mtlhlah`, `plhlah`, `rhrhun`. The gloss check says the problem is not the
  inconsistency. It is that **five of those values are attested modern words that mean
  something else**: `lxlax` 2× is 機槍 *a machine gun*, `rxrax` is 沒肉的骨頭 *a bone with no
  meat* (`rxraxay` 已啃骨頭), `rhrhun` belongs to 磨擦 *rub* (`rhrhaw` 讓…磨擦), and
  `pklxlax` / `lxlaxan` belong to the **snap** root (`pnklxlax` 使之斷裂, `empkklxlax`
  會使之光禿, `lxlaxan` 地裂).

  His root is **LHLAH**: `lmhlah` 6× 解開, `plhlah` 4× 被脫;被卸, `tlhlah` 2×, `splhlah` 2×
  使脫下, `mtlhlah` 掙脫, `lhlahi` 要脫掉;卸, `lhlah` 脫落, `mhlah` 脫;卸 — against his
  自由的、鬆開的、脫離的 / 被解開、拆開、鬆脫的 / 使解開－使脫下－釋放. Six forms were already
  on that stem; ten were not, and now are.

  **The lesson no earlier batch could teach: an ATTESTED value can be a WRONG value.** The
  n-gram sweep cannot see it, `assert v in LEX` cannot see it, and the **id tier manufactures
  it** — `l'xlax`→`lxlax` was tier `id`, i.e. "his spelling is already a modern word," which
  was true and irrelevant. Only the gloss sees it. Every remaining `id` claim is suspect in
  this new way, not just the impossible ones.

  Two adjudications inside the batch. `pkl'xlax`→`pklhlah` came back **newly impossible** on
  `pklh`/`klhl`, so the causative goes on the bare stem the modern paradigm itself alternates
  to — `mhlah` is `m`+`hlah` — giving **`pkhlah`**, licit and blind. And the rebuild added
  `mpslxlax`→`empslhlah` on its own (tier W, a previously unmapped word): licit, right stem,
  accepted. **NOT touched**, and this is what `dom33.py` asserts: `xlaxan`→`hrahan` 2× 拆除,
  `xlaxe`→`hrahi`, `xlaxon`→`hrahun` are his **other** root, XLAX without the `l`, whose
  modern form genuinely is `hrah`/`hurah` (his gloss there: 想要或必須拆除、拆解的東西). Two
  roots, two stems. 5 cards, 23 brown, 22 banned-form, **0 failures**. Impossible values
  1,094 → 1,088, identity claims 377 → 376.

  **Batch 34 — the elision mark deleted onto a different word (2026-07-30).** Batch 33's
  finding, made into a sweep. `apostrophe.py` takes every key carrying one of his elision
  marks whose value is just the mark **deleted** and the result attested, and ranks them by
  how far the modern gloss sits from his: 108 keys, and the top of the list is a list of
  wrong words. His mark is not decoration — deleting it lands on a real, usually very
  frequent, unrelated word, and every check the build runs says yes.

  | his form | was | frequency of the wrong word | is now |
  |---|---|---|---|
  | `"BI` 小屋 | `bi` | 6,292× 一定 | `biyi` 27× 工寮 |
  | `"MA` 舌頭 | `ma` | 343× (question particle) | `hma` 54× 舌頭 |
  | `"LU` 路 | `lu` | 79× 白費 | `elug` 224× 路 |
  | `"LO` 傳染 | `elug` | — the *other* fix's answer | `eeru` 5× 傳染 |
  | `"MU` 細塵 | `mu` | 3,047× 我 | nulled — nothing glosses 細塵 |

  The `"LU`/`"LO` pair is the shape of the whole problem: two of his marks, two different
  roots, and the map had them **swapped onto one word**. `gm"lu`→`gmeelug` 開路 and
  `pn"lu`→`pneelug` came with the road; `ma"lu`→`meelug` is blind but the paradigm
  doubles the vowel throughout. `"lo`→`ru` came back **newly impossible** on `^ru$` (the
  bare stem is never written alone), so it takes `eeru`, with `mreeru` 46× 會傳染
  confirming the paradigm. `"mu` and its three derivatives get a **null in
  `lexical_map.json`**, which freezes them green across every tier — the honest answer
  when the modern lexicon has no word for the sense.

  Verification found a defect **in the renderer**, not the map. `dom34.py` reported `'qan`
  green on the SOLA card, and `'qan`→`ekan` was an *exclusion*, asserted unmoved. The
  cause was `tidyLatin`'s matched-quote rule: his mark opens a word (`"qan`) and closes one
  (`Ma"`), so a line carrying both reads as a quotation, and `"qan n'xali ! Ma" so psola
  sadyaq!` was set as `“qan n'xali ! Ma” so psola sadyaq!` — the mark pulled off
  `ekan`, leaving a bare green `qan`. Across all 12,731 Truku strings the rule fires exactly
  **twice**: this line and one genuine French quotation (`Knlbuan = "matinalité"`). Only the
  lexicon separates them, so the rule now declines to pair when either end is a form the map
  knows. Both render correctly. 122 cards, 138 brown, 111 banned-form, **0 failures**.
  Impossible values 1,088 → 1,085; identity claims 376, unchanged; four keys leave the
  map, so changing tokens 4,809 → 4,805.

  **Batch 35 — the tail of the sweep, and five of eight suspects were RIGHT (2026-07-30).**
  Worth recording as the useful half of the result, because it is what keeps the method from
  becoming a licence to rewrite anything whose omnibus gloss looks odd. `sru` “木杵” is the
  instrument sense of his 懲戒－訓斥－處罰 (`msru` 打, `psru` 打（用手打）, `empsru` 要打);
  `bruq` is the blister root (`embbruq` 8× 起水泡); `krung` the wrinkle one (`krngan` 已…成皺的);
  `rsung` the annihilate one (`rmsung` 消滅); and `rdu` carries his 停止 through `mtndu`, whose
  modern gloss is literally 「停止;地陷下止住的地方」 — his sense and the omnibus's 地坦方 on one
  word. **A wrong-looking gloss is a question, not a verdict; the paradigm answers it.**

  Two real defects, one root each. **S'AYANG** 「有煤油味」 sat on `sayang` 1080× 今天, the most
  frequent wrong word the sweep has produced; `ayang` is 石化燃料 and `seayang` 2× is 油味.
  **"LU**, the road, where batch 34 fixed the headword and left five relatives on `sru`: his
  `S"LU` 計劃－預謀 carries 參見 "LU in his own hand, `Sm"lu` is 計劃, and the two with no gloss
  of their own (`ps"lu`, `ms"lu`) share an example about 行為不合乎正道 — conduct off the right
  path, the metaphor itself. `elug`'s own modern gloss is 行事. Six keys onto `eelug` on batch
  34's paradigm (`gmeelug`, `meelug`, `pneelug`), and the rebuild's `sneelugwan` for his
  `Snluwan` was replaced by hand with **`sneelugan`** — his glide is there because `snlu` ends
  in a vowel, and `elug` does not. 220 cards, 260 brown, 80 banned-form, **0 failures**.

  **Not fixable by a word map, and recorded so it is not re-proposed:** `l'ndax`. His `L'ndax`
  under L'DAX is 照亮－使發光, and that root keeps its x in modern Truku (`rdax` 24× 光線,
  `rmdax` 27× 發光, `prdax` 7× 照明), so the value `rndah` is the wrong word. But **L'NDAX
  (LNDAX) is a separate headword meaning 更加**, and `rndah` 2× is exactly 更加的；反而更. Two
  words, one spelling, one key. The headword keeps it; the sub-form is a homograph the map
  has no way to reach.

  Tier sizes above are now read straight from `modern_map.json`. The **M** figure had been
  the key count of `manual_map.json` (780 keys), which is not the same number as the tokens
  tier M actually wins (735) — earlier tiers take some of them first.

  **Batch 36 — a correspondence the tiers never learned, and a rule that ran one word too
  far (2026-07-30).** Both found by re-running `glossmatch.py` against the current map.

  **His `ts` is modern `cs`** — his `t` is written `c` before `s`. The lexicon has **67 words
  beginning `cs-`** against 48 containing `ts` at all, so `cs` is the norm, and five of his
  `ts` words have an attested twin whose gloss is his own: `csdamat` 17× 思念;寂寞;哀傷 for
  非常悲傷、非常思念, `csmanan` 清晨 for 破曉－約清晨三點, `csuraw` 驚醒;打昆 for 昆頭的－胡言亂語的,
  `csngiya` 7× 透透氣 for a headword he left glossed 「？？」, and `csgasut`, which the omnibus
  carries under **both** spellings with one gloss (做事細心).

  **`DITA` → `deita`.** Batch 30's `d`→`j` before `i` is right, and here it ran into a word
  that is not a `d` plus an `i`: his `Dita (D'ita)` is a sub-form of ITA, 我們, and the family
  — `Ddita` 我們全體自己人, `Sdita` 設法成為我們群體的一員, `Msdita` 善於交際的 — was sent to
  `jita`, which is 92× 走. Modern spells the stem `eita` and the family is enormous: `deita`
  我們, `ddeita`, `sdeita` 3×, plus `sgeita` 跟自己人…, `skeita` 一定要和自己人…, `speita`
  把…當作自己人 for his 自己人 sense and `ksteita` 親切 / `kmsteita` 2× 讓…親切 for his
  善於交際. All five of his occurrences sit under his ITA entry. **A rule that is right can
  still be wrong about one word; the gloss is what tells you which.**

  **Held, and this is the honest half.** The other `ts` keys — `tspatan`, `tssagan`,
  `tslabang`, `tskoe`, `tsdaxal` — have no `cs` twin in the lexicon and no gloss to argue
  from; TSKOE 桌子－書桌 is not Truku at all but Japanese *tsukue*, a tier-J question. And
  his whole **PAIS** family (`ppais` 敵人（複數）, `dpais`, `pnpais`, `mapais` and eight
  more) are identity claims the n-gram test calls impossible, but modern attests only `pais`
  126×, `kmpais` 7×, `kpais` 3×, `kkpais` 2×. **An unusual shape is not evidence of a wrong
  shape**, and there is nothing to put in their place. 124 cards, 159 brown, 31 banned-form,
  **0 failures**. Impossible values 1,085 → 1,078; four identity claims become real changes,
  so changing tokens 4,805 → 4,809.

  **Batch 37 — two more roots that lose a segment in his spelling, and three suspects that
  survived the look (2026-07-30).** Same shape as ELUG and EITA, found the same way.

  **`IMAX` is `imah`, but after a bare p- it is `eimah`.** The map was right for the bare and
  m- forms — `imah` 26×, `mimah` 124×, `kmimah`, `mnimah`, `nimah`, `mahun` 20×, `mahan`
  33× are all attested as written. But where p- sits **immediately** before the stem, modern
  writes `eimah`: `peimah` 3× 使…喝 for his Pimax 使人喝, `speimah` 讓…喝 for his Spimax
  用來給人喝, `empeimah` 要讓…喝 for his Mpimax 稍後將請人喝. It had `pimah`/`spimah`/`empimah`,
  none of which exist. Not a rule about p in general — his Ptgimax is `ptgimah` 因喝…而死,
  attested with no e, because tg- intervenes.

  **`TABU` 餵養、飼養牲畜 is `tabug`, with the g, exactly as 路 was `elug`.** His Mtabu
  餵養者－放牧者－牧人－牧者 is `mtabug` 26×, whose modern gloss is 牧師; Tmabu is `tmabug`
  26× 去餵食; Ptabu 託人餵養 is `ptabug` 使托養; and the locative **he gives himself** —
  *Tb'gan (Tbgan), 前一詞 TBUAN 的變體* — is `tbgan` 22× 養家畜的地方, which the map already
  reached from his g-spelling and did not reach from Tbuan.

  **Held: his headword `TABU` itself.** He has two of them — 餵養、飼養牲畜 and 不太適合加工的
  闊葉木材 — and one key cannot spell two words. That is the `l'ndax` rule, not a new one.

  **Exonerated, and this is what the looking is for.** NAMA 預備 was offered `psramal` 70×
  準備, but his root is real — `nama` 2× 先去;先去預備, `snama` 3×, `psnama` 2× 預備,
  `empgnama` 2× 將為…預備 — so Psnmaan is an ordinary blind on an attested stem. STAMA
  依靠 was offered `snraan` 2× 盼望, but `smtama` 50× 依賴, `stmaan` 21× 依賴, `stmaun`
  10×, `stama` 10×, `kntmaan` 3× 信仰 and `pstama` 2× are his whole family, attested.
  TKGABAL 已被拔起的 was offered `kgabal` 被拔 / `mtgabal` 被拔起, but **tk- is a real modern
  prefix** — 76 words begin with it, one of them his own `tkanan` — so there is no reason to
  prefer a different prefix over the one he wrote. Three of six suspects taken.
  56 cards, 120 brown, 50 banned-form, **0 failures**. Impossible values 1,078 → 1,072;
  changing tokens 4,809 → 4,816.

  **Batch 38 — the e was the class all along (2026-07-30).** ELUG, EITA, EIMAH and TABUG were
  four words found one at a time. They are one finding: **modern writes a schwa where his
  spelling writes nothing**, in two places.

  **(a) Between a prefix and a vowel-initial root — and his own elision mark is usually sitting
  exactly on the seam.** `P'adas` 寄送 is `peadas` 14×, `M'ulat` 抽筋 is `meurat`, `S'angal`
  用以拿取 is `seangal` 7×, `Pk'ulae` 使挨餓 is `pkeuray`, `Pk'angal` 使脫落 is `pkeangal` 2×
  脫落. The apostrophe he wrote is the morpheme boundary, and the boundary is where the vowel
  goes. **(b) Inside an n-cluster** — `Tngsaan` 學生 is `tnegsaan` 13×, `Pngluban` 協會 is
  `pnegluban` 8× 關係, `Kngoxan` is `kneguhan`, `Ngabal` is `negabal`.

  Swept mechanically instead of one at a time: for every map value the lexicon does not have,
  insert `e` after each prefix boundary and keep it only where **that** is an attested word.
  65 came back; then read the gloss on every one. **66 keys and not one blind — every target
  is attested.**

  A third shape the sweep could not see, because the map had already inserted an `a`: his GALU
  溫柔、憫憫、關愛 was `gaalu` and the whole family with it, but modern is **`gealu`** — `gnealu`
  50× 恩典慈愛, `gmealu` 25× 同情;疼惜, `sgealu` 23× 可憑, `mggealu` 7× 相愛, `pgealu` 3×
  要憫愛. Seven more keys, and tiers G and E projected fourteen others on their own.

  **Rejected — nine, all for one reason: the e-form is a real word but a DIFFERENT word.**
  `Tango`/`Tmango` 嫩芽 would become `teangu`/`tmeangu` 成為弟媳、騷擾弟媳 — `angu` is a
  sister-in-law, not a shoot. `Mpia` 第幾次 would become `empeiya` 不要. `Msnama` would
  become `msneama` 為了女婿而爭執`. `Pnalu`/`Knalu` 代替、頂替 would become `pnealu`/`knealu`
  放…的延長線 — that is `alu` 'cord', which his NALU is not. And `Tnaga`, `Mkmita`, `Kketa`
  are example-only forms each of which could be built on two different roots.

  558 cards, 962 brown, 429 banned-form, **2 failures, both checker artifacts**: his
  `Ti malu (TIMALU ?)` and `(vl. ti malu)` are collapsed by `joinClitics` into one token and
  render brown as TGMALU, so the bare MALU the checker looked for never exists in the DOM.
  Verified in the live DOM on both cards. Impossible values 1,072 → 1,057; changing tokens
  4,816 → 4,836. **Measured green after this batch: 639 types / 1,099 occurrences — 2.5% of
  displayed word occurrences, down from 2.8%.**

  `dom23.py` asserts the ten plus **twenty neighbours that must not have moved**,
  because the rejections are the load-bearing part: 77 cards, 98 brown, 90
  banned-form, 0 failures, with LABANG keeping its l on all four forms and
  `lnglongan` 52× (a different root, 心/思念, same g-l-ng shape) untouched.

  Left open rather than forced: **`klkari`** (his 眾多話語（複數形）, `krkari` 6×) — the
  reduplicant liquid is his l against modern r in `mllawa`→`mrrawa` 33× and
  `pllawa`→`prrawa` 11×, but `llabang`→`llabang` 16× keeps ll, so the rule is not
  uniform, and `kari` first-glosses as 挖掘, which makes `krkari` possibly "dig
  repeatedly". **`pslabang`** belongs to his *other* LABANG (誇大——誇張事實), whose
  r-side is well attested (`rmabang` 6×, `prbangan` 4×, `prabang` 2×) — 誇大 against
  `rabang` 較多 is plausible but unglossed, so the 寬闊/誇大 split needs its own pass.
  And **`mqlaq` → `mqraq` 2× is now suspect**: it is an existing non-identity mapping,
  but 癢 is `krak`, so the target is unglossed and may be a truncation of `mqraqil`
  皮. Reverting it needs its own evidence.

  **Batches 43–47 — the green list itself as the work queue (2026-07-31).** 108 keys in five
  batches: 941 → **1,049 manual keys**, changing tokens 4,854 → **4,972**, true green
  **597 types/947 occ → 522/808**. dom43 269 cards / 319 brown / 95 banned-form / 1 failure
  (fixed, below), dom44 29 / 54 / 55 / **0**, dom45 144 / 158 / 26 / **0**, dom46
  74 / 109 / 77 / **0**, dom47 32 / 48 / 43 / 1 — a real defect in app.js, finding (7) — and
  32 / 48 / 44 / **0** after repairing it.

  Per batch the green subtraction is 43–45: −58 types, 46: −16, **47: −1**. Batch 47 looks
  like a failure by that measure and is not: it found three words the app was actively
  mis-rendering. The reason it scored 1 is finding (7) — the counter had been lying.

  **(1) His `l'x` is `lh` or `rh` — never `dh`.** `l'xlax`→`lhlah`, `l'xeq`→`rhiq`,
  `l'xo`→`rhu`, `l'xkan`→`rhqan`: all ~60 keys carrying `'x` after `l` go one of those two
  ways. This is what forbids `l'xqoi` → `dhquy` *however exactly the gloss fits* — his
  `Payai l'xqoi` 黏糯 is modern `payay dhquy` 糯米 three times over in the corpus, the best
  gloss match found in weeks, and the shape still says no. Dumping the whole `'x` key class
  before believing a single member of it is now the standing move. (`D'XO` is not a
  counterexample: there the `'x` follows a stop, where it *is* `dh` — `d'xo` → `dhug`, which
  his own headword note asks for by suggesting the spelling D'XOG.)

  **(2) A trailing straight quote is its own key.** dom43's one failure — `D'XO` printing the
  non-word DHU — was real but tiny: his note offers a second spelling `D'XO"`, and `wordKey()`
  folds `"`→`'`, giving the unmapped key `d'xo'`, which then fell through to `charRules()`. A
  repo-wide scan of every string field found only four trailing-quote tokens in the book
  (`d'xo'` ×3, French `pas'` ×1), so the one-key fix in batch 44 closes the class.

  **(3) The map was sitting on unattested values inside otherwise-finished families.** Batch
  44's SQDO family found `psqdu`/`ppsqdu`/`tnqdu`/`qduan` all committed and all 0× — his own
  `Snqdgan` spells the root's `g`, so the family is `-qdug` throughout. Same for `md'xo`→`mdhu`,
  `smd'xo`→`smdhu`, `pkl'ulus`→`pklulus`, `mtkwini`→`mtkwini` (an identity claim on a form
  that is 0× either way while `mtkuni` is one letter off). This is why `imp.py` showed
  impossible values nearly flat across 43–45 while 50+ keys were added: repairs and new blind
  claims cancelled. **Auditing a family the map has already "done" is as productive as
  finding a new one.**

  **(4) Half a paradigm mapped is a green flag, not a finished card.** DUI was 41 green
  occurrences hiding behind three brown ones: the map had the goal-focus side (`Dian`→`jiyan`,
  `Diun`→`jiyun`, `Sdian`→`sjiyan`) and had left the entire actor side alone. It is `duuy`
  36× 抓住；握住 / `dmuuy` 165× / `mduuy` 101× / `sduuy` 22× / `mdduuy` 2× 互相殘殺 (his
  Mddui 彼此相扶持). Same shape in batch 46's XBUI (`Xbiyan`→`hbiyan` done, root `hbuy` green)
  and SKUI (`skuy`, `knskiyan` done, `mskui`/`kskui` green). **When a green token's card has
  brown siblings, the root is usually already decided — go read the card, not the corpus.**

  **(5) `OVERRIDE_KEYS` was freezing the human, not just the generator — and failing silently.**
  Batch 46 wrote 13 gloss-verified `-ui` keys; the rebuild reported success and **dropped all
  13**, because `if t in OVERRIDE_KEYS … continue` sat *above* the `t in manual` check in the
  main token loop. Nothing warned: `manual_map.json` had them, `site/modern_map.js` did not.
  The freeze list itself is right — his `-ui` cannot be decided by rule (see (6)) — so the fix
  is one line: `adjudicated = (set(manual) | set(llm)) - lex_block` lifts the freeze for tokens
  a human has actually ruled on, and `lex_block` stays frozen because a null in `lexical_map`
  is itself a decision ("stay green"). Intersection checked before the edit: exactly the 13
  keys, zero collisions with `lex_block`. **Verify a key landed in `modern_map.js`, not just in
  `manual_map.json` — the builder has tiers that can outrank you without saying so.**

  **(6) The `-ui` class, decided (batch 47, 27 keys).** The rule table offers both `ui→uy` and
  `ui→uwi`, which is why 39 tokens were frozen. Both are right, and the gloss is the only thing
  that picks: **KLUI 驚訝 → `kluwi`** (`nkluwi` 驚訝, `skluwi` 2× 嚇一跳, `mskluwi` 5× 驚嚇,
  `mnskluwi` 12×) but **BKLUI 下巴 → `bkluy`** (`sbkluy` 大下巴, `gmbkluy` 專取下巴) — the same
  `-klui` string, two spellings, no shape difference to appeal to. Also BUKUI 綁 → `bkuy` with
  `Mukui` → `mkuy` 16× 捆綁 (his epenthetic u dropped, as always), KTUI → `ktuy` / `kmtuy` 42×
  收割, TUTUI → `tutuy` 37× / `mtutuy` 108× 起床, and his own three-way spelling
  `m'xapui (mapui - mapwi)` all → `mhapuy` 124×. Unadjudicated members of the class stay frozen.
  **This class had already been decided once**, in `WORD_OVERRIDES` (app.js, note dated
  2026-07-19), and batch 47 re-derived it independently and agreed everywhere but three keys —
  which is the corroboration, and also finding (7).

  **(7) `respellable()` reads THREE tables, and the green counter only read one.** app.js:
  `WORD_OVERRIDES` → `MODERN_MAP` → `CLITIC_FORMS`, first match wins for both colour and
  output. Every green count taken by reading `modern_map.js` alone was therefore too high: the
  37 `WORD_OVERRIDES` keys (the whole `-ui` class) and 55 `CLITIC_FORMS` keys were being
  reported as unverified when the app renders them brown. Re-measured with all three
  (`tmp/green3.py`), the true figures are **597 types/947 occ before batch 43 → 522/808 now**,
  not the 622→535 the old counter gave. **Count against `respellable()`, not against the map.**

  Two of those overrides were also wrong, and only the second table's precedence hid it:
  `mpdui` → `mpduuy` (0×, against `empduuy` 3× 要握 and the documented `emp-`/`mp-` schwa
  class) and — worse — `m'xapui`/`mapui` → **`mapwi`, which is one of *his own* three
  spellings in the very sentence they occur in** (`m'xapui (mapui - mapwi)`), so modern mode
  was printing Pecoraro at the reader. The sentence is KSIA / Mksia 液化: "boil the fruits of
  this tree and they liquefy" — `mhapuy` 124× 在煮. All three keys were deleted from
  `WORD_OVERRIDES` so the map governs. **An override table that outranks the map has to be
  audited against the map, or it silently preserves the oldest guess.**

  **Batches 39–42 — two mechanical classes exhausted, and the green count finally measured
  where it lives (2026-07-31).** 34 keys across four batches; dom39 743 cards / 1,064 brown /
  141 banned-form / **0 real failures** (one proven clitic artifact: MANGALI's only `spat` is
  inside `Ti spat`, which `joinClitics` swallows — same class as `Ti malu`→TGMALU), dom40
  (batches 40+41) 208 / 253 / 116 / 0, dom42 53 / 79 / 44 / 0. Impossible values 1,057 →
  **1,019**, identity claims 1,894 → **1,876**, changing tokens 4,836 → **4,854**.

  **(1) The deletion class is his MORPHOLOGY, not his spelling.** 122 rows where his token is
  the map value minus exactly one character looked like a rich vein. It yielded **one** fix
  (`mspatuil`→`mspatul` 四十, 14×). Everything else was his own prefix or infix on a base the
  map already handles — n-, pn-, mk-, and the -n- past infix. A distance-1 test cannot tell a
  typo from a morpheme. Same for the **doubled-vowel repair sweep** (`v43.py`): 2 hits in the
  whole map, both glossless. Both classes are closed.

  **(2) The schwa is ROOT-specific, not cluster-specific** — the batch-38 finding, bounded.
  Test each proposal by counting modern words that prefix that root *with* the e against
  *without*: aji, isil, iril, ayus, apa, uda all take it (`meaji`, `mkeisil`, `mkeiril`,
  `sneayus`, `ppeapa`, `peuda`); `kiyux` 很窄 is attested bare, killing `mkeiyux`/`tkeiyux`/
  `empkeiyux`; `gklaan` 2× killed `negklaan`; `inu` has no prefixed form at all, so `mkeinu`
  is unwritable; gxal is mixed. And **the `-um-` infix is not a prefix**: `muda` 285× has no
  schwa even though `teuda`/`mtneuda` do.

  **(3) The maa- twin test.** Take `empaa-X`/`npaa-X` only where an attested `maa-X` twin
  exists — maabalay 4×, maamalu 2×, maabubu, maalaqi gave six keys; no twin killed mapais,
  mpasnao, mabugo, mpasimpu. `empee-` is a different morpheme: 'will BE', as in `empeepiya`
  2× 會有多少.

  **(4) Check the SHORT form before assuming the long one.** A 23-key "class" evaporated:
  modern writes both `qpah`/`qpahan`/`qpahi`/`mqpah`/`empqpah` **and** `qmeepah` 138×, so
  every proposed lengthening was already wrong. Batch 41's pre-flight killed three more the
  same way: `mmangali`/`mmngali` are 第九次 (MA+NGALI 'nine'), not the ANGAL family; attested
  `tneaga` is 三叉箭主人; `kketa`/`mkmita` repair onto *ita* 'we' while his forms are KITA 看.

  **(5) The green count is 92.7% solved on his own text, and the raw list is deceptive.**
  Whole-dictionary DOM census (`?q=%CC%81` — a lone U+0301 survives `trim()` but `norm()`s to
  `""`, so `filter()` returns all 1,967 cards): 855 green types / 1,099 occurrences. Split by
  whose text the word sits in (`gsplit.py`, classifying on whether the containing element's
  text starts with `§`): **543 green occurrences are Pecoraro's own words, 538 are the modern
  example sentences fetched at runtime from R2, 18 other**; brown is 6,945 his / 35,836
  modern-example / 694 other. **The R2 half needs no work at all** — those are already modern
  Truku. So of his own displayed words, 6,945 of 7,488 = **92.7% are brown**.

  Two traps in reading that list. **An unkeyed word still gets `charRules()` applied before
  printing**, so a green word can look perfectly modern on screen — his KLULU displays as
  KRURU and is *unverified*. A work list built by folding DOM text back to keys (`gwork.py`)
  therefore produced `kruru`/`mgdhu`/`krhqun`, none of which exist in entries.js. Build the
  list from **his tokens** instead (`green2.py`), excluding the `tag` field (French prose:
  `r` 2767×, `name` 540×, `emprunt`/`jap`/`chin` 242× each — this is what over-counted green
  ~6×) and excluding `§` examples: **622 distinct green keys / 1,213 occurrences**, which is
  the real remaining work list.
- **L** (237) — the former review queue, adjudicated case-by-case against Chinese
  glosses (`tools/orthography/llm_map.json`). Key discovery from this pass:
  Pecoraro k before a consonant is very often modern q (kbsulan→qbsuran,
  kpaxan→qpahan, klaxang→qlahang), and his q is often modern k (qeulit→qowlit,
  tmataq→tmatak). ~149 cases were deliberately left unmapped (false friends like
  qmapax "spread" ≠ qmpah "work", particles, unidentified loans) — they're in
  modern_map.json's "review" key.

  **This tier's own rule — "accepted only when the omnibus gloss matched his
  Chinese" — cannot be applied to a name, because a name entry has no gloss.**
  `name (m)` is a tag and the zh field is empty, so there was nothing to
  adjudicate against and eleven names were decided on shape alone: TALO, TARO,
  TERO and TORO all mapped to `tru` 三 (239×), MASA to `msa` 說 (652×), OKAN to
  `uqan` 153×, DAWAI to `dawi` 懶惰, DASI to `dsi` 帶, DUKA to `dka` 一半, QEPI to
  `qpi` 壓縮. Four Japanese given names became the numeral 3. This is the `_sogi`
  failure mode (杉 adjudicated to `sgi`, which glosses 去…分配) recurring in the one
  population where the tier's evidence is structurally absent, so the guard is now
  documented in `llm_map.json`'s `_names` key. Two survive: TALO/TARO keep `taru`,
  which is 6× in speech and carries no gloss in either wordlist — which is what a
  name looks like — and QAYO keeps `kayu`, because `kayu` glosses 木製湯碗, exactly
  his 容器－盤子－碟子, so it serves the common noun sharing the token. The other
  eight are dropped: five fall to tier N and three go green.
- **A** (468) — generated candidate, attested + Chinese-gloss-confirmed.
- **B** (1,343) / **B-rules** (27) — unique attested candidate via safe rules.
- **T** (225) — sister-dialect triangulation: Toda/Tgdaya cognates VALIDATE which
  generated Truku-shaped candidate is right (never supply spellings directly).
  Tgdaya folds l→r, o→u, d→j/t→c before i; both sisters also indexed by
  affix-stripped cores (≥5 chars) since cognates are usually differently-derived
  forms of the same root (baxang vs qbahang). Ties broken by weighted edit
  distance using measured correspondence odds (o→u/x→h cheap at 0.2; keeping
  o/x, or l→r, expensive at 0.8 — l usually stays l in Truku).
- **P** (1,046) — root-consistency projection: a resolved family member fixes the
  stem correspondence; unresolved hw/sub/paradigm forms of the same entry inherit
  it (infix-aware: mn/um/nm/m/n after the first consonant; affixes converted by
  the near-universal rules only). Mostly unattested by definition — the point is
  inheriting a verified stem and protecting derivatives from the char rules.
- **R** (672) — relative inheritance. The other tiers test WHOLE words against the
  omnibus, so a regularly derived form of a well-attested root falls through:
  `nduk` is unattested but `mduk` 關（門、窗）and `mnduk` are right there. Tier R
  peels prefix/infix/suffix off the Pecoraro token, matches the core against
  affix-stripped cores of the omnibus (≥3 chars, ≥2 supporting glossed words),
  and reattaches the affixes through the near-universal rules. Skips rather than
  guesses when two readings survive. The gloss veto here is a *rejection* test —
  no character in common at all — not `gloss_overlap()`, which wants a contiguous
  run and so rejected nduk/mduk for stating the same thing in a different order.
- **KL** (39) — keep-l guard: tokens frozen against a wrong l→r. It works off the
  map, so a token blocked out of every tier (see `pskluyun` below) is out of its
  reach too.
- **D** (125) — morphology over an already-solved base. Lowking Nowbucyang,
  太魯閣語構詞法研究 (*Word Formation in Truku*, 2008) §3.4: Truku reduplication is
  CV- or CVCV-, and since Truku doesn't write the schwa, CV- surfaces in the
  orthography as a **doubled initial consonant** (hmadan → hhmadan "many of them
  clearing"). Same treatment for the mn-/n- AF preterite and the collective d- on
  a personal name (Aman → dAman). None makes a new lexeme, so the answer is
  (his affix) + the modern spelling of the base. Pass order is
  J → id/A/B/T → P → R → KL → S → N → D → E → G, so any of those earlier tiers can
  supply the base — except X, whose "modern" is a different word. Order matters:
  attestation must not outrank family evidence, which is why S sits below KL.
  Rules fired: CV- 52, n- 47, mn- 11, d- 6, CVCV- 4. **66 of the 120 were being
  rendered wrong** by the char rules, nearly all of them by l→r on a root that
  keeps its l: `llisao` showed as *rrisau* for `rrisaw`, `xxei` as *hhei* for
  `hhiyi`, `nk'la` as *nk'ra*, `ttunux` as *ttunuh*. Why it was needed at all:
  tier R peels affixes off the Pecoraro token but calls `peel()` with the
  reduplication flag on the **modern side only**, so a reduplicated Pecoraro
  token could never match. The collective d- requires the base to appear
  capitalized in every one of its corpus occurrences — that is the test for "this
  is a personal name". Only 3 outputs land on an attested omnibus word (they are
  derived forms; that is why they fell through in the first place), but those 3
  confirm the semantics: `mnswayi` 兄弟姊妹複數, `nseejiq` 別人的.
  Every mapping is dumped to `tools/orthography/tier_d_log.txt` with its rule,
  its base and the tier the base came from — audit that file after regenerating,
  because a wrong base silently propagates.
- **E** (146) — projection into his own example sentences. Tier P refuses example
  tokens (a sentence is mostly other people's words), which also shut the door on
  a word's own family: `kxebong` occurs nowhere but the single sentence under
  XEBONG and went on screen as *khebung. A sentence token qualifies only if it
  CONTAINS a stem the SAME entry has already resolved, and one ambiguous
  candidate disqualifies it. Log: `tier_e_log.txt`.
- **S** (60) — attestation in running speech. Same claim as A/B — "this exact word
  exists in modern Truku" — but asked of `C:/dev/ILRDF/ILRDF_texts.xlsx`: 47,517
  transcribed Truku utterances, 277,014 tokens, cached as `spoken_truku.json`. A
  dictionary skips exactly what a transcript is full of (names, particles, the
  shape an inflected root really takes). Candidates are the rule-consistent
  readings of his token, and exactly ONE must appear **twice or more** — a hapax
  in an ASR transcript is as likely to be a mis-hearing as a word. Runs AFTER the
  KL guard, and a hit that flips an l is refused when the keep-l reading of the
  root is itself a modern word: `mk'alang` matched `karang` 蟹 in speech, but his
  word is built on `alang` 部落. Log: `tier_s_log.txt`.
- **N** (142) — proper names. "Sapah Sibar u…" — Sibal is a man, and the blind rule
  renamed him. Nothing attests a name and no tier above reaches it, so it falls to
  the char rules, the one population where they are guaranteed to be guessing.
  Test: capitalized mid-sentence in one of his own examples (only a proper noun
  is) AND lowercase nowhere near often enough to be the real reading. Those keep
  their l; o→u, x→h and final -ai/-ao still apply, so `Pisao`→Pisaw,
  `Labai`→Labay, `Sibal` stays Sibal. Log: `tier_n_log.txt`. Names are never
  allowed to seed tier G.

  The lowercase half of that test used to be absolute, and one keystroke could
  defeat it: Wilang is `Wilang` nine times mid-sentence and `WILANG` once as a
  headword, and `wilang` exactly once — and that single slip vetoed the man. The
  veto now needs the lowercase reading to be more than a slip: mid-sentence
  capitals must still be ≥60% of every occurrence. Measured, that admits five
  tokens and all five are proper nouns — Wilang and Dloan (men), Taolan (a
  neighbour), Tagaxan (a place) and Taiwan. Dropping the 60% and asking only
  that capitals outnumber lowercase admits 142, led by `ini`, `ana`, `adi` and
  `malu`, which are capitalized because they begin his sentences; that gate is
  worthless, and the measurement is the only thing that separates the two.

  **2026-07-30: the tag was the evidence all along, and nothing read it.** The
  capitalisation test reconstructs "is this a name?" from statistics for words the
  digitization already labels outright — `name (m)` 137 times, `name (f)` 87 — and
  `build_modern_map.py` read only the *loan* tag. So the tier reached only the names
  he happened to put in a sentence, and l→r renamed the rest: LAKAX came out
  *Rakah, SOBIL *Subir, TOLI *Turi, SIYAL *Siyar, PILEX *Pireh, TAILONG *Tairung.
  Seeding the loop with `name_heads` took the tier from 75 to 143 and added 65 map
  entries. Two restrictions, and both are load-bearing:

  - **It runs after tier S and the `t in result` guard is what keeps it there —
    attestation outranks the freeze.** The community really does write KULAS as
    `kuras` (24×), LABAI as `rabay` (42×), LIBIç as `ribix` (11×), ASAO `asaw`
    (91×), TADAO `tadaw` (71×), UMAO `umaw` (66×). Insert the freeze above
    attestation and those men are misnamed the other way. Measured on the 15
    l-bearing tokens the seed newly reached: keep-l and with-r are *both* 0× for
    every one of them (only `lingi` has 1×, for keep-l) — exactly the population
    the tier is for.
  - **A name whose token is also another entry's headword or sub-form is
    excluded.** Truku names ARE nouns — LONGAI 猴子, XALONG 松樹, PALAS, KALAO,
    BANAX 紅色 — and there the noun is the entry carrying the gloss, so freezing
    its l would break the word for the sake of the name. 30 of the 270 name tokens
    are in this class and they keep the noun's spelling; one bare token cannot
    render two ways. `name (.., jp)` is excluded too: his Japanese romanization is
    a different system (tier J: "his Japanese o stays o — SATO, DOKU"), so whether
    TORO is `turu` or `toro` is a question about Japanese, not about his Truku.

  **The documented `-ai/-ao` conversion had never once fired.** `keep_l` is
  o→u, and it ran *before* `endswith("ao")` was asked, so by then -ao was already
  -au and the branch was dead — the tier quietly emitted `-au`. It went unnoticed
  because tier S owns every attested -aw name, and the only -au tier N ever
  reached was `beau`, unattested either way. The tag seed makes it live (`amai`,
  `dawai`, `masai`, `tilae` are all reached now), so the order is fixed: convert
  the ending on the plain token, then `keep_l`. A dead branch in a tier that
  rarely fires is invisible until the tier's population grows.

  Names are also transliterated in Latin *inside the Chinese glosses* — "我的曾祖父
  是Arin", "是 Sipui 來勸他", "你不就是 Hlaon 的父親嗎" — a source of name spellings
  no tier has ever read. Note `"Laon` = **Hlaon**: his `"` there writes an h.
  Nothing attests `hlaun`, so it was left alone, but that is evidence about the
  elision mark, not about this name.
- **G** (24) — root projection ACROSS entries. Tier E only sees the entry a token
  stands in, and words don't respect that boundary: `mptgamil` occurs once, in a
  sentence under GABAL 拔, so nothing in its own entry could say that GAMIL 根 is
  right there resolved and keeps its l — it rendered as *mptgamir. Being global it
  is held to a much higher bar than E: the seeding root must be corpus-vouched
  (no projected tier may seed another projection, and no name), ≥4 chars, unique;
  the stem pair must be a letter-for-letter **correspondence** (only the attested
  swaps o/u l/r x/h k/q d/j t/c e/i — Pecoraro's MALO also surfaces as `nalu`, and
  reading n/m as orthography projected *mpamalu); prefix ≤3, suffix ≤3; only
  example-sentence tokens are eligible, never a form Pecoraro filed under a root
  of its own; the local root wins over a foreign one at equal length (`qalip` is
  KALIP 剪, not QALI 話); and it must actually **disagree** with the blind
  fallback, or it says nothing and the token stays honestly green. Log:
  `tier_g_log.txt`.
- **V** (18) — elision-mark variants. His two marks put the same word in two map
  keys (`wordKey()` folds `" → '` but does not remove it, so `L'QDO` and `LQDO`
  are different keys), and the passes then answer them separately: TNQDO's tag
  `(= R. ? - R. = L'QDO ?)` printed a green RQDU beside the brown RQDUG of the
  entry it points at. Two directions, both requiring the twins to agree on ONE
  value: an **unmapped** token inherits from its twins, and a token sitting on a
  **machine** value (R/D/P/E/G/B-rules/C-review) is overruled by a hand-verified
  (M) twin. The second is why `mg'li` printed *mgli beside the verified
  `mg'li"` → mgrig 跳舞; measured over the finished map, 16 twin groups hold an M
  member, 8 machine twins live in them, 5 already agreed, and all 3 that disagreed
  were the machine being wrong (`b'xgan` *bhgan for the attested brhgan 把…鎖,
  `mq'qan` *mqekan for mkeekan 打架 41× in speech). Never overrules an attested
  tier — id/A/B/S/T is evidence about the exact token in hand, which outranks a
  twin. Never a tier X key (the substitution has to declare itself on screen, and
  q'nao / sl'xeq / t'bako all have a mark-free twin that would print a bare brown
  QUSUL and bypass the disclosure), never a `lex_block` token (green on purpose),
  and never where the bare shapes disagree — for `kn'qan`/`knqan`, `p'lapa`/`plapa`,
  `wa'lo`/`walo` he is writing two different words, not one word two ways, and
  those stay green. Log: `tier_v_log.txt`.
- **W** (301) — the written schwa before a word-initial labial. A post-pass, run after
  V: it corrects values the other tiers already produced rather than reaching a token
  nothing else did, which is why the bulk of it comes from P (99 of the first 140) and
  only a handful from M. Modern
  writes the future/agentive prefix **`emp-`** (1,651 types / 2,251 spoken tokens) and
  the stative m- on a b-root **`emb-`** (201 / 1,011); his transcription drops the
  schwa, exactly as it does word-internally (`xnglyeq` → `hnegliq`, batch 25). Guarded
  per token — his form must be unattested in **both** corpora — so the
  class evidence never overrides evidence about the word in hand. Two branches:
  **`twin`** (140, batch 26) takes the e only where the e-form is itself attested;
  **`class`** (159, batch 27) takes it where nothing witnesses either form but the
  e-form's four-letter initial is one modern Truku licitly writes. Tiers **X, N and J
  are excluded**: X declares itself on screen, and N (names) and J (loans) are frozen
  populations a rule about a Truku prefix has nothing to say about — the class branch
  reached all four of `mpa`, `mpsq'lol`, `mbosi`, `mpasimpu` before the exclusion.
  Log: `tier_w_log.txt`.
- **J** (139) — the Japanese/Chinese loan stratum, romanized as a class. It is a
  **pre-pass**, above every attestation tier, because for this population
  attestation is actively misleading: modern standard Truku replaced most of the
  loans with native coinages (lumak for tobacco, mtgsa for teacher, tluan for
  table), so when a loan's shape does turn up in the modern corpus it is a
  homonym — and the more often it turns up, the more confident the wrong answer
  looked. TOKE 時計 was "confirmed" as `tuki`, which is 抵銷 (312× in speech);
  DOLI 道理 as `duri` 又 (517×); XAYA 汽車 as `haya` 這樣 (129×); MISO 味噌 as
  `misu` 你 (128×); BALAS 礫石 as `balas` 性交. Of the 63 loans the earlier passes
  claimed, seven landed on a modern word that means the right thing.
  Pecoraro himself is perfectly consistent here — across all 123 tagged entries
  there is not one loan he writes two ways. What his loan spellings are not is
  consistent with the rest of the book: he romanizes the **source** (Japanese o
  stays o — SATO, DOKU, OTOBAI) while his Truku o is modern u. Only that
  difference is corrected: o→u, his x for the source h (XINOKI→hinuki), final
  -e→-i for a vowel modern Truku has no word-final slot for (BALE→bali,
  NABE→nabi, both attested), and the two glides the modern orthography settled
  (-ai→-ay 2129:101, -wi→-uy 723:50). **l is left alone** — `bali` 子彈 keeps it,
  and l→r is guesswork on a word that was never Truku to begin with.
  Order inside the pass: an attested modern word whose Chinese gloss agrees
  (`gloss`, 9) → a curated mapping that *changed* something (`hand`; a manual
  entry that only says "leave it alone" was a verdict of "no modern form found"
  reached before the loans were looked at as a class, and is overruled) → a
  prefixed form inheriting a base resolved earlier in the pass (`base`; shortest
  first, so KENSAT→knsat makes Mkensat→Mknsat and not the rule's *mkensat*) →
  the rule. Log: `tier_j_log.txt`, with the branch each mapping came from.
  Three tag spellings mark the class, all his: `[emprunt jap./chin.]` ×121, `(J)`
  on KENSAT, `(J.?)` on BAKET. **A multi-token loan headword contributes only the
  tokens found nowhere outside the loan entries** — `Sapax kensat` "police
  station", `Tama denki`, `BALA-NO-XANA` are compounds with a native word in
  them, and taking them apart naively enrolled `sapax` (375 occurrences in the
  book), `tama` (131) and the Japanese genitive *no*, spelled exactly like the
  Truku particle `no` (210). A class pass that outranks attestation must not be
  allowed to decide those.

**Syncope.** Truku doesn't write the schwa, so a root loses its first vowel the
moment anything is prefixed: GAMIL 根 is the root but "where it took root" is
`Tgmilan`, not *Tgamilan. Testing a stem by literal containment therefore misses
a word's own conjugates — tier R reached `tgmilan` with no family to answer to and
guessed *tgmiran*. `stem_forms()` offers every resolved stem in both shapes; the
syncopated one counts only when both sides syncopate the same way, which is what
makes it a correspondence rather than a second guess. Used by tiers P, E and G.

**No diacritic ever leaves the generator.** A modern spelling is written in the
modern alphabet, so `plain()` (ç→x, marks stripped) runs over every tier's output
before either file is written. The app cannot repair this itself — a map hit
short-circuits `charRules()`. `charRules()` covers the unmapped remainder, and
folds `ł`/`ʔ` explicitly: they are letters, not letter-plus-mark, so NFD leaves
them standing.

**No vowelless modern word leaves it either.** Truku writes no schwa, but every
modern word still has a written vowel, so an output with none is a rule that ran
out of evidence, not a spelling: SK'LÖT 勒得很緊 came out `skrut`, which is nowhere
in any corpus (that sense is the `bsqur` family now, a different word). The gate
drops any non-X mapping whose value has no `aeiou` and returns the token to green.
It must NOT require the *input* to have a vowel — he writes the schwa as `'`, so
`sk'l't` and `sb'l's` have none either, and `sb'l's` is the real `sblus` 不鹹.

**The generator is deterministic.** It was not: three runs on identical inputs gave
different output, and `gmagwi` flipped between `gmeeguy` and `ggmeeguy` run to run.
String hash randomization varies `set()` iteration order, which fed length-only
sorts whose first match then `break`s. Every `for … in set(…)` is wrapped in
`sorted()` and all three length-only sorts have a total key
(`key=lambda x: (-len(x[0]), x[0], x[1])`). Keep it that way: auditing a change by
diffing modern_map.js is worthless without it — a "regression" can be a coin flip.

His **root tags are in the token census** (`take_tag`, gating exactly as `tagHtml`
does: no root mark means it renders as plain grey French and is not Truku). 443 of
1,850 tags qualify and they hold 103 token types no other field has — nearly all
his own bracketed variant spelling of the headword. They join `tokens` only, never
a family: a bracketed spelling he is unsure of is not an inflection, so it earns
attestation and elision-twin evidence but must not seed a projection. And only as
**new types** — bumping the count of a token the census already had re-orders the
frequency walk and flips decisions elsewhere in the book (it cost two correct
tier-E readings, `gmagwi` → *ggmeeguy and `pgleqe` → *pgliqi).

Pecoraro has **two** elision marks, `'` and `"` — 181 word types / 400
occurrences carry the `"`, whole paradigms use it consistently (T"TO, SBU",
G'LI", "LU), he brackets the pair as variants himself (`MA'GUL (M"GUL ?)`,
`TLA'TO (TL"TO)`), and single tokens carry both (`g'li"`). It is not a shift-key
slip: `"` is word-initial 161/401 times where `'` almost never is, and it follows
a capital LESS often than `'` does. `wordKey()` folds `" ’ ʼ ʔ → '` for lookup,
and `charRules()` must fold them on OUTPUT too — without that an unmapped token
kept whatever glyph he typed and `wa"lo` reached the screen as modern `WA"RU`.
The `"` that remains on screen is inside gloss fields (212 occurrences), which
are never modernized by design; some of those are genuine French/English
quotation marks and some are Truku words quoted in a definition.

## The spoken corpus — how to widen it (2026-08-02)

`load_spoken()` now reads the ILRDF collections twice: the flattened
`ILRDF_texts.xlsx` export, and `parquet_truku_freq.json`, the datasets read
directly. The export had lost a third of them (272,150 tokens against **361,630**,
47,517 utterances against 54,457). Batch 136 gave the wider reading to
`build_verified.py`, which only asks *does this string occur*; batch 137 gives it
to the tier that decides which spelling is right, which is the larger claim.

Two rules govern any future widening, and both were learned by breaking something.

- **MAX across readings, SUM within one.** The xlsx is an export *of* the
  parquets, so adding the two counts every shared utterance twice — and that
  breaks the only gate that matters, since a word occurring once would show 1+1
  and clear the `>= 2` bar built to reject exactly that hapax. Within the parquet,
  two plain types can `norm()` to one key (`q'mpah`, `qmpah`) and those *are*
  separate occurrences, so they sum.
- **The `>= 2` bar is universal, and it is load-bearing hardest where a hit
  SUBTRACTS.** Tier W's veto (`his form is itself modern Truku, so no e-form`) was
  ungated, and one new transcript token was enough to strip an attested spelling
  and hand the word back to one nothing attests: `mbrinah` 1× took the entry from
  `embrinah` (35× and in the dictionary), `mpurug` 1× from `empurug`, `mphuqil` 1×
  from `emphuqil`. Gating it repaired a fourth word the *narrow* corpus had already
  broken the same way — **MBUA**, held at `mbuwa` (nowhere in the omnibus) by a
  single xlsx token, is now `embuwa` 有氣泡 over his own root `buwa` 氣泡. `LICIT`
  takes the same bar: a mis-heard token is not evidence that an initial is licit.

The other change is **MIXALASI `mihalasi` → `miharasi`**, tier N → tier S. It is a
village, and the corpus names it outright — 「故改名為 *Miharasi*。漢語翻成
「見晴」」 — Japanese 見晴らし *miharashi*, so the `l` he wrote is that word's `r`
and the name-freeze was protecting a letter that was never there. This is the
documented order working as designed: attestation outranks the freeze.

Measured: 0 keys added or removed, **2 spellings changed**, 7 relevelled with the
same value (6 E→S, 1 N→S — an inference becoming a direct attestation, which is
what more evidence should do). verified.js +2 / −1 / **0 weaker**. DOM census
94.1280% → **94.1347%** dark (41,854 → 41,857; pale 2,579 → 2,576; green 32),
1,967 cards, 0 page errors in both spelling modes (`census137.py`).

## The names have a register, and it is digitized (batch 138, 2026-08-02)

**No wordlist has a reason to hold a personal name.** That is why tier N was the
one population where every spelling was a guess and every word stayed pale
permanently — "unverified" is a uselessly permanent verdict about a man's name.
The Council of Indigenous Peoples publishes the register:

    https://indigenous-name.ilrdf.org.tw/#/searchView?zuqunId=13&zuName=太魯閣族

**1,792 Truku names** (男名 928 / 女名 614 / 男女共名 258) and 461 Seediq, 162
shared, each with its type and a recording of a speaker saying it. It is a Vue
SPA over a JSON API and the page holds no data, so `fetch_ilrdf_names.py` posts
to the API the page posts to — `POST /api/api/EthnicLanguageData/GetFirsrWordList`
with `{FirstWord, EthnicGroupId, page, pageSize, NameTypes}`, EthnicGroupId 13 =
太魯閣族 and 10 = 賽德克族. There is no "all names" call, so the harvest walks the
initial-letter index the bundle's own `keyboardFirstName` defines; `o`, `x` and
`ʼ` come back empty for Truku, which is that alphabet's answer and not a gap.
The output is committed to `ilrdf_names.json` and **the build must never depend
on the network**.

`build_verified.py` widens `seen` with it at level 1 (LISTED), exactly as it does
with the parquets, and — like them — **never widens `lex`**: a name is not a
root, and handing 1,792 of them to the affix analyser as lexemes is the mistake
that re-cut `spsangay` onto `sang`.

**The gate is the design.** The register is matched only against the values the
NAME POPULATION puts on screen, exported by the map builder as
`name_population.json`: his own `name (m)`/`name (f)` tags (with tier N's two
restrictions already applied — no `name (.., jp)`, and no token that is also some
entry's headword) **union** tier N itself. The union is needed in both
directions: `tatu`, `aman` and `mici` are names he tags as such but an earlier
tier had already valued them, so tier N never fired and nothing downstream could
tell they were people. 235 tokens, 235 distinct values, **125 in the register**.

Ungated — plain string matching against 1,792 names — it would also clear **21
pale types the register lists and this page does not use as names**: `tabu` is
his 餵養 root, and `aku`, `mici`, `taya`, `urang`, `burung`, `satu`, `bulu`,
`eku`, `butang` are ordinary words that happen to be spelled like somebody. A
register of names is evidence about names. Those 21 are the load-bearing
assertion in `dom138.py`; if the gate ever reads the register as a wordlist they
are what falls first.

**Yield: 61 values / 189 occurrences turn dark**, led by `mikat` 33, `sikat` 16,
`tatu` 14, `talan` 13, `imin` 12, `tain` 11, `utun` 10. Three of them —
`masa`, `duka`, `atu` — are words the *earlier* name pass got wrong from the
other side: `llm_map.json`'s `_names` guard records MASA being adjudicated onto
`msa` 說 and DUKA onto `dka` 一半 because a name entry has no gloss to
adjudicate against. The register is the evidence that was missing then.

**Nine names the register spells differently**, applied to `manual_map.json`
under a stated rule (its `_ilrdf_names` key; `_`-prefixed keys are now filtered
there as they already were in `lexical_map` and `llm_map`, because this file's own
test — "the omnibus gloss matched his Chinese" — cannot be run on a name):
his form absent from the register, exactly one registered name one letter away,
that name's 男名/女名 type agreeing with his own tag, and the letter a
correspondence this book already documents.

| his | ours was | register | why |
|---|---|---|---|
| `lobyaq` | lubyaq | **lubyak** 女名 | q>k, his `name (f)`, 20 occ |
| `opiç` | upih | **upix** 男名 | his ç **is** modern x — tier N applied x→h to it anyway |
| `pido` | pido | **pidu** 男名 | o>u, blocked by tier R |
| `ixeng` | iheng | **ihing** 男名 | e>i |
| `sido` | sido | **sidu** 女名 | o>u |
| `pilex` | pileh | **pilih** 女名 | e>i |
| `komu` | komu | **kumu** 女名 | o>u; an identity claim overturned |
| `malwi` | maluy | **maruy** 男名 | l>r — the register overrules the name freeze |
| `tailong` | tailung | **taylung** 男名 | ai>ay, o>u |

Two of those are worth keeping in mind. **`upix` indicts the tier, not the map**:
this book's first orthographic rule is that his ç is modern x, and tier N ran
x→h over it regardless. **`maruy` is the documented order working** — the freeze
exists to stop l→r renaming a man (`Sapah Sibar`), and here the outside source
says the man really is Maruy, so it outranks the freeze exactly as attestation
does. `kumu` also brought his accented twin `komù` into agreement, which is what
tier V asks of a pair his marks split into two keys.

**What the register does NOT settle, and this is the honest half. 94 of the name
population's 235 values are still pale, 286 occurrences** — `liwis` 38, `ingay`
24, `lauken` 22, `timin` 11, `pilin` 11, `akit` 10, `atwi` 8. Twenty-two of those
have exactly one registered name a single letter away, and most were **refused**:
the edit is not a documented correspondence (`bal`→`balu`, `yiyah`→`biyah`,
`hatsu`→`hatu`), or the register's type contradicts his tag (`yageh` is his
`name (m)` and `yagih` is 女名), or two of his distinct names collapse onto one
registered name (`sipwi` and `sidwi` both sit one letter from `siwi`). The
tempting class is his final `-n` against the register's `-ing`/`-ung`
(`pilin`/`piling`, `arin`/`aring`, `apin`/`aping`, `laun`/`laung`, `pirin`/`piring`)
— **rejected**, because the register writes final `-n` freely itself: -an 115 /
-ang 136, -in 46 / -ing 112, -un 60 / -ung 105. That is a 30/70 split, not the
near-exceptionless correspondence tier W's evidence bar wants, and absence from a
register of names *in use* is weak evidence about a 1977 book.

The register is written in the modern orthography throughout, which is worth
recording as a check on the rules: 915 of its names carry `u` against 44 with
`o`, 174 carry `ay` against 4 with `ai` — but 355 carry `l` against 184 with `r`,
and 52 carry `x`. **l and x are real letters in real names**, which is the whole
reason the name freeze exists.

Measured: 0 map keys added or removed, **9 spellings changed** (5 N→M, 3 R→M, 1
M→M), 0 relevelled. verified.js **+69 keys, all level 1, 0 weaker**. DOM census
94.1347% → **94.6790%** dark (41,857 → 42,099; pale 2,576 → 2,334; green 32),
1,967 cards, 0 page errors in both spelling modes. `dom138.py`: 61 GAIN dark, 21
KEEP still pale, 3 JP and 4 MISS untouched, 9 FIX dark with all nine old
spellings gone from the page, **0 failures**. (14 of the occurrences
`census137.py` shows moving belong to commit 098b28f, whose six affix letters
postdate that script's baseline.)

**Appendix 4 reaches further than tier N does.** `site/entries.js` already holds
it — 270 name-tagged records, `name (m)` 137 / `name (f)` 87 / `name (f, jp)` 28
/ `name (m, jp)` 17 / `name (m) (?)` 1 — reaching across tiers M, R and V, well
beyond the 131 tier N had. That is why the population is his tags ∪ tier N rather
than tier N alone. **After the batch, 59 of the values his own non-jp name tags
put on screen are still pale, 190 occurrences** (measure this on the DISPLAYED
value: `modern_map.json` is `{"map": {token: {modern, tier}}}`, and a script that
forgets the `map` key silently compares his raw tokens instead, which undercounts).

## The register's ceiling, and its floor (batch 139, 2026-08-02)

Batch 138 accepted a respelling when exactly one registered name was **one letter
away**. That is the wrong shape for a correspondence set — `TAILONG` needed ai>ay
*and* o>u together and had to be done by hand — so this batch composes the
documented correspondences and re-asks, over the value each token **puts on
screen** rather than over his raw token. (A script that reads `modern_map.json`
without descending into its `map` key compares raw tokens and silently finds
nothing; that is how the first run of this measurement went wrong.)

The whole automated widening buys **two names**, and both are worth having:

| his | ours was | register | why |
|---|---|---|---|
| `sering` | sering | **siring** 男名 | e>i, the same as `ixeng`>`ihing` |
| `yagex` | yageh | **yagix** 男女共名 | **the `upix` failure again** |

`YAGEX` is the instructive one. His form already carries the x; tier N ran x>h
over it and printed `yageh`, which put it one letter from `Yagih` 女名 — and
batch 138 refused it for a type clash *the tier had manufactured*. Undo the x>h
and his own spelling is one e>i from `Yagix` 男女共名, which a `name (m)` may
bear. **When a tier's output is the thing being matched, the tier's bugs become
evidence.** Match his spelling.

Two more are reached and refused, and they are why the type-agreement clause is
load-bearing rather than decorative. `mixeng` is his `name (f)` and `Mihing` is
男名. `xane` and `lübaq` carry no tag of his at all — tier N flagged them off
capitalisation — so there is no type to agree with; and `XANE` is not a name,
it is a token in the example `ASO NA SAO'LE XANE` under his entry for the
possessive prefix **N**. `hane`>`hani` would have renamed a grammatical particle
after a man.

**The floor.** The register was asked for 氏族名 (NameType 3) and 屋名 (4)
directly, on every initial: **zero rows for 太魯閣族** — and that is not a hole in
the register. **Truku naming is 親子連名**, a person's own name followed by their
father's; clan names and house names are other peoples' institutions (屋名 Paiwan
and Rukai, 氏族名 Tsou and Saisiyat). The 1,792 harvested names are 男名 / 女名 /
男女共名 because that is all there is to have. Nothing is missing.

What is left is honestly out of reach: **58 values / 189 occurrences he himself
declares** `name (m)`/`name (f)`, plus 23 `name (.., jp)` values / 43 occurrences
that are a question about Japanese romanization, not about his Truku spelling —
`liwis` 38, `akit` 10, `atwi` 8, `apwi` 4. The register was asked and does not
know.

Measured: 0 map keys added or removed, **2 changed** (both N→M), 0 relevelled;
verified.js +2, all level 1. DOM 94.6790% → **94.6835%** dark (42,101 / 2,332 /
32; pecoraro 94.6866%), 1,967 cards, 0 page errors in both modes. `dom139.py`:
2 FIX dark with both old spellings gone, 9 KEEP still pale, **0 failures**.

## If the name is close, use it (batch 140, 2026-08-02)

Batches 138 and 139 required the edit to be a correspondence this book already
documents. **That is the wrong bar for a name.** A correspondence table is built
out of words, and a name is exactly the thing that does not have to obey one —
it can be his ear, his typewriter, or the family's own spelling. Refusing `qapi`
because e>a is not in the table left a woman unnamed to protect a rule that was
never about her.

The rule is now what actually identifies a name:

- **he declares it a name himself** (`name (m)` / `name (f)`), and
- **exactly one registered name of an agreeing type is one edit away** from the
  spelling his token puts on screen — his `name (m)` against 男名 or 男女共名,
  his `name (f)` against 女名 or 男女共名.

Nine more: `boin`>**buhin** 男名, `dado`>**kadu** 男女共名, `koxong`>**kunung**
女名, `pixeng`>**pihang** 男名, `qepi`>**qapi** 女名, `syobao`>**subaw** 男名,
`tibi`>**sibi** 男名, `unaq`>**unaw** 男名, `xatsö`>**hatu** 男女共名.

**The tag requirement is what makes closeness safe.** A token tier N flagged off
capitalisation has no type to agree with, and `xane` is why that matters: it is
one edit from `Hani` 男名 and it is not a name at all — it is a word in his
example `ASO NA SAO'LE XANE`, under the entry for the possessive prefix **N**.
Every untagged token stays refused, `lübaq` and `hane` included.

**Where "close" identifies nobody, nothing is chosen.** `akit` has six agreeing
names one edit away, `sidi` six, `uding` six. `ingay` — 24 occurrences, the
heaviest name in the book — has three, and all three are 女名 against his
`name (m)`. His spelling stands.

**The -Cwi set is refused as a set.** ATWI, APWI, SIDWI, SIPWI are four of his
names sharing a shape the register does not have, which reads as a convention of
his rather than four separate slips — and SIDWI and SIPWI would both land on
`Siwi`, collapsing two names his book keeps apart. `atwi` has a unique agreeing
match (`amwi`, 8 occ) and is still refused on that ground. One name is worth
having; a distinction is worth keeping. Contrast `qapi` and `unaw`, where two of
*his* spellings land on one registered name: there an outside source says they
were always one name, which is the opposite situation.

Measured: 0 map keys added or removed, **9 changed** (7 N→M, 2 R→M), 0
relevelled; verified.js +7, all level 1 (two of the nine values were already on
the page). DOM 94.6835% → **94.7037%** dark (42,110 / 2,323 / 32), 1,967 cards,
0 page errors. `dom140.py` 0 failures; `dom139.py` and `dom138.py` both still 0
(dom138's `unaw` expectation raised 1→2, because batch 140 put his UNAQ on the
same registered name).

Still pale and now genuinely out of reach: **49 values / 180 occurrences he
declares `name (m)`/`name (f)`** — `ingay` 24, `akit` 10, `atwi` 8 — plus 23
`name (.., jp)` values, which are a question about Japanese romanization.

## The root is listed, and nobody ever glossed it (batch 141, 2026-08-02)

`regular()` asks two things of a root and needs both — is it listed, and does
its gloss agree with his Chinese. For **138 types / 223 occurrences** the first
answer is yes and the second cannot be asked at all: `attested_gloss.json` holds
nothing for the root. That is a hole in the **gloss table**, not a verdict on
the word, and this project had already convicted the same hole twice by name —
`qriban`, and `ttmaan` in `inflection.py`'s HAND_NOT_ROOTED note ("what stops
regular() reaching it is that `ttmaan` carries no gloss, which is the listing
gap, not a morphology gap"). Most of a paradigm is glossless; the wordlist
glosses a citation form and leaves the slots bare.

So `Inflection.unglossed_root()` asks the paradigm instead. `ptbgi` is the
shape: `tbgi` is listed and bare, `tbgan` 養家畜的地方 is listed too, and his
gloss is 託人餵養－使人餵養 — agreeing on 養. The root's own inflection speaks for
the root.

**It cannot reopen the SISUN trap**, which is the first question to ask of any
rule that touches roots. SISUN's root `sisi` HAS a gloss — 用來濾酒的工具, the
rattan wine strainer — so `regular()` reads it, refuses on it, and the value
never arrives here. This rule fires only where `self.gl.get(root)` is empty.

The chain is exactly `vouched_root()`'s length — one affix step to a root, one
paradigm step from the root to a supporter — so it carries that method's guards
verbatim: slot-only Chinese, four-letter root floor, root unfrozen, `derived()`
yielding two DISTINCT affixes, whole/VSUF final-vowel witness. Its one stronger
respect is why it sits a level **above**: `vouched_root()`'s root is a
hypothesis, this one is a word the wordlist prints. Emitted level 4;
`vouched_root`→5, `sistered`→6, `syncopated`→7, `chained`→8, `affix`→9.
Renumbering is free because **`app.js` only tests membership** of
MODERN_VERIFIED (`hasOwnProperty`), never the number.

**26 values, read one by one, six pinned** in `HAND_NOT_UNGLOSSED`. All six
fail the same way, and it is the only way this kind of agreement can fail: the
shared character is not a word but a **particle**, and no gate can see that,
because a particle is a character like any other.

- `psqpahan`/`psqpahi`/`psqpahun` — his （主動）地黏貼－使黏附 against `qmpahan`
  工作的地, agreeing on 地: the ADVERBIAL 地 against the 地 that means ground. He
  has two roots here and they are not one, QPAH 工作 and SQPAX 黏貼. Right
  letters, wrong word — SISUN exactly.
- `mttama`/`tmtama` — 坐著的人／靠著休息 against `pttama` 守著, on 著, the aspect
  marker. All three glosses wear it and none of them means it.
- `mrbuq` — his 呈凹陷－形成凹穴 against `trbuq` 形容坑洞深, on the 形 of 形容, the
  head the wordlist writes before a gloss that DESCRIBES, same class as the 用來
  already in BOILER. Both readings really are hollows, so it is pinned rather
  than remapped: **the answer is right and the argument for it is worthless**.

Requiring a two-character RUN instead of a hand list was measured and refused —
it costs 14 of the 26 to save these 6, including `qnriqani` 恨, `trgrig` 舞,
`smbrinah` 回 and the three `pllg-` 動, every one a single character that IS a
word.

Measured: 0 map keys changed; `verified.js` **+20 keys, −0** (`matrima mlxan
msbrinah msparu mstama mtrima pjiyan pllgan pllgi pllgun pntrilun pqpahan psuqi
ptbgi qnriqani smbrinah spqnaqih spqpah sruciqun trgrig`). DOM 94.7037% →
**94.7892%** dark (42,148 / 2,285 / 32), original mode 42,621 / 2,309 / 32 =
94.7934%, 1,967 cards, 0 page errors in both. `dom141.py` 0 failures;
`dom138.py`, `dom139.py`, `dom140.py` all still 0.

## 大 and 小 are meanings, and STOP had swallowed them (batch 142, 2026-08-02)

`STOP` states its own test in its first line — "characters that carry no
meaning on their own, so sharing one is not agreement" — and then lists **大 and
小** among the pronouns and particles. Big and small are meanings. They were
swept in with the function words and then silently refused the two adjectives a
Formosan wordlist glosses most often: `paru` IS 大的 and `bilaq` IS 小, so his
使自己變小者 could not agree with 小 and `msbilaq` stayed pale.

Measured alone: **+10 values, 0 de-verified, 0 relevelled**. Eight are his own
word for big or small (`mkparu` 長大 / `paru` 大的, `msbilaq` 使自己變小 / `bilaq`
小, `tbilaq` 確實小, `skparu` 用以使…長大, `psblaqan`/`psblaqi` 使之變小, `knblaqan`
渺小 through the syncopated `bilaq`, `empsparu`). Two are coincidences, pinned in
the new `HAND_NOT_REGULAR`: `knslaan` 饑餓虛脫 against `sla` **大**外衣, and
`mkpakaw` 位於荊棘叢中的 against `pak`+`-aw` 老鷹抓**小**雞的動作 — whose RIGHT root
is sitting beside it, `pakaw` 有刺的野草, his gloss exactly, sharing no character
with him at all. That is the whole reason `_agrees` is a proxy and not a
measure.

**人 was tested identically and REFUSED**, though it fails the same "carries
meaning" test. In these two wordlists it is overwhelmingly a FRAME — 使人X "make
someone X", X的人, the agent nominalizer — and dropping it buys 9 of which the
first read is the proof: `pngraq` 使人變傻 agreeing with `ngraq` 比女**人**陰蒂的手勢.
上 likewise: +13, but `mtama` 當**上**父親的人 agrees with `tama` **上**帝 on a verbal
complement, and it would have let `mttama`/`tmtama` back in through a second
door batch 141 had just shut. 下 and 中 alone buy nothing at all.

DOM 94.7892% → **94.8319%** (42,167 / 2,266 / 32), original 94.8356%, 1,967
cards, 0 page errors both modes. `dom142.py` 0 failures; 138/139/140/141 all
still 0.

## Seven prefixes his book uses and PRE had never heard of (batch 143, 2026-08-02)

313 pale values find no root at all, and for some the reason is not a missing
root but a missing PREFIX — `roots()` peels only what `PRE` lists, so
`empaqsiya` was an unanalysable eight-letter string while `qsiya` 水 sat one row
away. Seven were priced alone, then together: `empa` `pkp` `spk` `sps` `npk`
`dmp` `emb` → **ADDED 14, REMOVED 0, RELEVELLED 3**. `psp` was priced the same
way and gave 0, so it is not in the list — a prefix earns its row by taking a
word, not by looking plausible.

**empa- is "will become X"**, which is what makes the group defensible on
meaning and not just arithmetic: `empaqsiya` 化成水 / `qsiya` 水; `empasnaw`
成為丈夫 / `snaw` 丈夫; `empaayug` 將變成溪流 / `ayug` 溪. The rest: `dmpuyas`
歌者 / `uyas` 歌; `npkrbagan` 夏天將至 / `rbagan` 夏天; `spkungat` 使消失 /
`ungat`; `spsqrinut` 使變窮 / `qrinut` 窮; `embsqrul`, `spkmalu`, `spspgan`,
`empanalu`, `empaqmpahan`.

**`pkpakux` is `pkp`+`akux` 翻, NOT the 老鼠 `pakux`.** One letter-string, two
readings, and only one is 翻 — the same split batch 142 pinned `mkpakaw` for
landing on the wrong side of. Nothing here reaches `mkpakaw`; `dom143.py`
asserts it stays pale.

`sgasut` came in at level 3, not through a new prefix: the widened `PRE` grew
its supporter set past the two-affix guard so `vouched()` could speak. `gasut`
is 工作範圍（工作的起點及終點）against his 照計畫、照正常程序進行.

DOM 94.8319% → **94.8859%** (42,191 / 2,242 / 32), original 94.8890%, 1,967
cards, 0 page errors both modes. `dom143.py` 0 failures; 138–142 all still 0.

## Pale is not a verdict a person's name can shed (batch 144, 2026-08-02) — **95% passed**

The name path had two gates in series and only one was doing the work. `named`
was the NAME POPULATION — his own `name (m)`/`name (f)` tags plus tier N's
"capitalized mid-sentence, never lowercase anywhere" — intersected with the
ILRDF registry. The docstring defended the intersection with the homograph trap
(`aku`, `taya`, `urang`, `tabu` are somebody's name AND ordinary vocabulary),
but **those are kept out by the population, which never held them.** The
registry was answering a second question — "and is this the modern spelling?" —
that three classes of name can never be asked:

- **Japanese-era loans** `denki` 電気, `banasi` 話, `stbaku` 煙草, `tausen`
- **place names** `tagahan` (他從Tagarhan出發), `taulan`, `tyakang`
- **Christian names** `jes` (Jes Cristo — *Notre Seigneur Jésus-Christ*), `maria`,
  `dcristu`, `yurdan`

No register of Truku **given** names will ever hold one, so requiring one kept
them pale forever on a test they cannot pass. So the registry now only REPORTS
(140 of 247 values) and the population is the gate; HAND_NAMES joins it.
**+82 values / 313 occurrences, 0 de-verified, 0 relevelled.** The heaviest pale
words in the book were all people: `liwis` 38 (里維斯), `ingay` 24, `lauken` 22,
`tagahan` 13, `pilin`/`timin` 11.

**What the intersection had been silently filtering, now `HAND_NOT_NAMES` by
hand** — 16 values, because at midcap=1 tier N's evidence is one capital letter.
Six are FRENCH out of his own glosses ("Beau père", "1) Grand père", "=
Grandeur - taille", "Vivant - mobile") and were then run through o>u, which is
where `cunnaissance` (connaissance) and `ruugeur` (rougeur) come from — **the
respelling is itself the proof they are not Truku.** `mpa` is his own prefix
card. The rest are ordinary words wearing one capital: `byeqay` a verb starting
a sentence, `qlap` an imperative after a semicolon, `yianu` his form label
*Yiano* "Pour vous", `pnsdahung` a nominalized verb, and four queried variants
in parentheses (`mnttlaqel`, `mpsqlul`, `tbasyaq`, `tsaleh`). A midcap>=2 floor
was measured as the alternative and REFUSED — blunt enough to drop `maria`, and
it keeps `mpa`.

**dom138/139/140's KEEP and MISS sets are superseded, not deleted.** Those
batches refused to RESPELL a name onto a register entry, and every one of those
refusals still stands — nobody was renamed and the -Cwi set was never collapsed.
They are dark now wearing HIS spelling, which is what the refusals protected.
Each file keeps the assertion inverted as `SUPERSEDED_144`, so a revert shows up.

DOM 94.8859% → **95.5898%** (42,504 / 1,929 / 32), original 95.5852%, 1,967
cards, 0 page errors both modes. Types: 5,219 dark of 6,566 = 79.485% — the
token figure is the one the target tracks. dom138–144 all 0 failures.

## A sentence gloss refuses no better than it accepts (batch 145, 2026-08-02)

`regular()` verifies a form by making HIS Chinese agree with the root's modern
gloss on a character. 264 pale values / 312 occurrences had no Chinese of his at
all attached to the word — the only Chinese near them belonged to an EXAMPLE
SENTENCE — so the test ran against a free translation of a whole clause and read
its silence as a disagreement.

**`vouched_root` had already written the argument, pointing the other way**: "a
sentence gloss describes a whole clause and shares a character with almost
anything", the `sktama` 已故的父親 / `kmtama` 信奉上帝 case. Too loose to license
an agreement is too loose to license a refusal. A translator writing
我們去求爸爸 owes no stem in the clause its dictionary meaning.

So `no_chinese()` enters on `slots_only` — he glossed no word here — and runs no
gloss test at all. The guards carry it: root listed **and glossed**, ≥4 letters,
gloss not merely 人名/地名, and **exactly one root candidate**, because with no
gloss nothing breaks a tie. New level 5 between 4 and 6; everything under it
renumbers, which is free — `app.js` only tests membership of `MODERN_VERIFIED`.

**SISUN is refused one step earlier than the morphology**: he glosses it 縫
himself, so the entry condition throws it out. `dom145.py` asserts it still pale
— it is what this rule would have to break to be wrong.

Six of the 139 had one candidate and it was the wrong word, all six reachable
only through an example sentence: `slungan` ← `slung` 毛線 when his own note says
**(Silong=海)**; `drnai` ← `drna` 鹿鞭 under DULUN 求; `ggitan` ← `gitu` 枇杷
under GIGIT 糾纏; `empslangan` ← `langu` 湖 under his headword SLANGAN 鏽蝕;
`mtgtmaq` ← `tmaq` 水桶樹 against 趴倒在地; `narung` ← `arung` 穿山甲 against
得獎. Pinned in `HAND_NOT_NC`.

+132 values / 161 occurrences, 0 de-verified, 0 relevelled. DOM 95.5898% →
**95.9519%** (42,665 / 1,768 / 32), original 95.9455%, 1,967 cards, 0 page
errors both modes. dom138–145 all 0 failures.

## The floor that hid vouched()'s own example (batch 146, 2026-08-02) — **96% passed**

`vouched()`'s docstring opens with `xal`: citation form 0×, his note
從未見過此簡單形式, and `pxal` 147× plus five more supporters. **`xal` is three
letters**, so `len(v) < 4` refused it on the first line. So did `niq` 存在－居住,
`rut` 重壓於上, `hdu` 完成, `yup` 吹, `pru` 引起傳染, and `muk` — whose card asks
「這會不會是以下詞的詞根：SMUK…G'MUK 蓋子」and whose question the modern wordlist
answers with nine supporters.

The floor was borrowed reasoning. Elsewhere it guards a root found INSIDE a
longer string; in `vouched()` the root is the whole word and supporters are
built by affixing it, so over-generation is what `len(set(d.values())) >= 2`
already refuses. What a short root costs is anchoring, so the floor became a
tightening: **below four letters the agreement must come from a SLOT gloss** —
Chinese he attached to the word as a word — the gate `vouched_root`,
`syncopated` and `chained` already take.

The gate keeps `rih` out (agreed with `krih` only on the 工作 of a sentence about
throwing money away) and **`nta`**, the largest pale word on the page at 20.
His NTA is **n- on the two-letter `ta` 我們, the frame of `lita` = l- + `ita`** —
right etymology, unreachable evidence: `lita` 一起, `ita`/`ta` 我們 and `nnita`
咱們的 are all in the modern wordlist and `nta` is in none of it, nor once in
361,630 parquet tokens. Klokah has it in **都達賽德克語 (Toda, d=15)** —
*Muray ku da, nta tuhuy mkan idaw pa!* — a sister dialect, not a Truku spelling.

+7 values / 25 occurrences, 0 de-verified, 0 relevelled, all at the existing
level 3. DOM 95.9519% → **96.0081%** (42,690 / 1,743 / 32), original 96.0055%,
1,967 cards, 0 page errors both modes. dom138–146 all 0 failures.

## A decoding inventory is not an attestation (batch 147, 2026-08-02)

Two new bodies of Truku turned up on this box. Both were measured; one was let in.

**In — the scripture readers.** `bible-app/src/data/bible_truku_{nt,ot}.json` are
Kari Pnsdhgan Bgurah / Smudal, 新約選讀 / 舊約選讀: 56 paragraphs, **15,338
tokens**, 2,058 types, 435 new. Edited and typeset, so unlike an ASR hapax a
hapax here is a spelling somebody stood behind — it needs no freq gate. Still a
text, so it widens `seen` and never `lex`.

**Two counting traps in those files.** Each paragraph carries six parallel
VERSIONS — tgdaya, truku, hh, xz, kjv, gnb — so walking every string in the JSON
returns **203,648 tokens, of which the Truku is 7.5%**, and offers `put` (79×),
`trap`, `nay`, `un` as Truku words. Only `paragraphs[].text` is Truku. And the
title says 選讀: these are selections, not a Bible.

**Out — the Kaldi decoder lexicon**, `kaldi_formosan_250514_Truku/graph/
words.txt`. 13,351 types, 2,040 new, worth 25 pale words. **1,918 of the 2,040 do
not occur in the ILRDF parquets at all**, and its new types are `alagn`, `alnag`,
`aalng` for alang, with `amerika`/`amerrika`/`amrika` side by side. A decoding
inventory is *required* to hold every string the acoustic model might emit — that
is its job, and it is the opposite of evidence. Admitting it would have listed
`alagn` as modern Truku.

**Checked, not assumed.** `dict_truku.json` beside them is 32,208 glossed Truku
headwords and looks like a major find — it is **100.0% already inside
`attested_modern.json`**. Its Bible companion yielded one new type. The ILRDF
Truku dialogues are all eight datasets, in since batch 136 at 361,630 tokens;
there is no ninth.

+11 values / 24 occurrences, 0 de-verified, 26 relevelled upward into `listed`.
DOM 96.0081% → **96.0621%** (42,714 / 1,719 / 32), original 96.0589%, 1,967
cards, 0 page errors both modes. dom138–147 all 0 failures.

## 房子 and 家 are the same thing and share no character (batch 148, 2026-08-02)

`_agrees` tests sameness of meaning by shared bigram, then shared character.
**That is a proxy, and the codebase already said so** — in the note refusing
`mkpakaw`: the right root `pakaw` 有刺的野草 is "his gloss exactly — and shares
no character with him at all, which is the whole reason `_agrees` is a proxy and
not a measure."

432 pale values / 742 occ were refused by that proxy, and they fail the same way
over and over: 房子 vs 住屋；家, 不容易 vs 困難的, 取代 vs 頂替－繼承, 不露面 vs
躲藏, 去警戒 vs 守衛們——守望者們.

**SYN** — a third tier in `_agrees`: 26 hand-written lines of Chinese
expressions that name one concept, each read off an actual refused pair and
carrying it in a comment.

**Every member is ≥ 2 characters, asserted at import.** STOP's lesson again: 一
is in STOP because it is inside everything, so `kingal` 一個 could never reach
SNKINGAL 單一的; two-character 一個/單一/一次 give that back without the bare 一,
and 家 stays out while 住屋 and 房子 work — one-character 家 matches inside 大家,
國家, 家人 and hands the rule a SISUN.

**A line groups what is INTERCHANGEABLE, not what is associated.** `paux` 犁田 vs
his KPAUX 翻轉 is the most expensive line NOT written — 15 occ across KMPAUX,
KPAUX, KPAUXI, PAUXUN, PKPAUX. Ploughing does turn soil; 犁田 and 翻轉 are still
not the same word, and "related if you think about it" is what SISUN punishes.

**15 of the 50 hits were unpredicted, and all 15 read correct by hand** —
`mkingal` 僅僅一次 off `kingal`, `skkuyuh` 亡妻 off `kuyuh` 太太, `prbung` 使埋葬
and `mrbung` 設下陷阱 off one `rbung` 深坑 (why the pit gets two lines: a grave is
not a snare even though the hole is), the `sblus` 變淡 family, and
`traqil`/`mtraqil` via `vouched_root`. `mkpakaw` came OUT of HAND_NOT_REGULAR.

+50 values / 101 occ, 0 de-verified, 2 relevelled. DOM 96.0621% → **96.2892%**
(42,815 / 1,618 / 32), original 96.2858%, 1,967 cards, 0 page errors both modes.

## A glossary may say what a text may not (batch 149, 2026-08-02)

Batch 147 found `dict_truku_bible.json`, checked its SPELLINGS against
`attested_modern.json`, found them already there, and moved on without reading a
single gloss. That was the whole value of the file.

**A corpus and a glossary answer different questions.** 147's rule — a text can
say a string occurs, never what it means — is why the scripture readers widened
`seen` and nothing else. This is 2,033 headwords with Chinese and English
definitions, edited and published for this dialect, and meaning is what a
wordlist is FOR. It is loaded as `self.bgl` and read by `_gloss()`.

**It answers what bucket D was actually full of**: not his Chinese disagreeing
with the root, but the wordlist giving the root one sense and it being the wrong
one — `tama` 上帝 → 父親；天父 (his SKTAMA 已故的父親 is 11 occurrences alone),
`pajiq` 人名（女）→ 蔬菜, `kari` 挖掘 → 話語, `rusuq` 卵子 → 水滴；淚珠, `putuh`
人名 → 斷絕, `saw` 希望，但願 → 像；如此.

**Additive, never replacing**, so it can only turn a refusal into an agreement —
0 de-verified, a property rather than a hope. **Where the property broke, the
change was reverted**: routing `no_chinese()`'s candidate filter through
`_gloss()` looks obviously right (NAMEGL exists for roots glossed 人名, and
`pajiq` is the root it was wrong about) but that rule refuses on AMBIGUITY, so a
second gloss source creates ties as well as candidates — it cost `mtbrinah`,
`mkphing`, `mnksaw`, `tnklai` and six more to buy 7 occurrences. The ten are
asserted DARK in dom149. A second opinion may say what a root means; it may not
make a rule less sure WHICH root it is.

It glosses neither `sisi` nor `paux`, so it cannot reopen SISUN or the `paux`
family — a property of the file, pinned from the DOM. `pnnaki` resolves to
`nanak` 獨自, the guess Pecoraro pencilled into his own entry; the `kray` family
is told apart from the basket `kray` 背蔞 by `knkrayan`/`pskrayun` 堅; and
`empkhuway` has two sources that never saw each other agreeing on 治癒 against
the wordlist's 慷慨.

**A pin that names one cause must be retired when a second cause appears.**
dom147 asserted `mskingal` pale as proof Kaldi stayed out. Batch 148's SYN
reached it legitimately via `skingal` 專一, so the assertion was stale for a
batch; leaving it in would have made a real gain read as a contaminated source.

+37 values / 64 occ, 0 de-verified, 32 relevelled. DOM 96.2892% → **96.4331%**
(42,879 / 1,554 / 32), original 96.4325%, 1,967 cards, 0 page errors both modes.

## Fix the glosses before writing the synonyms (batch 150, 2026-08-02)

Twelve more SYN lines, read off the same refused bucket as batch 148's — but
read AFTER batch 149 gave every root a second gloss, which is the cheap way
round. 149 removed from that bucket the pairs that were never a synonymy problem
at all: `tama` was not 上帝 written another way, it was the wrong sense. Had
these been written first, several would have been synsets papering over a
wordlist error (犁田 for `paux`, 卵子 for `rusuq`, 人名（女）for `pajiq`) — and a
synonym table is exactly where that mistake is invisible, because a bad line
looks like a good one until someone re-reads the source.

**One line can be worth a whole paradigm.** 下坡 下來 下去 下山 cleared
`tbuyun`, `tbuyan`, `tbuyi`, `ptbuyun`, `ptbuyan`, `ptbuyi` and `tmnabuy` — the
syncopating `tabuy` 下來 paradigm, refused because he writes its slots 下去－奔下
and 使下坡. Six of the seven arrive through `syncopated()` rather than
`regular()`, so a synset pays off in rules far from the one it was written for.

Rules unchanged and still asserted at import: members ≥2 characters, and a line
groups what is INTERCHANGEABLE, not what is associated. `paux` still refused —
and the Bible glossary declines to gloss it at all, so nothing has appeared to
change that reading.

+22 values / 34 occ, 0 de-verified, 3 relevelled. DOM 96.4331% → **96.5096%**
(42,913 / 1,520 / 32), original 96.5082%, 1,967 cards, 0 page errors both modes.

## A pin comes down when evidence overturns it, not when the rule tires (batch 152, 2026-08-02)

`paux` was refused for four batches. The wordlist glosses it 犁田, to plough;
his family is 翻轉, to turn over; batch 148 declined to write the synonym line
and 149 and 150 each re-checked and left it standing. That was correct every
time, and the temptation each time was to widen SYN by a hair and take the 15
occurrences.

What actually moved it was looking somewhere else. The same wordlist prints
`mknpaux` 反過來 and `mspaux` 會翻 — **the root's own paradigm, saying plainly
what its headword gloss said narrowly.** Ploughing is turning soil over. The
gloss was not wrong, it was one sense of the word, and no amount of re-reading
the synonym table was ever going to show that.

Two things follow, and they are the reusable part:

- **A citation gloss and a paradigm are not equal evidence.** One is an
  editor's choice of a sense to print; the other is the same source writing the
  root out across its slots, and a wrong sense cannot survive all of them.
  `outvoted()` is that principle as a rule, and it is deliberately a SEPARATE
  rule a level below `unglossed_root()` rather than a relaxation of it — rule 4
  asks the paradigm where the gloss table is silent, this asks it where the
  gloss table speaks and rule 2 has already refused what it said. Different
  claim, different level.
- **Overriding evidence costs more than filling a hole.** The bar is two
  independent inflections agreeing, or one agreeing on a whole two-character
  word. One voice found 37 roots; two found 13, and the 24 dropped were
  coincidences — `qdriq` agreeing 的人 out of 住在Driq 的人, `taril` agreeing 方
  out of 地方. A single shared character is a fragment, and often a fragment of
  a fragment. The bar even splits one family: `kmpaux` carries two of his
  glosses and hears two supporters, `kpaux` carries one and stays pale.

And the trap got stronger rather than weaker. Every rule since 145 has had to
say why it cannot reopen his SISUN 縫, and the answer was always that the value
never arrives — `sisi` is glossed, so rule 2 reads it and refuses it. This rule
fires precisely BECAUSE the gloss disagrees, so `sisun` arrives for the first
time, is asked, and is refused on its merits: no inflection of `sisi` agrees
with 縫 either. **A refusal that survives being asked directly is worth more
than one that was never reached**, and dom152.py asserts it by calling
`outvoted("sisun")` rather than by trusting the entry condition.

+20 values / 53 occurrences, 0 de-verified. 96.5771% -> **96.6963%**.

## A rule that does not do what its log says (batch 154, 2026-08-02)

The bar above is described everywhere — in this file, in the docstring, in
dom152.py — as **two independent supporters must agree**. The code counted
distinct agreement STRINGS:

    agree = {sh for _, sh in sup}
    if len(agree) < 2 and not strong:

Those come apart in precisely the case where the evidence is strongest.
**Unanimity collapses to one item.** `siyang` 肉 had three inflections answering
his 養肥 — `ksiyang` 肥, `msiyang` 很肥;結實, `pksiyangay` 使肥大 — all on 肥, so
the set held one string and the rule refused. Three voices saying one thing
scored below two voices saying two things, and the root went onto the list of
questions only a speaker could settle. `len(sup)` is the whole fix.

Two things worth carrying forward:

- **The coincidences were never at risk, which is why the change is a
  correction and not a widening.** A coincidence is one supporter matching one
  fragment (`taril` on the 方 of 地方), and one is one however it is counted.
  All eight genuine ones stayed pale across the rebuild; dom154.py asserts them.
- **dom152.py had to be edited, not just superseded.** It listed 17 values as
  "the coincidences the bar cost" and nine of them were the miscount, so the
  file was asserting a wrong claim as a passing test. A log that documents a
  measurement is worth exactly what the measurement was; when the measurement
  turns out to have been of something else, say so in the file rather than
  letting the next batch inherit it.

Two hand pins in the new `HAND_NOT_OUTVOTED`, both the particle trap: `tnbusan`
(right answer, agreeing on the 去 inside 過去) and `mhmadan` (wrong answer,
agreeing on the 成 of 成為). Neither character goes into STOP — they are
worthless only as the frame verb of a gloss, the shape batch 142 measured for
人 and refused to drop.

+13 values / 25 occurrences, 0 de-verified. 96.7255% -> **96.7817%**.

## The freeze gates spelling; ambiguity means two roots (batch 163, 2026-08-02)

Two guards were asked what they were actually guarding, and neither answer was
the one the code was giving.

**`outvoted()` — `self.frozen` is the NAME freeze, and this rule asks about
MEANING.** The freeze exists so l→r cannot rename a man (batch 21's `Sapah
Sibar`), and tier N in `build_modern_map.py` is what enforces that on the page.
Nothing in `outvoted()` can respell anybody — the root is being asked what it
MEANS and the answer only ever decides a colour. So a frozen root whose citation
gloss reads *only* 人名 is now admitted, because **"this is a name" is not a
sense a derived form inherits**, which makes it the one citation gloss a paradigm
cannot be outvoted *by*. `banah` is cited 人名（男）with 27 derived forms glossed
紅 (`embanah` 紅色的, `kbanah` 染紅, `knbanah`, `gmbanah`) against his `mabanah`
將要變紅; `tasaw` is cited 人名（男）with `mtasaw`/`pgtasaw`/`sgtasaw` all on 清.
Same distinction as batch 156's `lex` (may be printed) against `voices` (may be
heard), one level further out.

The root floor drops 4→3 in the same rule, for the reason batch 146 gave
`vouched()`: elsewhere the floor guards a root found INSIDE a longer string,
while here over-generation is already refused by the two-distinct-affix and
supporter bars. It buys `pix`, whose **citation gloss is 山羊的叫聲** — a goat's
bleat — outvoted by `mapix` 壓在其上－按壓, `empapix` 被壓垮的 and the supporters
`pixi`/`mnpix`/`pixan`, every one 壓. The fourth time a citation gloss has lost to
its own paradigm (`paux` 152, `siyang` 154, `liwaq` 157, `seesu` 159), and the
first where no synonym table could have reached it.

**`no_chinese()` — a tie needs two ROOTS, and these were two SPELLINGS.** The
rule refuses when more than one root candidate survives, because with no Chinese
of his there is nothing to break a tie. But **the wordlist files a paradigm's
cells as separate headwords**, so `pnsblaqan` reaches `blaq`, `blaqa`, `blaqan`,
`blaqi`, `sblaqa`, `sblaqan` and `sblaqi` — one lexeme found seven times over.
Whichever is picked the answer is the same word. `root_groups()` partitions
candidates by containment, before or after one paradigm suffix is peeled off
either side (a suffix difference is a SLOT difference, not a root difference),
and the rule needs exactly one GROUP. Containment alone gives 44 types;
suffix-aware collapse gives 57.

**The load-bearing half is the eleven that still refuse** — `kngusan` [kgus,
ngus], `stmaqun` [taqi, tmaq], `ptbnuun`, `ppdsun`, `gmnaliq`, `kmkmalu`,
`empsneanak`, `knkmuyuh`, `nkmuyuh`, `sneelug`, `psmkun` — two roots apiece,
which is what the guard was written for, asserted pale in `dom163.py`.

**Seven hand pins, each read against the sentence he prints it in**, the same
method and the same failure as batch 145's six: one candidate, and it is the
wrong word. `mslangan` (BMBANG 鐵皮－鐵桶, rust on tin — `empslangan`'s own
sibling, not `langu` 湖), `snpsaran`/`snpsarun` (PUSAL 更新／成雙－加倍, his TWO
root, not `sari` 芋頭), `sbuwai` (把書交給, not `buwa` 氣泡), `shnkan` (`sapah
shnkan` = 監獄, not `hnka` 便宜), `psnluun` (SN'LO 傳達／傳遍各處, not `luun`
將會省著用), and **`tmukan`, which is the price of the widening and is named as
such**: the only one of the seven the group collapse reached rather than the old
one-candidate guard, standing in TUYOQ 唾液－吐口水 (他們全都朝他的臉吐了口水)
against `tuki` 抵銷／點鐘；小時 — precisely the Japanese 時計 loan-homograph tier J
was built around, where "the more often it turns up, the more confident the wrong
answer looked".

**Two kept after the same scrutiny.** `nhnaan` ← `hnaa` stands in 澆我們種的花,
newly-planted, and `hana` 剛剛 IS that lexeme; `mnkbubu` ← `kbubu` is his own
bracketed variant `mnqbobo (mnkbobo ?)` in 戴著帽子就進了我家, the hat `qbubu`.

**One arrival flagged rather than defended.** `pnsblaqan`'s root `blaq` is glossed
松鼠;老鼠;…碎粒, a homograph — the source is his BLAEQ 幸福 / `bilaq` 小 family, and
batch 142 already verified `psblaqan`/`psblaqi` off `bilaq` 小. The morphology
lands on a real listed paradigm either way, so the value stands and the odd gloss
is recorded rather than left looking like evidence.

+53 values / 60 occurrences, 0 de-verified, **0 new pale types**.
97.0986% → **97.2335%** (43,231 / 1,198 / 32).

## A worksheet row reports the ANALYSER, not the book (batch 170, 2026-08-03)

`logs/dom170.py`. Sheet 1 row 4 filed seven pale occurrences under `bus`
蒸氣洩出聲（擬聲詞）and not one of them belongs to it. That is not a printing
accident and the sheet is not at fault: **the sheets are generated from
`roots()`, so a row shows where the analyser cut the word.** `knsbusan` (his
SIBUS 甘蔗), `mbusi` and `snbusi` (his BOSI 帽子) all cut onto `bus`, because the
root each one actually needs is a root `roots()` is not allowed to see.

**Read a bad row as a diagnosis.** When a row's Chinese has nothing to do with
the cards under it, the question is not "which root is this" but "why can the
analyser not see the right one" — and the answer names a class, not a word.
Second and third instance of this on sheet 1 alone, after row 1's `dagi` and
row 3's `biyi`.

**Two blocked classes, both blocked on purpose:**

- **Root-internal syncope.** `knsbusan` needs `sibus` 甘蔗, which is listed, whose
  sisters `msibus` 甜的 / `ssibus` 很甜 hit his 甜味—甜 exactly, and whose syncope
  the language demonstrates in `psbusi` 用甘蔗來製糖. `roots()` never offers it,
  because the vowel that drops is inside the root. No gloss table can fix a root
  that is never handed to it.
- **Corpus-only loans.** `busi` 帽子 (Japanese 帽子) is real modern Truku — 7 in
  the parquets, already dark at rank 1 — and still cannot be the root of `mbusi`,
  because `seen` widens and `lex` never does. There is **no positive hand-root
  table in this codebase, only refusal lists**, and that is a design decision,
  not an omission. Do not invent one to win occurrences.

**Supply the missing argument; do not overturn the refusal.** Batch 154 had
already written down that winnowing and sifting grain are the same word, and
pinned `tnbusan` anyway because the only agreement `outvoted()` could find was
the 去 of 過去 — a particle. Batch 170 adds the SYN line 簸揚 篩榖 篩穀 篩去 and
leaves the pin standing, with `tnbsan` added to `HAND_NOT_OUTVOTED` beside it so
the pin follows the respelling instead of dying silently. **When you respell a
pinned word, move the pin.**

The line rests on his card, not on my reading: TBUS is 使用簸箕（＝**Bluxeng**）,
and `Bluxeng` is modern **`bluhing` 簸箕**, listed, 5× in the parquets. He names
the tool, the wordlist names the act. 簸箕 is deliberately NOT a member of the
line — it would reach the 43-word `giya` 小簸箕 family off a different root.

**The n-perfective drops the vowel, 22 to 1.** Of 388 CCVC roots, `-an` drops the
vowel 55 times and keeps it 45 — a coin flip. But the listed n-perfectives off
those roots take the dropped shape 22 times of 23 (`bnkgan`, `dngqan` 打鼾,
`knrtan` 手術後, `snpgan` 數過, `qnslan` 夾), the one exception being a doublet
whose root also lists the dropped form. So his `Tnbusan` is **`tnbsan`**, off the
listed slot `tbsan` 篩穀子的地方.

**And the 45 that keep the vowel are mostly sound words** — `bras` 發出「bras」的
聲音, `brut` 在「brut」聲, `bsus` 用…「bsus」刺 — which keep it because the vowel
IS the sound. That is why `tbusan` 被噴到 and `tbsan` 篩穀子的地方 are both listed
and both right, and it is the wordlist refuting the row's premise by itself.

**A cognate explains a word; it never spells one** (second statement of batch
169's rule). Tgdaya `bunuh` 帽子 is not the source of `busi`: Truku `bunuh` is
小腹, with a 26-word family and a 輪軸 sense besides. Same string, two dialects,
unrelated words.

+2 occurrences. 97.4337% → **97.4382%** (43,322 / 1,107 / 32).

## His bare -e is `i`, his -AE is `-ay`, and only one of them is a suffix (batch 169, 2026-08-03)

`logs/dom169.py`. Three refusals, no occurrences moved. All of it is invisible to
the census, which is why it is written down.

**His four word-final vowels are two systems, not four.** Measured over
`modern_map.js`:

| his | modern | n | what it is |
|---|---|---|---|
| `-e` | `-i` | ~170 | `laqe`>`laqi`, `taqe`>`taqi`, `bale`>`bali` |
| `-o` | `-u` | ~450 | `ako`>`aku`, `bato`>`batu`, `buyo`>`buyu` |
| `-ae` | `-ay` | 49 | `balae`>`balay`, `tblae`>`tbalay` |
| `-ao` | `-aw` | 289 | `asao`>`asaw`, `spadao`>`pspadaw` |

The subjunctive/projective pair is the one carrying an extra letter. Bare `-e`
and `-o` are just his `i` and `u`, so a headword in `-e` is NOT a subjunctive.

**The batch-167 rung is what makes the test sharp**, and it should be the first
thing reached for whenever a final vowel is in question. A real `-aw` suffix
ALTERNATES before another suffix — SPADAO > `pspadaw`, but `pspdagan`,
`pspdagun`, `pspdagi`. Root material SURVIVES. Every one of his `-e` headwords
that has a suffixed slot keeps the vowel: LAQE = `laqi` in `Lqean`, TAQE =
`taqi` in `Tqean`/`Tnqean`, LABE = `rabi` in `Klbiyun`/`Pklbiyan`, TABE in
`Tbian (Tbiyan)`/`Tnbiyan`/`Tbiun`. `laqi` 孩子 and `taqi` 睡 settle it.

A first pass scored this 0 of 4 — backwards — because the classifier looked for
the stem vowel without allowing syncope (`ta-` > `t-`), so it missed the vowel in
every slot that had one. Four cases is small enough to read by hand, so read
them by hand. Same class as the `inf.roots()` tuple trap: **a heuristic that
returns the opposite answer without erroring.**

**Same root in two dialects is not a licence to merge two cards.** His TABE 犁
and TABUN 開墾 are one word — Tgdaya `tabul` covers both, and his own note on the
TABE card asks 是否與 TMABUN 有親屬關係. But modern Truku kept only the digging
half (`tabun`, `tmabun`, `mtabun`, `stabun`, `tbunaw`, all dark already), and the
ploughing half he glosses 同義詞＝SAKOL, with the map writing his unsuffixed forms
onto `sakur` 犁. `sakur` has no suffixed slot in the wordlist, so his eight
suffixed TABE occurrences have nowhere to land and stay pale — even though
`tnbiyan` 犁過的田 sits one vowel from listed `tnbunan` 已開墾的地方. Pinned. **A
cognate in another dialect explains a word; it does not spell one.**

**A sheet row names a string, not a root.** Row 3 proposed `biyi` for the TABE
card. `biyi` is 工寮 — the modern dictionary writes the hut in full as `biyi
qmpahan` — and its family is all building (`pbiyi`, `tmbiyi`, `spbiyi`). Second
false row on sheet 1 after row 1's `dagi`; read row 1 before printing, and
distrust any row whose root gloss has nothing to do with the cards under it.

**`tbilan`: the `miri` line is closed.** `pniri` 挑織布紋的衣服 is a perfect
semantic match for `Lukus tbilan` 節慶服飾, but the family reduces to `-iri`/`-ri`
with no b and no l, he has no MIRI card, and `tbilan` is in no modern corpus in
any spelling. p. 320 shows him doing T-prefix analysis on the neighbouring cards
(TBALAE, TBNAO) and failing on this one. Still held. Only thread left: `hmuril`
鈴鐺（裝飾品）, with `pnril`/`tnrilan` unglossed in the lexicon.

97.4337% unchanged (43,320 / 1,109 / 32).

## His <r> had never crossed, and a speaker crossed it (batch 168, 2026-08-03)

`logs/dom168.py`. Sheet 1 row 2 asked whether `biri`/`tbiran` come from `bir`
車聲（擬聲詞）. They do not, and reading the cards asked a better question.

**OCR sanity check first, and it came back clean.** p. 41 really does carry two
cards spelled BIRI — `(R.?) = Dernier` and `(R.?) = Mouillé tout outre`. `(R.?)`
is his own doubt marker on the root. **The scan offset is not uniform**: the
`pages` field of `data/batch_NNN.json` indexes `scans/full/page_NNN.png`
directly, NOT the printed page number, which runs 21 lower in that stretch.
Check the content, not the header, when confirming a card.

**A statistic said no and a speaker said yes.** His `<l>` is ambiguous — 1,151
become modern `<r>`, 1,275 stay `<l>` — but his `<r>` had never once crossed: 0
cases of `<r>` → `<l>` in 5,514 respellings, against 71 where it stays. `bili`
很濕 (spoken ×10, with `blbili`/`dbili`/`empsbili`/`gmnbili` behind it) is the
first crossing in the map. It stands, because `Biri kana lukus mo da` is `bili
kana lukus mu`. Recorded so the *second* crossing is not waved through on the
strength of this one.

**Two of the four occurrences are knowingly wrong, and that is the price.**
`modernize()` takes a word and no entry, so one key spells both cards — the same
wall as p. 222's two `Mpolo` subs. Batch 69 held this tie for that reason; this
ruling overrides it. Both cases now sit in `audit_rare.py`'s docstring, which is
the only place the census's blindness is written down.

`tbilan` is untouched: he glosses it `？？` himself, it is transparently an LF in
`-an`, and with the root unknown the `<l>` is a coin flip.

+4 occurrences. 97.4247% → **97.4337%** (43,320 / 1,109 / 32).

## A root in -aw writes -ag- before a suffix (batch 167, 2026-08-03)

`inflection.py: awag()`, rung 10 of 14. `logs/dom167.py`.

**The worksheet's own top row was a false question, and reading it is what found
the rule.** Sheet 1 ranked `dagi` first: four pale words, ten occurrences, and
the wordlist glosses `dagi` 要煮飯. Cooking rice has nothing to do with his
SPADAO card, so the sheet was about to ask a speaker whether `pspdagi` is a
cooking word. Nobody should be asked that. **Read row 1 of a generated sheet
before printing it** — the ranking is by occurrences, so a bad row goes to the
top exactly when it is worth the most.

**He was right; the wordlist had the whole family.** Modern Truku prints
`pspadaw` 慷慨（不計價的送人）, `pnpadaw` 送過的禮物, `emppadaw` 將…作為禮物 and
`pnspadaw`, and the map had already landed his unsuffixed forms on them — 4
`pspadaw` and 4 `pnspadaw` were dark before this batch. Only the four SUFFIXED
slots fell through, and `roots()`, finding nothing better, reached inside
`pspdagi` and pulled out the rice.

**The alternation is regular and it is his own: 76 pairs against 2.** A root in
`-aw` writes `-ag-` when a suffix follows, so `pspdagun` IS the modern slot of
`pspadaw`. Nothing is misspelled; a rung was missing. This is the same shape as
`syncopated` — an orthographic fact of the paradigm, not a claim about meaning —
and like it, the rule still refuses to fire without a gloss of his to agree with.

**Longest-first, or it lands on the wrong card.** The wordlist files `padaw` as
「是 spadaw 不可靠的人 的詞根（無意義詞）」, an entry its own derivatives refute.
Candidates are walked longest-first exactly as batch 165 settled for
`syncopated`, so the search stops at `pspadaw` and never at `padaw`. A `<n>` in
the first two positions is treated as the infix it is, not a letter of the stem.

Three refusals are pinned: `pkagi` (no `-ag-` stem long enough), `knsrhagan` and
`pnslhagan` (no `-aw` word the gloss agrees with). A later widening that sweeps
them up has stopped reading his Chinese.

+10 occurrences, 4 values off honest pale onto listed modern words, 0 de-verified.
97.4022% → **97.4247%** (43,316 / 1,113 / 32).

## What is left is a speaker's, and the unit is the ROOT (2026-08-03)

`tools/orthography/build_worksheets.py` → `tools/orthography/worksheets/*.md`.

**`inf.roots(v)` returns `(root, prefix, suffix, slot)` TUPLES, not strings.**
`self.gl.get(tuple)` is therefore always None, and a triage script that forgets
this reports that every candidate root is unglossed. It is a silent wrong answer,
not a crash, and it produced one here before being caught. Any scratch script
over `roots()` must take `a[0]`.

**The honest triage of the 1,123 pale occurrences**, once that is fixed:

| | occ | types |
|---|---|---|
| reaches no listed root under any analysis | 612 | 426 |
| reaches a glossed root, and the glosses **disagree** | 307 | |
| reaches a root the wordlist lists and never glosses | 122 | 84 |
| no gloss of HIS to test with | 81 | |
| agrees, pale for some other reason | 1 | |

The 612 get no worksheet row: there is no proposal to put in front of anybody.
The rest resolve into 356 roots covering 326 types / 510 occurrences.

**The last computational idea was measured and refused.** `_his_glosses` gives a
SUB the parent card's gloss only when the sub's own gloss is a pointer (參見,
的過去式), so a sub with a gloss of its own is judged with the root card he wrote
it on invisible — `Skdolox` 直－真誠－誠實 weighed without `KDOLOX`
牆—整齊排列的堆疊 standing over it. That looked like the structural gap behind
the whole bucket. It buys **zero** occurrences: 135 candidates have no parent
gloss to read, and for the other 192 the parent disagrees exactly as the sub did.
Feeding in more of HIS Chinese cannot settle a question that turns on what the
MODERN word means. The gap is real and it is not load-bearing.

**So ask per root, not per word.** One answer unlocks a paradigm — `dagi` holds
`pspdagi`, `pspdagun`, `pspdagan`, `pnspdagan`, ten occurrences — and a speaker
can answer "what does this root mean" without being shown a dictionary. Two row
shapes, because there are two kinds of silence: where the wordlist glosses the
root and says something else (`dagi` 要煮飯 against his 贈送／禮物; `bir`
車聲（擬聲詞） against his 最後的 — both plainly homographs, both answered in
seconds), print both and ask which is right; where the wordlist lists the root
and glosses nothing, print his Chinese as a PROPOSAL and ask for the meaning.

His Chinese is never the answer, only the proposal. **A speaker contradicting him
is the most valuable outcome on the sheet** — that is the one that keeps a wrong
spelling off the page, which is the whole lesson of batch 166.

Sheets are ranked by occurrences and steeply front-loaded: the first 45 roots
(sheets 01–03) are worth about half the 510. Nothing is dropped; the tail is
1-occurrence roots. The standing refusals ride along on purpose — `biri`/`tbiran`
is row 2 of sheet 1 — because a NO is as good as a YES: it turns a PIN that
currently rests on our judgement into one that rests on a speaker's.

Nothing here scores until it is ruled. The census moves on the respelling, never
on the sheet.

## Hunting the batch-166 error everywhere else, and not finding it (2026-08-03)

`tools/orthography/audit_rare.py`. Batch 166's bug scored itself **dark** —
`seelug` and `smeelug` are listed modern words, so rule 1 verified them at
sight. The census is structurally blind to that class of error: a wrong spelling
that happens to be somebody else's right spelling counts exactly like a right
one. Driving the percentage up cannot find it. So the audit went looking for the
same shape everywhere else in the map.

**Two signals, and neither is worth anything alone.**

*Rarity.* The map makes 5,513 respellings out of 573 distinct letter
correspondences, and a handful of them are the whole system (`o>u` 882, `l>r`
811, `x>h` 643, `->e` 418, `'>-` 381). Canonicalise both sides through the
classes the map actually swaps and 3,680 respellings collapse to distance 0 —
the same word in two alphabets. Then 1,451 at 1, 303 at 2, 63 at 3, 14 at 4, one
each at 5 and 6. `s'lu` → `seelug` sits at **3**.

But rarity is not evidence. All 57 rows at distance ≥ 3 were read and 56 are
lexical swaps he licenses himself: `tabe` → `sakur` 犁 with his own note
同義詞＝SAKOL, `tbako` → `lumak`, `sengse` → `mtgsa`, `sadyaq` → `seejiq`,
`daloas` → `dowras`, the whole `mpa-` → `empaa-` prefix family. He is not
misspelling those, he is naming a different word for the same thing, which is
what a dictionary does.

*Disagreement.* `_agrees` between his gloss and the modern one. Alone it fires
519 times on ordinary homonymy and on two glosses written a century and a
language apart.

**Together they cut 266 rows to 34**, and 34 is a number a person can read. All
34 were read. Thirty-three cleared, and the clearances are the useful part:

- `P"lu` → `peelug` — his own example gloss ends **（在同一條路上）**. He derived
  正當…之時 "at that very moment" from the road himself.
- `Skdolox` → `sdrux` — `KDOLOX` is 牆—整齊排列的堆疊 and `qdrux` is 石牆. His
  直／真誠／誠實 is the figurative half of one root, which his own `Mskdoloç`
  prints together as 正直的、排列整齊的.
- `mpaxei` → `empaahiyi` — `hiyi` is flesh AND fruit, so 會有瘦肉 and 將結成果實
  are one word.
- `daloas` → `dowras` — cited 人名 because the cliff word is also a man's name.
- `x'lyeq` → `hgliq` — 毀約 is 撕裂 applied to an agreement.

**The one that did not clear cannot be fixed by the map.** p. 222 carries two
subs both spelled `Mpolo`: 發起者／模仿者, which is `purug`, and 患風濕、痛風的人
with the example `mpolo kana papaq mo!` 我的腳滿是風濕. The second is a different
word. The map is keyed on the raw **token**, so both get one spelling and no map
entry can separate them — it needs a per-card override or a speaker. Recorded,
not patched.

**So the finding is that there is nothing to find, and that is worth as much as
a find.** The map is clean where it is strangest. Re-run `audit_rare.py` after
any batch that adds unusual mappings; its rows are the only place the census
cannot see. It self-tests on the historical `s'lu` → `seelug` pair, so widening
the letter classes until the bug is invisible fails loudly.

## When he doubts his own root, believe the doubt (batch 166, 2026-08-03)

**p. 284 is a card about making things and we were printing roads on it.** His
`S"LU` and `SM"LU` cards both carry the tag `(R. = "LU ?)` and cross-reference
`"LU` (p. 386) 路－通道－道理（意義）－方法. The map followed the pointer:
`s'lu`→`seelug`, `sm'lu`→`smeelug`, `sn'lu`→`sneelug`, `snluwan`→`sneelugan` —
four road words on a card glossed 計劃－預謀 and 決定.

The root is **SALU** 'to make, to repair'. Tgdaya *salu* = to make, *smalu* is
the actor focus, *snluwan* is the preterite locative focus. Ruled by a speaker,
2026-08-03. `"LU` itself is untouched and was never in doubt — *elu* in Tgdaya,
*elug* in modern Truku, all 91 occurrences correct.

**Modern Truku had the paradigm all along**: `salu` 修理, `smalu`/`smmalu` 製作,
`snalu` 用...做的, `psalu` 請…製造或修理, **`sluun` 要被製作**, and `sluan` /
`snluan` listed unglossed. `sluun` is the proof — modern Truku writes the
syncopated stem `slu-` in the exact slot where he wrote `S"LU`, so his `"` is
the reduced vowel of *salu*, not a glottal standing in for *elu*.

**The page was already spelling it right everywhere else.** Before the patch:
5 `salu`, 13 `smalu`, 6 `snalu`, 3 `snluan`, all rendered from tokens he typed
without the `"`. Only the four tokens carrying his reduced-vowel mark were
misrouted — because a rule believed a pointer he had explicitly flagged.

**Two of the thirteen scored DARK.** `seelug` and `smeelug` are listed modern
words, so rule 1 verified them at sight. Same shape as the SISUN trap: *a
spelling error wearing a verification's clothes.* **The metric cannot see this
class at all** — only a reader can, which is the standing argument for spending
attention on the darks and not only on the pale count.

**It settles what dom165 could not.** Batch 165 refused two pointers sitting
inside a question mark but could not say whether `(R. = X ?)` in a TAG meant he
doubted the root or his spelling of it. It means the root, and he was right.
**The tag is evidence AGAINST the pointer it contains.** 226 cards carry it.

**The instrument this suggests, and the one it doesn't.** Sweeping all 226 is
mostly noise: 49 show the S"LU fingerprint and ~45 of those are ordinary
correspondences (o→u, x→h, ao→aw, l→r) doing their job. The sharp test is
rarity — the map makes 5,513 respellings using 573 distinct correspondences,
and `o>u` fires 882 times while the S"LU error fired **once**. **212 rule-1
darks rest on a once-only correspondence.** That is the audit population, and
it is a list of candidate spelling errors currently scoring as verified.
(scratch: `tmp/rare166.py` under the job dir.)

+5 occurrences net; 13 respelled, 2 of them off false darks.
97.3910% → **97.4022%** (43,306 / 1,123 / 32).

## A greedy algorithm over an unordered input is a sample, not a rule (batch 165, 2026-08-03)

**The build had not been reproducible for some time and nothing had noticed.**
Rebuilding twice with no change at all and diffing the output showed `mngahan`
appearing in three builds out of four. `root_groups()` partitions candidate
roots greedily — each candidate joins the first group it touches — so its answer
depends on the order it walks them, and it walked a **set** sorted by length
alone. Every tie among equal-length candidates was broken by Python's
per-process hash order. `mngahan` reaches six candidates tied at two lengths and
fell into one group or two by luck, so `no_chinese()`'s one-group gate passed or
failed and the word came out verified or pale. The sort key is now `(len, x)`.

Two things to carry forward. **dom164 asserted `mngahan` GAINED — that
assertion had been a coin flip since the moment it was written**, and all 195 of
`no_chinese()`'s values were exposed to the same instability. And the cheapest
possible test found it: *run the build twice and diff*. Do that before believing
any measurement, because a flaky verification does not look like a bug, it looks
like a number.

**Two evidence sources no rung had ever read.**

*His own paradigm, where the wordlist has none.* `unglossed_root()` asks a
listed-but-unglossed root's modern paradigm what the root means. For eleven
types the paradigm is glossless too, end to end — the wordlist is not
disagreeing, it is **silent** — and `_agrees` returns None for want of anything
to read. So ask his paradigm: the wordlist lists `ngangah` and glosses neither it
nor any of its three slots, while Pecoraro wrote four separate cards on it that
agree with each other on 啞巴 and 痴. Guards: the agreement must be a **bigram**
(two glosses of his share 的 and 使 and 人 by the nature of his prose), and it
takes **two** supporters (one cross-referencing card is a restatement, not
corroboration — `pnkltudan` and `pkltudan` carry the same sentence and would
vouch for each other in a circle). Where the paradigm SPEAKS and disagrees the
value stays pale, and that is the larger half of the bucket.

*He names the word himself.* Some glosses are not meanings but **pointers** —
`rnjingan`'s entire gloss is （ldingan 的過去式）— so `_agrees` has nothing to
weigh rather than something to reject. A stated root beats an inferred one:
every other rule peels affixes and then argues the inference is right; here he
says it outright.

**The refused third shape, and why it is the SISUN error with a citation
attached.** Letting the pointer SUPPLY a root where the affix rules find none,
paid for with a gloss agreement, gains ten types and every one is wrong the same
way. His 參見 and 較常說 are **see-also** notes: `loai` 外部 carries
較常說：NGANGOT, `nilaq` a mushroom cross-references another mushroom. The
pointer names a synonym, the gloss agrees because synonyms mean the same thing,
and out comes `loai`'s spelling certified by a modern word that is not `loai`.
**A cross-reference is evidence about the root of a word he is analysing, never
about the spelling of a word he is merely comparing.** The pointer must land on
a root the morphology independently found.

**A pointer inside a question is not a citation.** He marks his own uncertainty
with ？ and is scrupulous about it, so the punctuation is his evidence. `tbowyak`
is （詞根 BOYAQ？）＝痛得打滾 — he is *asking* whether the root is BOYAQ, and
`bowyak` is 山豬 a wild boar. `empsibus` is （Pksibus?）加糖 while its own sibling
`pksibus` carries 參見 Psibus with no question mark; the pair draws the line
exactly where he drew it.

**Refuted cheaply, and worth not reopening.** The 612 occurrences whose root is
in no wordlist stay dead: `spoken_truku.json` is a strict subset of
`attested_modern.json` (0 types outside it), and admitting `parquet_truku_freq`
+ `bible_truku_freq` as root sources reaches 26 occurrences, nearly all trivia.
The SYN vein is 163 rows / 292 occurrences that fail only on `_agrees`, and
under SYN's own doctrine — interchangeable, not merely associated — one
qualifies (`embbuway` 互相贈與 / `buway` 給).

**A tripwire set in advance caught this batch.** (a) verified `psiisi`,
`psiisan`, `psiisun` and dom153 went red. Batch 153 respelled his SISI/SISAN/
SISUN paradigm on a Truku speaker's ruling, let the unlisted causatives go
honestly pale, and wrote the trap in the same breath: *"if these ever go dark
without a speaker or a listing behind them, the respelling has been allowed to
carry verification with it, which it must never do."* Exactly what happened —
this rung asks whether his own cards agree about a **listed** root, and `siisan`
is listed only because we put it there, so what agreed with itself was our own
respelling. Six occurrences refused, in `HAND_NOT_FAMILY`. **Run the whole suite
before committing, not the new log.** A log that only ever confirms the batch
that wrote it is decoration.

+11 values / 22 occurrences, 0 de-verified, **0 new pale types**.
97.3415% → **97.3910%** (43,301 / 1,128 / 32).

## An empty candidate list is not a refusal (batch 164, 2026-08-02)

Nineteen batches of widening rungs, and the largest block left in the census
was never being judged by a rung at all. **Every rung opens by asking `roots()`
for something to read, so when `roots()` returns nothing the value is not
refused — it is invisible, to all eleven at once.** 465 of the 807 pale types,
665 occurrences, 55% of the whole pale mass, decomposed to nothing whatever.
Diagnose the *empty* list before widening the *judgement* on a non-empty one.

**`roots()` peels one prefix, and Truku stacks them.** `dmtqsurux` is
dm+t+`qsurux` 魚, `kmspusu` is km+s+`pusu` 根本, `ndjyamu` is n+d+`jyamu`
屬你們的 against his own 你族人中的一個. A second peel, depth-capped at two.

**Write it as a fallback, not a widening — the distinction is the safety.**
`no_chinese()` refuses a value whose candidates fall into more than one root
group, so handing an extra candidate to a value that *already* has some can
split a clean one-group reading into a tie and **de-verify** it. That is the
one direction the "widening only adds membership" invariant does not cover.
Firing only on an empty list makes it impossible by construction. The same
ordering rule appears twice more in this batch, and both times it was load-
bearing rather than decorative.

**A gloss hole is not evidence, and two rungs each assumed the other covered
it.** `unglossed_root()` exists for a root the wordlist lists but never
glossed — but it can only fire where HIS Chinese exists to compare the root's
paradigm against. `no_chinese()` is the rule for where his Chinese is absent —
but it demands a GLOSSED root. A value with **neither** falls between them and
nothing in the file can see it. `nglngu`: `lngu` is listed, bare, and the
wordlist inflects it thirteen ways. *A root inflected a dozen ways is a word
whether or not anyone wrote down what it means.* Witness borrowed from
`unglossed_root()` minus the comparison there is nothing to compare.

Run it only when the glossed candidate list is empty. `stmaqun` is why: its
glossed candidates `taqi`/`tmaq` are two real roots that must keep refusing
(dom163's assertion), while its unglossed `stmaqi`/`tmaqi` are one group and
would have quietly overridden them.

**When a threshold is a proxy, spell the guard instead.** Batch 163 dropped
`outvoted()`'s root floor 4→3; this drops the same floor and replaces the
number with what it stood for — a root has to be pronounceable. Four letters
keeps `hng` out by accident; **requiring a vowel keeps it out for the reason**,
since Truku writes no schwa and a listed form with no vowel is a consonant
cluster the wordlist filed, not a syllable anyone says. `smhngi` is the only
thing the floor was buying.

Two veins were priced and **refuted**, which is why they are recorded here:
*a "gloss" that is a structural note* (`同上之動詞形。` is 25 pale occurrences,
the largest single string in the census) turns out never to stand alone — it
always sits beside a real gloss, so the whole class is 9 values / 20 occ; and
*onomatopoeia roots* are a trap rather than a vein — `bir` 車聲 inside `biri`
(his 濕透), `bus` 蒸氣洩出聲 inside `mbusi` (his 戴帽子), `puq` 手指扭折聲
inside `puqi` (his 餵食) are `mnalu`/`tabu` homographs at scale, and the rungs
are right to refuse all 20 of them.

The price is six substring accidents in the new `HAND_NOT_STACK`, pinned at the
*peel* rather than at a rung because the claim being refused is the peel's own.
`empnalu` is his 將會變好、康復 — that is `malu` 好, the root batch 161 already
refused `mnalu` over, not `alu` 陷阱線 a snare line.

**An earlier batch's deliberate refusal outranks a later batch's newly-widened
reach — and only the regression suite will tell you.** The gloss-hole fallback
reached `tnaga` through `taga` 等 and coloured it verified; dom161 had asserted
it pale. Batch 161's refusal was epistemic, not a missing rule: `tnaga` is in
the C-n- infix class, where `<n>` perfective and `<m>` actor-focus share a
slot, so the token is either t-n-aga on `taga` or his typewriter's n for the m
of `tmaga`, and nothing on the card decides which. A rule that *reaches* a word
is not thereby entitled to it. Pinned in `HAND_NOT_NC`. Nineteen of the twenty
dom logs passed untouched; this was the twentieth, and it is the reason the
suite runs before the commit rather than after.

+41 values / 48 occurrences, 0 de-verified, **0 new pale types**.
97.2335% → **97.3415%** (43,279 / 1,150 / 32). Past the 97.3333% mark.

## Tier X — lexical substitution, shown in brackets (2026-07-29)

Sometimes his word is simply gone from the language and a different word carries
the meaning. That is not a respelling, and the toggle promises spelling, so a
substitution has to **declare itself on screen**: modern mode renders
`QUSUL (Q'NAO)` — the substitute in the modern brown, his own word beside it in
the green that means "Pecoraro's spelling" everywhere else. Pecoraro mode is
untouched; there is nothing to disclose when his spelling is what's on screen.

- Source: `tools/orthography/lexical_map.json`, its own file, keys prefixed `_`
  are documentation. Tier `X` outranks every other tier in the generator — no
  spelling rule can reach these, and no attested-candidate search should be
  allowed to overrule a decision made on the meaning.
- Exported separately as `window.LEXICAL_SUBS`; `linkifyTruku()` appends the
  bracket, `.w-orig` styles it.
- The bar for adding one: (1) no reflex of his word anywhere in the omnibus by
  gloss, by fuzzy shape and by substring, and (2) his dictionary has no form of
  the modern word either — i.e. the two lexicons really don't share the word.
- A value of **`null` blocks the token instead of substituting it** — it says "we
  looked, and there is no modern form to name", and the word stays green. That is
  the right answer three ways: a derivative whose base was substituted but which
  has no modern derivative of its own (`stbako` "to smell of tobacco"; `slumak`
  is unattested in all three corpora); a paradigm the substitute doesn't reach
  (`sl'xqe` / `sl'xqan` / `sl'xqon` / `slx'qon`); and a **homograph whose two
  entries want different answers** — BIRI "trempé" is the modern `bili` 很濕, a
  plain r/l respelling, while BIRI "dernier" is a word that is gone (`biri` is 0
  everywhere; 最後 is now khici / tqring / nhdan). The map is keyed on the token
  and the search index is built from it, so one token cannot render two ways
  without breaking lookup. Green is the honest colour for a reading that depends
  on which entry you are standing in.
- A fourth use, and the one that shows what the block does and does not buy:
  **a rule output nobody can check**. `pskluyun` was reaching the screen as
  PSKRUYUN, an l→r on a family that keeps l in all eleven of its attested modern
  forms (`kluwi` 驚醒, `skluwi` 嚇一跳, `mskluwi` 驚嚇, `mnskluwi` 12× …), and the
  KL guard had not caught it. There is no modern `-un` form of any `-uwi` root on
  record, so `pskluwiun` would be an invention; the block is the honest move.
  But **blocking changes the colour, not the spelling**: green words are still
  displayed through `charRules()`, which does the same l→r, so the word still
  reads PSKRUYUN — in green now, alongside its siblings `kluyun` and `skluyun`,
  which were already green and already showing that r. Green does not mean
  "left as he wrote it"; it means "rule-guessed, unverified". What the block
  bought is that one of the three no longer *claims* the r. There is no third
  state available: `respellable()` is membership in one of the three tables, so
  every word is either a claim (brown) or a guess (green).

  **Batch 19 unblocked it, and the reason overturns the paragraph above.** The
  choice was never "invent `pskluwiun` or accept green" — a **keep-letter identity**
  (`pskluyun` → `pskluyun`) asserts nothing about the `-un` shape and only declines
  the l→r, which is precisely the finding batch 14 had already made in words ("a
  family that keeps l in all eleven of its modern forms"). Blocking to avoid a rule
  output *delivers that rule output*, because `charRules()` runs on green. So a
  `null` only buys silence for a token the char rules would leave alone; for a token
  holding an l, o or x, **blocking is not abstention, it is voting for the rule** —
  and if the reason for blocking was that the rule is wrong, the block is
  self-defeating. `kluyun` and `skluyun` took the same identity in the same batch;
  `lexical_map.json` is down to 23. Re-read the remaining blocks against this test:
  a block is honest when the *lexical* answer is unknowable (`stbako`, BIRI), not
  when a *letter* is.

  Batch 15 blocked `ttuun` / `ttuon` the same way, and the reasoning is worth
  keeping because it distinguishes a block from a projection. They are the `-un`
  slot of his cut root (TA'TO 切割), and they were identity-mapped, i.e. claiming
  a word that exists nowhere: modern has **no** suffixed form of `teetu` at all
  (`teetun`, `teetuun`, `teetuan`, `tteetu` are all 0), and the `ttuy-` forms that
  do exist (`ttuyan` 8×, `ttuyaw` 被叫醒) belong to his *other* entry, TUTWI 起身,
  whose paradigm he himself spells with the y. So there was nothing to claim, and
  blocking put all three of TA'TO's `-an`/`-un` slots into the same green.
  Contrast the four PT"TO slots the tiers added off the newly-correct root
  (`mpteetu`, `pnteetu`, `pteetuan`, `pteetuun`, all 0-attested): those are
  **regular affixation of a stem that is itself proven**, which is what the P and R
  tiers do 1,981 times over. The line is whether a *stem* is attested, not whether
  the exact affixed shape is.
- The six live now:
  - `q'nao` → `qusul` (garlic). All 32,212 omnibus words swept; the modern Allium
    field is `qusul` / `pixil` / `neygi` / `sangas` and nothing is shaped like
    /qnaw/. He has no `qusul`-shaped word either, and he separates the native
    `Q'NAO` from the loan `NEGI` = oignon.
  - `sl'xeq` → `shik`, `sml'xeq` → `smhik` (to lick).
  - `tbako` / `t'bako` → `lumak` (tobacco). His TBAKO is the Japanese loan and it
    did not survive — tbaku, tbako, tmbaku, stbaku are absent from the omnibus,
    from truku_dict and from 277k tokens of speech. The modern word is the native
    `lumak` 煙草 (with pslumak, pnslumak, ptglumak, rnabaw lumak), and his own
    idiom survives with it: he writes `mqan tbako` for smoking, and the omnibus
    says `mkan lumak` 抽煙 over and over. He has no lumak-shaped word anywhere.
  - `sengse` → `mtgsa` (teacher). He tags it `[emprunt jap./chin.]` himself
    (sensei / 先生). `sensi` and `sengse` are in no corpus; modern Truku teaches
    with the native tgsa root — mtgsa 老師 (296 in speech), emptgsa (198), tmgsa
    (97) — and mtgsa is the commonest.

Keep the list short. A long one means the toggle has quietly become a translator.

## Truku cited inside a gloss (2026-07-29)

Glosses are never run word-by-word through `modernize()` — the char rules turn
French "Palissade" into "Parissade" — but his definitions are full of Truku:
cross-references (`See T"TO`) and forms cited to build a sense (`B"lo babwi =
piglet`). Those sat frozen in his spelling inside an otherwise modern page.

`glossCites()` claims exactly one thing: **a token carrying his second elision
mark `"`**. No French, English or Chinese word has a word-internal double quote,
and `tidyLatin`/`tidyZh` have already converted the real quotations to `« »` /
`" "` / `「 」` by then, so what's left is unambiguous — 102 occurrences across
the three languages, 30 types, every one Truku, zero false positives. Those
tokens go through `linkifyTruku()`, so they follow the toggle, take the word
colours and link.

Do not widen this. The apostrophe cannot be recruited the same way (`l'occasion`,
`don't`), and "is it a headword?" is far worse — measured, it claims `a`, `I`,
`on`, `do`, `un`, `ta`, `ma`, `si`: **10,819 occurrences** of ordinary French and
English prose. The `"` is the whole of the safe signal.

Two repairs fell out of the same pass: `esc()` now escapes `"` (headwords like
`SBU"` and `"LU` were closing their own `data-ref="…"` attribute early), and the
"stop glued to next word" rule no longer splits a dotted abbreviation — `i.e.`
became `i. e.`, which then hid it from the `ABBR` guard and came back as
`i. E. Bodyguards`. All 13 dotted forms now on screen are real abbreviations.

## French inside a Truku field (2026-07-30)

The mirror-image defect. His remarks are in French, and some of them are not in a
gloss at all: they sit in a bracket on a **sub-form** — `Pqaya (Est-ce de la R.
QAYA ?)`, `Pqboan (= contraction pour: PQBBOAN ?)`, `Mskui (parfois = Mskwi !!)` —
and four example lines under AN are not examples but French gloss pairs, `Malu =
Beau, bien; Knmlaan = beauté, bonté`. Those two fields are tokenized as Truku, so
the char rules ran on French and printed it back as fake Truku: PRUDUIT,
CUNTRACTIUN, SAVUIR, CUNNAISSANCE, BUNTE, matinarite. Six were worse than mangled
— the curated map claimed them, so they came out **brown**, asserting a verified
modern Truku spelling for a French word: ne→ni (which is his own word for "and"),
pour→puur, page→pagi, nique→niqi, non→nun, matin→macin.

`FORM_PROSE` is a **separate set from `TAG_PROSE`**, not a reuse of it, for two
measured reasons: `UN` is one of his headwords, so the French "un" that TAG_PROSE
needs would grey an entry; and `vl.`/`var.` are already named by `metaAbbr`, which
gives them a tooltip the prose branch would take away (`vl|vel — ou / or` is
asserted in the test). Passed at exactly two call sites, the example line and the
sub-form. Every word in it was read off those two fields, and every occurrence of
every one is French — 24 fields, 56 occurrences, 42 types, not one Truku word
among them.

**A list read off the data once is not closed.** Four more were still rendering as
fake Truku, and two of them **brown**: `Rougeur` as RUUGEUR and G'LEQ's `(=Volant)`
as VULANT, each asserting a verified modern Truku spelling for a French word — plus
`bouche` and `rouge` green in YA. Added, and the fields went 20 → 24. No map entry
was deleted for it: `rougeur` and `volant` are in no curated tier, they are generated,
so a deletion regenerates — and the prose branch sits *before* `respellable()` is
asked, so greying the word is the whole fix.

**Predicting the page means replicating the GUARD, not just the branch.** `frtok.py`
computed `MAP[k] or charRules(k)` and reported 17 mangled words, 13 of which
FORM_PROSE/TAG_PROSE/metaAbbr had already handled — the same blindness as computing
green counts from `modern_map.json` while WORD_OVERRIDES sits in `app.js`. Its
successor replicated the prose sets but still assumed every tag reaches the word
path, and so reported the largest defect of the class: `plant` in 67 tags and
`animal` in 64 rendering PRANT and ANIMAR. **Not real.** `tagHtml()` enters
`linkifyTruku` only when `ROOT_MARK` matches; everything else is `esc(tag)`. So our
own digitization metadata (`plant`, `animal`, `note`, `name (m)`,
`[emprunt jap./chin.]`) never reaches `modernize()`, and neither does K'LOX's French
remark `(Y aurait il parentée avec QOLOX = crâne ?)`, which holds no lone R. The DOM
settled all of it in one run.

Two things the sweep turned up that are **not** this defect, and are left alone: his
own words get quoted inside his French glosses, so "appears in a gloss" is not the
test — `lqlaqe` is in 50 Truku slots and 4 glosses, and a French intrusion is the
other way round (`bouche`, 1 slot against 37 glosses). And `Morisaka` 森坂 (5 example
slots, mapped `murisaka`) and `Eco` (KBSULAN's example, rendering ECU green) are a
**place name and a personal name**, not French. Truku writes no o, so `murisaka` is at
least consistent with the phonology — but nothing attests either, and a name reached
only through an example never got a name tag. That is the tier-D name-seeding gap,
not this one.

Verify by **counting spans, not naming them**. The first test hand-typed the Truku
words standing beside the French and 8 of 13 were wrong, because in modern mode the
page shows the modern spelling — `G'LEQ` renders as GRIQ, `Adi` as AJI. `dom_fr2.py`
reads `FORM_PROSE` out of `app.js`, locates each field in the DOM by containment,
and asserts the coloured-span count equals the number of tokens that are neither
French nor a meta abbreviation. That is what catches a French word left off the
list: it survives as a surplus coloured span whatever the char rules did to its
shape. Two did — `produit`, dropped while composing the string, and `matinalité`,
whose scare quotes `tidy()` has already converted to curly ones before tokenizing,
so the key is the bare accented word.

Discoveries encoded in the generator: Pecoraro's ç = modern x (tunuç→tunux);
ao/oa = aw/ow/uwa (daolas→dowras, boax→buwax); d→j and t→c before i (adi→aji,
tmoting→tmucing); schwa vowels Pecoraro wrote are often dropped (kensat→knsat);
q/k swaps need gloss proof. Gloss evidence must cover ≥20% of the omnibus gloss —
a 2-char overlap inside a long definition is coincidence (the raki/laqi trap).
Regenerate modern_map.js whenever entries.js changes; if manual_map.json or
llm_map.json change, just rerun the generator.

Coverage (44,306 displayed token occurrences / 4,938 distinct hw+sub+paradigm
forms): 77.4% / 44.5% verified-attested (id+M+A+B); 80.6% / 52.1% adding the
gloss-adjudicated L and sister-validated T tiers; 85.6% / 73.0% total mapped
including projection. Remainder falls to the char-rule fallback. (Baseline under
rules alone was 57.2% / 24.7%.)

Word-final "-ui" was reviewed the same way: every headword/sub-form in the corpus
ending in -ui (~17 real entries once repeated example-sentence occurrences are
collapsed) was checked individually against the omnibus — the outcome is root-
dependent, not a single rule (klui-startle/kui-insect family → -uwi; cold/harvest/
tie/get-up families → -uy; carry-hold family (dui) → -uuy; drip family (xbui) →
-uy after x→h; grammatical imperative-mood "-ui" endings, e.g. GTUI, don't change
at all — confirmed identical in the omnibus). Applied as a `WORD_OVERRIDES` lookup
in `app.js`, checked before the character rules. A few forms (TOKO's `Ptkui`,
`SKUI`=dwarf bamboo, `Kmubui`/`kmbui`) had no confirmed modern counterpart and are
left unchanged.

## A gain of the right size is not a gain of the right kind (batch 155, 2026-08-02)

`manual_map.json` is keyed on Pecoraro's **raw** tokens, before normalisation.
His `PSQPAXAN` normalises to `psqpahan`, and a manual_map key written
`psqpahan` therefore matches nothing — **and says nothing**. No error, no
warning, no diff in the "mapped with actual spelling change" count.

That is ordinary enough. What made it dangerous is what it was paired with. The
batch removed three `HAND_NOT_UNGLOSSED` pins on the grounds that the
respelling made them unreachable. The respelling was not there, so the pins came
off words that were still spelled his way, and all three verified off `qpah`
工作 — **the precise error the batch existed to fix.**

**The census could not see it.** +5 values / +8 occurrences, 0 de-verified,
43,042 dark, 96.7997% — digit for digit identical to the correct build. Three
words went dark either way. Only the reason differed, and the reason is the
entire content of the claim the dictionary makes when it prints a word dark.

What caught it was `logs/dom155.py`'s GONE list: an assertion that his
spellings `psqpahan`/`psqpahi`/`psqpahun` no longer render **at all**. That is
a statement about which words exist, not about how many are verified, and it is
the only kind of check that could have failed here. The GAIN and PIN lists both
passed on the broken build.

**Reusable:** when a batch's argument is "X is now unreachable, so its guard can
go", the log must assert the unreachability directly. A guard removed on the
strength of a change that silently did not happen is a guard removed for
nothing, and the metric will congratulate you for it.

## A voice is not a spelling (batch 156, 2026-08-02)

`self.lex` and `self.voices` answer different questions and the code now says
so. A word is in **`lex`** because the dictionary may PRINT it — that is what
the standing rule "`seen` widens, `lex` never does" protects. A word is in
**`voices`** because it can AGREE or fail to agree with one of Pecoraro's
glosses. Agreeing is not a claim about how anything is spelled, so widening the
second is not the thing the first rule forbids.

Batch 149 added the Truku Bible glossary as an **additive gloss source** —
`_gloss()` reads it — but its headwords were never added to the population
`derived()` sweeps. For seven batches a word the build could READ was a word
the build could not HEAR. `smqdug` 控告 sits on the roots `sqdug`/`qdug`, is
glossed by the glossary, resolves correctly, and could never be a supporter.

`voices = lex | bible_gloss`, read by `derived()` and nothing else. That last
clause is the whole safety argument, so `logs/dom156.py` asserts it
mechanically — it greps `inflection.py` and fails if a second reader appears.
**A guarantee stated only in prose is a guarantee that drifts.**

Worth 21 occurrences immediately, and two of them were homographs no gloss
comparison could break: `krwahan` 吝惜 sat on a listed `rwahi` 打開 *open* with
the glossary's `krwahi` 顧惜；捨不得 unreachable beside it; `kdagi` 扛抬 sat on
`dagi` 要煮飯 *cook rice* with `pkdagan` 使抬著 unreachable beside it.

## He wrote the rule down, and the wordlist obeys it (batch 158, 2026-08-02)

Three of his entries state a sound correspondence in prose — DUK
「請注意詞尾輔音P與K之間常見的變換；派生詞保留P，而詞基往往作K」, NDUP
「NDUK 的變體（詞尾的 P 實現為 K）」, GALUK「見 GALUP」. It is the only one he
bothers to write out, and **the modern wordlist splits the same root the same
way**: base `iyuk` 吹;吹氣 / `miyuk` 吹 with K, derived `yupi` 吹洞簫 /
`yupan` 要…吹 / `yupun` 吹 with P. Five listed words, one root, both consonants,
conditioned exactly where he says. Not drift between 1977 and now — a live
alternation he described correctly.

**So the rule is about BASES and must never become a rule about the letter.** A
blanket p→k would have rewritten those three listed, glossed, dark derived slots
into forms nothing attests. The gate is `regular()`'s: respell only where the
K-twin is **listed** and its gloss agrees with his. Five values pass, all at
rank 1 — `iyup`→`iyuk`, `qmrap`→`qmrak`, `trap`→`trak`, `qnrap`→`qnrak`,
`mdup`→`mduk`. `dup` is refused and stays pale at 7 because bare `duk` is
unlisted (modern writes `eduk` 門扇), and `dupan` 獵場 is a different root.

**This overturns batch 29's refusal of `mdup`, and the measurement it refused on
is the same one that overturns it.** `-dup$` is 0 words in 40,760; `-duk$` is 96.
Batch 29 read that as "his variant has no modern counterpart, so replacing it is
lexical substitution"; it means the p-spelling names nothing. A substitution is
when his WORD is gone and a different word carries the sense (`q'nao`→`qusul`).
Batch 19 had already taken six GALUP p-forms to k on his own doubled spelling, so
the two rulings sat in this file contradicting each other for 139 batches.
**The tie-breaker is not which is later — it is that 19 rested on his own writing
and 29 on an inference about what a zero count means.** Corrected in place above.

+5 values / 8 occurrences, 0 de-verified. 96.8605% → **96.8784%**.

## A miss in four corpora is not a verdict about the language (batch 159, 2026-08-02)

**`nta` is dark, and it is in no corpus.** It is the first entry in `HAND_SPOKEN`
(inflection.py) — a fifth kind of evidence, and the only one in this build that is
a person rather than a document. Like the parquets, the Bible and the names, it
widens `seen` and never `lex`, and `build_verified.py` prints it **on its own
line** so no later reader can mistake it for a wordlist hit.

The miss is real, re-measured, and recorded rather than explained away: **0 hits
in the 40,760-word wordlist, 0 in the 2,058 types of the Truku Bible, 0 in 14,600
parquet types, 0 in 11,820 spoken types**, against `nita` 5 and `nnita` 25 for the
genitive 我們的, which is a different word. What that shows is that no modern
Truku *text we hold* spells it. His own note says why — 邀請前往（唯一使用的形式，
與 LITA 並用）, and `Nta da ! ... Kia ! Lita da !` is a hortative interjection,
which is exactly what a Bible and a wordlist have no slot for. Its whole frame is
dark and attested: `ita`/`ta` 我們, `nita` 我們的, `nnita` 咱們的, `lita` 一起.

**What was retracted is a claim I made in a report, not one the log made.**
dom146.py refused `nta` honestly — the slot gloss that reached it was `ptntun`'s
起, which is not its paradigm — and said "the outside source was asked and did not
know". Reporting that to the informant as *"blocked — it's Toda, not Truku"* was
the error: where Klokah happened to record a form says nothing about where the
form is absent, and it cannot outweigh a Truku dictionary that prints the word
with a usage note and eight examples. **The gate did not loosen.** `rih`, `dup`
and `klulu` were pinned pale beside it in dom146 and are pinned pale still; that
is the proof. The shortlist was always a list of questions no corpus can answer,
put to a speaker one by one. This is the first answer, filed as an answer.

**SA'SO is SEESU, and a root's one-line gloss loses to its own paradigm — the
third time.** His 沉靜－羞怯－羞恥心 family (`Msa'so` 羞怯的－沉靜的, `Knsa'so`
謙遜, `Psa'so` 使平靜) is the modern `seesu` family slot for slot: `mseesu` 安靜,
`mgseesu` 默默的;文靜, `mnegseesu` 文靜的, `ttgseesu` 溫柔；謙和, `knseesu`.
Bare `seesu` is glossed 看輕人 and is outvoted, exactly as `siyang` 肉 lost to its
肥 paradigm (154) and `liwaq` 化妝/銀 lost to its shine paradigm (157). `pseesu`
verifies at level 5, the outvoted rung, **fired by the machinery and not by hand.**

**A gate on respellings is not the only road to dark.** `psa'so` and `pgsa'so`
were written off in advance as unlisted, and went dark anyway: once the root
moved, the root projection carried their spelling for free and the ordinary
derived rungs reached them at 5 and 4. Predicting otherwise was my error, not the
build's.

+6 values / 36 occurrences, 0 de-verified. 96.8784% → **96.9615%**.

## The typewriter's blind spot was position 0 and 1 (batch 160, 2026-08-02)

**The batch that passes 97% is mostly not a spelling-map batch.** Two thirds of
it is a *transcription* repair, and keeping the layers apart is the point: a map
entry would leave "original spelling" mode showing a word Pecoraro never printed.

The 1977 typescript prints an `m` the digitization read as `n` — proved by his
own French, mangled the same way (`nonbreuses`, `Conbien`, `janais`). The sweep
that finds them ("nothing in modern Truku, but a real word if one `n` is read as
`m`") had been run with an index guard of `i >= 2`. **That guard hid positions 0
and 1, which is where the rest of them were.** `knnalu` was repaired at position
2 long ago; `nnalu`, one letter earlier in the same entry, had never been seen.

**A word-initial `n-` is a real Truku prefix and looks identical, so his French
is what decides each one.** The discriminator is on the page:

  * `Nngangax` "A partir du fait d'être muet" — `n-` on `ngangah`. **Correct as
    printed, refused.**
  * `Nnalu` "A partir du bien … Il était bien autrefois" — `n-` on `malu`, so
    the *second* letter is the misread m. `nmalu` 原本是好的.

Same formula, opposite verdicts. Repaired: `Nnalu`→`nmalu`, `Nniyax`→`mniyah`
("qui es venu"), `Nllawa`→`mrrawa` ("chahuter"), `Naxon`→`mahun` ("l'eau pour
boire"), and two of three `naso`→`masu` ("le millet"). **The third `naso` is his
分配 root — "Distribue cet argent en trois parts" — so the repair is anchored on
its two sentences, not on the word.** The C-n- class stays off limits:
`mnalu`, `snkrawah`, `qnbsranan`, `tnaga` were all offered and all refused,
because `<n>` perfective and `<m>` actor-focus share a slot.

The map layer adds five. `winuk`→`hwinuk` is **his own cross-reference** — his
note reads 無疑是 XWINUK 的縮略形式；參 XWINUK, and X is his h. The other four are
the final-g class already known from 路 `elug` and 餵養 `tabug`, each confirmed
by HIS Chinese: `snpu`=`snpug` 數過 (his 沒辦法數了), `msnulu`=`msnulug` 恰好
(his 就在那一刻), `lubu`=`lubug` / `lmubu`=`lmubug` under his LUBU 樂器.

**`psilin` was the sixth, and its refusal is the lesson.** His Psilin sits under
his own headword SILING, so the ng is his and the argument was sound. But a key
`psilin`→`psiling` reads to the cross-entry root projection as "append g", and
it re-applied that to his RAW `psiling` (3×) and `mpsiling` — putting `psilingg`
and `empsilingg` on the page. It bought 1 dark and cost 4. **A respelling that is
right about the word can still be wrong about the machine, and only the census
catches that, never the argument.** Compare batch 155: a gain of the right size
is not a gain of the right kind. Here it was a *loss* wearing a gain's clothes.

Still refused: `tabu` 5× (homograph — 餵養 and a hardwood share the token, this
map is token-keyed, same blocker as `bir`) and `tksaw` 5× (his own `Xksao`
already owns `hksaw`; sending `Tksao` there would erase a distinction he drew).

+9 map occurrences / +14 transcription occurrences, 0 de-verified.
96.9615% → **97.0109%**. Roughly 445 spans to the percent.

## Assert the replacement COUNT, or you will unhook the audio (batch 161, 2026-08-02)

Batch 160 opened positions 0 and 1 of the m-read-as-n sweep; batch 161 worked
the rest of that list. **45 candidates, 18 accepted, 27 refused** — and the
ratio is the point. The sweep proposes, his French disposes.

**Tense in his French is the discriminator.** `ntaga` is the clean case: "je
t'attendrai" is FUTURE and `n-` is past, so the letter cannot be an `n`. The
same test refuses `Nngangax` "A partir du fait d'être muet", a genuine `n-`.
The best of the eighteen is `nlut`, because **he flagged it himself**: his text
reads `Asi nlut (m'lut ?) xeaan`, question mark his. `mrut` 按住 against his
"en faisant pression sur lui" answers a question the book had already asked.

The refusals sort into five kinds, all worth keeping: C-n- infix (`snkrawah`,
`tnaga`, `qnbsranan`, `sneelug`, `tnquri`, `sneuwit`, `snka`, `snnru`), genuine
`n-` prefix (`nngangah`), false friends (`nilaq` his 菇類 vs `milaq` 碎粒;
`narung` "a obtenu le prix" vs `marung`, a man's name), unglossed target
(`ntlawa`, `nruq`, `nay`, `nhnaan`, `nsntug`, `nsleelug`, `niyak`, `snuk` — a
word with no Chinese cannot confirm anything), and **homograph**: `mnalu` at 5
occurrences would have been the largest single gain in the batch and is refused,
because his MALU prints Mnalu "s'entr'aimer" and his NALU prints Mnalu "qui
tient la place" — the same raw string in two entries.

**THE TRAP, and it is a new one.** The first run replaced 51 strings where 36
were expected. The extra 15 were inside `"a"` fields — **audio filename slugs**,
e.g. `ex_qpaxan_so_manu_ka_ntqeli_tqean_so`. Renaming one in the JSON renames
nothing on disk. It unhooks the recording, silently, while the page still
renders perfectly and the dark count still goes up. Nothing about the census
would ever have shown it.

It was caught only because the patcher asserted a replacement COUNT PER TOKEN
(each of these words occurs once in the book, so exactly 2 — one in `data/`, one
in `site/entries.js`). **Any raw-text patch of `data/` or `entries.js` must mask
`"a": "..."` values before substituting, and must assert its counts.** The
patcher now does both, and batch 160 was re-checked against the same fault and
is clean. Compare [[shipped-is-not-the-same-as-fixed]]: a green census is not
proof the thing you did not measure still works.

+18 occurrences, 0 de-verified. 97.0109% → **97.0513%**.

## Two refutations and a second witness (batch 162, 2026-08-02)

Two candidate veins were opened and killed by measurement before the batch that
worked, and the refutations are the durable part.

**An entry-mate rung would have been wrong.** 326 pale occurrences are words his
own dictionary lists as SUBS of an already-verified headword; `Empskeagul` is
glossed 同上（d°），未來式, "same as above, future tense". That reads like the
dictionary vouching structurally for a form the gloss-agreement rungs cannot
hear. Measure it: of those 326, the number both in the modern lexicon AND
analysable as an affixation of their own verified parent is **zero**. They are
not pale because a gloss test rejects them — they are pale because no modern
source attests them. **Always ask why a bucket is failing before building the
machine that would rescue it.**

**A flat tally is what a mined-out seam looks like.** Tallying every
single-letter substitution that lands a pale type on a lexicon word gives u→a
47 occ, n→m 33, a→u 25, l→h 22 — no dominant class, and the top entry is false
friends (`rngut` féconder vs `rngat` crier). When batch 161 found the n→m class
it stood out; nothing stands out now. Edit-distance-1 is done.

**What worked: `PQ_MIN` discards hapaxes UNREAD.** The parquet gate drops every
type the ILRDF corpus saw once, because an ASR hapax is as likely a mis-hearing
as a word. Correct in bulk — but 15 of those hapaxes are words on this page,
and that means each already has a second witness: **Pecoraro typed it in 1977.**
A 2020s acoustic model cannot mis-hear its way onto a string a French priest
typed fifty years earlier; the witnesses have no path to each other. So the gate
is not loosened, it is ANSWERED per word, in `PARQUET_HAPAX`.

**The coincidence argument fails on short strings, and the rule was made to
cost something.** At two or three letters chance can reach a real string. `rih`
is refused at SIX occurrences — the largest single gain left on the page — even
though his 幾乎－接近－有點像 fits the parquet's `qhuqil kana rih saw psahug
dhyaan` ("killed them all, almost as a punishment to them") rather well. Batch
146 pinned it, and batch 159 showed the only honest way out: `nta` went dark
because **a person spoke for it**, not because a gate moved. One ASR token is
not a person. `kn` is refused twice over — two letters, and its one occurrence
is inside `Fu-kn-su`, the romanized Japanese 撫墾署 split on its hyphens.

Like every corpus source this widens `seen`, never `lex`, and vouches for a
SPELLING and not for his gloss.

+21 occurrences, 0 de-verified, 0 new pale types. 97.0513% → **97.0986%**.

**The tail is now flat: 873 pale types over 1,258 occurrences, 587 of them
occurring exactly once, and the top 24 types (9% of the mass) are almost all
standing refusals.** There is no big fish left; from here every batch is
individual adjudications, not sweeps.

## Deploy

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6   # project: pecoraro-taroko
```
