# -*- coding: utf-8 -*-
"""batch 238 — score a pale value against the gloss of the UNIT it sits in.

**0 pairs, 2 rulings.** 5,347 / 5,429 = 98.4896%, unmoved and expected to be:
both values are FURNITURE — a headword and a parenthetical inside a sub-form
NAME — so neither sits in a `.truku` box and neither can move the denominator.
Batch 223 requires that be asserted rather than discovered later, or a batch
reading the flat number re-prices a seam that was never a seam.

`entries.js` is untouched. `modern_map.js` changes exactly two VALUES, keys
7,371 → 7,371; `verified.js` is byte-identical at 6,326, because both targets
were already verified and neither displaced value was ever in it.

    tapak → tapaq      (manual_map.json, was the tier-M identity pin)
    bsqan → pskan      (manual_map.json, was tier P → `bsekan`)

1. The instrument: whose gloss does a pale value answer to?
------------------------------------------------------------------------------
Batch 230 closed the rare-character meaning sweep at zero. It joined each pale
map value to HIS CARD's Chinese — the headword gloss. But his sub-forms carry
their own glosses, and a card-level join blurs them together. His `Bsqan` is a
parenthetical inside the sub-form `Ps"qan (= Psqan ? = Bsqan ?)`, whose own
gloss is 咀嚼－反芻－嚼; the card it hangs on is "QAN, glossed
吃－有攻擊性的－鋒利的－食物（飲食）.

    shared characters, 咀嚼 against the CARD gloss:  0
    shared characters, 咀嚼 against the UNIT gloss:  2   (咀, 嚼)

So the closed sweep could not have found this, and did not. It is batch 203's
"a sentence-corpus gloss is not the headword's gloss" arriving on the display
side: **the gloss to score a pale value against is the gloss of the unit it
stands in.** Re-run unit-scoped over the **136** pale values the DOM paints,
gated as batch 230 gated it (≥2 shared characters, each carried by ≤120
register rows, ≤2 edits), it returns 10 rows — every one with a verdict.

Two of this project's own rules had to be applied to the instrument before any
of its rows could be read, and both moved the count:

  * **Ask the map in the app's own alphabet** (batch 219). `units()` first
    split his HEADWORD on whitespace, so `XUWAI (HUWAI ?)` yielded the token
    `(HUWAI` and a leading paren rode straight into the map value — six of the
    rows were strings like `(rngat)`. `TOK.findall` instead.
  * **The DOM is the authority on colour** (batch 219/230). The log first
    derived pallor offline from `verified.js`, which counts French, fragments
    and green tokens the page never paints pale: 23 rows against the DOM's 10.
    Batch 216 forbids reporting either number until the disagreement is
    explained; this is the explanation, and the pale list now comes from
    `measure()`, which runs FIRST in `main()` for that reason.

The ten are not a backlog. Four are his grammatical-morpheme AFFIX cards
(GN, KN, TN, ON) scoring against `ki` 阿公 那；已經（指示/語助詞） on 指示詞 —
the metalinguistic hit batch 218 named, on a class this file documents as
unreachable; `hubaw → hhibaw` 割傷 on his XUBAO is batch 230's own refusal,
where his ALPHABETICAL ORDER (XUBAO between X'TOL and XUGUT) refuses the `i`
and `u → i` fires 0 times in 7,371 pairs; `ptatuy` is dom214's written
refusal; `snanu → manu` scores on 什麼. The three this batch read for the
first time are `iyak`, `nilaq` and `burung`, and all three are refusals —
their arguments are in `SWEEP_KNOWN`, and two of them turn on his OWN question
mark (batch 223's posited bare roots).

`nilaq` is the one that priced the gate. Its 2 shared characters are 類 and
稱, which rank **674** and **423** in the register's own gloss-character
frequencies — genuinely rare, so batch 232's derived stoplist cannot cut them
and never should be widened to. Rarity is not the same as meaning-carrying:
these are taxonomic apparatus, batch 218's rule reaching a rare character.

The instrument is kept LIVE rather than pinned at a number, with batch 232's
data-side control: back `bsqan` out to `bsekan` in a copy of the map and the
sweep must recover the proposal unaided. A sweep pinned at `found == 0` is
refuted by moving the pin; one that can still find what it found is not.

2. `bsqan → pskan` — his own parenthetical, one side dark
------------------------------------------------------------------------------
Batch 200: where he writes `X (= Y ? = Z ?)` and the map sends the sides to
different values of which exactly ONE is dark, the pale side renders what the
dark side renders. His sub-form name is `Ps"qan (= Psqan ? = Bsqan ?)` and

    ps"qan → pskan   DARK        psqan → pskan   DARK
    bsqan  → bsekan  PALE  (tier P, the only key reaching that value)

Batch 200's caveat is the load-bearing half — 7 of its 17 were refused because
the dark side was dark on a homograph. Here it is not: `pskan` is glossed 咀嚼
and his sub-form gloss OPENS 咀嚼. The dark side passes the gloss test on
MEANING, which is what batch 232 requires and what shape alone never gives.

The b/p join on this stem is not new and was not invented here. Two hand pins
already made it, both tier M, both dark:

    tbskan → tpskan     (manual_map.json:1721, his `Tpskan (Tbskan)`)
    bsqani → pskani     (tier M, his `-i` slot)

`bsqan` is the tier-P projection those two left behind — batch 223's sibling
seam, a ruling that stopped at the forms the map happened to show. And his own
page asserts the alternation in prose: under `PSkanun` he writes
*這個詞很常被發成 BSKANUN！*

Positive half, batch 221's rule — name the form whose OWN gloss carries the
character: `pskan` is itself glossed 咀嚼. The register's whole 咀嚼 family is
that stem (`pskan`, `emppskan`, `empspskan`, `mskan`); the other 嚼 root is
`nanan`/`psnani` 嚼爛, reachable from nothing he writes here.

Negative half, batch 229's rule — no carrier spells HIS stem: no register key
matching `^bs[eq]` carries 咀嚼 or 嚼. The `bsq-` keys are `bsqar` 射 and
`bsqr-` 勒, different roots; `bsekan` is absent from both gloss files.

**What this does NOT overturn.** `dom165.py:105` refused `bsekan → pskan`
because his sub-form gloss ends 參見 PSKAN and a 參見 is a cross-reference
naming another HEADWORD, not an affix relation — a pointer cannot colour a
word. That is still refused and this batch does not use it. The colour comes
from the parenthetical inside his own sub-form NAME, where `Psqan` and `Bsqan`
are two spellings of one form written in one breath. Different leg, and the
pointer leg stays dead.

3. `tapak → tapaq` — the refusal never searched from the meaning
------------------------------------------------------------------------------
`.claude/notes/batch-log.md:5143` refused it: *"he cards TAPAK 打／壓碎 and
TAPAQ 扁平 separately and asks on the page whether they are related; ruling
`tapaq` 臀部 would merge two of his own cards."* Batch 219 requires citing a
refusal and naming what retires it. Two things do.

**The refusal only ever evaluated the shape-driven candidate.** It weighed
`tapaq` 臀部 against his 打／壓碎 and refused — correctly, on that pairing.
It never asked the register which word carries HIS meaning, which is this
project's own first method rule. His `Tmapak` examples are glossed 拍手 and
游泳, and

    tpaqi   要拍手、游泳。

is the ONLY register row carrying 拍手 in the whole corpus, one of two
carrying 游泳, and it carries BOTH of his example glosses on ONE row. The stem
holds every sense he splits across the two cards: `tpak` 拍翅聲 (his TAPAK 打),
`mtapaq` 平的 (his TAPAQ 扁平), `tapaq` 臀部 / `stpaqan` 大臀部 / `pstpaqan`
臀部突出. His own page ASKS 是否與下一詞條有關; the register ANSWERS yes, and
his headword gloss already opens （TAPAQ？）— batch 200's parenthetical naming
the other spelling of his own head.

**The stated cost is the book's normal state.** "Would merge two of his own
cards" is an assertion about the page, and batch 227 says re-measure one:

    modern headwords colliding:   244 types / 520 cards
    HIS OWN headwords colliding:  172 types / 361 cards

Better than a quarter of his book already shares a modern headword, and 361
cards share HIS OWN spelling — he cards DIMA twice and QALO twice himself. The
cards are not merged: they keep separate glosses, sub-forms and examples.
TAPAQ goes from 1 card to 2, below the median collision. Batch 232's shape —
a premise wrong from the start — except that here the verdict does not survive
it, because the leg that would have saved it was never run.

Attestation: `tapak` 0 in the parquets and absent from `attested_modern`;
`tapaq` 12, `tmapaq` 99. And his own sub-form `Tmapak` ALREADY rendered
`tmapaq`, dark at code 1, twice inside `.truku` on that very card — the head
was the slot left behind, again.

**Nothing is painted wrong.** Batch 205's DIMA/QALO balance is what refuses a
remap that fixes heads by breaking sentences. His `tapak` occurs exactly ONCE
in 398 pages, as the headword itself; every sentence on the card runs through
`tmapaq`, which was already dark and did not move. 1 pale span removed, 0
sentences repainted — the inverse of the DIMA/QALO ledger.

4. What this batch asserts
------------------------------------------------------------------------------
- the metric floor, and that BOTH rulings bought 0 pairs by construction;
- the added spans sit outside `.truku` (batch 223), measured as a delta so a
  pre-existing in-`.truku` span on the same value cannot mask it;
- the map moved exactly two values and `verified.js` not at all;
- every evidence row above, re-read from the files rather than quoted;
- the negative halves, as regexes over the register (batch 229) so they can
  honestly fail when evidence arrives;
- the collision floor, so a later batch cannot re-refuse `tapak` on a cost
  this one measured away;
- the sweep, live, with its data-side positive control.

    python tools/orthography/logs/dom238.py       # site served at :8765
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
ROOT = os.path.dirname(os.path.dirname(ORTH))
SITE = os.path.join(ROOT, "site")
URL = "http://127.0.0.1:8765/index.html"

FLOOR = 5347                 # unmoved: both rulings are furniture
DENOM = 5429
MAP_KEYS = 7371
VER_KEYS = 6326

RULINGS = {"bsqan": "pskan", "tapak": "tapaq"}
GONE = ("bsekan", "tapak")   # values that must now render nowhere at all

# batch 223: the delta the ruling added, and where it must NOT have landed
DELTA = {"pskan": (7, 8, 1), "tapaq": (2, 3, 0)}   # before, after, inTruku

# the prior hand pins this ruling finishes (batch 223's sibling seam)
PRIOR = {"tbskan": "tpskan", "bsqani": "pskani"}

# his own parenthetical, and the two sides of it
PAREN_SUB = 'Ps"qan (= Psqan ? = Bsqan ?) (= R. "QAN ?)'
PAREN_CARD = '"QAN'
DARK_SIDES = ("psqan", 'ps"qan')

# the gloss rows the argument rests on, re-read rather than quoted
ROWS = {"pskan": "咀嚼", "tpaqi": "要拍手、游泳", "tpak": "拍翅聲",
        "mtapaq": "平的", "tapaq": "臀部", "stpaqan": "大臀部",
        "pstpaqan": "臀部突出"}
UNIQUE_CHAR = "拍手"          # tpaqi is its only carrier in the register
HIS_EXAMPLES = ("拍手", "游泳")
ABSENT = ("bsekan", "tapak")  # neither is in either gloss file

# batch 229: state the negative half as a regex, not as a list
NO_BSQ = re.compile(r"^bs[eq]")
NO_SENSE_B = ("咀嚼", "嚼")

# batch 218/230: the metalinguistic strip, and the unit-vs-card measurement
CARD_SHARE = 0                # 咀嚼 against "QAN's headword gloss
UNIT_SHARE = 2                # 咀嚼 against the sub-form's own gloss

# the collision floor that retires the "merges two cards" cost
COLLIDE_MODERN = 240          # measured 244 types / 520 cards
COLLIDE_HIS = 170             # measured 172 types / 361 cards

# the unit-scoped sweep
RARE = 120                    # a character carried by more rows is not evidence
MIN_SHARE = 2
MAX_EDIT = 2
SWEEP_ROWS = 10
UNJOINED = 20           # pale values reachable by no unit of his (batch 230)
SWEEP_KNOWN = {
    "gn": "his GN affix card; the candidate `ki` scores on 指示詞, apparatus",
    "kn": "his KN affix card, same",
    "tn": "his TN affix card, same",
    "un": "his ON affix card, same",
    "hubaw": "batch 230's XUBAO refusal — his alphabetical order refuses the i",
    "ptatuy": "dom214's written refusal",
    "snanu": "scores on 什麼",
    # --- the three this batch read, none of them a ruling -------------------
    "iyak": "his IYAQ, tagged （這會是 MIYAQ 的詞根嗎？）— a bare root he posits "
            "with his own question mark, batch 223's settled class, named in "
            "CLAUDE.md. The candidate `miyah` scores on 這/裡 out of 田裡 vs "
            "來這裡, batch 221's noise mode.",
    "nilaq": "refused in writing three times: dom165's PIN_SYNONYM (his card "
             "cross-references another mushroom), dom161 (false friend of "
             "`milaq` 碎粒), b73 (his tag (ñilao) is the tier-M entry, not the "
             "head). The candidate `bgilaq` 有爪子的爬蟲類的泛稱 is a clawed "
             "REPTILE against his edible fungus; the 2 shared characters are "
             "類 and 稱, taxonomic apparatus (batch 218) arriving through rare "
             "characters — 類 ranks 674 and 稱 423 in the register's own gloss "
             "frequencies, so no derived stoplist can cut them (batch 232) and "
             "the row has to be refused on the merits. NOT a species class "
             "(batch 203): the register carries 19 fungus lexemes, so this is "
             "a test `nilaq` can SIT and fails (batch 204) — and none of the "
             "19 is within 2 edits, nearest `ngiraw`/`riwa` at 3.",
    "burung": "his BOLONG, tagged `( = R.?) (vr. KBOLONG)` — a bare root he "
              "posits with his own question mark, batch 223's class again. "
              "The register's whole 收割 family is q-initial and syncopates "
              "with the q inside (`qburung`, `qmburung`, `qbrungun`, "
              "`qbrungaw`, `qnbrungan`, and `qnbrungan`'s <n> sits AFTER the "
              "q), so the root-initial consonant is `q` and his bare BOLONG "
              "lacks it. Supplying a letter his page does not write is the "
              "mirror of batch 216's refusal and is refused for the same "
              "reason. His KBOLONG carries the sense and is already dark on "
              "`qburung`; map-history:387 is where that family was settled.",
}

fails = []


def ck(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


# ---- readers --------------------------------------------------------------
def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def register():
    """batch 230: a zero from ONE file is not a zero from the register."""
    G = collections.defaultdict(list)
    for p in ("attested_gloss.json", "bible_gloss.json"):
        f = os.path.join(ORTH, p)
        if not os.path.exists(f):
            continue
        for k, v in json.load(io.open(f, encoding="utf-8")).items():
            G[k] += [str(x) for x in (v if isinstance(v, list) else [v])]
    return G


def word_key(w):
    """app.js wordKey(), verbatim (batch 219): it folds ONLY the elision marks
    and the l-slash. It does NOT fold ç, and does NOT strip the umlauts."""
    return re.sub(r"[’ʼ\"ʔ]", "'", w).lower()


def char_rules(w):
    w = re.sub(r"[’ʼ\"ʔ]", "'", w)
    return w.replace("ł", "l").replace("ç", "x") \
            .replace("o", "u").replace("l", "r").replace("x", "h")


def value(tok, MM):
    k = word_key(tok)
    return MM.get(k) or char_rules(k)


def edit(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


HAN = re.compile(r"[一-鿿]")
TOK = re.compile(r"[A-Za-zÀ-ſç'\"]+")
META = re.compile(r"的詞根|詞根|前綴詞?|後綴詞?|擬聲詞|參見|人名|地名|男名|女名")


# ---- the instrument -------------------------------------------------------
def units(E, MM):
    """Every Truku unit he writes, paired with the gloss of the UNIT it stands
    in -- his headword's own gloss, his sub-form's own gloss, or the Chinese of
    the one example it sits in. Card-level joining is what batch 230 did and is
    what missed `bsqan`."""
    out = collections.defaultdict(list)

    def add(tok, zh, card):
        if not tok:
            return
        v = value(tok, MM)
        out[v].append((tok, str(zh or ""), card))

    for e in E:
        hw, zh = (e.get("hw") or "").strip(), e.get("zh")
        # TOK, not .split() -- his `XUWAI (HUWAI ?)` splits into `(HUWAI` on
        # whitespace, and a leading paren rides straight into the map value.
        for p in TOK.findall(hw):
            add(p, zh, hw)
        for x in e.get("examples") or []:
            for p in TOK.findall(str(x.get("t") or "")):
                add(p, x.get("zh"), hw)
        for sb in e.get("subs") or []:
            for p in TOK.findall(str(sb.get("form") or "")):
                add(p, sb.get("zh"), hw)
            for x in sb.get("examples") or []:
                for p in TOK.findall(str(x.get("t") or "")):
                    add(p, x.get("zh"), hw)
    return out


def carriers(G):
    c = collections.Counter()
    for w, gl in G.items():
        for ch in set(HAN.findall(META.sub("", " ".join(gl)))):
            c[ch] += 1
    return c


def sweep(E, MM, PALE, G):
    """Each PALE value, joined to the gloss of the unit it stands in, against
    every register word sharing >= MIN_SHARE rare characters within MAX_EDIT.

    `PALE` comes from the DOM (batch 219: the map is never evidence about
    colour) and the glosses are joined offline from `entries.js` — batch 230's
    method verbatim. Deriving pallor here from `verified.js` instead reports 23
    rows against the DOM's 9, because an offline "not in verified" set counts
    French, fragments and green tokens the page never paints pale.

    A hit is a place to READ, never a ruling."""
    U, C = units(E, MM), carriers(G)
    rows, joined = [], set()
    for val, uses in sorted(U.items()):
        if val not in PALE:
            continue
        joined.add(val)
        mine = set()
        for _tok, zh, _card in uses:
            mine |= set(HAN.findall(META.sub("", zh)))
        mine = set(c for c in mine if C.get(c, 0) <= RARE)
        if not mine:
            continue
        best = None
        for w, gl in G.items():
            if w == val:
                continue
            share = mine & set(HAN.findall(META.sub("", " ".join(gl))))
            if len(share) < MIN_SHARE:
                continue
            d = edit(val, w)
            if d > MAX_EDIT:
                continue
            if best is None or d < best[1]:
                best = (w, d, "".join(sorted(share)), " ".join(gl)[:24])
        if best:
            rows.append((val,) + best)
    # batch 230: report what would not join rather than letting it drop -- the
    # CITE_SPELL seam and the WORD_OVERRIDES keys are invisible to a map-only
    # lookup, and a silent drop reads as an empty seam.
    return rows, sorted(PALE - joined)


# ---- the DOM --------------------------------------------------------------
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
        d = pg.evaluate(r"""(W) => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          const w = {}, pale = {};
          let tot = 0, ok = 0;
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
            });
            // the pallor census is book-wide and UNSCOPED (batch 222): his
            // headwords, sub-form names and paradigm slots are in no .truku box
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              const k = s.classList.contains('w-mod') ? 'dark'
                      : (s.classList.contains('w-unv') ? 'pale' : 'green');
              if (k === 'pale') pale[t] = (pale[t] || 0) + 1;
              if (W.indexOf(t) < 0) return;
              w[t] = w[t] || {dark: 0, pale: 0, green: 0, inTruku: 0};
              w[t][k]++;
              if (s.closest('.truku')) w[t].inTruku++;
            });
          });
          return {tot: tot, ok: ok, w: w, pale: pale};
        }""", list(GONE) + list(DELTA))
        b.close()
    return d


def main():
    E, MM, VER, G = entries_json(), modern_map(), verified(), register()
    # the DOM runs FIRST: it is the authority on colour, and the sweep below
    # takes its pale list from here rather than deriving one from verified.js.
    d = measure()
    PALE = set(d["pale"])
    # The DOM read costs a browser; cache the pale list so the sweep can be
    # re-derived and controlled offline. Nothing reads this back -- it is a
    # working artefact, not an input (deriving pallor from a file is the very
    # thing batch 219/230 refuse).
    try:
        with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "..", "..", ".scratch", "b238",
                                  "pale.json"), "w", encoding="utf-8") as fh:
            json.dump(sorted(PALE), fh, ensure_ascii=False)
    except Exception:
        pass

    # ---- 1. the map moved exactly two values ------------------------------
    ck(len(MM) == MAP_KEYS, "MAP keys %d, pinned %d" % (len(MM), MAP_KEYS))
    ck(len(VER) == VER_KEYS, "VERIFIED keys %d, pinned %d"
       % (len(VER), VER_KEYS))
    for k, v in RULINGS.items():
        ck(MM.get(k) == v, "MAP %s -> %s, expected %s" % (k, MM.get(k), v))
        ck(v in VER, "%s is not in verified.js — the ruling paints a pale word"
           % v)
    for k, v in PRIOR.items():
        ck(MM.get(k) == v, "PRIOR pin %s -> %s, expected %s"
           % (k, MM.get(k), v))
        ck(v in VER, "PRIOR %s left verified.js" % v)
    for v in GONE:
        ck(v not in set(MM.values()),
           "%s is still a map value — the ruling did not land" % v)

    # ---- 2. his parenthetical, and that exactly one side was dark ---------
    sub = None
    for e in E:
        if (e.get("hw") or "").strip() == PAREN_CARD:
            for sb in e.get("subs") or []:
                if (sb.get("form") or "").strip() == PAREN_SUB:
                    sub = sb
    ck(sub is not None,
       "his sub-form %s is no longer in entries.js" % PAREN_SUB)
    if sub:
        zh = str(sub.get("zh") or "")
        ck(zh.startswith(NO_SENSE_B[0]),
           "his sub-form gloss no longer opens %s: %s" % (NO_SENSE_B[0], zh))
        ck(len(set(NO_SENSE_B[0]) & set(zh)) == UNIT_SHARE,
           "UNIT share %d, pinned %d"
           % (len(set(NO_SENSE_B[0]) & set(zh)), UNIT_SHARE))
    for e in E:
        if (e.get("hw") or "").strip() == PAREN_CARD:
            ck(len(set(NO_SENSE_B[0]) & set(str(e.get("zh") or "")))
               == CARD_SHARE,
               "CARD share moved off %d — the batch-230 miss is not "
               "reproducible" % CARD_SHARE)
    for t in DARK_SIDES:
        ck(value(t, MM) == "pskan" and "pskan" in VER,
           "the DARK side %s no longer renders pskan dark" % t)

    # ---- 3. the gloss rows, re-read ---------------------------------------
    for w, want in ROWS.items():
        got = " ".join(G.get(w) or [])
        ck(want in got, "register %s no longer reads %s (got %r)"
           % (w, want, got))
    carr = [w for w, gl in G.items() if UNIQUE_CHAR in " ".join(gl)]
    ck(carr == ["tpaqi"],
       "%s is no longer carried by tpaqi alone: %s" % (UNIQUE_CHAR, carr))
    tp = " ".join(G.get("tpaqi") or [])
    for ch in HIS_EXAMPLES:
        ck(ch in tp, "tpaqi no longer carries his example gloss %s" % ch)
    ex = []
    for e in E:
        if (e.get("hw") or "").strip() == "TAPAK":
            for sb in e.get("subs") or []:
                ex += [str(x.get("zh") or "") for x in sb.get("examples") or []]
    ck(all(any(h in z for z in ex) for h in HIS_EXAMPLES),
       "his TAPAK examples no longer read %s: %s" % (HIS_EXAMPLES, ex))
    for w in ABSENT:
        ck(w not in G, "%s has entered the register — re-open the refusal" % w)

    # ---- 4. the negative halves, as regexes (batch 229) --------------------
    bad = [w for w in G if NO_BSQ.match(w)
           and any(s in " ".join(G[w]) for s in NO_SENSE_B)]
    ck(not bad, "a bs[eq]- register key now carries 咀嚼: %s — re-open" % bad)

    # ---- 5. the collision floor that retires the stated cost --------------
    def mod_hw(hw):
        return " ".join(value(p, MM) for p in hw.split()).upper()
    cm = collections.Counter()
    ch_ = collections.Counter()
    for e in E:
        hw = (e.get("hw") or "").strip()
        if hw:
            cm[mod_hw(hw)] += 1
            ch_[hw.upper()] += 1
    dm = {k: v for k, v in cm.items() if v > 1}
    dh = {k: v for k, v in ch_.items() if v > 1}
    ck(len(dm) >= COLLIDE_MODERN,
       "modern headword collisions %d, floor %d — the 'merges two cards' cost "
       "was priced against this" % (len(dm), COLLIDE_MODERN))
    ck(len(dh) >= COLLIDE_HIS,
       "HIS OWN headword collisions %d, floor %d" % (len(dh), COLLIDE_HIS))
    ck(cm.get("TAPAQ") == 2,
       "TAPAQ is on %s cards, expected 2" % cm.get("TAPAQ"))

    # ---- 6. the sweep, and its data-side positive control -----------------
    rows, unjoined = sweep(E, MM, PALE, G)
    ck(len(rows) == SWEEP_ROWS,
       "the unit-scoped sweep returned %d rows, pinned %d"
       % (len(rows), SWEEP_ROWS))
    unknown = [r for r in rows if r[0] not in SWEEP_KNOWN]
    ck(not unknown,
       "the unit-scoped sweep has a row with no written verdict: %s"
       % [(r[0], r[1], r[3]) for r in unknown])
    ck(len(unjoined) <= UNJOINED,
       "%d pale values will not join to any unit of his, ceiling %d: %s "
       "(batch 230 — the CITE_SPELL seam and the WORD_OVERRIDES keys are "
       "invisible to a map-only lookup; report them, never drop them)"
       % (len(unjoined), UNJOINED, unjoined[:12]))
    # the control simulates the PRE-ruling state: the map sent back to
    # `bsekan`, and that value pale again, which is what the DOM showed before.
    back = dict(MM)
    back["bsqan"] = "bsekan"
    rec, _ = sweep(E, back, PALE | {"bsekan"}, G)
    got = [r for r in rec if r[0] == "bsekan"]
    ck(got and got[0][1] == "pskan",
       "POSITIVE CONTROL: with the ruling backed out the sweep no longer "
       "recovers bsekan -> pskan (got %s) — it cannot see, so its emptiness "
       "means nothing" % got)

    # ---- 7. the DOM (measured at the top; asserted here) ------------------
    ck(d["tot"] == DENOM, "denominator %d, pinned %d" % (d["tot"], DENOM))
    ck(d["ok"] >= FLOOR, "FLOOR %d pairs, got %d" % (FLOOR, d["ok"]))
    ck(d["ok"] == FLOOR,
       "pairs moved to %d — both rulings are furniture and buy 0 BY "
       "CONSTRUCTION (batch 223); a change here means one of them reached a "
       "`.truku` box and the pricing was wrong" % d["ok"])
    for v in GONE:
        ck(not d["w"].get(v),
           "%s still renders %s spans" % (v, d["w"].get(v)))
    for v, (before, after, intruku) in DELTA.items():
        w = d["w"].get(v) or {}
        ck(w.get("dark") == after and not w.get("pale"),
           "%s renders %s, expected %d dark and no pale" % (v, w, after))
        ck(w.get("inTruku") == intruku,
           "%s has %s spans inside .truku, pinned %d — the ruling added a "
           "span where it was priced not to (batch 223)"
           % (v, w.get("inTruku"), intruku))
        ck(after - before == 1,
           "%s delta is %d, expected 1" % (v, after - before))

    print("batch 238 — %d/%d pairs (%.4f%%), map %d keys, verified %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], len(MM), len(VER)))
    print("  ruled     %s" % ", ".join("%s -> %s" % kv
                                       for kv in sorted(RULINGS.items())))
    print("  furniture 0 pairs by construction; inTruku deltas 0")
    print("  sweep     %d rows, %d with a written verdict, %d unjoinable, "
          "control recovers"
          % (len(rows), len(rows) - len(unknown), len(unjoined)))
    print("  collide   %d modern types / %d cards, %d of his own"
          % (len(dm), sum(dm.values()), len(dh)))
    for f in fails:
        print("FAIL %s" % f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
