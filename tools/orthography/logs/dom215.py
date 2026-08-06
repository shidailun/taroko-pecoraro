# -*- coding: utf-8 -*-
"""batch 215 — `rih` off a two-batch pin, a freeze his own family convicted,
and a refusal argued from his orthography instead of from the register.

### `lex` → `rih` — retiring a pin batch 146 set and batch 162 restated

Both refusals named the same blocker: length-as-chance over one ASR hapax plus
`krih`, an onomatopoeion. `derived('rih')` returns twelve supporters, and they
are the WRONG family — `marih` 嘔氣, `embrih` 會…代價, six unglossed. The right
family is reduplicated and therefore invisible to the analyser (`inf.roots()`
has no rule for CC-): `ririh` 取代 14, `mririh` 取代者 35, `pririh` 還 17,
`rrihan` 被取代 4, `empririh` 賠償 4. Five of his own LILEX forms are already
dark on five of them, and `ririh tama` 叔叔 stands beside his `Lex mo tama`
"(= mon oncle)". Six inflections in four affix shapes is not chance. 3 pairs.

### `ngali` — the first citation seam a FAMILY convicted

His NGALI (R) 剩餘 head rendered `ngali` 拿走；拿取, 27 speakers: dark AND wrong.
The gloss row alone would only have raised the question; what answered it was the
four children he wrote under the head, each already mapped to the other letter
and each gloss-verified there — `nngali`→`nngari` 剩餘的, `sngali`→`sngari` 剩餘,
`msngali`→`msngari` 剩下, `psngali`→`psngari`. A family that already agrees
convicts a head that keeps its own letters.

Fixed at the citation seam, not in the map, because all five running-text renders
are the 拿取 sense and correct as they stand. Seven of seven renders checked, not
sampled. The hook still only REFUSES: `ngari` is in the omnibus but never a map
value, so `build_verified.py` never emits it and `darkClass` pales it. The head
goes from dark-and-wrong to honestly pale and no sentence moves.

**What it does not reach**, recorded so nobody reads it as an oversight: five
gloss-internal references to NGALI (four on SNGARI, one on NGARI) still render
dark, because they take the linkified path where `noLink` is false. Widening the
hook there would reach the five 拿取 sentences too.

### LANGI — investigated, ACQUITTED, and the reason is worth keeping

`langi → rangi` looks exactly like the `ngali` freeze: his cards read 呆滯 and
剩下的, and the register row for `rangi` reads 不遵守習俗（犯忌）. The family
answers it — `srangi` 剩餘 (`srangi laqi rbnaw ka dnuuy`) and `msrangi` 剩菜／剩飯,
eight utterances, against his `Mslangi` "les reliefs d'un repas" 剩菜 verbatim.
A single gloss row is not the register's answer (batch 200), and the same
instrument that convicted `ngali` acquits `langi`. Do not re-run this.

### `slangan` 鏽 — refused from HIS ORTHOGRAPHY, a test this project had not used

The register's rust word is `sgrangan` 生銹, off the 45-member `girang` family
(`skringan` 生鏽 is its k/g variant and a rootless isolate). His gloss matches it
exactly, which is normally enough to look for a respelling. His own hand refuses
one: across 398 pages he never writes a `gr` cluster — the only two hits in the
book are the French *grand* and *grandeur* — and the correspondence he DOES use
for modern `gr` is `gl`/`g'l`, in 81 map values (`glangan → grangan`, `g'laq →
graq`, `dglil → dgril`). He had the shape and used it elsewhere. What his `sl'`
regularly renders is modern `sr` (`sl'ngao → srngaw`, `slamal → sramal`). So
`sgrangan` would have been `sglangan` in his hand, a cluster his book does not
contain, and his SLANGAN is regularly `srangan`, which no source lists. Different
root; nothing to respell; the pallor is correct (batch 204's meaning test).

The scan was asked first (batch 202): page 282 at 1.5× reads `SLANGAN` double-
underlined, with `mpslangan` in his own example. No rival reading.

### The other refusals

  * `ksudan` — his card is `(R. = ?)` with no head gloss; the modern shuttle is
    `gikus` (register 做梭者／製作梭, parquet `tklihug muda brah ka gikus`), a
    different root. 0 corpus hits, no shape candidate. 3 pairs.
  * `tbilan` — his TBILAN head gloss is literally `？？`; only `Lukus tbilan`
    節慶服飾 with his own `(vl. lukus pspingan)`. No register word for 盛裝／禮服,
    0 corpus, no shape candidate. 3 pairs.
  * `lngiyan` — his `Lngiyan` 剩下來的東西 has no attested modern counterpart;
    the register carries the meaning on `nngari` 剩餘的 / `nengari` 剩下的, which
    is his OTHER card's root, and merging two cards he kept apart is not licensed.
    The identity claim came off anyway: his four siblings all render `-rngiy-`
    (`psrngiyan`, `psrngiyun`, `srngiyun`, `pnsrngiyan`), so `rngiyan` is the
    consistent value. Pale before, pale after — a consistency fix, not a claim.

Asserted here:
  1. `lex → rih` and `rih` verified code 1; `lilex → ririh` still code 1
  2. the LEX/LILEX rows render with every span dark
  3. `ngali`'s headword renders `ngari` and is PALE, and all five running-text
     `ngali` renders are still dark — the seam, in both directions
  4. `langi → rangi` still stands, with `srangi`/`msrangi` still dark under it —
     the acquittal is asserted, not just written down
  5. the orthographic correspondence the `slangan` refusal rests on: no `sgl`
     key, no `sl*` key mapping to `sgr*`, and the `gl`→`gr` class populated
  6. each refused word still pale, each reason restated
  7. the pair metric floor, 5327 of 5429 (a floor, never equality — batch 209)
"""
import io
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SITE = os.path.join(ROOT, "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 15000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const hits = [], words = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent||'').trim().toLowerCase();
      if (/^(ngali|ngari|rih|ririh|rngiyan|srangi|msrangi|rangi)$/.test(t))
        words.push({hw: hw, w: s.textContent.trim(), cls: s.className,
                    ex: !!s.closest('.example')});
    });
    c.querySelectorAll('.example').forEach(x => {
      const tr = x.querySelector('.truku'); if (!tr) return;
      const sp = [...tr.querySelectorAll(SEL)]; if (!sp.length) return;
      tot++;
      const bad = sp.filter(s => !s.classList.contains('w-mod'));
      if (!bad.length) ok++;
      const t = (tr.textContent||'').trim();
      if (/rih|ngari|ngali|rngiyan|ksudan|tbiran|slangan|srangan|sgrangan/i.test(t))
        hits.push({hw: hw, t: t, n: sp.length,
                   bad: bad.map(s => s.textContent.trim()+'|'+s.className)});
    });
  });
  return {tot: tot, ok: ok, hits: hits, words: words}; }"""

FLOOR = 5327
DENOM = 5429

# rendered form -> the reason the pallor is correct
REFUSED = {
    "ksudan": "his card is (R. = ?) with no head gloss; the modern shuttle is "
              "gikus, a different root, and there is no shape candidate",
    "tbiran": "his TBILAN head gloss is literally ？？; no register word for "
              "盛裝/禮服, 0 corpus, no shape candidate",
    # keyed on the rendered form, which is his BMBANG sentence's `mslangan` --
    # the bare head never reaches running text, and its own card renders
    # `empslangan`. A key of `slangan` finds nothing and passes vacuously.
    "mslangan": "he never writes a gr cluster in 398 pages and uses gl/g'l for "
                "modern gr, so sgrangan 生銹 would have been sglangan in his hand",
    "rngiyan": "no attested modern counterpart; the register carries 剩下來的東西 "
               "on nngari/nengari, which is his separate NGALI card's root",
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

    # 1 + 2 — the rih ruling
    if M.get("lex") != "rih":
        fails.append("map lex -> %s, batch 215 ruled rih off the reduplicated "
                     "paradigm the analyser cannot see (ririh 取代, mririh "
                     "取代者, pririh, rrihan, empririh)" % M.get("lex"))
    if V.get("rih") != 1:
        fails.append("rih is verified %s, batch 215 hand-ruled it to 1. Two "
                     "pins named length-as-chance; six inflections in four "
                     "affix shapes retired them." % V.get("rih"))
    if M.get("lilex") != "ririh" or V.get("ririh") != 1:
        fails.append("lilex -> %s (ver %s); the LILEX card is the family that "
                     "carried the ruling" % (M.get("lilex"), V.get("ririh")))
    rih_rows = [h for h in r["hits"]
                if re.search(r"(?<![a-z])r?ri?rih[a-z]*(?![a-z])", h["t"], re.I)]
    print("rows on the rih family: %d (floor 3)" % len(rih_rows))
    if len(rih_rows) < 3:
        fails.append("the rih family renders %d rows; the ruling cleared 3 "
                     "sole-blocked pairs" % len(rih_rows))
    for h in rih_rows:
        if h["bad"]:
            fails.append("a rih row is not all dark: %r %s"
                         % (h["t"][:40], h["bad"][:3]))

    # 3 — the ngali citation seam, in both directions
    heads = [w for w in r["words"]
             if not w["ex"] and w["w"].lower() in ("ngali", "ngari")]
    pale_head = [w for w in heads
                 if w["w"].lower() == "ngari" and "w-unv" in w["cls"]]
    print("citation renders of ngali/ngari: %d   pale ngari heads: %d"
          % (len(heads), len(pale_head)))
    if not pale_head:
        fails.append("no citation render of his NGALI head reads a pale ngari. "
                     "CITE_SPELL['ngali'] = 'ngari' is what takes the head off "
                     "ngali 拿走；拿取 (27 speakers), which is dark AND wrong on "
                     "a card glossed 剩餘. If the hook went, the freeze is back.")
    if any("w-mod" in w["cls"] for w in heads if w["w"].lower() == "ngari"):
        fails.append("a citation ngari rendered DARK. The hook may only refuse "
                     "(batch 202) — build_verified.py must not emit ngari.")
    run = [w for w in r["words"] if w["ex"] and w["w"].lower() == "ngali"]
    print("running-text renders of ngali: %d (floor 5, all dark)" % len(run))
    if len(run) < 5:
        fails.append("only %d running-text ngali renders; all five are the 拿取 "
                     "sense and the seam depends on them staying" % len(run))
    for w in run:
        if "w-mod" not in w["cls"]:
            fails.append("a running-text ngali went pale (%s on [%s]). The hook "
                         "must not reach running text." % (w["cls"], w["hw"]))
    if M.get("ngali") != "ngali":
        fails.append("map ngali -> %s. Batch 215 fixed this at the citation "
                     "seam, NOT in the map, because five sentences need the "
                     "map's value." % M.get("ngali"))

    # 4 — the LANGI acquittal, asserted rather than merely written down
    if M.get("langi") != "rangi":
        fails.append("map langi -> %s. Batch 215 investigated this as a freeze "
                     "and ACQUITTED it: srangi 剩餘 and msrangi 剩菜/剩飯 (8 "
                     "utterances) answer the 犯忌 row, and his Mslangi is 'les "
                     "reliefs d'un repas' verbatim." % M.get("langi"))
    for k, v in (("slangi", "srangi"), ("mslangi", "msrangi")):
        if M.get(k) != v or V.get(v) != 1:
            fails.append("%s -> %s (ver %s); these two ARE the acquittal of "
                         "langi -> rangi" % (k, M.get(k), V.get(M.get(k))))

    # 5 — the orthographic correspondence the slangan refusal rests on
    gr = [(k, v) for k, v in M.items()
          if "gr" in v and k not in ("grand", "grandeur")]
    sgl = [k for k in M if "sgl" in k]
    slsgr = [(k, v) for k, v in M.items()
             if k.startswith("sl") and v.startswith("sgr")]
    print("map values carrying a modern gr: %d   his sgl keys: %d   sl->sgr: %d"
          % (len(gr), len(sgl), len(slsgr)))
    if len(gr) < 60:
        fails.append("only %d map values carry a modern gr; the slangan refusal "
                     "rests on gl/g'l being his populated correspondence for it"
                     % len(gr))
    if sgl:
        fails.append("his book now has an sgl cluster (%s). The slangan refusal "
                     "said sgrangan would have been sglangan in his hand and "
                     "that his book contains no such shape — re-price it."
                     % sgl[:3])
    if slsgr:
        fails.append("an sl* key now maps to sgr* (%s), which is the crossing "
                     "the slangan refusal said does not occur" % slsgr[:3])
    if not [1 for k, v in M.items() if k.startswith("sl'") and v.startswith("sr")]:
        fails.append("no sl' -> sr mapping left; that class is what makes his "
                     "SLANGAN regularly srangan, which no source lists")

    # 6 — the refusals, each still pale, each reason restated
    for w, why in sorted(REFUSED.items()):
        rows = [h for h in r["hits"]
                if any(re.match(r"^%s\|" % w, b, re.I) for b in h["bad"])]
        pale = rows or [x for x in r["words"]
                        if x["w"].lower() == w and "w-unv" in x["cls"]]
        print("  refused %-9s still pale in %d row(s)" % (w, len(pale)))
        if not pale:
            fails.append("%s is no longer pale. Batch 215 refused it: %s. If "
                         "evidence arrived, retire this pin in writing — do not "
                         "delete the assertion." % (w, why))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
