# -*- coding: utf-8 -*-
"""[batch 222] The twice-carded queue is closed, and it was never a metric seam.

`twice211.py` enumerates the headwords Pecoraro carded TWICE, where a
token-keyed map can serve only ONE of the two senses. It has sat open for eleven
batches as though it were a backlog of pairs. It is not. Batch 222 priced it and
then measured it, and both answers are here:

  * PRICED (`twiceprice.py`): 51 flagged tokens, exactly ONE where a remap could
    pay -- `qaya`, SERVED 1 / ORPHAN 2 / OTHER 0.
  * MEASURED (this log): **0 of the 51 values renders PALE anywhere in the
    book.** Every one of them is already dark on both cards. A remap therefore
    trades one dark value for another dark value and moves the metric by zero,
    whichever way it goes.

That is the finding, and it is what closes the queue: the twice-carded class is
a CORRECTNESS seam, not a pallor seam -- exactly what CLAUDE.md already says of
a homograph freeze ("invisible to every colour metric, because the span is
already dark"). Nothing here can be spent on the 98 remaining blocked pairs.
Work it for wrongness if wrongness turns up; never work it for pairs.

### `qaya` -- refused, and the instrument caught out again

The one payable row dissolves on inspection, twice over:

1. The ORPHAN column said 2. Reading the occurrences, one of them is the string
   `QAYA` inside his own French apparatus -- the sub-form
   `Pqaya (Est-ce de la R. QAYA ?)`, "is this from the root QAYA?". That is a
   cross-reference, not a Truku claim (batch 208: the apparatus is not the
   sentence). The real orphan count is 1 against 1: an exact wash even before
   the evidence.

2. The SERVED/ORPHAN split was scored against `qaya`'s register ROW, which reads
   工具;財物 and so served only his second card (東西－物件－行李) and orphaned
   his first (妨礙－障礙－阻礙－阻止). But a single gloss row is not the
   register's answer; the family is (batch 200). Ask the family and the register
   serves the FIRST card too, in three of his own sub-forms with his own
   glosses:

       his Qmaya  同上，動詞形 (=妨礙)     -> qmaya  阻礙
       his Qyaan  障礙－困難               -> qyaan  被擋住
       his Pqaya  懸掛－把某物掛起         -> pqaya  掛

   So modern Truku carries the same polysemy his book does, on the same root.
   Batch 204: a modern homophone is not a freeze. There is nothing to remap --
   `qaya` is the right modern spelling of BOTH his cards, and the register's
   bare row is merely incomplete about it.

This log pins the refusal from both sides, per batch 221's rule that a refusal
must assert its POSITIVE half: the three family glosses must still carry his
meaning, AND `qaya` must still map to itself. If a later batch remaps `qaya`,
the identity pin fails and this refusal is reinstated by the suite rather than
by anyone remembering it.

    python tools/orthography/logs/dom222.py     # site served at :8765
"""
import io
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
SITE = os.path.join(HERE, "..", "..", "..", "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0, green = 0;
  const greens = [], seen = {}, unv = {}, seenAll = {}, unvAll = {};
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    // The PALLOR question is book-wide, so it is asked unscoped. His headword,
    // his sub-form names and his paradigm slots render in .hw / .sub-form /
    // .paradigm, NOT in a .truku box -- the scoped walk below cannot see them,
    // and reported `qaya`, `qyaan` and four other queue values as rendering
    // NOWHERE. A test that cannot see a colour reports it as an absence
    // (batch 216); this log's own assertion caught that. Scoping stays on the
    // PAIR metric, where batch 208's rule applies and a gloss span is not a
    // Truku claim.
    c.querySelectorAll(SEL).forEach(s => {
      const t = (s.textContent||'').trim().toLowerCase();
      seenAll[t] = (seenAll[t] || 0) + 1;
      if (s.classList.contains('w-unv')) unvAll[t] = (unvAll[t] || 0) + 1;
    });
    // scope to .truku, and walk the boxes -- a '.truku ' prefix on a
    // comma-separated selector scopes only the FIRST alternative (batch 216).
    c.querySelectorAll('.truku').forEach(box => {
      box.querySelectorAll(SEL).forEach(s => {
        const t = (s.textContent||'').trim().toLowerCase();
        seen[t] = (seen[t] || 0) + 1;
        if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
        if (s.classList.contains('w-raw')) {
          green++; greens.push(s.textContent.trim() + '|' + hw); }
      });
    });
    c.querySelectorAll('.example').forEach(x => {
      const tr = x.querySelector('.truku'); if (!tr) return;
      const sp = [...tr.querySelectorAll(SEL)]; if (!sp.length) return;
      tot++;
      if (!sp.filter(s => !s.classList.contains('w-mod')).length) ok++;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, seenAll: seenAll,
          unvAll: unvAll, green: green, greens: greens}; }"""

FLOOR = 5331
DENOM = 5429
GREEN = 2
AUDIO_IDS = 5134

# `twiceprice.py`'s 51 flagged map values, verbatim. The claim is about the
# WHOLE list, not about qaya: none of these renders pale, so no remap anywhere
# in the twice-carded class can buy a pair.
QUEUE = """balas balung basaw bawa bgihur bili bngrux buhug bulang bunga
dgiyaq dha gasil hana haya hini hiraw isu ita iyax jima jiyan karaw kasi klabi
ksa lituk lpi lulung mami masaq mirit mu ngungu paah pada pala pgagu qalu qaya
qulit quluh rabi rijig sagu samaw sinaw snru suyang uray wana""".split()

# the refusal's positive half: his first QAYA card IS served by the register,
# through the family rather than through the root's own row. value -> the
# character of his gloss that the register word must still carry.
FAMILY = {"qmaya": "礙", "qyaan": "擋", "pqaya": "掛"}

# his own French cross-reference, the second "orphan" occurrence. Pinned as a
# string so a later re-count knows why ORPHAN read 2 and not 1.
APPARATUS = "Pqaya (Est-ce de la R. QAYA ?)"

# every token of the family renders; a value that renders NOWHERE cannot be
# pale either, and a test that cannot see a colour reports it as an absence
# (batch 216). Assert presence before asserting the absence of pallor.
RENDERS = ("qaya", "qmaya", "qyaan", "pqaya", "spqaya", "qnqaya", "qyqaya")


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    # modern_map.js writes keys with NO leading whitespace; verified.js writes
    # them with two (batch 207).
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def read_gloss():
    g = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"),
                          encoding="utf-8"))
    return {k: (" ".join(v) if isinstance(v, list) else (v or ""))
            for k, v in g.items()}


def entries_text():
    return io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()


def audio_ids():
    s = entries_text()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
    out = set()

    def walk(e):
        for x in (e.get("examples") or []):
            if x.get("a"):
                out.add(x["a"])
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in E:
        walk(e)
    return out


def main():
    fails = []
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

    print("rows with spans: %d   all-dark: %d   %.4f%%"
          % (r["tot"], r["ok"], 100.0 * r["ok"] / DENOM))
    if r["tot"] != DENOM:
        fails.append("denominator moved: %d rows carry spans, expected %d"
                     % (r["tot"], DENOM))
    if r["ok"] < FLOOR:
        fails.append("deliverable pairs FELL to %d, floor is %d"
                     % (r["ok"], FLOOR))

    M, G = read_map(), read_gloss()
    # unscoped for the pallor question -- see the note in JS above
    seen, unv = r["seenAll"], r["unvAll"]

    # 1 -- THE finding. The twice-carded queue holds no pallor at all.
    pale = sorted((w, unv[w]) for w in QUEUE if unv.get(w))
    print("queue values rendering pale: %d of %d" % (len(pale), len(QUEUE)))
    if pale:
        fails.append(
            "a twice-carded value now renders PALE: %s. Batch 222 closed this "
            "queue on the measurement that none of the 51 does -- every remap "
            "trades one dark value for another and buys zero pairs. If one has "
            "gone pale the queue is a metric seam again and the closure has to "
            "be re-argued, not assumed." % pale)
    absent = [w for w in QUEUE if w not in seen]
    if absent:
        fails.append(
            "%d queue values render NOWHERE: %s. The zero-pale result is then "
            "an absence, not a colour (batch 216) -- re-derive the list from "
            "twiceprice.py before trusting it." % (len(absent), absent[:8]))

    # 2 -- the refusal, negative half: no remap of qaya happened
    if M.get("qaya") != "qaya":
        fails.append(
            "map qaya -> %s. Batch 222 REFUSED the remap: his 妨礙 card and his "
            "物件 card are one root in modern Truku too, carried by qmaya 阻礙, "
            "qyaan 被擋住 and pqaya 掛. A modern homophone is not a freeze "
            "(batch 204), so there is no orphan sense to send elsewhere."
            % M.get("qaya"))

    # 3 -- the refusal, positive half: the family still carries his meaning
    for w, ch in sorted(FAMILY.items()):
        gl = G.get(w, "")
        if not gl:
            fails.append(
                "%s has dropped out of the register. The qaya refusal rests on "
                "the FAMILY serving his 妨礙 card where the bare root's row "
                "does not; without %s the refusal loses a leg." % (w, w))
        elif ch not in gl:
            fails.append(
                "%s's gloss now reads '%s' and no longer carries %s. Batch 222 "
                "refused the qaya remap because this row matched his own "
                "sub-form gloss; if it has drifted, re-read his card before "
                "leaving the refusal standing." % (w, gl, ch))
        if M.get(w) != w:
            fails.append(
                "map %s -> %s. The family evidence is that HIS spelling and "
                "the register's are the same string; a map entry moving one of "
                "them breaks the identification the refusal was built on."
                % (w, M.get(w)))

    # 4 -- the family renders, and renders dark
    for w in RENDERS:
        if w not in seen:
            fails.append(
                "%s renders nowhere. The QAYA cards were measured all-dark "
                "span by span; a value that has stopped rendering means the "
                "card changed shape and the measurement no longer describes "
                "it." % w)
        elif unv.get(w):
            fails.append(
                "%s renders PALE %dx. Both QAYA cards were entirely dark when "
                "batch 222 refused the remap -- the refusal cost nothing "
                "BECAUSE nothing there was pale." % (w, unv[w]))

    # 5 -- the apparatus occurrence that inflated ORPHAN to 2
    if APPARATUS not in entries_text():
        fails.append(
            "the sub-form %r is gone from entries.js. It is the second of the "
            "two 'orphan' occurrences twiceprice.py counted, and it is French "
            "apparatus, not a Truku claim (batch 208). If the string changed, "
            "re-price the row before citing 'SERVED 1 / ORPHAN 2'."
            % APPARATUS)

    # 6 -- standing invariants
    if r["green"] != GREEN:
        fails.append("green spans: %d, expected %d %s"
                     % (r["green"], GREEN, r["greens"][:6]))
    n = len(audio_ids())
    if n != AUDIO_IDS:
        fails.append(
            "attached audio ids: %d, expected %d. An id is a URL and batch 222 "
            "wrote no data file at all -- a spelling refusal cannot move this."
            % (n, AUDIO_IDS))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
