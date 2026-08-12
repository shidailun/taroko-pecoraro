# -*- coding: utf-8 -*-
"""batch 244 — the colophon is not a Truku word, and it was in the census.

His book has two cards tagged `note`, and neither is a lexical entry. REMARQUE
is his prose on Taroko naming customs; COLOPHON is the printer's imprint at the
very end — *Paris, 128 R. du Bac, Octobre 1976 - Juin 1977* over two rows of
typewriter divider glyphs. Both were transcribed because the digitization ran
page by page across all 398 pages, front and back matter included, and both were
being rendered as headwords.

That is where the fault is. `colophon` has no map entry, so in modern spelling
`charRules()` fired on it — `o→u`, `l→r` — and the card printed **CURUPHUN**: a
Truku word the dictionary invented out of a French one, on a headword line, in
his own typeface. It is the "Palissade → Parissade" fault the hard invariants
name for glosses, promoted to a headword, and it had been live long enough to
cost a real lookup: `edictionary_trv.json:229` carries `"curuphun": null`,
somebody having asked the ILRDF e-dictionary for the invented word.

**0 pairs, by construction.** A headword sits in no `.truku` box (batch 223), so
this cannot move the metric and the log asserts that it did not: the pair count,
the denominator and every `.truku` figure are identical either side of the fix.

The fix is display-only and the smallest available — `entryHtml()` prints the
headword of a `note` card raw, the way `tagHtml()` already prints a tag that
carries no root mark. **`entries.js` keeps both cards**, so the record of the
page is untouched; what stops is the spelling claim about it.

What this batch is really correcting is a MEASUREMENT. Two spans of French were
sitting in the green class — green meaning "no map entry fired", which reads as
an unresolved Truku token. They were never Truku, so counting them was batch
234's `t == fr` fault in a second place: French in a Truku field, inflating a
figure. Book-wide green falls 15 → 13 spans and 14 → 12 types, and **that is a
correction, not a win** — the two spans leave the numerator and the denominator
together. Dark holds at 44,726 and pale at 165, which is the assertion that says
so: if this had bought anything, one of those two would have moved.

The pins below are therefore mostly EQUALITIES on things that must not move,
and one ceiling on the green class, which falls as the project works.
"""
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
URL = "http://127.0.0.1:8765/"

# ---- the pins -------------------------------------------------------------
NOTE_HWS = ["COLOPHON", "REMARQUE"]   # his two `note` cards, in `entries.js`
INVENTED = "curuphun"                 # what charRules() made of the first one

CARDS = 1967                          # entries.js, unchanged: display-only fix
DARK_FLOOR = 44726                    # book-wide dark spans; grows with rulings
PALE_CEIL = 165                       # book-wide pale spans; falls with rulings
GREEN_CEIL = 13                       # book-wide green spans, was 15
GREEN_TYPE_CEIL = 12                  # ... in 12 types, was 14

TRUKU_SPANS = 36308                   # `.truku`-scoped, IDENTICAL either side
TRUKU_GREEN = 1                       # of the fix -- that is the 0-pairs claim

fails = []


def ck(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


# ---- the DOM --------------------------------------------------------------
READ = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const cls = s => s.classList.contains('w-raw') ? 'green'
                 : s.classList.contains('w-unv') ? 'pale' : 'dark';
  const tot = {dark: 0, pale: 0, green: 0};
  const tru = {dark: 0, pale: 0, green: 0};
  const greenTypes = {}, notes = [], invented = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hwEl = c.querySelector('.hw');
    const hw = hwEl ? (hwEl.textContent || '').trim() : '';
    const tagEl = c.querySelector('.tag');
    const tag = tagEl ? (tagEl.textContent || '').trim() : '';
    c.querySelectorAll(SEL).forEach(s => {
      const k = cls(s), t = (s.textContent || '').trim();
      tot[k]++;
      if (k === 'green') greenTypes[t.toLowerCase()] = 1;
      if (t.toLowerCase() === '%s') invented.push(hw);
    });
    c.querySelectorAll('.truku').forEach(b => {
      b.querySelectorAll(SEL).forEach(s => tru[cls(s)]++);
    });
    if (tag === 'note')
      notes.push({hw: hw, spans: c.querySelectorAll('.hw ' + SEL).length,
                  boxes: c.querySelectorAll('.truku').length});
  });
  return {tot: tot, tru: tru, notes: notes, invented: invented,
          greenTypes: Object.keys(greenTypes).length,
          cards: document.querySelectorAll('#results > article.entry').length};
}""" % INVENTED

# The controls patch `entries.js` ON THE WIRE and reload, because mutating
# `window.ENTRIES` in place does not re-render: the app builds its index at
# load, and dispatching `input` on the search box moves nothing (`#results`
# innerHTML is byte-identical before and after). A control that patched a live
# object and then read a stale DOM would have passed for free -- batch 234's
# rule about a leg that does not refuse, arriving through the render path
# rather than through the field.
#
# Leg A patches the field the guard READS (`tag`), and the invented word has to
# come back. Leg B writes to a field it does not read (`fr`) and must NOT bring
# it back -- batch 235's pairing, which is what says leg A passes on the tag
# and not merely on the card having been touched. The patcher raises before the
# route is even registered if its string is absent, so a control that patched
# nothing cannot report success.
PATCHES = {
    "tag": ('"hw": "COLOPHON",\n    "tag": "note",',
            '"hw": "COLOPHON",\n    "tag": "",'),
    "fr": ('"hw": "COLOPHON",\n    "tag": "note",\n    "fr": "[decorative',
           '"hw": "COLOPHON",\n    "tag": "note",\n    "fr": "[DECORATIVE'),
}


def patched_page(pw, field):
    """load the book with one field of the colophon card rewritten."""
    old, new = PATCHES[field]
    body = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    if old not in body:
        raise RuntimeError("control leg %r matched no card: the patch string "
                           "is stale, so this leg proves nothing" % field)
    body = body.replace(old, new, 1)
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.route("**/entries.js*", lambda r: r.fulfill(
        status=200, content_type="application/javascript; charset=utf-8",
        body=body))
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=colophon")
    pg.wait_for_timeout(3000)
    out = pg.evaluate(REREAD)
    b.close()
    return out

REREAD = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  const out = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hwEl = c.querySelector('.hw');
    if (!hwEl) return;
    out.push({hw: (hwEl.textContent || '').trim(),
              spans: hwEl.querySelectorAll(SEL).length});
  });
  return out;
}"""


def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        d = pg.evaluate(READ)
        b.close()
        d["ctlA"] = patched_page(pw, "tag")   # guard's own field: must return
        d["ctlB"] = patched_page(pw, "fr")    # a field it never reads: must not
    return d


def main():
    d = measure()
    E = entries_json()

    print("SPANS book dark %d pale %d green %d (%d types) | truku %d green %d"
          % (d["tot"]["dark"], d["tot"]["pale"], d["tot"]["green"],
             d["greenTypes"], sum(d["tru"].values()), d["tru"]["green"]))

    # --- 1. the invented word is off the page
    ck(not d["invented"], "%s still renders as a span, on %s: the char rules "
       "are still making a Truku word out of his French"
       % (INVENTED.upper(), ", ".join(d["invented"][:3])))

    # --- 2. his two note cards print his own letters, with no spans at all
    got = sorted(n["hw"] for n in d["notes"])
    ck(got == NOTE_HWS, "the `note` cards render %s, expected %s"
       % (got, NOTE_HWS))
    for n in d["notes"]:
        ck(n["spans"] == 0, "the %s headword carries %d span(s): a note card "
           "makes no spelling claim and must print raw" % (n["hw"], n["spans"]))
        ck(n["boxes"] == 0, "the %s card has %d `.truku` box(es), so this "
           "ruling could have moved the metric after all" % (n["hw"], n["boxes"]))

    # --- 3. display-only: entries.js keeps both cards
    notes = [e for e in E if (e.get("tag") or "").strip() == "note"]
    ck(len(E) == CARDS, "entries.js has %d cards, want %d entries, got %d"
       % (len(E), CARDS, len(E)))
    ck(sorted(e["hw"] for e in notes) == NOTE_HWS,
       "entries.js no longer carries both note cards (%s): the fix is "
       "display-only and the page stays in the record"
       % sorted(e["hw"] for e in notes))

    # --- 4. what moved, and what must not have
    ck(d["cards"] == CARDS, "the DOM rendered %d cards, want %d cards, got %d"
       % (d["cards"], CARDS, d["cards"]))
    ck(d["tot"]["dark"] >= DARK_FLOOR, "book-wide dark fell to %d from %d: "
       "this batch removed two spans of FRENCH and must not have touched a "
       "Truku one" % (d["tot"]["dark"], DARK_FLOOR))
    ck(d["tot"]["pale"] <= PALE_CEIL, "book-wide pale rose to %d from %d"
       % (d["tot"]["pale"], PALE_CEIL))
    ck(d["tot"]["green"] <= GREEN_CEIL, "book-wide green rose to %d, ceiling "
       "%d" % (d["tot"]["green"], GREEN_CEIL))
    ck(d["greenTypes"] <= GREEN_TYPE_CEIL,
       "book-wide green types rose to %d, ceiling %d"
       % (d["greenTypes"], GREEN_TYPE_CEIL))
    ck(sum(d["tru"].values()) == TRUKU_SPANS and d["tru"]["green"] == TRUKU_GREEN,
       "the `.truku` scope moved: %d spans / %d green against %d / %d. A "
       "headword is in no `.truku` box, so a note-card ruling buys 0 pairs BY "
       "CONSTRUCTION and this is the leg that says so"
       % (sum(d["tru"].values()), d["tru"]["green"], TRUKU_SPANS, TRUKU_GREEN))

    # --- 5. the receipt: the invented word cost a real lookup
    ed = json.load(io.open(os.path.join(ORTH, "edictionary_trv.json"),
                           encoding="utf-8"))
    ck(INVENTED in ed and ed[INVENTED] is None,
       "`%s` is no longer a null lookup in edictionary_trv.json -- that row is "
       "the evidence the invented word was live long enough to be asked of a "
       "real Truku dictionary" % INVENTED)

    # --- 6. the controls
    bad = 0
    a = [r for r in d["ctlA"] if r["hw"].upper() == INVENTED.upper()]
    if not (a and a[0]["spans"] > 0):
        bad = 1
        print("CONTROL A did not refuse: stripping the `note` tag left the "
              "headword raw, so the guard is not what suppresses %s and this "
              "log is measuring nothing" % INVENTED.upper())
    b = [r for r in d["ctlB"] if r["hw"].upper() == INVENTED.upper()]
    if b:
        bad = 1
        print("CONTROL B refused for free: the same string written to a field "
              "the guard does not read brought %s back, so leg A passes on "
              "something other than the tag" % INVENTED.upper())
    if not bad:
        print("CONTROLS both behaved: tag patched -> %s returns; fr patched "
              "-> it does not" % INVENTED.upper())

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
