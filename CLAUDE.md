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
`tools/orthography/build_modern_map.py`, 6,529 tokens of which 4,555 actually
change the spelling) maps corpus tokens to
modern spellings; lookup order in `modernize()` is
WORD_OVERRIDES → MODERN_MAP → `charRules()`. Map tiers:
- **id** (1,095) — original spelling already attested in the omnibus; left unchanged
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
- **M** (514) — hand-curated, gloss-verified (`tools/orthography/manual_map.json`).
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
- **L** (251) — the former review queue, adjudicated case-by-case against Chinese
  glosses (`tools/orthography/llm_map.json`). Key discovery from this pass:
  Pecoraro k before a consonant is very often modern q (kbsulan→qbsuran,
  kpaxan→qpahan, klaxang→qlahang), and his q is often modern k (qeulit→qowlit,
  tmataq→tmatak). ~149 cases were deliberately left unmapped (false friends like
  qmapax "spread" ≠ qmpah "work", particles, unidentified loans) — they're in
  modern_map.json's "review" key.
- **A** (468) — generated candidate, attested + Chinese-gloss-confirmed.
- **B** (1,343) / **B-rules** (27) — unique attested candidate via safe rules.
- **T** (241) — sister-dialect triangulation: Toda/Tgdaya cognates VALIDATE which
  generated Truku-shaped candidate is right (never supply spellings directly).
  Tgdaya folds l→r, o→u, d→j/t→c before i; both sisters also indexed by
  affix-stripped cores (≥5 chars) since cognates are usually differently-derived
  forms of the same root (baxang vs qbahang). Ties broken by weighted edit
  distance using measured correspondence odds (o→u/x→h cheap at 0.2; keeping
  o/x, or l→r, expensive at 0.8 — l usually stays l in Truku).
- **P** (1,223) — root-consistency projection: a resolved family member fixes the
  stem correspondence; unresolved hw/sub/paradigm forms of the same entry inherit
  it (infix-aware: mn/um/nm/m/n after the first consonant; affixes converted by
  the near-universal rules only). Mostly unattested by definition — the point is
  inheriting a verified stem and protecting derivatives from the char rules.
- **R** (750) — relative inheritance. The other tiers test WHOLE words against the
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
- **E** (162) — projection into his own example sentences. Tier P refuses example
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
- **N** (75) — proper names. "Sapah Sibar u…" — Sibal is a man, and the blind rule
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
- **V** (17) — elision-mark variants. His two marks put the same word in two map
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
every one is French — 20 fields, 51 occurrences, 38 types, not one Truku word
among them.

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

## Deploy

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6   # project: pecoraro-taroko
```
