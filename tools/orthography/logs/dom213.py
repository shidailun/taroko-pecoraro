# -*- coding: utf-8 -*-
"""batch 213 — his TQELI paradigm, a refusal, and a `kn` read as `m`.

Three rulings, and the pins they earned.

### 1. The TQELI card — 圍繞 — three pairs

`tqliyan`, `tnqliyan`, `tqliyun`, `ptqliyun` were all pale on one card. The
register does not list his `l` shapes, but `inf.sistered('tqriyun')` returns
`('', 'tqri', 'yun', ['tqrian', 'tqrii'])` — the wordlist writes his stem with
two OTHER slots of the same paradigm, which is the sister-slot instrument, and
it spells the stem `tqri`. The parquets then carried his sense, which the
register's lone 裝填 row does not:

    tgska tqrian dgiyaq …          四周群山圍繞…
    tqrian dha tluung ka pratu paru  圍住其鉢盤坐著

— "a single gloss row is not the register's answer; the family is" (batch 200).

`tqliyan → tqrian` and `tnqliyan → tnqrian` were already code 1, so they
darkened on arrival. `tqliyun → tqriun` drops the epenthetic `y` that neither
`tqrian` nor `tqrii` writes; `sistered()` reaches the shorter shape with the
same two sisters, so the change costs no colour. `ptqliyun → ptqriun` needed
`HAND_RULED`.

**The near miss, pinned here.** The register lists `ptqiun` (spoken 2), which
would have auto-darkened as code 1 — and it has no `r`, is glossed 放置；安放,
and its one utterance is about putting something into a basket. Taking it would
have frozen his 雞舍圍起來 sentence onto an unrelated word: dark and wrong,
invisible to every colour metric. The gloss-matched value is the Bible
glossary's `ptqriun` 使繞行；巡行.

### 2. TMAGO 驕傲 — refused

`mtmago → mtmagu`, pale, spoken 0. Both slots of the two-slot card are pale, so
the paradigm instrument has nothing to say; unattested in register, parquet,
Bible and e-dictionary; and the meaning is carried by DIFFERENT roots — `dahu`
自誇、自傲 26 and `psparu` 驕傲 30. That is batch 204's shape: a different
attested word spells the sense, so there is no respelling to find and the pallor
is correct. Not a settled class either — 驕傲 is everyday speech. An
edit-distance sweep found no rival reading, so the scan question never opens.

### 3. NII — a `kn` transcribed as `m`

His NII card read `Mniyax so smuwan ? ... Snii bi !` 你什麼時候來的？ — and
`smuwan` is not a word in any source. Batch 208's shape, so the scan ran first:
at 8× the glyph is unambiguously `k` + `n`, ascender and diagonal legs. The page
reads **`sknuwan`**, which his own book spells four other times (S, SADYAQ,
SÜEQ, XDIL), every one glossed 什麼時候 — the sense of this very sentence. So
the fix is a transcription correction in `entries.js` and `batch_202_205.json`,
NOT a map entry (batch 212's rule about where a fix goes), and the word darkened
for free: already in the map as an identity, code 1, spoken 16.

The row's audio id was re-minted with it — `ex_mniyax_so_smuwan_snii_bi` →
`ex_mniyax_so_sknuwan_snii_bi`. That orphans one clip URL, which is the correct
trade: the take on disk voices a non-word.

Asserted here:
  1. all five TKURI rows render the `tqri` stem with every span dark
  2. the `ptqriun` row and the QIRI card's `Tqriun su na ka pais` are dark
  3. no row anywhere renders a `tql-` shape or the old `tqriyun`
  4. the map still sends the four tokens to the ruled values, and `ptqliyun`
     does NOT go to the register's `ptqiun` 放置 — the near miss
  5. the NII row renders `sknuwan` all dark; `entries.js` spells `smuwan`
     nowhere and `sknuwan` five times
  6. `mtmagu` is still pale. This is the refusal, held as a measurement: if it
     darkens, someone found evidence and this pin must be retired in writing.
  7. the pair metric floor, 5320 of 5429 (a floor, never equality — batch 209)
"""
import io
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE))), "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 15000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const hits = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    c.querySelectorAll('.example').forEach(x => {
      const tr = x.querySelector('.truku'); if (!tr) return;
      const sp = [...tr.querySelectorAll(SEL)]; if (!sp.length) return;
      tot++;
      const bad = sp.filter(s => !s.classList.contains('w-mod'));
      if (!bad.length) ok++;
      const t = (tr.textContent||'').trim();
      if (/tqri|tql|tqliy|sknuwan|smuwan|tmagu/i.test(t))
        hits.push({hw: hw, t: t, n: sp.length,
                   bad: bad.map(s => s.textContent.trim()+'|'+s.className)});
    });
  });
  return {tot: tot, ok: ok, hits: hits}; }"""

FLOOR = 5320
DENOM = 5429

# token -> the value ruled in this batch
RULED = {
    "tqliyan": "tqrian",
    "tnqliyan": "tnqrian",
    "tqliyun": "tqriun",
    "ptqliyun": "ptqriun",
}


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    body = t[a:t.index("\n};", a) + 2]
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$', body, re.M))


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
        fails.append("deliverable pairs FELL to %d, floor is %d" % (r["ok"], FLOOR))

    # 1 + 2 — every row the TQELI ruling touches
    tq = [h for h in r["hits"] if re.search(r"tqri", h["t"], re.I)]
    print("rows rendering the tqri stem: %d (floor 6)" % len(tq))
    if len(tq) < 6:
        fails.append("only %d rows render a tqri value; the ruling reached 6 "
                     "(5 on TKURI, the ptqriun row, the QIRI pais row)" % len(tq))
    for h in tq:
        if h["bad"]:
            fails.append("a tqri row is not all dark: %r %s"
                         % (h["t"][:44], h["bad"][:3]))
    pais = [h for h in tq if "pais" in h["t"]]
    ptq = [h for h in tq if re.search(r"(?<![a-z])ptqriun(?![a-z])", h["t"], re.I)]
    print("  QIRI pais row: %d   ptqriun row: %d" % (len(pais), len(ptq)))
    if not pais:
        fails.append("the QIRI card's `Tqriun su na ka pais` no longer renders "
                     "the tqri stem")
    if not ptq:
        fails.append("the 雞舍 row no longer renders ptqriun — check it did not "
                     "drift to the register's ptqiun 放置, the near miss")

    # 3 — nothing survives of the old shapes
    stale = [h for h in r["hits"]
             if re.search(r"(?<![a-z])p?t(?:n)?qliy?[au]n(?![a-z])|tqriyun",
                          h["t"], re.I)]
    print("rows still rendering a tql-/tqriyun shape: %d (expected 0)" % len(stale))
    for h in stale:
        fails.append("%s still renders an unruled shape: %r" % (h["hw"], h["t"][:44]))

    # 4 — the map itself, so a drift to a third spelling still fails
    M = read_map()
    for k, v in sorted(RULED.items()):
        got = M.get(k, "-")
        print("  map %-10s -> %-9s (want %s)" % (k, got, v))
        if got != v:
            fails.append("map %s -> %s, batch 213 ruled %s" % (k, got, v))
    if M.get("ptqliyun") == "ptqiun":
        fails.append("ptqliyun took the register's ptqiun 放置；安放 — the near "
                     "miss. It has no r and its one utterance is about a basket; "
                     "his sentence is 雞舍圍起來.")

    # 5 — the NII transcription, in the source and on the page
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
    sm = kn = 0
    for e in E:
        for x in (e.get("examples", []) +
                  [y for sb in e.get("subs", []) for y in sb.get("examples", [])]):
            t = x.get("t") or ""
            sm += len(re.findall(r"(?<![a-z])smuwan(?![a-z])", t, re.I))
            kn += len(re.findall(r"(?<![a-z])sknuwan(?![a-z])", t, re.I))
    print("entries.js: smuwan %d (expected 0)   sknuwan %d (expected 5)" % (sm, kn))
    if sm:
        fails.append("entries.js spells smuwan %d time(s) — the scan reads k+n "
                     "at 8x and his book spells sknuwan four other times" % sm)
    if kn < 5:
        fails.append("entries.js spells sknuwan only %d time(s); the four he "
                     "already had plus the NII correction make 5" % kn)
    nii = [h for h in r["hits"] if re.search(r"sknuwan|smuwan", h["t"], re.I)
           and "Snii" in h["t"]]
    print("the NII row: %d" % len(nii))
    if len(nii) != 1:
        fails.append("expected 1 NII sknuwan row, found %d" % len(nii))
    for h in nii:
        print("  § %s" % h["t"][:64])
        print("    spans %d   not dark: %s" % (h["n"], h["bad"] or "none"))
        if "sknuwan" not in h["t"]:
            fails.append("the NII row does not render sknuwan: %r" % h["t"][:44])
        if h["bad"]:
            fails.append("the NII row has non-dark spans %s" % h["bad"][:3])

    # 6 — the TMAGO refusal, held as a measurement
    tm = [h for h in r["hits"] if re.search(r"tmagu", h["t"], re.I)]
    pale = [h for h in tm if any("tmagu" in x.lower() for x in h["bad"])]
    print("TMAGU rows: %d   still pale: %d (expected >=1)" % (len(tm), len(pale)))
    if tm and not pale:
        fails.append("mtmagu darkened. Batch 213 refused it: unattested "
                     "everywhere, and 驕傲 is carried by dahu / psparu, "
                     "different roots. If evidence arrived, retire this pin in "
                     "writing — do not delete the assertion.")

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
