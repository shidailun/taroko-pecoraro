# Batch log (batch 136 onward)

<!-- Moved out of CLAUDE.md 2026-08-03 to keep the always-loaded file small. Content is verbatim; nothing was deleted. -->

Newest work is at the top of each dated heading group, as in the original.

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

## A test that cannot see a colour reports it as an absence (cleanup, 2026-08-03)

The regression suite was carrying 289 failures across 23 logs and every one was
a defect in the TEST, not in the dictionary. Three causes, in descending size.

**No log numbered below 74 knows the pale class, and that was ~270 of the 289.**
They scrape `.w-mod, .w-raw` — the only two colours that existed when they were
written — so a word de-verified at any point in the last 110 batches disappears
from their census entirely and is reported `BROWN … missing`, the same string a
genuinely wrong respelling produces. dom63 went 79 failures to 0, dom58 43 to 0,
dom66 32 to 0, on one selector. **A three-valued world read by a two-valued
test does not report "unknown", it reports the value it can't see as absent.**
The GREEN check is unaffected — only `.w-raw` gets the `~` prefix — so adding
`.w-unv` is monotone: it can only turn failures into passes, never the reverse.

**dom57–dom73 could not run at all**, and the cause was one line: they read
their own batch file as `io.open("bNN.py")`, relative to the CWD, so they only
worked from `tools/orthography/logs/`. Resolved against `__file__` now. I
reported to the user that the `bNN.py` files "were never committed" — they are
all tracked in HEAD, and the claim came from a `head -3` truncating my own
listing. **Do not diagnose a missing file from a truncated `ls`.**

**The remaining 20 were real supersessions, and they get a table, not a delete.**
dom138 already had the convention and its wording is the rule: "the assertion is
kept and inverted rather than deleted, so a revert shows up here." So `PIN`/
`KEEP`/`STOPPED` entries that a later batch legitimately overturned move to a
`SUPERSEDED_NNN` dict asserting the NEW colour, named for the batch that did it
— 105 `l'pun`→`rpun`, 117, 120, 121, 132, 148 `mkpakaw`, 149 `mtama`, 151-152
`mttama`/`tmtama`, 155 `psqpah*`, 164 `taya`, 166 `s'lu`→`salu`. In the map-layer
logs the table is keyed on **(token, old spelling)**, so a key that drifts to
some THIRD spelling nobody argued for still fails. Deleting the assertion loses
the claim; asserting only the new value loses the history.

Two shapes worth naming. Batch 155 respelt `psqpah*` out of existence, so the
supersession is an ABSENCE assertion, not a colour — the transcription layer is
the one kind of overturning a colour test cannot express. And dom65's `ti` was
never a supersession at all: the only `Ti` on T'LO is inside the sub form
`Tit'lo (Ti t'lo ?)`, his own parenthetical doubt about his own segmentation,
which the renderer gives no word span. **A generated HOLD set will sweep up
strings the page never paints**; exclude them by name so the exclusion is
findable if the renderer ever changes.

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


## Batch 172 — the loan gate that was built but never wired

**`DUP` is `eduk`, and his own card wrote the rule.** His DUK card states the
alternation outright — "mutation fréquente des consonnes finales: P et K …
派生詞保留P，而詞基往往作K" — and the modern wordlist obeys it: derived `dpi`
關門 (pq=20), `dpan`, `dpay`, `dpun` against base `mduk` 關(門、窗) (pq=6),
`dmeeduk`/`dmpteeduk` 關門者. His DUP card names the answer itself ("Vr. NDUK.
et: DUK"), and `duk` was ALREADY mapped to `eduk` at `manual_map.json:164`
while `dup` sat on an identity claim one line below. A family that agrees
convicts a head keeping its own letters. `eduk` is attested, verified 1,
glossed 門扇. The hunt homograph does not interfere: `dupan`/`dupun` 獵場/要追獵
live under ADUK and did not move — decided slot by slot, confirmed by a
per-token diff showing only `dup`, `ndup`, `eduk`, `neduk` changing at all.

`dup` 7 pale → 0, `ndup` 1 → 0, `eduk` 7 → 10 dark, `neduk` 0 → 1 dark.
Eight pale out, four dark in: **the missing four are self-referential crossrefs
the app collapses** once DUP renders as its own crossref target. Card counts
held at 1,967 / 2,948 / 5,437, so nothing was lost — measured from the DOM, not
the map. 97.4472% → **97.4650%**.

**The loan population was exported by batch 171 and never consumed.** `git log
-S loan_population` returns exactly one commit (`cbb4eec`, batch 171) and it
touches only `build_modern_map.py`. The producer shipped; the consumer was
never written. That is why a previous session could quote ~97.7% and "under
1000" and the tree could still measure 97.4472% — the figure was a correct
prediction of a gate that was never wired, not a regression.

The argument for wiring it is already written in `build_verified.py`'s own name
block, which cites `denki` 電気, `banasi` 話, `stbaku` 煙草 as names no register
of Truku given names can ever hold, and answers that their modern spelling comes
from the same o>u, l>r, x>h rules that spell every other word on the page. A
Japanese or Chinese loan is in that identical position: no Truku wordlist will
list `abura` 油 or `budosyu` 葡萄酒, so attestation is not a test tier J can
fail — it is a test tier J cannot sit. Pale there reported the absence of a
source that was never going to exist. Gated to the 141-token population for the
same reason names are, widening `seen` and never `lex`.

+124 occurrences, 122 of them tier J. 97.4650% → **97.7439%**, pale 1,095 → 971.

**`NALU` was a false dark, and only the gloss could catch it.** `manual_map.json`
sent his NALU 代替、頂替 to `malu` — attested, verified 1, pq=718, and glossed
好、良善、美. An attested value can still be a wrong value. The modern word
carrying 代替 is `nirih` (pq=55), nothing like either; and his own family points
the other way, `nluan` → `nruan`, attested and glossed **代替者**, the gloss
agreeing with his headword exactly. Not an OCR slip either, which was the first
suspicion: the entry carries a full gloss, two sub-forms and four example
sentences ("Mnalu ko laqe so dmayao" 我代替你的兒子來工作), and modern Truku
independently keeps an n-initial word for his meaning. Set to `naru`, which
`nruan` evidences by syncope. Costs 8 spans of wrong dark for 8 of right pale —
**97.7439% → 97.7259%** — and is worth it, because those 8 were queued to be
recorded as the word for "good". `mnalu` stays identity: it is a genuine
homograph across his MALU 和睦相處 and his NALU 頂替, and the map is keyed by
token, so the slot-by-slot call cannot be made there.

**An elision mark expanded where the corpus writes nothing.** `mpskagul` carried
`w_was: mpskeagul` into the W tier and came out `empskeagul`; the corpus attests
`empskagul` (pq=2), and the root `skagul` is id-tier attested. Same for
`mpgaluk` → `empgealuk` against attested `empgaluk`. Both pinned in tier M.
Only 2 types / 5 occurrences of the 44 W-tier pale occurrences have an attested
e-deleted twin, so this is a pin and not a sweep. +4 dark; the fifth span is one
more collapsed self-crossref, MPGALUK and MPGALUP now displaying alike.

**Batch total: 97.4472% → 97.7371%, pale 1,103 → 974 occurrences / 645 types.**

Tier J has left the pale census entirely. What remains is M 431, P 192, R 133
occurrences, and the tail is flatter than ever — top item 8, then a run of 4s
and 3s. **98% needs +122 occurrences, which is roughly 45 separate
adjudications.** There is no lever left of that size; the loan gate was the last
one. Two standing categories can never clear by evidence and should not be
counted against the target: grammatical-morpheme cards like MPA 前綴, which are
prefixes and not words, and the refusals already pinned (`rih`, `klulu`,
`msnoxel`). 100% dark is not a reachable gate.

## Batch 173 — the refusal was wrong on two counts

Batch 173 measured the 462 sole-blocked pairs, classified 235 types / 257 pairs
as "never a headword (example text only)", called them unadjudicable, and made
no changes. Both halves of that reasoning are wrong.

**1. "Never a headword" does not mean glossless.** Every form on the page
reaches an entry — through `FORMS`, through `lookupWord()`, or through a
generated SLOT card. A word that appears only inside an example sentence still
resolves to a root, and **that root has a gloss**. The adjudication should
resolve each blocker to its root and use the ROOT's Chinese, which is exactly
the unit `build_worksheets.py` already says the work is keyed on. The batch-173
classifier asked only whether the token itself was printed as a headword or
sub-form, which is a question about the index, not about the evidence.

This is **not** the sentence-gloss rule batch 146 refused. That rule proposed
letting a translated sentence vouch for a respelling — a sentence in the 1977
book attests HIS spelling and cannot confirm ours, and `sktama` stands as its
counter-example. Resolving a form to its root and reading the root's word-level
Chinese is the ordinary method, the one every previous batch used. Batch 173
conflated the two and refused 257 pairs on the strength of the wrong rule.

**2. Affixed loans miss the tier-J gate.** The loan gate wired in batch 172 keys
on the bare tokens listed in `loan_population.json`, so a loan carrying a
documented prefix never matches. `ddcristu` is `dd-` (human plural) + `cristu` —
a tier-J loan the gate cannot see, pale for a reason that has nothing to do with
the respelling. The same argument that put bare loans dark covers the affixed
ones: no Truku wordlist will list them either.

**Standing next action:** measure how many pale occurrences decompose as a
documented prefix plus a tier-J loan, then extend the gate to cover them.

No adjudications were made in batch 173. Pair total unchanged at 4,950 / 5,435.


## Darryl's queue, 2026-08-03

Queued, not acted on. Recorded verbatim from Darryl.

**GENERAL PRINCIPLE, applies to everything below:** always propose the "it's
his" reading before the "it's ours" reading. Several suspected transcription
errors today have plausible readings as real features of his text. Entries were
read off page images, so any real error is a misreading, not the PDF's OCR
layer.

### SYSTEMATIC — measure these, don't hand-fix

**A. Affixed loans miss the tier-J gate.** It keys on bare tokens in
`loan_population.json`. `ddcristu` = `dd-` (human plural) + `cristu`. Count pale
occurrences that are a documented prefix + a tier-J loan.

**B. Stem alternation may be breaking the regular-inflection gate.** BUWAY
paradigm (`Muway`, `buway`, `biqi`, `biqan`, `biqun`) should all be dark as
regular inflections of a dark root. If they are pale, the gate is not firing —
likely because the root wears two stems (`buway`/`biq`) and the analyser can't
follow the alternation. Count pale forms that are regular inflections of a dark
root whose stem alternates. Could be larger than A.

**C. Dark words with no reachable page.** `khibung` renders dark in
§ *Mhibung ka ribul su; ini hari khibung ka naku* but has no entry. SLOTS only
generates cards for forms he listed on ° lines. Count dark example-sentence
tokens with no reachable page. If large, widening SLOTS to attested example
tokens would fix the navigation gap AND give the batch-173 blockers a root gloss
to be adjudicated against.

**D. Which documented rules were never swept as a class?** The loan gate, the
batch-32 word-initial-`ii` rule, and the prefix chains all look like rules
derived once and applied to the case at hand. List them.

### CORRECTIONS TO BATCH 173

**E. "Never a headword" was mis-diagnosed.** Every form ultimately reaches an
entry — `FORMS`, `lookupWord()`, or a generated SLOT card whose root is glossed.
Re-derive the 235-type / 257-pair class by resolving each blocker to its ROOT and
using the root's gloss. This is not the batch-146 sentence-gloss rule.

**F. `sblangan` 矛 → try `sbrangan`, NOT `smbrangan`.** The refusal was against
`smbrangan`, which needs an inserted `m` no char rule licenses. `sbrangan` is
plain `l→r`. Check its gloss; `smbrangan` is attested pq=13 but unglossed, and if
both are one root with and without the `-m-` infix that settles the gloss for
both. Example sentence (刀、弓和矛) corroborates. Likely a template — other
batch-173 refusals may have had the right candidate one letter from the one
tested.

### ADJUDICATION RULE

**G. Regular beats bracketed-irregular.** A bracketed alternative is often his
own guess from five decades ago. Where the unbracketed form is regular against
the headword, the bracket does not compete: QUDAK / `Qdakan` (`Kdapan`?) —
`Qdakan` is regular, `Kdapan` is not (`k-` for `q-`, `p` for `k`), so `Kdapan` is
irrelevant. Two constraints: (i) this applies to ADJUDICATION only, never to
parsing or display — `collapsed()`, `collapseTagBrackets()` and the `cells()`
cell-count invariant all depend on brackets being read as spellings; (ii) it
cannot become "ignore brackets," because SPU (`SPU"` - `SPUG`) is the
counter-case where his bracketed form was the fuller and correct one. Then
measure: how many pale forms have a bracketed alternative irregular against the
headword while the unbracketed form is regular? Decide as a class.

### INDIVIDUAL WORDS

**H. KMRNU √ / Restaurer / 修復** — suspected misreading; no vowel between M and
R. Check: (1) does the entry carry sub-forms or examples? A misread headword
usually stands alone. (2) Omnibus search for 修復 and the `km-r` skeleton — a
modern word with his gloss and a vowel where he has none locates the error.
(3) Alphabetical neighbours — does KMRNU sit where it should? If a misreading,
the fix is `data/batch_*.json` plus rebuild, not a map entry.

**I. ANAY 姊妹的丈夫／妻子的兄弟, § *Mha su inu, nay?*** — `nay` is probably a
clipped vocative of ANAY, not an error. His own note says the term is very
frequent and expresses friendship, and the sentence is direct address. Check:
(1) omnibus for `anay` and `nay` separately, with glosses; (2) other clipped
kinship/address terms elsewhere in the book; (3) only if both empty, check the
page image for a dropped initial A. If it is a real clipped vocative, do NOT
respell it to `anay` — that would erase a real form.

**J. `iiyah` "will come"** — batch 32 already established word-initial `ii` is not
written in modern Truku. Check: is `iiyah` pale, and at what tier and value? Root
is `iyah`/`uyah` 來 — confirm which. If `ii-` is his future marker rather than a
spelling variant, the fix is not a respelling. See D.

**K. `mnkyayung`, § *Mnkyayung ku kdjiyax tmabuy* / 我一路沿著溪流下來** —
`yayung` 河流 is solid. First determine WHICH token in the line is actually pale:
`mnkyayung`, `kdjiyax`, or `tmabuy`. If `mnkyayung`, confirm `yayung` is dark and
check whether `mn-` + `k-` is a documented prefix chain; if so this is verified
level 2, not a new mapping. If `tmabuy`, see L.

**L. TABWI ° line:** `° Tmabuy, tabuy, tbgi (?) Tbuyi (?), tbuyan, (tbuyan?),
Tbuyun.` (1) Count the cells — the positional slot labels need five. This reads
as seven tokens; if `cells()` does not return five, SLOT_SUF is the fallback and
the positional read is forfeited for this line. (2) `tbuyan` appears twice, once
bracketed — his hedge or a transcription error? Check the page image.
(3) Capitalization is inconsistent across cells; determine whether that is his.

**M. Capitalization may be positionally meaningful.** `biqun` renders lower case,
`Muway` capitalized; the TABWI line does the same (`Tmabuy`, `tabuy`, `tbgi`,
`Tbuyi`). Check whether `Muway`'s capital comes from the page or from
`matchCase()`. Then test across the 380+ five-cell ° lines whether capitals
cluster by slot position. If they do, that is a second independent witness to the
positional read `parslot4.py` measured — his own annotation, not our inference.

### FEATURE REQUEST

**N. No "go back" navigation.** A slot link or crossref opens a card with no way
to return. Needs to work for crossref (two-tap), slot link (one tap), and A–Z
listing → card. Consider `history.pushState` so the phone back button works — the
app already has `?q=` deep links.


## Batch 174 — B measured and closed; the paradigm split is the wordlist's shape

**B is closed.** The premise case is already correct: BOAI's line renders
`muway, buway, biqi, biqan, biqun` all five DARK, so the analyser does follow
the boai/byeq -> buway/biq alternation. 404 paradigm lines rendered against 404
`paradigm` fields in `entries.js`, so the harness saw all of them.

53 lines have a dark anchor and at least one pale cell. 112 pale types sit under
a dark anchor: 44 where the stem alternates (65 pale occ, 11 sole-blocked pairs)
and 68 where it agrees (96 pale occ, 16 pairs). Clearing every one of the 112
moves the pair total 4,950 -> 4,977. B is not a big lever.

**The third group is not a gate bug.** 73 pale cells have a dark sibling on the
same stem. The hypothesis was an incomplete suffix set — `-an` recognised in some
frame where `-i` and `-un` are not. It is false. `BASE_SUF` holds
`'' un an i ay aw ani anay aan aneyi`, and the data shows all three slots
analysing together wherever the stem is analysable at all: `psbrnuxi`,
`psbrnuxan`, `psbrnuxun` all cut to `brnux`+`ps`+suffix; `dkari`, `dkaran`,
`dkarun` all cut. There is no frame where the suffixes are treated unequally.

**What splits them is the shape of the wordlist.** 57 of the 73 dark siblings are
level 1 — a modern source lists that exact word, so they never went through the
analyser at all. `kayagan` is dark because it is listed, not because the gate
accepted it. And 60 of the 73 dark siblings are BARE, against pale cells that are
`-i` (24), `-un` (23), `-an` (13). Wordlists list citation forms. The split is
the corpus's, not the analyser's, and a pale sibling here is an absence rather
than a refusal.

The two failure modes are both doing their job. 41 cells cut cleanly and fail
because no gloss agrees — the same test that keeps `spsangay` off `sang`. 33
cells return nothing from `roots()` because no candidate root is in `lex`.

Inside that 33 there is one narrow gap: **13 have exactly one listed sibling on
the same stem and none have two or more.** `sistered()` (level 8, "a slot the
wordlist writes with two other suffixes") needs two, and all 13 miss by one.
Dropping the threshold to one is a one-line change and was REFUSED: it weakens
the standing two-supporters rule for at most 13 types, and unanimity over one
item is not unanimity. The remaining 19 have no listed sibling at all; nothing
reaches them.

**Ceilings.** All 73 cells clearing = 4,950 -> 4,966 pairs, 16 pairs. The 13-type
threshold change buys less than that. Neither is worth the price. No changes
made; pair total unchanged at 4,950 / 5,435.


## Batch 175 — the monospace grid, and the class it opens

Technique written up separately in `.claude/notes/grid-method.md`. The finding
that produced it: LIWANG's example on p.164 reads `mnalox`, not `rinalox`. The
word measures 99px against a ~16px cell — six cells, the same as `liwang` (101)
— and `rinalox` is seven characters. `mnalox` ×52 in the merged text (×152 in
the raw batch files, counting sub-form and ° occurrences), `rinalox` ×1.

**The candidate class, measured two ways.**

Hapax types with an edit-distance-1 neighbour occurring ≥10 times: **592** of
7,216 Truku types. Tightening the neighbour threshold gives 307 at ≥25, 190 at
≥50, 112 at ≥100. This list is NOISY and is not a fix list — its top entries are
`nai`/`ini`, `kala`/`kana`, `aga`/`ana`, which are real distinct words that
happen to sit one letter apart. Short types dominate it for the obvious reason.

**The sweep cannot see its own motivating case.** `rinalox` → `mnalox` is edit
distance TWO (`ri` → `m`), so a d=1 sweep misses it entirely. The confusion this
typeface makes is one glyph read as two, which is why. Measuring that class
directly — hapax explained by a one-glyph-as-two substitution with a neighbour
≥10 — returns **4**: `rinalox`→`mnalox` ×52, `hma`→`lima` ×20, `ban`→`loan` ×15,
`snn`→`snii` ×11. Small, checkable one page at a time, and it is where the grid
earns its keep.

`manalox` (×1) is edit distance 1 from `mnalox` and sits in the 592. Neither it
nor `rinalox` has been corrected — both want a page check first, and the grid is
a per-word tool because the m/n confusion runs both directions on the same line.


## Batch 176 — word pages for groups 1 and 3; group 2 refused

C found 1,835 dark example-sentence occurrences over 1,002 types with no page to
open. 988 of those types were never a headword, a sub-form or a ° cell — words he
used and never defined. They render dark, respelled, and lead nowhere.

**What was built.** `tools/orthography/build_wordpages.py` → `site/wordpages.js`,
a TABLE (`window.WORD_PAGES`), consumed by app.js. Group 1 (value = the root)
names the one candidate root `Inflection.roots()` reaches when that root is
already dark; group 3 (value = `""`) carries only the concordance. **Group 2 is
omitted from the file entirely**, so silence in the table is a refusal in the
app — a token whose root would have to be CHOSEN (`spsapox` between `psapuh` and
`sapuh`) gets no page, because choosing is an adjudication and a generator does
not adjudicate.

**Neither card asserts anything new.** Group 1's root has its own page and its
own gloss; the analysis that reaches it is the same analysis `regular()` already
runs. Group 3 says only "this word occurs in these sentences", and a concordance
is his text, not a claim about morphology. Both are marked the way the ° slot
cards are — italic headword, dashed tag (`in his examples / 例句詞形`), italic
generated gloss, `morph-note` saying he gave the form no entry. **A page we built
must never read like a page he wrote.**

**The population is wider than the measurement.** The DOM census measured the
unreachable DARK example-only types (988 → 315/536/137). The generator runs the
same two tests over ALL 1,594 example-only types, pale and green included, so it
emits **876 keys — 446 group 1, 430 group 3 — not 452**. The tests are identical;
only the population differs. Over-generating here is safe and under-generating is
not, because app.js re-tests reachability at runtime against `lookupWord()` and
`slotByKey()`, which know about bracketed aliases and variants the generator does
not, and drops any key with no `CONC_IDX` row. Of the 876, 632 types actually
render a link.

**10 of the 446 roots are dark with nothing to open** — `truku`, `drudan`,
`dmblaiq` … Dark means a modern source vouches for the SPELLING, not that he gave
the word an entry. Those roots are still named in the gloss (the analysis is the
same) but the → pointer is not clickable. Ranking throughout is
`lookupWord` > `slotByKey` > word page: a real entry always outranks a card we
generated, and a slot he printed outranks one we inferred.

**Measured from the DOM.** Unreachable dark example tokens **1,835 occ / 1,002
types → 958 / 557**; 890 dark spans over 445 types now carry `word-link`. Card
counts hold: 1,967 entries, 5,437 examples, 0 word cards in the whole-dictionary
view (`?q=%CC%81` norms to "" and `wordMatches("")` returns []). One tap opens a
word page, like a slot and unlike a crossref — there is no gloss for a preview to
show. **Pair total unchanged at 4,950 / 5,435 (91.08%)**: navigation is not
orthography, and nothing here changed a spelling.

Group 2 (536 types / 914 occ) left entirely, as instructed. 536 decisions is not
a batch, and half of them will be answered better once groups 1 and 3 are
navigable.

**Post-build audit, before deploy.** Three defects, all found by rendering every
card and reading the DOM (`scratchpad/wpcolour.py`), none visible from the table.

*The population really is wider, and it is pale.* 876 keys emitted, **612 render**
— the runtime re-test against `lookupWord()` / `slotByKey()` / `CONC_IDX` drops
264. Of the 612, **183 have a pale headword** (40 group 1, 143 group 3) and 2 are
green. The headword does carry `w-unv`, so the colour is honest, but a colour is
a legend away and the heading is the one thing on a generated card a reader takes
as given. It is not given, and for a group-1 card the affix analysis was run ON
that proposal. A clause now says so, appended to either note whenever
`spellClass(key) !== "w-mod"`.

*The named root rendered GREEN — 254 of 347.* `spellClass()` keys on HIS token;
the root is a modern string no table holds, so it fell through to `w-raw`, which
the ⓘ legend defines as "nothing vouched for it, the blind char rules ran". The
exact opposite of true for a root the generator picked BECAUSE it is in
MODERN_VERIFIED. Fixed by asking `attested()` directly about the root instead of
routing it through `linkifyTruku`. All 320 surviving roots now render dark.
**A colour that is merely uninformative is survivable; one that reads as its own
opposite is not.**

*27 roots, not 10, had no page to open.* My pre-build estimate approximated
`lookupWord()` and undercounted by 17 — the DOM is the only witness for this,
which is the standing rule and it held again. Those cards are now group 3
outright: a root nothing can open is not a pointer, and naming one while offering
nothing to check it against asserts MORE than a concordance-only card does, not
less. Effective split is now **group 1 = 320, group 3 = 292**.

Pair total unchanged at 4,950 / 5,435; reachability unchanged (958 occ / 557
types still unreachable); 1,967 entries and 5,437 examples still render.

## Batch 177 — the clitic joins were never in the verified table

**`table(app, "CLITIC_FORMS")` read 34,309 characters of the wrong file.**
`var CLITIC_FORMS = {};` is filled at RUNTIME from `CLITIC_JOIN`, so the parse
ran past the empty literal to the next `\n  };` — 675 lines down — and returned
8 junk keys: UI strings, punctuation, and `"tap"`, which was being emitted into
`MODERN_VERIFIED` as a verified Truku spelling. Not one joined form was in
`vals`. Seven of the eleven were dark anyway because the map reaches them by
another key; the four that no single token also maps to — `tgbasi`, `tgbhgay`,
`tgbilaq`, `tgima` — have rendered PALE since the table was written, each one
checked against `spoken_truku.json` by hand at the time and each one listed.
Fixed by reading `CLITIC_JOIN` and taking its values. **+4 pairs, 4,951 → 4,955
(91.17%).** Distinct values 6,539 → 6,526; `"tap"` gone.

**A derived table cannot be scraped from source.** `table()` finds a name and a
`{`, and an empty literal gives it no reason to stop. WORD_OVERRIDES and
CLITIC_JOIN were re-checked and both bound correctly (48 keys / 63 lines, 11
keys / 11 lines).

**Attestation is exhausted on the blockers.** Of the 384 types that are the sole
blocker of an otherwise-clean pair, exactly one — `rih`, already pinned in batch
146 — has any corpus witness at all (parquet freq 1). No hapax argument, no
sister argument and no name-registry argument can reach the rest. Split by what
the inflection gate finds: 202 types / 238 pairs reach no candidate root, 55 /
60 reach a listed root carrying no gloss, 127 / 163 reach a listed root whose
gloss disagrees. The path to 5,000 is per-word adjudication of the last two.

**The p-/m- sister class is 5 types / 6 pairs.** Measured after the user's
`psbiyuq` case, over every blocking type: `pngraq`, `prudaw`, `psqgu`, `ptaril`,
`pneydang`. `psbiyuq` itself frees NOTHING — his `Psbiyoq` occurs three times in
`entries.js` and never inside an example sentence, so it blocks no pair. The
reading is right (`msbiyuq` 流汁 is listed against his `BIYOQ` 汁液, and the gate
refused only because stripping `ps-` lands on `biyuq` 人名（男;女）) and it is
worth nothing against the metric. **A sound argument is not automatically a
lever.**

**REFUSED — `tksaw`** (4 pairs, the largest single adjudicable blocker). His
`Tksao` <SAO 像－以……的方式> is glossed 模仿－假裝－裝作. Modern has two stems:
bare `ksaw` (listed 2×, unglossed; `mksaw` 希望和…一樣, `pksaw`, `empksaw`) and
`hksaw` 假冒;假裝 (`thksaw` 假冒 9×, `tghksaw` 裝著的, `gmnhksaw` 假裝). The 假/裝
of his gloss sits only in the h-family — but **his own orthography writes modern
h as x**, and he wrote `tksao` with no x, so the h-family cannot spell his word.
That leaves the bare stem, whose single glossed supporter `mksaw` 希望和…一樣
shares no character with 模仿－假裝－裝作. One supporter is not two. Stays pale.

**REFUSED — `gmquwaq`** (3 pairs). He files it under `GQOAQ` 搖頭 as its verbal
form, and separately under `QOAQ` 嘴巴 as `Gmqoaq (=R. QOAQ ?)` — his own
question mark. The only attested neighbour is `quwaq` 洞口, i.e. the reading HE
marked as uncertain. `gquwaq` is in no modern list. The pointer inside a question
is not a citation.

**Already pinned, not re-derived:** `naru`/`mnalu` (batch 114 and 161 — `nalu` is
a phantom root, `nmalu` and `snalu` stripping to the same four letters),
`tnaga` (164), `rih` (146), `ksudan` and `empsbiyuq` (NAMEGL, deliberate).

## Batch 178 — a capital inside the word is his, and it names a person

`§ Mksipao ka dTome` (`data/batch_270_273.json:744`, fr "Tomé et les siens
habitent en face") rendered as **`dtumi`**. The person was gone: `dtumi` reads as
a common noun.

`matchCase(sample, target)` read the case off `cased[0]` only, so every capital
after the first was flattened. That is a third case class and it is doing work —
he bonds an affix straight onto a proper name and capitalises the NAME rather
than the word: `dTome`, `dTroko`, `dDiyan`, `mkMorisaka`, `skBoxil`, `ddCristo`.
Census of `entries.js`: **32 types / 41 occurrences.**

The mark is now carried by POSITION over the cased characters (his diacritic
vowels `äëïöü` and the elision marks `'’ʼ"ʔ` carry no case and are skipped on
both sides), guarded by `target.replace(CASELESS,"").length >= cased.length`.

**Only a shortening can slide a later letter left past the mark.** `PPPaon` →
`ppaun` is six cased letters to five, so a mark at index 2 would land on the
`a` and print `ppAun`. The guard sends that one back to the old initial-capital
reading, which is what it already had — no regression.

DOM-verified: `dTumi`, `dTruku`, `dSbnawan`, `mkMurisaka`, `mkEfunang`,
`ddCristu`, `MkMurisaka`, `skBowxil` now print the internal capital; `Ppaun`
falls back.

**Trailing `=` re-checked across every field** — hw, fr, en, zh, paradigm,
crossRef, and every example and sub-form field: **0**, not just in example `t`.

## Batch 178b — queue item N: a way back

A slot link, a crossref or an A–Z row opened a card and stranded the reader.
Every screen is now one of six view descriptors — home, letter, entry, slot,
word, search — recorded on the browser's own stack.

**Recording lives inside the show functions, not at the click sites.** A card is
reachable from more than one branch of the `results` handler — a slot from its
link, from its A–Z row, from a search — and one of those paths would have been
missed.

**A redraw is not a navigation.** `rerender()` (spelling radio, language
checkboxes) and `popstate` raise `navLock`, which replaces the current entry
instead of pushing one. Without it, toggling the spelling four times cost four
taps of Back to leave a single card.

**The rule "a search replaces a search" was too broad — that was the one real
bug.** Typing must not push per keystroke, but a crossref runs through
`openEntry()`, which sets the box and searches, so a tapped link produced a
SEARCH view and got swallowed by the same rule; Back skipped the card you came
from. `forcePush` says a link is a navigation whatever kind of view it lands on.

**`rerender()` now re-shows a named card instead of searching for it.** It had to:
`render()` would turn an entry card back into a search for its own headword, and
with history that redraw silently overwrote the card's state with a search's.
His single-letter headwords S, M and A make that the same trap `showEntry()` was
written to avoid.

**A letter listing gets `?l=`, not `?q=`** — `?q=S` reloads as a search for every
card containing an s.

Entry / slot / word states carry INDEX AND KEY: the index is what the rendered
HTML already uses, the key is what survives a deploy, since Back can land on
state written by an older `entries.js` in which that index means another word.

The ← button (`#btn-back`) shows only where `history.state.n > 0` — depth counted
forward from this tab's first paint, not `history.length`, which counts whatever
the reader did before arriving. **A control that does nothing is worse than no
control.**

DOM-measured (`scratchpad/nav178.py`): **28 pass, 0 fail** — deep link, one-tap
slot, one-tap word page, two-tap crossref, forward, three searches = one entry,
button appears and hides. Cards still 1,967; deliverable pairs still 4,955
(91.17%).

## Batch 179 — the group-2 refusal was withholding the page, not just the root

`qmpahan` (his `kmpaxan`) occurs in **58** of his example sentences and is a
headword nowhere. Searching it delivered 47 entry cards — the whole of BUYU,
five sub-forms and every example among them — because a root that merely
*contains* the word answers for it. `pngalun` the same, at one occurrence.

Both were **group 2** in `build_wordpages.py`: `roots()` finds two or more
candidates, choosing is an adjudication, and the generator refuses to adjudicate.
That refusal was right about the root and wrong about the page. **A concordance
asserts nothing about morphology**, so nothing an unresolved analysis leaves open
makes a list of his own sentences unsafe to print.

Group 2 now emits `"?"` — page, no root named. It is kept distinct from group 3's
`""` because their cards must not say the same thing: group 3's says *no analysis
reaches a root*, which for these is false. `WORD_NOTE_2` and a third `wordSense()`
branch say instead that more than one root would explain it and the page does not
choose.

**718 types gained a page; 1,593 of 1,593 example-only types now have one, up
from 876.** Cards still 1,967; nav suite 28/28.

Two findings recorded while adjudicating the words the user raised:

- **`kmux` is a homophone, and the p- argument runs backwards there.** His
  `K'MUX` (R) is 稗草 tares; modern lists `kmux` 握拳, `skmux` 因…握拳, `pkmux`
  在握拳 — a complete three-member family, all of it about a fist. The only
  modern word carrying 稗 is `pypayi` 一些壞掉的稗草, built off `payay` "rice",
  which is the very word in his own example. Admitting `pskmux` on the strength
  of `skmux` would be inheriting from a fist. Cost of demoting the two: **0
  deliverable pairs** — neither occurs in a sentence row.
- **`bbuyu` 打獵 is not a clash but a confirmation.** His gloss is "maquis -
  savanne - forêt vierge", and his own example glosses `wada bbuyo` as "est parti
  à la chasse". Dark stands.
- **The BUYU sub-order is his**, verified against `scans/full/page_057.png`:
  BBuyo, Pkbuyo, Tnbuyan, Kmubui (kmbui ?), Bbuyo — the same word at both ends,
  "maquis" first and "obscurité (sans doute par assimilation)" last. There is
  nothing to un-scramble; there is an order to impose. One thing there IS ours:
  he prints the `°Pkbuyo, .?., pkbuyan, pkbuyun` line after that sub-form's
  example, and the app hoists it above the gloss.

## Batch 179b — two principles: one order inside a root, and a sentence is not a root

He stated both as law: "1. there should be a consistent order within every root.
2. for extra sentences — just cause a root happens to contain a word somewhere
does not mean that EVERYTHING in the root has to come along!"

**Principle 1 — `subOrder()` (app.js, before `entryHtml`).** Sub-forms were
printed in file order, which is his page order, and his page order is not one
order: BUYO ran BBuyo, Pkbuyo, Tnbuyan, Kmubui, Bbuyo — the base form both first
and last (`scans/full/page_057.png`, read and confirmed verbatim). Alphabetical
will not do either: under K'MUX it puts the causative Pskmux before the base
Skmux, since P < S. So the sort is DERIVATIONAL, keyed on the head: longest
common substring with the headword gives (a) where in the sub-form the shared run
starts — prefixless forms first — and (b) how many characters the sub-form adds
on top of it. Ties fall back to the key, then to file order, so it is total and
stable. Measured: 24.8% of multi-sub entries change order. Verified in the DOM
that `K'MUX → [Skmux, Pskmux]` and `BUYO → [BBuyu, Bbuyu, Pkbuyu, Tnbuyan,
Kmubui (kmbui?)]`, and that the order is IDENTICAL in Pecoraro mode — the
spelling toggle must not rearrange his page.

**Principle 2 — `looseHtml()`.** `filter()`'s fifth tier is `contains`: the query
is in no headword, no sub-form, no ° line, only somewhere in the body. Those
entries were rendering as FULL CARDS. `qmpahan` — a word he never gave an entry —
answered with 47 whole roots, BUYO arriving with five sub-forms, every example
and its concordance, because one buried sentence says qmpahan. A root that
happens to contain a word somewhere is not thereby an answer about that word.
Now a contains-hit prints only the sentences that contain it, each naming the
entry it came from (`concRowHtml`'s shape; the pointer opens that entry on one
tap), under one `Elsewhere in his sentences` heading. **`qmpahan`: was 47 root
cards, now 1 word page + 46 sentence cards carrying 59 sentences.**

The fallback is not a corner case. The same tier catches a hit inside a FRENCH
gloss — `palissade` reaches two entries with no matching sentence at all — and
there the full card is the honest answer and is kept whole. Never run a gloss
through `modernize()` to find one: it turns "Palissade" into "Parissade".

`exGlossHtml()` factored out of `examplesHtml`/`concRowHtml`/`looseHtml`: the same
three gloss lines are printed in three places and had begun to drift.

Measured: 16/16 on `loose179.py`, 28/28 on `nav178.py`, whole-dictionary census
still 1,967 cards with zero sentence cards in it, deliverable pairs unmoved at
4,955 (91.17%).

## Batch 179c — a pointer that names a spelling nothing on screen shows

Two of his own devices had fallen out of step with modern mode.

**The inline see-also.** PSANIQ's French says "VR. SANYAQ.", and our English and
Chinese carry it over as "See SANYAQ" / "參見 SANYAQ". 373 gloss fields hold one;
138 distinct forms are named. In modern mode SANYAQ is SANIQ on its own card, in
the A–Z listing and in every sentence — so the pointer was the last place on the
page still printing a spelling nothing else shows, and being plain text it
pointed without linking. `citeTargets()` now finds them and `glossCites()` renders
each as the same `.crossref-link` his `crossRef` field uses: modern spelling,
`spellClass` colour, two taps to open. **1,165 links over the whole dictionary,
770 of them respelled.**

Two guards make this safe against the never-modernize-a-gloss rule. Only a token
`lookupWord()` resolves to a real entry is touched — a French word resolves to
nothing, so the char-rule fallback can never reach it — and a match is all or
nothing, because "QDALAN, QDALUN" is one pointer written twice and half of it
respelled would read as two words. The scan must run on the WHOLE gloss before
`glossCites()` splits it: the split puts every word in its own part, and the
marker would no longer be beside the word it points at. That was the first
attempt, and it linked nothing.

**The variant note that named itself.** `Lqlaqe (vl. llaqe)` rendered as
`Lqlaqi (vl. lqlaqi)` — a bracket distinguishing a word from itself. `collapsed()`
was already built to catch exactly this and could not, because `variants()`
returns the pieces AS WRITTEN and the apparatus label rides along: it was
comparing "vl. lqlaqi" against "lqlaqi". `variants()` now strips `AL_LEAD`, the
same closed list of apparatus words the A–Z index already strips for the same
reason. Self-referring brackets in modern mode: **4 → 0**, five brackets closed,
spans 44,957 → 44,947.

In HIS spelling four brackets still read as self-referring — `Snkaxa (Snkaxa?)`,
`M'wa'la (M'wa"la)` and two more of that pair. They stay. The first is his own
hesitation and the others are the two elision marks, which are both real; his
spelling is the record.

Unmoved: 1,967 cards, deliverable pairs 4,955 (91.17%), 480 blocked. Dark
43,925 / 97.73%, pale 988, green 34. 9/9 `cite179.py`, 16/16 `loose179.py`,
28/28 `nav178.py`.

## Batch 180 — the gate agreed about the morphology and refused on a synonym

`ppdsun` — his `ppd'sun`, in § *Ongat ko bi ana manu ppd'sun mo tmaan diyan*
under ADAS / **Pp'adas 用來寄送之物**. Darryl: "ppdsun is fut pf. what's the
problem?"

**Nothing was wrong with the analysis.** `roots()` finds THREE, and every root of
all three is already dark: `p-` + `pdsun`「…(人)將會帶去(未來式)」, `pp-` +
`dsun`「要帶」, `p-` + `pdsi`「帶去」+ `-un`. The modern wordlist calls `pdsun`
the future itself, and `pp-` is a live modern prefix (batch 20, with mm-, tt-,
ss-). The ruling names the slot the wordlist already names.

**It failed one test, gloss agreement, and failed it on synonymy.** He never
glossed the word AS a word, so the only Chinese `regular()` holds is the sentence
translation 我實在沒有任何東西可以捎給(送給)Djian 的父親 — and 捎/送 share no
character with 帶 or 拿走. The instrument is a shared Han character; two synonyms
are invisible to it. *A refusal on character overlap is not a refusal on
meaning.*

**The word-level gloss was one line up and the code drops it.** `_his_glosses()`
feeds an example's tokens `x.zh or szh` — an OR — so a sentence carrying its own
translation shadows the gloss of the sub-form it sits under. Fixing that in
general was measured before proposing it: over all 549 blocked sentences,
restricted to tokens sharing a 3-character run with the parent form (without that
restriction every function word in the sentence inherits the parent's gloss), it
frees **3 types and 3 pairs** — `empabgu`, `pnsdahung`, `empnhmadan` — and does
not reach this word anyway, since 用來寄送之物 shares no character with 帶
either. Priced and not taken.

**The family acquits, and the sweep found nothing else.** Of the 59 distinct
tokens in the ADAS entry — headword, nine sub-forms, both ° lines, every example
— **58 were already dark**. This was the last pale word in a family that agrees
with itself throughout.

Entered as `HAND_RULED` in `inflection.py`, consumed in `build_verified.py` and
printed on its own line. Kept SEPARATE from `HAND_SPOKEN`, which answers a
different question: there the corpus is silent about whether a word is Truku at
all (`nta`, batch 159); here the corpus has already said yes to every part of the
word and only the gloss test refused. Both widen `seen`, never `lex`.

**Deliverable pairs 4,955 → 4,956 (91.17% → 91.19%), blocked 480 → 479, pale
988 → 987, dark types 5,873 → 5,874.** Cards 1,967.

## Batch 182 — a source that attests nothing and settles thirty pairs

`tksaw` first, ruled in by the informant on the shape batch 180 named: two
analyses, `tk-`+`saw` 像；如此；那樣 and `t-`+`ksaw` 像這樣, both roots listed
and glossed, and the refusal was gloss agreement alone against his 模仿－假裝－
裝作. "Make like" and "imitate" are one word and a shared-character test cannot
see it. THE FAMILY ACQUITTED TWICE: `tksao` was the only pale token in SAO
(45/46 dark) and the only one in KPOXEL (25/26). 4 pairs.

Then the wide net, and its result is the interesting part.

**Everything local was already mined for attestation.** All eight ILRDF
datasets feed parquet_truku_freq.json, `ithuan_formosan_text` included with the
right column (`formosan`, not `transcript`). What is NOT mined is their Mandarin
side — `translation` at 90–100% across every set, 6,940 Truku sentence pairs in
the text set alone, and `fb_ilrdf_dict_asr/tts` which are dictionary recordings
at 96–100%. We take the tokens and throw the Chinese away. Still unread.

**The ILRDF online dictionary is reachable.** web.klokah.tw/multiSearch calls
`POST e-dictionary.ilrdf.org.tw/wsReDictionary.htm` with FMT/account/TribesCode/
qw; TribesCode 33 is 太魯閣語. fetch_edictionary.py wraps it: cached including
misses, sequential, 0.7s apart, a miss never retried. 611 words asked — every
blocked type and every candidate root.

**It attests nothing.** 165 hits, and not one is a word attested_modern.json
does not already hold. Zero of the 378 blocked types are in it: `tksaw` and
`gmquwaq` return 無搜尋結果 while their roots are there in full, because it
indexes headwords. The derived forms are in the printed Patas pusu kari Truku
(1,267 roots, 29,788 derived, three volumes) and that is not online. klokah's
own teaching corpus returns 0 for `tksaw` across all fourteen material types,
which is consistent — it is where our parquets came from.

**It glosses.** 17 of the 85 glossless roots under the blocked pairs: `bsrat`
吝嗇, `siisan` 縫補, `qqrinut` 貧窮, `tbrnahi` 忘恩, `brnux` 平地. Wired into
`_gloss()` on the Bible glossary's exact terms — additive, and deliberately NOT
into `voices` or `seen`, because there is nothing here to widen them with.

Priced at 8 types / 8 pairs before the build; delivered **37 types and 30
pairs**, because a root's gloss feeds every rung and not just unglossed_root().
**0 words lost their verification** — the "adding evidence must never subtract a
claim" check, run as a set difference over MODERN_VERIFIED.

**It confirmed batch 152 from outside.** The dictionary glosses `paux` as
翻過來／犁田／腳向上 — both senses, printed side by side. Batch 152 reached
翻轉 by reading the root's own paradigm (`mknpaux` 反過來, `mspaux` 會翻) after
four batches of refusing 犁田, and wrote that a citation gloss is one editor's
choice of sense. Here is a second editor choosing differently. `kpaux`, which
that batch left pale for carrying one supporter, is now dark. **The SISUN trap
stays shut**: `sisi` is not in the cache and `sisun`/`sisan`/`ssisun` are all
still pale.

DOM after: dark 43,993 (97.8775%), pale 920, green 34, total 44,947; types dark
5,912 / pale 601 / green 25. Blocked pairs 479 → 445, deliverable **4,990 =
91.81%**. Regressions 16/16, 9/9, 28/28.

## Batch 183 — the corpus's other column, and where it runs out

Darryl: "well if we have these unused sentences work them!!!! what are you
waiting for? quwaq is mouth so gm- seems reasonable as a double prefix."

**`gmquwaq` ruled.** His `gm'kuwaq`. `quwaq` is 嘴/嘴巴 in the e-dictionary at
freq 125 and 洞口 in the omnibus — both senses printed, and `gm-` over a body
part is the ordinary actor form. Entered in `HAND_RULED`.

**`build_parquet_gloss.py` — the Mandarin side of the eight Truku datasets.**
`build_parquet_attested.py` had been reading those files for years and throwing
the translation column away. It answers a different question: not *does this
string occur* but *what does it mean*. 54,457 rows, of which 8,875 have a
one-token Truku side; 1,420 words, 2,315 distinct glosses, 328 of them words the
omnibus does not gloss.

**Only the one-word rows are taken.** A two-word row is a phrase and splitting
its Chinese across both halves is the instrument that failed for ppdsun —
`baga bubu` 母親的雙手 would gloss `baga` as 母親 as readily as 雙手, and a gate
reading a shared Han character cannot tell which half it matched.

**The phrase rows were then priced properly, and refused on measurement.**
Co-occurrence — a bigram kept when it appears in ≥60% of a word's rows and in
≤5% of the corpus — recovers the known gloss for **56 of 58** words that already
have one (97%), so the method works. It proposes a gloss for **2 of 58**
still-glossless blocked roots (`pitay` 朋友, `rangah` 樹洞). The rare roots are
rare in the corpus too. *A method that is accurate where you can check it can
still be silent where you need it.* Not wired in.

Rebuild: **gained 9 types, lost 0** — `dsbnawan gmquwaq pkpruan pkpruun
pkungatan pnqihi pnqihun pnslhagan ppeapa`. Unverified 611 → 602 of 6,526.

Blocked pairs 445 → **438** (416 sole over 349 types, 22 multi). Deliverable
pairs **4,997 / 91.94%**, from 4,956 / 91.19% at the session's start. Dark
44,009 / 97.9131%, pale 904 (from 988), green 34. 16/16 `loose179.py`, 9/9
`cite179.py`, 28/28 `nav178.py`.

## Batch 184 — the word he marked with question marks

`snkrawah` — his `snklawax`/`snqlawax`, three sentences, and one of the three is
his own headword SNQLAWAX glossed 「？？－悲傷（？）－孤獨（？）－可憐（？）」.
He did not know what it meant. The ILRDF dictionary does.

**The root's second sense was missing from the wordlist.** `rawah` is 打開蓋子
in the omnibus and that is why the gate refused — 處於不利／被犧牲／可憐 shares
no character with it. The online entry prints its Truku definitions beside the
Chinese: `mangal gnumuk` 打開蓋子, `beytaq brhug` 鑰匙 — and `ini qbqan` 婉惜,
`malu kuxul` 情緒穩定. *An open lid and an open heart are the same word.*

**The k-forms carry the emotional sense and are attested with it.** `smkrawah`
可惜 (freq 5), `kmrawah` 捨不得（因需要不肯割愛）／愛惜 (freq 16), `mtrawah`
心情開朗. His form is the s<n> perfective of `smkrawah`, which is already in
`attested_modern.json`; 可惜 landing on a person is 可憐. Of the 16 `rawah`
members the wordlist holds, every k-form anyone has glossed is glossed with
regret.

This is the first ruling the e-dictionary settled on its own — batch 182 said
its value was glosses, not attestations, and here the value is a sense the
wordlist omitted rather than a word it lacked.

Gained 1, lost 0. Blocked pairs 438 → **435**; deliverable **5,000 / 91.99%**.

## Batch 185 — one ruling, two refusals, and the difference between them

**`mnalu` ruled.** MALU › Mnalu 和睦相處——彼此相愛; m<n>alu is the plain
perfective of `malu` 好, which the ILRDF dictionary gives at **frequency 661**.
The gate refused on synonymy for the third time in this run — 和睦 shares no
character with 好, and being good together is what 和睦 IS. His own note names
MKMALU as the frequent equivalent and `mkmalu` is listed. His second `Mnalu`
(NALU › Mnalu 頂替——以…之名) is a different word and the ruling says so in the
comment: modern 代替 is `nirih`, and neither `nalu` nor `naru` is listed. What
carries to that card is the orthography alone, which is his own letters
unchanged — the map already held the identity, since `l→r` would make *mnaru of
a word modern Truku writes with l.

**`tbiran` refused.** His `tbilan`, only ever in the phrase *lukus tbilan*
節慶盛裝, and he glossed his own TBILAN entry 「？？」. Neither `tbilan` nor
`tbiran` is in the wordlist, in the corpus, or in the online dictionary;
`tblian` is 做子彈／取尾巴; the one root it reaches is `bir` 車聲（擬聲詞）. His
own variant note gives the synonym — *vl. lukus pspingan*, and `psping` 妝扮飾物
is listed — which tells us what the phrase MEANS and nothing about how his word
is spelled. **A synonym identifies a sense; it never spells a word.**

**`msska` refused,** and it is the instructive one because it arrives looking
exactly like `mnalu`: same report bucket, same identity spelling, root listed
and glossed. The difference is the only place it can be. `mnalu`'s root means
好 and his gloss means 和睦 — the same thing said twice. `msska`'s root `ska`
means 中間 and his gloss is 龜裂——裂開; getting from one to the other needs
"splits down the middle", which is a story about the word rather than evidence
about it. `mss-` is the reciprocal (67 members in the wordlist, all "at each
other"), modern 土地裂開 is `bkal`, and `msska` is absent from wordlist, corpus
and dictionary alike. *A synonym failure and a real disagreement look identical
in the report; only the root's meaning tells them apart.*

**`conc.py` added** — every corpus sentence containing a word, printed with its
Mandarin. The refusal in batch 183 was about AUTOMATION: splitting one
translation across several words is a guess. A person reading four sentences
that all contain a word is identifying it by its contexts, which is how the
work is done. It prints and never writes. All four words tried this batch
returned 0 sentences, which is itself the finding — these are Pecoraro's words,
not the corpus's.

Gained 1, lost 0. Blocked pairs 435 → **432**; deliverable **5,003 / 92.05%**.
Dark 44,019 / 97.9353%, pale 894. 16/16, 9/9, 28/28.

## Batch 186 — the analysis was wrong, not the gloss

`pnguwan` — his `Pngoan`, 3 pairs, PONGO › Pngoan 綁紮——已打好的結 plus two
sentences under SLOXAO about a knot that will not come undone.

**It was never a gloss problem.** `roots()` reached `pgu` 藜 — goosefoot, the
plant — and stopped, so the gate was refusing an analysis nobody would defend.
The word is `pungu` + `-an`, and the ILRDF dictionary gives `pungu` as
膝關節／**繩結**／關節／膝蓋 at frequency 26. His 已打好的結 and its 繩結 share
結 outright: had the analysis reached the root, the ordinary gloss test would
have passed it with no hand at all. `pnpungu` 做繩結 is in the wordlist too. A
knee is the knot of a leg.

**A rung was priced first and refused.** `awag()` exists because a root in -aw
writes -ag- before a suffix, and the wordlist settles that 76 pairs to 2. The
parallel claim — a root in -u writes -uw- — has 121 forms of the right shape and
23 where a vowel restores to a listed root, which reads as support until the 23
are read: `huway` 慷慨, `buwan` and `ruway` are roots in their own right, so
`gmhuway` is `gm-huway`, not `gmihu-ay`. Only `mktru` → `mktruwan` survives.
*One supporter is not two*, and a rule built on it is a shape test with a story.
`mktruwan` still does the one job it can: the glide is WRITTEN, so the form is
`pnguwan` and not `pnguan`.

**One ruling, six words.** `pnguwan` vouches the root, and `ppungu`, `emppungu`,
`ppngui`, `ppnguun`, `ppnguwan` followed off it. Lost 0.

Blocked pairs 432 → **429**; deliverable **5,006 / 92.11%**. Dark 44,029 /
97.9576%, pale 884. 16/16, 9/9, 28/28.

## Batch 187 — his k was a q, and the map had already said so twice

`tknayun` — TAXA 我沒有同伴 and TK'NAI › Tknayun 同伴（所期望的、正常的）.
`roots()` reached `kayu` 木製湯碗, a wooden soup bowl, which is the same kind of
false analysis batch 186 refused: the letters admit it and nothing else does.

**The corpus settles it, sentence against sentence.** `qnay` and `mtqnay` are
一起走（去）, and `conc.py` returns ten real corpus sentences for `tqnay`:
*tqnay su ima?* 跟誰去, *tduwa ku tqnay mowsa hug?* 我也可以一起去嗎,
*asi na pseupu tqnay musa da* 他只好帶著弟弟同行. His own sentence is
*Ima ka tknayun so?* 誰要陪你去 — **the same sentence**. This is the use the
phrase rows were kept for: read for one word by a person, not split by a rule.

**This one changes his letters, so it went in the map and not in HAND_RULED.**
`tknai` → `tqnay`, `tknayan` → `tqnayan`, `tknayun` → `tqnayun`; `tqnay` and
`tqnayan` are listed, and `tqnayun` is `t-` + `qnayun`, also listed. q↔k is
excluded as a blind char rule and stays excluded — this is one word decided on
its gloss, which is the only way that letter may ever move.

**The map had already made the substitution for the sister slots.** `tknai` and
`tknayan` were ALREADY `tqnay` and `tqnayan` before this batch, derived by the
generator with no manual entry; only `tknayun` held out on an identity claim.
The family was evidence, and it was already written down. Adding the three
manual entries changed exactly one rendered token — the per-token map diff says
so — and the two that agreed were confirmations, not changes.

**One phantom.** The rebuild also dropped a map key `rinalox`, which reads as a
lost claim until you look for the token: it is in no entry of `entries.js` in
any spelling. A projected key no token uses is dead weight, and the DOM confirms
it — green held at 34 across the rebuild. *A map key is not a claim about the
page unless a token reaches it.*

`tknayun` ×4 pale → dark. Blocked pairs 429 → **426**; deliverable **5,009 /
92.16%**. Dark 44,033 / 97.9665%, pale 880, green 34. 16/16, 9/9, 28/28.

## Batch 188 — two rulings, and the same failure under both

**`embqru`** — his `mbq'lo`, BQ'LO › Mbq'lo 滿是凹凸與高低不平, and in BALAE
about levelling a road. `bqru` is 肉瘤／痛風；關節石, a lump on a body, and a
bumpy road shares no character with a tumour. **The family had already made the
extension**: of its 89 members, `dmpsbqru` is 採樹瘤者 — a gatherer of TREE
burls — and `sbqru` is 長很多肉瘤, covered in them. `embqru` is absent from the
89, which a family that large makes look like evidence; what it shows is that
the wordlist files this root's em- forms as `empeebqru` and `embbqru`. `em-` +
a listed root is routine and not a favour — **116 verified em- words are absent
from the wordlist**, mapped by the tier-W schwa rule and verified off the root.

**`pnsmkan`** — his `pnsm'kan`, SMUK › Pnsm'kan 已釘之物；釘的動作. The wordlist
glosses `smuk` 金鋼樹（樹木名）, a tree; the ILRDF entry prints 金鋼樹（樹木名）
／**釘子**／蘇穆克（地名）／**鐵釘** at frequency 7. His 已釘之物 shares 釘 with
it outright. The gate never saw that root: `roots()` offered `smka` 一半, `smku`
保存, `mkan` 吃 and `psmkan` 讓…金鋼樹, because reaching `smuk` needs the root's
own u restored. His apostrophe is the evidence for the syncopated spelling — he
wrote a mark where the u had been.

**Both were the same failure, and it is not the one the bucket names.** A
refusal filed under "gloss disagrees" can mean the gate weighed the meaning and
said no; it can also mean the gate never reached the word. `pnguwan` (186),
`pnsmkan` and, in a different way, `tknayun` (187) were all the second kind.
The bucket cannot tell them apart and the dossier can.

Gained 3 — `embqru`, `pnsmkan`, and `psmuk` off the vouched root — lost 0.
Blocked pairs 426 → **422**; deliverable **5,013 / 92.24%**. Dark 44,040 /
97.9821%, pale 873, green 34. 16/16, 9/9, 28/28.

## Batch 189 — the vowel that has to go back before anything can be read

Three of the last eight rulings (`pnguwan` 186, `tknayun` 187, `pnsmkan` 188)
were the same failure, and none of them was a failure about meaning. `roots()`
walked the letters he wrote, found no listed root inside them, and the refusal
was filed under "gloss disagrees" — a bucket that names the last test rather
than the one that actually stopped. In each case the root was there and one
vowel was missing from it.

`Inflection.restored()` generalises the three. For a word no rung above reaches,
put ONE vowel back at one position — every `aeiou` at every index — and analyse
the result. **The gloss gate is unchanged**: `_agrees` must still find a shared
Han character between his word-level Chinese and the root's modern gloss, so a
search that can invent five letters at every position is still answering to the
meaning and not the shape. Candidates are sorted longest-root-first, the same
guard rule 10 carries.

Over all 589 unverified map values it fires on 17. The paradigm `pqdrxan` /
`pqdrxi` / `pqdrxun` is the case that shows it is a rule and not a coincidence:
three slots, no rule above touches any of them, and one `u` puts all three onto
`qdrux` 石牆. That is the shape a real syncope leaves behind. The rest run the
same way — `puqi` ← `uqa` 吃, `ppyaun` ← `iya` 不要, `smkan` ← `smuk` 釘子,
`qnbsranan` ← `qbsuran` 兄姊, `tnbuyan` ← `tabuy` 下來.

**And the rung nearly shipped as a subtraction.** Wired into `word()` at
0.0390625 it reported *gained 0, LOST 7* — `emppuyas`, `ndyami`, `nnuhan`,
`pdjilan`, `pnttukan`, `pnuhi`, `pnuhun`. Nothing evidential had happened: the
ladder returns a score, but the writer collects the verified values by listing
each score band by hand, and 0.0390625 was in neither the `good` sum nor the
`emit` table. Seven words that used to fall through to `chained` now stopped one
rung earlier, scored, and were dropped on the floor. Fixing the collection —
`restd`, `good`, `emit`, and the tier renumbering 11-14 → 12-15 — turned the
same build into gained 17, lost 0. **A cascade whose bands are enumerated
downstream is not additive by construction; inserting a rung is an edit in two
places, and the measurement is what says whether you made both.**

Blocked pairs 422 → **412**; deliverable **5,023 / 92.42%**. Dark 44,069 /
98.0466%, pale 873 → 844, green 34. 16/16, 9/9, 28/28.

## Batch 190 — eleven rulings, one map pin, and a family that convicted its own head

Twelve dossiers off the `gloss disagrees` and `root unglossed` buckets. Eleven
went to `HAND_RULED`; one was not a colour question at all.

**The refusal pattern that dominated the batch: two glosses that mean the same
thing with zero shared Han characters.** 因濕冷而發抖 vs 凍僵, 甜味 vs 甘蔗,
無知 vs 白痴, 主幹 vs 田埂, 拿 vs 除去, 讚美 vs 仰慕. `regular()` requires
`_agrees()` — a shared character between his Chinese and the root's modern gloss
— so each of these failed a test it was right about. No widening of the *shape*
rules reaches this class. Only reading the two glosses does, which is why these
are hand rulings and not a new rung.

**A word that needs two rungs at once falls through both.** `mritan` wants
`restored()` to find its root *and* the crossref rung for his pointer gloss; each
rung supplies exactly what the other is missing, so the cascade — being a strict
first-match — delivers neither. Worth remembering before adding a rung to fix a
word: check whether the word needs two.

**`sblangan` was a map question, not a colour question.** It carried an identity
claim no source supports. Pinned to `smbrangan` 矛 in `manual_map.json` (ILRDF
freq 42, 11 corpus sentences, and confirmed in the Truku hunting literature by
web search). One key, one line of `modern_map.js` diff.

**`dlutun` / `dldan` — the family convicted the head.** His DLUT (R)
磨碎——搓碾——揉皺 sits over a root the map already handles: `dlut`→`drut`,
`dmlut`→`dmrut`, `mdlut`→`mdrut`, `dnlut`→`dnrut`, `pdlut`→`pdrut`. Two keys kept
the `l` — `dldun`→`dlutun` and `dldan`→`dldan`, an identity claim — and neither
value is attested anywhere. `drut` is ILRDF 輾過去／**用手揉起來**, sharing 揉
with his own gloss outright: search from the meaning, not from the letter.

The vowel was the only open question, and the wordlist splits on it: `brut`→
`brutun` keeps it, `krut`→`krtun` drops it, and those are exact rhymes of `drut`.
Shape cannot decide between two words of the same shape going opposite ways. His
own witness can — he wrote `DLUT` full and `Dldun`/`Dldan` syncopated, which is
the `krut` alternation. Pinned `drtun` / `drtan`.

**I predicted they would stay pale and they did not.** The syncope rung had been
in the ladder since long before; it simply could never see the root through the
`l`. Removing a wrong claim let an existing rung fire — so the gained/LOST
difference, not the prediction, is what reported the outcome. *A correction is
allowed to be worth more than you costed it; measure it anyway.*

Blocked pairs 412 → **391**; deliverable **5,044 / 92.80%**. Dark 44,104 /
98.1245%, pale 844 → 809, green 34. 16/16, 9/9, 28/28.

## Batch 191 — the loss line as an instrument

Seven rulings. Two of them were nearly wrong in ways only the gained/LOST
difference would have shown, so this batch is mostly about that measurement.

`ddngusun` (his DUNGUS 理所當然——相稱——合宜): root `dngusun` 目標；對象 ILRDF
freq 12, and the imperatives `dngusa` 別專注 / `dngusi` 去專注於 name the verb —
"focus on, aim at", which is what gives his `Msdungus` 盡心盡力. Reduplicant plus
`-un` = "what one aims at" = 被視為理所當然的事. No shared character anywhere.

`stgtgut`: the analyser stopped at `tgtgut` 最邊, which is itself `tg-` over
**`gtgut` 鄰居** (freq 8, 4 corpus sentences). His card is 毗鄰的——鄰近的——相鄰的
with `Ggtgut` 鄰居們 — 鄰 in both. `s-` + `tg-` + `gtgut`, degeminated, and the
真正 in his 為了真正靠近 *is* that `tg-`. **A half-peeled root fails a gloss test
its full form would pass.**

`kkrang` / `mkkrang` (his KK'LANG 發抖——打顫): root `krang`/`kran`
碗掉下來破碎的聲音（擬聲詞）, freq 14. The bridge is on the same root — `krkran`
發抖, `pkrkran` 發抖 — clatter becoming shiver-until-you-rattle. Modern
reduplicates it as `krkran`, not `kkrang`; that is a cognate, and a cognate
explains a word but never spells one, so no pin.

`knslaan`: his headword KSLAAN *is* the modern lemma letter for letter (freq 5,
缺乏) against his 饑餓虛脫－精疲力竭. His `Knslaan` gloss is the pointer "d° dans
la forme accomplie" — the mritan shape, a gloss with no content to test.

### The K'LOX near-miss — an override the loss line refused

`krhun` (his K'lxon) is rooted by the analyser in `krhi` 烤; the root is `kruh`
旱地, which shares 旱 with his 乾——乾旱——荒漠般的, and `krhan` 烤乾 shares 乾 with
his `K'lxan` 乾旱——貧瘠. One homophone off.

But before seeing that I chased his own tag: *"(Q'LOX ? — parentée avec QOLOX =
crâne ?)"* — and `quluh` really is 光禿的山和不長毛髮的頭／骷骼／貧瘠地, one lemma
holding both his 頭骨 and his 荒漠般的, with `qlquluh` 貧瘠地 and `mquluh` 很貧瘠
behind it. I repinned the whole K'LOX family to it. The build answered **LOST 3**:
`kruh`, `krhan`, `mkruh` were already dark, on attested spellings, with the right
glosses. **His tag carried a question mark; attestation outranks it.** QOLOX keeps
`quluh`, K'LOX keeps `kruh`, and the fix was one hand ruling, not seven pins.

Second lesson from the same detour: **reverting by popping keys assumes the keys
were new.** Two of the seven — `k'lxon` and `q'lxan` — were committed entries with
their own values, and popping them deleted claims I had never made. The map diff
against HEAD is what caught it; `git checkout` on the file is the honest revert.

### `pklbiyan` — a place name protecting a common word

His LABE (R) 一夜的時間 is `rabi` 晚上／夜 (freq 9), and `Mklabe` 過夜 is `mkrabi`
過夜 (freq 5) — both already mapped and dark. Three syncopated members kept his
`l`: `klbiyun`, `pklbiyan`, `pklbiyun`, the middle one on a tier-M identity. The
`l` looked attested, because **`klbiyun` is in the wordlist as 奇萊山** — Mount
Qilai. A name is not evidence about a common word that happens to spell like it
(MIXALASI in reverse), and his own suffixed forms write the vowel as `i`
(`lbi-yan`), confirming the root. Pinned `krbiyun` / `pkrbiyan` / `pkrbiyun`; all
three went dark on `rabi`, since 過夜的地點 shares 夜 with 晚上／夜. `klbiyun`
leaves the file, and his book uses that token on the LABE card only — checked.

Blocked pairs 391 → **383**; deliverable **5,052 / 92.95%**. Dark 44,123 /
98.1667%, pale 809 → 790, green 34. 16/16, 9/9, 28/28. The `gloss disagrees`
bucket falls 39 → 31 types, which is where all seven rulings landed.

## batch 192 — eight hand rulings, and a source key that only looked inconsistent

Eight rulings, no map pins, every one measured LOST 0 as it landed: empraqat
(耀田 vs 三叉的箭頭), mrbuq (凹陷 vs 深), pnrikit (殘廃 vs 瘧), empklutut (親戚 vs
繼續), knluusan, pknluun, penduk (使之關閉 vs 門；橫隔膜), empngpung (小丘 vs 山崗).
Seven of the eight are the same refusal the last three batches have been made
of — two glosses meaning one thing with no character in common — and none of
them needed a spelling decision, only the reading of the two glosses.

The one that cost something was empngpung. His sub is a single slot he spells
two ways, Mpnpong and mpngpong, and manual_map sent those two keys to two
different modern words: empngpung and mpngpung. I read that as an
inconsistency-within-a-root, repinned mpnpong to mpngpung on the argument that
his own variant yields it under the plain rules while empngpung needs an e he
never wrote, and rebuilt. The build answered by mapping BOTH keys to empngpung
anyway. Tier W — the written schwa before a word-initial labial, batch 25 — had
already settled the question with a measured argument: ^mp occurs in exactly one
of 38,687 modern types, modern writes emp- (1,651 types), and his transcription
drops the schwa word-initially exactly as it does word-internally (xnglyeq →
hnegliq). The e is not invented; it is what modern orthography writes.

**A source key that looks inconsistent is not a rendered inconsistency.** The
map is generated, and a post-pass composes with the pins; two keys can differ in
manual_map.json and still print one word on the card. Read the generated map
before repinning — the same reflex as the standing rule that only the DOM is
evidence about colour. Reverted with git checkout on the generated input, and
modern_map.js came back byte-identical, which is what a clean revert should look
like.

ILRDF holds none of the prefixed forms — mpngpung, mngpung, pkpngpung,
pnkpngpung all return nothing — so the register carries pngpung 山崗 alone, with
six corpus sentences, every one of them a rise of ground: 高山斜稜, 山頂,
奇萊山南峰. His head PNPONG is 山頂＝隆起一個包 and shares 山 with it, so only the
sub ever failed. The ruling cleared the whole card: all three PNPONG examples
now resolve with no blocked span.

DOM: dark 44,140 (98.2046%) | pale 773 | green 34 | total 44,947. Blocked pairs
383 → 375 (354 with one blocker over 307 types, 21 with two or more).
Deliverable 5,060 / 5,435 = **93.10%**. Suites 16/16, 9/9, 28/28.

## batch 193 — six rulings, three refusals, and a pin written in the wrong alphabet

Six rulings (haduri, qmapah, tpssagan, sdmatan, psnegulun, knsupu) plus the
STA"TO card taken whole, and three refusals. Gained 10, LOST 0.

Two of the six were homophones the analyser lost, and in both the sentence was
the only instrument that could find them. haduri: his Xdoli reads as hduri, the
imperative of hdur 不同意／反對, matching his vowels with nothing dropped — or as
haduri from hadur 獵首筵席, needing the schwa restored. The example is Mark 1:44,
要按真正的禮儀獻祭…好給他們以此為見證, and "oppose it according to the true rite"
is not a sentence. sdmatan: the register glosses damat 菜 and sdamat 菜；菜餚, so
the analyser offered dmatan 用…配菜 for a card meaning 悲傷、鬱悶、思念 — but the
same root carries the second sense across csdamat 思念;寂寞;哀傷, kdamat 想念,
kmdamat, empkdamat, smdamat, and tnsdamat 悲傷 shows sdamat takes it as a stem.

**A pin must be written in the map's key form, not in his.** The STA"TO card was
entirely unmapped because his " marks a long vowel; modern writes it ee (steetu
上坡, 11 corpus sentences). I pinned seven forms and four were inert — tkey()
folds " to ', so the map's key is sta'to, and my sta"to matched nothing. The
gained-list caught it: smteetu was ruled but never appeared. Rewritten in the
apostrophe form, the card cleared four sentence pairs, and it turned out the map
already had sta'to→steetu and snta'to→snteetu right; only msttu and smttu were
wrong. Same lesson as batch 192 from the other side — read the generated map
before and after, because the source key and the rendered key are different
things.

psnegulun was one form escaping its own root: every other form on his SNUGUL
card was already on snegul 跟隨 (psnugul→psnegul 是跟隨, mpsnugul→empsnegul), and
only the apostrophe form fell through the lexical match to the blind rules,
which took his gul to gur and dropped the schwa his apostrophe marks. Prompted a
check of the whole class — 1,150 apostrophe keys in the map, 94 with a non-dark
value. Healthy; an individual miss, not a vein, so no sweep.

Three refusals. psqgu: the sense is certain (his 猛然跳起 against msqqgu 跳起來)
but the form is not — the register splits the senses by the doubled q, msqgu is
會有"公雞叫聲", the rooster stem's own p- form is pqguaw, and no corpus token
exists on either stem. One supporter that disagrees in the very letter at issue
is not two. sdangan: no source in any shape, his own gloss ？？（詞義不明）.
snuqu: nuqu 倒是 and uqu 生氣 are both glossed and both wrong, and suqu is in the
attested list but absent from ILRDF with no family and no corpus token — an
unglossed orphan is not a supporter.

DOM: dark 44,160 (98.2490%) | pale 753 | green 34 | total 44,947. Blocked pairs
375 → 367 (347 with one blocker over 300 types, 20 with two or more). The gloss-
disagrees bucket fell 23 → 15 types. Deliverable 5,068 / 5,435 = **93.25%**.
Suites 16/16, 9/9, 28/28.

## batch 194 — fifteen rulings, six refusals, and a vowel that is only there
## before a suffix

The TG'LA card came up split: mtgila dark with the vowel, tgla, mtgla and
tnglaan dark without it, and his own head note saying 某些說話者清楚地讀成 TGI…
His sub is spelled "Tmg'la (tngila)" — he writes the vowel his apostrophe
elides. tgla is attested, but its gloss is 麴, yeast; the register carries his
sense on the voweled family — gila is glossed 「tggila 拖拖拉拉」的詞根, tggila runs
in text as tggila mtutuy kdjiyax ka swayi snaw 弟弟常常賴床, tgila is listed. An
attested value can still be a wrong value, and only the gloss catches it.

So I pinned the whole card onto the vowel, and had to take half of it back. The
batch-190 note two screens up already held the counter-evidence: sglaan 讓…耽誤
(freq 6) and sglai 使…耽誤 are attested, sgilaan and sgilai are not. This vowel
syncopates before a suffix and stays everywhere else. His Tnglaan and Kntglaan
were right as he wrote them; tgila, tmgila, mtgila and tngila take the vowel.
A root can be consistent and still take two shapes, if the split is conditioned
— and **don't re-derive a standing finding** cuts both ways: the note I did not
read was the one that had already done this work.

Taking the two pins out was not enough. With the head pinned to tgila, root
projection respells every slot on the card off it, and both -an slots came back
respelled with no pin of their own. A slot the projection must not reach has to
say so out loud, so tnglaan and kntglaan are now identity pins.

The same syncope then settled slungan in one step: his slongan blocks two
sentences and his own AN card glosses it — parler à la mer (Silong = mer). silung
海 and gsilung 海 are attested, the latter with 222 corpus sentences, and silung +
-an drops the penult exactly as sgila does. msilung, the stative on that root,
went with it.

Two cards were rendering one root as two words. TBNAO is in the register almost
slot for slot — tbnaw 胖子, mtbnaw 胖, kntbnaw 胖, ptbnaw 使胖的 — and only his -un
form had wandered off to ptbnuun, on the analyser's root tbnuun 要堆壓, a shape
hit meaning to pile and press. The root ends in -aw and its own -an form shows
what a suffix does to it: kntbnagan, w→g, the same alternation the register makes
in bgbagun, bglagun, bhragun, bkragun, btragun, dhagun. So ptbnagun. On BUGO the
prefix itself was written short: the map had mabugo→mabgu and mpabugo→empabgu,
but the inchoative is maa- (468 types) and empaa- (51), ma- before a consonant
cluster does not occur, and the seven bare empa- types are all emp- on an
a-initial root. maabagu 形成焦黑 is the same shape on a b-initial CCV root. So
maabgu and empaabgu — which drops mabgu, dark on a rung that spelt the prefix
short. That is the second override this batch and both were priced first.

The rest were the gate refusing on Chinese it could not match. ptkanun: TIKAN
renders cikan at the head and pcikan in the causative but keeps tkan- in every
suffixed slot, and tkanun 杵 runs in text as dmux o tkanun ni skuu 以備舂米或保存用
— his faire décortiquer, in the character his own head gloss carries and his sub
gloss drops. mtkumax and tmkumax: TKUMAX and ptkumax 使...不準 are attested, so
the register writes this root with these letters and takes the causative on it;
the ILRDF gloss 不準；沒有命中 shares nothing with 顛倒, but its one corpus sentence
is a deadfall trap being tripped, 整塊石板被動快速壓下, which is his renversé.
mtudu stood on a standing finding — batch 190 settled that tudu is the ridge and
the spine — plus mntudu, the ⟨n⟩ perfective of the word itself. sghuwayan had its
sense one slot away: mhuway is glossed 恩慈／感謝／慷慨／謝謝 and his card is 謝意.
ntlawa was ruled off its sister mtlawa 藍色, his own second sense, sharing the
character. msska: ska is 中間, but skaun is 切成半粒, and ms- doubles its s before
an s-initial root exactly as in mssaang and mssbarux 相互換工 — a rock that splits
down its own middle. kkdsan needed no ruling at all, only the pin: 一生；終身 is
attested and in the corpus, and his kk- is their kk-.

Six refusals, four of them the same shape of finding — the register has the
thing, under another word. ksudan 織布用的梭子: the shuttle is gikus, freq 24, with
a family (tmggikus 製作梭, tnegikus 梭的主人) and a corpus sentence of it crossing
the warp; ksudan, sudan and suda are absent everywhere. mslangan: the analyser
offered mslangu 積水 and a rusted roof that pools water is a metaphor I would be
inventing — his own SLANGAN card says Rouille 鏽 outright, and the register's rust
is girang with some twenty derivations. tbiran 節慶盛裝、禮服: no gloss in any table
carries 盛裝 or 禮服, and the variant he prints beside it is the one that spells
itself (pspingan 讓…化妝). snpsaran was thinner still — pusal, spusal, smpusal,
psalan, psaran absent from wordlist, e-dictionary and corpus alike, and the only
gloss carrying 重新開始 is snegbarah. With tnbiyan and tbiyun recorded earlier, the
gloss-disagrees bucket is now 6 types and every one of them is a written refusal.

DOM: dark 44,188 (98.3135%) | pale 724 | green 34 | total 44,946. Blocked pairs
367 → 348 (328 with one blocker over 286 types, 20 with two or more). Deliverable
5,087 / 5,435 = **93.60%**. Suites 16/16, 9/9, 28/28.

## batch 195 — twenty-three rulings, five refusals, and the root gloss that kept
## belonging to somebody else

The pattern of this batch was not a spelling rule. It was that the analyser's root
gloss was, again and again, a real modern word that was not his word. hnkan is
attested and means 把…便宜, from hnuk 便宜 — but his sxnkan is a prison, and the
register's prison is hmkan 關（被關；坐牢）, kolo hmkan in the corpus. ruq is attested
as 吞食聲, a swallowing noise, while his n'loq pierces a roof and his own LOQ card
reads 洞－被刺穿的－破裂的, which is mruq 破 and pruq 洞. alu is 陷阱線, a trap line;
bus is 蒸氣洩出聲; gur is 成群來到的聲音; yuq is a rooster's cry with corpus frequency
0. punu and pitay are both glossed as personal names. Six of the ten were
onomatopoeia or names — the parts of a wordlist that collide most easily with real
words, and the parts a gate reading one gloss cannot tell apart.

The way through was his own book each time. He has a card for XMUK "enfermé - clos
- fermé", for LOQ "trou - percé - brisé", for PUNO "choléra - esprit dérangé", for
PONGO "noeud - articulation" — and the e-dictionary's pungu glosses as 膝關節／繩結
／關節／膝蓋, both of his senses in one entry, because a knee is a knot. Where the
book did not have the root, the ruling did not happen: npnalu (his NALU 代替; the
corpus's only nalu words are snalu 65× and smnalu 22×, both 製作), ppitay (his 臭蟲;
pitay is Pitay Losing in all six corpus sentences and absent from the e-dictionary),
kyuqan (his crachats; the register spits with halus). snpsarun and empslangan were
not re-derived at all — pusal and slangan were searched to exhaustion one batch ago,
and a second suffix on an absent root is not a second question.

Two findings worth keeping. **The sentence can carry its own paradigm.** sxnkan sits
beside Lntadan, and his LATAT paradigm line derives ltadan → l⟨n⟩tadan; so hkan →
h⟨n⟩kan, prefix s- in front, and shnkan needs no letter changed beyond x→h. The case
turned on a single stroke — m or n — so the scan was read before the ruling: page 147
has the two-stroke n, and his nk answers to a modern mk nowhere in the map, 0 of 41.
**And the class can be real when the word is not.** Not one kmkm string occurs in the
whole ILRDF corpus, but kmk- is attested eight times over and every gloss is a want —
kmkdudux 想率先, kmkeisil 想到別處, kmkla 好希望會. The one register word that looked
like an answer, kkmalu, is the purposive 為了…好, a different form; wanting to recover
and being led toward goodness are not the same word.

Three pins came down or went in. nl'bu was going to lbu 不長, the short root, when
this one is the morning root — ml'bu was already pinned to mgrbu, and rbu is glossed
早上（破曉至黎明）, so nl'bu → nrbu completes a split that was half made. s'gulan was
pinned to sguran, which is the blind l→r rule and nothing else: the tie-root is l
throughout — seegul 綁住, enegul 綁著, negul 繫有, empeegul 要…綁住 — and the S'LYEQ
long/short ablaut already in the map notes gives seegul bare against sgulan suffixed.
smalyeq was pinned to smaliq, which is attested nowhere; smeeliq is attested 67× as
浪費, his card's own gloss, and he himself asks whether the a-forms are deformations
of SM'LYEQ. gmalyeq → gmaliq stays, because gmaliq is attested. Slot by slot.

The whole PADYAQ card went dark on one fact: pajiq is 菜, 蔬菜, 青菜 — and empajiq is
glossed 綠色, mgpajiq 綠色的. His card had said so in a line ("généralement employé
pour désigner la couleur verte"), and the gate could not see it because 青菜 and 綠色
share no character. Green and greens are one word here.

DOM: dark 44,213 (98.3692%) | pale 699 | green 34 | total 44,946. Blocked pairs
348 → 324 (304 with one blocker over 262 types, 20 with two or more). The sentence-
gloss-only bucket fell from 44 types / 47 pairs to 20 / 23. Deliverable
5,111 / 5,435 = **94.04%**. Suites 16/16, 9/9, 28/28.

## Batch 196 — a fourth colour, and the pin that was waiting for it

Thirteen rulings, two refusals, one claim withdrawn, and a display change the
user asked for: **names, onomatopoeia and Japanese loans go a deeper brown.**

**The rulings.** `psmkun snka stmaqun muli pneydang psnruun pklilug ciyusun
ppskngalun` through `HAND_RULED` (78 → 87), and `ma isu` / `nasug` / `sbgay` /
`psnruun` / `meakay` through `manual_map.json` (1,869 → 1,877 keys). Two patterns
recurred: *the gloss table holds one sense of a word that has three* — `smuk` is
the tree in the table and 釘子 in the e-dictionary — and *the map had already
ruled the root and left one slot to the blind rules*, `gnwit` beside
wit→uwit/mawit→meuwit, `psnluun` beside sn'lo→snru. `meakay` is the shape worth
keeping: pinning the spelling let the analyser reach `akay` 痛, whose gloss
agrees with his card, so the word went dark with no hand rule at all. `gneuwit`
was pinned as a **deliberate pale** — regular by `kneuwit`/`gneabu`, attested
nowhere, so it buys no dark; what it buys is that one card stops saying two
different things about one root.

Refused into `refused.txt`: `narung` (no card, no candidate) and `ddjilun`
(`djilan`/`djilun` listed but glossed nowhere; the e-dictionary holds none of
five queried forms).

**The fourth colour is a display change, not a metric change, and that is the
point.** Names (247 values) and loans (141) were already dark — folded into
`seen` and emitted as code **1**, which says *a modern source lists this word*.
No source lists `budosyu` 葡萄酒 and none lists every man in a 1977 village.
The claim was true in colour and false in kind. Code **16** now names the real
warrant, 256 values reach the page on it, and `app.js` paints them
`--accent-deep`. The class is **additive** — the span carries `w-mod w-cls` —
so `blockers.py` and `dom171.py`, which both select on `w-mod`, keep counting
these as dark and nothing downstream had to be taught the new state. Measured
from the DOM (`logs/brown196.py`): 673 occurrences, 256 distinct, computed
colour `rgb(90,36,22)` against `rgb(156,69,48)` for ordinary dark. **A harness
that cannot see a colour reports it as an absence, so the census asks the page
for the colour and not the stylesheet for the rule.**

Onomatopoeia was voted in with the other two and got no population, on his own
evidence: his book declares **7 sound cards and 2 name cards**. The onomatopoeia
problem was the analyser's roots, never his words.

**`pdrut`, and what rule 2 will agree on if you let it.** dom171.py had pinned
`pdrut` pale with an instruction on the pin — *if this ever goes dark, check that
it did so on a gloss and not on another `id` freeze*. It was dark, at code 2, and
the check refused it. Not a freeze: the character his gloss and the root's share
is **去**, from his EXAMPLE sentence 我沒時間去請人磨小米 against `drut` 輾過去.
A man with no time *to go* and a millstone that rolls *over* are not the same 去,
and neither is about grinding; his own word gloss, 使人碾磨, agrees with the root
on nothing. In `HAND_NOT_REGULAR`, and the LOST line reports exactly one value.

Whether that was a rung or a hand list was **measured, not assumed**
(`logs/share196.py`): of 1,068 code-2 values, 593 distinct characters carry the
agreements; 223 reach it only through a sentence-shaped string of his, but 72 of
those agree on a *run* (燒焦, 呻吟, 上面, 先走), which coincidence does not supply;
and of the 151 single-character ones only **nine** agree on a character thin
enough to mean nothing — `empsparu` 大, `kdagun` 來, `mkatan` 來, `pdrut` 去,
`pngalun` 來, `psagan` 來, `spkmalu` 好, `tnklaun` 到, `tnqtaan` 到. Nine is a
list to read one at a time, which is what batch 142 concluded about 大/小. The
other eight are the queue.

**Two stale pins came off the same file, on batch 190's evidence.** `dldan` and
`dlutun` were pinned pale as syncopated slots no rung could reach; batch 190
respelled them `drtan`/`drtun` on his own full-versus-syncopated witness and the
syncope rung fired on both. The strings the pin named are no longer rendered at
all, and **an absent span is not a pale one** — the test was reporting a colour
it could not see. They are pinned dark now, in the direction they actually went.

`loose179.py`, `cite179.py` and `nav178.py` — the three standing suites — lived
only in the session scratchpad and are now in `logs/`, where a later session can
still run them.

DOM: dark 44,230 (98.4070%) — of which 673 settled by class — pale 682, green 34,
total 44,946. Blocked pairs 324 → **310** (290 with one blocker over 250 types, 20
with two or more); the sentence-gloss-only bucket 20 types → 10. Deliverable
5,125 / 5,435 = **94.30%**. Suites 16/16, 9/9, 28/28; dom171 4/4.

## batch 197 — to 98.5%, and the census that outranked the blocker list

Twenty-one words settled: seventeen hand rulings, four names, and two respellings
in `manual_map.json`. Eleven refusals written down. LOST 0 at every rebuild.

**The rulings, and what unblocked each.** All seventeen were the same shape — the
root is in the modern wordlist and carries no gloss, so the gate had nothing to
agree with — and each was decided by reading the family or by searching from the
meaning, never from the letter.

    pnkltudan  lutut 連結/親戚 70 is his own 相連; pklutut listed 12, pnltudan 24
    kmpspusu   pusu 主要的,根本的 958 shares 根 with his 根基/根源
    sshgan     sahug 水瓢(舀水用) — his 舀 inside their gloss; shgi is the syncope
    ndmpatas   empatas 在…讀書 105, patas 信 737, against his 讀書人
    smhngi     shngii/shngiun/shngian 忘記, nine glossed forms of his x'nge
    snsikan    smsik glossed 我在掃地 by the corpus, not by any table
    dtduling   tluling 腳趾（與tduling 同義）— the register names his spelling
    mtru       tru 三 497; `taru` was 大陸 transliterated, a homograph freeze
    msthulang  psthulang 自大, the only one of twelve pride words he can reach
    dtanah     the corpus prints 「Tanah tunux」=「紅頭」, which is his 日本人
    empkmalux  mnalux 生病, found by meaning after l→r had produced a null
    treura     mtreura 明顯 7, mteura 公開的, pteura 很明顯的, steura 清楚的

**Two spellings changed, both because a rule had beaten a gloss.** `mt'lo` had
been given a restored vowel and landed on `taru`, whose 31 corpus sentences are
all Ta-ru, a syllable of transliterated 大陸 — the batch 171 freeze again, a
homograph holding a slot. `mpkmalox` had been given l→r and landed on `marux`,
listed at 0 with no gloss and no sentence; the meaning search found `mnalux`
生病 with the l standing. Batch 168 measured this letter — 1,151 of his l become
r, 1,275 stay — so the rule cannot call it and the gloss must.

**Four names, and where a hand-ruled name goes.** `name_population.json` is
generated by `build_modern_map.py`; three tokens written into it by hand were
silently overwritten on the next map build. The place for a name reached only
through an example sentence is `HAND_NAMES` in `inflection.py`, which is what it
was built for. dtumi (§ Mksipao ka dTome), sktadaw and skbowxil (his SK card
glosses the prefix *feu*, the late), dbiyang, and nkmurisaka/dmurisaka finishing
the Morisaka set that murisaka and mkmurisaka started. All emit code 16.

`ndiyan` was written into HAND_NAMES and taken out again: the DOM says w-raw,
green, not pale — his spelling has no o, l or x, so the char rules hand it back
unchanged with no map entry at all. Colouring it would need an identity entry
claiming his Diyan is modern `diyan`, and his French writes the man Djian. One
occurrence is not worth a spelling verdict we cannot back. **A green span is not
a pale one, and the fix for green is a map entry, not a warrant.**

**The census outranked the blocker list.** `blockers.py` ranks by sentence pairs,
so a word spent on headwords, sub-forms and crossrefs never appears on it. Late
in the batch the DOM's pale spans were ranked by occurrence instead, and the head
of that list held `treura` at 13 — more than any blocker on the board and the
largest single pale word left on the page. It was ruled in one reading. The rest
of that head was priced and refused: rngut/rmngut/rngutan at 15 (the register's
pregnancy root is mshjil end to end), klulu at 7 (tlulug 葡萄 agrees and cannot
spell his k), qrip at 6 (nothing of that shape exists), msnoxel at 5, ksudan at 4
(the shuttle is gikus). **Rank the pale by occurrence, not only by pair.**

Suites 16/16, 9/9, 28/28; dom171 0 failures. Blocked pairs 310 → 282, so
deliverable 5,153 / 5,435 = 94.81%. Dark 44,275 / 44,946 = **98.5071%** (dark
43,594 + class 681), pale 637, green 34.


## Batch 198 — "Worth trying for 98.67?", and the pale bucketed before it was worked

The question was a number, so the first work was pricing it, not ruling. The pale
head is flat — the top 45 of 447 types carry 23% of the occurrences — so a
leaderboard could not answer whether 98.67% was reachable. `price198.py` sorted
every pale type by what the analyser can say about it:

- **A** — root attested *and* glossed: 91 types, 110 occurrences.
- **B** — root listed but unglossed: 28 types, 34 occurrences.
- **C** — no analysis at all: 328 types, 493 occurrences.

A+B ≈ 144 occurrences is the whole reachable seam; 98.67% needed +70 of them, so
the answer was yes-but-it-is-half-the-seam, and the practical ceiling is ≈98.8%.
**Bucket the pale before working it.** The buckets tell you whether a
morphological argument exists — they do not rule anything, since HAND_RULED will
darken any value listed in it. That is exactly why the pricing had to come first.

Sixty-one rulings landed, from three seams.

**The sibling seam.** Many HAND_RULED entries from old batches license the slot
beside them: empraqat→praqat, knluusan→knluus, pknluun→pknluan, sdmatan→psdmatan,
pklilug→plilug, kkrang/mkkrang→tkkrang, ptkanun→ptkanan, psnegulun→psnegulan.
Cheap and consistent — but **a sibling is only a sibling if it is the same card**.
`pngraq` looked like a warrant for graq/gmraq/graqun until `d2.py` showed it is
his Png'laq off NG'LAQ 愚蠢——白痴, not G'LAQ 拿取——奪取. Refused.

**The gloss/family seam.** mdakar 禁止 9 for his DAQAL (dkaran/dkari/dkarun);
mring 汗水 19 for his M'LING (mtnring/tnring); gsilung 海 420, where he writes
"SILONG (＝GSILONG)" himself; mhing 熄火 8 for his XENG (khngun/knhngun); qaras
喜樂 46; mrana 逐漸增多 103; dmijil 提著 18; biyuq 淚滴／果樹汁 from the
e-dictionary against the wordlist's "personal name"; gnaliq 取過首級 6, his one
sentence being a beheading.

**The reduplication seam.** `inf.roots()` has no reduplication rule, so every
CC-/VV- form lands in bucket C with root "" — the analyser cannot see
reduplication, and bucket C is therefore not a verdict about a word, only about
the analyser. Stripping the doubled onset by hand found 19 occurrences on very
frequent stems: uuyas<uyas 216, klkari<kari 1608, ssiisil<isil 215, iisu<isu 508,
kiima<ima 525 (he analyses it himself: ki'ima = kii + ima), qqsahur<qsahur 內臟 33.

**Five map values were wrong, and pale was reporting it faithfully.** glani→gleani
(listed outright — it needed the right map value, not a ruling), sqtaqi→sktaqi,
tmtaru→tmtru (the 大陸 syllable trap batch 197 caught, one card further on),
psnguran/psnguri→psnegulan/psneguli (l→r wrongly applied to snegul 跟隨 46).

**`naru` was nearly taken and was not.** 8 occurrences, the biggest single lever
left. `nruan` 代替者 supports the spelling — but grepping this log first turned up
the batch-114 pin: seven of the eight tokens sit in sentences whose Chinese says
好, his nalu being a homograph of malu that a token-keyed map cannot split.
Darkening would queue seven spans to be harvested as the word for "good". The pin
stands. Refusals priced and written to `refused.txt`: the TABE 犁 family (8 over
five slots — the register's plough is sakur, which he names on that card as his
own synonym), rih (6), snpusal (5, the stem `pusal` is not listed at all), sapat
(5), tbiran (4, batch-193 re-priced and standing), slangan (3), graq (3), kdapan,
prjilun, ppitay, kmupan, empkpakux, emburung, kblungi.

New tool: `logs/pale198.py`, ranking `span.w-unv` by occurrence off the DOM with
an `ex` column for spans inside example lines.

gained 62, **LOST 0**. Suites 16/16, 9/9, 28/28; dom171 0 failures. Blocked pairs
282 → 268, so deliverable 5,167 / 5,435 = 95.07%. Dark 44,359 / 44,946 =
**98.6940%** (dark 43,678 + class 681), pale 553, green 34 — the 98.67 asked for,
cleared.

## Batch 199 — the lone pale slot, and 99%

Asked for 98.8, then for 99, and both came out of one instrument: **a pale slot
on a card whose other slots are dark**. Batch 198 had priced the remaining pale
by what `inf.roots()` could say about each word and concluded the seam was nearly
spent at ~98.8%. That was a fact about the analyser. His card is a *paradigm* —
so the question that pays is not "what is this word?" but "what is every other
slot on this card?", and 53 cards were carrying 139 pale occurrences beside three
or more dark ones.

Two passes, 87 rulings and 20 map values in total. **99.0010%** — 43,810 dark +
684 class of 44,943 spans; pale 415 / 294 distinct; green 34. Deliverable pairs
**5,208 / 5,435 = 95.82%** (from 5,167), blocked pairs 268 → 227.

**The gloss test did the real work, and it ran before each ruling, not after.**
It refused a third of the queue, including one that would have been six wrong
words at once: his TABE family looked like clean `-un`/`-i` gaps beside a dark
`tbiyan` — and `tbiyan` is glossed 下來, not 犁. Also `sapat` 舖 vs his 行為不檢,
`qrut` 啃骨聲 vs his 梁, `shik` 吻 vs his 舔, `mqraq` 抓（seize）vs his 發癢 (the
register's 癢 is `ghguh`), and `rangi` 不遵守習俗 sitting dark on the card he
glosses 剩下的, where the register's 剩餘 is `sngari`. **A card head that is dark
for the wrong reason licenses nothing beside it.**

Five b198 pins came down — `prjilun`, `kdapan`, `empkpakux`, `kblungi`,
`emburung`, `ppitay` — each refused for a reason the lone-slot view answered.
`kdapan` had been read as 寡婦 (`kmptuhan`); it is the `-an` slot of QODAP 熄滅,
where `qudak` (風)減弱 is dark. Its card now renders QDAKAN.

**PAKOX is the case for deciding slot by slot.** `pakux` is glossed 老鼠 — a
homophone — but `makux` 翻動 on the same card meets his 翻轉 exactly, so the root
is right and the six empty slots are gaps.

**Reduplication as a seam, not a caveat.** `roots()` still cannot see it, so every
CC- form reports no root; stripping the doubled onset by hand and asking whether
the base is dark *on the same card* found `rramil`, `rranaq`, `hhmadan`,
`llabis`, `ppitay`, `qqiri` — and the gloss test refused two of the nine.

Two generator facts, both learned by breaking something:

- A manual entry whose value is its key plus a letter feeds back into the
  consonant-strip rule. `psilin → psiling` produced `mpsiling → empsilingg` *and*
  `psiling → psilingg`. The LOST check caught it (gained 10, **LOST 1**); the fix
  is to pin both shapes. Assume any `X → X+C` entry does this.
- `loan_population.json` is regenerated by `build_modern_map.py`, exactly as
  `name_population.json` is (batch 197). `siba` was hand-added and vanished on the
  next build. **`HAND_LOANS` now exists** for the reason `HAND_NAMES` does. `siba`
  is his own verdict — SIBA "Gazon (terme japonais)" 草坪（日語詞）= 芝生 — written
  into the gloss, which the generator's `tag` test cannot see. Widening that test
  to a gloss regex was measured and rejected: eleven entries say japonais/chinois
  in a gloss and only this one is a borrowing; the rest are `QOLIT`
  "Cyprès-japonais", `PILA` on the Ami language, `L'QNUX` on the deer.

Two DOM spans left the page (44,945 → 44,943) and both were chased before being
believed: `Kmbui`/`Kmubui` now both spell `kmbuyu`, and his `Kdapan` now spells
the `qdakan` already on the card. His doublets printing once — the map working.

Refused and priced: `rngut`/`rmngut`/`rngutan` 15 (懷孕 is `knshjilan` off `shjil`
重), `btuluk` family 8 (`tlukun` and `pntlukan` are dark and both lack his b- —
"Pntlukan (Pnbtlukan ?)" is his own open question), `klulu` 7 (葡萄 is `tlulug`;
k~t is not one of the three char rules), `naru` 8 (the batch-114 pin stands),
`msnoxel` 5 (嫉妒 is `hkrig`), `rih` 6, `srhq*` 5, `lngiyan`/`pslangi` 3.

## Batch 200 — his own parenthetical, and the pair ranking

**The percentage was nearly spent; the pair metric was not.** After batch 199
closed at 99.0010%, ~65 of the 415 remaining pale occurrences were already priced
and refused in writing, and the three permanent classes covered much of the rest.
So this batch worked the metric CLAUDE.md actually names — deliverable sentence
pairs — and ranked by **sole blockers**: one pale word holding a whole example
hostage. 227 pairs were blocked, 216 of them by a single type.

**Result: 5,208 → 5,242 pairs, 95.82% → 96.45%.** Brown 99.0010% → 99.0875%.
Pale 415 → 376 occurrences, 294 → 263 distinct. Blocked pairs 227 → 193.

### The instrument: he already told us they are one word

Four of the first slice's rulings had the same shape, and it generalises. In
running text he writes `X (Y ?)`, `X (vl. Y)`, `X (Y)` — naming two spellings of
one word — and the map sends them to two different values of which **exactly one
is dark**. That is not a spelling question. He has testified they are the same
word, so the pale one should render whatever the dark one renders.

`vari200.py` sweeps for it. It found 17 pairs and **ruled 10**:

    dbsnawan -> dsbnawan   m'gwi -> gmeeguy    mnttlaqel -> mntraqil
    ntnling  -> mtnring    n'gk'laan -> nklaan snkiila   -> snkila
    tx'ldo   -> thdu       tbskan -> tpskan    pnbtlukan -> pntlukan
    bntuluk  -> pntuluk

Gloss-confirmed where the register has one: `nklaan` 上升處 on his KALA 上升,
`snkila` 喜歡留下;習慣 on his SKILA 覺得自在, `gmeeguy` 偷竊 on his 你偷竊,
`pskan` 咀嚼 on his PSKAN 咀嚼, `mhdu` 完成 on his XDO 完成－結束.

**It rules nothing on its own, and that is the point.** Seven of the seventeen
were refused because the DARK side is dark on a homograph — `pgagu` is glossed
笛子 and his card is 鴿子; `nguy` is 哭聲 and his sentence is 偷竊; `gmluq` is
做黏貼 and his G'LUK is 從中拉出. Following the parenthetical there would spread a
freeze, not settle a word. All seven are in `refused.txt`, three flagged as
suspect darks for a future batch.

### Two generator bugs, found by measuring rather than by reading

1. **`l→r` fired inside `pusal`.** `empusal` 二十 is listed with its `l`, and
   `spusalan` was hand-ruled with its `l` in batch 199 — but `snpsalan` and
   `snpsalun` came out `snpsaran`/`snpsarun`. The sibling was dark and the
   syncopated form was pale, for no reason but the char rule. Pinned as identity
   entries, which is the one thing an identity entry is *for*: it blocks
   `charRules()` where the rule is wrong. A sweep for `sal`-keys with `sar`-values
   found exactly these two and one true positive (`sali` → `sari` 芋頭).
2. **`npgxei` → `npghii`, alone.** `xei` → `hiyi`, `mgxei` → `mghiyi` (glossed
   結果實, exactly his sentence 稻子結果), `pgxei` → `pghiyi` — all dark. One token
   slipped to `hii`. Sized the seam before fixing it: **one token**, not a class.

### What his own book settles that no register can

- **`nilit` is `milit`.** Two sentences say 羊奶 and the register's 山羊 is
  `mirit`; the n/m looked like an override. Then: he writes **`milit` 15 times**
  elsewhere in the book and `nilit` twice, and `milit → mirit` is already dark.
  His own text spells the goat. Search the book, not only the register.
- **`dbsnawan` is an ethnonym**, proved by a sentence on a different card:
  `dSbnawan ni dTroko` 阿尼人與太魯閣人. `dtroko → dtruku` is dark and `dsbnawan`
  (his other spelling, with the S) was **already dark**. His own doublet.
- **`handulu` is a Japanese loan he glossed himself** — `xandolu (=Volant)`
  方向盤, ハンドル. Into `HAND_LOANS`, because the tagger reads `tag` and this
  verdict is in a gloss. Second instance of the batch-199 rule.
- **`mkefunang`, `ddcristu`, `put`** are the exact parallels of `mkmurisaka`,
  `dcristu`, `aput` — all three already in `HAND_NAMES`. `Put!` is the clipped
  vocative of the name Aput ("我可憐的小 Aputs").

### The gloss test kept earning its place

`damat`'s only gloss row is **恢復原狀**, which would have refused `pdmati`. The
family overrules the row: `dmatan` 用…配菜, `dmatun` 要用…做菜餚, `dmaci` 要配菜吃,
`dmamat` 配菜, `ddamat` 要吃的菜餚 — his DAMAT card is 菜餚——佐料 and the card is
unanimous. **A single gloss row is not the register's answer; the family is.**

Conversely `empaa-` turned out fully productive (`empaadxgal` 會變成塵土,
`empaababuy` 變成豬 — 12+ forms) and `npaabuqa` exists, so `empaamalu`/`npaamalu`
off `maamalu` 變好 are regular, not inventions. His three sentences say 好看,
痊癒, 舒服些.

### Doublet collapse, again — 11 spans

Total DOM spans 44,943 → 44,932. Every one is his own `X (Y)` now printing one
word, plus `bnlaxan`/`bnlnaxan` and `s'xiga`/`s'iga`. Chased, not assumed.

### Closing

dark 43,832 / 5,956 distinct · class 690 / 268 · pale 376 / 263 · green 34 / 25
total 44,932 · **brown 99.0875%** · deliverable pairs **5,242 / 5,435 = 96.45%**
Suites: loose179 16/16, cite179 9/9, nav178 28/28, dom171 0 failures.

## batch 201 — every blocker tier closed, and seven words dark on the wrong meaning

**5,242 → 5,305 deliverable pairs (96.45% → 97.61%). Blocked 193 → 130.**
13 net manual_map entries, 81 refusals written, one pin lifted, one class added.

The batch worked the SOLE-blocker ranking batch 200 built, then the tier behind
it. Both are now closed: a filtered re-rank reported **sole blockers total 95,
open 0**, and the 2-blocker tier — 10 clusters, no recurring word pair — is ruled
or refused item by item. What still blocks 130 pairs is held by words with a
written refusal. The next gain needs new evidence, not a new ranking.

### Seven homograph freezes — dark, and wrong

The batch's real finding. A homograph freeze is a raw token mapped onto a
same-shaped modern word with an unrelated gloss: the span renders dark, every
colour metric counts it as settled, and it says the wrong thing. No attestation
test can see one. Only the gloss test can.

- `lungut` → `rungut` 冰雹 — his card is 懷孕. Blocked by an identity pin.
- `psttui` → root `ttui` 切、剁 — his card is 起身. Ruled to `pstutuy`.
- `koyoç` → `kuyuh` 女人 — his card is **雨**. The rain family, below.
- `q'löt` → `qrut`, `mmalox` → `mmlux`, and the bare `mu` — three earlier in the
  batch, each on the same instrument.

The rule that finds them is the one already written: **run the gloss test on the
word you are leaning on, before you write the value.**

### The rain family, and the letter that was doing all the work

`koyoç` 雨 → `quyux` should have been a five-key sweep: `npkoyoç`, `knkmoyoç`,
`nkmoyoç` follow the head. The gained/LOST check came back
`LOST ['empakuyuh', 'npkuyuh']` — one of those was the freeze coming off, the
other was a **different card breaking**. He writes KOYOX 女人—妻子—雌性 with `x`
and KOYOç 雨 with `ç`, and § Mpakoyox so ka yako 即使你說不，你也一定會成為我的妻子
belongs to the first. `koyox → quyux` was removed; only the ç-side kept.
`plain()` strips the diacritic downstream, which is exactly why a sweep keyed on
shape crosses two cards. **Assert gained/LOST on every sweep** — nothing else
caught this.

### Three char-rule contradictions inside one root

`mp'yax` → `mpyah` sat beside a dark `iyax`; `upsk'la` → `upskra` beside a dark
`skla` (`empskla` 會趕上 is listed with his own sentence for a gloss); and the
DLUT crossing from batch 171. In each, `l→r` or `x→h` fired on one slot of a card
whose other slots keep the letter. That is the fallback overreaching, not a
variant — check the siblings before believing it.

### Onomatopoeia becomes the third settled class

"names, onomatopoeia, and Japanese loans: i vote for making them dark brown."
`HAND_ONOM` added to `inflection.py` and plumbed through `build_verified.py`
alongside `HAND_NAMES`/`HAND_LOANS` — same code **16**, same additive `w-cls`.
First member is `paaaq`, the noise a felled tree makes, read off his own gloss.
Attestation is not a test a noise can fail; it is one it cannot sit.

### A pin lifted, on the instrument that set the precedent

`ndiyan` was refused in batch 196 on the grounds that colouring it would claim a
spelling for his Djian. This batch ruled `dmikat`/`nmikat` on the identical
instrument — the prefixed slot is ruled because the bare name under it is ruled —
and `ndiyan → ndiyan` claims only that the n-possessive of a capitalised name is
not a word any register lists. Landing it took a second edit: the build log said
`curated keys that never landed [BLOCKED]: 1`, because `lexical_map.json` carried
a null for it and a null outranks manual by design. **The pin came down with the
refusal it enforced.** `ddliwis` closed the same family: `liwis` was already a
hand-ruled name, and his own Chinese reads ddLiwis as Liwis 的朋友們.

### French in a Truku field, and five pairs that were never pairs

"if it's in french it should not be in our statistics." Six example rows have a
Truku field **identical to their French one** — his AN (3) card demonstrates the
circumfix that way, and `Paro = Grand; Knplaan = Grandeur` is the same string in
both. The test `t == fr` modulo punctuation finds **exactly those six** across
5,437 examples, with zero near misses, because no real sentence equals its own
translation.

Two things were wrong. The map was painting French words brown — *Grandeur*,
*Connaissance*, *Rougeur*, *"matinalité"* — and **five of the six were counted
DELIVERABLE**, French lines scoring as Truku pairs. Only one of them was in the
blocked list, which is why the batch had priced this as two blocked pairs; it was
one, and the real cost was five phantom pairs on the other side of the ledger.

`metaLine()` in `app.js` now renders them with no spans at all: no map, no links,
as the book prints them. All three example call sites are guarded (the assertion
caught a fourth site on the first attempt and refused to write). The metric reads
the DOM, so dropping the spans drops them from the denominator by the same act —
one implementation, nothing to drift. **5,435 → 5,429.**

### What the 2-blocker tier refused

`thiy`+`snuk` (XNUK 這木頭很軟，釘子釘不牢 — 釘子 is `samu`, a lexical substitution),
`pdaqi`+`pstui` (SPONG, the Lord's Prayer petition — 試探 and 拯救 return **0**
register rows), `tbasyaq`, `nrikut`+`krikut`, `dmtsapat`+`dmtbasyaq`. And two
pairs that are not spelling questions at all: his AN card's `Paru = Grand` /
`Knplaan = Grandeur` is French metalinguistic text sitting inside a Truku field.
The denominator no longer keeps it — see above.

`pstui` is worth one line on its own: it is shape-identical to the `psttui` this
batch ruled to `pstutuy` 起身, and it is a different word. **Decide slot by slot.**

### One test failed, and the test was wrong

`loose179` asserted BUYO's fifth sub-form renders `Kmubui (kmbui?)`. Both
spellings now map to `kmbuyu`, so `collapsed()` correctly drops a bracket that
would read "Kmbuyu (kmbuyu?)". The ORDER that test guards — principle 1 — is
unchanged; only the rendering of slot 5 moved. Expectation updated with the
reason.

### Closing

dark 43,884 / 6,001 distinct · class 705 / 282 · pale 299 / 195 · green 28 / 20
total 44,916 · **brown 99.2720%** · deliverable pairs **5,300 / 5,429 = 97.62%**
Suites: loose179 16/16, cite179 9/9, nav178 28/28, dom171 0 failures, 0 page errors.
