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

Five kinds, and each one re-asserts something rather than merely excusing it:

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
    # --- dom58.py
    ('dom58.py', 'BROWN m\'mu mmu missing on ["MU]'):
        ('map', 'meemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN n\'mu nmu missing on ["MU]'):
        ('map', 'neemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN nn\'mu nnmu missing on ["MU]'):
        ('map', 'nneemu', 'batch 201 respelled it'),
    ('dom58.py', 'BROWN pn\'mu pnmu missing on ["MU]'):
        ('map', 'pneemu', 'batch 201 respelled it'),
    # --- dom66.py
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
}


def sig(line):
    """The stable half of a failure line, and the volatile half beside it.

    Counts drift with the book; card lists drift with the map. Key on what the
    pin CLAIMED, carry what it SAW separately, and a re-run compares like with
    like."""
    s = " ".join(line.split())
    if ", got " in s:
        head, got = s.split(", got ", 1)
        return head, got
    return s.split(" green there:")[0], ""


FAILLINE = re.compile(r"( want \d+ \w+, got )|^(BROWN|GREEN|STALE|WAS) ")


def failures(text):
    for l in text.splitlines():
        s = l.strip()
        if FAILLINE.search(s):
            yield s


def load_map():
    s = open(os.path.join(ROOT, "site", "modern_map.js"), encoding="utf-8").read()
    return dict(re.findall(r'^"(.+?)":"(.+?)"', s, re.M))


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
    healed = sorted(k for k in set(LEDGER) - seen_keys if k[0] in set(names))
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
