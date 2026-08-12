# -*- coding: utf-8 -*-
"""The regression suite: run every DOM log, then adjudicate what it reports.

Each `logs/dom*.py` is a batch's own measurement, frozen at the moment it was
written. Run them again a year later and some will fail, because the project
moved: a word the batch held pale is dark now, a spelling it asserted has been
overturned, a card it counted has more pages behind it. **A failure is not a
regression until something says which.** Before this file there was nothing that
said, and the last sweep to claim zero failures had run against a `verified.js`
that predated class colouring — 181 real failures, reported as none.

So the logs are never edited. They are the record of what a batch measured, and
editing one to make it pass would destroy the only evidence that anything moved.
The supersession goes here instead, keyed on the exact failure line, and it
carries the batch that overturned the pin:

    ('dom150.py', 'PIN kpaux: want 3 pale'): ('dark', '', 'batch 182, code 1')

Seven kinds, and each one re-asserts something rather than merely excusing it:

  dark     the pin wanted pale; the word is dark now and `verified.js` has a code
           for it. Re-checked: it must still be dark, and dark alone.
  dark>=N  the pin wanted a count as well as a colour, and the count rose because
           the book grew behind it. Colour re-checked, floor re-checked.
  absent   the modern string the pin named is nowhere on the page, because a
           later batch respelled the raw token. Re-checked: still absent.
  map      an old-style log asserting `token -> spelling`; the token maps
           somewhere else now. Re-checked against `modern_map.js`, so a drift to
           a THIRD spelling nobody argued for still fails here.
  meta     the map claim is intact and the SPAN is gone: batch 207 stopped
           painting the six rows whose Truku field is its own French translation,
           which is all of the AN (3) circumfix card. Re-checked both ways — the
           map value must be unchanged AND the row must still test as
           metalinguistic in `entries.js`.
  floor    the metric FELL below a log's pin. Batch 218 spent three pairs
           reverting a homograph freeze, which no colour metric can score as
           anything but a loss. Re-checked both ways: not fallen further, and
           the ruling the pairs were spent on still in the map.
  ruled    a log's written REFUSAL, overturned by a later ruling. Re-checked
           against both tables — the map must still say what overturned it, and
           the value must still be verified, since a value that goes pale puts
           the refusal back in force without anyone deciding to.

**A failure kind with no entry here does not get adjudicated at all — it exits
rc=1 with a line `failures()` cannot see, and the suite calls the log CRASHED.**
That has happened twice: the floor in batch 218, and in batch 219 the prose
`FAIL <word> ... It was refused because ...` line that dom214/216/217 write. Four
real failures hid behind the second for a batch, three of them overrides of
those same logs' written refusals. When a log crashes, read its output before
assuming the log is broken.

An unexplained failure is a regression and is printed. A ledger row whose failure
line has stopped appearing is printed too, under HEALED: a pin that came back is
as much news as a pin that broke, and it is the only thing standing between this
file and a list of excuses that grows forever.

    python tools/orthography/suite.py            # all of them, 4 at a time
    python tools/orthography/suite.py dom16      # just the ones matching

Needs the site served at 127.0.0.1:8765.
"""
import concurrent.futures as cf
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOGS = os.path.join(HERE, "logs")

# Every pin a later batch overturned, with the batch that did it.
LEDGER = {
    # --- dom57.py
    ('dom57.py', 'BROWN dup dup missing on [DUP]'):
        ('map', 'eduk', 'batch 172 respelled it'),
    ('dom57.py', "BROWN dup dup missing on [L'PAN]"):
        ('map', 'eduk', 'batch 172 respelled it'),
    ('dom57.py', 'BROWN mgangax mgangah missing on [NGANGAX]'):
        ('map', 'mngangah', 'batch 201 respelled it'),
    ('dom57.py', "BROWN mpn'mu empnmu missing on [QBOBOL]"):
        ('map', 'empneemu', 'batch 201 respelled it'),
    ('dom57.py', "BROWN gn'lyeq gneeliq missing on [S'LYEQ]"):
        ('map', 'gnaliq', 'batch 201 respelled it'),
    ('dom57.py', 'BROWN psttuy psttuy missing on [TUTWI]'):
        ('map', 'pstutuy', 'batch 201 respelled it'),
    ('dom57.py', 'BROWN mpn\'mu empnmu missing on ["MU]'):
        ('map', 'empneemu', 'batch 201 respelled it'),
    # Batch 213 ruled his whole TQELI paradigm off the stem the wordlist itself
    # writes for it — `sistered('tqriyun')` returns `tqrian` and `tqrii`, neither
    # of which carries the epenthetic `y` the char rule had supplied. These three
    # rows pin the pre-ruling values, so the failure IS the ruling landing.
    ('dom57.py', 'BROWN ptqliyun ptqliyun missing on [TQELI]'):
        ('map', 'ptqriun', 'batch 213 ruled the TQELI paradigm'),
    # Batch 218 overturned an AGED identity pin. `pslangi -> pslangi` was the
    # verdict "no modern form found", written when nothing on the SLANGI card
    # was dark; `srangi`, `msrangi` and `psrngiyan` are dark now, and the
    # register's `psrngiun` 留一些 carries his 使之有剩餘.
    ('dom57.py', 'BROWN pslangi pslangi missing on [SLANGI]'):
        ('map', 'psrangi', 'batch 218 overturned the aged pin'),
    # Batch 220 finished the same card. The `-rngiy-` shape these two rows pin
    # was never evidence — batch 215 wrote it in as a stated consistency fix,
    # "pale before, pale after — a consistency fix, not a claim". The register
    # spells this root's syncopated stem in exactly four forms and not one
    # carries a `y`: `psrngiun` 留一些, `psrngion`, `rngii`, `rngiun`. So the
    # tie-break is retired by attestation, and it is retired in both slots at
    # once — `srngiun` bought the pair, `psrngiun` (LISTED, code 1) replaced an
    # inference and bought nothing but coherence.
    ('dom57.py', 'BROWN slngiyun srngiyun missing on [SLANGI]'):
        ('map', 'srngiun', 'batch 220 ruled it off the register'),
    ('dom57.py', 'BROWN pslngiyun psrngiyun missing on [SLANGI]'):
        ('map', 'psrngiun', 'batch 220 ruled it off the register'),
    # [batch 231] His SLIYU example writes `Malu kasayang da` joined and its own
    # second clause writes `ka xedao` split. `b57.py:127` pinned the join to his
    # own letters -- a tier-M identity pin, which batch 216 names as the one map
    # entry that ages. The outside voice retires it: `ka sayang` is 403x in the
    # ILRDF parquets and the join 0x, fifteen of them in his own frame. The
    # failure IS the ruling landing. Kind `map` re-reads modern_map.js, so a
    # drift to a third spelling still fails; the darkness assertion, and the
    # assertion that BOTH halves are verified, live in dom231.py.
    ('dom57.py', 'BROWN kasayang kasayang missing on [SLIYU]'):
        ('map', 'ka sayang', 'batch 231 split his typewriter join'),
    ('dom63.py', 'BROWN kasayang kasayang missing on [SLIYU]'):
        ('map', 'ka sayang', 'batch 231 split his typewriter join'),
    ('dom67.py', 'BROWN kasayang kasayang missing on [SLIYU]'):
        ('map', 'ka sayang', 'batch 231 split his typewriter join'),
    # Batch 230 ruled his SNOXEL card onto the register's OTHER jealousy root.
    # These logs pinned the identity freeze b57.py:120 wrote when `charRules`
    # printed "SNUHER" beside brown siblings and it looked like a fake word. It
    # is two edits from the listed `sneuhir` 忌妒;吃味;容不下人, the gap being the
    # epenthetic schwa the char rules cannot supply. The failure IS the ruling
    # landing; the darkness assertion lives in dom230.py.
    ('dom57.py', 'BROWN snoxel snoxel missing on [SNOXEL]'):
        ('map', 'sneuhir', 'batch 230 ruled the uhir jealousy root'),
    ('dom57.py', 'BROWN msnoxel msnoxel missing on [SNOXEL]'):
        ('map', 'msneuhir', 'batch 230 ruled the uhir jealousy root'),
    # --- dom58.py
    ('dom58.py', 'BROWN m\'mu mmu missing on ["MU]'):
        ('map', 'meemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN n\'mu nmu missing on ["MU]'):
        ('map', 'neemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN nn\'mu nnmu missing on ["MU]'):
        ('map', 'nneemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN pn\'mu pnmu missing on ["MU]'):
        ('map', 'pneemu', 'batch 201 respelled it'),
    # Batch 229 reverted a homograph freeze and ruled the identity beside it.
    # `n'gui -> nguy` painted his 偷 card with 哭聲 — dark AND wrong, which the
    # colour metric scores as a win, so only an assertion keeps it out. `nagui`
    # was the pre-ruling identity claim on the same SLAP example. Both now go to
    # `gneeguy` 偷了, which carries his gloss. The failure IS the ruling landing.
    ('dom58.py', "BROWN n'gui nguy missing on [SLAP]"):
        ('map', 'gneeguy', 'batch 229 reverted the nguy freeze'),
    ('dom58.py', 'BROWN nagui nagui missing on [SLAP]'):
        ('map', 'gneeguy', 'batch 229 ruled the identity beside it'),
    # [batch 239] dom58 is one of the git-relative HOLD logs (`git show
    # HEAD:site/modern_map.js`, batch 230), so it holds `bsqan` at the value it
    # had before batch 238 ruled it. The failure IS that ruling landing, and the
    # row is kind `map` rather than absorbed: it re-reads modern_map.js, so a
    # drift to a third spelling still fails. Batch 238 added the dom165 row for
    # the same ruling and missed this one — the two logs assert it from
    # different sides, and only one had a ledger entry.
    ('dom58.py', 'BROWN bsqan bsekan missing on ["QAN]'):
        ('map', 'pskan', 'batch 238 ruled his parenthetical to the dark side'),
    # --- dom59.py
    ('dom59.py', 'BROWN tqliyun tqriyun missing on [QELI]'):
        ('map', 'tqriun', 'batch 213 ruled the TQELI paradigm'),
    # --- dom63.py
    # He carded LIDIL twice, and `rijil` is the BEND root (`mrijil` 使彎曲). The
    # handle root is `rijig` 柄（刀;鋤）, glossed 柄 right through its family. These
    # two logs pinned the freeze, so the failure IS the fix landing.
    ('dom63.py', "BROWN lidil rijil missing on [L'BU]"):
        ('map', 'rijig', 'batch 211 split the LIDIL homograph'),
    # Batch 214: two identity claims fell. `snola -> snola` blocked charRules()
    # beside five dark `-eura` slots on his own SOLA card; `kmbyanan` is his own
    # `Knbyanan` one line up on page 92, three stems against two. Both pinned
    # rows recorded the pre-ruling value, so the failure IS the ruling landing.
    ('dom63.py', 'BROWN kmbyanan kmbyanan missing on [GBIYAN]'):
        ('map', 'knegbiyan', 'batch 214 ruled the GBIYAN example'),
    ('dom63.py', 'BROWN snola snola missing on [LUUS]'):
        ('map', 'sneura', 'batch 214 ruled snola off the SEURA family'),
    # Batch 215 retired a pin two batches had set. dom146 and dom162 each froze
    # `rih` as SIX PALE renders, and both named the same blocker: length-as-
    # chance over one ASR hapax plus `krih`, an onomatopoeion. What retired it is
    # the reduplicated paradigm `inf.roots()` cannot see -- `ririh` 取代 14,
    # `mririh` 取代者 35, `pririh` 還 17, `rrihan` 被取代 4, `empririh` 賠償 4 --
    # with five of his own LILEX forms already dark on five of them. So the
    # failure IS the ruling landing, and the supersession re-asserts it as a
    # FLOOR: six or more, every one of them dark. A drift of `lex` to some third
    # spelling is caught in dom215.py, which reads the map directly.
    ('dom146.py', 'PIN rih: want 6 pale'):
        ('dark>=6', 'rih', 'batch 215 ruled rih off the reduplicated paradigm'),
    # --- dom162.py
    ('dom162.py', 'PIN rih: want 6 pale'):
        ('dark>=6', 'rih', 'batch 215 ruled rih off the reduplicated paradigm'),
    # --- dom65.py
    ('dom65.py', 'BROWN tqliyun tqriyun missing on [QELI]'):
        ('map', 'tqriun', 'batch 213 ruled the TQELI paradigm'),
    # Batch 218 reverted a TIER-B freeze: `mqlaq` 發癢 had been awarded `mqraq`
    # 抓 by the one tier that needs no gloss proof. Zero of the 43 register
    # words glossing 癢 are q-initial; the modern itch root is krak/ghguh. The
    # identity pin is load-bearing — charRules('mqlaq') spells mqraq on its own.
    ('dom65.py', 'BROWN mqlaq mqraq missing on [QLAQ]'):
        ('map', 'mqlaq', 'batch 218 reverted the mqlaq freeze'),
    # Batch 230. His SPUNG example spells the causative `pstui` once against
    # `pstutwi` 6× (batch 213's hapax test), and three sibling spellings were
    # already pinned to `pstutuy` 使扶起身. This is the fourth.
    ('dom63.py', 'BROWN pstui pstui missing on [SPONG]'):
        ('map', 'pstutuy', 'batch 230 ruled the fourth spelling to the register'),
    # --- dom66.py
    # Batch 230, the same SNOXEL ruling reaching his TAKOL example.
    ('dom66.py', 'BROWN msnoxel msnoxel missing on [TAKOL]'):
        ('map', 'msneuhir', 'batch 230 ruled the uhir jealousy root'),
    ('dom66.py', "BROWN lidil rijil missing on [L'BU]"):
        ('map', 'rijig', 'batch 211 split the LIDIL homograph'),
    ('dom66.py', 'BROWN kmbyanan kmbyanan missing on [GBIYAN]'):
        ('map', 'knegbiyan', 'batch 214 ruled the GBIYAN example'),
    ('dom66.py', "BROWN ml'bu mgrbu missing on [AN]"):
        ('meta', 'mgrbu', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN grand grand missing on [AN]'):
        ('meta', 'grand', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN grandeur grandeur missing on [AN]'):
        ('meta', 'grandeur', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN knbnaxan knbnahan missing on [AN]'):
        ('meta', 'knbnahan', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN kndusan kndsan missing on [AN]'):
        ('meta', 'kndsan', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN knklaan kngkla missing on [AN]'):
        ('meta', 'kngkla', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN knlbuan knlbuan missing on [AN]'):
        ('meta', 'knlbuan', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN knmlaan knmalu missing on [AN]'):
        ('meta', 'knmalu', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN knplaan knpraan missing on [AN]'):
        ('meta', 'knpraan', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN malu malu missing on [AN]'):
        ('meta', 'malu', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN mbanax embanah missing on [AN]'):
        ('meta', 'embanah', "batch 207 — the AN card's rows are French"),
    ('dom66.py', "BROWN mk'la mkla missing on [AN]"):
        ('meta', 'mkla', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN mudus meudus missing on [AN]'):
        ('meta', 'meudus', "batch 207 — the AN card's rows are French"),
    ('dom66.py', 'BROWN paro paru missing on [AN]'):
        ('meta', 'paru', "batch 207 — the AN card's rows are French"),
    # --- dom71.py
    ('dom71.py', 'BROWN qalip qrip missing on [QALIP]'):
        ('map', 'qrib', 'batch 199 respelled it'),
    # --- dom72.py
    ('dom72.py', 'BROWN knmlaan knmalu missing on [AN]'):
        ('meta', 'knmalu', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN grand grand missing on [AN]'):
        ('meta', 'grand', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN grandeur grandeur missing on [AN]'):
        ('meta', 'grandeur', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN knbnaxan knbnahan missing on [AN]'):
        ('meta', 'knbnahan', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN kndusan kndsan missing on [AN]'):
        ('meta', 'kndsan', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN knklaan kngkla missing on [AN]'):
        ('meta', 'kngkla', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN knlbuan knlbuan missing on [AN]'):
        ('meta', 'knlbuan', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN knplaan knpraan missing on [AN]'):
        ('meta', 'knpraan', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN malu malu missing on [AN]'):
        ('meta', 'malu', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN mbanax embanah missing on [AN]'):
        ('meta', 'embanah', "batch 207 — the AN card's rows are French"),
    ('dom72.py', "BROWN mk'la mkla missing on [AN]"):
        ('meta', 'mkla', "batch 207 — the AN card's rows are French"),
    ('dom72.py', "BROWN ml'bu mgrbu missing on [AN]"):
        ('meta', 'mgrbu', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN mudus meudus missing on [AN]'):
        ('meta', 'meudus', "batch 207 — the AN card's rows are French"),
    ('dom72.py', 'BROWN paro paru missing on [AN]'):
        ('meta', 'paru', "batch 207 — the AN card's rows are French"),
    # --- dom138.py
    ('dom138.py', 'KEEP aku: want 1 pale'):
        ('dark', '', 'batch 203, code 16'),
    ('dom138.py', 'KEEP bulu: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP butang: want 3 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP emi: want 1 pale'):
        ('dark', '', 'batch 203, code 16'),
    ('dom138.py', 'KEEP miru: want 1 pale'):
        ('absent', '', 'batch 203 respelled it'),
    ('dom138.py', 'KEEP muli: want 1 pale'):
        ('dark', '', 'batch 196, code 1'),
    ('dom138.py', 'KEEP nuli: want 2 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP sabung: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP satu: want 2 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP sugi: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom138.py', 'KEEP tabu: want 5 pale'):
        ('dark', '', 'batch 196, code 16'),
    # [batch 238] dom138's KEEP holds registered names that are NOT this page's
    # names, to prove the NAME gate refuses them. The gate still does: `tapaq`
    # is in neither `name_population.json` nor `loan_population.json`, and it
    # is code 1 -- LISTED. The darkness is the register's own row arriving
    # through `manual_map.json`, not a name-population leak, which is why this
    # is kind `ruled` (re-asserting the ruling) and not kind `dark`.
    ('dom138.py', 'KEEP tapak: want 1 pale'):
        ('ruled', ('tapak', 'tapaq'),
         'batch 238 — his own （TAPAQ？） and `tpaqi` 要拍手、游泳, the only '
         'register row carrying 拍手 and carrying BOTH his Tmapak example '
         'glosses; retires the "would merge two of his own cards" refusal at '
         'batch-log:5143 / dom218.py:96, since 244 modern headword types '
         'already collide across 520 cards'),
    ('dom138.py', 'KEEP turu: want 1 pale'):
        ('dark', '', 'batch 203, code 16'),
    ('dom138.py', 'JP boro: want 2 pale'):
        ('dark', '', 'batch 201, code 16'),
    ('dom138.py', 'JP mori: want 1 pale'):
        ('dark', '', 'batch 203, code 16'),
    ('dom138.py', 'JP xalo: want 1 pale'):
        ('dark', '', 'batch 203, code 16'),
    # --- dom141.py
    ('dom141.py', 'PIN mrbuq: want 2 pale'):
        ('dark', '', 'batch 192, code 1'),
    # --- dom142.py
    ('dom142.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom142.py', 'STOPPED pngraq: want 3 pale'):
        ('dark', '', 'batch 190, code 1'),
    # --- dom144.py
    ('dom144.py', 'PIN byeqay: want 2 pale'):
        ('absent', '', 'batch 201 respelled it'),
    ('dom144.py', 'PIN grand: want 1 pale'):
        ('absent', '', 'Hear the language spoken: four new tiers, and stop renaming pe respelled it'),
    ('dom144.py', 'PIN grandeur: want 1 pale'):
        ('absent', '', 'Hear the language spoken: four new tiers, and stop renaming pe respelled it'),
    ('dom144.py', 'PIN mnttlaqel: want 1 pale'):
        ('absent', '', 'batch 200 respelled it'),
    ('dom144.py', 'PIN mpa: want 4 pale'):
        ('absent', '', 'batch 203 respelled it'),
    ('dom144.py', 'PIN mpsqlul: want 1 pale'):
        ('absent', '', 'batch 199 respelled it'),
    ('dom144.py', 'PIN pnsdahung: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom144.py', 'PIN tsaleh: want 1 pale'):
        ('absent', '', 'batch 201 respelled it'),
    ('dom144.py', 'PIN yiyah: want 1 pale'):
        ('absent', '', 'batch 201 respelled it'),
    # --- dom145.py
    ('dom145.py', 'GAIN psttui: want 1 dark'):
        ('absent', '', 'batch 201 respelled it'),
    # Batch 218 took his QALIT card off the 溢滿 root. These two pinned the
    # n-infix slots on the OLD value, so their absence IS the ruling landing —
    # `qalit` was tier A, gloss-PROVED, and had scored 3 against `qlit` on the
    # substring 的詞根, which is apparatus and not meaning.
    ('dom145.py', 'GAIN qnlit: want 1 dark'):
        ('absent', '', 'batch 218 ruled the QALIT card onto qrib'),
    ('dom145.py', 'GAIN mnqlit: want 1 dark'):
        ('absent', '', 'batch 218 ruled the QALIT card onto qrib'),
    ('dom145.py', 'PIN drnai: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom145.py', 'PIN ggitan: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom145.py', 'PIN mtgtmaq: want 1 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom145.py', 'PIN slungan: want 2 pale'):
        ('dark', '', 'batch 194, code 1'),
    # --- dom146.py
    ('dom146.py', 'GAIN niq: want 4 dark'):
        ('dark>=4', '', 'the book grew after this pin'),
    ('dom146.py', 'GAIN xal: want 9 dark'):
        ('dark>=9', '', 'the book grew after this pin'),
    ('dom146.py', 'GAIN yup: want 2 dark'):
        ('dark>=2', '', 'the book grew after this pin'),
    ('dom146.py', 'PIN dup: want 7 pale'):
        ('absent', '', 'batch 172 respelled it'),
    ('dom146.py', 'PIN klulu: want 7 pale'):
        ('dark', '', 'batch 202, code 16'),
    # --- dom147.py
    ('dom147.py', 'PIN put: want 1 pale'):
        ('dark', '', 'batch 200, code 16'),
    ('dom147.py', 'PIN tgbasi: want 1 pale'):
        ('dark', '', 'batch 177b, code 1'),
    ('dom147.py', 'PIN tgbhgay: want 1 pale'):
        ('dark', '', 'batch 177b, code 1'),
    ('dom147.py', 'PIN tgbilaq: want 2 pale'):
        ('dark', '', 'batch 177b, code 1'),
    # --- dom148.py
    ('dom148.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom148.py', 'PIN kpaux: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom148.py', 'PIN kpauxi: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom148.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom149.py
    ('dom149.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom149.py', 'PIN kpaux: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom149.py', 'PIN kpauxi: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom149.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom150.py
    ('dom150.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom150.py', 'PIN kpaux: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom150.py', 'PIN kpauxi: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom150.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom151.py
    ('dom151.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom151.py', 'PIN kpaux: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom151.py', 'PIN kpauxi: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom151.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom152.py
    ('dom152.py', 'PIN knslaan: want 2 pale'):
        ('dark', '', 'batch 191, code 1'),
    ('dom152.py', 'PIN kpaux: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom152.py', 'PIN kpauxi: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom152.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom152.py', 'COINCIDENCE emppungu: want 1 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom152.py', 'COINCIDENCE ppungu: want 2 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom152.py', 'COINCIDENCE ptaril: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom152.py', 'COINCIDENCE ssiyang: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom153.py
    ('dom153.py', 'PALE psiisan: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom153.py', 'PALE psiisi: want 1 pale'):
        ('dark', '', 'batch 182, code 4'),
    ('dom153.py', 'PALE psiisun: want 2 pale'):
        ('dark', '', 'batch 182, code 4'),
    # --- dom154.py
    ('dom154.py', 'COINCIDENCE emppungu: want 1 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom154.py', 'COINCIDENCE ppungu: want 2 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom154.py', 'COINCIDENCE ptaril: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom154.py', 'COINCIDENCE ssiyang: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom154.py', 'PIN mhmadan: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom155.py
    ('dom155.py', 'PIN pqapah: want 1 pale'):
        ('dark', '', 'batch 198, code 1'),
    # --- dom157.py
    ('dom157.py', 'COINCIDENCE emppungu: want 1 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom157.py', 'COINCIDENCE ppungu: want 2 pale'):
        ('dark', '', 'batch 186, code 2'),
    ('dom157.py', 'COINCIDENCE ptaril: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom157.py', 'COINCIDENCE ssiyang: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom158.py
    ('dom158.py', 'PIN dup: want 7 pale'):
        ('absent', '', 'batch 172 respelled it'),
    ('dom158.py', 'KEEP eduk: want 7 dark'):
        ('dark>=7', '', 'the book grew after this pin'),
    # --- dom159.py
    ('dom159.py', 'FRAME ita: want 37 dark'):
        ('dark>=37', '', 'the book grew after this pin'),
    # --- dom160.py
    ('dom160.py', 'PIN nasu: want 1 pale'):
        ('absent', '', 'batch 196 respelled it'),
    ('dom160.py', 'PIN psilin: want 1 pale'):
        ('absent', '', 'batch 199 respelled it'),
    ('dom160.py', 'PIN tabu: want 5 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom160.py', 'PIN tksaw: want 5 pale'):
        ('dark', '', 'batch 182, code 1'),
    ('dom160.py', 'KEPT psiling: want 3 dark'):
        ('dark>=3', '', 'the book grew after this pin'),
    # --- dom161.py
    ('dom161.py', 'PIN mnalu: want 5 pale'):
        ('dark', '', 'batch 185, code 1'),
    ('dom161.py', 'PIN nngangah: want 2 pale'):
        ('dark', '', 'batch 198, code 1'),
    ('dom161.py', 'PIN snkrawah: want 5 pale'):
        ('dark', '', 'batch 184, code 1'),
    ('dom161.py', 'PIN tnaga: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom163.py
    ('dom163.py', 'AMBIGUOUS empsneanak: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom163.py', 'AMBIGUOUS gmnaliq: want 1 pale'):
        ('dark', '', 'batch 198, code 1'),
    ('dom163.py', 'AMBIGUOUS kmkmalu: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom163.py', 'AMBIGUOUS kngusan: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom163.py', 'AMBIGUOUS knkmuyuh: want 1 pale'):
        ('absent', '', 'batch 201 respelled it'),
    ('dom163.py', 'AMBIGUOUS nkmuyuh: want 1 pale'):
        ('absent', '', 'batch 201 respelled it'),
    ('dom163.py', 'AMBIGUOUS ppdsun: want 1 pale'):
        ('dark', '', 'batch 180, code 1'),
    ('dom163.py', 'AMBIGUOUS psmkun: want 1 pale'):
        ('dark', '', 'batch 196, code 1'),
    ('dom163.py', 'AMBIGUOUS ptbnuun: want 2 pale'):
        ('absent', '', 'batch 194 respelled it'),
    ('dom163.py', 'AMBIGUOUS stmaqun: want 2 pale'):
        ('dark', '', 'batch 196, code 1'),
    ('dom163.py', 'PIN psnluun: want 1 pale'):
        ('absent', '', 'batch 196 respelled it'),
    ('dom163.py', 'PIN sbuwai: want 1 pale'):
        ('absent', '', 'batch 196 respelled it'),
    ('dom163.py', 'PIN shnkan: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom163.py', 'PIN snpsaran: want 2 pale'):
        ('absent', '', 'batch 200 respelled it'),
    ('dom163.py', 'PIN snpsarun: want 1 pale'):
        ('absent', '', 'batch 200 respelled it'),
    ('dom163.py', 'PIN tmukan: want 1 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom164.py
    ('dom164.py', 'PIN empkduriq: want 1 pale'):
        ('dark', '', 'batch 201, code 1'),
    ('dom164.py', 'PIN empnalu: want 1 pale'):
        ('dark', '', 'batch 199, code 1'),
    ('dom164.py', 'PIN ggitan: want 1 pale'):
        ('dark', '', 'batch 195, code 1'),
    ('dom164.py', 'PIN mtgtmaq: want 1 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom164.py', 'PIN mtkkrang: want 1 pale'):
        ('dark', '', 'batch 201, code 1'),
    ('dom164.py', 'PIN ntnring: want 1 pale'):
        ('absent', '', 'batch 200 respelled it'),
    ('dom164.py', 'PIN smhngi: want 1 pale'):
        ('dark', '', 'batch 197, code 1'),
    ('dom164.py', 'PIN spsdharun: want 1 pale'):
        ('dark', '', 'batch 201, code 1'),
    ('dom164.py', 'PIN stmaqun: want 2 pale'):
        ('dark', '', 'batch 196, code 1'),
    ('dom164.py', 'PIN tmukan: want 1 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom164.py', 'PIN tnaga: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom165.py
    # [batch 238] dom165's PIN_SYNONYM refused `bsekan` because his 參見 PSKAN
    # is a see-also and there is no affix relation between the two. That leg
    # stays dead -- the ruling does not use the cross-reference. It uses his
    # sub-form NAME, `Ps"qan (= Psqan ? = Bsqan ?)`, where the other two
    # spellings render DARK on `pskan` and the pale one is his own
    # parenthetical (batch 200), with the dark side passing the gloss test
    # 咀嚼 as batch 200 requires. `bsekan` has stopped being a map value.
    ('dom165.py', 'PIN bsekan: want 1 pale'):
        ('ruled', ('bsqan', 'pskan'),
         'batch 238 — his parenthetical, plus the two b/p pins already on this '
         'stem (`tbskan → tpskan`, `bsqani → pskani`) and his own prose '
         '這個詞很常被發成 BSKANUN！'),
    ('dom165.py', 'PIN dup: want 7 pale'):
        ('absent', '', 'batch 172 respelled it'),
    ('dom165.py', 'PIN empsibus: want 1 pale'):
        ('dark', '', 'batch 198, code 1'),
    ('dom165.py', 'PIN kiima: want 2 pale'):
        ('dark', '', 'batch 198, code 1'),
    ('dom165.py', 'PIN mnalu: want 5 pale'):
        ('dark', '', 'batch 185, code 1'),
    ('dom165.py', 'PIN msilung: want 2 pale'):
        ('dark', '', 'batch 194, code 1'),
    ('dom165.py', 'PIN pauxun: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom165.py', 'PIN psiisan: want 3 pale'):
        ('dark', '', 'batch 182, code 2'),
    ('dom165.py', 'PIN psiisi: want 1 pale'):
        ('dark', '', 'batch 182, code 4'),
    ('dom165.py', 'PIN psiisun: want 2 pale'):
        ('dark', '', 'batch 182, code 4'),
    ('dom165.py', 'PIN qnbsranan: want 2 pale'):
        ('dark', '', 'batch 189, code 11'),
    ('dom165.py', 'PIN qtaqi: want 2 pale'):
        ('dark', '', 'batch 199, code 1'),
    ('dom165.py', 'PIN smhngi: want 1 pale'):
        ('dark', '', 'batch 197, code 1'),
    ('dom165.py', 'PIN snulu: want 1 pale'):
        ('absent', '', 'batch 206 respelled it'),
    ('dom165.py', 'PIN stmaqun: want 2 pale'):
        ('dark', '', 'batch 196, code 1'),
    ('dom165.py', 'PIN tbowyak: want 1 pale'):
        ('dark', '', 'batch 198, code 1'),
    ('dom165.py', 'PIN tnaga: want 2 pale'):
        ('dark', '', 'batch 182, code 2'),
    # --- dom166.py
    ('dom166.py', 'GAIN salu: want 10 dark'):
        ('dark>=10', '', 'the book grew after this pin'),
    # Not the book growing this time: batch 229 ruled `sml'lu -> smalu` off his
    # own parenthetical `Sm"lu (sml'lu)`, so a 17th span went dark. A floor, as
    # every count pin is — a FALL below 16 is the news (batch 209).
    ('dom166.py', 'GAIN smalu: want 16 dark'):
        ('dark>=16', '', "batch 229 ruled sml'lu onto it"),
    ('dom166.py', 'ROAD elug: want 91 dark'):
        ('dark>=91', '', 'the book grew after this pin'),
    # --- dom167.py
    ('dom167.py', 'REFUSED knsrhagan: want 2 pale'):
        ('dark', '', 'batch 199, code 1'),
    ('dom167.py', 'REFUSED pkagi: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom167.py', 'REFUSED pnslhagan: want 2 pale'):
        ('dark', '', 'batch 183, code 2'),
    # --- dom170.py
    ('dom170.py', 'BLOCKED knsbusan: want 3 pale'):
        ('dark', '', 'batch 190, code 1'),
    ('dom170.py', 'BLOCKED mbusi: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    ('dom170.py', 'BLOCKED snbusi: want 1 pale'):
        ('dark', '', 'batch 196, code 16'),
    # --- the metric floor. The first FALL in the project's history: batch 218
    # spent three pairs reverting a tier-B homograph freeze, `mqlaq` 發癢 ->
    # `mqraq` 抓. A freeze paints dark AND wrong, so no colour metric can see
    # it and removing one can only ever LOOK like a regression. These three
    # rows carry that cost forward; each re-asserts that the metric has not
    # fallen FURTHER and that the ruling it was spent on is still in the map.
    # [retired batch 219] The metric recovered to 5,330, above all three pins,
    # so dom215/216/217 stopped failing on the floor at all. Reproduced
    # serially before retiring, per batch 217. The mqlaq revert is still in the
    # map; what ended was the DEBT, not the ruling.
    # --- batch 219. Three refusals whose named blocker was a root shape the
    # analyser could not find -- and the ruling that overturned them spells a
    # DIFFERENT stem, so the blocker each one named is simply not the question
    # any more. `trgr`/`tlgl` are empty because the root keeps a final g his own
    # card writes eight times; `pqluy` is empty because the -un slot of an -uli
    # root drops the i (13 of 13 in the register) and the stem is `pqlulun`.
    # Each row re-asserts the ruling itself, so a drift to a third spelling --
    # or a value that stops being verified -- fails here.
    ('dom216.py', 'FAIL mtrgri no longer renders anywhere on the page. It was '
     'refused because tlgl and trgr are both empty in attested_modern.json -- '
     'if the transcription or the map changed, the refusal needs re-arguing, '
     'not deleting.'):
        ('ruled', ('mtlgli', 'mtrgrig'), 'batch 219, code 2 off his G\'LI" card'),
    ('dom216.py', 'FAIL tgrgri no longer renders anywhere on the page. It was '
     'refused because tlgl and trgr are both empty in attested_modern.json -- '
     'if the transcription or the map changed, the refusal needs re-arguing, '
     'not deleting.'):
        ('ruled', ('tglgli', 'tgrgrig'), 'batch 219, code 2 off his G\'LI" card'),
    ('dom216.py', 'FAIL pklluyun no longer renders anywhere on the page. It '
     'was refused because qluy and pqluy are both empty in '
     'attested_modern.json -- if the transcription or the map changed, the '
     'refusal needs re-arguing, not deleting.'):
        ('ruled', ('pklluyun', 'pqlulun'), 'batch 219, tier-A root plus 13/13'),
    ('dom217.py', 'FAIL mtrgri no longer renders anywhere on the page. It was '
     'refused because tlgl and trgr are both empty in attested_modern.json -- '
     'if the transcription or the map changed, the refusal needs re-arguing, '
     'not deleting.'):
        ('ruled', ('mtlgli', 'mtrgrig'), 'batch 219, code 2 off his G\'LI" card'),
    ('dom217.py', 'FAIL tgrgri no longer renders anywhere on the page. It was '
     'refused because tlgl and trgr are both empty in attested_modern.json -- '
     'if the transcription or the map changed, the refusal needs re-arguing, '
     'not deleting.'):
        ('ruled', ('tglgli', 'tgrgrig'), 'batch 219, code 2 off his G\'LI" card'),
    ('dom217.py', 'FAIL pklluyun no longer renders anywhere on the page. It '
     'was refused because qluy and pqluy are both empty in '
     'attested_modern.json -- if the transcription or the map changed, the '
     'refusal needs re-arguing, not deleting.'):
        ('ruled', ('pklluyun', 'pqlulun'), 'batch 219, tier-A root plus 13/13'),
    # --- dom219.py. [batch 231] Its refusal of `isuka` rested on the LOBONG
    # CARD's gloss rather than on the word: the 蓋住 is `Lmobong`, while `isoka`
    # is a pronoun plus a case marker (batch 203 -- a sentence gloss is not the
    # word's gloss). The different-root test was run on the wrong left-hand side
    # and never had a candidate to find. What rules it is his own line, which
    # writes BOTH spellings -- `iso ka (isoka)`, the running text split and the
    # parenthesis joined (batch 200). The value is TWO WORDS, so this handler
    # re-asserts each half as well as the whole string; `attested()` splits on
    # the space. The darkness assertion lives in dom231.py.
    ('dom219.py', 'FAIL isuka no longer renders anywhere. It was refused '
     'because 蓋住 is spuy, 覆蓋 is bbungan; different roots -- if the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('isoka', 'isu ka'), 'batch 231 split his typewriter join'),
    # --- dom60.py. The same G'LI" ruling seen from the map side.
    ('dom60.py', 'BROWN tglgli tgrgri missing on [QALAS]'):
        ('map', 'tgrgrig', 'batch 219 restored the final g his card writes'),
    # --- dom148.py. The book grew by one: batch 219 corrected `drbiyax` to
    # `dmbiyax` on page 177, a three-legged glyph beside two two-legged n's.
    ('dom148.py', 'GAIN dmbiyax: want 3 dark'):
        ('dark>=3', '', 'batch 219 corrected a transcription slip onto it'),
    # --- dom57.py. The other end of the SIBLING SEAM (inflection.py:1670).
    # Batch 201 moved his QQ'LANG head from `qqlang` to `qqrang`; the t- slot of
    # the cross-referenced card was left tracking the OLD head, and `b57.py:116`
    # says so in its own comment: `"tqq'lang": "tqqlang",  # qq'lang>qqlang;
    # was TQQRANG`. So this pin is not a refusal being overruled -- it is the
    # unfinished half of a supersession, and batch 223 finished it. `map`
    # re-reads the map, so a drift to a third spelling still fails here;
    # dom223.py carries the assertion that the value renders DARK.
    ('dom57.py', "BROWN tqq'lang tqqlang missing on [QQ'LANG]"):
        ('map', 'tqqrang', 'batch 223 finished batch 201\'s head re-ruling'),
    # --- dom66.py. The CITATION SEAM, arriving as a failure for the first time.
    # He carded LIDIL twice and batch 211 split the homograph: the handle sense
    # takes `rijig` 柄 in running text, and `CITE_SPELL['lidil'] = 'rijil'`
    # refuses the map wherever the form renders as a NAME. So BOTH his LIDIL
    # heads paint `RIJIL` PALE (confirmed from `.hw`, w-unv on cards 526 and
    # 527), and the bend card -- six affixed subs, no example -- carries no
    # bare running-text token at all, so there is no `rijig` span on it to find.
    # A HOLD assertion demanding the running-text value on a card that only
    # CITES the word is asking for the half of the split that was refused.
    # Kind `cite` re-asserts both halves, because either one alone would let
    # this row stand over a book that had quietly re-merged the two senses.
    ('dom66.py', 'BROWN lidil rijig missing on [LIDIL]'):
        ('cite', ('lidil', 'rijig', 'rijil'),
         'batch 211 split the LIDIL homograph; the seam pales the citation'),
    # --- batch 236. `teumuk -> towmuk`: one ruling, seven failing rows across
    # four logs. dom221 is the overturned REFUSAL; the other six are the loss
    # shape moving because a pale type came out of it.
    #
    # The refusal read "首領 is bukung and thowlang, neither within reach of
    # teumuk by any correspondence in the map" (dom221.py:138) -- an
    # ORTHOGRAPHIC claim, and batch 236 grants it: his `eu` answers `u`
    # sixteen times against `ow` twice, so `towmuk` takes the minority
    # correspondence. What retires the refusal is that it searched the three
    # gloss files, where `towmuk` is glossed in none and cannot be, its single
    # parquet row having an empty translation column; `towmuk` reaches
    # `attested_modern` by the corpus-sentence leg instead, and his own
    # TXOULANG prose names TEUMUK a Japanese import from 頭目. The majority
    # correspondence has nothing to offer -- `tumuk`, `tmuk`, `tomuk`,
    # `tuwmuk` are in no source at all. Note dom221's own NO_SHAPE regex for
    # 領, `^t?[ei]?umuk`, still returns nothing: `towmuk` never matched it, so
    # the negative half of that refusal is untouched by this ruling and goes
    # on asserting exactly what it always asserted.
    ('dom221.py',
     'FAIL teumuk no longer renders anywhere. It was refused because '
     '首領 is bukung and thowlang, neither within reach of teumuk by '
     'any correspondence in the map -- if the map changed, the refusal needs '
     're-arguing, not deleting.'):
        ('ruled', ('teumuk', 'towmuk'),
         'batch 236 overturned it: the refusal searched the gloss files, and '
         'towmuk is attested by corpus sentence, glossed nowhere'),
    ('dom232.py', 'FAIL FLOOR 5346 pairs'):
        ('floor', (5347, 'teumuk', 'towmuk'),
         'batch 236 RAISED the metric; dom232 pins the pair count by equality, '
         'so a rise fails it exactly as a fall would'),
    ('dom232.py', 'FAIL sole-blocked 79/67 pairs/types'):
        ('shape', ((78, 66), 'teumuk', 'towmuk'),
         'batch 236 took one type out of the sole-blocker list'),
    # The sweep iterates over PALE values, so darkening one drops its row. The
    # lost proposal is `teumuk -> tumun`, one of the eleven batch 232 itself
    # classed as noise: `tumun` is the root for ROUND (mtumun 很圓, mntumun
    # 圓的, stumun 為…做成圓形) and all five of its bare parquet tokens are the
    # personal name Tumun Awi. Neither reading is 首領. The trap row the log
    # guards separately, `yianu -> yamu`, is untouched.
    ('dom232.py', 'FAIL the sentence sweep returned # proposals, expected #'):
        ('shape', ((12, None), 'teumuk', 'towmuk'),
         'batch 236 darkened teumuk, dropping its noise proposal tumun 圓'),
    ('dom234.py', 'FAIL sole-blocker types #, pinned #'):
        ('shape', ((66, None), 'teumuk', 'towmuk'),
         'batch 236 took one type out of the sole-blocker list'),
    ('dom235.py', 'FAIL sole-blocker types #, pinned #'):
        ('shape', ((66, None), 'teumuk', 'towmuk'),
         'batch 236 took one type out of the sole-blocker list'),
    ('dom235.py', 'FAIL sole-blocked pairs #, pinned #'):
        ('shape', ((78, None), 'teumuk', 'towmuk'),
         'batch 236 freed the pair teumuk was holding'),

    # --- batch 241. ONE sentence, cleared by TWO acts, which is why it sat
    # unmoved for eleven batches: every instrument that reached it asked one
    # question of both words. His XNUK example
    # `§ Mxnuk bi ka qouni, ini na txey ka snuk` was one of batch 230's four
    # two-type rows.
    #
    #   * `snuk` is not his word. It occurred exactly ONCE in a book that
    #     repeats itself (batch 213) and he CARDS `SMUK` (R) 釘子 with two
    #     examples and three sub-forms, so there was no glyph left in doubt on
    #     that side (batch 235). Page 374 at 8x, batch 202's protocol: the `n`
    #     of `na` four cells earlier has two legs, the `m` of his French
    #     `(mou)` on the same line has three, and the whole page's French
    #     carries the same fault -- *neuble*, *narché*, *Comne*. So the fix
    #     went in `entries.js`, not in the map (batch 212), and `smuk -> smuk`
    #     was ALREADY dark: the correction cost no map entry at all.
    #   * `txey` reads cleanly on that line, so it IS his and the question is
    #     a spelling one. Ruled `thiy` off his TOXOI 與…在一起 card, whose nine
    #     other family slots already render dark.
    #
    # dom230's REFUSAL of `snuk` is NOT overturned -- "釘 is carried by the
    # `samu` family, a different root" is a correct answer to *what respells
    # `snuk`?* and it never asked whether the string was his. Its row below is
    # therefore credited to the CORRECTED reading and re-asserts that reading's
    # darkness, because that is the fact a rebuild could take away.
    ('dom217.py',
     "FAIL thiy renders # time(s) and NONE is pale. It was refused because "
     "his Txey sits on the XNUK 軟／便宜 card, not on TOXOI; thiyan 和…在一起 "
     "is TOXOI's word and following it would cross two cards"):
        ('ruled', ('txey', 'thiy'),
         'batch 241 retired it: its one leg describes where the token is '
         'PRINTED, not which headword it belongs to. That sentence is running '
         'text, and `smuk` and `qouni` in it are dark off two other cards'),
    ('dom230.py', 'FAIL snuk no longer renders pale; a refused word going dark '
                  'is a ruling nobody wrote'):
        ('ruled', ('smuk', 'smuk'),
         'batch 241 corrected the transcription: `snuk` is a misread `smuk` '
         'and has left the book entirely, so it renders nothing rather than '
         'going dark. The refusal stands; what this row re-asserts is that '
         'the corrected reading is still dark, since a pale `smuk` would mean '
         'the correction had reintroduced the blocker under a new spelling'),
    ('dom232.py', 'FAIL the spellcheck sweep returned # shapes, expected #'):
        ('shape', ((39, None), 'txey', 'thiy'),
         'batch 241 darkened thiy and deleted snuk from the book; the sweep '
         'iterates over PALE values, so both rows left it'),
    ('dom235.py', 'FAIL two-type blocked pairs #, pinned #'):
        ('shape', ((3, None), 'txey', 'thiy'),
         'batch 241 cleared BOTH blockers of one two-type row, 4 -> 3'),
    ('dom235.py', 'FAIL a two-type cluster this batch pinned has left the book '
                  '(snuk+thiy): batch # confirmed all four as refusals, so one '
                  'healing is news'):
        ('shape', ((None,), 'txey', 'thiy'),
         'batch 241 is that news, argued in writing: dom230 confirmed the four '
         'as refusals of RESPELLINGS, and snuk needed a transcription instead. '
         'The only number in this line is the batch it cites, which is source '
         'code and not a measurement'),
    ('dom236.py',
     "FAIL the two-type seam moved: # rows, [('dmtbasyaq', 'dmtsapat'), "
     "('krikut', 'nrikut'), ('tbasyaq', 'tibasyaq')]. Batch # confirmed all "
     "four refusals; a NEW row of this shape is a pair the sole-blocker "
     "ranking cannot see."):
        ('shape', ((3, None), 'txey', 'thiy'),
         'batch 241 removed the snuk+thiy row; the three that remain are the '
         'three this key names, so a NEW row of the shape re-keys and is '
         'reported, which is what the assertion was for'),
    # [batch 241] The three rows below move the OTHER way, which is why `grew`
    # exists. dom238 and dom239 pin `verified.js` by equality and dom238 pins
    # the pair count by equality beside its own `>= FLOOR` leg; a ruling raises
    # both. A ceiling would fail on the next ruling and force every future
    # batch to re-touch these rows -- bookkeeping, which is what `shape` was
    # written to avoid -- while a floor keeps the assertion that matters: a
    # verified key DISAPPEARING is the shape a ruling being silently lost would
    # take, and a pair count falling is the metric regressing.
    ('dom238.py', 'FAIL VERIFIED keys #, pinned #'):
        ('grew', ((6327, None), 'txey', 'thiy'),
         'batch 241 added `thiy`, 6326 -> 6327'),
    ('dom238.py', 'FAIL pairs moved to # — both rulings are furniture and buy '
                  '# BY CONSTRUCTION (batch #); a change here means one of '
                  'them reached a `.truku` box and the pricing was wrong'):
        ('grew', ((5348, None, None), 'txey', 'thiy'),
         "batch 241 bought a pair on a DIFFERENT card, so dom238's furniture "
         'claim is untouched -- its own `inTruku == 0` legs still pass and '
         'still carry it (batch 223). Only the two constants in the sentence '
         'are the log\'s own pin'),
    ('dom239.py', 'FAIL VERIFIED keys #, pinned #'):
        ('grew', ((6327, None), 'txey', 'thiy'),
         'batch 241 added `thiy`, 6326 -> 6327'),
    ('dom239.py', 'FAIL book-wide pale TYPES #, pinned #'):
        ('shape', ((135, None), 'txey', 'thiy'),
         'batch 241 took two types off the book: `thiy` went dark and `snuk` '
         'left the transcription, 137 -> 135'),

    # [this rebuild] Five logs pin MAP_KEYS at 7371, a number batch 241 itself
    # never disturbed -- its own dom241.py log says so explicitly: the entry
    # `snuk -> snuk` is "ORPHANED and left alone... asserted as zero rather
    # than deleted." That was true of the modern_map.js ON DISK at the moment
    # batch 241 ran its suite, because the entries.js correction (snuk is a
    # misread smuk, batch 241 section 1) had landed without anyone re-running
    # `build_modern_map.py`. This rebuild is the first one since, and the
    # generator's own DEAD-key accounting (`build_modern_map.py:1622`, "the key
    # matches no token in entries.js... harmless") is what actually drops it:
    # no token in entries.js reads `snuk` any more, so the manual_map.json
    # entry no longer lands. MAP_KEYS 7371 -> 7370, one key, and it is the
    # same key across all five rows -- so all five are credited to the one
    # `smuk -> smuk` identity claim (`smuk` is tier `id`, already attested,
    # confirmed still in both `modern_map.js` and `verified.js`). A further
    # DEAD key dropping out on some future rebuild is the generator working as
    # documented; a RISE is news a ceiling here is built to catch.
    #
    # dom241.py itself prints this failure TWICE per run -- `main()` does
    # `fails.extend(fs)` where `fs` is already a copy of the same global
    # `fails` list `checks()` just populated, so every checks()-sourced
    # failure doubles. That is a pre-existing bug in a frozen log, not
    # something this rebuild touched, and one LEDGER row adjudicates both
    # printed copies since they share one exact failure line.
    ('dom236.py',
     'FAIL the map has # keys, pinned #: this batch moved three VALUES and '
     'no key'):
        ('shape', ((7370, None), 'smuk', 'smuk'),
         'this rebuild dropped the DEAD `snuk` key once entries.js no longer '
         'contained the token; batch 241 corrected the transcription, this '
         'rebuild is what finally regenerates modern_map.js against it'),
    ('dom237.py',
     'FAIL the map has # keys, pinned #: batch # changes no spelling at '
     'all'):
        ('shape', ((7370, None, None), 'smuk', 'smuk'),
         'same event as dom236.py: the DEAD `snuk` key dropped on this '
         'rebuild, batch 237 itself changed nothing -- sig() blanks EVERY '
         'digit run, including the "237" inside the message text, so `got` '
         'carries three numbers (map keys, pinned keys, batch number) and '
         'the ceilings tuple needs a third None for the batch number, which '
         'is not a measurement at all'),
    ('dom238.py', 'FAIL MAP keys #, pinned #'):
        ('shape', ((7370, None), 'smuk', 'smuk'),
         'same event: the DEAD `snuk` key dropped on this rebuild'),
    ('dom239.py', 'FAIL MAP keys #, pinned #'):
        ('shape', ((7370, None), 'smuk', 'smuk'),
         'same event: the DEAD `snuk` key dropped on this rebuild'),
    ('dom241.py', 'FAIL MAP keys #, pinned #'):
        ('shape', ((7370, None), 'smuk', 'smuk'),
         'batch 241\'s own ORPHAN check (dom241.py:421) already tolerates '
         'this: `MM.get(*ORPHAN)` reads `MM.get("snuk", "snuk")`, so a '
         'missing key and a present identity key are indistinguishable to '
         'it. This row is the OTHER assertion in the same log, the raw key '
         'count, which does not have that escape hatch'),


    # === batch 242 -- the informant's answer sheet. A native Truku speaker
    # answered 71 pale words on a printed sheet; 23 map values changed and ten
    # words entered `HAND_SPOKEN`. 81 blocked pairs -> 53. Every row below is one
    # of those rulings landing on a pin, and the pins are overwhelmingly written
    # REFUSALS -- which is the shape this batch has, because an informant is the
    # one source that can retire a refusal resting on "nothing attests it".
    #
    # The discriminator the batch runs on, argued in full in the batch log: an
    # answer is a RESPELLING only where it is shape-continuous with his token
    # under his own correspondences (`o->u`, `l->r`, `x->h`, `'`/`"` as schwa,
    # `c,` for `x`, final `-e` for `-i`, `q` for modern `k`). Otherwise it names
    # the MEANING and is a translation, not evidence about his letters. Four
    # answers landed on modern HOMOGRAPHS and were refused on that ground
    # (`rqraq` 砍倒, `basiq` 太魯閣石櫟, `rangi` 犯忌, `pgagu` 笛子 -- the last
    # being literally the freeze batch 219 reverted, so it doubles as the
    # batch's control).
    ('dom218.py',
     'FAIL mqlaq no longer renders anywhere on the page. It was refused '
     'because zero of the # register words glossing 癢 are q-initial or '
     'contain raq; the modern itch root is krak/ghguh and mqraq is 抓. Tier X '
     'to mkrak was refused too -- batch # ruled that a lexeme modern Truku '
     'replaced is not a settled class -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL mqlaq maps to mrkrak, not to itself. The identity pin is '
     'load-bearing: charRules(mqlaq) spells mqraq on its own, so deleting the '
     'entry restores the freeze rather than removing it.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 replaced the identity pin with a value. The pin was '
         'load-bearing for exactly the reason it states -- charRules(mqlaq) '
         'spells `mqraq` unaided -- and `mrkrak` blocks it just as well while '
         'also being the word'),
    ('dom218.py',
     'FAIL qlaq no longer renders anywhere on the page. It was refused '
     'because same refusal as mqlaq: there is no q-shaped itch word to find '
     '-- if the transcription or the map changed, the refusal needs '
     're-arguing, not deleting.'):
        ('ruled', ('qlaq', 'rkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL qlaq maps to rkrak, not to itself. The identity pin is '
     'load-bearing: charRules(qlaq) spells qraq on its own, so deleting the '
     'entry restores the freeze rather than removing it.'):
        ('ruled', ('qlaq', 'rkrak'),
         'batch 242 replaced the identity pin with a value; charRules(qlaq) '
         'still spells `qraq` unaided, so the entry is still load-bearing'),
    ('dom221.py',
     'FAIL map mqlaq -> mrkrak. Batch # reverted the tier-B freeze onto mqraq '
     '抓 at a cost of # pairs -- his head is 發癢, the two share no character, '
     'and zero of the # register words glossing 癢 are q-shaped. The identity '
     'pin is what stops charRules spelling mqraq on its own.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL only # row(s) blocked by mqlaq, batch # measured #. A FALL is the '
     'news: it means something darkened the word again.'):
        ('shape', ((0, None, None), 'mqlaq', 'mrkrak'),
         'batch 242 darkened it, so it blocks nothing. The log calls a FALL '
         'news and it is right to -- this is that news, and the ceiling is '
         'set at 0 so the word blocking a row again re-opens the question'),
    ('dom65.py',
     'BROWN mqlaq mqlaq missing on [QLAQ]'):
        ('map', 'mrkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom65.py',
     'BROWN qlaq qlaq missing on [QLAQ]'):
        ('map', 'rkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom65.py',
     'BROWN sqlaq sqlaq missing on [QLAQ]'):
        ('map', 'srkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom217.py',
     'FAIL qloq no longer renders anywhere on the page. It was refused '
     'because the neighbours qloqon and qloqi are unglossed, so the card '
     'offers nothing to read the slot against -- if the transcription or the '
     'map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ("q'loq", 'rkruk'),
         'batch 242 ruled it, and it is the weakest of the four and marked as '
         'such in the batch log: `rkruk` is listed but unglossed, and what '
         'carries it is the exact vowel-parallel to the `qlaq`/`rkrak` pair '
         "the gloss did confirm. The refusal's own reason -- the neighbours "
         'qloqon and qloqi are unglossed, so the card offers nothing to read '
         'the slot against -- is retired by a speaker, which is a source the '
         'card does not have'),
    ('dom57.py',
     "BROWN q'loq qloq missing on [Q'LOQ]"):
        ('map', 'rkruk',
         "batch 242 ruled his Q'LOQ 煤煙 slot to `rkruk`"),
    ('dom57.py',
     "BROWN q'loq qloq missing on [SLöS]"):
        ('map', 'rkruk',
         "batch 242 ruled his Q'LOQ 煤煙 slot to `rkruk`"),
    ('dom217.py',
     'FAIL dmbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('dmbasyaq', 'dmbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL dmtbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ("dmt'basyaq", 'dmptbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL tbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('tbasyaq', 'tbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL tibasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('tibasyaq', 'tbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom144.py',
     'PIN tbasyaq: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `tbasyaq -> tbsiyak`; the old value is nowhere on '
         'the page'),
    ('dom57.py',
     'BROWN tibasyaq tibasyaq missing on [BASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom57.py',
     'BROWN tibasyaq tibasyaq missing on [TIBASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom57.py',
     'BROWN tbasyaq tbasyaq missing on [BASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom58.py',
     "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]"):
        ('map', 'dmptbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom58.py',
     'BROWN dmbasyaq dmbasyaq missing on [SAPAT]'):
        ('map', 'dmbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom59.py',
     'BROWN dmbasyaq dmbasyaq missing on [SAPAT]'):
        ('map', 'dmbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom59.py',
     "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]"):
        ('map', 'dmptbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom215.py',
     'FAIL mslangan is no longer pale. Batch # refused it: he never writes a '
     "gr cluster in # pages and uses gl/g'l for modern gr, so sgrangan 生銹 "
     'would have been sglangan in his hand. If evidence arrived, retire this '
     'pin in writing — do not delete the assertion.'):
        ('ruled', ('mslangan', 'skringan'),
         "batch 242 retires HALF of it, and batch 230's rule is why: check "
         'what a refusal SEARCHED. Every word of the `gr` cluster count '
         'stands -- he never writes `gr` in 398 pages and his correspondence '
         "for it is `gl`/`g'l` -- and it refuses `srangan -> sgrangan`, a "
         'different word with a different cluster. The informant wrote '
         '`skringan` 生鏽'),
    ('dom145.py',
     'PIN empslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom163.py',
     'PIN mslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom164.py',
     'PIN empslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom164.py',
     'PIN mslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom215.py',
     'FAIL rngiyan is no longer pale. Batch # refused it: no attested modern '
     'counterpart; the register carries 剩下來的東西 on nngari/nengari, which is '
     "his separate NGALI card's root. If evidence arrived, retire this pin in "
     'writing — do not delete the assertion.'):
        ('ruled', ('lngiyan', 'rngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom220.py',
     'FAIL rngiyan no longer renders anywhere. It was refused because the '
     'register has no -an form of this root in the syncopated stem at all; '
     'its 剩下的東西 is nngari/nengari, off the FULL stem, which is his OTHER '
     "card's root -- if the map changed, the refusal needs re-arguing, not "
     'deleting.'):
        ('ruled', ('lngiyan', 'rngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom220.py',
     'FAIL pnsrngiyan no longer renders anywhere. It was refused because '
     "same: the register's 使留一些 is pnsngari, built on the full stem. "
     'Inventing pnsrngian to tidy the paradigm would be the metric deciding '
     'the spelling -- if the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('pnslngiyan', 'pnsrngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom57.py',
     'BROWN pnslngiyan pnsrngiyan missing on [SLANGI]'):
        ('map', 'pnsrngian',
         'batch 242 ruled the -an slot on testimony'),
    ('dom230.py',
     'FAIL HOLD snxelan -> snxelan got snhiran -- nothing in this batch '
     'reached that slot'):
        ('ruled', ('snxelan', 'snhiran'),
         'batch 242 reached the slot batch 230 left: he wrote `snhiran` AND '
         '`uhir` beside it, and the second word is what makes the answer '
         'usable -- it names the root and rules out the `hir` 氣喘 homograph '
         'the bare shape would otherwise reach'),
    ('dom230.py',
     'FAIL snxelan no longer renders pale; a refused word going dark is a '
     'ruling nobody wrote'):
        ('ruled', ('snxelan', 'snhiran'),
         'batch 242 wrote the ruling: `snxelan -> snhiran`, `HAND_SPOKEN`, '
         'completing the card batch 230 ruled two slots of'),
    ('dom57.py',
     'BROWN snxelan snxelan missing on [SNOXEL]'):
        ('map', 'snhiran',
         'batch 242 ruled the third slot of the jealousy root'),
    ('dom221.py',
     'FAIL smmul no longer renders anywhere. It was refused because his '
     "SA'MUL 抱在懷裡 is carried by kmeabuh, verbatim, off abuh; the nearest "
     'samul-shaped words are smulus 拉著 and smuling 汙辱 -- if the map changed, '
     'the refusal needs re-arguing, not deleting.'):
        ('ruled', ("sm'mul", 'seemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom221.py',
     'FAIL snmul no longer renders anywhere. It was refused because same card '
     'as smmul, and the whole card is pale head included -- there is no dark '
     'sibling to reason from -- if the map changed, the refusal needs '
     're-arguing, not deleting.'):
        ('ruled', ("sn'mul", 'sneemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom227.py',
     'FAIL CARD snmul renders nowhere; the map entry is not firing'):
        ('ruled', ("sn'mul", 'sneemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom227.py',
     'FAIL REFUSED snmul now has # .truku occurrences, pinned at #'):
        ('shape', ((0, None), "sn'mul", 'sneemur'),
         'batch 242 respelled the token, so the refused string has left the '
         'page entirely. Ceiling 0: the string coming back is what wants a '
         'new row'),
    ('dom215.py',
     'FAIL ksudan is no longer pale. Batch # refused it: his card is (R. = ?) '
     'with no head gloss; the modern shuttle is gikus, a different root, and '
     'there is no shape candidate. If evidence arrived, retire this pin in '
     'writing — do not delete the assertion.'):
        ('ruled', ('ksudan', 'kusutan'),
         'batch 242: he wrote `kusut (kusut-an)`, naming the slot himself, '
         'against the listed `kusut` 線綜棒 on a card glossed 織布用的梭子. The '
         'refusal searched for a shuttle and found `gikus`, a different root, '
         'and said so correctly -- what it could not search is a speaker. +3 '
         'pairs, the largest single card in the batch'),
    ('dom216.py',
     'FAIL graqun no longer renders anywhere on the page. It was refused '
     'because graqil/grqilun are the 賤價 root; the word that fits the sentence '
     "is qrapun, which is his own separate K'LAP card -- if the transcription "
     'or the map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('glaqon', 'glkun'),
         'batch 242: `glkun` is the syncopated -un of the `geeluk` 搶奪 he '
         "wrote on the neighbouring row, and his G'LAQ sentence is 別讓雲豹抓走你的山羊 "
         "-- don't let the clouded leopard SNATCH your goat. The refusal is "
         'right that `graqil`/`grqilun` are the 賤價 root; the word was neither '
         'of them'),
    ('dom217.py',
     'FAIL graqun no longer renders anywhere on the page. It was refused '
     'because graqil/grqilun are the 賤價 root; the word that fits the sentence '
     "is qrapun, which is his own separate K'LAP card -- if the transcription "
     'or the map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('glaqon', 'glkun'),
         'batch 242 ruled it to `glkun`, the syncopated -un of his `geeluk` '
         '搶奪'),
    ('dom216.py',
     'FAIL shmqan no longer renders anywhere on the page. It was refused '
     'because his GMALYEQ card is headed 詞根不明; 監獄/監牢 return # and the sole 牢 '
     'hit hmkan is a verb off another root -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242: he wrote `shmuk` 關著 against his sentence 他們進了監獄. The '
         'refusal searched 監獄/監牢 and the register carries the sense on 關, '
         'which is what the speaker supplied'),
    ('dom217.py',
     'FAIL shmqan no longer renders anywhere on the page. It was refused '
     'because his GMALYEQ card is headed 詞根不明; 監獄/監牢 return # and the sole 牢 '
     'hit hmkan is a verb off another root -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242 ruled it to `shmuk` 關著'),
    ('dom217.py',
     'FAIL hlakuh no longer renders anywhere on the page. It was refused '
     'because his card is 盾牌; hlak is 肉片 and hlaka 展翅, neither a shield -- if '
     'the transcription or the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('xlakux', 'hlakuk'),
         'batch 242: `hlakuk` 用包狀物包起來 is listed and carries a 30-form '
         'covering family, against his 盾牌－保護之物. The refusal searched `hlak` '
         '肉片 and `hlaka` 展翅 and correctly found neither a shield; it did not '
         'reach the covering sense'),
    ('dom217.py',
     'FAIL qlap no longer renders anywhere on the page. It was refused '
     'because his card is 品嚐－親吻; the only qlap- gloss is qlapan 不能生育的女人 -- if '
     'the transcription or the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('qlap', 'qrak'),
         "batch 242: `qrak` 抓 is one edit from the char rules' own `qrap`, in "
         'a sentence glossed 抓住他. The refusal is right that `qlapan` 不能生育的女人 '
         'is the only qlap- gloss -- and that is a fact about the LETTER, '
         'which is what a respelling changes'),
    ('dom231.py',
     'FAIL urang no longer renders pale; a refused word going dark is a '
     'ruling nobody wrote'):
        ('ruled', ('ulang', 'ulan'),
         'batch 242: `ulan` 久病纏身（被病纏身）against his ULANG 反覆發生的－週期性的－慣常的 and '
         "his own sentence about a chronic disease. Batch 230's rule about "
         "what a refusal SEARCHED, applied to batch 230's own refusal: it "
         'searched 週期, 慣常 and 反覆 and never searched 久病 or 疾'),
    ('dom138.py',
     'KEEP urang: want 2 pale'):
        ('absent', '',
         'batch 242 ruled `ulang -> ulan`; `urang` was the char-rule value '
         'and is nowhere on the page now'),
    ('dom144.py',
     'PIN qlap: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `qlap -> qrak`; the old value is nowhere on the '
         'page'),
    ('dom217.py',
     'FAIL rikut renders # time(s) and NONE is pale. It was refused because '
     'his LIKUT 藉口－詭計; 詭計 sits on rnqdug and 欺騙 on qdug, a different root'):
        ('ruled', ('likut', 'rikut'),
         'batch 242, and the weakest entry in it, kept and labelled: he wrote '
         '`rikut`, 口語才部份有，大都用 rabih, qrbling -- "colloquially it partly '
         'exists". Partly exists is still exists, and it is asserted about '
         'the BARE root only, so the four derived slots got nothing and stay '
         'pale. The map never moved: `likut -> rikut` is unchanged and what '
         "darkened is the attestation. That is exactly what this row's second "
         'leg checks -- drop `rikut` from `HAND_SPOKEN` and it leaves '
         'verified.js and the refusal is back'),
    ('dom217.py',
     'FAIL sapi renders # time(s) and NONE is pale. It was refused because '
     'his SAPE is 小鋤頭; the sister sapaw is 舖（舖床、舖葉等）, and the modern word for '
     'a small hoe is parih (# spk) -- a different root, so there is no '
     'respelling of his to find'):
        ('ruled', ('sape', 'sapi'),
         'batch 242 retires ONE leg of a three-leg refusal and leaves the '
         'other two standing. The three-hoe system (`parih`, `bkaruh`) and '
         'the absence of any `sap-` hoe in the register are both still true '
         'and neither is retired. What the refusal ALSO said is that nothing '
         'attests the word at all, and his answer is 是否為借詞，有在用 -- "loanword '
         'or not, it IS in use", the one claim no document could make. The '
         'map value is unchanged; the word went from unattested to attested '
         'by a person'),
    ('dom231.py',
     'FAIL sruweq no longer renders GREEN. Green means no map entry fired, '
     'and the refusal was that supplying one is itself a spelling claim '
     '(batch #)'):
        ('ruled', ('sloweq', 'sruwaq'),
         'batch 242 ruled `sloweq -> sruwaq`. Batch 231 closed the class of '
         '11 headwords he could not gloss himself on the ground that the '
         'gloss test needs a gloss on HIS side too, and that limit is real -- '
         'four of the eleven are on this sheet and exactly ONE is ruled. It '
         'is ruled by SHAPE, never by the informant supplying a meaning: '
         'charRules already prints `sruweq` and `sruwaq` is one vowel from '
         'it, so the answer is shape-continuous and needs no gloss on either '
         'side. The other three were refused'),
    ('dom231.py',
     'FAIL `sruweq` sole-blocks # pairs, was # -- the limit was priced at '
     'that number'):
        ('shape', ((0, None), 'sloweq', 'sruwaq'),
         'batch 242 ruled it, so it blocks nothing. Ceiling 0 -- the pair '
         'coming back is the news'),
    ('dom216.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom217.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom218.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom219.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom220.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom221.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom222.py',
     "FAIL green spans: #, expected # ['Mngusyeh|SIRAS (NGUSYEX)']"):
        ('shape', ((1, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom233.py',
     'FAIL the tag census is (#, #, #), pinned (#, #, #)'):
        ('shape', ((None, 14, 5, None, None, None), "q'loq", 'rkruk'),
         "batch 242 darkened ONE tag span: his LQLOQ tag reads (R. = Q'LOQ = "
         "suie ?) and `q'loq -> rkruk` paints the variant brown. 321/15/5 -> "
         '322/14/5, total held at 341. Only the pale and green halves carry '
         'ceilings -- a DARK rise is the project working, and putting a '
         'ceiling on it would make the row bookkeeping (batch 241)'),
    ('dom233.py',
     "FAIL the non-dark tag rows split {'root': #, '?': #, 'variant': #} by "
     "shape, pinned {'root': #, 'variant': #, '?': #}"):
        ('shape', ((14, 2, 2, None, None, None), "q'loq", 'rkruk'),
         'the same one span, seen by shape: root 15 -> 14, `?` and `variant` '
         'unmoved. Batch 233 closed this class -- every non-dark tag row is a '
         'settled class or a written refusal -- and a row LEAVING it does not '
         're-open it'),
    ('dom235.py',
     'FAIL a two-type cluster this batch pinned has left the book '
     '(tbasyaq+tibasyaq; dmtbasyaq+dmtsapat; snuk+thiy): batch # confirmed '
     'all four as refusals, so one healing is news'):
        ('shape', ((None,), 'tibasyaq', 'tbsiyak'),
         'batch 242 cleared it: `tibasyaq -> tbsiyak` and `tbasyaq -> '
         "tbsiyak` took both blockers of one two-type row, and `dmt'basyaq -> "
         'dmptbsiyak` took one of another. The list this key names is the '
         'batch-241 row plus the two this batch cleared, so the head re-keys '
         'whenever another one goes -- which is the assertion working. The '
         'only number in the line is the batch it cites, which is source code '
         'and not a measurement'),
    ('dom235.py',
     'FAIL only # of # sole blockers are rare, where this batch measured #. '
     'Rarity was pinned as a property of the whole seam; if it has become '
     "discriminating, batch #'s test can rank the pale after all."):
        ('shape', ((37, 44, None, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 took 23 types out of the sole-blocker list, so both '
         'halves of the fraction fell: 55 of 67 -> 37 of 44. The PROPORTION '
         'is what batch 235 pinned and it is unmoved (82% -> 84%), so the '
         'finding stands -- rarity still does not discriminate. Ceilings on '
         'both counts, because a blocker coming back is the news'),
    ('dom236.py',
     "FAIL the two-type seam moved: # rows, [('krikut', 'nrikut')]. Batch # "
     'confirmed all four refusals; a NEW row of this shape is a pair the '
     'sole-blocker ranking cannot see.'):
        ('shape', ((1, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 cleared it: `tibasyaq -> tbsiyak` and `tbasyaq -> '
         "tbsiyak` took both blockers of one two-type row, and `dmt'basyaq -> "
         'dmptbsiyak` took one of another, leaving one row, `krikut+nrikut` '
         '-- and `rikut` is in this batch too, as the deliberately weak '
         'HAND_SPOKEN entry that buys the BARE root and none of the four '
         'derived slots. Ceiling 1: a NEW row of this shape is still a pair '
         'the sole-blocker ranking cannot see'),
    ('dom241.py',
     'FAIL VERIFIED keys #, pinned #'):
        ('grew', ((6350, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 added 23 verified values, 6327 -> 6350. `grew`, not '
         '`shape`: a verified key DISAPPEARING is the shape a ruling being '
         'silently lost would take. dom241.py prints this failure twice per '
         'run (its own pre-existing double-`extend` bug), and one row '
         'adjudicates both copies'),
    ('dom237.py',
     'FAIL the sweep no longer reaches shmqan; it is the positive control on '
     'the instrument, and losing it means the sweep is blind, not that the '
     'record is clean'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242 ruled `sxmqan -> shmuk`, and the log is right that this '
         'leaves the sweep without its positive control -- the control was a '
         'PALE value, and the sweep iterates over pale values, so darkening '
         'it is exactly what removes it. That is a real cost and it is '
         "recorded rather than excused: batch 237's instrument needs a new "
         'control before it is trusted again, and this row re-asserts that '
         'the ruling which took the old one is still standing in both tables'),
}

# [batch 226] Rows whose failure was HEAD-RELATIVE, and which the commit of
# batches 211-225 absorbed. Six of these logs (dom57/59/60/63/65/66) hold their
# neighbours at `val(t, OLD)` where `OLD = git show HEAD:site/modern_map.js`
# (dom66.py:51). The pin says "this neighbour must still paint what it painted
# before the rebuild" -- so the moment the rebuild is committed, HEAD carries
# the new value, the assertion re-baselines onto it, and the row stops firing.
# That is not a pin retiring on evidence; it is the working copy and HEAD
# agreeing again, and it fired eleven times at once because one commit carried
# fifteen batches. The rows and their reasons are KEPT -- deleting them would
# destroy the record, and a genuine return of any of these failures still finds
# its explanation in LEDGER -- but they are subtracted from the HEALED report,
# which would otherwise stand at 11 forever and mask the next real healing.
ABSORBED = {
    ('dom57.py', 'BROWN pslangi pslangi missing on [SLANGI]'),
    ('dom57.py', 'BROWN pslngiyun psrngiyun missing on [SLANGI]'),
    ('dom59.py', 'BROWN tqliyun tqriyun missing on [QELI]'),
    ('dom60.py', 'BROWN tglgli tgrgri missing on [QALAS]'),
    ('dom63.py', 'BROWN kmbyanan kmbyanan missing on [GBIYAN]'),
    ('dom63.py', "BROWN lidil rijil missing on [L'BU]"),
    ('dom63.py', 'BROWN snola snola missing on [LUUS]'),
    ('dom65.py', 'BROWN mqlaq mqraq missing on [QLAQ]'),
    ('dom65.py', 'BROWN tqliyun tqriyun missing on [QELI]'),
    ('dom66.py', 'BROWN kmbyanan kmbyanan missing on [GBIYAN]'),
    ('dom66.py', "BROWN lidil rijil missing on [L'BU]"),
    # [batch 230] The batch-226 mechanism again, and the first time it has
    # arrived for a log outside the six named there: dom58.py:12 also reads its
    # *before* map out of `git show HEAD:site/modern_map.js`. Committing batch
    # 229 put `n'gui`/`nagui -> gneeguy` into HEAD, so the log's before and
    # after now agree and the rows stop failing. Nothing about the book moved.
    # Kept in LEDGER because the explanation is still owed if they come back.
    ('dom58.py', "BROWN n'gui nguy missing on [SLAP]"),
    ('dom58.py', 'BROWN nagui nagui missing on [SLAP]'),
    # [batch 231] The same mechanism, and this run explains why batch 230's four
    # rows split three-and-one. A HOLD value comes from `val(t, OLD)`, and
    # `val()` reads `WORD_OVERRIDES` BEFORE the map (dom57.py:63) -- so a token
    # in OV never re-baselines however the map moves. `msnoxel` and `pstui` are
    # map-only and healed the moment batch 230 went into HEAD; `snoxel` is in
    # OV, so its row still fails and stays live. Absorbed, not deleted.
    ('dom57.py', 'BROWN msnoxel msnoxel missing on [SNOXEL]'),
    ('dom63.py', 'BROWN pstui pstui missing on [SPONG]'),
    ('dom66.py', 'BROWN msnoxel msnoxel missing on [TAKOL]'),
    # [batch 232] Committing batch 231 healed the `kasayang` row in TWO of the
    # three logs that carried it, and the split is not batch 231's OV/map one --
    # it is TARGET versus HOLD. dom63 and dom67 held the token as a NEIGHBOUR,
    # `val(t, OLD)` off `git show HEAD:site/modern_map.js`; HEAD now says
    # `ka sayang`, so before and after agree and the row stops failing with
    # nothing about the book having moved (batch 226's mechanism). dom57 pins it
    # as its own TARGET -- `b57.py:127` is where the identity claim was written
    # -- and a target is read from the batch's pin file, never from HEAD, so
    # that row can only heal if the map reverts. It stays live in LEDGER, kind
    # `map`. Ask which of the two a row is BEFORE explaining why it healed.
    ('dom63.py', 'BROWN kasayang kasayang missing on [SLIYU]'),
    ('dom67.py', 'BROWN kasayang kasayang missing on [SLIYU]'),
    # [batch 242] A raw COUNT assertion healed without its subject moving --
    # the arithmetic refilled the hole, and the reason each row records is still
    # literally true. Batch 241's transcription fix dropped the DEAD `snuk` key
    # and left the map at 7370 against a pin of 7371, which is what these five
    # rows explain. Batch 242 added exactly ONE key, `sloweq` (the SLOWEQ head
    # had no map entry at all, which is why it rendered GREEN), and the map is
    # back at 7371. `snuk` is still gone -- `MAP.get("snuk")` is None -- so
    # nothing these rows assert has been undone; a key count simply cannot tell
    # "the lost key came back" from "a different key arrived". Batch 241 noted
    # that dom241's ORPHAN check has an escape hatch its raw count "does not
    # have"; this is the raw count's own blind spot, and it is the reason the
    # rows are kept rather than retired.
    ('dom236.py',
     'FAIL the map has # keys, pinned #: this batch moved three VALUES and no '
     'key'),
    ('dom237.py',
     'FAIL the map has # keys, pinned #: batch # changes no spelling at all'),
    ('dom238.py',
     'FAIL MAP keys #, pinned #'),
    ('dom239.py',
     'FAIL MAP keys #, pinned #'),
    ('dom241.py',
     'FAIL MAP keys #, pinned #'),
    # [batch 242] Re-keyed, not retired. Both lines carry a LIST inside the
    # message, so clearing a cluster changes the key rather than silencing the
    # assertion -- which is exactly what batch 241 said this shape was for ("a
    # NEW row of this shape re-keys and is reported"). Batch 242 cleared
    # `tbasyaq+tibasyaq` and `dmtbasyaq+dmtsapat`, so both messages re-key and
    # their successors are in the batch-242 block above, carrying the new
    # lists. The old keys can only fire again if the rulings revert.
    ('dom235.py',
     'FAIL a two-type cluster this batch pinned has left the book '
     '(snuk+thiy): batch # confirmed all four as refusals, so one healing is '
     'news'),
    ('dom236.py',
     "FAIL the two-type seam moved: # rows, [('dmtbasyaq', 'dmtsapat'), "
     "('krikut', 'nrikut'), ('tbasyaq', 'tibasyaq')]. Batch # confirmed all "
     'four refusals; a NEW row of this shape is a pair the sole-blocker '
     'ranking cannot see.'),
    # [batch 242] The assertion did not RUN. dom232 prints `parquets not
    # mounted -- sweeps 1 and 2 SKIPPED`, which is batch 232's own rule working
    # (an absent source must skip, not bank its emptiness as a zero) -- and a
    # sweep that does not run emits no failure line, which reads on screen
    # exactly like a pin retiring. An absence the instrument cannot see is not
    # a healing. The row stays live in LEDGER for whenever the parquets are
    # mounted again -- and on the batch's verification run they WERE: the sweep
    # ran, returned 8 proposals against the pin of 13, and its ledger row
    # adjudicated it (superseded 285 -> 286, healed 9 -> 0). That one-count
    # difference in the green line is the drive, not the book.
    ('dom232.py',
     'FAIL the sentence sweep returned # proposals, expected #'),
    # [batch 242] Batch 226's mechanism once more, on the log batch 230 added
    # to the class: `dom58.py:12` reads its *before* map from `git show
    # HEAD:site/modern_map.js`. Batch 238 ruled `bsqan -> pskan`, and once that
    # went into HEAD the log's before and after agree, so no HOLD row for the
    # old `bsekan` is generated at all. Note this healed BEFORE batch 242
    # touched anything -- it is the commit of b43895b, not this batch's work.
    ('dom58.py',
     'BROWN bsqan bsekan missing on ["QAN]'),
}


def sig(line):
    """The stable half of a failure line, and the volatile half beside it.

    Counts drift with the book; card lists drift with the map. Key on what the
    pin CLAIMED, carry what it SAW separately, and a re-run compares like with
    like."""
    s = " ".join(line.split())
    # [batch 218] The metric floor. The log's own pin is the STABLE half; the
    # measurement beside it is the volatile one, exactly as for a count. Before
    # this, a floor failure carried the measured number in the key, so it
    # crashed the suite instead of reaching the adjudicator -- the one failure
    # kind batch 209 never wired up, because the metric had only ever risen.
    m = re.match(r"FAIL deliverable pairs FELL to (\d+), floor is (\d+)$", s)
    if m:
        return "FLOOR %s" % m.group(2), m.group(1)
    if ", got " in s:
        head, got = s.split(", got ", 1)
        return head, got
    # [batch 219] A prose refusal assertion. dom214/216/217 write their pins as
    # `FAIL <word> ... It was refused because ...`, which carried no recognised
    # shape at all -- so the log exited rc=1 with nothing `failures()` could see
    # and the suite called it CRASHED. Four real failures hid behind that for a
    # whole batch. The numbers inside the sentence are the measurement, exactly
    # as in a count line, so key on the sentence with them blanked and carry
    # them beside it.
    if s.startswith("FAIL "):
        nums = re.findall(r"\d+", s)
        return re.sub(r"\d+", "#", s.split(" green there:")[0]), " ".join(nums)
    return s.split(" green there:")[0], ""


FAILLINE = re.compile(r"( want \d+ \w+, got )|^(BROWN|GREEN|STALE|WAS) "
                      r"|^FAIL ")


def failures(text):
    for l in text.splitlines():
        s = l.strip()
        if FAILLINE.search(s):
            yield s


def load_map():
    s = open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
    return dict(re.findall(r'^"(.+?)":"(.+?)"', s, re.M))


def load_ver():
    # verified.js writes its keys with TWO leading spaces and modern_map.js with
    # none (batch 207). A pattern that works on one silently matches nothing on
    # the other.
    s = open(os.path.join(ROOT, "site", "verified.js"), encoding="utf-8").read()
    return dict((k, int(n)) for k, n in re.findall(r'^  "(.+?)": (\d+),?$', s, re.M))


def load_cite():
    """`CITE_SPELL` (app.js): the refuse-only seam that pales a citation.

    Read from app.js and nowhere else. It is invisible to the generator, so a
    value here is absent from verified.js by construction (batch 215) -- which
    is exactly what makes a wrong seam cost a pale headword and not a dark
    wrong word, and what makes this table the other half of a split ruling."""
    s = open(os.path.join(ROOT, "site", "app.js"), encoding="utf-8").read()
    i = s.index("var CITE_SPELL = {")
    return dict(re.findall(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"',
                           s[i:s.index("\n  };", i)]))


def meta_rows():
    """The rows batch 207 stopped painting: `t` is its own French translation."""
    s = open(os.path.join(ROOT, "site", "entries.js"), encoding="utf-8").read()
    E = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
    norm = lambda x: re.sub(r"[\s.!?;:,'\"’“”]+", "", (x or "")).lower()
    out = []
    for e in E:
        groups = [(e["hw"], e.get("examples") or [])]
        for sub in e.get("subs") or []:
            groups.append((e["hw"], sub.get("examples") or []))
        for hw, exs in groups:
            for x in exs:
                if x.get("t") and x.get("fr") and norm(x["t"]) == norm(x["fr"]):
                    out.append((hw, x["t"]))
    return out


GOT = re.compile(r"'(\w+)': (\d+)")


def adjudicate(log, line, MAP, META):
    """Does the ledger explain this failure, and does its reason still hold?"""
    head, got = sig(line)
    rec = LEDGER.get((log, head))
    if not rec:
        return None, "no ledger row"
    kind, arg, why = rec
    seen = dict((k, int(v)) for k, v in GOT.findall(got))
    if kind == "dark":
        if seen != {} and list(seen) == ["dark"]:
            return rec, ""
        return rec, "ledger says dark, page says %s" % (got or "nothing")
    if kind.startswith("dark>="):
        n = int(kind[6:])
        if list(seen) == ["dark"] and seen["dark"] >= n:
            return rec, ""
        return rec, "ledger says dark >= %d, page says %s" % (n, got or "nothing")
    if kind == "absent":
        if not seen:
            return rec, ""
        return rec, "ledger says absent, page says %s" % got
    if kind == "shape":
        # [batch 236] The LOSS SHAPE -- sole-blocker types, sole-blocked pairs,
        # and the count of proposals a sweep returns. A ruling removes a pale
        # type, so every log that pinned the shape fails at once; six did this
        # batch. The temptation is to key on the new numbers and re-key them
        # every batch, which is equality by another name and would make these
        # rows pure bookkeeping. So the assertion is DIRECTIONAL, like `floor`
        # and for the same reason: a blocker count that FALLS is the project
        # working, and a count that RISES is news that wants its own row.
        #
        # `arg` is (ceilings, tok, val). `ceilings` runs parallel to the
        # integers in the volatile half, one per number, and `None` marks a
        # number that is the LOG'S OWN PIN rather than a measurement -- sig()
        # blanks every digit in a prose FAIL, so the pin and the measurement
        # arrive side by side and only one of them is a fact about the book.
        # Asserting the pin would be asserting the log's source code.
        ceilings, tok, val = arg
        nums = [int(n) for n in re.findall(r"\d+", got)]
        if len(nums) != len(ceilings):
            return rec, ("ledger expects %d number(s) in this failure, the "
                         "page reports %d (%s) -- the log's wording moved and "
                         "the row is no longer measuring what it says"
                         % (len(ceilings), len(nums), got))
        for n, c in zip(nums, ceilings):
            if c is not None and n > c:
                return rec, ("ledger says this count is at or below %d since "
                             "%s was ruled %s; the page measures %d, which is "
                             "a RISE and wants its own row" % (c, tok, val, n))
        if MAP.get(tok) != val:
            return rec, ("ledger says the shape moved when %s was ruled %s, "
                         "but the map says %s -- the row is excusing a count "
                         "change whose cause is gone"
                         % (tok, val, MAP.get(tok)))
        ver = load_ver()
        for part in [val] + (val.split() if " " in val else []):
            if part not in ver:
                return rec, ("ledger says %s -> %s moved the shape, but %s is "
                             "not in verified.js, so it renders pale and the "
                             "blocker it removed is back" % (tok, val, part))
        return rec, ""
    if kind == "grew":
        # [batch 241] `shape` MIRRORED. Some prose counts move the other way:
        # `verified.js` keys and the deliverable-pair count RISE when the
        # project works, so a ceiling on them would fail on the next ruling and
        # force every future batch to re-touch the row -- bookkeeping, which is
        # what `shape` was written to avoid. The direction has to be declared by
        # the row rather than inferred from the wording, so this is a separate
        # kind and not a sign convention inside `shape`: a count that RISES is
        # the project working, a FALL is news, and a verified key disappearing
        # is exactly the shape a ruling being silently lost would take.
        #
        # `arg` is (floors, tok, val), floors parallel to the integers in the
        # volatile half, `None` marking a number that is the LOG'S OWN PIN
        # rather than a measurement (batch 236) -- for a prose line that is
        # every constant the sentence happens to contain, including the batch
        # numbers it cites.
        floors, tok, val = arg
        nums = [int(n) for n in re.findall(r"\d+", got)]
        if len(nums) != len(floors):
            return rec, ("ledger expects %d number(s) in this failure, the "
                         "page reports %d (%s) -- the log's wording moved and "
                         "the row is no longer measuring what it says"
                         % (len(floors), len(nums), got))
        for n, c in zip(nums, floors):
            if c is not None and n < c:
                return rec, ("ledger says this count is at or above %d since "
                             "%s was ruled %s; the page measures %d, which is "
                             "a FALL and wants its own row" % (c, tok, val, n))
        if MAP.get(tok) != val:
            return rec, ("ledger says the count moved when %s was ruled %s, "
                         "but the map says %s -- the row is excusing a count "
                         "change whose cause is gone"
                         % (tok, val, MAP.get(tok)))
        ver = load_ver()
        for part in [val] + (val.split() if " " in val else []):
            if part not in ver:
                return rec, ("ledger says %s -> %s moved the count, but %s is "
                             "not in verified.js, so it renders pale and the "
                             "ruling it is credited to is effectively gone"
                             % (tok, val, part))
        return rec, ""
    if kind == "floor":
        # [batch 218] A floor supersession is the easiest row in this file to
        # write as an excuse, so it re-asserts TWO things: the metric is still
        # at or above the floor the overturning batch set (a further fall is
        # news and fails here), and the ruling that cost the pairs is still in
        # the map. Removing the ruling without restoring the pairs fails too.
        new, tok, val = arg
        now = int(got) if got.isdigit() else -1
        if now < new:
            return rec, ("ledger says the floor moved to %d when %s was ruled "
                         "%s; the page now measures %s, which is a NEW fall "
                         "and wants its own row" % (new, tok, val, got))
        if MAP.get(tok) != val:
            return rec, ("ledger says these pairs were spent ruling %s -> %s, "
                         "but the map now says %s -- the cost is being carried "
                         "for a ruling that is no longer there"
                         % (tok, val, MAP.get(tok)))
        return rec, ""
    if kind == "ruled":
        # [batch 219] A written refusal overturned by a later ruling. The row is
        # only allowed to stand while that ruling does, so it re-reads BOTH
        # tables: a drift to a third spelling fails here, and so does a value
        # that has stopped being verified -- which is the shape a refusal would
        # take if it were quietly reinstated by a rebuild.
        tok, val = arg
        if MAP.get(tok) != val:
            return rec, ("ledger says the refusal was overturned by %s -> %s, "
                         "but the map says %s -- the supersession is being "
                         "carried for a ruling that is no longer there"
                         % (tok, val, MAP.get(tok)))
        # [batch 231] A map value can be TWO WORDS -- his typewriter joined a
        # clitic to its host, and the ruling splits it. `attested()` splits on
        # the space and takes the min over the parts, so a single membership
        # test on the whole string would pass over a value that renders pale
        # because one half of it is unverified.
        ver = load_ver()
        for part in [val] + (val.split() if " " in val else []):
            if part not in ver:
                return rec, ("ledger says %s -> %s overturned the refusal, but "
                             "%s is not in verified.js, so it renders pale and "
                             "the refusal it superseded is effectively back"
                             % (tok, val, part))
        return rec, ""
    if kind == "cite":
        # [batch 226] A SPLIT ruling: the map carries one sense and CITE_SPELL
        # refuses it for the other. Re-assert both halves, or the row would go
        # on excusing this failure over a book that had re-merged the senses --
        # and the merge could arrive from either side, since deleting the
        # CITE_SPELL key would send every citation back to the map's value and
        # changing the map would move the running text out from under the seam.
        tok, running, cited = arg
        if MAP.get(tok) != running:
            return rec, ("ledger says the split sends running text to %s, the "
                         "map says %s" % (running, MAP.get(tok)))
        cs = load_cite()
        if cs.get(tok) != cited:
            return rec, ("ledger says CITE_SPELL pales the citation to %s, "
                         "app.js says %s -- the other half of the split is "
                         "gone, so this is no longer a seam" % (cited, cs.get(tok)))
        return rec, ""
    if kind in ("map", "meta"):
        m = re.match(r"^BROWN (\S+) (\S+) missing on \[(.+?)\]$", head)
        tok, claim, card = m.groups()
        now = MAP.get(tok)
        if now != arg:
            return rec, "ledger says %s maps to %s, the map says %s" % (tok, arg, now)
        if kind == "meta" and card not in META:
            return rec, "ledger says [%s] is a metalinguistic card; it is not" % card
        return rec, ""
    return rec, "unknown ledger kind %r" % kind


def run(f):
    r = subprocess.run([sys.executable, f], cwd=LOGS, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return f, (r.stdout or "") + (r.stderr or ""), r.returncode


def main():
    pick = sys.argv[1] if len(sys.argv) > 1 else ""
    names = sorted(os.path.basename(p) for pat in ("dom*.py", "freeze2*.py")
                   for p in glob.glob(os.path.join(LOGS, pat)))
    names = [n for n in names if pick in n]
    MAP = load_map()
    META = set(hw for hw, _ in meta_rows())
    if len(META) != 1 or len(meta_rows()) != 6:
        print("!! the metalinguistic-row test no longer finds six rows on one "
              "card: %d rows, cards %s" % (len(meta_rows()), sorted(META)))
    ok = superseded = regressions = crashed = 0
    seen_keys = set()
    bad = []
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for f, txt, rc in ex.map(run, names):
            fs = list(failures(txt))
            if rc and not fs:
                crashed += 1
                bad.append("  CRASH   %-13s rc=%d %s" % (f, rc, txt.strip()[-90:]))
                continue
            if not fs:
                ok += 1
                continue
            for line in fs:
                head, _ = sig(line)
                seen_keys.add((f, head))
                rec, err = adjudicate(f, line, MAP, META)
                if err:
                    regressions += 1
                    bad.append("  %-13s %s\n                %s" % (f, line[:96], err))
                else:
                    superseded += 1
    # Only over the logs this run actually executed — a filtered run must not
    # report every unselected log's rows as healed.
    healed = sorted(k for k in set(LEDGER) - seen_keys - ABSORBED
                    if k[0] in set(names))
    # [batch 217] Healing must be REPRODUCED before it is reported, and
    # reproduced SERIALLY. A ledger row heals when its exact failure line stops
    # appearing -- and the line carries the measurement in it, so a log that
    # under-renders emits `got {}` where it used to emit `got {'dark': 1}` and
    # the key stops matching. That is indistinguishable from a pin retiring.
    # It happened: four wiring_score shards from another project saturated the
    # machine, this pool put four more browsers on it, and dom154 -- a 2026-era
    # log still waiting 6s where the standard is now 22s -- reported all five of
    # its COINCIDENCE/PIN rows healed at once. Run alone, it reproduced every
    # one of them as `got {'dark': N}`: five true pins, and the advice on
    # screen was `retire them`. Retiring a row destroys the only evidence
    # anything moved, so the burden of proof belongs on the healing.
    if healed:
        rescued = 0
        reran = sorted({k[0] for k in healed})
        for f in reran:
            _, txt, _rc = run(f)
            for line in failures(txt):
                key = (f, sig(line)[0])
                if key in healed:
                    rescued += 1
                seen_keys.add(key)
        healed = sorted(k for k in set(LEDGER) - seen_keys - ABSORBED
                    if k[0] in set(names))
        if rescued:
            print("re-ran %d log(s) serially: %d apparent healings did NOT "
                  "reproduce (a contended run under-renders and reports a "
                  "colour it cannot see as an absence)"
                  % (len(reran), rescued))
    print("SUITE %d logs — %d clean, %d superseded, %d REGRESSIONS, %d crashed"
          % (len(names), ok, superseded, regressions, crashed))
    for b in bad:
        print(b)
    if healed:
        print("HEALED %d ledger rows no longer fail — retire them:" % len(healed))
        for k in healed[:20]:
            print("   %s  %s" % k)
    return 1 if (regressions or crashed) else 0


if __name__ == "__main__":
    sys.exit(main())
