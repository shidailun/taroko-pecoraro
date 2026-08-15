# Pecoraro Taroko — 4-language Truku dictionary

Digitization of Ferdinando Pecoraro MEP's *Essai de dictionnaire taroko-français*
(SECMI, Paris, 1977). Original is Truku (Taroko) → French; we add English +
Traditional Chinese (translated from the French, draft pending native review).

- Live: https://pecoraro-taroko.shidailun.com (Cloudflare, `wrangler.jsonc`).
  The legacy address https://pecoraro-taroko.netlify.app (site_id
  `d6e80a1c-405b-4bf9-8977-3630174261c6`) is frozen behind a "we moved" banner.
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

### The gloss test — the only non-circular question

- **The gloss of the candidate must match the gloss of the entry it renders in.**
  A shape hit plus high frequency is not evidence — `bitaq` was 321× and wrong.
- **Search from the meaning, not from the letter.** Ask the omnibus which modern
  word carries his Chinese, rather than deciding a letter and hoping a word exists.
- **An attested value can still be a wrong value.** Attestation tests cannot catch
  this; only the gloss can.
- **A gloss score can land on the apparatus** (batch 218). His QALIT 剪刀 scored 3
  in tier A — the gloss-PROVED tier — on the substring **的詞根**, "…'s root". His
  note and `qlit`'s register row were both saying *this is the root of
  something*, and `gloss_overlap` counted that as agreement about MEANING.
  `meta_a.py` re-scored all 419 glossed tier-A entries with metalinguistic
  phrases stripped from both sides: **418 survive, exactly 1 collapses.** The
  tier is sound; the one hit was a freeze onto 溢滿.
- **A wrong-looking gloss is a question, not a verdict** — the paradigm answers it.
- **An attestation test over pale words is circular** (batch 204). Pale MEANS not
  in `attested_modern`, so re-asking it returns 0 of 37 across the top seven
  cards. The only non-circular question is the meaning test: does a DIFFERENT,
  attested word spell his? For RNGUT 懷孕 it is `mshjil` and for SNOXEL 嫉妒 it is
  `hkrig` — different roots, so there is no respelling to find and the pallor is
  correct.
- **A modern homophone is not a freeze** (batch 204). `sgsapat` 姦淫 (2× parquet,
  1× Bible) acquits his SAPAT 放蕩 head, which the register also lists as 舖床:
  both roots are real. But the acquitted head still cannot license its family,
  because it is dark on the OTHER one.
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
- **A gloss instrument that falls back to an example gloss manufactures its own
  only hit** (batch 221). `logs/tail221.py` runs batch 204's different-root test
  over the tail: reverse the blocker to his token, take his Chinese, report the
  register word sharing a Han character that is closest in shape. Twelve of
  fourteen rows are noise — one common character (著, 子, 一, 人) at 2–4 edits.
  The one row that looked real, `mqlaq → mqraq` at one edit sharing 抓, is the
  freeze batch 218 paid three pairs to remove, and the 抓 came from his
  EXAMPLE's gloss because the token has no headword Chinese. Mark those rows and
  discount them (batch 203) and the tail has no candidates at all. Keep the
  negative result; don't rebuild it (closed-instruments table).
- **A single gloss row is not the register's answer; the family is** (batch 200).
- **A multi-letter affix article scores its MODERN prefix** (batch 203). `mpa`
  scores 0 and `emp` scores 689; the zero is the tier-W schwa showing up as a
  lookup miss, not evidence against his card. `HAND_AFFIX` names the string to
  count.
- **A sentence-corpus gloss is not the headword's gloss** (batch 203). `bgiya`
  appears in 都是專捕虎頭蜂人 but its own row reads 打緯線; `srcing` is the 虎頭蜂.
- **Two supporters must be INDEPENDENT, not the same test twice** (batch 203);
  unanimity over one item is not unanimity. Closest-string alone proposed a
  Japanese surname for a given name; his own `(m)`/`(f)` tag checked against
  the register's 男名/女名 refused nine of fifteen.
- **A pricing count must exclude his parenthesised apparatus too** (batch 222) —
  batch 218's rule reaches occurrence COUNTS, not only gloss scoring. `qaya`
  showed ORPHAN 2 against SERVED 1, and the second occurrence was the string
  `QAYA` inside his own French sub-form `Pqaya (Est-ce de la R. QAYA ?)`, a
  cross-reference. Read the occurrences before believing a 2. Unstripped on the
  gloss side the same fault scored `xalong`'s 松樹 card SERVED against a value
  glossed 人名（男）, on the 人 of 太魯閣人.

### His card, his family, his own book

- **The family is evidence in both directions.** A family that already agrees
  convicts a head that keeps its own letters; it also acquits.
- **A card head that is dark for the wrong reason licenses nothing beside it**
  (batch 199). His TABE `-un`/`-i` slots looked like clean gaps beside a dark
  `tbiyan` — which is glossed 下來, not 犁. Six wrong words in one ruling. Run the
  gloss test on the neighbour you are leaning on, BEFORE writing the value.
- **A pale slot beside three dark ones is the cheapest question on the page**
  (batch 199, the instrument that cleared 99%). His card is a paradigm, so ask
  what every other slot on it says, not what the analyser can say about the word.
- **Decide slot by slot when a homophone exists**, not once for the root.
- **Same root in two dialects is not a licence to merge two cards.**
- **A sibling is only a sibling if it is the same card.** A ruled form one slot
  over licenses its neighbour — but check which headword it comes off first:
  `pngraq` is his Png'laq off NG'LAQ 愚蠢, not G'LAQ 拿取 (batch 198).
- **His own parenthetical is testimony that two spellings are one word** (batch
  200). Where he writes `X (Y)`, `X (vl. Y)`, `X (Y ?)` and the map sends the two
  to different values of which exactly ONE is dark, the pale side should render
  what the dark side renders — a consistency fix, not a new attestation claim.
  **The dark side still has to pass the gloss test**: 7 of 17 were refused because
  the dark value is dark on a homograph, and following it would spread a freeze.
- **His parenthetical can carry the JOINED spelling and his running text the
  split one** (batch 231). `Lmobong ko payai mo sayang, iso ka (isoka) npkoyoç`
  writes both, so there is no choice of readings to make: `iso → isu` and
  `ka → ka` are dark, `isuka` was pale, and the pale side renders what the dark
  side renders. **A map value may be TWO WORDS** — `attested()` splits on the
  space and `build_verified.py:424` takes the min over the parts, so both halves
  must be verified, and anything asking "is this value verified?" has to split
  too (the suite's `ruled` handler did not, until this batch).
- **"No card, no candidate" is a claim about the whole book** (batch 235), and it
  is repaired by searching for the CARD, not for the letter — batch 229's rule
  one level up. His `nalong` was refused that way; his MALONG card sits 76 pages
  off, tagged `(R)`, glossed *une rondelle d'ivoire … marquant le mérite … suite
  à un acte de bravoure*, which is the sentence's own 得獎 verbatim. The verdict
  survived on three other legs (the scan reads `n`; batch 216 refuses swapping an
  initial consonant; 象牙 returns 0 register rows and nothing sense-carrying sits
  within 2 edits) — as in batch 232, a premise wrong from the start with the
  verdict still sound.
- **His own inflected slot spells the stem, and a MANUAL pin can drop a letter
  too** (batch 219). `tglgli → tgrgri` and `mtlgli → mtrgri` sat pale beside eight
  dark slots of his G'LI" 舞蹈 card — `grig`, `mgrig`, `rmgrig`, `grigan`,
  `grigun`, `pgrig`, `trgrig`, `tgrgrigun` — every one carrying a final `g` the
  two pale ones lacked. His own `Tglgligun → tgrgrigun` is one suffix over from
  `tglgli` and writes the `g`. Restoring it verified both at code 2 off the
  ladder, no hand-ruling. Note `mtlgli → mtrgri` was **tier M**: the missing
  letter was hand-pinned, so batch 201's contradiction test must be run over
  manual entries too, not only over char-rule output.
- **A slot pinned to TRACK a head goes stale when the head is re-ruled** (batch
  223). Batch 201 moved his QQ'LANG head from `qqlang` to `qqrang` and the t-
  slot kept the `l`, leaving six of seven forms across two cross-referenced cards
  on `r`. This is the other end of `inflection.py:1670`'s SIBLING SEAM — a
  ruling that stops at the form the map happened to show is half a ruling, and
  the half left behind is findable from the pale side. **Grep the legacy
  `logs/b*.py` pin files, not only `dom*.py`**: `b57.py:116` carries
  `"tqq'lang": "tqqlang",  # qq'lang>qqlang;  was TQQRANG` — the comment records
  both what it was tracking AND the value it displaced, so restoring it finishes
  a supersession instead of overruling a refusal.
- **A zero character-overlap is not a refusal when the candidate is the char
  rules' own output on HIS OTHER spelling of the same headword** (batch 223). His
  XOIL (XOWIL ?) 舀小米酒的杓子 shares no character with `huwir` 湯匙, which is
  why no overlap instrument ever surfaced the card — and `xowil` derives to
  `huwir` by x→h, o→u, l→r with nothing left over. Batch 204's different-root
  test is what settles it: the register's ladle family (`isux` 飯瓢, `sahug`
  水瓢, `wihi` 水瓢、湯匙, `hahug` 舀) contains no word reachable from either of
  his spellings, so there is no rival root and nothing to respell away from.
  **The general sweep is now exhausted** — **SUPERSEDED, batch 225**, see "read
  one parenthetical" below: headwords of the shape `X (Y ?)` whose two sides map
  to different values of which exactly one is dark returned ONE row in 1,967
  entries, and it was this one. The sweep read a SINGLE parenthetical per tag and
  so never saw his 92 compound ones; re-parsed the shape returns **10**. The XOIL
  ruling stands — only the exhaustion claim fell.
- **His TAG SHAPE separates a variant from a posited root** (batch 223). Batch
  200's parenthetical rule applies to `(KL'ULUS ? - R. = ULUS ?)`, which names
  another spelling of the headword KLUULUS — his ULUS card confirms it by writing
  "la R. de KL'ULUS (=disperser)". It does NOT apply to `(R. ? - R. = POXEL ?)`,
  where he posits a bare ROOT and marks it with his own question mark: KPOXEL is
  not POXEL, the head is already served by `qpuhir` 耳聾, and there is no
  inconsistency to fix. Bare roots he posits — `dux`, `eydang`, `eysa`, `ihur`,
  `iyak`, `kuy`, several marked on the page (IYAQ 這會是 MIYAQ 的詞根嗎？;
  UKWI 從未單獨出現) — are a settled class in batch 203's sense, and naming the
  class is not a door to clear it.
- **The sibling seam can span two CARDS, and `contra223.py` cannot see that**
  (batch 225). That instrument keys on his `l`/`x` rendering both ways inside ONE
  entry. His KUBWI head sat on `kubuy` while batch 49 (`Pkbuyo → pkbuyu`) and
  batch 201 (`Kmubui/kmbui → kmbuyu`) had already put seven spellings of the same
  root on the `buyu`/`kbuy-` stem — on the BUYO card, which his own tag names as
  the root. **When a card's tag names a root, rule the head against THAT card's
  ledger**, not against the head's own shape.
- **Batch 223's `X (Y ?)` sweep was not exhausted — it read one parenthetical**
  (batch 225). Ninety-two entries carry a COMPOUND tag; his KUBWI is
  `(KBUI ?) (R. = BUYO ?)`, and the sweep saw only the second. Re-parsed with
  every parenthetical and batch 223's tag-shape rule applied, the shape returns
  **10** rows. Two live pale-side ones remain — PSAANAK `(PSAANAQ ?)` and SA'MUL
  `(S'MUL ?)`, the latter the mirror shape with his HEAD pale. The other five are
  GREEN-side, which is a different question: green means no map entry fired, so
  the fix is itself a new spelling claim.
- **His dropped letter can be 21 pages from the card that spells it** (batch
  229). `pqeli` lacked the `x` that fifteen slots of his XOQEL 死亡 card write,
  including the `Pxoqel` "Tuer" paradigm — the same fault as batch 219's
  `tglgli`, but the evidence was not on the card the token sits on. Search the
  ROOT's slots book-wide, not the neighbouring ones.

### His orthography and the char rules

- **A speaker's answer is a RESPELLING only when it is shape-continuous with his
  token under his own correspondences; otherwise it names the MEANING** (batch
  242, over a 71-item answer sheet from a Truku informant). Asked how `Kndoto`
  手鐲 is written today a speaker writes `sirug` 帶項鍊;手鐲 — correct, and it
  buys nothing: it does not say his KNDOTO survives, it says the modern word for
  a bracelet is `sirug`, which is a tier-X claim nobody was asked to argue. The
  test is his own `o→u`, `l→r`, `x→h`, his `'`/`"` schwa, `ç` for `x`, final
  `-e` for `-i`, `q` for modern `k`. Sorted by it, that sheet was 24 respellings
  and 47 answers about the world. **The gloss test still runs on the 24** — a
  speaker lands on homographs exactly as the map does, and four of his answers
  were listed words with unrelated glosses (`rqraq` 砍倒 for the itch card,
  `basiq` 石櫟 for the glutton card, `rangi` 犯忌 for the leftovers card, and
  `pgagu` 笛子, which is the freeze batch 219 already reverted — the sheet
  reproducing a mistake the project made and undid is the best control on it).
- **Where two answers about one root disagree, the two that agree win** (batch
  242) — batch 203's independence requirement, applied to testimony. Name the
  overruled answer in the log rather than dropping it.
- **A speaker attests; he does not spell.** `HAND_SPOKEN` (`inflection.py`)
  widens `seen` and never supplies a value — the spelling must already be
  reachable through `manual_map.json`, `lexical_map.json` or the char rules.
  Use it where no corpus holds the word at all and the slot family is spelled
  for its neighbours (batch 224's sister test, passing positively).
  `build_verified.py` prints those types on their own line, separate from every
  corpus count, because this is the one attestation on the page that is a person
  and not a document.
- **`lexical_map.json`'s `_`-prefixed comments are written refusals in a data
  file, and tier X outranks tier M** (batch 242). Two informant answers were
  inert before they were wrong: `mngusyex → mngasih` hit batch 93's
  `"mngusyex": null` and the generator printed
  `curated keys that never landed [BLOCKED]`; `sm → smdalih` hit batch 93's
  `"sm": "sm"` and landed **silently**, because a lexical null blocks loudly and
  a lexical identity blocks quietly. `build_modern_map.py` tests `if t in
  lexical … continue` BEFORE `if t in manual`. Grep that file, not only the
  logs, before writing a value.
- **His initial consonant takes a modern reflex, never zero** (batch 216). When a
  gloss match requires DELETING a letter his page writes, test that letter
  against his other heads with the same onset first: his L- surfaces as `r`
  (`lbagan → rbagan`, `lb'nao → rbnaw`) or stays `l` (`lb'lak → lblak`). `gluq`
  carries his LG'LOQ 樹脂 gloss verbatim and is still refused, because dropping
  the L is a lexical substitution wearing a respelling's clothes.
- **His typewriter joined a clitic to its host, and the join is findable
  mechanically** (batch 231): take every token beginning with the clitic whose
  remainder he ALSO writes standing alone ≥20×, **and which he does not CARD**.
  Over his whole book that returns exactly one token per clitic — `kasayang`,
  `isoka`, both hapaxes. The card exclusion is doing the work and is not a
  fitted parameter: without it `ka` also returns `kana` 全部 (435×) and `kaya`
  蚊帳, whose tag reads `[emprunt jap./chin.]` — a hapax, so no frequency guard
  would have caught it. **A word he gives a headword to is a word he asserts
  exists, not a slip.** The outside voice is the corpus: `ka sayang` 403× in the
  parquets and the join 0×, fifteen of them in his own frame.
- **Search his own book, not only the register.** `nilit` looked like an override
  of `mirit` 山羊 until the count came in: he writes `milit` 15× and `nilit` 2×.
  His own text spelled it. Same instrument proved `dbsnawan` an ethnonym —
  `dSbnawan ni dTroko` stands it beside the Truku.
- **His orthography can refuse a candidate the gloss accepts** (batch 215). When
  a modern word carries his meaning exactly but needs a cluster he doesn't write,
  ask whether he had a spelling for that cluster and used it elsewhere. In 398
  pages he never writes `gr` — the only two hits are the French *grand* and
  *grandeur* — and his correspondence for modern `gr` is `gl`/`g'l`, in 81 map
  values (`glangan → grangan`, `g'laq → graq`). So `sgrangan` 生銹 would have
  been `sglangan` in his hand, a shape his book does not contain, and his SLANGAN
  鏽 is regularly `srangan`, which no source lists. Different root, nothing to
  respell. The test is cheap and reproducible: count his cluster, count the map's
  correspondence for it, and check the crossing does not already occur.
- **A char-rule output a couple of edits from a listed word is not a "fake
  word"** (batch 230). `b57.py:120` froze `snoxel` to identity to suppress
  `charRules`' "SNUHER"; `snuher` is two edits from `sneuhir`, the gap being the
  epenthetic schwa the char rules cannot supply. Before freezing an output as
  nonsense, measure its distance to the register.
- **His own ALPHABETICAL ORDER is testimony about a letter** (batch 230), and it
  is cheaper than the scan. His XUBAO sits between X'TOL and XUGUT among the XU-
  words, so the vowel cannot be an `i` however well `hibaw` 刀鋒 / `hnibaw` 被割傷
  fit his XUBAO/XNUBAO pair. Batch 68 had held that card for want of an attested
  bare form; the bare forms exist now, the premise is repaired, and the verdict
  stands — because `u → i` occurs **0** times in 7,371 map pairs while `o → u`
  fires 1,804 (batch 215's instrument, returning zero).
- **A pin that spells what `charRules` already spells is still load-bearing**
  (batch 227, as batch 218's `mqlaq → mqlaq`). Deleting a reverted freeze's map
  entry does not return the word to his letters: `charRules("s'mul")` = `smur`
  unaided, so the freeze's string comes back as a GREEN span. Assert the char-rule
  output in the log, or a later tidy-up will read the identity pin as a no-op.
- **A char-rule contradiction inside one root is a bug, not a variant** (batch
  201, three of them: `mp'yax`→`mpyah` beside `iyax`, `upsk'la`→`upskra` beside
  `skla`, and the DLUT crossing). Where `l→r` or `x→h` fires on one slot of a card
  whose other slots keep the letter, the char rule has overreached — check the
  siblings before believing the fallback.
- **A diacritic can be the whole distinction** (batch 201). His `ç` vs `x` is what
  separates KOYOç 雨 from KOYOX 女人—妻子; `plain()` strips it downstream, so a
  sweep keyed on shape will cross the two cards. The gained/LOST assertion is what
  catches it — `koyox → quyux` broke the 女人 card and was reverted.

### The scan — when to re-read the page

- **A word he CARDS closes the scan question without a crop** (batch 235, batch
  231's rule applied to batch 213's test). The class batch 213 catches is a token
  appearing ONCE; his KAXOI is a headword with a tag, both glosses, a `Mkaxoi`
  sub-form and a sentence under each — four independent writings of the stem, so
  there is no glyph to re-read.
- **Ask the scan before you blame the language** (batch 202). His French `m`
  renders n-like at page resolution. Crop the disputed glyph and a known `n` and
  a known `m` **from the same line** at 6×, and count legs.
  `damat`'s only row reads 恢復原狀, which would have refused `pdmati`; the five
  family members are all 菜餚/配菜 and his card agrees with them.
- **The scan decides WHERE the fix goes, not whether to act** (batch 212). A slip
  is corrected in `entries.js` (batch 208's `ln'xlax`); a reading the page really
  carries is respelled in the map, because the map is display-only and his letter
  is the record. His Q'NAO `mbuyan` is an `n` at 7× beside `bisol`'s `s` on the
  same line — and is still his 肚子 word, which his KUI card spells `mbuyas` in
  the same frame. `mbuyan → nbuyas`, source untouched.
- **Ask whether the string is even his before pricing a respelling** (batch 213).
  A token appearing exactly once in a book that repeats itself is a candidate for
  the scan, not for the register. His NII `smuwan` sat one letter from the listed
  `snuwan` 問什麼時候 — and the page reads `sknuwan`, a `kn` transcribed as `m`,
  which his own book spells four other times, all glossed 什麼時候. The blocker
  cleared by DELETING a map entry.
- **The scan question only opens when a rival reading exists** (batch 213). An
  edit-distance sweep around TMAGO 驕傲 found no proud word at all, so there was
  nothing for the glyph to be. Refused on batch 204's test instead: `dahu` and
  `psparu` carry the meaning off different roots.
- **His own `(?)` is testimony about the FORM, not about the transcription**
  (batch 224). Where he marks a paradigm slot uncertain, the scan still has to be
  read — page 196 at 8× against the `m` of `psnmaan` on the same line gave two
  legs against three, so `psnnai` is what the page carries and `entries.js` is
  untouched. His doubt is then evidence that the form itself is shaky, which is a
  reason not to tidy it into the regular shape his other four slots predict.

### The analyser — `roots()`, the peel, the swallowed vowel

- **The analyser cannot see reduplication.** `inf.roots()` has no rule for it, so
  every CC-/VV- form reports no root. That is a fact about the analyser, not a
  verdict about the word — strip the doubled onset by hand before believing it.
- **Restore a swallowed vowel only where the suffix replaced one** (batch 217).
  Widening `roots()`' restoration branch to the hortative was right for `-aw`
  and `-ay`, which displace the base vowel, and WRONG for `-i`, where that vowel
  is itself what separates two roots: it verifies his `Qnadi` (QADI 編織物) off
  `qnada` 已丟棄的 through `no_chinese()`, the one rung that skips the gloss
  test. Three of the four words the `-i` leg touched were already dark, so the
  count alone read as a bargain. **Price an analyser widening word by word, and
  guard it on an empty candidate list** — batch 164's peel guard is what makes
  a widening incapable of DE-verifying anything.
- **The sister sweep is closed** (batch 217). A pale word whose sisters in the
  same slot family are verified while it scores level 0 itself is the
  fingerprint of an analyser gap; over all 174 pale values it returns five, four
  of them traps already refused in writing (`qadi`/`qnadi`, `tbiyi`/`tbiyun`)
  and the fifth — `sapi`, his SAPE 小鋤頭 against `parih` — a refusal too. One
  ruling in the whole seam. Don't widen `roots()` again expecting a second.
- **Ask what the value you are REPLACING decomposes to** (batch 223). A pale
  value is not inert: `pttui` on his PT"TO 豎立 card looked like a dropped-letter
  artefact, and `ttui` turns out to be a listed root glossed 切、剁 — so the map
  was spelling his imperative-of-*erect* as an inflection of *cut*, the meaning of
  his OTHER card, T"TO 切割. That is the positive half of the argument for
  `pteetui`, and it costs one `roots()` call. **The same fact can refuse the
  neighbouring fix**: `t"tuan → ttuan` is dark off that same `ttui` 切 and his
  `T"tuan` is glossed 切成的塊－切割的情況, so it is CORRECT and must not be
  "made consistent" as `teetuan`. One notational defect, two slots, opposite
  verdicts.
- **The analyser's PEEL can land on a homograph, exactly as the map can** (batch
  224). `roots('graka')` returns one analysis, `('raka', 'g', …)` — it takes the
  `g` for a prefix and lands on `raka`, listed and glossed 人名（男）. The gloss
  test then scores a male personal name against his GLAQA 觀察—窺探—監視 and
  refuses, correctly, on the wrong candidate. **The tell is a pale head beside a
  dark, LISTED sibling of its own card** (`gmraka`, his Gmlaqa): the project has
  already accepted which root the card is, so the head has nothing left to prove.
  The instrument is to ask which listed forms spell the stem WHOLE — `empgraka`
  要埋伏 and `spgraka` 讓…去埋伏 prefix `graka`, not `raka`, which is what makes
  the `g` root and not affix. Then name the form whose own gloss carries his
  character: `grkaan` 監視;埋伏. The map needed no change at all; the ruling
  changed a COLOUR.
- **Silence is evidence only where the slot is spelled for OTHER stems** (batch
  224) — otherwise it is batch 217's empty candidate list wearing batch 220's
  clothes. His `psnnai (?)` was refused because the register spells **zero**
  forms of that syncopated stem, and that counts because the register DOES spell
  the same `-i` slot for its neighbours (`psnani` 要嚼爛, `psnaki` 要區別,
  `psnangi` 象徵性的做). Check the sisters before calling an absence a refusal.

### Refusals, premises, and the record

- **A label is not an argument**, and **a cognate explains a word but never spells
  one**.
- **A pin comes down when evidence overturns it, not when the rule tires**, and a
  pin naming one cause must be retired when a second cause appears.
- **Overriding evidence costs more than filling a hole.** Prefer the fix that adds.
- **A refusal can score the CARD's gloss against a word that is not the card's
  word** (batch 231) — batch 203's rule, arriving as a refusal instead of as a
  freeze. `dom219.py:233` refused `isuka` because "蓋住 is spuy, 覆蓋 is
  bbungan; different roots", but the 蓋住 is `Lmobong`; `isoka` is a pronoun
  plus a case marker and never had a candidate to find. Batch 204's
  different-root test is only as good as its LEFT-hand side: check the token
  being refused is the token the gloss is about.
- **A ruling that contradicts a written refusal must cite that refusal and say
  what new evidence retires it** (batch 219). Four went in without doing so and
  all four came back out — the suite caught them, not the reasoning. Three were
  bare `HAND_RULED` additions with **no comment beside them**, in a file where
  every other addition carries a paragraph; `HAND_RULED` darkens whatever is put
  in it, so an unargued entry is the metric deciding the spelling. The fourth,
  `pg'go → pgagu`, followed the dark side of his parenthetical past batch 200's
  own caveat: `pgagu` is 笛子 in the register, there is no 斑鳩 in it at all, and
  its 鴿子 is `byutux`. **Before writing a value, grep the logs for the word** —
  `dom*.py` refusal pins are prose and say why. A batch that can move the metric
  by overruling its own record is not measuring the book.
- **A consistency fix labelled "not a claim" is retired by the first
  attestation** (batch 220) — and the label is what makes it cheap. Batch 215
  gave the SLANGI card `-rngiy-` because his four siblings agreed, saying in
  writing "pale before, pale after — a consistency fix, not a claim". The
  register spells that root's syncopated stem in exactly four forms and not one
  writes the `y`: `psrngiun` 留一些, `psrngion`, `rngii`, `rngiun`. So
  `slngiyun → srngiun` (+1) and, in the same breath, `pslngiyun → psrngiun` —
  which was already dark and bought nothing but coherence, replacing an
  inference (code 7) with the listed word (code 1). **Repin a dark slot when the
  same evidence settles its pale sibling**, or the map renders one suffix of his
  two ways.
- **The register's SILENCE about a slot refuses the sibling** (batch 220). The
  same four-form query that ruled `-un` found no `-an` of that root in the
  syncopated stem, and no `-yan` anywhere on it — its 使留一些 is `pnsngari`,
  built on the FULL stem, which is his other card's root. So `rngiyan` and
  `pnsrngiyan` keep the inferred shape and stay pale. Evidence where there is
  evidence, inference where there is none; inventing `rngian` to tidy the
  paradigm is the metric deciding the spelling. **Assert the negative half in
  the log** — if an `-an` form ever enters the register, that is exactly the
  news that re-opens the two refusals.
- **Assert the POSITIVE half of a refusal, and name the form whose OWN gloss
  carries the character** (batch 221). A refusal of the shape "a different root
  carries this meaning" is only as good as the row it cites, so `dom221.py`
  re-reads that row — and failed twice on its first run, against the person
  writing it. Bare `bkiluh` is glossed 苦瓜;釋迦（植物名）, a plant: the 疥癬 is on
  `embkiluh` 長疥癬 / `knbkiluh` 疥癬的樣子. Bare `bukung` is 校長；首長: the 領袖
  is on `thowlang` 王、領袖或頭目. Batch 200's "a single gloss row is not the
  register's answer; the family is", enforced mechanically. Assert the negative
  half too, as a regex over the register rather than a list — a word matching
  the refused shape ever appearing is the news that re-opens the refusal.
- **A written refusal can rest on a premise that later goes false** (batch 227),
  and repairing it is not overturning it. Batch 221 refused `snmul` because "the
  whole card is pale head included — there is no dark sibling to reason from",
  which was untrue: his bracketed variant `S'MUL` rendered DARK on `smur` 濕冷, a
  tier-B projection with no second source and no character in common. Reverting
  it made the stated reason literally true and left the refusal standing. **Read
  a refusal's reason as an assertion about the page and re-measure it**, rather
  than treating the whole sentence as settled — the verdict can be right while
  the fact it names has rotted.
- **…and a premise can be wrong from the START, with the verdict still sound**
  (batch 232). `dom214.py:97` refuses `gaqat → gakat` because "`gakat` 起身;站立
  shares the SHAPE only". It never did: his own GAKAT card is 蹲著——彎著——屈著
  and glosses the bicycle 腳踏車（人蹲坐其上的車）, so scored on MEANING the pair
  passes. What refuses it is the homograph two cards away — he cards GAQAT
  冰塊、冰柱 separately, the register's ice word is `huda` with a family of its
  own and nothing within one edit of `gaqat` carries 冰, and 2 of his 3 tokens
  are that ice sense, so a remap paints two correct renders wrong to fix one
  (batch 205). `CITE_SPELL` cannot rescue the good half either: both blocked
  sentences are running text. **Repair the premise in the new log and pin BOTH
  halves** — the map still refuses the remap, AND the old log still contains the
  sentence being repaired — or the repair is orphaned the moment the file moves.
- **When the record refuses a word, check what the refusal SEARCHED, not only
  what it concluded** (batch 230, the mirror of batch 221's "grep the record").
  Both of that batch's rulings needed a written refusal retired, and neither
  refusal was bad reasoning — each was sound over an incomplete search. Two
  shapes recur, and both are cheap to re-run:
  - **A zero from ONE gloss file is not a zero from the register.** Batch 201
    refused the SPUNG card because 試探 and 拯救 "return 0 register rows". 試探
    returns 0 in `attested_gloss.json` and **4** in `bible_gloss.json`, which
    existed at that very commit. Search both, always.
  - **Search his gloss CHARACTER BY CHARACTER, not as a string.** His 嫉妒 returns
    38 rows of which 34 are the unreachable `hkrig` family; the single character
    **妒** puts the listed `sneuhir` at 2 edits, top of the list. Gate on carrier
    rarity (妒 43, vs 子 887 and 為 1569) or the output is batch 221's noise.
- **A refusal that names one blocker dies when that blocker is removed** (batch
  202). `naru` was refused three times for one reason — "a token-keyed map cannot
  split them" — and his `nalu` really is two words (好 in seven sentences, 代替 on
  his own headword). `CITE_SPELL` in `app.js` fires only where `noLink === true`,
  which is every render of a form as a NAME and no render of running text. A
  citation entry can only REFUSE the map's value, never assert a new one, so a
  wrong seam costs a pale headword and not a dark wrong word. That asymmetry is
  the licence; do not use the hook to assert.
- **The premise-failure class is EMPTY** (batch 231), and the sweep that proves
  it is kept in `logs/premise231.py`. Batch 230 repaired two false premises by
  hand, which reads like a seam; run mechanically over the whole record — 132
  anchored token-absence claims, 34 gloss-absence claims — every one of the 38
  candidates is the regex binding the PRESENT alternative rather than the absent
  word, because this project's refusals name both in one breath. Don't rebuild
  the sweep (closed-instruments table).

### Pricing a seam — rankings, and the classes that cannot be ruled

- **A lexeme modern Truku replaced is NOT a settled class** (batch 204). The four
  classes share one property: attestation is a test they cannot SIT. An obsolete
  verb can sit it and fails it. Naming a fifth class there is the bulk clearance
  already priced and rejected twice.
- **Bucket the pale before working it** (batch 198): root attested-and-glossed /
  root listed-unglossed / no analysis. That prices the seam. It does not rule
  anything — `HAND_RULED` will darken any value put in it, so the pricing has to
  come first or the metric decides the spelling.
- **Grep the ranking against the record before working it** (batch 221). The
  cheapest cut on any tail: for each blocker type, grep the batch log and every
  `dom2*.py`. Twelve of the sixteen largest already had prior mentions; the four
  with **none at all** were the whole batch. Costs one command.
- **A generated ranking's own "unreachable" class is a label, not an argument**
  (batch 228). `blockers.py` writes *"no analysis reaches a candidate root at
  all, so there is nothing to rule on"* over 65 types / 74 pairs, and that class
  had never been worked. But `roots()` has no reduplication rule, so every
  doubled onset lands there regardless of whether it has a root. Bucket by shape
  and strip the doubling by hand: `hhtran` reaches `htran` 阻擋 and his own
  French says *arrêter*. **Price the artefact before believing the label** — and
  price it from the DOM, which put the whole seam at 3 types and 1 pair, so the
  `roots()` widening it argues for is refused. That negative result IS the
  finding; don't re-open it.
- **The rare-character meaning sweep is closed** (batch 230). Over all 131 pale
  values joined to his Chinese, gated at ≤120 carriers and ≤2 edits with batch
  218's metalinguistic strip, it returns 48 rows; batch 221's record-grep leaves
  4 with no prior mention and **none is a ruling** — three score on a common
  character (品, 花, 為 at 1,569 carriers) and the fourth is XUBAO. Positive
  control: fed the pre-ruling state it finds `snuher → sneuhir`. A negative
  result, kept; don't rebuild it (closed-instruments table).
- **The ILRDF e-dictionary is closed AT THE PALE** (batch 234). Batch 182's
  "attests nothing new" was a statement about the lookups made; asked of the
  pale, where an attestation is the only thing that could buy a pair, it is
  sharper. Of the **146 pale map values, 131 have been asked and every one is a
  miss — 0 hits**, and the 15 never asked are 10 French plus 5 that each carry a
  written record. All five are DERIVED forms and the instrument indexes
  HEADWORDS (`tksaw`, `gmquwaq` return 無搜尋結果 beside roots listed in full),
  so it cannot reach them by construction. There was never a lookup to make.
  `dom234.py` keeps it live as `ASKED_HITS == 0` plus the containment that fires
  when a NEW pale value appears unasked; don't re-open batch 182 by hand.
- **Rarity does not rank the pale — it defines it** (batch 235). Batch 213's
  scan-first test is the cheapest question on any single row and paid four times
  in batch 229, so it reads like a ranking. It is not: **56 of the 67 sole
  blockers have his tokens totalling ≤2 occurrences**, holding 58 of the 79
  pairs. A pale blocker is typically a derived slot he wrote once, so sorting by
  rarity sorts nothing. What discriminates is the CROSSING batch 229 used — a
  rare token of his one edit, or one glyph, from a token he writes ≥10× — which
  returns 14 rows in 8 types, every one already refused in writing. (Two of the
  67 are reached by no map key at all, so a map-only join would have measured 65
  while reporting 67: count the unjoinable out loud, per batch 230.)
- **A settled class is a fourth kind of answer**, beside ruled, refused and
  pending (batch 203). Where a word is pale because the register has no reason to
  carry it — a wild species, a name, a loan, an onomatopoeion, a bare affix —
  the fix is to name the class, not to hunt harder. Ask which of the four it is
  BEFORE pricing a respelling: `klulu` was refused twice as a spelling and is
  correct as a class.
- **A word HE could not gloss is a limit on the instrument, not a fifth class**
  (batch 231). His SLOWEQ is tagged `(R. = ??)` with `fr = "??"` and
  `zh = "？？"`, and the gloss test — the only non-circular question to ask of an
  unattested word (batch 204) — needs a gloss on HIS side too. `sruwaq` 不滿 sits
  one edit away and there is nothing to test it against. He leaves **11**
  headwords unglossed and only three of them sole-block: SDANGAN 1, SLOWEQ 1,
  TBILAN 3, so the whole class costs **5 pairs**. Naming the limit is not a door
  to clear it, and `sruweq` is GREEN besides — no map entry fires, so the fix
  would itself be a new spelling claim.
- **Census per TOKEN, never per headword** (batch 203). A multi-word head like
  WA"LO 蜜蜂 has no single map key, so a headword-keyed census reported eight
  already-dark cards as green.
- **Measure a queue's COLOUR before working it for pairs** (batch 222). The
  `twice211.py` twice-carded queue sat open eleven batches as though it were a
  backlog of pairs. It holds none: **0 of its 51 values renders pale anywhere**,
  so every remap in it trades one dark value for another and moves the metric by
  zero. That is the standing homograph-freeze fact ("invisible to every colour
  metric, because the span is already dark") applied to a whole class at once.
  The queue is a CORRECTNESS seam — work it if wrongness turns up, never for
  pairs. Ask this of any list before pricing its items: one DOM pass, and it can
  close a queue that a per-item walk would have spent weeks on.
- **A name-only register gloss does not convict a dark value** (batch 225). Over
  all 1,967 entries, 41 dark map values are glossed ONLY as a name in
  `attested_gloss.json` while their card's Chinese shares no character with it —
  and they are overwhelmingly CORRECT: `harung` 松樹, `sudu` 雜草, `waray` 線,
  `pajiq` 蔬菜, `putuh` 截斷, `urung` 角. Truku personal names ARE ordinary words
  and the gloss file often carries only the name row; four of eight sampled have a
  second source supplying the everyday meaning. **A negative result — don't sweep
  it.** What convicted `kubuy` 狗名 on his KUBWI 遮蔽／悶死 was not the name gloss
  but that it had NO second source (bible 0, parquet 1, under the `>= 2` bar) while
  its own root was spelled seven other ways in the same book.
- **A pale-blocker ranking presents every row as a spelling question, and most
  of them are not** (batch 229). Of nine unworked types, FOUR were glyphs read
  wrong off the scan (`k'aon`, `mman`, `olo`, `rqeli`) and two more were his own
  typing the map had to absorb (`iniko` two words, `sml'lu` his parenthetical).
  One needed an orthographic argument. Batch 213's cheap test — a token
  appearing once in a book that repeats itself is a candidate for the scan —
  priced more of that seam than any reasoning about letters did, so **run it
  first on every row, before opening the register**. The tells that paid: a slip
  can land one letter from HIS OWN headword (`mman` beside his IMA oblique
  `Maan`, which he writes five other times), and a correction is checkable
  against his own frequency (`ole` 67× against `olo` never; `ini ko` spaced 122×
  against joined once).

### The map, the DOM, and the citation seam

- **A table-side darkness test misses everything the char rules spell** (batch
  218). `MM.get(k) in V` reads the map only, and `o` has no map entry —
  `charRules('o')` = `u` and the span renders DARK. That under-priced the
  `mqlaq` revert by one pair (predicted 2, cost 3). Price a revert from the DOM.
- **A tier-M identity pin is the one map entry that ages** (batch 216). It
  records a search that FAILED; every other tier records evidence found. When a
  card's other slots get ruled, its identity pins are the cheapest place to look
  for a pair — no new evidence needed, only the family that arrived since.
  `tnoxoi → tnoxoi` sat pale beside six ruled slots on his own TOXOI card.
- **The map is never evidence about colour; only the DOM is.** `WORD_OVERRIDES` is
  invisible to the generated map. Any tool asking "is this still green?" must
  consult the whole chain (`respellable()` reads three tables).
- **`CITE_SPELL` cannot split a homograph he carded TWICE** (batch 205). The
  `naru`/`nalu` fix worked on an asymmetry — one sense had a headword, the
  other only sentences. DIMA heads 竹子 AND 已經, QALO heads 梳子 AND 豬油, and in
  both his example sentences are the sense the map already renders. A remap
  would paint four correct sentences wrong to fix three heads. Leave them.
- **A probe must ask the map in the app's own alphabet** (batch 219). `wordKey()`
  folds ONLY `’ ʼ " ʔ → '` and `ł → l`. It does NOT fold ç→x and does NOT strip
  ü/ö, and seven map keys (`ilüs`, `iyüs`, `libiç`, `lübak`, `lübaq`, `opiç`,
  `xatsö`) are reachable in no other spelling. A scratch probe that normalised
  harder asked for `opix`, missed, fell to `charRules`, and reported PALE — while
  the live `opiç → upix` renders brown16 twice. **Absence in the wrong alphabet
  reads as pallor**; that artefact is what made the whole no-gloss bucket look
  like a seam. Copy `wordKey()` verbatim, and confirm from the DOM.
- **The DOM blocker ranking reports map VALUES, not his tokens** (batch 219). In
  modern mode a span's textContent is what the map emitted, so a blocker named
  `shkun` or `tgrgri` may be a string that appears nowhere in `entries.js`.
  Reverse it before searching his book: every map key sending to that value, plus
  every raw token whose `charRules()` output is it.
- **The refuse-only asymmetry is structural, not a convention** (batch 215).
  `build_verified.py` emits colours for MAP VALUES, and a `CITE_SPELL` value is
  not one — `naru`, `rijil` and now `ngari` are all ABSENT from `verified.js`, so
  `darkClass` pales them however well attested the word is. `ngari` 剩餘;結餘 has
  31 speakers and is still pale at the seam. Don't "fix" that; it is what makes a
  wrong seam cost a pale headword. And **check the seam at every render, not by
  sampling** — his `ngali` splits 5 running-text (拿取, correct) against 2
  citations (剩餘, frozen), seven of seven.
- **The citation seam does not reach a linkified crossref** (batch 215).
  `crossref-link` is set only where `noLink` is false, so a Truku name inside a
  gloss takes the running-text path and `citeSpell` never fires on it. Five
  gloss-internal `NGALI` references stay dark on the wrong sense, and widening
  the hook to reach them would reach the five correct sentences too. A recorded
  limit, not an oversight.

## Target

- **The metric is deliverable sentence pairs** — examples whose every Truku span
  is dark, over 5,429. **Currently 99.02%** (5,376). Not token share. A pair is
  what an MT session can consume; a token percentage is not. For scale, the same
  page is **99.71%** dark by SPAN inside `.truku` (36,207 of 36,311) and 99.44%
  book-wide. Those answer a different question; only the pair figure is the target.
- **Every figure in this file is a SNAPSHOT, not maintained state.** The metric
  above and the suite's green line are hand-edited at the end of a batch and are
  stale the moment the next ruling lands. They are re-measured by
  `python tools/orthography/logs/blockers.py` (the live blocked-pair shape) and
  `python tools/orthography/suite.py` (the live green line). **Where this file
  and those commands disagree, the commands are right** — and a batch that finds
  them disagreeing should fix the file rather than reason from the stale number.
  The same goes for the loss shape below and the pale-type counts.
- **Rank by SOLE blockers, not by occurrences** (batch 200). One pale word can
  hold a whole example hostage; 216 of the 227 blocked pairs were blocked by a
  single type. The occurrence ranking spends effort where the pairs are already
  lost. (Its trailing claim that the 2-or-more-pair tier was "exhausted" is
  **SUPERSEDED, batch 230** — see the multi-blocker rule below. The RANKING rule
  itself stands and is what this bullet is for.)
- **Every blocker tier is now closed** (batch 201) — **SUPERSEDED, batches 230
  and 241; every figure in this bullet is three generations stale.** The
  sole-blocker tier went to zero open, and the 2-blocker tier behind it — 10
  clusters, no recurring word pair — was ruled or refused item by item, leaving
  130 pairs blocked and all held by words with a written refusal. What the claim
  could not see is the very next rule: a pair blocked by TWO types of one root
  appears in no sole-blocker list at all. **The live figures are 53 pairs,
  52 + 1 + 0** (batch 242, below). What survives is the half that was never about
  the tiers — the next gain has to come from new evidence, not from re-ranking
  what is already priced.
- **The sole-blocker ranking hides pairs held by TWO types of the same root**
  (batch 230). A sentence blocked by `pdaqi` and `pstui` at once appears in no
  sole-blocker list, so the multi-blocker seam sat unworked for thirty batches
  while every tier above it was declared closed. It had six rows; two were
  rulings (+4 pairs) and the other four were confirmed refusals. When a ranking
  reports a tier exhausted, ask what shape of pair the ranking cannot see.
- **The loss now has a measured SHAPE: 79 + 4 + 0** (batch 235). Of the 83 pairs
  still blocked, 79 are held by a single pale type, **4 by exactly two — batch
  230's four confirmed refusals — and none by three or more**. That last figure
  is the answer to the rule above, pinned rather than assumed: there is no third
  tier hiding behind the two-type seam. It is a pin that can fail, since a ruling
  moves a two-type row into the sole list and a third pale type appearing would
  be the first row of that shape this project has had. **Now 78 + 3 + 0 over 81
  pairs** (batch 241) — and the row that moved did NOT move the way the pin
  predicted: clearing one blocker of a two-type row would have added a sole
  blocker, but both of that row's blockers fell at once, so the sole tier did
  not grow. **A two-type row can need two DIFFERENT KINDS of act**, and every
  instrument that reached this one asked one question of both words: `snuk` was
  a misread `smuk` (batch 213, a transcription) and `txey` was a spelling ruled
  `thiy` off his TOXOI card. Ask of each blocker separately whether it is even
  his string before pricing either as a respelling. **Now 52 + 1 + 0 over 53
  pairs** (batch 242), and this time the pin behaved: clearing `dmtbasyaq` moved
  its co-blocker `dmt'sapat` into the sole list, where it appears for the first
  time. Still no third tier.
- **A prior MENTION is not a written refusal** (batch 234) — batch 221's
  record-grep and batch 228's label rule, crossed. "0 of the 67 sole blockers
  have no prior mention" confirms the Target section and is a label; classify
  the mentions by whether any sits in refusal-shaped prose and **one** type comes
  back unworked. `kyuqan` was mentioned exactly once in the whole record, as a
  parenthesis inside a list of words a batch had NOT re-derived. The
  classification is left live in `dom234.py:unworked()` and returns 0 now: it
  fires when a blocker turns up with no refusal anywhere, or when an existing
  refusal is deleted. **Grep is how you find the record; only reading it is how
  you price the row.**
- **French in a Truku field is not a pair, and was inflating the metric.** Six
  example rows have a `t` identical to their `fr` — his AN (3) card demonstrates
  the circumfix that way (`Paro = Grand; Knplaan = Grandeur`). `metaLine()` in
  `app.js` renders those with no spans at all, which drops them from the
  denominator because the metric reads the DOM. **Five of the six had been
  counted DELIVERABLE**: French sentences scoring as Truku pairs. The test is
  `t == fr` modulo punctuation — it finds exactly six, no near misses, because no
  real sentence equals its own translation. Denominator 5,435 → **5,429**.
- **…and those rows left TEN French words in the map, all inert** (batch 234).
  `grand`, `grandeur`, `beau`, `savoir`, `vivant`, `volant` plus the char rules'
  own output on his French — `connaissance → cunnaissance`, `matin → macin`,
  `pour → puur`, `rougeur → ruugeur`. Six come from the `t == fr` rows and two
  from his parentheticals (`xandolu (=Volant)`, `Pqboan (= contraction pour:`),
  and **every one renders zero spans**, so there is nothing to clean. The
  consequence is a measurement one: a pale census taken from the MAP counts ten
  values the DOM does not have, so the pale-value seam is **136, not 146**.
  Batch 219's rule in the cheapest possible place.
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

## Audio

**The buttons are WITHDRAWN** (`AUDIO_WITHDRAWN` in `app.js`, one line). Every
clip in the bucket is a placeholder reading, and a 🔊 button asserts *this is how
the word sounds* — a stronger claim than any spelling on the page, and the one
claim a reader cannot check against the scan. The removal is display-only and
the smallest one available: **all 5,134 `a` fields stay in `entries.js` and every
object stays in R2**, because an id is a URL and stripping ids unhooks clips
already recorded and paid for (and fails dom219/220/221 on the spot). Restoring
the audio is deleting one `return ""`.

Clips are TTS (F5-TTS v5, White Dog / Huling Bhgay narrator) on Cloudflare R2 at
`R2_BASE + id + ".mp3"`, played only in modern spelling — his 1977 orthography
gets no button, because offering one would put a pronunciation in his mouth that
his page does not spell.

- **Do not synthesize anything until there is a voice.** The order is: the text
  to 100, THEN a voice, THEN redo the audio. The White Dog / Huling Bhgay v5
  narrator voiced the clips now in the bucket; it is not the voice the rebuild
  will use, so a run started before that is settled is 3,328 clips of the wrong
  reading. Measuring the staleness is free and worth doing; voicing it is not.
- **Build the item list from the DOM**: `python tools/build_tts_items.py`
  (`--write` to emit). The old `ilrdf/build_full_items.py` was a second
  implementation of `modernize()` and drifted several batches behind the app
  before dying on `modern_map.js`'s second object. Don't revive it.
- **His own spelling is the join key.** The page reorders sub-forms within a
  root, so position cannot pair the render against `entries.js`, and the nodes
  carry no id. Rendered with the toggle off and normalised to letters, every unit
  keys back 10,350 for 10,350.
- **An id is a URL.** A re-minted id silently unhooks a clip already recorded and
  paid for, so nothing is written unless all 5,134 already-attached ids mint back
  identically. Assert that before writing, never after.
- **`build_entries.py` no longer reproduces `site/entries.js`'s audio wiring**
  (batch 219). Both HEAD and the working copy carry exactly 5,134 attached ids;
  a plain rebuild emits **5,427** — 301 minted onto examples that had none, and 7
  dropped, six of them the `t == fr` French rows the metric already excludes. The
  entry/sub-form/example counts are identical (1,967 / 2,948 / 5,436), so nothing
  in the diff looks wrong. **Correcting a transcription slip therefore does NOT
  mean re-running the builder**: restore, patch the one string in `entries.js`
  directly, and assert `lost=[] new=[]` on the id set. Fixing the builder is its
  own job and belongs with the audio rebuild, not inside a spelling batch.
- **A reworded example keeps its old id on purpose.** `Dludan ni drbiyax` became
  `dmbiyax`; re-minting to `ex_dludan_ni_dmbiyax` would unhook the clip, so the
  id stays and the clip joins the known-stale set. Staleness is tracked and the
  rebuild is pending; an unhooked URL is not recoverable.
- **Compare words, not typography.** `items.json` predates `tidy()`; a raw-string
  diff calls 4,964 of 5,134 clips stale when the true figure is 3,061, because
  `da` vs `da.` scores 275 times on its own.
- **A resumable run cannot see a rewording** — the wav is on disk, it just says
  the wrong word. `full_sentences_synth.py` reads `tts_full/worklist.json`.
- **A wav on disk is not evidence that synthesis worked.** `verify_voice.py`
  re-voices sentences whose wording has NOT changed and compares duration and
  level against the take already in hand.
- **Smart App Control is enforced on this machine** and blocks numba's DLLs
  wherever they sit. It reaches the pipeline through one line —
  `librosa/filters.py` wants `jit` as a decorator, not as a compiler — so
  `ilrdf/numba_stub.py` stands in, guarded, and the real numba wins if it loads.
- **Bump `AUDIO_VER` in `app.js`** whenever clips change under existing keys;
  they are cached `immutable` for a year.

## Testing and measurement

- **Run the suite with `python tools/orthography/suite.py`** (site served at
  :8765, ~4 min). It runs every `logs/dom*.py` and `freeze2*.py` and adjudicates
  what they report against a ledger keyed on the exact failure line. Green reads
  `85 logs — 32 clean, 279 superseded, 0 REGRESSIONS, 0 crashed` (batch 244,
  parquets mounted). **The superseded count is environment-dependent by one**:
  with the parquets unmounted dom232's sentence sweep SKIPS, emits no failure
  line, and the green line reads 285. Mounted, the sweep runs and fails
  (8 proposals against a pin of 13) and is adjudicated by its ledger row.
  A one-off difference in that number is the drive, not the book.
- **A count assertion can heal without its subject moving** (batch 242). Five
  logs pin the map's raw KEY COUNT, and batch 241's transcription fix left them
  failing at 7370 against a pin of 7371. Batch 242 added exactly one unrelated
  key — `sloweq`, whose head had no map entry at all, which is why it rendered
  green — and all five stopped failing while `MAP.get("snuk")` is still None.
  Nothing they assert was undone: a raw count cannot tell *the lost key came
  back* from *a different key arrived*. Absorbed, never retired. **Read a
  healing as a claim about the instrument first** — of batch 242's nine, only
  one was even caused by this batch, and none was a pin retiring on evidence:
  one was a re-baselined HEAD read (dom58, batch 226's mechanism, healed by the
  commit and not by the batch), two were messages carrying a LIST that re-keyed
  when the list changed, and one was an assertion that did not RUN at all
  (dom232 prints `parquets not mounted — sweeps 1 and 2 SKIPPED`, and a sweep
  that does not run emits no failure line, which reads on screen exactly like a
  pin retiring).
- **A ledger row must declare its DIRECTION, not infer it from the wording**
  (batch 241). `shape` asserts a ceiling because a blocker count that falls is
  the project working — but `verified.js` keys and the pair count move the other
  way, and dom238/dom239 pin both by equality. A ceiling there would fail on the
  very next ruling and force every future batch to re-touch the row, which is
  the bookkeeping `shape` exists to avoid. `grew` is `shape` mirrored, a
  separate kind rather than a sign convention inside it, and it keeps the
  assertion that matters: **a verified key DISAPPEARING is the shape a ruling
  being silently lost would take.**
- **A supersession is credited to the act that caused it, which is not always a
  ruling** (batch 241). dom230's `snuk` row fails with "a refused word going
  dark is a ruling nobody wrote" — and no ruling was written; the word left the
  book through a transcription fix. So the row re-asserts the CORRECTED
  reading's darkness (`smuk`), because a pale `smuk` would mean the fix had
  reintroduced the same blocker under a new spelling. Control it with a PAIRED
  leg: that row must survive the batch's other ruling moving, and vice versa, or
  nothing is holding the two credits apart.
- **Take a ledger key from `sig()`, never from the log's format strings** (batch
  241). A hand-written key that matches nothing is INVISIBLE — the suite prints
  `no ledger row` and the failure stands, which reads on screen exactly like a
  row that was never needed. `.scratch/b241/keys.py` runs the log and prints the
  key the adjudicator will compute.
- **A CRASH can be the machine, and its five failures go missing with it** (batch
  228). Under two foreign jobs (`align.py`, a 16-thread `screen_solo.py` shard)
  `dom154.py` timed out navigating and the suite read `71 logs — 37 clean, 191
  superseded, 0 REGRESSIONS, 1 crashed`. Run alone it completed and emitted its
  five ledgered rows — **191 + 5 = 196**, which is the arithmetic that proves the
  crash swallowed a whole log's adjudication rather than the book having moved.
  The same run's serial re-check rescued five apparent healings. Check the
  superseded count adds up before believing a crash. It recurred in batch 230 —
  `align.py` at 21,708 CPU-seconds, `dom216.py` timing out, three rows missing,
  `194 + 3 + 4 = 201` — so treat it as the normal reading of a crash, not a
  one-off.
- **A batch that finishes an old supersession fails the log that recorded the
  unfinished half** (batch 223). Ruling `tqq'lang → tqqrang` made `dom57.py`
  report `BROWN tqq'lang tqqlang missing on [QQ'LANG]` — not a regression, the
  pin's own comment in `b57.py:116` says it was tracking a head batch 201 had
  already moved. Ledger kind `map` (precedent: `dom60.py`'s `tglgli` row); the
  darkness assertion belongs in the new batch's log, not in the ledger row.
- **A frozen measurement is not a test until something adjudicates its
  failures** (batch 209). The logs are records of what a batch measured; the
  project moves under them, so failures accumulate that are not regressions. 181
  of them had, and the sweep before had reported zero by reading a stale
  `verified.js`. **Never edit a log to make it pass** — that destroys the only
  evidence anything moved. The supersession goes in the ledger, naming the batch
  that overturned the pin.
- **Healing must be REPRODUCED before it is reported** (batch 217), and
  reproduced serially. A ledger row heals when its exact failure line stops
  appearing — but the line carries the measurement inside it, so a log that
  under-renders emits `got {}` where it emitted `got {'dark': 1}`, the key stops
  matching, and the screen says `retire them`. It happened to all five of
  `dom154.py`'s rows at once: four `wiring_score.py` shards from another project
  saturated the machine, the suite's own pool added four browsers, and dom154
  still waits 6s where the standard is now 22s. Run alone it reproduced every
  one. **Retiring a row destroys the only evidence anything moved, so the burden
  of proof belongs on the healing** — `suite.py` now re-runs any log with
  apparent healings, serially, and reports only what survives. Controlled both
  ways: five artefacts rescued, an injected unreachable row still reported.
  Not a dom154 quirk — **53 of the 61 logs wait under 15s** (19 at 2.5s, 34 at
  6s, one at 30s). They pass because the book renders fast on an idle machine.
  Fix the adjudicator, never the 53 waits.
- **A HOLD assertion is HEAD-relative, so COMMITTING re-baselines it** (batch
  226). Six logs (dom57/59/60/63/65/66) read their *before* map from
  `git show HEAD:site/modern_map.js` (`dom66.py:51`) and hold every neighbour at
  the value it had there. Committing batches 211–225 in one go made **eleven
  ledger rows stop failing at once** and re-keyed a twelfth — the batch-217
  fingerprint exactly, and the serial re-run reproduced all eleven as clean,
  because nothing about the book had moved. They are kept in `LEDGER` and
  subtracted in `ABSORBED`: deleting them destroys the record, and a failure that
  comes back still needs its explanation, but a HEALED report standing at 11
  forever masks the next real healing. **Suspect the git-relative logs first
  whenever healings arrive in a clump right after a commit.** And the class is
  not those six: **`dom58.py:53` reads HEAD the same way** (batch 230), so
  committing batch 229 healed its two SLAP rows over a book that had not moved.
  The rule is about the git-relative READ — `grep "git show" logs/*.py` — not
  about the logs batch 226 happened to catch.
- **An OV-pinned HOLD row never re-baselines, however the map moves** (batch
  231). A HOLD value comes from `val(t, OLD)`, and `val()` reads
  **`WORD_OVERRIDES` BEFORE the map** (`dom57.py:63`) — so a token pinned in
  `app.js` takes its value from a file that is not git-relative at all. That is
  why batch 230's four rows split three-and-one: `msnoxel` and `pstui` are
  map-only and healed the moment that batch entered HEAD; `snoxel` is in OV, so
  its row still fails and stays live. When healings arrive in a clump after a
  commit, **the ones that DON'T heal are the OV-pinned ones** — a fact about the
  read order, not about the word, and not evidence that anything is wrong.
- **…and ask whether the row is a TARGET or a HOLD before explaining a healing
  at all** (batch 232). Committing batch 231 healed the same `kasayang` failure
  line in dom63 and dom67 and left dom57's standing, and OV had nothing to do
  with it: a HOLD neighbour is `val(t, OLD)` off `git show HEAD:site/
  modern_map.js`, so HEAD moving re-baselines it, while a TARGET is read from
  the batch's own pin file — `b57.py:127` is where `kasayang → kasayang` was
  written — and can only heal if the map REVERTS. One is bookkeeping and the
  other would be news. Absorb the first kind, keep the second live, and assert
  the split by READING both the `b*.py` pin files and HEAD, rather than trusting
  the comment that explains it.
- **The citation seam can FAIL a darkness assertion, and that is by design**
  (batch 226). `CITE_SPELL` pales any form rendered as a NAME, so both his LIDIL
  heads paint `RIJIL` `w-unv` and the bend card — six affixed subs, no example —
  carries no bare running-text token at all. A HOLD row demanding the
  running-text `rijig` there is asking for the half of batch 201's split that was
  deliberately refused. Ledger kind **`cite`** re-asserts BOTH tables, because a
  re-merge can arrive from either side: drop the app.js key and every citation
  falls back to the map; move the map and the running text leaves the seam.
- **The DOM is the authority on COLOUR, not on his gloss** (batch 230). There is
  no `.gloss-zh` class — `app.js:1589` renders `<p class="gloss"><span
  class="lang-chip zh">中</span>…`, so a probe selecting `.gloss-zh, .zh` returns
  the string `中` once per card and nothing else. A sweep keyed on his Chinese
  must take the pale VALUES from the DOM and join the glosses **offline from
  `entries.js`**, running his tokens through the same three tables the app reads.
  Eleven of 142 pale values will not join that way — the `CITE_SPELL` seam and
  the `WORD_OVERRIDES` keys, which are invisible to a map-only lookup; report
  them rather than letting the join silently drop them.
- **Ask the DOM in the DOM's own CASE** (batch 226) — the display-side twin of
  batch 219's alphabet rule. `.hw` prints the modern headword UPPERCASE, so a
  probe filtering spans on lowercase `rijil` reported both LIDIL headwords as
  rendering nothing at all, which reads as the seam having stopped firing.
- **Check the machine before believing a suite result.** The wall-clock tell is
  a ~4 min suite taking ~17; `Get-CimInstance Win32_Process` names the culprit,
  and it may belong to another project entirely.
- **A supersession must re-assert the reason, not excuse the failure** (batch
  209). `dark` re-checks that the word is dark AND alone; `map` re-reads
  `modern_map.js` so a drift to a third spelling still fails; `meta` re-derives
  batch 207's metalinguistic test from `entries.js`. And **run the negative
  control** — 13 tampered lines fed to `adjudicate()` — because a ledger that
  cannot fail is a list of excuses.
- **A failure kind `failures()` cannot see is reported as a CRASH, not as a
  regression** (batch 219). `rc and not fs` sends the log straight to CRASHED, so
  an unrecognised failure line hides the failure completely. It has happened
  twice: the floor in batch 218, and the prose `FAIL <word> … It was refused
  because …` line dom214/216/217 write for their refusal pins — four real
  failures behind it, three of them overrides of those same logs' refusals.
  **Read a crashed log's own output before assuming the log is broken.** `sig()`
  now keys a prose FAIL on the sentence with its digits blanked, and kind
  `ruled` re-asserts both halves of an overturned refusal: the map still says
  what overturned it, AND the value is still in `verified.js` — a value that
  goes pale reinstates the refusal without anyone deciding to.
- **The metric floor is a ledger kind, and the first FALL was batch 218.** A
  floor failure used to CRASH the suite instead of reaching `adjudicate()` — the
  one failure kind batch 209 never wired up, because the metric had only ever
  risen. `sig()` now keys on the log's pin (`FLOOR 5329`) and carries the
  measurement beside it, and kind `floor` re-asserts two things: the metric has
  not fallen FURTHER than the overturning batch's own floor, and the ruling the
  pairs were spent on is still in the map. Negative control: 7 tampered cases,
  2 pass, 5 refused, plus the sig()-keys-on-the-pin check.
- **Removing a freeze can only ever LOOK like a regression.** A homograph freeze
  paints dark AND wrong, so the colour metric scores it as a win; reverting it
  costs pairs. Batch 218 paid 3 for `mqlaq`. Budget for that, don't flinch at it.
- **A pinned occurrence count is a snapshot of a growing book** (batch 209). All
  eight count drifts were increases, from later pages and from map arrivals.
  Assert a floor, never equality; a count that FALLS is the news.
- **Measure from the DOM, not from the map.** Assert against rendered cards.
- **A `.truku` prefix on a comma-separated selector scopes only the FIRST
  alternative** (batch 216). `'.truku ' + 'span.w-mod, span.w-unv, span.w-raw'`
  means `.truku span.w-mod` OR `span.w-unv` OR `span.w-raw` anywhere in the card,
  so dark is scoped and pale and green are not. It reported 17 green where there
  are 2 (`REMARQUE`, `PA`, `R` — a French gloss word and two tags) and 247 pale
  where there are 107. **The fingerprint: every spurious span is pale or green
  and none is dark.** Walk the `.truku` boxes and query inside them. (Those
  figures are batch 216's snapshot and the `REMARQUE` in them is gone — it was a
  note headword, unspanned since batch 244. Live: **13 green spans / 12 types**
  book-wide, **1** inside `.truku`.)
- **A pallor census is book-wide; only the PAIR metric is `.truku`-scoped**
  (batch 222). His headword, his sub-form names and his paradigm slots render in
  `.hw` / `.sub-form` / `.paradigm` — **not** inside any `.truku` box. Scoped,
  the book shows 87 pale span types; unscoped, **159**. Nearly half the pallor
  sits on his card furniture, invisible to a probe copied from a pair log. Batch
  208's scoping rule is right about the metric, where a pale name in a French
  gloss must not block a row whose Truku is dark, and wrong about a census. Ask
  each question in its own scope; `dom222.py` collects both dicts in one pass.
- **A negative control must inject a value that is in the tested state NOW**
  (batch 222). Controlling the zero-pale assertion meant injecting a known-pale
  word and requiring a FAIL. `treura` — named in this file as the biggest pale
  word on the page — passed, because it has since gone dark. A control keyed on
  the notes rather than on the current measurement proves nothing and reads as
  proof. Pick it from the run you just did (`rngut`, 9 pale spans, fails
  correctly).
- **A control leg that patches the wrong field passes for FREE** (batch 234) —
  the same fault one level up, and it reads as *explained* rather than as an
  error. Three legs did it at once: the hapax count reads his Truku `t` fields,
  so appending to `fr` moved nothing; his demonstration rows sit on the AN card
  as sub-form examples, not on `AN (3)`; and injecting a sole blocker that is
  already one (`mqlaq`) changes no count. **A control leg that does not refuse is
  a claim about the world and has to be read as one** — check the patch reached
  the field the assertion measures before believing the leg. The mechanical form
  (batch 235) is to make the patcher itself RAISE when it matched no card, and to
  PAIR every field-sensitive leg with the same string written to the wrong field,
  which must not refuse. Take an injected value from the measured data rather
  than inventing one — an injected join the register happens not to list passes
  for the same free reason.
- **A control that can CLEAR its own earlier failure proves nothing** (batch
  233). One leg wanted to check not just that an injection refuses but that it
  refuses with the right MESSAGE, and was written `bad = 0 if ok else 1` — which
  erased a real BAD from the leg above it and printed *all controls behaved* over
  a failure. Accumulate (`bad = bad or …`). Same shape as the ledger rule: never
  edit the thing that records that something moved. And **a gloss leg has to
  patch all THREE sources** — blanking `ptgeanak` in `attested_gloss.json` alone
  left `bible_gloss.json` carrying 隔開 and the leg passed for the wrong reason.
- **When two of your own instruments disagree, neither number is reportable**
  until the disagreement is explained (batch 216). Chasing a 15-span gap between
  the census and a new log found the bug in the log, not the census.
- **A furniture ruling buys 0 pairs BY CONSTRUCTION — assert it** (batch 223).
  His headwords, sub-form names and paradigm slots are in no `.truku` box, so a
  value ruled there cannot move the denominator. Assert `inTruku == 0` on every
  such value in the batch's log, or a later batch reads the flat metric as a
  failed seam and re-prices it. `logs/furniture.py` is the ranker; it is the only
  instrument in the project that is not `.truku`-scoped.
- **A ruling on a tag VARIANT removes a span; it never darkens one** (batch 233).
  `tagHtml()` (`app.js:1332`) modernises every variant in a tag and, when they
  all agree with the modernised headword, returns the root mark ALONE. So ruling
  `psaanaq → pseanak` did not paint his `(PSAANAQ ?)` brown — it stopped being
  printed, and the card now reads `√ (= PSANIQ?)`. As colour it is the same win,
  one pale span off the book, but a log asserting "the value renders dark" FAILS,
  and a control has to put the span back BOTH pale and dark, because a probe
  waiting for `w-mod` would pass the dark injection.
- **A tag with no root mark makes no spelling claim at all** (batch 233).
  `tagHtml()` line 1324 escapes any tag that does not carry his standalone
  `R`/`R.` and prints it RAW — no spans, no modernisation. That is 558 of his
  1,850 tags, and it is why batch 225's five "GREEN-side" compound-tag rows
  needed no argument: they were never spans. Asking the MAP what those tokens
  modernise to invents a seam; the DOM says zero. Of the 341 tag spans that DO
  render, 321 are dark and every non-dark one is a settled class (15 are batch
  223's posited roots) or a written refusal — the class is closed.
- **A card whose HEADWORD is not a Truku word must print raw too** (batch 244),
  and removing it from the census is a CORRECTION, not a win. His two `note`
  cards are prose, not lexemes: REMARQUE is his paragraph on Taroko naming
  customs and COLOPHON is the printer's imprint at the end of the book. Both
  headwords went through `modernize()`, so `charRules()` fired on French —
  `colophon` → **`curuphun`** by `o→u` and `l→r`, the "Palissade → Parissade"
  fault promoted from a gloss to a HEADWORD, and it stood long enough that
  `edictionary_trv.json` carries a lookup for `curuphun` returning null: the
  project once went and asked a dictionary about a word it had invented.
  `entryHtml()` now prints a `tag == "note"` headword with `esc()`, exactly as
  `tagHtml()` prints a tag with no root mark. Display-only — `entries.js` keeps
  both cards, per the standing rule that his page is the record.
  **The accounting is the point**: green falls 15 → 13 spans and 14 → 12 types
  and NOTHING else moves — dark 44,726, pale 165, cards 1,967, and every
  `.truku` figure identical, so the pair metric is untouched by construction
  (batch 223's furniture rule). A green span that was never his word was
  inflating the pallor, not measuring it; assert the unchanged figures beside
  the changed one or the next batch reads the drop as a ruling.
- **Rank the pale by occurrence, not only by pair.** `blockers.py` ranks by
  sentence pairs, so a word spent on headwords and crossrefs never reaches it —
  the biggest pale word on the page (`treura`, 13 — dark since, batch 222) was
  invisible to it.
- **A green span is not a pale one.** Green means no map entry fired; the fix is
  a map entry, which is itself a spelling claim, not a warrant in `verified.js`.
- **A test that cannot see a colour reports it as an absence** — check the harness
  before believing a null result.
- **Assert the replacement COUNT** on any sweep, or you will unhook the audio.
- **Read a bad row as a diagnosis**, and don't diagnose a missing file from a
  truncated `ls`.
- **An empty candidate list is not a refusal.** Batch 217 is the sharpest case:
  `roots()` restores the swallowed vowel for `un`/`an` and their long forms and
  for nothing else, so `spngan` and `spngun` reach the listed `spngi` while
  `spngaw` — the same paradigm, one suffix over — strips to `spng`, matches
  nothing, and is invisible to all fifteen rungs at once. **Probe the sisters
  before believing a level 0**: two words of one paradigm getting opposite
  verdicts locates the gap in the inventory, not in the word.
- **A greedy algorithm over an unordered input is a sample, not a rule.**
- **An empty sweep and a broken sweep have the same output — control it from the
  DATA side** (batch 232). Pinning `found == 0` is refuted by moving the pin,
  which proves nothing about the instrument. The join sweep's readable leg is
  the positive one: back batch 231's two rulings out of the map and it recovers
  `kasayang` and `isoka` unaided. Feed it an empty corpus and it can no longer
  recover them, which is what separates *found nothing* from *cannot see*. And
  **an absent source must SKIP, not score zero** — parquets unmounted prints
  that sweeps did not run rather than banking their emptiness.
- **`seen` is EVERY span, not the dark ones** (batch 232). Dark is what is left
  when both pale classes come out: `DARK = seen − unv − raw`. A probe that reads
  `seen` as dark makes a pale word its own supporting evidence, and the tell is
  a scratch probe disagreeing with the log by a few rows — 14 proposals against
  13, 34 shapes against 40. Explain the disagreement before reporting either
  number (batch 216); the strict count was a subset of the loose one both times.
- **A stoplist must be DERIVED, and its depth set by the record** (batch 232).
  Batch 218 and batch 221 both say a shared Han character is evidence only if it
  carries meaning, so any gloss test needs one — but hand-picking it fits it to
  the batch it was written for. Take the commonest characters across the
  register's own glosses, and set the cut where the derivation reproduces every
  character the project has already NAMED as noise (著 sits at rank 26, so the
  cut is 30, not 25). Assert that reproduction as the control. It is
  load-bearing and the amount is measurable: withdrawn entirely, batch 232's
  spellcheck sweep has 3 survivors, all scoring on 的/不/是/人 inside his
  sentence gloss; at the pinned depth, none.
- **Sentence-against-sentence over the parallel corpus is closed at zero**
  (batch 232). Batch 183 refused the corpus's phrase rows for building a
  word→gloss file, and rightly; a question that never attributes a gloss to a
  word escapes that objection — take HIS example and ITS Chinese, find corpus
  rows whose Chinese overlaps, ask which Truku word there is close in shape. Use
  CONTAINMENT, not Jaccard, or a single-word corpus row scores a perfect sense
  match at 0.1. It yields 13 proposals over 50,848 rows: eleven are batch 221's
  noise mode (有, 我的, 你們的, 正在, 孩子們), the twelfth is `yianu → yamu` —
  batch 231's written refusal, which is the cheapest confirmation the instrument
  is aimed right and the seam is empty — and the thirteenth is `gaqat`. Keep the
  negative result; don't rebuild it (closed-instruments table).
- **Ask `entries.js` for his TEXT, never for the raw file** (batch 229) — the
  display-side twin of batch 219's alphabet rule and batch 226's case rule. Two
  faults, both in one log: `Sm"lu` is JSON-escaped on disk, so a sentence
  assertion searching the raw string silently never matches; and the raw file
  carries every corrected-away reading inside the **audio ids** (`ex_ini_ko_bi_
  stama_ana_mman_ka_yako`), so a "this misreading is gone" check fires on an id
  that is supposed to keep it. Parse, walk his fields, join. That id fault is
  itself an assertion worth having — an id is a URL, so pin the stale ones BY
  NAME, and control the pin with a SWAP rather than a drop, because re-minting
  holds the count and the count assertion cannot see it.
- **A different-root refusal written with `startswith` convicts its own
  morphology** (batch 229). `w.startswith("bkuy")` over the 39 register forms
  glossed 捆綁 flagged `gmnbkuy`, `mkmbkuy`, `mhhaut` as rival roots — his
  family's own prefixes. Widening to a substring then showed the claim "all 39
  are off bkuy/haut" was never true (`pskrut`, `smbbsqur` are other roots), and
  the refusal never rested on it. **State the negative half as "no carrier
  spells HIS stem"** — that is what makes it a test rather than a list, and it
  can honestly fail when evidence arrives.
- **Word-boundary BOTH sides, or the Truku check fires on his French** (batch
  229): `\bmman` matched `commandements`.
- Verifying crossref behaviour needs two taps: first shows the gloss preview,
  second opens the entry (`app.js:1272–1276`). A single `.click()` moves nothing.

### Closed instruments — read this table BEFORE building a sweep

Ten sweeps have been run to a negative result and kept. Each is argued in full at
the rule that names it; this table exists so "has this already been asked?" costs
a glance instead of a grep. **A negative result is evidence and rebuilding one
spends a batch to re-derive nothing** — but note what each actually asked, because
a genuinely different question escapes the closure (batch 234 re-opened batch
182's ILRDF result that way, by asking it AT THE PALE).

| instrument | the question it asked | result |
|---|---|---|
| `logs/freezesweep.py` (206) | gloss test over the whole book, no pairing file — which dark headwords are freezes? | 827 of 2,420 flagged, all synonym noise (`tama` 父親 vs 上帝); a shape-search second leg leaves 156 and is the same test twice |
| sister sweep (217) | a pale word whose slot-family sisters are verified while it scores level 0 — an analyser gap? | 5 of 174 pale values; 4 already refused in writing, the 5th (`sapi`) a refusal too |
| `logs/tail221.py` (221) | batch 204's different-root test over the tail | 14 rows, 12 noise on one common character; the one real-looking row scored off an EXAMPLE gloss |
| unreachable class (228) | `blockers.py`'s own "no analysis reaches a candidate root" class — 65 types | a `roots()` artefact: reduplication has no rule. Priced from the DOM at 3 types / 1 pair, so the widening it argues for is refused |
| rare-character meaning sweep (230) | all 131 pale values against his Chinese, ≤120 carriers, ≤2 edits | 48 rows; 4 with no prior mention and none a ruling. Positive control recovers `snuher → sneuhir` |
| `logs/premise231.py` (231) | 132 token-absence + 34 gloss-absence claims — which refusals rest on a premise gone false? | the class is EMPTY; all 38 candidates are the regex binding the PRESENT alternative |
| sentence-against-sentence (232) | his example + its Chinese against 50,848 corpus rows, by containment | 13 proposals: 11 noise, 1 a written refusal (`yianu`), 1 `gaqat` |
| ILRDF at the pale (234) | does the e-dictionary attest any PALE value? | 131 of 146 asked, **0 hits**; the 15 unasked are 10 French plus 5 derived forms a headword index cannot reach |
| name-only gloss (225) | 41 dark values glossed ONLY as a name, sharing no character with his card | overwhelmingly CORRECT (`harung` 松樹, `sudu` 雜草, `waray` 線) — don't sweep it |
| `twice211.py` queue (222) | the twice-carded queue — is it a backlog of pairs? | 0 of its 51 values renders pale anywhere. A CORRECTNESS seam, never a pair seam |

Two more closures are not sweeps and live at their own rules: batch 231's
unglossed-headword class (11 heads, 5 pairs, and his `(R. = ??)` leaves the gloss
test nothing to score) and batch 233's tag spans (341 render, 321 dark, every
non-dark one a settled class or a written refusal).

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

**Deploying means Cloudflare. It does not mean Netlify.**

```powershell
npx wrangler deploy   # pecoraro-taroko.shidailun.com (Cloudflare, wrangler.jsonc)
```

**Do not run the Netlify command** unless the user names Netlify in that same
message. It is metered — the user pays per deploy — and a "deploy!" answering an
offer that listed both commands is a yes to the Cloudflare one only. This
section used to read *"two hosts are live and they must not drift — same
`site/`, deploy both"*, and that sentence is what shipped an unwanted deploy on
2026-08-15. **Drift is the intended end state**: the netlify.app address is
frozen behind a "we moved" banner, so its copy of `site/` falling behind is the
legacy site behaving as designed, not a fault to correct. The command, for the
day it is asked for by name:

```powershell
netlify deploy --prod --dir site --no-build --site d6e80a1c-405b-4bf9-8977-3630174261c6
```

Cloudflare is the main app; the netlify.app site is the legacy address and
carries `site/legacy-banner.js`, which prints a "we moved" notice on any host
that is not `pecoraro-taroko.shidailun.com`. The banner is served from the same
`site/` dir, so it ships to both and stays silent on the new host by design.

**The two hosts carry the same NAME on purpose** — `pecoraro-taroko` in both
places, matching the netlify.app address the project has answered to since the
start. The Cloudflare worker was briefly `taroko-pecoraro`; renaming it in
`wrangler.jsonc` does not rename the deployed worker, it **creates a second
one**, so the old worker and the old hostname stay live until they are deleted
by hand. Deploy the new name BEFORE shipping the banner change, or
`legacy-banner.js` points the legacy site at a host that does not resolve yet.
`taroko-pecoraro` was deleted 2026-08-12 (`wrangler delete taroko-pecoraro`),
and deleting the worker took its custom domain's **DNS record with it** — the
authoritative answer for the old hostname is NXDOMAIN, so there is nothing left
to clean up in the dashboard. The tell that it worked is on the resolver, not
the wire: for the first minutes the old name still answered **530**, which reads
like an orphaned record but is the local cache serving the A record it already
had, to an edge with no worker bound. **Ask 1.1.1.1 before believing a 530**,
and flush the cache before believing a 200 — the same lag ran the other way
when the NEW name 404'd locally while resolving fine at authority.
