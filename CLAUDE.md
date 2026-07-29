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
  by mode: modern gains H and J (DIMA→JIMA, d→j before i), loses O (o→u), and keeps
  a 4-form X row (map `id` tier). It is recomputed on toggle, not cached.
- Toggling while browsing follows the words, not the letter (X → H), via
  `rerender()`; calling `render()` there would turn the listing into a search.
- A–Z is the 🔤 sheet button, shown on the cover and in results alike. The strip
  the pre-redesign code built along the bottom of the cover is gone for good: it
  was an opaque band across the "FERDINANDO PECORARO MEP" byline, and it was
  unreachable from a listing. Don't reinstate `#alpha-row`.

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
`tools/orthography/build_modern_map.py`, 5,597 tokens) maps corpus tokens to
modern spellings; lookup order in `modernize()` is
WORD_OVERRIDES → MODERN_MAP → `charRules()`. Map tiers:
- **id** (1,103) — original spelling already attested in the omnibus; left unchanged
  (also protects loanwords like `lemon` from the char rules). "Unchanged" means
  his capitals and apostrophes, not his diacritics — `norm()` ignores those, so
  the tier used to hand back `däxa` for `däxa`.
- **M** (222) — hand-curated, gloss-verified (`tools/orthography/manual_map.json`).
- **L** (254) — the former review queue, adjudicated case-by-case against Chinese
  glosses (`tools/orthography/llm_map.json`). Key discovery from this pass:
  Pecoraro k before a consonant is very often modern q (kbsulan→qbsuran,
  kpaxan→qpahan, klaxang→qlahang), and his q is often modern k (qeulit→qowlit,
  tmataq→tmatak). ~149 cases were deliberately left unmapped (false friends like
  qmapax "spread" ≠ qmpah "work", particles, unidentified loans) — they're in
  modern_map.json's "review" key.
- **A** (474) — generated candidate, attested + Chinese-gloss-confirmed.
- **B** (1,387) / **B-rules** (27) — unique attested candidate via safe rules.
- **T** (257) — sister-dialect triangulation: Toda/Tgdaya cognates VALIDATE which
  generated Truku-shaped candidate is right (never supply spellings directly).
  Tgdaya folds l→r, o→u, d→j/t→c before i; both sisters also indexed by
  affix-stripped cores (≥5 chars) since cognates are usually differently-derived
  forms of the same root (baxang vs qbahang). Ties broken by weighted edit
  distance using measured correspondence odds (o→u/x→h cheap at 0.2; keeping
  o/x, or l→r, expensive at 0.8 — l usually stays l in Truku).
- **P** (1,230) — root-consistency projection: a resolved family member fixes the
  stem correspondence; unresolved hw/sub/paradigm forms of the same entry inherit
  it (infix-aware: mn/um/nm/m/n after the first consonant; affixes converted by
  the near-universal rules only). Mostly unattested by definition — the point is
  inheriting a verified stem and protecting derivatives from the char rules.
- **R** (753) — relative inheritance. The other tiers test WHOLE words against the
  omnibus, so a regularly derived form of a well-attested root falls through:
  `nduk` is unattested but `mduk` 關（門、窗）and `mnduk` are right there. Tier R
  peels prefix/infix/suffix off the Pecoraro token, matches the core against
  affix-stripped cores of the omnibus (≥3 chars, ≥2 supporting glossed words),
  and reattaches the affixes through the near-universal rules. Skips rather than
  guesses when two readings survive. The gloss veto here is a *rejection* test —
  no character in common at all — not `gloss_overlap()`, which wants a contiguous
  run and so rejected nduk/mduk for stating the same thing in a different order.
- **KL** (42) — keep-l guard: tokens frozen against a wrong l→r.
- **D** (126) — morphology over an already-solved base. Lowking Nowbucyang,
  太魯閣語構詞法研究 (*Word Formation in Truku*, 2008) §3.4: Truku reduplication is
  CV- or CVCV-, and since Truku doesn't write the schwa, CV- surfaces in the
  orthography as a **doubled initial consonant** (hmadan → hhmadan "many of them
  clearing"). Same treatment for the mn-/n- AF preterite and the collective d- on
  a personal name (Aman → dAman). None makes a new lexeme, so the answer is
  (his affix) + the modern spelling of the base. Pass order is
  id/A/B/T → P → R → KL → S → N → D → E → G, so any of those earlier tiers can
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
- **E** (162) — projection into his own example sentences. Tier P refuses example
  tokens (a sentence is mostly other people's words), which also shut the door on
  a word's own family: `kxebong` occurs nowhere but the single sentence under
  XEBONG and went on screen as *khebung. A sentence token qualifies only if it
  CONTAINS a stem the SAME entry has already resolved, and one ambiguous
  candidate disqualifies it. Log: `tier_e_log.txt`.
- **S** (66) — attestation in running speech. Same claim as A/B — "this exact word
  exists in modern Truku" — but asked of `C:/dev/ILRDF/ILRDF_texts.xlsx`: 47,517
  transcribed Truku utterances, 277,014 tokens, cached as `spoken_truku.json`. A
  dictionary skips exactly what a transcript is full of (names, particles, the
  shape an inflected root really takes). Candidates are the rule-consistent
  readings of his token, and exactly ONE must appear **twice or more** — a hapax
  in an ASR transcript is as likely to be a mis-hearing as a word. Runs AFTER the
  KL guard, and a hit that flips an l is refused when the keep-l reading of the
  root is itself a modern word: `mk'alang` matched `karang` 蟹 in speech, but his
  word is built on `alang` 部落. Log: `tier_s_log.txt`.
- **N** (74) — proper names. "Sapah Sibar u…" — Sibal is a man, and the blind rule
  renamed him. Nothing attests a name and no tier above reaches it, so it falls to
  the char rules, the one population where they are guaranteed to be guessing.
  Test: capitalized mid-sentence in one of his own examples (only a proper noun
  is) AND never written lowercase anywhere in the book. Those keep their l; o→u,
  x→h and final -ai/-ao still apply, so `Pisao`→Pisaw, `Labai`→Labay, `Sibal`
  stays Sibal. Log: `tier_n_log.txt`. Names are never allowed to seed tier G.
- **G** (31) — root projection ACROSS entries. Tier E only sees the entry a token
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
- Currently one: `q'nao` → `qusul` (garlic). All 32,212 omnibus words swept; the
  modern Allium field is `qusul` / `pixil` / `neygi` / `sangas` and nothing is
  shaped like /qnaw/. He has no `qusul`-shaped word either, and he separates the
  native `Q'NAO` from the loan `NEGI` = oignon.

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

## Deploy

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6   # project: pecoraro-taroko
```
