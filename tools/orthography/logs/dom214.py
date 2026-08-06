# -*- coding: utf-8 -*-
"""batch 214 — SOLA, GBIYAN, and five refusals; the metric crosses 98%.

Two rulings, one root-correction that deliberately stays pale, five refusals.

### `snola → sneura` — a slot of a paradigm the card already renders

The map had an IDENTITY claim, `snola → snola`, which blocks `charRules()` and
looks like a verdict. His book has the card: SOLA 羨慕（無惡意）－想要, sub
`Smola`, and the map already sends it to the modern SEURA paradigm — `sola →
seura`, `smola → smeura`, five dark slots. `sneura` is in `attested_modern`, so
it darkened as code 1 and both pairs cleared.

The near miss: `sura` 想要;期望 is listed, matches his head-gloss as well as
`seura` does, and the char rules produce `snura` unaided. The family refuses it —
five dark slots all spell `-eura`.

### `kmbyanan → knegbiyan` — his own control, one line up

`Knbyanan` 傍晚(夜幕已垂之時) is a sub-form on the same card, already mapped to
`knegbiyan` 已經傍晚, code 1. The example spells the same word `Kmbyanan`, and on
page 92 the two sit on **one typewritten line** with `étant` and `tombé` between
them as controls. Three stems: he typed `m`. Faithful transcription, so the fix
goes in the map (batch 212), and `entries.js` keeps his letter.

### `sl'xqon` → `shkun` — right root, still pale, on purpose

`srhqun` was raw char-rule fallback, and his own head is SHIK (SL'XEQ) with
`sml'xeq → smhik` 在吻 already ruled code 1. `srhqun` lands one letter from
`srhqul` 諷刺 — the shape a freeze arrives in. Repointed to the `-un` slot of
`shik`; NOT hand-ruled, because the register has no suffixed form of this root
and its one parallel argues the other way (`hdhik` → `hdhikan`, vowel kept). The
pallor is the honest state of a settled root with an unsettled vowel.

### Refused, with the reason each pin must keep re-asserting

  * `gaqat` — `gakat` 起身;站立 shares the shape only, and he uses the token in
    a SECOND sense (`Tdoloi gakat (gaqat)` 腳踏車), so one key cannot serve both.
  * `gnlqan` — his `Gnloq` 入鞘 is off LOQ 洞, but the map sends the family to
    the grease root (`gluq` 污垢, `gnluq` 用過防銹油). Dark on the OTHER sense,
    so it licenses nothing (batch 204). Recorded as an unfixed freeze.
  * `loai` — `rahuq` 除了這些還有… carries it off a different root.
  * `qadi` — 編織 is `cinun`, 網子 is `rahug`; only `qada` 丟掉 shares the shape.
  * `ptatwi` — the register has a construction, not a word: `speangal` 用比喻.

Asserted here:
  1. both SOLA rows render `sneura` with every span dark, and the SEURA card's
     five slots are still dark — one value serves them all
  2. `snola` no longer maps to itself; an identity claim returning is the news
  3. both `kmbyanan` rows render `knegbiyan` all dark, and `entries.js` still
     spells `Kmbyanan` twice — the scan is the record
  4. `sl'xqon` and `slx'qon` both map to `shkun` and neither renders `srhqun`
  5. the five refused words are still pale, each with its reason restated
  6. the pair metric floor, 5324 of 5429 (a floor, never equality — batch 209)
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
      if (/eura|snola|gbiyan|byanan|shkun|srhqun|gaqat|gakat|gnlqan|loai|qadi|ptatuy|ptatwi/i.test(t))
        hits.push({hw: hw, t: t, n: sp.length,
                   bad: bad.map(s => s.textContent.trim()+'|'+s.className)});
    });
  });
  return {tot: tot, ok: ok, hits: hits}; }"""

FLOOR = 5324
DENOM = 5429

# the five refusals: rendered form -> the reason the pallor is correct
REFUSED = {
    "gaqat": "gakat 起身;站立 shares the shape only, and his Tdoloi gakat (gaqat) "
             "腳踏車 is a second sense under the same key",
    "gnlqan": "his Gnloq 入鞘 is off LOQ 洞; the map's family value is the grease "
              "root, dark on the OTHER sense",
    "loai": "rahuq 除了這些還有… carries it off a different root",
    "qadi": "編織 is cinun, 網子 is rahug; only qada 丟掉 shares the shape",
    "ptatuy": "the register has a construction, not a word: speangal 用比喻",
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

    M = read_map()

    # 1 + 2 — the SOLA ruling
    sn = [h for h in r["hits"]
          if re.search(r"(?<![a-z])sneura(?![a-z])", h["t"], re.I)]
    print("rows rendering sneura: %d (expected 2)" % len(sn))
    if len(sn) != 2:
        fails.append("expected 2 sneura rows (LALA and LUUS), found %d" % len(sn))
    for h in sn:
        print("  § %s" % h["t"][:60])
        print("    spans %d   not dark: %s" % (h["n"], h["bad"] or "none"))
        if h["bad"]:
            fails.append("a sneura row is not all dark: %s" % h["bad"][:3])
    fam = [h for h in r["hits"] if re.search(r"(?<![a-z])s?m?n?e?seura|smeura|"
                                             r"(?<![a-z])seura(?![a-z])",
                                             h["t"], re.I)]
    print("rows on the SEURA family: %d (floor 5)" % len(fam))
    if len(fam) < 5:
        fails.append("the SEURA family renders %d rows; the entry was written "
                     "beside five dark slots" % len(fam))
    if M.get("snola") == "snola":
        fails.append("snola is an identity claim again. That tier blocks "
                     "charRules() and hid a dark paradigm for 213 batches; "
                     "the value is sneura, attested, code 1.")
    if M.get("snola") != "sneura":
        fails.append("map snola -> %s, batch 214 ruled sneura" % M.get("snola"))
    if M.get("snola") == "snura":
        fails.append("snola took the char-rule value snura off sura 想要;期望. "
                     "The family spells -eura in all five dark slots.")

    # 3 — GBIYAN
    kb = [h for h in r["hits"]
          if re.search(r"(?<![a-z])knegbiyan(?![a-z])", h["t"], re.I)]
    print("rows rendering knegbiyan: %d (floor 2)" % len(kb))
    if len(kb) < 2:
        fails.append("only %d rows render knegbiyan; the GBIYAN and PLIYAX "
                     "examples both take it" % len(kb))
    for h in kb:
        if h["bad"]:
            fails.append("a knegbiyan row is not all dark: %r %s"
                         % (h["t"][:40], h["bad"][:3]))
    if M.get("kmbyanan") != "knegbiyan":
        fails.append("map kmbyanan -> %s, batch 214 ruled knegbiyan"
                     % M.get("kmbyanan"))

    # 4 — the root correction that stays pale
    for k in ("sl'xqon", "slx'qon"):
        if M.get(k) != "shkun":
            fails.append("map %s -> %s, batch 214 repointed it to shkun, the "
                         "-un slot of shik 吻. srhqun was the wrong root and "
                         "sits one letter from srhqul 諷刺." % (k, M.get(k)))
    if [h for h in r["hits"] if re.search(r"(?<![a-z])srhqun(?![a-z])",
                                          h["t"], re.I)]:
        fails.append("a row still renders srhqun — the char-rule reading his own "
                     "SHIK (SL'XEQ) head contradicts")

    # 5 — the refusals, each still pale, each reason restated
    src = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    E = json.loads(src[src.index("["):src.rindex("]") + 1])
    kmb = 0
    for e in E:
        for x in (e.get("examples", []) +
                  [y for sb in e.get("subs", []) for y in sb.get("examples", [])]):
            kmb += len(re.findall(r"(?<![a-z])Kmbyanan(?![a-z])",
                                  x.get("t") or ""))
    print("entries.js rows spelling Kmbyanan: %d (expected 2)" % kmb)
    if kmb != 2:
        fails.append("the source was emended: %d rows read Kmbyanan, expected 2. "
                     "Page 92 has three stems beside his own Knbyanan on the "
                     "same line — his spelling is the record." % kmb)

    for w, why in sorted(REFUSED.items()):
        rows = [h for h in r["hits"]
                if any(re.match(r"^%s\|" % w, b, re.I) for b in h["bad"])]
        print("  refused %-8s still pale in %d row(s)" % (w, len(rows)))
        if not rows:
            fails.append("%s is no longer pale. Batch 214 refused it: %s. If "
                         "evidence arrived, retire this pin in writing — do not "
                         "delete the assertion." % (w, why))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
