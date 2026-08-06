# -*- coding: utf-8 -*-
"""[batch 223] The pale that lives only on his card furniture.

Batch 222 found that a `.truku`-scoped probe sees 87 pale span types where the
book has 159. The missing ~72 are on his HEADWORDS, his SUB-FORM names and his
PARADIGM slots, which render in `.hw` / `.sub-form` / `.paradigm` and are inside
no `.truku` box at all.

Every ranking instrument this project has built is `.truku`-scoped, because they
were all written to serve the pair metric. So this set has never been ranked by
anything. That is not the same as never having been WORKED -- batch 199's slot
cards and batch 216's identity pins both live here -- which is why the last
column greps the record before anyone spends a batch on a name already refused
in writing (batch 221: the cheapest cut on any tail, one command).

These words cannot move the metric directly: the denominator is example rows,
and a headword is not one. They are worth ranking for the reason batch 199 gives
-- a pale slot beside dark ones is the cheapest question on the page, and a root
ruled here licenses the forms of it that DO appear in his sentences.

    python tools/orthography/logs/furniture.py     # site served at :8765
"""
import io
import os
import re
import subprocess
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const scoped = {}, all = {}, where = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    c.querySelectorAll(SEL).forEach(s => {
      if (!s.classList.contains('w-unv')) return;
      const t = (s.textContent||'').trim().toLowerCase();
      all[t] = (all[t] || 0) + 1;
      const host = s.closest('.truku') ? 'truku'
                 : s.closest('.paradigm') ? 'paradigm'
                 : s.closest('.sub-form') ? 'sub-form'
                 : s.closest('.hw') ? 'hw'
                 // name the container rather than binning it as 'other' --
                 // a crossref and a slot card are different questions
                 : (s.parentElement.className || s.parentElement.tagName)
                     .split(' ')[0] || 'other';
      (where[t] = where[t] || {})[host] = (where[t][host] || 0) + 1;
      if (!where[t].card) where[t].card = hw;
    });
    // batch 199's shape: how many slots on THIS card are already DARK? A pale
    // slot beside dark ones is a question his paradigm can answer. A pale slot
    // on an all-pale card has no sibling to reason from and is not cheap --
    // batch 221's SA'MUL was refused partly for exactly that reason.
    let dark = 0, palen = 0;
    c.querySelectorAll(SEL).forEach(s => {
      if (s.closest('.truku')) return;              // furniture only
      if (s.classList.contains('w-unv')) palen++; else dark++; });
    c.querySelectorAll(SEL).forEach(s => {
      if (s.closest('.truku') || !s.classList.contains('w-unv')) return;
      const t = (s.textContent||'').trim().toLowerCase();
      const e = where[t];
      if (e.dark === undefined || dark > e.dark) { e.dark = dark; e.pale = palen; }
    });
    c.querySelectorAll('.truku').forEach(b => b.querySelectorAll(SEL)
      .forEach(s => { if (s.classList.contains('w-unv'))
        { const t = (s.textContent||'').trim().toLowerCase();
          scoped[t] = (scoped[t] || 0) + 1; } }));
  });
  return {scoped: scoped, all: all, where: where}; }"""


def mentioned(word, card=""):
    """batch 221's cheapest cut: has the record already priced this word?

    Grep HIS CARD as well as the value. The record argues about cards by his own
    headword and about roots by the root, while this ranking reports inflected
    map VALUES -- so `ptbiyan`, `ptbiyi` and `ptbiyun` came back "-- NONE --"
    from a card CLAUDE.md refuses by name, because the refusal is written
    against `tbiyan` and SAKUR. An exact-string grep over a ranking of inflected
    forms under-reports the record and manufactures fresh candidates.
    """
    keys = [word] + [k for k in re.findall(r"[A-Za-z'\"]+", card) if len(k) > 2]
    hits = []
    for path in [os.path.join(ROOT, ".claude", "notes", "batch-log.md")] + \
                sorted(os.path.join(HERE, f) for f in os.listdir(HERE)
                       if re.match(r"dom\d+\.py$", f)):
        try:
            t = io.open(path, encoding="utf-8").read()
        except Exception:
            continue
        # word boundaries, or `ihur` matches inside `bgihur` and a FRESH
        # candidate is hidden behind a mention that is not about it
        for k in keys:
            if re.search(r"(?i)(?<![a-z'\"])%s(?![a-z'\"])" % re.escape(k), t):
                hits.append(os.path.basename(path))
                break
    return hits


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("http://127.0.0.1:8765/")
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL)
        pg.wait_for_timeout(WAIT)
        r = pg.evaluate(JS)
        b.close()

    scoped, allp, where = r["scoped"], r["all"], r["where"]
    only = {w: n for w, n in allp.items() if w not in scoped}
    print("pale types: scoped %d, book-wide %d, furniture-only %d"
          % (len(scoped), len(allp), len(only)))

    rows = sorted(only.items(), key=lambda kv: (-kv[1], kv[0]))
    META = ("card", "dark", "pale")
    print("\n%-13s %3s  %-15s %-18s %-8s %s"
          % ("pale value", "n", "renders in", "on his card", "drk/pal",
             "prior mentions"))
    fresh = 0
    for w, n in rows[:40]:
        h = where.get(w, {})
        hosts = " ".join("%s:%d" % (k, v) for k, v in sorted(h.items())
                         if k not in META)
        m = mentioned(w, h.get("card") or "")
        if not m:
            fresh += 1
        print("%-13s %3d  %-15s %-18s %3d/%-4d %s"
              % (w, n, hosts[:15], (h.get("card") or "")[:18],
                 h.get("dark", 0), h.get("pale", 0),
                 ",".join(m[:2]) if m else "-- NONE --"))
    print("\n%d of the top %d have no prior mention in the record"
          % (fresh, min(40, len(rows))))

    # the only thing this seam can be worth: batch 199's cheap question
    cheap = [(w, where[w]) for w, _ in rows
             if where[w].get("dark", 0) >= 3
             and not mentioned(w, where[w].get("card") or "")]
    print("%d furniture-pale values sit on a card with 3+ DARK slots and have "
          "no prior mention -- batch 199's shape" % len(cheap))
    for w, h in cheap[:16]:
        print("   %-13s %-20s dark %2d, pale %d"
              % (w, (h.get("card") or "")[:20], h["dark"], h["pale"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
