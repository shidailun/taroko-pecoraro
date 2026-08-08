# -*- coding: utf-8 -*-
"""Where do the 15 never-asked pale map values actually RENDER? (batch 234)

Ten of them are FRENCH -- `grand`, `savoir`, `cunnaissance` (char rules on
*connaissance*) -- so the question is not what to spell them but whether they
are spans at all. The map is never evidence about colour; only the DOM is
(batch 219). Prints verdicts, not cards.
"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
URL = "http://127.0.0.1:8765/index.html"
WANT = ["beau", "cunnaissance", "grand", "grandeur", "knbuyu", "macin",
        "mqlaq", "puur", "rngiyan", "ruugeur", "savoir", "shkun", "smul",
        "vivant", "volant"]

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    d = pg.evaluate(r"""(want) => {
      const SEL = 'span.w-mod, span.w-unv, span.w-raw';
      const W = new Set(want);
      const hits = {}, sole = {}, pale = {};
      let tot = 0, ok = 0;
      document.querySelectorAll('#results > article.entry').forEach(c => {
        const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
        c.querySelectorAll('.truku').forEach(box => {
          const sp = [...box.querySelectorAll(SEL)];
          if (!sp.length) return;
          tot++;
          if (sp.every(s => s.classList.contains('w-mod'))) ok++;
          else {
            const bad = [...new Set(sp.filter(s => !s.classList.contains('w-mod'))
                           .map(s => (s.textContent||'').trim().toLowerCase()))];
            if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
          }
        });
        c.querySelectorAll(SEL).forEach(s => {
          const t = (s.textContent || '').trim().toLowerCase();
          const cls = s.className.trim();
          if (!cls.split(/\s+/).includes('w-mod'))
            pale[t] = (pale[t] || 0) + 1;
          if (!W.has(t)) return;
          // which box is it in? walk up for the nearest named container.
          let host = 'other', n = s;
          while (n && n !== c) {
            const k = n.className || '';
            for (const c2 of ['truku', 'gloss', 'paradigm', 'hw', 'sub-form',
                              'tag', 'example', 'meta-abbr'])
              if ((' ' + k + ' ').includes(' ' + c2 + ' ')) { host = c2; n = c; break; }
            if (n === c) break;
            n = n.parentElement;
          }
          (hits[t] = hits[t] || []).push([hw, cls, host]);
        });
      });
      return {hits: hits, sole: sole, pale: pale, tot: tot, ok: ok};
    }""", WANT)
    b.close()

print("PAIRS %d / %d   pale span types (unscoped) %d   sole-blocker types %d"
      % (d["ok"], d["tot"], len(d["pale"]), len(d["sole"])))
print("\n15 never-asked pale map values, as the DOM has them:")
for w in WANT:
    rows = d["hits"].get(w) or []
    if not rows:
        print("  %-13s renders NOWHERE" % w)
        continue
    cls = sorted(set(r[1] for r in rows))
    host = sorted(set(r[2] for r in rows))
    cards = sorted(set(r[0] for r in rows))
    print("  %-13s %2d span(s)  %-24s in %-22s on %s"
          % (w, len(rows), "/".join(cls)[:24], "/".join(host)[:22],
             ", ".join(cards)[:34]))
    if w in d["sole"]:
        print("  %-13s   ... and is a SOLE blocker of %d pair(s)" % ("", d["sole"][w]))

json.dump(d, io.open(".scratch/b234/dom.json", "w", encoding="utf-8"),
          ensure_ascii=False)
print("\nsole blockers written to .scratch/b234/dom.json")
