# -*- coding: utf-8 -*-
"""batch 217 — a suffix the analyser could not strip, the leg of the same fix
that had to be refused, and nineteen refusals written down.

### `spngao` → `spngaw` — an analyser gap, not a verdict

His SM"LU card is 獲得（？）；決定；落到誰身上, and it has no sub-forms at all —
so batch 199's cheapest question, *what do the other slots on this card say*,
returns nothing. The word had to stand on its own root.

It does. `roots()` restores the swallowed vowel for `un`, `an`, `ani`, `anay`
and `aneyi` — and for nothing else:

    cands = [r]
    if sf in ("un", "an", "ani", "anay", "aneyi"):
        cands += [r + c for c in VOW]      # the swallowed vowel

`spngan` (attested, 38 speakers, 分) and `spngun` both reach the listed `spngi`
(16 speakers) through that branch. `spngaw` strips to `spng`, a string no
wordlist holds, and comes back with an EMPTY candidate list — invisible not to
one rung but to all fifteen, since every rung begins by asking `roots()` for
something to read. The probe is what settled it: every predicate refused
`spngaw` and `spngay`, while `spngun` — equally unattested — passed `regular`,
`sistered` and `restored`. Two words, one paradigm, opposite verdicts, and the
only thing separating them is which suffix is in a five-item tuple. That is a
fact about the inventory, the same shape as *the analyser cannot see
reduplication*.

The root is sound in meaning as well as in shape: `spung` 不要太過分 (9 spk),
`smpung` 量一量 (13), `spngpun` 嘗試一下, `spngan` 分. His sentence is
§ Spngao ta otoç (vl. spngao ta lqti) — "let's draw lots for it (vl. draw
straws)", the instrument varying while the verb stays put, which is *let us
try/allot* and not a lexeme meaning 抽籤. The two register words that DO carry
抽籤 — `klaaw` 查明；抽籤決定 and `slug` 運氣；抽籤 — are different roots, and
batch 203 is why that does not refuse him: a sentence-corpus gloss is not the
headword's gloss. What the sentence is *about* is lot-casting; what his word
*is* is `spung`'s hortative.

`spngaw` came back **code 6** — `no_chinese`, a regular inflection of a listed
root for which he wrote no Chinese as a word, which is exactly true here: the
only Chinese near it belongs to the example. 1 pair, 5328 → 5329.

### the `-i` leg — refused, and it is the whole reason to write this down

The obvious fix was to add `aw`, `ay` AND `i` to the tuple. Priced, that buys
three promotions of words already dark (`pteuqi` 11→2, `qhdi` 11→2, `tlami`
3→2, all three exact gloss matches) and one new WRONG value:

    qnadi  ->  root qnada  已丟棄的        his card QADI 格子架、編織物

His `Qnadi paqao` 以荊棘、藤蔓編紮而成 is q⟨n⟩adi, the perfective of his own
weaving root. Restoring a vowel before `-i` roots it instead on `qnada`, *the
already-discarded*, a different word one final vowel away — and it is admitted
through `no_chinese()`, the one rung that SKIPS the gloss test, because the only
Chinese near the word is the example's. A homograph freeze arriving through the
analyser rather than through the map, and dark spans do not show up in any
colour metric.

The asymmetry is the rule: before `-aw`/`-ay` the suffix REPLACES the base
vowel, so restoring one is recovering something the morphology took away.
Before `-i` that vowel is itself what distinguishes two roots, so restoring one
invents a relationship. `aw` and `ay` only.

Guarded on an empty candidate list, for the reason batch 164's two-prefix peel
is guarded: nothing that decomposes today can gain a candidate, so `no_chinese`
can never be tipped from a clean one-group reading into an ambiguous one and
DE-verify something. Measured both directions: +1 value, 0 lost, 0 relevelled,
map 7373 → 7373 unchanged.

### the sister sweep — a negative result, kept reproducible

The finding generalises into an instrument: a pale word whose sisters in the
same slot family are VERIFIED, while it scores level 0 itself, is the
fingerprint of an analyser gap rather than of a missing word. Run over all 174
pale values it returns **five**, and four are traps already refused in writing —
`qadi` and `qnadi` are the `-i` leg refused above, `tbiyi` and `tbiyun` are
batch 199's six-wrong-words-in-one-ruling beside `tbiyan` 下來. The fifth,
`sapi`, had not been read: his SAPE is 小鋤頭, its sister `sapaw` is
舖（舖床、舖葉等）, and the modern word for a small hoe is `parih` (43 spk), a
different root. Refused. **The seam is closed with exactly one ruling in it**,
which is worth knowing before anyone widens `roots()` again on the strength of
batch 217.

### twenty refusals, written down

Two families, seven neighbours and the sweep's one hit — the families and
neighbours all researched in batch 216 and none of them recorded until now.
Each renders on the page and each is pale, checked off the DOM rather than off
this dict.
"""
import io
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "..", "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0, green = 0;
  const hits = [], greens = [], seen = {}, unv = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    // Walk the .truku boxes. A prefix on the selector string -- '.truku ' + SEL
    // -- scopes only the FIRST alternative and leaves w-unv and w-raw matching
    // the French too (batch 216).
    c.querySelectorAll('.truku').forEach(box => {
      box.querySelectorAll(SEL).forEach(s => {
        const t = (s.textContent||'').trim().toLowerCase();
        seen[t] = (seen[t] || 0) + 1;
        if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
        if (s.classList.contains('w-raw')) {
          green++; greens.push(s.textContent.trim() + '|' + hw); }
      });
    });
    c.querySelectorAll('.example').forEach(x => {
      const tr = x.querySelector('.truku'); if (!tr) return;
      const sp = [...tr.querySelectorAll(SEL)]; if (!sp.length) return;
      tot++;
      const bad = sp.filter(s => !s.classList.contains('w-mod'));
      if (!bad.length) ok++;
      const t = (tr.textContent||'').trim();
      if (/spngaw|qnadi/i.test(t))
        hits.push({hw: hw, t: t, n: sp.length,
                   bad: bad.map(s => s.textContent.trim()+'|'+s.className)});
    });
  });
  return {tot: tot, ok: ok, hits: hits, seen: seen, unv: unv,
          green: green, greens: greens}; }"""

FLOOR = 5329
DENOM = 5429
GREEN = 2

# rendered form -> the reason the pallor is correct
REFUSED = {
    # --- batch 216, carried forward -------------------------------------
    "lgluq": "gluq carries his 樹脂 verbatim but has no onset; his L never "
             "deletes -- lbagan->rbagan, lb'nao->rbnaw, lb'lak->lblak",
    "pggu": "his own parenthetical pairs it with pgago, whose map value pgagu "
            "is 笛子; following a frozen dark value spreads the freeze",
    "kakuh": "木屐 returns 0 in all five gloss files; ramil is 拖鞋",
    "kkakuh": "木屐 returns 0 in all five gloss files; ramil is 拖鞋",
    "kahui": "妓/娼 return 0; the sense sits on mngeangal 淫亂 and sgsapat 姦淫, "
             "different roots",
    "mkahui": "妓/娼 return 0; the sense sits on mngeangal 淫亂 and sgsapat 姦淫, "
              "different roots",
    "kndutu": "every 手鐲 hit is the sirug root, the verb to wear, off a "
              "different root",
    "ayuq": "the only 腺 hits are biqir 甲狀腺腫瘤, a disease not a gland; ayug "
            "小溪/山谷 is the shape-trap the pallor keeps him off",
    "graqun": "graqil/grqilun are the 賤價 root; the word that fits the sentence "
              "is qrapun, which is his own separate K'LAP card",
    "shmqan": "his GMALYEQ card is headed 詞根不明; 監獄/監牢 return 0 and the "
              "sole 牢 hit hmkan is a verb off another root",
    "mtrgri": "tlgl and trgr are both empty in attested_modern.json",
    "tgrgri": "tlgl and trgr are both empty in attested_modern.json",
    "pnnanu": "nanu and nano are both empty in attested_modern.json",
    "pklluyun": "qluy and pqluy are both empty in attested_modern.json",
    "sm": "his DALING example reads `Miyax ko sm(?) sunan` -- the (?) is HIS",

    # --- batch 217, the LIKUT family ------------------------------------
    # His LIKUT is 藉口－詭計. The register puts 詭計 on rnqdug and 欺騙 on
    # qdug -- a different root, so there is no respelling of his to find and
    # the pallor is the correct record (the batch-204 meaning test).
    "rikut": "his LIKUT 藉口－詭計; 詭計 sits on rnqdug and 欺騙 on qdug, a "
             "different root",
    "krikut": "off his LIKUT 藉口－詭計; the 詭計 root is rnqdug, not his",
    "nrikut": "off his LIKUT 藉口－詭計; the 詭計 root is rnqdug, not his",
    "nprikut": "off his LIKUT 藉口－詭計; the 詭計 root is rnqdug, not his",
    "tnrikut": "off his LIKUT 藉口－詭計; the 詭計 root is rnqdug, not his",

    # --- batch 217, the BASYAQ family -----------------------------------
    # His BASYAQ is 暴飲暴食. Modern 貪吃 sits on hadur, msqnaniq and dmhiqur,
    # three roots and none of them his.
    "tbasyaq": "his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, "
               "all different roots",
    "tibasyaq": "his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, "
                "all different roots",
    "dmbasyaq": "his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, "
                "all different roots",
    "dmtbasyaq": "his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, "
                 "all different roots",

    # --- batch 217, seven neighbours ------------------------------------
    # Each was tested by asking what the neighbouring slots say, and each
    # neighbour turned out to be a different word. A card head dark for the
    # wrong reason licenses nothing beside it (batch 199).
    "qloq": "the neighbours qloqon and qloqi are unglossed, so the card offers "
            "nothing to read the slot against",
    "sdangan": "his DYAX is 日; the three sdang- neighbours are sdanga 用…餵, "
               "sdangar 石板陷阱 and sdangi 愛人 -- three unrelated roots",
    "hlakuh": "his card is 盾牌; hlak is 肉片 and hlaka 展翅, neither a shield",
    "knhgun": "his card is 下坡; knhgut is 減退 and knhghug 水井",
    "qlap": "his card is 品嚐－親吻; the only qlap- gloss is qlapan 不能生育的女人",
    "thiy": "his Txey sits on the XNUK 軟／便宜 card, not on TOXOI; thiyan "
            "和…在一起 is TOXOI's word and following it would cross two cards",
    "prngut": "confirms batch 204's RNGUT refusal: his 使受孕 against prngutan "
              "有掛鉤 and prngatay 禮儀",
    "pnrngut": "off his RNGUT 使受孕; the prngut- neighbours are 有掛鉤/禮儀",
    "rmngut": "off his RNGUT 使受孕; the prngut- neighbours are 有掛鉤/禮儀",
    "rngutan": "off his RNGUT 使受孕; the prngut- neighbours are 有掛鉤/禮儀",

    # --- batch 217, the sister sweep's one live hit ----------------------
    # The spngaw finding generalises: a pale word whose SISTERS are verified
    # but which scores level 0 itself is the fingerprint of an analyser gap.
    # Run over all 174 pale values it returns five, and four are traps already
    # refused in writing -- qadi and qnadi are the -i leg refused above,
    # tbiyi and tbiyun are batch 199's six-wrong-words-in-one-ruling beside
    # tbiyan 下來. sapi is the only one that had not been read, and it is a
    # refusal too, so the seam is closed with no ruling in it.
    "sapi": "his SAPE is 小鋤頭; the sister sapaw is 舖（舖床、舖葉等）, and the "
            "modern word for a small hoe is parih (43 spk) -- a different "
            "root, so there is no respelling of his to find",
}


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def read_ver():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((k, int(n))
                for k, n in re.findall(r'^  "(.+?)": (\d+),?$', t, re.M))


def main():
    fails = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("http://127.0.0.1:8765/")
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL)
        pg.wait_for_timeout(WAIT)
        r = pg.evaluate(JS)
        b.close()

    print("rows with spans: %d   all-dark: %d   %.4f%%"
          % (r["tot"], r["ok"], 100.0 * r["ok"] / DENOM))
    if r["tot"] != DENOM:
        fails.append("denominator moved: %d rows carry spans, expected %d"
                     % (r["tot"], DENOM))
    if r["ok"] < FLOOR:
        fails.append("deliverable pairs FELL to %d, floor is %d"
                     % (r["ok"], FLOOR))

    M, V = read_map(), read_ver()
    seen, unv = r["seen"], r["unv"]

    # 1 — the ruling
    if M.get("spngao") != "spngaw":
        fails.append("map spngao -> %s. Batch 217 ruled it spngaw, the "
                     "hortative of the listed spngi, after finding roots() "
                     "could not strip -aw at all." % M.get("spngao"))
    if V.get("spngaw") != 6:
        fails.append("spngaw is verified %s, batch 217 built it to code 6 "
                     "(no_chinese: a regular inflection of a listed root for "
                     "which he wrote no gloss as a word)." % V.get("spngaw"))

    # 2 — it must be DARK on the page, twice: his sentence repeats it in the vl.
    if seen.get("spngaw", 0) < 2:
        fails.append("spngaw renders %d time(s), expected 2 -- his sentence "
                     "carries it in the vl. as well as in the main clause"
                     % seen.get("spngaw", 0))
    if unv.get("spngaw"):
        fails.append("spngaw is pale again (%d of %d spans). The ruling rests "
                     "on the -aw restoration branch in roots(); if that was "
                     "reverted the ledger must name the batch."
                     % (unv["spngaw"], seen.get("spngaw", 0)))

    # 3 — the row it cleared
    srows = [h for h in r["hits"]
             if re.search(r"(?<![a-z])spngaw(?![a-z])", h["t"], re.I)]
    print("rows carrying spngaw: %d (floor 1)" % len(srows))
    if not srows:
        fails.append("no rendered row carries spngaw; the ruling cleared the "
                     "SM\"LU row `Spngao ta otoç`")
    for h in srows:
        if h["bad"]:
            fails.append("the spngaw row is not all dark: %r %s"
                         % (h["t"][:44], h["bad"][:3]))

    # 4 — the leg that was REFUSED. qnadi must stay pale: it is q<n>adi off his
    # own QADI 編織物, and the -i restoration would root it on qnada 已丟棄的
    # through no_chinese(), the rung that skips the gloss test.
    if "qnadi" not in seen:
        fails.append("qnadi no longer renders. It is the pin on the refused "
                     "-i leg of the batch-217 restoration branch.")
    elif "qnadi" not in unv:
        fails.append("qnadi is DARK. Batch 217 refused the -i leg of the "
                     "vowel restoration precisely because it verifies this "
                     "word off qnada 已丟棄的, a different root one final "
                     "vowel away, while his card is QADI 格子架、編織物.")

    # 5 — every refusal still pale, read off the DOM and not off REFUSED. Keys
    # are RENDERED forms; a key matching nothing passes vacuously (batch 215's
    # slangan bug), so absence is itself a failure.
    for word, why in sorted(REFUSED.items()):
        if word not in seen:
            fails.append("%s no longer renders anywhere on the page. It was "
                         "refused because %s -- if the transcription or the "
                         "map changed, the refusal needs re-arguing, not "
                         "deleting." % (word, why))
        elif word not in unv:
            fails.append("%s renders %d time(s) and NONE is pale. It was "
                         "refused because %s" % (word, seen[word], why))

    # 6 — green
    print("green spans: %d %s" % (r["green"], sorted(r["greens"])))
    if r["green"] != GREEN:
        fails.append("green moved to %d spans, batch 217 measured %d (%s). "
                     "Green means no map entry fired; a rise is a generator "
                     "regression, a fall wants a ledger row."
                     % (r["green"], GREEN, sorted(r["greens"])))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
