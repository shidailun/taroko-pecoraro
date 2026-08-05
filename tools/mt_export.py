# -*- coding: utf-8 -*-
"""Regenerate exports/ — the MT hand-off files.

Taken from the RENDERED PAGE, never from the maps. Colour is the confidence
signal and it is only real in the DOM: `WORD_OVERRIDES` and `CITE_SPELL` live in
app.js and are invisible to `modern_map.js`, so anything that asks a table
instead of the page gets a different answer.

Two passes over the whole dictionary — modern spelling for the tokens and their
colour, original spelling for `truku_pecoraro` — zipped by DOM order, which is
deterministic for one query. They are NOT token-aligned with each other: modern
mode joins proclitics he spaced (`A sao` -> `Asaw`), so the two spellings of one
sentence have different token counts. The `tokens` array describes the modern
string only.

Usage:  python tools/mt_export.py [--port 8765]
"""
import sys, os, json, collections, argparse
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "exports")
CENSUS = "?q=%CC%81"          # matches a combining acute: every card in the book
WAIT = 30000

HARVEST = r"""() => {
  const clean = el => {
    const c = el.cloneNode(true);
    c.querySelectorAll('button').forEach(b => b.remove());
    return c.textContent.replace(/\s+/g, ' ').trim();
  };
  const out = [];
  for (const e of document.querySelectorAll('#results .example')) {
    const card = e.closest('article.entry');
    const tk = [...e.querySelectorAll('.w-mod,.w-unv,.w-raw')].map(s => ({
      w: s.textContent,
      c: s.classList.contains('w-mod') ? 'd'
       : s.classList.contains('w-unv') ? 'p' : 'g'
    }));
    const g = {};
    for (const p of e.querySelectorAll('.ex-gloss')) {
      const chip = p.querySelector('.lang-chip');
      if (!chip) continue;
      const k = chip.className.replace('lang-chip', '').trim();
      g[k] = p.textContent.slice(chip.textContent.length).trim();
    }
    out.push({
      hw: ((card && card.querySelector('.hw')) || {}).textContent || '',
      truku: clean(e.querySelector('.truku')),
      tokens: tk, fr: g.fr || '', en: g.en || '', zh: g.zh || ''
    });
  }
  return out;
}"""


def harvest(pw, port, modern):
    br = pw.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')"
        % ("modern" if modern else "original"))
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:%d/%s" % (port, CENSUS))
    pg.wait_for_timeout(WAIT)
    cards = pg.evaluate(
        "document.querySelectorAll('#results > article.entry').length")
    rows = pg.evaluate(HARVEST)
    br.close()
    return cards, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()

    with sync_playwright() as pw:
        ncards, mod = harvest(pw, a.port, True)
        ncards2, orig = harvest(pw, a.port, False)

    assert ncards == ncards2 == 1967, (ncards, ncards2)
    assert len(mod) == len(orig), (len(mod), len(orig))
    print("cards %d   examples %d" % (ncards, len(mod)))

    # A row whose Truku field is his French demonstration has no spans at all --
    # six of them, his AN (3) circumfix card and kin. They are not pairs and they
    # were inflating the metric; excluded from the denominator, kept in the
    # record with truku_spans = 0.
    recs, nz = [], 0
    for i, (m, o) in enumerate(zip(mod, orig)):
        bad_p = sorted({t["w"].lower() for t in m["tokens"] if t["c"] == "p"})
        bad_g = sorted({t["w"].lower() for t in m["tokens"] if t["c"] == "g"})
        spans = len(m["tokens"])
        if not spans:
            nz += 1
        recs.append({
            "i": i, "hw": m["hw"].strip(),
            "deliverable": bool(spans) and not bad_p and not bad_g,
            "truku_spans": spans,
            "truku_modern": m["truku"], "truku_pecoraro": o["truku"],
            "fr": m["fr"], "en": m["en"], "zh": m["zh"],
            "unconfirmed": bad_p, "unmapped": bad_g,
            "tokens": m["tokens"],
        })

    denom = len(recs) - nz
    deliv = [r for r in recs if r["deliverable"]]
    print("denominator %d (%d French-in-Truku rows excluded)   deliverable %d = %.4f%%"
          % (denom, nz, len(deliv), 100.0 * len(deliv) / denom))

    with open(os.path.join(OUT, "mt_sentences.jsonl"), "w",
              encoding="utf-8", newline="\n") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(os.path.join(OUT, "mt_deliverable.tsv"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("truku\tzh\ten\tfr\theadword\n")
        for r in deliv:
            f.write("\t".join(x.replace("\t", " ") for x in
                    (r["truku_modern"], r["zh"], r["en"], r["fr"], r["hw"])) + "\n")

    # Word types over EXAMPLE tokens only -- this list exists to explain the
    # sentence files, so a headword-only word does not belong in it.
    occ, indel, st = collections.Counter(), collections.Counter(), {}
    for r in recs:
        for t in r["tokens"]:
            w = t["w"].lower()
            occ[w] += 1
            st[w] = {"d": "confirmed", "p": "unconfirmed", "g": "unmapped"}[t["c"]]
            if r["deliverable"]:
                indel[w] += 1
    with open(os.path.join(OUT, "mt_wordlist.tsv"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("modern\tstatus\toccurrences\tin_deliverable_sentences\n")
        for w in sorted(occ):
            f.write("%s\t%s\t%d\t%d\n" % (w, st[w], occ[w], indel[w]))
    print("types %d   wrote 3 files to exports/" % len(occ))

    blocked = [r for r in recs if r["truku_spans"] and not r["deliverable"]]
    sole = collections.Counter()
    for r in blocked:
        b = set(r["unconfirmed"]) | set(r["unmapped"])
        if len(b) == 1:
            sole[next(iter(b))] += 1
    print("blocked %d   of which by a single type %d"
          % (len(blocked), sum(sole.values())))


if __name__ == "__main__":
    main()
