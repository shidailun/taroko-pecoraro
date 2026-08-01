# -*- coding: utf-8 -*-
"""Both-mode census + the batch-131 words in the DOM.

The gain list is six words, and the REFUSED list is again the load-bearing half:
`sghuwayan` is the whole reason the gate was built and must be PALE, `tntmaan` is
pinned, and `sklbai` is a claim this batch RETRACTS — it was verified in 130 and
has to go back to pale, because its only witness was a bogus `klba`+`yun` reading
of `klbayun`, which is really `klbay` 成…軟弱 + `un`.

`sqaan` is in the watch list for the opposite reason: the ungated glide family
re-cut it off `siqa` 害羞, his own gloss-agreeing word, onto a bare sister list.
The gate refuses `sqawi` (the root ends in a), so the better analysis survives —
it must still be dark, and by the same route as before.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
GAIN = ["psrngiyan", "sndngiyan", "sbuan", "pktngiyan", "pkrui", "qriyun"]
HELD = ["slui", "bkii", "sqaan"]
REFUSED = ["sklbai", "tntmaan", "sghuwayan"]
WATCH = GAIN + HELD + REFUSED

with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        c = {k: pg.evaluate('()=>document.querySelectorAll("span.%s").length' % k)
             for k in ("w-mod", "w-unv", "w-raw")}
        cards = pg.evaluate('()=>document.querySelectorAll("article.entry").length')
        t = sum(c.values())
        print("%-9s %s  total %d  dark %.4f%%  cards %d  errors %d"
              % (mode, c, t, 100.0 * c["w-mod"] / t, cards, len(errs)))
        if mode == "modern":
            seen = pg.evaluate(SPANS, WATCH)
        ctx.close()
    b.close()

for name, ws in (("newly verified", GAIN),
                 ("held dark through the re-cut", HELD),
                 ("REFUSED by this batch — must be PALE", REFUSED)):
    print("\n-- %s" % name)
    for w in ws:
        print("   %-11s %s" % (w, seen.get(w) or "absent"))
