# -*- coding: utf-8 -*-
"""Type and token coverage, in BOTH scopes.

`seen` is EVERY span, so DARK = seen - unv - raw (batch 232). The pallor
question is book-wide and the PAIR metric is `.truku`-scoped (batch 222), so
both are collected in one pass. The probe walks the `.truku` boxes rather than
prefixing a comma-separated selector (batch 216), and folds case because `.hw`
prints the modern headword UPPERCASE (batch 226).

A TYPE here is a distinct rendered span string, not one of his tokens: one span
can hold two words and one hyphenated word can hold two spans (batch 208).
"""
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const A = {seen: {}, unv: {}, raw: {}};        // book-wide
  const T = {seen: {}, unv: {}, raw: {}};        // scoped to .truku
  const bump = (d, k, t) => { d[k][t] = (d[k][t] || 0) + 1; };
  const tally = (d, s) => {
    const t = (s.textContent || '').trim().toLowerCase();
    if (!t) return;
    bump(d, 'seen', t);
    if (s.classList.contains('w-unv')) bump(d, 'unv', t);
    if (s.classList.contains('w-raw')) bump(d, 'raw', t);
  };
  document.querySelectorAll('#results > article.entry').forEach(c => {
    c.querySelectorAll(SEL).forEach(s => tally(A, s));
    c.querySelectorAll('.truku').forEach(box =>
      box.querySelectorAll(SEL).forEach(s => tally(T, s)));
  });
  return {A: A, T: T}; }"""


def report(name, d):
    seen, unv, raw = d["seen"], d["unv"], d["raw"]
    tok = sum(seen.values())
    ptok, gtok = sum(unv.values()), sum(raw.values())
    dtok = tok - ptok - gtok
    typ = len(seen)
    # a type is DARK only if it renders dark everywhere it renders
    pty = len(set(unv))
    gty = len(set(raw))
    dty = len(set(seen) - set(unv) - set(raw))
    print("%s" % name)
    print("  tokens (spans)  %6d   dark %6d = %7.4f%%   pale %4d   green %d"
          % (tok, dtok, 100.0 * dtok / tok, ptok, gtok))
    print("  types           %6d   dark %6d = %7.4f%%   pale %4d   green %d"
          % (typ, dty, 100.0 * dty / typ, pty, gty))
    mixed = sorted(set(unv) & (set(seen) - set(unv)))
    print("  types rendering BOTH dark and pale somewhere: %d" % len(
        [t for t in unv if seen[t] > unv[t] + raw.get(t, 0)]))


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    # Force modern spelling and settle as dom232 does. Without this the page
    # renders HIS 1977 spelling: the colour classes are identical but the span
    # TEXT is his, so a type census counts 7,407 types instead of 6,472 and the
    # pale figures disagree with dom232 by 2 spans / 3 types. The mode is the
    # variable, not the keying (`pctdiff.py` holds the keying and reproduces
    # dom232 exactly).
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL)
    pg.wait_for_timeout(WAIT)
    r = pg.evaluate(JS)
    b.close()

report("BOOK-WIDE (his card furniture included)", r["A"])
report("SCOPED to .truku (the pair metric's own scope)", r["T"])
