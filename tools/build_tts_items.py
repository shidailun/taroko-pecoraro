# -*- coding: utf-8 -*-
"""Rebuild the TTS item list from the RENDERED page, and price the resynthesis.

`ilrdf/build_full_items.py` built `items.json` by porting `modernize()`,
`WORD_OVERRIDES` and `MODERN_MAP` into Python — a second implementation of the
thing the app already does. It is several batches behind: it knows nothing of
the clitic joins, of `tidy()`, of `.w-orig` or `.meta-abbr`, or of batch 207's
metalinguistic rows. It also cannot run at all any more — it takes the first `{`
to the last `}` of `modern_map.js`, and that file has held a second object,
`window.LEXICAL_SUBS`, since tier X landed.

So this asks the page, which is the project's rule for everything else: the
colour metric, the MT export, and every `logs/dom*.py`. One implementation, in
`app.js`, and no port to drift.

    python tools/build_tts_items.py            # report only, writes nothing
    python tools/build_tts_items.py --write    # write items.json + the worklist

**The ids must not move.** A clip lives at `R2_BASE + id + ".mp3"`, so a
regenerated id is a silent unhooking of audio that is already recorded and
already paid for. Ids are minted exactly as the original did — `kind_slug(his
text)`, deduplicated with `_2`, `_3` in entries.js order — and the assertion
that this is still the same rule is that every one of the 5,134 ids the page
carries in `data-audio` comes back identical. Nothing is written unless it does.

**What the DOM adds that the port could not.** His six metalinguistic rows
(`Paro = Grand; Knplaan = Grandeur` — the `t` field IS the French) render with no
spans, and reach this file as text with no Truku in it. They are dropped from the
item list rather than sent to a voice.

The worklist is the point of the exercise: `changed` are clips that now read a
word the page no longer shows, `new` are examples with no clip at all.
"""
import json
import os
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ITEMS = ROOT.parents[1] / "ilrdf" / "tts_full" / "items.json"
WORKLIST = ROOT / "exports" / "tts_worklist.json"
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 30000

# The page renders sub-forms in a consistent order within every root, which is
# NOT the order they sit in the file, so position cannot pair the two walks and
# the nodes carry no id. What pairs them is HIS OWN SPELLING: rendered with the
# toggle off, every unit is his text again, and normalised to letters it keys
# back into `entries.js` 10,350 for 10,350 with nothing left over. So the page is
# read twice — once for identity, once for what the voice should say.
KEYS = r"""() => {
  const t = el => { if (!el) return '';
    const c = el.cloneNode(true); c.querySelectorAll('button').forEach(x => x.remove());
    return c.textContent.replace(/\s+/g, ' ').trim(); };
  const out = [];
  for (const card of document.querySelectorAll('#results > article.entry:not(.stub)')) {
    const hw = t(card.querySelector('.hw-line .hw'));
    out.push({kind: 'hw', hw: hw, key: hw});
    for (const e of card.querySelectorAll(':scope > .examples > .example'))
      out.push({kind: 'ex', hw: hw, key: t(e.querySelector('.truku'))});
    for (const s of card.querySelectorAll(':scope > .subentry')) {
      out.push({kind: 'form', hw: hw, key: t(s.querySelector('.sub-form'))});
      for (const e of s.querySelectorAll('.example'))
        out.push({kind: 'ex', hw: hw, key: t(e.querySelector('.truku'))});
    }
  }
  return out;
}"""

# The sentence as a voice should read it: no buttons, and none of the apparatus.
# `.meta-abbr` is his editorial note (`vl.`, the French asides he sets in
# brackets) and `.w-orig` is the superseded word shown beside its modern
# replacement — batch 208 found both being shipped as Truku to the MT export,
# and a TTS run would have read them aloud.
HARVEST = r"""() => {
  const train = el => {
    if (!el) return '';
    const c = el.cloneNode(true);
    c.querySelectorAll('button, .meta-abbr, .w-orig').forEach(b => b.remove());
    return c.textContent.replace(/\s+/g, ' ')
      .replace(/\(\s*[.,:;!?\s]*\)/g, '').replace(/\(\s*[.,:;]\s*/g, '(')
      .replace(/\s+\)/g, ')').replace(/\s+([,.;:!?])/g, '$1')
      .replace(/\s+/g, ' ').trim();
  };
  const ex = (e, hw, out) => {
    const b = e.querySelector('.audio-btn');
    out.push({kind: 'ex', hw: hw, modern: train(e.querySelector('.truku')),
              audio: b ? b.getAttribute('data-audio') : null,
              meta: e.classList.contains('meta')});
  };
  const out = [];
  // Slot cards are generated, not his: they carry no entries.js row and would
  // throw the walk out of step with the file.
  for (const card of document.querySelectorAll('#results > article.entry:not(.stub)')) {
    const hw = train(card.querySelector('.hw-line .hw'));
    out.push({kind: 'hw', hw: hw, modern: hw, audio: null, meta: false});
    for (const e of card.querySelectorAll(':scope > .examples > .example')) ex(e, hw, out);
    for (const s of card.querySelectorAll(':scope > .subentry')) {
      const f = s.querySelector('.sub-form');
      out.push({kind: 'form', hw: hw, modern: train(f), audio: null,
                ref: f ? f.getAttribute('data-ref') : null, meta: false});
      for (const e of s.querySelectorAll('.example')) ex(e, hw, out);
    }
  }
  return out;
}"""


def slug(s):
    """The original id rule, unchanged. Moving it moves every clip URL."""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40] or "x"


def source_units():
    """entries.js in render order, with the id each unit has always had."""
    src = open(SITE / "entries.js", encoding="utf-8").read()
    entries = json.loads(src[src.index("["):src.rindex("]") + 1])
    units, seen = [], set()

    def add(kind, hw, raw):
        raw = (raw or "").strip()
        if not raw:
            return
        base = "%s_%s" % (kind, slug(raw))
        idd, n = base, 1
        while idd in seen:
            n += 1
            idd = "%s_%d" % (base, n)
        seen.add(idd)
        units.append({"id": idd, "kind": kind, "hw": hw, "pecoraro": raw})

    for e in entries:
        hw = e.get("hw", "")
        add("hw", hw, hw)
        for x in e.get("examples") or []:
            add("ex", hw, x.get("t", ""))
        for s in e.get("subs") or []:
            add("form", hw, s.get("form", ""))
            for x in s.get("examples") or []:
                add("ex", hw, x.get("t", ""))
    return units


WORD = re.compile(r"[^\W\d_]+(?:['’\"][^\W\d_]+)*", re.UNICODE)


def pieces(s):
    """Words, not typography. `items.json` predates `tidy()`, so comparing raw
    strings scores every comma and final stop as a change — 4,964 of 5,134 rows
    'drift' that way, which measures the punctuation. A clip is stale when the
    voice would say a different WORD."""
    return [w.lower() for w in WORD.findall((s or "").replace("-", " "))]


def norm(s):
    """Letters and digits only. `tidy()` respaces his punctuation at display
    time, so the rendered text is his wording but not his typography."""
    return re.sub(r"[^0-9a-z]+", "", (s or "").lower())


def read_page(pg, mode, js):
    pg.goto(URL)
    pg.evaluate("m => localStorage.setItem('taroko_pecoraro_spelling_v1', m)", mode)
    pg.reload()
    pg.wait_for_timeout(WAIT)
    return pg.evaluate(js)


def main():
    write = "--write" in sys.argv
    units = source_units()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context().new_page()
        keys = read_page(pg, "original", KEYS)
        rows = read_page(pg, "modern", HARVEST)
        cards = pg.evaluate(
            "document.querySelectorAll('#results > article.entry:not(.stub)').length")
        b.close()

    if len(keys) != len(rows):
        print("!! the two reads disagree on the page itself: %d vs %d units"
              % (len(keys), len(rows)))
        return 1

    # One `.example` on the page has nothing to say. Batch 207 read the scan at
    # 1.8× and found the § followed directly by French: the empty `t` is HIS
    # omission and stays in `entries.js` as the faithful record. `add()` has
    # always dropped empty text, so the page carries one unit the file does not.
    # Counted, not assumed — a second empty row would be news, not noise.
    pairs = list(zip(keys, rows))
    blank = [1 for k, _ in pairs if not norm(k["key"])]
    pairs = [(k, r) for k, r in pairs if norm(k["key"])]

    if len(pairs) != len(units):
        print("!! page has %d units (after %d blank), entries.js has %d — "
              "nothing written" % (len(pairs), len(blank), len(units)))
        return 1

    # His spelling is the key. A key that repeats does so inside one card and
    # renders identically both times, so the two ids are interchangeable; they
    # are handed out in file order to keep the run reproducible.
    src = {}
    for u in units:
        src.setdefault((u["kind"], norm(u["hw"]), norm(u["pecoraro"])), []).append(u)
    taken, unkeyed = {}, 0
    for k, r in pairs:
        q = src.get((k["kind"], norm(k["hw"]), norm(k["key"])))
        if not q:
            unkeyed += 1
            continue
        taken[id(k)] = q.pop(0)
    if unkeyed:
        print("!! %d rendered units key to nothing in entries.js — nothing "
              "written" % unkeyed)
        return 1

    # The assertion that licenses everything downstream: the id rule has not
    # moved. A clip lives at its id, so a re-minted id is a silent unhooking.
    attached = [(k, r) for k, r in pairs if r["audio"]]
    wrong = [(r["audio"], taken[id(k)]["id"]) for k, r in attached
             if r["audio"] != taken[id(k)]["id"]]
    if wrong:
        print("!! %d of %d attached clips mint a DIFFERENT id — writing would "
              "unhook them. First: %s -> %s"
              % (len(wrong), len(attached), wrong[0][0], wrong[0][1]))
        return 1

    old = {}
    if ITEMS.exists():
        old = {it["id"]: it for it in json.load(open(ITEMS, encoding="utf-8"))}

    items, meta, changed, new, same = [], 0, [], [], 0
    for k, r in pairs:
        u = taken[id(k)]
        if r["meta"]:
            meta += 1
            continue
        it = dict(u)
        it["modern"] = r["modern"]
        items.append(it)
        if u["kind"] != "ex":
            continue
        was = old.get(u["id"])
        if not was:
            new.append(u["id"])
        elif pieces(was["modern"]) != pieces(r["modern"]):
            changed.append(u["id"])
        else:
            same += 1

    ex = [i for i in items if i["kind"] == "ex"]
    print("cards %d - units %d (hw %d, form %d, ex %d) - blank rows %d, "
          "metalinguistic rows dropped %d" % (cards, len(items),
                          sum(1 for i in items if i["kind"] == "hw"),
                          sum(1 for i in items if i["kind"] == "form"), len(ex),
                          len(blank), meta))
    print("against the clips as built: %d unchanged, %d CHANGED wording, %d new "
          "- %d of %d sentences need a voice (%.1f%%)"
          % (same, len(changed), len(new), len(changed) + len(new), len(ex),
             100.0 * (len(changed) + len(new)) / len(ex)))
    print("ids minted back identically for all %d attached clips" % len(attached))
    if not write:
        print("report only — pass --write to update items.json and the worklist")
        return 0
    json.dump(items, open(ITEMS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    work = {"changed": changed, "new": new,
            "note": "ids to (re)synthesize; text is in items.json"}
    # Beside items.json is where `full_sentences_synth.py` looks; in the repo is
    # where it can be read six months from now.
    WORKLIST.parent.mkdir(exist_ok=True)
    for path in (ITEMS.parent / "worklist.json", WORKLIST):
        json.dump(work, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote items.json + worklist.json (%s) and %s" % (ITEMS.parent, WORKLIST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
