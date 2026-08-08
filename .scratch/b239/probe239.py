# -*- coding: utf-8 -*-
"""Before/after probe for batch 239 — the qbolong freeze.

Prints the summary line only (the lean-context rule): pair metric, book-wide
pale TYPE count, and the colour of every span whose text is one of the watched
values. Scoped both ways in one pass (batch 222): the pair metric is
`.truku`-scoped, the pallor census is book-wide.

    python .scratch/b239/probe239.py before
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
URL = "http://127.0.0.1:8765/index.html"
WATCH = ["qburung", "qbolong", "qbulung", "kbowlung", "qbrungan", "qbrungi"]


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "run"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        d = pg.evaluate(r"""(W) => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          const w = {}, pale = {};
          let tot = 0, ok = 0;
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
            });
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              const k = s.classList.contains('w-mod') ? 'dark'
                      : (s.classList.contains('w-unv') ? 'pale' : 'green');
              if (k === 'pale') pale[t] = (pale[t] || 0) + 1;
              if (W.indexOf(t) < 0) return;
              w[t] = w[t] || {dark: 0, pale: 0, green: 0, inTruku: 0};
              w[t][k]++;
              if (s.closest('.truku')) w[t].inTruku++;
            });
          });
          return {tot: tot, ok: ok, w: w, pale: Object.keys(pale).length};
        }""", WATCH)
        b.close()

    print("[%s] pairs %d/%d (%.4f%%)  pale types %d"
          % (label, d["ok"], d["tot"], 100.0 * d["ok"] / max(1, d["tot"]),
             d["pale"]))
    for k in WATCH:
        v = d["w"].get(k)
        if v:
            print("    %-10s dark %d pale %d green %d  inTruku %d"
                  % (k, v["dark"], v["pale"], v["green"], v["inTruku"]))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "probe_%s.json" % label), "w") as fh:
        json.dump(d, fh, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
