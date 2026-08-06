# -*- coding: utf-8 -*-
"""batch 212 — his Q'NAO belly word, and why the scan did NOT settle it.

`mbuyan` was the sole blocker of one pair, on his Q'NAO 大蒜 card:

    Tai ka mqan bi q'nao o , ongat xali bisol mbuyan na ole
    常吃大蒜的人肚子裡不常有蛔蟲。

It has batch 208's shape — a transcription slip landing one letter from a word
the register lists — so the mandatory check ran first: crop the glyph with a
known `s` (`bisol`, same line) at 7× and count. **The page reads `mbuyan`.** The
`n` has two stems and an arch; his `s` is nothing like it. So the transcription
is faithful, `entries.js` keeps `mbuyan`, and the question went back to the
language — which is the point of asking the scan first, and the first time that
check has come back NO.

What decided it was his own book, not the register:

  * his KUI card writes the same referent in the same frame —
    `Bisol, ksun ta o, kika kui mbuyas` 我們所稱的 Bisol，就是肚子裡的蟲
  * his BUYAS 肚子——腹 card carries the note （常聽作 MBUYAS）, and he cards
    MBUYAS 肚子 separately
  * `mbuyas → nbuyas` was already in the map: attested, spoken 13, glossed 肚子
  * the Q'NAO gloss is his own 肚子

and the register has no `buyan` of any shape — the whole `buy-` family is
babuy 豬 / bbuyu 打獵 / buyak 肢解. So the map takes `mbuyan → nbuyas`: a
display-time respelling, which is what the map is for, and NOT an emendation.
The source keeps his letter; the reader gets the word he meant.

Asserted here:
  1. the Q'NAO row renders `nbuyas` with every span dark
  2. no row anywhere renders `embuyan`, and no pale span carries `buyan`
  3. his KUI witness and the BUYAS family still render `nbuyas` — one value
     serves them all, so the entry darkened a pair without splitting anything
  4. `entries.js` still reads `mbuyan`. The scan is the record; if a later hand
     "fixes" the source, this fails and says why.
  5. the pair metric floor, 5316 of 5429 (a floor, never equality — batch 209)
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
      if (/nbuyas|buyan/i.test(t))
        hits.push({hw: hw, t: t, n: sp.length,
                   bad: bad.map(s => s.textContent.trim()+'|'+s.className)});
    });
  });
  return {tot: tot, ok: ok, hits: hits}; }"""

FLOOR = 5316
DENOM = 5429


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

    # 1 + 2 — the Q'NAO row, and no survivor of the old value anywhere
    qnao = [h for h in r["hits"] if "qusul" in h["t"] and "bisur" in h["t"]]
    print("Q'NAO rows: %d" % len(qnao))
    if len(qnao) != 1:
        fails.append("expected 1 Q'NAO belly row, found %d" % len(qnao))
    for h in qnao:
        print("  § %s" % h["t"][:64])
        print("    spans %d   not dark: %s" % (h["n"], h["bad"] or "none"))
        if "nbuyas" not in h["t"]:
            fails.append("the Q'NAO row does not render nbuyas: %r" % h["t"][:40])
        if h["bad"]:
            fails.append("the Q'NAO row has non-dark spans %s" % h["bad"][:3])

    # `tnbuyan` 有蔭之處 is off his BUYO 草叢 card, a different root, and stays.
    # What must not survive is the old value of HIS belly token.
    stale = [h for h in r["hits"]
             if re.search(r"(?<![a-z])(?:em|m)?buyan(?![a-z])", h["t"], re.I)]
    print("rows still rendering the old *buyan value: %d (expected 0)" % len(stale))
    for h in stale:
        fails.append("%s still renders a buyan value: %r" % (h["hw"], h["t"][:40]))

    # 3 — the witness and the family the value already served
    fam = [h for h in r["hits"] if "nbuyas" in h["t"]]
    kui = [h for h in fam if "ksun ta" in h["t"]]
    print("rows rendering nbuyas: %d   his KUI witness among them: %d"
          % (len(fam), len(kui)))
    if len(fam) < 2:
        fails.append("nbuyas serves %d rows; it served more before the entry"
                     % len(fam))
    if not kui:
        fails.append("his KUI witness (Bisol, ksun ta o, kika kui mbuyas) no "
                     "longer renders nbuyas — the entry split the value")

    # 4 — the source keeps his letter
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
    src = 0
    for e in E:
        for x in (e.get("examples", []) +
                  [y for sb in e.get("subs", []) for y in sb.get("examples", [])]):
            if re.search(r"\bmbuyan\b", x.get("t") or "", re.I):
                src += 1
    print("entries.js rows still spelling mbuyan: %d (expected 1)" % src)
    if src != 1:
        fails.append("the source was emended: %d rows read mbuyan, expected 1. "
                     "The scan reads n — his spelling is the record, and the "
                     "respelling belongs in the map." % src)

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
