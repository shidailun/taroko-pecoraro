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
    # --- dom66.py
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
        if val not in load_ver():
            return rec, ("ledger says %s -> %s overturned the refusal, but %s "
                         "is not in verified.js, so it renders pale and the "
                         "refusal it superseded is effectively back"
                         % (tok, val, val))
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
