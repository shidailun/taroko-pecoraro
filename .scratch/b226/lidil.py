# -*- coding: utf-8 -*-
"""Which LIDIL card is dom66's new failure on, and what does it actually paint?

The suite's one regression is `BROWN lidil rijig missing on [LIDIL]`. He carded
LIDIL twice; batch 211 split the homograph (`rijig` 柄 for the handle, `rijil`
使彎曲 for the bend) and put the bend value in CITE_SPELL, which fires only where
a form renders as a NAME. So the prediction is: the bend card paints `rijil`
PALE on its headword and no `rijig` anywhere. Confirm from the DOM, not the map.
"""
import io, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
t = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(t[t.index("["):t.rindex("]") + 1])
IDX = [i for i, e in enumerate(E) if (e.get("hw") or "").upper() == "LIDIL"]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(22000)
    dom = pg.evaluate("""() => Array.from(
        document.querySelectorAll('article.entry')).map(a => {
        const cls = s => s.className.indexOf('w-raw') >= 0 ? 'green'
                       : s.className.indexOf('w-unv') >= 0 ? 'PALE' : 'dark';
        return Array.from(a.querySelectorAll('.w-mod, .w-unv, .w-raw'))
                    .map(s => cls(s) + ':' + s.textContent.trim());
    })""")
    b.close()

print("cards rendered %d, entries %d" % (len(dom), len(E)))
for i in IDX:
    zh = (E[i].get("zh") or "")[:14]
    ws = dom[i]
    hit = [w for w in ws if "rijil" in w or "rijig" in w]
    print("\ncard %d  %s  subs=%d ex=%d" % (i, zh, len(E[i].get("subs", [])),
                                            len(E[i].get("examples", []))))
    print("  rijil/rijig spans: %s" % (hit or "NONE"))
    print("  spans on card: %d" % len(ws))
