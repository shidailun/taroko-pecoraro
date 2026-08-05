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
import sys, os, re, json, collections, argparse
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

WORD = re.compile(r"[^\W\d_]+(?:['’\"][^\W\d_]+)*", re.UNICODE)


def pieces(s):
    """Comparable word pieces: hyphens split, elision marks do not, case folded."""
    return [w.lower() for w in WORD.findall((s or "").replace("-", " "))]


PAREN = re.compile(r"\s*\(([^)]*)\)")


def strip_variants(s):
    """Drop a bracketed Truku variant from the TRAINING string only.

    Removing `vl.` and `var.` leaves the citation they introduced standing —
    `Biyuq qhuni (var. qhuni)` became `Biyuq qhuni (qhuni)` — and 295 of the
    5,315 deliverable rows still carried one. They are apparatus: an alternative
    form (`Snpi (mnspi) ku sunan`), an equivalence (`Mha su inu ki (=baki)?`),
    or a fuller phrasing (`Ssbusun mu idaw ka kiya (Spsbusun mu idaw ka kiya)`).
    Checked against the glosses on a sample: the French and English translate
    the sentence WITHOUT the bracket every time, so shipping it makes the source
    say something the target does not — a misaligned pair, not a richer one.
    The French's own parentheses are synonyms and live in the gloss field, which
    this never touches.

    `truku_modern` keeps the brackets; his record is not edited, only the string
    offered for training. Unbalanced brackets (his page-break damage) do not
    match and are left alone, and a bracket that IS the whole sentence is kept
    rather than deleted to nothing.
    """
    out = PAREN.sub("", s or "")
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out if WORD.search(out) else s

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
  // The training string is the sentence WITHOUT the apparatus. The page already
  // knows which is which: `.meta-abbr` is his editorial note (`vl.`, and the
  // French asides he sets in brackets), `.w-orig` is the superseded word shown
  // beside its modern replacement. Harvesting textContent shipped both as Truku.
  const train = el => {
    const c = el.cloneNode(true);
    c.querySelectorAll('button, .meta-abbr, .w-orig').forEach(b => b.remove());
    return c.textContent
      .replace(/\s+/g, ' ')
      .replace(/\(\s*[.,:;!?\s]*\)/g, '')     // brackets emptied by the strip
      .replace(/\(\s*[.,:;]\s*/g, '(')        // "(vl. x)" -> "(x)"
      .replace(/\s+\)/g, ')')
      .replace(/\s+([,.;:!?])/g, '$1')
      .replace(/\s+/g, ' ').trim();
  };
  const out = [];
  for (const e of document.querySelectorAll('#results .example')) {
    const card = e.closest('article.entry');
    // Scoped to `.truku`. The app respells inside the glosses too — a name in
    // the French renders as a word span like any other — so an unscoped query
    // counts 700 gloss spans in 256 rows as sentence tokens, and a pale name in
    // the FRENCH can block a row whose Truku is entirely dark.
    const tk = [...e.querySelectorAll('.truku .w-mod,.truku .w-unv,.truku .w-raw')].map(s => ({
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
      train: train(e.querySelector('.truku')),
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
    residue = collections.Counter()
    for i, (m, o) in enumerate(zip(mod, orig)):
        m["train"] = strip_variants(m["train"])
        bad_p = sorted({t["w"].lower() for t in m["tokens"] if t["c"] == "p"})
        bad_g = sorted({t["w"].lower() for t in m["tokens"] if t["c"] == "g"})
        spans = len(m["tokens"])
        if not spans:
            nz += 1
        # Anything in the training string that carried no span at all. After the
        # apparatus strip this should be empty; a non-empty residue is a token
        # the page rendered as running Truku without colouring it, which no
        # colour metric can see. Reported, never silently shipped.
        #
        # Both sides are broken to PIECES first, because a span and a word are
        # not the same unit in either direction: one span can hold two words
        # (his `Mpaso` renders `Empaa su`, the clitic join) and one hyphenated
        # word can hold two spans (`Empa-laqi`). Comparing them whole reported
        # thirteen rows, every one of them coloured — a detector that cries wolf
        # will hide the real hit it exists to catch.
        # A spanless row is already counted and excluded by `nz`; letting its
        # every word through here would report the same six French demonstration
        # lines a second time under a name that means something else.
        left = collections.Counter(pieces(m["train"])) if spans else \
            collections.Counter()
        left -= collections.Counter(p for t in m["tokens"] for p in pieces(t["w"]))
        left = sorted(w for w in left.elements() if len(w) > 1)
        residue.update(left)
        recs.append({
            "i": i, "hw": m["hw"].strip(),
            "deliverable": bool(spans) and not bad_p and not bad_g,
            "truku_spans": spans,
            "truku_train": m["train"],
            "truku_modern": m["truku"], "truku_pecoraro": o["truku"],
            "fr": m["fr"], "en": m["en"], "zh": m["zh"],
            "unconfirmed": bad_p, "unmapped": bad_g, "residue": left,
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
                    (r["truku_train"], r["zh"], r["en"], r["fr"], r["hw"])) + "\n")

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
    # An unbalanced bracket survives strip_variants() by design — it is his
    # page-break damage, and where the missing half goes is a question for the
    # scan, not for a regex. Two rows, named so they are not mistaken for clean.
    unb = [r for r in recs if r["deliverable"]
           and r["truku_train"].count("(") != r["truku_train"].count(")")]
    if unb:
        print("unbalanced bracket (his page-break damage), left as found: %d   %s"
              % (len(unb), ", ".join(r["hw"] for r in unb)))
    # The same shape on the TARGET side, and deliberately NOT stripped. About
    # 1,800 deliverable rows carry a parenthesis in a gloss, but nearly all are
    # the translator clarifying («défoncer (retourner, piocher)») and that is
    # translation, not apparatus. The 188 marked `var.` / `vl.` / `n.b.` are
    # apparatus — yet they are not the same thing as the Truku variants removed
    # above. A source variant is another FORM of one sentence, so keeping his
    # headword form loses nothing; a target variant is another MEANING of it
    # («thanks to you» / «your fault»), and dropping one picks a reading he
    # declined to pick. Ambiguity he recorded is data. Counted, left in place.
    GAPP = re.compile(r"[(（]\s*(vl\.|var\.|n\.?\s?b\.|或[:：]|註[:：])", re.I)
    gapp = sum(1 for r in recs if r["deliverable"]
               and GAPP.search((r["fr"] or "") + (r["en"] or "") + (r["zh"] or "")))
    print("gloss-side variants (var./vl./n.b.), kept as recorded: %d" % gapp)
    nres = sum(1 for r in recs if r["residue"])
    print("uncoloured residue in the %d spanned rows: %d tokens / %d types "
          "in %d rows%s"
          % (len(recs) - nz, sum(residue.values()), len(residue), nres,
             ("   " + ", ".join("%s(%d)" % t for t in residue.most_common(8)))
             if residue else ""))


if __name__ == "__main__":
    main()
