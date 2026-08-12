# -*- coding: utf-8 -*-
"""Harvest the blocked sentence pairs for the translator page.

Two renders of the same page, paired by the GLOBAL index of the `.truku` box:
modern (which carries the colours) and his own 1977 spelling (which is the
record). Order is stable across a toggle because the app re-renders the same
cards in the same order — asserted by comparing the box counts and the French
gloss of every paired row, not assumed.

Writes .scratch/b235/blocked.json. Prints a summary line only.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
OUT = os.path.join(H, ".scratch", "b243", "blocked.json")
URL = "http://127.0.0.1:8765/index.html"

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  // The box's text with every NOT-dark span delimited. Rebuilt from the node
  // tree rather than from textContent so the mark keeps its place in the
  // sentence: a span can hold two words and a hyphenated word two spans, so
  // there is no string operation that finds it afterwards.
  const marked = (box) => {
    let s = '';
    const walk = (n) => {
      if (n.nodeType === 3) { s += n.nodeValue; return; }
      if (n.nodeType !== 1) return;
      if (n.matches(SEL) && !n.classList.contains('w-mod')) {
        s += '⟦' + n.textContent + '⟧'; return;
      }
      n.childNodes.forEach(walk);
    };
    walk(box);
    return s.replace(/🔊/g, '').trim();
  };
  const out = [];
  let i = 0, ci = -1;
  document.querySelectorAll('#results > article.entry').forEach(c => {
    ci++;
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    c.querySelectorAll('.truku').forEach(box => {
      const sp = [...box.querySelectorAll(SEL)];
      if (!sp.length) return;
      const idx = i++;
      const wrap = box.parentElement;
      const g = {};
      (wrap ? [...wrap.querySelectorAll('.ex-gloss, .gloss')] : []).forEach(p => {
        const chip = p.querySelector('.lang-chip');
        if (!chip) return;
        const k = (chip.className.match(/lang-chip (\w+)/)||[])[1];
        g[k] = (p.textContent||'').replace(/^(FR|EN|中)/, '').trim();
      });
      out.push({i: idx, c: ci, hw: hw, mark: marked(box),
                text: (box.textContent||'').trim(),
                spans: sp.map(s => [(s.textContent||'').trim(),
                                    s.className]),
                fr: g.fr || '', en: g.en || '', zh: g.zh || ''});
    });
  });
  return out;
}"""

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    got = {}
    for mode in ("modern", "orig"):
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','%s')"
                    % mode)
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        got[mode] = pg.evaluate(JS)
    b.close()

MOD, ORIG = got["modern"], got["orig"]
assert len(MOD) == len(ORIG), "box counts differ: %d vs %d" % (len(MOD),
                                                               len(ORIG))


def shape(s):
    """a French gloss with every latin letter removed. `glossCites` colours the
    Truku names INSIDE a French gloss, so `Ingay`/`Ingai` and `Rabay`/`Labai`
    differ between the two renders while the sentence does not (64 rows). What
    survives -- punctuation, spacing, digits, Chinese -- does not, so this
    catches a real misalignment while ignoring the respelling. His two elision
    marks come out with the letters: a French gloss citing `Knta"to` renders it
    `Knteetu`, so a `"` inside a WORD is part of the spelling, not punctuation
    (2 rows)."""
    return re.sub(r"[A-Za-zÀ-ÿ'\"’ʼ]+", "", s or "")


mismatch = [(m, o) for m, o in zip(MOD, ORIG)
            if shape(m["fr"]) != shape(o["fr"])]
for m, o in mismatch:
    print("MISMATCH i=%d %s\n  mod  %s\n  orig %s\n  frM  %s\n  frO  %s"
          % (m["i"], m["hw"], m["text"][:60], o["text"][:60],
             m["fr"][:60], o["fr"][:60]))
assert not mismatch, "%d rows paired to a different gloss" % len(mismatch)
# The card ORDINAL, not the card label: `.hw` prints the modernised headword,
# so two adjacent cards sharing one modern spelling merge in one pass and not
# in the other. That is a fact about the label, not about the alignment.
assert [r["c"] for r in MOD] == [r["c"] for r in ORIG], (
    "the two passes assign boxes to cards differently: the pairing is by "
    "position and this is what would make that unsafe")

rows = []
for m, o in zip(MOD, ORIG):
    pale = sorted(set(t.lower() for t, c in m["spans"]
                      if "w-mod" not in c.split()))
    if not pale:
        continue
    # HIS token behind each pale value, taken from the DOM rather than by
    # reversing the map: `spellClass()` keys on his token and is
    # mode-independent, so span k of the orig render is the same token as span
    # k of the modern one. The exception is real and has to be checked, not
    # assumed — `linkifyTruku` runs `joinClitics(collapseInline(...))` in modern
    # mode ONLY, so a box where a clitic joined has one span fewer there.
    same = len(m["spans"]) == len(o["spans"])
    rows.append({"hw": m["hw"], "orig": o["mark"], "mod": m["mark"],
                 "spans": m["spans"], "his": o["spans"], "aligned": same,
                 "pale": pale,
                 "fr": m["fr"], "en": m["en"], "zh": m["zh"]})

io.open(OUT, "w", encoding="utf-8").write(
    json.dumps(rows, ensure_ascii=False, indent=1))
n1 = sum(1 for r in rows if len(r["pale"]) == 1)
print("boxes %d | blocked %d (sole %d, two %d, 3+ %d) | clitic-shifted %d -> %s"
      % (len(MOD), len(rows), n1,
         sum(1 for r in rows if len(r["pale"]) == 2),
         sum(1 for r in rows if len(r["pale"]) > 2),
         sum(1 for r in rows if not r["aligned"]),
         os.path.relpath(OUT, H)))
