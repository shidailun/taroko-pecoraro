# -*- coding: utf-8 -*-
"""batch 211 — the LIDIL homograph freeze, measured in the DOM.

He carded LIDIL twice: 工具的柄 and 傾斜的－歪的－扭曲的. The map sent the token to
`rijil` for both, and `rijil` is the BEND root — `mrijil` 使彎曲, which is his own
Plidil 使彎曲－扭 verbatim. The handle root is `rijig` 柄（刀;鋤）, and its whole
modern family says 柄: `emprijig` 要做柄, `prjigi` 讓…做柄, `tmrijig` 專做柄. So four
running sentences shipped a dark, correctly-spelled, WRONG word — the shape no
colour metric can see, because the span was already dark.

The fix is a remap plus a citation refusal, and it is the mirror image of the
batch 205 DIMA/QALO refusal: there his sentences were the sense the map already
rendered, so a remap would have painted correct sentences wrong. Here the
sentences are the wrong side and one head is the right one.

Asserted here:
  1. all four handle sentences render `rijig`, every span dark
  2. NEITHER headword renders the handle root — CITE_SPELL refuses at citation
     sites, so the 傾斜 card is never painted with it. Both heads go pale, which
     is what `naru` already costs his NALU card; a refusal that rendered dark
     would be an assertion.
  3. the 傾斜 card's family still renders the `-l` root, dark. Every affixed
     `*lidil` form in the book is on that card — the handle card has no subs at
     all — so the root projection was crossing two cards he kept apart. The five
     forms it moved are pinned in manual_map.json, and this is what re-checks
     that the pins held.

`?q=lidil` returns exactly the five cards that carry the token. Verdicts only.
"""
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

URL = "http://127.0.0.1:8765/?q=lidil"
WAIT = 900

JS = """() => [...document.querySelectorAll('article.entry')].map(a => ({
  head: [...(a.querySelector('.hw') || a).querySelectorAll('.w-mod,.w-unv,.w-raw')]
          .map(s => s.textContent.trim() + '|' + s.className),
  txt: a.textContent,
  rows: [...a.querySelectorAll('.example')].map(e => ({
    t: e.querySelector('.truku') ? e.querySelector('.truku').textContent : '',
    spans: [...(e.querySelector('.truku') || e).querySelectorAll('.w-mod,.w-unv,.w-raw')]
             .map(s => s.textContent.trim() + '|' + s.className)
  }))
}))"""

# his four handle sentences, keyed on a word of the rendered modern form
HANDLE = ["rijig na ka naqih", "rijig na", "rijig pucing su", "rijig su"]
# the 傾斜 card's family, which must keep the bend root
BEND = ["mrijil", "pkrijil", "nsrijil", "pnsrijil"]


def main():
    fails = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("http://127.0.0.1:8765/")
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL)
        pg.wait_for_timeout(WAIT)
        cards = pg.evaluate(JS)
        b.close()

    print("cards for ?q=lidil: %d" % len(cards))
    if len(cards) != 5:
        fails.append("expected 5 cards carrying his token, got %d" % len(cards))

    # 2 — the two headwords. Identify them by the √ root mark on his LIDIL cards.
    heads = [c for c in cards if c["head"] and len(c["head"]) == 1]
    print("single-span headwords (his two LIDIL cards): %d" % len(heads))
    if len(heads) != 2:
        fails.append("expected 2 LIDIL headwords, got %d" % len(heads))
    for h in heads:
        txt, cls = h["head"][0].rsplit("|", 1)
        dark = "w-mod" in cls
        print("  head %-8s %s" % (txt, "dark" if dark else "pale"))
        if re.search(r"rijig", txt, re.I):
            fails.append("headword renders the handle root (%s) — cite seam did "
                         "not fire, and the 傾斜 card is now frozen" % txt)
        if dark:
            fails.append("headword %s is dark; a citation may only refuse" % txt)

    # 1 — the four handle sentences, every span dark
    seen = 0
    for c in cards:
        for r in c["rows"]:
            if not any(k in r["t"] for k in HANDLE):
                continue
            seen += 1
            pale = [s for s in r["spans"] if "w-mod" not in s.rsplit("|", 1)[1]]
            root = [s.rsplit("|", 1)[0] for s in r["spans"]
                    if re.match(r"riji[gl]$", s.rsplit("|", 1)[0], re.I)]
            ok = root == ["rijig"] and not pale
            print("  § %-34s %-7s %s" % (r["t"][:34].strip(), root, "ok" if ok else "FAIL"))
            if root != ["rijig"]:
                fails.append("sentence %r renders %s" % (r["t"][:26], root))
            if pale:
                fails.append("sentence %r has pale spans %s" % (r["t"][:26], pale[:3]))
    print("handle sentences measured: %d (expected 4)" % seen)
    if seen != 4:
        fails.append("expected 4 handle sentences, measured %d" % seen)

    # 3 — the bend family held its root, and nothing on that card leaked
    bend = [c for c in cards if "Penché" in c["txt"]]
    if not bend:
        fails.append("the 傾斜 card was not in the result set")
    else:
        t = bend[0]["txt"]
        missing = [f for f in BEND if f not in t]
        leak = re.findall(r"\brijig\b", t, re.I)
        print("bend family present: %d/%d   handle-root leaks onto it: %d"
              % (len(BEND) - len(missing), len(BEND), len(leak)))
        if missing:
            fails.append("bend family lost %s — a pin did not hold" % missing)
        if leak:
            fails.append("the 傾斜 card leaked the handle root %d times" % len(leak))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
