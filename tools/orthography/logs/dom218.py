# -*- coding: utf-8 -*-
"""batch 218 — the aging identity pin, a gloss score that landed on the
apparatus, and a freeze paid for at three pairs.

### The instrument: an identity pin is a verdict with a date on it

`.claude/rules/orthography.md` already says an identity entry in tier M is a
verdict reached at a particular time — "no modern form found" — and may be
overturned when a family turns up attested. Nothing had ever asked WHICH pins
had aged. `agepins.py` does: of 174 pale tier-M values, 35 are identity pins,
and 5 of those sit on a card whose OTHER slots are dark. A pin alone on its card
is a verdict about a word nobody has since found. A pin beside dark siblings is
a card contradicting itself, and the siblings are the evidence that was missing
when the pin was written.

Five: `pslangi` (SLANGI), `qlaq` (QLAQ), `qmalit` (QALIT), `sloong` (SLOONG),
`tapak` (TAPAK). Two ruled, one refused, one became this batch's headline, and
one — `qlaq` — is correct as it stands.

### `sloong` -> `sluung`, `pslangi` -> `psrangi`

Both are the cheapest question on the page (batch 199): the card is a paradigm,
so ask what every other slot says. SLOONG's `msluung` 打瞌睡 is dark and the root
`luung` is listed; his 眼皮沉重／睏得快睡著 shares 睡 with it. SLANGI's `srangi`,
`msrangi` and `psrngiyan` are all dark and the register's `psrngiun` 留一些
carries his 使之有剩餘.

They came back on different rungs, and the difference is the evidence: `sluung`
is **code 2**, `regular` — a regular inflection of the LISTED root `luung`,
which is the strongest rung short of being listed itself. `psrangi` is **code
7**, `vouched_root` — an inflection of a root vouched by its own paradigm, which
is what `srangi`/`msrangi`/`psrngiyan` are. A probe that calls the rung
predicates directly reports both as `no_chinese` as well; the ladder is ordered
and short-circuits, so what a predicate ACCEPTS is not what the word is built
on. Read the emitted code, not the probe.

### `qalit` -> `qrib`: a gloss score that landed on the apparatus

QALIT 剪刀 was **tier A**, the gloss-PROVED tier, mapped to `qlit` with a score
of 3. `qlit`'s only register row reads 「是「psqlit 使溢滿」;「sqqlit 溢滿狀」的詞根」
and his own note reads 「QALIT 就只是所有由 QALIP 衍生之詞的詞根」. The three
characters both texts share are **的詞根** — "…'s root". Two texts saying *this
word is the root of something*, scored as agreement about meaning. His scissors
were mapped onto overflowing.

`meta_a.py` re-scores every tier-A entry with metalinguistic phrases stripped
from both sides. 419 carry a register gloss; **418 survive and exactly one
collapses**, `qalit` 3->0. The tier is not broken — one entry was never about
the word.

What it should be is on his own card: 剪刀。（註：如常見的情形，字尾的 P 讀作 T）
— QALIT is QALIP with final P read as T. QALIP is already `qrib`, KALIP 剪、切
（尤指用剪刀）is already `qrib`, and the whole family — `qmrib`, `mqrib`, `pqrib`,
`qriban` — is already dark. The root is gloss-verified from outside by `qribi`
要剪下 and `qribun` 剪成.

The two n-infix slots, `qnrib` and `mnqrib`, went into `HAND_RULED` beside the
four already there. That is not an escalation: NO member of this family is
attested — `qrib`, `qmrib`, `mqrib`, `pqrib`, `qriban` are all 0/0 in both
corpora and all dark by hand ruling alone, resting on the two register
inflections. The n-infix slots are the same status as their four siblings.

Metric movement: **zero**. `qnalit` and `mnqalit` were already dark — on
`qnlit`/`mnqlit`, off the 溢滿 root. The ruling replaced dark-WRONG with
dark-RIGHT, which no colour metric can see, and turned two pale headwords dark.

### `mqlaq` -> `mqlaq`: a tier-B freeze, paid for at three pairs

Tier B is the one tier awarded with no gloss proof — `elif len(safe) == 1`, the
only safe candidate wins whatever it means. `mqlaq` 發癢 was frozen onto `mqraq`
抓, two words sharing no character. The sweep that found it (`tierb.py`) asks
one question of all 1,291 tier-B entries: does the token's own card carry a pale
identity pin? A card whose head reports "no modern form found" while an
inflection lands on an attested word is contradicting itself. **3 of 1,291.**

The refusal of `mqraq`: zero of the 43 register words glossing 癢 are q-initial
or contain `raq`; the modern itch root is `krak` (`mkrak` 很癢) and `ghguh`
皮膚粗糙; the `qraqil` family belongs to his QLAQEL 受苦 card, where he asks on
the page whether it is the same root as KLAQEL 皮膚. The French is
"Démangeaison - prurit". Flagged twice before, in `map-history.md` and in
`batch-log.md`, and never acted on.

**Tier X was considered and refused.** `mkrak` would recover all three pairs and
disclose the original — but batch 204 already ruled that a lexeme modern Truku
replaced is NOT a settled class, and a lexical substitution here is that bulk
clearance wearing a different hat. His 癢 root has no modern reflex. The pallor
is the honest record of that.

Cost: 5,329 -> **5,326**. Priced at 2 by a table-side tool that read the map
only, and `o` has no map entry — `charRules('o')` = `u` and the span renders
dark. A map-keyed darkness test cannot see the char rules. Price from the DOM.

### Refused, and why the pallor is correct

`qlaq`/`sqlaq` — same refusal as `mqraq`; there is no q-shaped itch word to find.
`tapak` — he cards TAPAK 打／壓碎 and TAPAQ 扁平 separately and asks himself on the
page whether they are related. Ruling `tapaq` 臀部 would merge two of his own
cards, which batch 205 forbids.
"""
import io
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "..", "site")
ORTH = os.path.join(HERE, "..")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0, green = 0;
  const greens = [], seen = {}, unv = {}, rows = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    // scope to .truku: unscoped, a pale name in the FRENCH blocks a row whose
    // Truku is entirely dark (batch 208).
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
      if (/qnrib|mnqrib|mqlaq/i.test(t))
        rows.push({hw: hw, t: t.slice(0, 60),
                   bad: bad.map(s => s.textContent.trim())});
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv,
          green: green, greens: greens, rows: rows}; }"""

FLOOR = 5326
DENOM = 5429
GREEN = 2

# the QALIT card, his spelling -> the value batch 218 ruled
QALIT = {"qalit": "qrib", "qmalit": "qmrib", "mqalit": "mqrib",
         "qnalit": "qnrib", "mnqalit": "mnqrib"}
# the two aged pins that were overturned: his token -> (value, emitted code).
# The codes differ and that IS the evidence -- sluung is a regular inflection of
# the listed root luung, psrangi an inflection of a paradigm-vouched root.
PINS = {"sloong": ("sluung", 2), "pslangi": ("psrangi", 7)}
# refused: the rendered form -> why the pallor is correct
REFUSED = {
    "mqlaq": "zero of the 43 register words glossing 癢 are q-initial or "
             "contain raq; the modern itch root is krak/ghguh and mqraq is 抓. "
             "Tier X to mkrak was refused too -- batch 204 ruled that a lexeme "
             "modern Truku replaced is not a settled class",
    "qlaq": "same refusal as mqlaq: there is no q-shaped itch word to find",
}


def read_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    # modern_map.js writes keys with NO leading whitespace; verified.js writes
    # them with two. One regex over both reports every change as no change
    # (batch 207).
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def read_ver():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((k, int(n))
                for k, n in re.findall(r'^  "(.+?)": (\d+),?$', t, re.M))


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

    # 1 -- the QALIT card, every slot on the qrib root
    for tok, val in sorted(QALIT.items()):
        if M.get(tok) != val:
            fails.append("map %s -> %s. Batch 218 ruled it %s: his own note "
                         "says QALIT is QALIP with final P read as T, and "
                         "QALIP/KALIP are already qrib." % (tok, M.get(tok), val))
        if val not in V:
            fails.append("%s is not verified. The whole qrib family is dark by "
                         "HAND_RULED alone -- none of it is attested -- so a "
                         "value dropping out of verified.js means the hand "
                         "ruling was edited, not that evidence moved." % val)

    # 2 -- the freeze it replaced must be gone from the page
    for dead in ("qlit", "qnlit", "mnqlit"):
        if seen.get(dead, 0):
            fails.append("%s renders %d time(s). It is the 溢滿 root; batch 218 "
                         "found QALIT scored 3 against it on 的詞根, which is "
                         "apparatus, not meaning." % (dead, seen[dead]))

    # 3 -- the two aged identity pins, re-deriving the reason
    RUNG = {2: "regular -- a regular inflection of a LISTED root",
            7: "vouched_root -- an inflection of a root vouched by its own "
               "paradigm"}
    for tok, (val, code) in sorted(PINS.items()):
        if M.get(tok) != val:
            fails.append("map %s -> %s, batch 218 overturned the identity pin "
                         "to %s off its card's dark siblings."
                         % (tok, M.get(tok), val))
        if V.get(val) != code:
            fails.append("%s is verified %s, batch 218 built it to code %d "
                         "(%s). A DIFFERENT code is not automatically a "
                         "regression -- but it means the rung this pin was "
                         "overturned on has moved, and the overturn has to be "
                         "re-argued on the new one."
                         % (val, V.get(val), code, RUNG[code]))

    # 4 -- the refusals. Re-check the pallor is still THERE and still alone.
    for word, why in sorted(REFUSED.items()):
        if word not in seen:
            fails.append("%s no longer renders anywhere on the page. It was "
                         "refused because %s -- if the transcription or the "
                         "map changed, the refusal needs re-arguing, not "
                         "deleting." % (word, why))
        elif seen[word] != unv.get(word, 0):
            fails.append("%s renders %d time(s) and only %d are pale. It was "
                         "refused because %s"
                         % (word, seen[word], unv.get(word, 0), why))
        if M.get(word) != word:
            fails.append("%s maps to %s, not to itself. The identity pin is "
                         "load-bearing: charRules(%s) spells %s on its own, so "
                         "deleting the entry restores the freeze rather than "
                         "removing it."
                         % (word, M.get(word), word,
                            word.replace("o", "u").replace("l", "r")
                                .replace("x", "h")))

    # 5 -- the three rows the revert cost, named. A count is a snapshot of a
    # growing book (batch 209), so assert the floor, not equality.
    blocked = [x for x in r["rows"] if x["bad"]]
    print("rows touching the ruling: %d   blocked: %d"
          % (len(r["rows"]), len(blocked)))
    for x in r["rows"]:
        print("   %-9s %-60s bad=%s" % (x["hw"], x["t"], x["bad"]))
    if len(blocked) < 3:
        fails.append("only %d row(s) blocked by mqlaq, batch 218 measured 3. A "
                     "FALL is the news: it means something darkened the word "
                     "again." % len(blocked))
    for x in blocked:
        if [w for w in x["bad"] if w.lower() != "mqlaq"]:
            fails.append("a row blocked by mqlaq is also blocked by %s; the "
                         "revert was priced at exactly these three rows"
                         % x["bad"])

    # 6 -- green
    print("green spans: %d %s" % (r["green"], sorted(r["greens"])))
    if r["green"] != GREEN:
        fails.append("green moved to %d spans, batch 218 measured %d (%s). "
                     "Green means no map entry fired; a rise is a generator "
                     "regression, a fall wants a ledger row."
                     % (r["green"], GREEN, sorted(r["greens"])))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
