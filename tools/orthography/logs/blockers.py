# -*- coding: utf-8 -*-
"""logs/blockers.md — every pale type that is the sole blocker of a pair, with
the gate's own diagnosis beside it, sorted by what ruling on it would buy.

WHY IT IS TWO HALVES. The count comes from the DOM, because that is the only
place the whole chain is visible — CLITIC_FORMS, WORD_OVERRIDES and MODERN_MAP
all feed spellClass(), and a map-only census has been wrong before. The
diagnosis comes from inflection.py, because `regular()` is what actually
refused. Neither half can be read off the other.

WHAT A ROW IS FOR. `ppdsun` (batch 180) was found by accident: the informant read
one sentence and asked why a word in it was pale. The answer was that the gate
had already agreed about the morphology and refused on gloss agreement, whose
instrument is a shared Han character and which cannot see a synonym. If that
shape is common, each instance is one ruling — and the agreed workflow for the
speaker shortlist is "we'll go one by one". This file is that list, ordered so
the reading starts where the pairs are.

A row is NOT a proposal. It carries what the gate found and what he wrote, and
nothing about which reading is right. The rules that decide that — the gloss of
the candidate must match the gloss of the entry it renders in; an attested value
can still be a wrong value; two independent supporters must agree — are not
things a generator applies.

    python tools/orthography/logs/blockers.py       (needs the local server up)
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
H = os.path.dirname(os.path.dirname(ORTH))
H = os.path.join(H, "taroko-pecoraro") if not os.path.exists(
    os.path.join(H, "site")) else H
SITE = os.path.join(H, "site")
sys.path.insert(0, ORTH)
os.chdir(ORTH)
from inflection import Inflection

URL = "http://127.0.0.1:8765/?q=%CC%81"
CACHE = os.path.join(HERE, "blockers_dom.json")

# One row per rendered example: the entry it sits under, its Truku text, and the
# spans that are not dark. `.w-unv` is pale, `.w-raw` is green (a blind char-rule
# guess) — a green span blocks a pair exactly as a pale one does.
DOM = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const out = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw') || {}).textContent || '').trim();
    c.querySelectorAll('.example').forEach(x => {
      const tr = x.querySelector('.truku');
      if (!tr) return;
      const sp = [...tr.querySelectorAll(SEL)];
      if (!sp.length) return;
      const bad = sp.filter(s => !s.classList.contains('w-mod'))
        .map(s => s.textContent.trim().toLowerCase());
      if (!bad.length) return;
      const g = {};
      x.querySelectorAll('.ex-gloss').forEach(p => {
        const l = (p.querySelector('.lang-chip') || {}).textContent || '';
        g[l] = p.textContent.slice(l.length).trim(); });
      out.push({hw: hw, n: sp.length, bad: bad,
                t: (tr.textContent || '').replace(/^§\s*/, '').trim(),
                zh: g['中'] || '', en: g['EN'] || ''});
    });
  });
  return out; }"""


def dom():
    # The cache is opt-in, and deliberately so: it holds a rendering of a
    # particular verified.js, and every ruling changes verified.js. A cache that
    # loaded itself would keep reporting a word pale for the rest of the session
    # after the ruling that darkened it — the same silent-staleness failure as a
    # harness that cannot see a colour and reports it as an absence.
    if "--cache" in sys.argv and os.path.exists(CACHE):
        print("(--cache: reusing %s)" % os.path.basename(CACHE))
        return json.load(io.open(CACHE, encoding="utf-8"))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg = ctx.new_page()
        pg.goto(URL)
        pg.wait_for_timeout(15000)
        rows = pg.evaluate(DOM)
        br.close()
    json.dump(rows, io.open(CACHE, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False)
    return rows


def read(p):
    return io.open(p, encoding="utf-8").read()


def main():
    rows = dom()
    # A type's value is the pairs it ALONE blocks. A sentence with two blockers
    # is worth nothing to either of them until the other also falls, so it is
    # counted separately and never credited to one.
    sole = collections.Counter()
    occ = collections.Counter()
    where = {}
    shared = collections.Counter()
    for r in rows:
        bad = set(r["bad"])
        for b in bad:
            occ[b] += 1
        if len(bad) == 1:
            b = bad.pop()
            sole[b] += 1
            where.setdefault(b, r)
        else:
            for b in bad:
                shared[b] += 1

    m = read(os.path.join(SITE, "modern_map.js"))
    a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    mp = json.loads(m[a:m.index("\n};", a) + 2])
    v = read(os.path.join(SITE, "verified.js"))
    b = v.index("window.MODERN_VERIFIED = {") + len("window.MODERN_VERIFIED = ")
    dark = set(json.loads(re.sub(r",(\s*})", r"\1",
                                 v[b:v.index("\n};", b) + 2])))
    lex = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                                encoding="utf-8")))
    inf = Inflection(lex, mp)

    def diagnose(t):
        """(class, the analyses, the root glosses, his own Chinese for it).

        Every root roots() returns is in `lex` by construction, so "is the root
        listed" is not a question worth a bucket — an earlier cut of this file
        asked whether the root was itself a rendered value instead, which is a
        fact about the dictionary's word pages and not about the gate. What
        separates one refusal from another is only ever which of the two glosses
        was missing, or that both were there and disagreed.
        """
        cands = [(c, p, sf) for c, p, sf, _ in inf.roots(t)]
        if not cands:
            return "no root", [], {}, sorted(inf._his(t))
        gl = {c: sorted(inf._gloss(c)) for c, _, _ in cands}
        his = sorted(inf._his(t))
        slot = sorted(inf._his(t, True))          # word-level only
        if not any(gl.values()):
            return "root unglossed", cands, gl, his
        if not slot:
            return "sentence gloss only", cands, gl, his
        return "gloss disagrees", cands, gl, slot

    buckets = collections.Counter()
    out = []
    for t, n in sole.most_common():
        cls, listed, gl, his = diagnose(t)
        buckets[cls] += 1
        out.append((n, t, cls, listed, gl, his))

    print("blocked pairs with ONE blocker: %d over %d types | "
          "pairs with two or more: %d"
          % (sum(sole.values()), len(sole),
             sum(1 for r in rows if len(set(r["bad"])) > 1)))
    for k in sorted(buckets):
        print("  %-22s %3d types  %3d pairs"
              % (k, buckets[k], sum(n for n, t, c, _, _, _ in out if c == k)))

    f = io.open(os.path.join(HERE, "blockers.md"), "w",
                encoding="utf-8", newline="\n")
    f.write(u"<!-- Generated by tools/orthography/logs/blockers.py — "
            u"do not edit by hand. -->\n\n")
    f.write(u"# Sole blockers, by what a ruling would buy\n\n")
    f.write(u"%d pairs are blocked by exactly one type; %d by two or more and "
            u"are not credited to any single word.\n\n"
            % (sum(sole.values()),
               sum(1 for r in rows if len(set(r["bad"])) > 1)))
    f.write(u"| class | types | pairs |\n|---|---|---|\n")
    for k in sorted(buckets):
        f.write(u"| %s | %d | %d |\n"
                % (k, buckets[k], sum(n for n, t, c, _, _, _ in out if c == k)))
    f.write(u"\n`gloss disagrees` and `sentence gloss only` are the adjudicable "
            u"ones: the gate reached a dark root and refused on the Chinese. "
            u"`no root` is not reachable by any argument we hold.\n")

    for k in ("gloss disagrees", "sentence gloss only", "root unglossed",
              "no root"):
        rowsk = [r for r in out if r[2] == k]
        if not rowsk:
            continue
        f.write(u"\n## %s — %d types, %d pairs\n\n"
                % (k, len(rowsk), sum(r[0] for r in rowsk)))
        if k == "no root":
            f.write(u"Listed for completeness only. No analysis reaches a "
                    u"candidate root at all, so there is nothing to rule on.\n\n"
                    + u", ".join(u"%s (%d)" % (r[1], r[0]) for r in rowsk)
                    + u"\n")
            continue
        for n, t, cls, listed, gl, his in rowsk:
            ex = where.get(t, {})
            f.write(u"### %s — %d pair%s%s\n\n"
                    % (t, n, "" if n == 1 else "s",
                       (u", %d more shared" % shared[t]) if shared[t] else u""))
            f.write(u"- under **%s**\n" % ex.get("hw", "?"))
            # The 🔊 is the audio button; textContent cannot see that it is a
            # control rather than a word.
            f.write(u"- § %s\n" % ex.get("t", "").replace(u"🔊", "").strip())
            if ex.get("zh"):
                f.write(u"- 中 %s\n" % ex["zh"])
            for c, p, sf in listed[:4]:
                f.write(u"- `%s%s%s` → **%s** %s\n"
                        % (p + "-" if p else "", c, "-" + sf if sf else "",
                           c, u"／".join(gl.get(c) or []) or u"(no gloss)"))
            if his:
                f.write(u"- his: %s\n" % u" ／ ".join(x.strip() for x in his[:3]))
            f.write(u"\n")
    f.close()
    print("wrote tools/orthography/logs/blockers.md")


if __name__ == "__main__":
    main()
