# -*- coding: utf-8 -*-
"""batch 220 — the register spells the slot, and a tie-break made in the absence
of evidence is retired when the evidence arrives.

### Where the blocker came from

Batch 219's G'LI" instrument — *is the pale value a proper prefix of, or one
letter short of, a dark value on the same card* — was written for one pair and
then run over all 66 `no root` blockers. Three hits. One (`pggu`) is refused in
writing; one (`qloq` inside `lqloq`) has a single dark word on its whole card
and proves nothing. The third was `srngiyun`, sitting pale on a card with
**five dark slots**.

### SLANGI — the register spells his suffix, and spells it without the `y`

His SLANGI 剩下的－剩餘之物 card renders `srangi`, `msrangi`, `psrangi`,
`psrngii`, `psrngiyan` dark and `srngiyun`, `pnsrngiyan` pale. The `-rngiy-`
shape was not evidence: batch 215 put it there as a **consistency fix, and said
so in writing** — "his four siblings all render `-rngiy-` … pale before, pale
after — a consistency fix, not a claim". A tie-break, taken in the absence of
anything better.

The register has something better. Asked for every form of this root carrying
the syncopated stem, it returns exactly four, and **not one of them writes a
`y`**:

    psrngiun   留一些。      psrngion      rngii      rngiun

`psrngiun` is the causative slot of his own `Pslangi` 使之有剩餘 — dom218
already cites it as the vouching form for that head — and `rngiun` is the bare
stem in the same slot. The alternation is demonstrable inside the register on
its own terms: `psngari` 多餘的 and `psrngiun` 留一些 are the same word, so
`-ngari` syncopates to `-rngi-` before `-un`. Apply it to `sngari` 剩餘 (74
speakers) and his slot is `srngiun`.

His gloss agrees: `Slngiyun` is 他們用餐後剩下的一切, and 剩／留 are the two
characters his own card and the register's `sngari` 剩餘 / `rngii` 留著 share.

`slngiyun -> srngiun` came back **code 6** off the ladder, no hand ruling, and
bought the pair. **+1: 5,330 -> 5,331.**

### The same evidence, run back over a slot that was already dark

His card writes ONE suffix and the map was rendering it two ways — `srngiun`
but `psrngiyun`. `psrngiyun` is not in the register; `psrngiun` and `psrngion`
are. Repinning it replaces an INFERENCE with an ATTESTATION (code 7 -> **code
1**) and costs nothing, because the word was dark either way. It is the batch-219
rule applied in the direction that is cheap: cite the tie-break, name the
evidence that retires it, and only then write the value. `census130.py` carries
`psrngiyun` in its `GAIN` list and now prints it `absent` — but that log is a
census and exits 0 either way, so the repin cost no supersession. The cost was
priced BEFORE the edit, on the assumption it would; it did not.

### Refused — the `-an` slots, and why the pallor is correct

`lngiyan -> rngiyan` and `pnslngiyan -> pnsrngiyan` are the card's two remaining
pale values and this batch does NOT rule them. The same question that settled
`-un` refuses them: over the whole register there is **no `-an` form of this
root in the syncopated stem at all**, and no `-yan` form of it either. The four
syncopated forms are `-i`, `-un`, `-on`. The register's own 使留一些 is
`pnsngari`, built on the FULL stem, which is his other card's root — and merging
two cards he kept apart is not licensed (batch 215, and the LANGI/`rangi`
acquittal, which is written up in the batch log and was deliberately not
re-derived here).

So `-an` keeps the inferred `-rngiy-` and stays where it is. Evidence where
there is evidence, inference where there is none; inventing `rngian` to make the
paradigm look tidier would be the metric deciding the spelling.

### What this log asserts

  1. the two SLANGI rulings, map value and emitted code, and that `srngiyun`
     and `psrngiyun` no longer render at all
  2. the five dark slots that convicted them — the argument is the card
  3. the register facts the ruling rests on, read from `attested_modern.json`:
     the four syncopated forms are listed, and no `-an`/`-yan` form is
  4. the two refused `-an` values are still pale and still there
  5. the metric floor, the denominator, green, and the audio-id invariant
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
  const greens = [], seen = {}, unv = {}, rows = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
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
      const bad = sp.filter(s => !s.classList.contains('w-mod'));
      if (!bad.length) ok++;
      const t = (tr.textContent||'').trim();
      if (/\bsrngiun\b|\bpsrngiun\b/i.test(t))
        rows.push({hw: hw, t: t.slice(0, 62),
                   bad: bad.map(s => s.textContent.trim())});
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv,
          green: green, greens: greens, rows: rows}; }"""

FLOOR = 5331
DENOM = 5429
GREEN = 2
AUDIO_IDS = 5134

# his token -> (value ruled, emitted code). srngiun came off the ladder on the
# rung that skips the gloss test, which is what the register evidence had to
# make up for; psrngiun is LISTED, which is the whole point of repinning it.
RULED = {
    "slngiyun":  ("srngiun", 6),
    "pslngiyun": ("psrngiun", 1),
}

# the values these two used to render. Batch 215 put the `y` there as a stated
# tie-break, not as a claim; if either comes back the tie-break has been
# reinstated over the register's own spelling.
SUPERSEDED = ("srngiyun", "psrngiyun")

# the dark slots of his SLANGI card. They are the reason the pale one was worth
# asking about at all -- five dark, two pale, one instrument.
SLANGI = ["srangi", "msrangi", "psrangi", "psrngii", "psrngiyan"]

# the register's own spelling of this root's syncopated stem: four forms, no y.
# Read from attested_modern.json, because that is the file the claim rests on.
LISTED = ("psrngiun", "psrngion", "rngii", "rngiun")

# refused this batch -- the rendered value -> why the pallor is correct
REFUSED = {
    "rngiyan": "the register has no -an form of this root in the syncopated "
               "stem at all; its 剩下的東西 is nngari/nengari, off the FULL "
               "stem, which is his OTHER card's root",
    "pnsrngiyan": "same: the register's 使留一些 is pnsngari, built on the "
                  "full stem. Inventing pnsrngian to tidy the paradigm would "
                  "be the metric deciding the spelling",
}


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    # modern_map.js writes keys with NO leading whitespace; verified.js writes
    # them with two (batch 207).
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def read_ver():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((k, int(n))
                for k, n in re.findall(r'^  "(.+?)": (\d+),?$', t, re.M))


def read_entries():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def audio_ids(E):
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

    M, V = read_map(), read_ver()
    seen, unv = r["seen"], r["unv"]

    # 1 -- the two rulings, map value and emitted code
    for tok, (val, code) in sorted(RULED.items()):
        if M.get(tok) != val:
            fails.append("map %s -> %s, batch 220 ruled it %s off the "
                         "register's own spelling of the slot"
                         % (tok, M.get(tok), val))
        if val not in V:
            fails.append("%s is not verified. srngiun came off the ladder and "
                         "psrngiun is LISTED, so a value dropping out means "
                         "the map or the register table moved under it." % val)
        elif V.get(val) != code:
            fails.append("%s is verified code %s, batch 220 built it to %d. "
                         "psrngiun in particular was repinned FOR its rung -- "
                         "code 1 is the attestation that retired the tie-break, "
                         "and off it the repin buys nothing."
                         % (val, V.get(val), code))
    for w in SUPERSEDED:
        if seen.get(w, 0):
            fails.append("%s renders %d time(s) again. Batch 215 put that `y` "
                         "there as a stated consistency fix, not a claim, and "
                         "the register spells the slot without it (psrngiun, "
                         "psrngion, rngii, rngiun -- four forms, no y)."
                         % (w, seen[w]))

    # 2 -- the card is the argument. Five dark slots are what made one pale
    # value worth an instrument; if they go the ruling has nothing under it.
    for w in SLANGI:
        if w not in V:
            fails.append("SLANGI slot %s is no longer verified. srngiun was "
                         "reached BECAUSE its card was five-eighths dark and "
                         "the pale value was one letter off a dark sibling."
                         % w)

    # 3 -- the register facts the ruling rests on, re-read from the file. The
    # positive half AND the negative half: the negative is what refuses -an.
    lex = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                                encoding="utf-8")))
    for w in LISTED:
        if w not in lex:
            fails.append("%s is no longer in attested_modern.json. The whole "
                         "ruling is that the register spells this root's "
                         "syncopated stem, and spells it without a y." % w)
    an = sorted(w for w in lex
                if re.search(r"(rngi|ngari|rangi)(y?an)$", w))
    if an:
        fails.append("the register now lists %s -- an -an form of this root. "
                     "That is exactly the evidence batch 220 looked for and "
                     "did not find, and it re-opens rngiyan/pnsrngiyan."
                     % an)

    # 4 -- the refusals. Re-check the pallor is still there and still alone.
    for word, why in sorted(REFUSED.items()):
        if word not in seen:
            fails.append("%s no longer renders anywhere. It was refused "
                         "because %s -- if the map changed, the refusal needs "
                         "re-arguing, not deleting." % (word, why))
        elif seen[word] != unv.get(word, 0):
            fails.append("%s renders %d time(s) and only %d are pale. It was "
                         "refused because %s"
                         % (word, seen[word], unv.get(word, 0), why))

    # 5 -- the row this batch bought, named
    blocked = [x for x in r["rows"] if x["bad"]]
    print("rows touching the ruling: %d   still blocked: %d"
          % (len(r["rows"]), len(blocked)))
    for x in blocked:
        print("   BLOCKED %-9s %-62s bad=%s" % (x["hw"], x["t"], x["bad"]))
    if len(r["rows"]) < 1:
        fails.append("no row carries the ruled values, batch 220 bought 1 "
                     "(SLANGI). A count is a snapshot of a growing book, so "
                     "this asserts a floor -- a FALL is the news.")
    if blocked:
        fails.append("%d of the rows this batch bought are blocked again: %s"
                     % (len(blocked), [x["bad"] for x in blocked]))

    # 6 -- the audio wiring. build_entries.py no longer reproduces it (batch
    # 219); an id is a URL, so this stays an invariant of every batch.
    ids = audio_ids(read_entries())
    if len(ids) != AUDIO_IDS:
        fails.append("entries.js carries %d attached audio ids, batch 220 "
                     "measured %d. A RISE means build_entries.py was re-run "
                     "and minted ids onto examples that had none; a FALL means "
                     "clips were unhooked." % (len(ids), AUDIO_IDS))

    # 7 -- green
    print("green spans: %d %s" % (r["green"], sorted(r["greens"])))
    if r["green"] != GREEN:
        fails.append("green moved to %d spans, batch 220 measured %d (%s). "
                     "Green means no map entry fired; a rise is a generator "
                     "regression, a fall wants a ledger row."
                     % (r["green"], GREEN, sorted(r["greens"])))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
