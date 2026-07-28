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
- **M** (201) — hand-curated, gloss-verified (`tools/orthography/manual_map.json`).
- **L** (255) — the former review queue, adjudicated case-by-case against Chinese
  glosses (`tools/orthography/llm_map.json`). Key discovery from this pass:
  Pecoraro k before a consonant is very often modern q (kbsulan→qbsuran,
  kpaxan→qpahan, klaxang→qlahang), and his q is often modern k (qeulit→qowlit,
  tmataq→tmatak). ~149 cases were deliberately left unmapped (false friends like
  qmapax "spread" ≠ qmpah "work", particles, unidentified loans) — they're in
  modern_map.json's "review" key.
- **A** (474) — generated candidate, attested + Chinese-gloss-confirmed.
- **B** (1,350) / **B-rules** (24) — unique attested candidate via safe rules.
- **T** (255) — sister-dialect triangulation: Toda/Tgdaya cognates VALIDATE which
  generated Truku-shaped candidate is right (never supply spellings directly).
  Tgdaya folds l→r, o→u, d→j/t→c before i; both sisters also indexed by
  affix-stripped cores (≥5 chars) since cognates are usually differently-derived
  forms of the same root (baxang vs qbahang). Ties broken by weighted edit
  distance using measured correspondence odds (o→u/x→h cheap at 0.2; keeping
  o/x, or l→r, expensive at 0.8 — l usually stays l in Truku).
- **P** (1,032) — root-consistency projection: a resolved family member fixes the
  stem correspondence; unresolved hw/sub/paradigm forms of the same entry inherit
  it (infix-aware: mn/um/nm/m/n after the first consonant; affixes converted by
  the near-universal rules only). Mostly unattested by definition — the point is
  inheriting a verified stem and protecting derivatives from the char rules.
- **R** (836) — relative inheritance. The other tiers test WHOLE words against the
  omnibus, so a regularly derived form of a well-attested root falls through:
  `nduk` is unattested but `mduk` 關（門、窗）and `mnduk` are right there. Tier R
  peels prefix/infix/suffix off the Pecoraro token, matches the core against
  affix-stripped cores of the omnibus (≥3 chars, ≥2 supporting glossed words),
  and reattaches the affixes through the near-universal rules. Skips rather than
  guesses when two readings survive. The gloss veto here is a *rejection* test —
  no character in common at all — not `gloss_overlap()`, which wants a contiguous
  run and so rejected nduk/mduk for stating the same thing in a different order.
- **KL** (53) — keep-l guard: tokens frozen against a wrong l→r.

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

**Lexical replacements** live in `manual_map.json` alongside the respellings.
There is currently one: `q'nao` → `qusul` (garlic). It is a substitution, not a
respelling — a sweep of all 32,212 omnibus words (Allium glosses, 15 fuzzy
shapes of /qnaw/, every `*naw*`/`*now*`/`*nau*` substring) found no reflex of his
word, and no `qusul`-shaped word exists anywhere in his 1977 dictionary either.
The two lexicons simply do not share a word for garlic. Keep such cases rare and
list them here, because the toggle otherwise promises spelling only.

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
