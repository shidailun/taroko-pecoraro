# -*- coding: utf-8 -*-
"""batch 221 — six refusals, and an instrument whose only hit was its own bug.

No pairs. The metric stands at 5,331 where batch 220 left it. What this batch
produced is written refusals for the four families in the tail that had never
been looked at, and a reproducible negative result over the rest.

### The four families

Every blocker in the `no root` class with two or more pairs already carries a
written refusal. Four types had **no prior mention anywhere** — not in the batch
log, not in a `dom*.py` pin. Each was reversed to his own token first, because
the ranking reports map VALUES (batch 219), and then asked batch 204's question:
does a DIFFERENT, attested word carry his meaning?

**SA'MUL** 把（嬰兒）抱在懷裡－抱著孩子 — `smmul`, `snmul`, 2 pairs. The
register's 抱 family is large and lives entirely on `abuh`: `kmeabuh` is glossed
帶種子袋;挖成窪地;**抱在懷裡**, which is his headword verbatim, and `seabuh`
用毯子抱在懷裡, `keabuh` 抱著, `mnabuh` 抱過, `smeabuh` 常常抱. Beside it
`qrapu` 擁抱 and `duuy`. Nothing shaped like `samul` — the nearest are `smulus`
拉著, `smuling` 汙辱, `smuluh` 娶近親違反習俗, three different meanings on three
different roots. Note the whole card is pale, head included: this is not a pale
slot beside dark ones, so batch 199's cheapest-question instrument does not
apply. Different root, nothing to respell.

**SYULING** 皮癬－濕疹－蕁麻疹 — `syuring`, `msyuring`, 2 pairs. His own
headword gloss is `?? .` ／ ??（意義不明）: **he did not know what the word
meant**, and only his example glosses it. The register's skin-disease root is
`bkiluh`, some fifty forms of it, plus `tgsu` 老人癬. No `syuring`-shaped word
carries any of it. Name the derived form, not the root: bare `bkiluh` is glossed
苦瓜;釋迦（植物名）and the 疥癬 is on `embkiluh` 長疥癬 / `knbkiluh` 疥癬的樣子 —
this log's own assertion refused `bkiluh` as the carrier, which is batch 200
working on the person writing the refusal. Same for 領袖: `bukung` alone is
校長；首長, and the gloss is on `thowlang` 王、領袖或頭目 and `kbukung` 成為領袖.

**TEUMUK** 首領－負責人－小王, 1 pair. The register's 首領／領袖／頭目 is
`bukung` (a family of a dozen) and `thowlang` 王、領袖或頭目. Neither is within
reach of `teumuk` by any correspondence in the map.

**XBUGI** 吸！－舔食！(his own tag: forme nominale-impérative), 1 pair. The
register's 吸 is `hgut` 去吸（抽） / `gut` / `cip`, and 舔食 returns **zero**
rows in the whole register — the only 舔 anywhere is `pshpaha` 讓…吻（舔）, off
`hpah`. No `hbug`-shaped word exists: `bugan`, `gbuguk` 箭袋, `pstnbugay` are
the whole neighbourhood.

### The instrument, and the one hit it produced

`logs/tail221.py` mechanizes the question: reverse the blocker to his token,
take his Chinese, and report the register word carrying a shared Han character
that is CLOSEST IN SHAPE. Run over the fourteen largest blockers it returns what
CLAUDE.md predicts of any gloss test run at scale — noise. Twelve of fourteen
rows share a single common character (著, 子, 一, 人, 名, 便) at 2–4 edits.

Exactly one row looked real: `mqlaq` → **`mqraq`, one edit, sharing 抓**. It is
the freeze batch 218 removed, at a cost of three pairs. His MQLAQ headword is
發癢 and `mqraq` is 抓 (seize, not scratch); they share no character, and zero of
the 43 register words glossing 癢 are q-shaped.

The 抓 came from **his example's gloss, not his headword's** — the tool falls
back to the sentence when a token has no headword Chinese, and the row is marked
`EX` for exactly that reason. So the single apparent candidate in the entire
tail is batch 203's rule showing up as an artefact of the fallback. Discount the
six `EX` rows and the tail has no candidates at all.

That is the negative result, and it is why the file is kept: **the tail is
refusals, and this is the run that shows it.** Don't rebuild it (cf.
`freezesweep.py`).

### What this log asserts

  1. the six refused values still render, still pale, still alone
  2. the register facts each refusal rests on, re-read from
     `attested_gloss.json` — the positive half (his meaning IS carried, by
     `kmeabuh` / `embkiluh` / `thowlang` / `hgut`) and the negative half (no
     word shaped like his carries it)
  3. the negative control: `mqlaq` still maps to ITSELF, and its value is not
     `mqraq`. The identity pin is load-bearing, because `charRules` spells
     `mqraq` on its own (batch 218).
  4. the metric floor, the denominator, green, and the audio-id invariant
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
  const greens = [], seen = {}, unv = {};
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
      if (!sp.filter(s => !s.classList.contains('w-mod')).length) ok++;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv,
          green: green, greens: greens}; }"""

FLOOR = 5331
DENOM = 5429
GREEN = 2
AUDIO_IDS = 5134

# refused this batch -- the rendered value -> why the pallor is correct
REFUSED = {
    "smmul": "his SA'MUL 抱在懷裡 is carried by kmeabuh, verbatim, off abuh; "
             "the nearest samul-shaped words are smulus 拉著 and smuling 汙辱",
    "snmul": "same card as smmul, and the whole card is pale head included -- "
             "there is no dark sibling to reason from",
    "syuring": "his own headword gloss is ??（意義不明）; the register's "
               "skin-disease root is bkiluh 疥癬 throughout",
    "msyuring": "same card as syuring",
    "teumuk": "首領 is bukung and thowlang, neither within reach of teumuk by "
              "any correspondence in the map",
    "hbugi": "吸 is hgut/gut/cip and 舔食 returns zero rows in the whole "
             "register; no hbug-shaped word exists",
}

# the positive half of each refusal: his meaning IS in the register, on a word
# that is not a respelling of his. value -> (register word, character of his it
# must still carry). If one of these stops carrying it the refusal is unfounded.
# Note WHICH form is named. This assertion refused two of its own first picks:
# the bare `bkiluh` is glossed 苦瓜;釋迦（植物名）, a plant, and `bukung` alone is
# 校長；首長. The 疥癬 and the 領袖 sit on the DERIVED forms -- batch 200's "a
# single gloss row is not the register's answer; the family is", enforced here
# against the person writing the refusal.
CARRIERS = {
    "smmul": ("kmeabuh", "抱"),
    "syuring": ("embkiluh", "癬"),
    "teumuk": ("thowlang", "領"),
    "hbugi": ("hgut", "吸"),
}

# the negative half: no word shaped like his carries the meaning. These are the
# shapes the refusals say do not exist -- a regex over the register, not a list.
NO_SHAPE = {
    "抱": r"a?mul$",
    "癬": r"syu|siu",
    "領": r"^t?[ei]?umuk",
    "吸": r"hbug|bug[iu]$",
}


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    # modern_map.js writes keys with NO leading whitespace; verified.js writes
    # them with two (batch 207).
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def audio_ids():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
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

    M = read_map()
    seen, unv = r["seen"], r["unv"]

    # 1 -- the refusals. Still there, still pale, still alone.
    for word, why in sorted(REFUSED.items()):
        if word not in seen:
            fails.append("%s no longer renders anywhere. It was refused "
                         "because %s -- if the map changed, the refusal needs "
                         "re-arguing, not deleting." % (word, why))
        elif seen[word] != unv.get(word, 0):
            fails.append("%s renders %d time(s) and only %d are pale. It was "
                         "refused because %s"
                         % (word, seen[word], unv.get(word, 0), why))

    # 2 -- the register facts, both halves. A refusal that says "a different
    # root carries this" is only as good as the row it names.
    g = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"),
                          encoding="utf-8"))

    def G(w):
        v = g.get(w)
        return " ".join(v) if isinstance(v, list) else (v or "")

    for word, (carrier, ch) in sorted(CARRIERS.items()):
        if ch not in G(carrier):
            fails.append("%s was refused because %s carries %s and is a "
                         "different root; %s's gloss now reads %r and no "
                         "longer carries it -- the refusal has lost its "
                         "positive half."
                         % (word, carrier, ch, carrier, G(carrier)[:40]))
    for ch, pat in sorted(NO_SHAPE.items()):
        hits = sorted(w for w in g
                      if ch in G(w) and re.search(pat, w))
        if hits:
            fails.append("the register now lists %s -- a word matching /%s/ "
                         "that carries %s. Every refusal in this batch rests "
                         "on no such word existing, so this re-opens one."
                         % (hits[:4], pat, ch))

    # 3 -- the negative control. tail221.py's single edit-1 hit was mqraq, and
    # mqraq is the freeze batch 218 paid three pairs to remove. The identity pin
    # is load-bearing: charRules spells mqraq off mqlaq on its own.
    if M.get("mqlaq") != "mqlaq":
        fails.append("map mqlaq -> %s. Batch 218 reverted the tier-B freeze "
                     "onto mqraq 抓 at a cost of 3 pairs -- his head is 發癢, "
                     "the two share no character, and zero of the 43 register "
                     "words glossing 癢 are q-shaped. The identity pin is what "
                     "stops charRules spelling mqraq on its own."
                     % M.get("mqlaq"))

    # 4 -- the audio wiring. build_entries.py no longer reproduces it (batch
    # 219); an id is a URL, so this stays an invariant of every batch.
    ids = audio_ids()
    if len(ids) != AUDIO_IDS:
        fails.append("entries.js carries %d attached audio ids, batch 221 "
                     "measured %d. A RISE means build_entries.py was re-run "
                     "and minted ids onto examples that had none; a FALL means "
                     "clips were unhooked." % (len(ids), AUDIO_IDS))

    # 5 -- green
    print("green spans: %d %s" % (r["green"], sorted(r["greens"])))
    if r["green"] != GREEN:
        fails.append("green moved to %d spans, batch 221 measured %d (%s). "
                     "Green means no map entry fired; a rise is a generator "
                     "regression, a fall wants a ledger row."
                     % (r["green"], GREEN, sorted(r["greens"])))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
