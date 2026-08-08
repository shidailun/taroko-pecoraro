# -*- coding: utf-8 -*-
"""batch 219 — a probe that asked the map in the wrong alphabet, a letter his
own card writes, and a builder that no longer reproduces its own output.

### The alphabet bug, and why it looked like a seam

The batch opened on a "no-gloss bucket" that seemed to hold seven or more pairs.
It held none. `app.js` `wordKey()` folds ONLY `’ ʼ " ʔ -> '` and `ł -> l`; it
does NOT fold c-cedilla and does NOT strip umlauts. A scratch probe normalised
harder, asked the map for `opix`, missed, fell through to `charRules`, got
`upih`, found it unverified and reported PALE — while the live key `opiç` maps
to `upix`, verified code 16, rendering deeper brown twice on the page.

Seven map keys are reachable in no other spelling: `ilüs`, `iyüs`, `libiç`,
`lübak`, `lübaq`, `opiç`, `xatsö`. **Absence in the wrong alphabet reads as
pallor.** Four assumed values were wrong too (`libiç` is `ribix`, not `libih`;
`lübak` is `lbak`; `xatsö` is `hatu`; `natsö` is `natu`) — read them from
`modern_map.js`, never guess them. The whole bucket dissolved when measured from
the DOM, and `opiç` — which the previous session had queued for a HAND_NAMES
entry — needed no ruling at all.

The same bug was live in `scratchpad/card.py` and is fixed there.

### Corollary: the blocker ranking reports map VALUES, not his tokens

In modern mode a span's textContent is what the map emitted. `shkun`, `tgrgri`
and `ptatuy` are strings that appear nowhere in `entries.js`. Reverse a blocker
to his own spelling before searching his book, or the search returns nothing and
the nothing reads as evidence.

### G'LI" — a letter his own card writes, dropped by a MANUAL pin

`tglgli` and `mtlgli` sat pale beside EIGHT dark slots of his G'LI" 舞蹈 card:
`grig`, `mgrig`, `rmgrig`, `grigan`, `grigun`, `pgrig`, `trgrig`, `tgrgrigun`.
Every one carries a final `g`; the two pale ones did not. His own `Tglgligun ->
tgrgrigun` is one suffix over from `tglgli` and writes it. And the gloss test is
his own text: `TLg'li"` reads 熱烈起勁地跳舞——手舞足蹈, which is verbatim the
QALAS sentence's 手舞足蹈, and `Tglgligun` 將歡騰——將雀躍 is the KTUI 跳舞慶祝.

Restoring the letter verified both at **code 2** off the ladder — the same rung
as `trgrig` and `tgrgrigun` on the same card. No hand ruling.

Note WHERE the missing letter was: `mtlgli -> mtrgri` was **tier M**, hand
pinned. Batch 201's char-rule-contradiction test has to be run over manual
entries too, not only over char-rule output.

### KLULI — an identity pin, and the register asked about the slot, not the word

`pklluyun` rendered ITSELF (tier R), an identity claim that blocks `charRules`.
His card is otherwise settled: `kluli -> qluli` is **tier A, gloss-proved**
(his （河水）流動——被急流沖走——溺水 against `qluli` 溺水), `pkluli -> pqluli`
使之溺水, `mppkluli -> emppqluli`, all dark.

The register lists no `-un` slot for this root at all, so the question was asked
of the shape instead: of listed roots ending in `-uli`, THIRTEEN have a listed
`-un` slot and every one drops the `i` — `bbuli>bbulun`, `csduli>csdulun`,
`quli>qulun`, `skuli>skulun`. None takes `-iun`. Over all i-final roots it is
667 to 6. `pqluli` + `-un` = **`pqlulun`**, which the analyser reaches off both
`pqluli` and `qluli`.

His own parenthetical is what ties the token to the slot: he writes `mppkluli ko
(pklluyun mo)`, offering the one as an alternative to the other.

It emitted **code 6**, `no_chinese` — the rung batch 217 flagged as skipping the
gloss test. That is honest here: the word occurs only inside a sentence and has
no headword gloss of its own to test. The ruling rests on the tier-A root, three
dark siblings, the parenthetical and the 13/13 register unanimity, not on the
rung.

### BYOTOç — a ruling this batch made and then reverted, and three more

`pg'go -> pgagu` was ruled here as batch 200's parenthetical consistency fix:
he writes `daxa pgago (pg'go)`, the two sides went to different values, and only
`pgagu` was dark. The argument offered was that PGAGO is HIS OWN headword,
glossed 斑鳩－鴿子 and 白鴿, against the sentence's 兩隻**斑鳩**.

**That is his gloss of his word, not evidence about the modern one**, and batch
200's own caveat says the dark side still has to pass the gloss test. It does
not: `pgagu` in the register is **笛子**, a flute, one utterance. The register
has no 斑鳩 at all and its 鴿子 is `byutux` — which is what his BYOTOç head
already maps to. So `pgago -> pgagu` has the shape of a homograph freeze, and
following it would have spread one. **dom216 and dom217 had refused this exact
ruling in writing**, naming that reason, and the suite is what caught the
override. Reverted; `pg'go` returns to `pggu` and the row stays blocked.

Three more went in the same direction. `gnlqan`, `hlakuh` and `emphlakuh` were
added to `HAND_RULED` — which darkens whatever is put in it — with **no comment
beside them**, in a file where every other addition carries its argument. They
override dom214 (his Gnloq 入鞘 is off LOQ 洞; the family value is the grease
root, dark on the other sense) and dom217 (his card is 盾牌; `hlak` is 肉片 and
`hlaka` 展翅, and the register's only 盾 is `tgqrung`). No evidence was recorded
for any of the three, and a pin comes down when evidence overturns it, not when
the batch wants the number. All three reverted.

**The four cost five pairs, 5,335 -> 5,330, and the batch's honest gain is +4.**
A metric a batch can move by overriding its own written refusals is not
measuring the book.

Left open, deliberately, and not acted on: whether `pgago -> pgagu` is ITSELF a
freeze. It is dark today and reverting it would cost pairs — batch 218's shape
exactly. That is a ruling of its own and wants its own evidence, not a decision
taken at the end of a batch to tidy up a mistake.

### LUDAN — a transcription slip, and the scan says where the fix goes

`drbiyax` occurs once. His BIYAX card carries a HEADWORD `Dmbiyax` glossed
壯年人的群體,正值壯年者 — which is verbatim the gloss of the disputed example,
`Dludan ni drbiyax` = 長者與年輕人（**正值壯年者**）— and `dmbiyax` occurs three
times and is dark.

Page 177 at 6×: on the same line, `Dludan`'s final `n` and the `n` of `ni` each
have two legs; the disputed glyph has three. It is an `m`, and nothing like an
`r`. The page reads `dmbiyax`, so the fix is a transcription correction in the
source and the map key `drbiyax` disappears — no new spelling claim.

### The builder trap this uncovered

Correcting the slip meant re-running `build_entries.py`, and its output no
longer reproduces the shipped file's audio wiring. Entry counts match exactly
(1,967 / 2,948 / 5,436) so nothing in the diff looks wrong — but HEAD and the
working copy each carry **5,134** attached ids and a plain rebuild emits
**5,427**: 301 minted onto examples that had none, 7 dropped, six of them the
`t == fr` French rows the metric already excludes.

An id is a URL. The rebuild was discarded and the one string patched directly,
asserting `lost=[] new=[]` over the id set. The reworded example KEEPS its old
id — re-minting to `ex_dludan_ni_dmbiyax` would unhook a clip already paid for,
so it joins the known-stale set instead. This log asserts the 5,134 as an
invariant, because the next person to fix a slip will reach for the builder.

### Refused

Eight tail items on batch 204's different-root test, which is the only
non-circular question over pale words: the nearest register word carrying each
meaning is 4 to 7 edits away, so the meaning lives on a different root and there
is no respelling to find. `ayuq` (淋巴腺 — the register has no 淋巴 at all),
`kndutu` (手鐲 is `sirug`/`knrima`), `mtmuhung` (花苞 is `puyuy`), `isuka`
(蓋住 is `spuy`), `nkllu` (公開 is `ura`), `pnnanu` (幼稚 is on `laqi`),
`mngusyeh` (兔唇 is `siras`, pq=0, and there is no derived person-form),
`pnnguan` — and that last one is also batch 203's warning: the card glosses
鬆脫 but the WORD is the 結 in 你打的結總是鬆開, and the register's knot root is
`bkuy`.

`rngiyan` and the LANGI cluster were NOT re-derived: `langi -> rangi` was
investigated as this exact freeze and acquitted in the batch log, and `lngiyan`
is refused there in writing.
"""
import io
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "..", "site")
URL = "http://127.0.0.1:8765/?q=%CC%81"
WAIT = 22000

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0, green = 0;
  const greens = [], seen = {}, unv = {}, cls = {}, rows = [];
  document.querySelectorAll('#results > article.entry').forEach(c => {
    const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
    // scope to .truku, and walk the boxes -- a '.truku ' prefix on a
    // comma-separated selector scopes only the FIRST alternative (batch 216).
    c.querySelectorAll('.truku').forEach(box => {
      box.querySelectorAll(SEL).forEach(s => {
        const t = (s.textContent||'').trim().toLowerCase();
        seen[t] = (seen[t] || 0) + 1;
        if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
        if (s.classList.contains('w-cls')) cls[t] = (cls[t] || 0) + 1;
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
      if (/tgrgrig|mtrgrig|pqlulun|dmbiyax/i.test(t))
        rows.push({hw: hw, t: t.slice(0, 62),
                   bad: bad.map(s => s.textContent.trim())});
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, cls: cls,
          green: green, greens: greens, rows: rows}; }"""

FLOOR = 5330
DENOM = 5429
GREEN = 2
AUDIO_IDS = 5134

# his token -> (value ruled, emitted code). The G'LI" pair came back on the same
# rung as the slots they sit beside; pklluyun on the rung that skips the gloss
# test, which is what its evidence had to make up for.
RULED = {
    "tglgli":   ("tgrgrig", 2),
    "mtlgli":   ("mtrgrig", 2),
    "pklluyun": ("pqlulun", 6),
}

# ruled by this batch and REVERTED by it, four of them. The map value on the
# left must be what the page renders again, and the three HAND_RULED words must
# be pale again -- these are the assertions that make the override visible if
# anyone reinstates it.
REVERTED = {"pg'go": "pggu"}
UNRULED = ("gnlqan", "hlakuh", "emphlakuh")

# the eight dark slots of his G'LI" card. The two ruled values are the only ones
# that ever lacked the final g, and this is what convicted them.
GLI = ["grig", "mgrig", "rmgrig", "grigan", "grigun", "pgrig",
       "trgrig", "tgrgrigun"]

# the seven map keys reachable only with diacritics intact, and what they render.
# A probe that folds c-cedilla or strips umlauts reports these as pale.
DIACRITIC = {"opiç": "upix", "lübaq": "lubaq", "iyüs": "iyus",
             "libiç": "ribix", "lübak": "lbak", "xatsö": "hatu"}

# refused this batch -- the rendered value -> why the pallor is correct
REFUSED = {
    "ayuq": "the register has no 淋巴 at all; the nearest gloss-carrier is "
            "biqir 甲狀腺腫瘤, five edits away and a different root",
    "kndutu": "手鐲 is sirug/knrima/ssmusu, four to five edits away on "
              "different roots -- there is no respelling of his to find",
    "isuka": "蓋住 is spuy, 覆蓋 is bbungan; different roots",
    "nkllu": "公開 is ura/mteura; different roots",
    "pnnanu": "幼稚 is qnlaqi/mglaqi, built on laqi, not on his rbnaw",
    "pnnguan": "his card glosses 鬆脫 but the WORD is the 結 in 你打的結總是鬆開 "
               "(batch 203: a sentence gloss is not the word's gloss), and the "
               "register's knot root is bkuy",
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


def all_tokens(E):
    TOK = re.compile(r"[A-Za-zÀ-ɏ'’ʼ\"]+")
    out = set()

    def walk(e):
        for f in [e.get("hw") or e.get("form") or ""]:
            out.update(w.lower() for w in TOK.findall(f))
        for x in (e.get("examples") or []):
            out.update(w.lower() for w in TOK.findall(x.get("t") or ""))
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
    E = read_entries()
    seen, unv = r["seen"], r["unv"]

    # 1 -- the four rulings, map value and emitted code
    for tok, (val, code) in sorted(RULED.items()):
        if M.get(tok) != val:
            fails.append("map %s -> %s, batch 219 ruled it %s"
                         % (tok, M.get(tok), val))
        if val not in V:
            fails.append("%s is not verified. It was built off its card's own "
                         "family, so a value dropping out means the map or the "
                         "ladder moved under it." % val)
        elif code is not None and V.get(val) != code:
            fails.append("%s is verified code %s, batch 219 built it to %d. A "
                         "different code is not automatically a regression, but "
                         "the rung the ruling was argued on has moved and has "
                         "to be re-argued on the new one." % (val, V.get(val), code))

    # 1b -- the four this batch reverted. dom214/216/217 refuse these in
    # writing; batch 219 overrode all four and put them back. If a rebuild or a
    # later batch reinstates one, it has to argue it there and not here.
    for tok, val in sorted(REVERTED.items()):
        if M.get(tok) != val:
            fails.append("map %s -> %s. Batch 219 ruled it pgagu and REVERTED "
                         "that: pgagu is 笛子 in the register, the register has "
                         "no 斑鳩 at all, and dom216/217 refused this ruling in "
                         "writing. Following the dark side of his parenthetical "
                         "here spreads a freeze." % (tok, M.get(tok)))
    for w in UNRULED:
        if w in V:
            fails.append("%s is verified again. Batch 219 put it in HAND_RULED "
                         "with no comment, overriding a written refusal, and "
                         "reverted it. HAND_RULED darkens whatever is put in "
                         "it, so the metric cannot price this -- the argument "
                         "has to be written beside the word." % w)

    # 2 -- the G'LI" card is what convicted the two pale slots. If its own
    # slots stop being dark the argument is gone, ruling or no ruling.
    for w in GLI:
        if w not in V:
            fails.append("G'LI\" slot %s is no longer verified. tglgli/mtlgli "
                         "were ruled BECAUSE every other slot on the card "
                         "carries the final g and is dark." % w)
    for w in ("tgrgri", "mtrgri"):
        if seen.get(w, 0):
            fails.append("%s still renders %d time(s) -- the g-less value is "
                         "back on the page" % (w, seen[w]))

    # 3 -- the transcription slip. His token must be gone from the book AND
    # from the map; the corrected one must be present and dark.
    toks = all_tokens(E)
    if "drbiyax" in toks:
        fails.append("drbiyax is back in entries.js. Page 177 at 6x shows "
                     "three legs where Dludan's n and ni's n both show two; "
                     "the page reads dmbiyax.")
    if "drbiyax" in M:
        fails.append("the map still carries a drbiyax key. The token no longer "
                     "exists in the book, so a key for it means entries.js was "
                     "reverted or the slip was re-introduced.")
    if "dmbiyax" not in toks:
        fails.append("dmbiyax is not in entries.js at all")
    if "dmbiyax" not in V:
        fails.append("dmbiyax is not verified; the slip was corrected TO it "
                     "because it is his own BIYAX headword, dark, glossed "
                     "正值壯年者 -- verbatim the disputed example's own gloss")

    # 4 -- the audio wiring. build_entries.py no longer reproduces it: a plain
    # rebuild mints 301 ids and drops 7. An id is a URL.
    ids = audio_ids(E)
    if len(ids) != AUDIO_IDS:
        fails.append("entries.js carries %d attached audio ids, batch 219 "
                     "measured %d. A RISE means build_entries.py was re-run "
                     "and minted ids onto examples that had none; a FALL means "
                     "clips were unhooked. Patch the string, do not rebuild."
                     % (len(ids), AUDIO_IDS))
    if "ex_dludan_ni_drbiyax" not in ids:
        fails.append("the reworded example lost its id. It KEEPS the old one "
                     "on purpose -- re-minting to ex_dludan_ni_dmbiyax would "
                     "unhook a clip already recorded and paid for.")

    # 5 -- the alphabet. These keys are reachable only with the diacritics
    # intact, and every one of them renders DARK. If a value here goes pale the
    # generator has started stripping marks on input, not just on output.
    for k, val in sorted(DIACRITIC.items()):
        if M.get(k) != val:
            fails.append("map %s -> %s, batch 219 read %s off modern_map.js. "
                         "These seven keys are the ones a probe that folds "
                         "c-cedilla or strips umlauts can never reach."
                         % (k, M.get(k), val))
        if val in seen and unv.get(val, 0):
            fails.append("%s renders pale %d time(s). It was the whole "
                         "no-gloss 'seam': the pallor was a probe artefact, "
                         "measured from the DOM it is dark."
                         % (val, unv[val]))

    # 6 -- the refusals. Re-check the pallor is still there and still alone.
    for word, why in sorted(REFUSED.items()):
        if word not in seen:
            fails.append("%s no longer renders anywhere. It was refused "
                         "because %s -- if the map changed, the refusal needs "
                         "re-arguing, not deleting." % (word, why))
        elif seen[word] != unv.get(word, 0):
            fails.append("%s renders %d time(s) and only %d are pale. It was "
                         "refused because %s"
                         % (word, seen[word], unv.get(word, 0), why))

    # 7 -- the rows this batch bought, named
    blocked = [x for x in r["rows"] if x["bad"]]
    print("rows touching the ruling: %d   still blocked: %d"
          % (len(r["rows"]), len(blocked)))
    for x in blocked:
        print("   BLOCKED %-9s %-62s bad=%s" % (x["hw"], x["t"], x["bad"]))
    if len(r["rows"]) < 4:
        fails.append("only %d row(s) carry the ruled values, batch 219 bought "
                     "4 (QALAS, KTUI, KLULI, LUDAN). A count is a snapshot of a "
                     "growing book, so this asserts a floor -- a FALL is the "
                     "news." % len(r["rows"]))
    if blocked:
        fails.append("%d of the rows this batch bought are blocked again: %s"
                     % (len(blocked), [x["bad"] for x in blocked]))

    # 8 -- green
    print("green spans: %d %s" % (r["green"], sorted(r["greens"])))
    if r["green"] != GREEN:
        fails.append("green moved to %d spans, batch 219 measured %d (%s). "
                     "Green means no map entry fired; a rise is a generator "
                     "regression, a fall wants a ledger row."
                     % (r["green"], GREEN, sorted(r["greens"])))

    print("\n%d assertions failed" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
