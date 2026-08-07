# -*- coding: utf-8 -*-
"""batch 237 — does a refusal describe the token it is refusing?

**0 pairs.** 5,347 / 5,429 = 98.4896%, unmoved. `entries.js`, `modern_map.js`
and `verified.js` are all untouched: this batch changes no spelling. It builds
one instrument, reports its result, and repairs one refusal's premise while
leaving the verdict standing.

Batch 231 named the fault and batch 236 hit it again from the other side, so it
was worth asking mechanically how often the record commits it:

    a refusal whose stated reason is about a token that is not the
    token being refused.

`dom219.py:233` refused `isuka` because "蓋住 is spuy" — and the 蓋住 belonged
to `Lmobong`, a different word in the same sentence. `dom216.py:200` refused
`shmqan` because "his GMALYEQ card is headed 詞根不明" — which is his note about
GMALYEQ, the beheading verb, while `sxmqan` is the prison word inside the
example. Both verdicts survived; both premises were about the wrong word.

This is NOT what `logs/premise231.py` swept. That instrument asked whether a
refusal's ABSENCE claim was TRUE, and closed the class at zero. This asks
whether the claim is about the right WORD, which a perfectly true claim can
fail. Different question, different fault, and the two do not overlap.

1. The instrument, and why its filter is self-selecting
------------------------------------------------------------------------------
A Han string quoted inside a refusal is one of two things: a REGISTER gloss the
refusal is citing (`首領 is bukung`) or a quote of HIS gloss. A register gloss
will not appear on his card; a quote of his will. So the flag is

    the run appears SOMEWHERE on his card,
    but NOWHERE in the scope the refused token actually sits in

where a scope is a headword's own gloss, a sub-form's own gloss, or the Chinese
of the one example the token stands in. No stoplist decides that half — his own
card does.

Over the 8 `REFUSED` dicts in the record (dom214–dom221), **75 refusals across
56 values**, that returns **20 rows**. Most are benign: his LIKUT card is glossed
藉口－詭計 and its examples say 找藉口 and 編故事, which is the same meaning in
different words. So the second leg is batch 232's — a shared Han character is
evidence only if it carries meaning — and a run sharing a meaning-carrying
character with the token's own scope is a PARAPHRASE, not a scope fault.

That leaves **10 rows over 8 values**, and reading them gives **3 rows over
2 values**: `shmqan` (twice, repaired in batch 236) and `gnlqan` (repaired
below). The other 7 rows are the character test's own false positives — 詭計
against 編故事, 暴飲暴食 against 又吃又喝 — where the meaning matches and only
the string does not. The instrument does not decide those; reading them does.

A note on building it, because it cost a wrong number on the first pass: the
card-wide text has to be JOINED, not `extend`-ed. Extending a list with a string
extends it by CHARACTERS, so `" ".join()` then puts a space between every Han
glyph and no two-character run can ever be found in it. That silently hid one
row — `pnnguan` against his L'XLAX 鬆脫 — and reported 19.

**Keep the negative result; don't rebuild it**, on the standing of
`freezesweep.py`, `tail221.py` and `premise231.py`. Two faults in 75 refusals,
both already found by hand, neither worth a pair. What the sweep buys is the
containment below: a NEW refusal committing the fault raises the count.

2. `gnlqan` — the refusal read the first of his three senses
------------------------------------------------------------------------------
`dom214.py` refuses `gnlqan` with

    his Gnloq 入鞘 is off LOQ 洞; the map's family value is the grease
    root, dark on the OTHER sense

and the batch log adds *the corpus's only 鞘 word is `hmgluq` 拔刀出鞘*. Two
things are wrong with that as a description of the token.

**His card carries three senses, and the token is in the third.** G'LOQ is
glossed 放入鞘中——刺入——性交, and `Gnl'qan` does not sit on the headword at all:
it is the example under his `Gm'loq` sub-form, glossed

    你是什麼時候侵犯（與之發生關係）這個女孩的？

So the meaning to search is 性交, and the refusal searched 入鞘. Batch 231's
fault exactly — a refusal scoring the CARD's gloss against a word that is not
the card's word.

**And 鞘 is in neither gloss file.** It returns **0 rows** across
`attested_gloss.json` and `bible_gloss.json` together, so the sentence naming
`hmgluq` 拔刀出鞘 was quoting a source the refusal's own test could not see —
batch 230's "a zero from ONE gloss file is not a zero from the register",
arriving as its mirror: a HIT that no gloss file carries either.

**The verdict stands, on the sense the token actually has.** Positive half,
naming the forms whose own glosses carry the character (batch 221): the
register's 性交 is `hmthut` 交媾 / `hut` 交媾 / `kmhthut` 想性交, plus `mux`,
glossed 為「tmeemux 交配」的詞根（單用在人性交方面）, plus `balas` and `smbalas`,
both marked as the animal sense. That is three roots and not one of them is reachable from any spelling of
his G'LOQ — his own `Xg'loq`, `Gm'loq`, `G'qani` and `Gnl'qan` all carry the
`g…lq` skeleton, and `hut`/`mux`/`balas` share no consonant frame with it.
(Bare `hthut` is 腰力, not the sense — batch 221's rule that a refusal must name
the form whose OWN gloss carries the character, caught on this log's first run.)
Negative half, as a regex rather than a list (batch 229): **no register key
matching `g.?n?l.?q` carries any of 性交 / 侵犯 / 交媾 / 鞘**, and `gnlqan`
itself is absent. What the register does list on that skeleton is the grease
root — `gluq` 污垢, `gnluq` 用過防銹油, `gmluq` 做黏貼, `glqan` 被黏合；塗上（柏
油） — and the pull-out root `hgluq` 取所藏匿 / `hmgluq` 抽;拔. Both are dark on
the OTHER sense, so batch 204 refuses letting them license the family.

His `G'qani (Gl'qani ?)` is the one place batch 200's parenthetical rule could
fire, and the register's `glqani` is glossed 拿去出草 — headhunting, not 收刀入
鞘. The dark side fails the gloss test, so following it would spread a freeze,
which is the caveat batch 200 attached to its own rule.

**A premise repair is not a ruling.** `gnlqan` stays pale and keeps sole-blocking
its pairs; nothing is added to `HAND_RULED`, because there is no candidate. The
old sentence is repaired HERE and the old log keeps the sentence being repaired
(batch 232): `dom214.py` is untouched.

    python tools/orthography/logs/dom237.py
"""
import ast
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

FLOOR = 5347                 # this batch spends nothing and gains nothing
DENOM = 5429
AUDIO_IDS = 5134
MAP_KEYS = 7371

# -- section 1, the instrument
REFUSAL_LOGS = ("dom214", "dom215", "dom216", "dom217",
                "dom218", "dom219", "dom220", "dom221")
RAW_FLAGS = 20               # runs on his card, absent from the token's scope
GATED_FLAGS = 10             # ... and sharing no meaning-carrying character
GATED_VALUES = 8             # over this many values; 3 of the rows are real
SCOPE_FAULTS = ("gnlqan", "shmqan")   # what reading the 10 gives
STOP_DEPTH = 30              # batch 232: derived, not hand-picked
# the derivation must reproduce characters the project has NAMED as noise ...
STOP_MUST = "的人不是"
# ... and must not swallow the characters this batch's argument rests on
STOP_MUST_NOT = "鞘性交詭藉暴詞根"

# -- section 2, the gnlqan repair
CARD = "G'LOQ"
CARD_SENSES = ("放入鞘中", "刺入", "性交")
TOKEN_SCOPE = "侵犯"         # the example the token actually sits in
OLD_PREMISE = "入鞘"         # the sense the refusal searched
SHEATH = "鞘"                # ... which no gloss file carries at all
# positive half: the forms whose OWN gloss carries his sense
CARRIERS = {"hmthut": "交媾", "hut": "交媾", "kmhthut": "性交",
            "mux": "交配", "smbalas": "性交"}
# negative half, as a regex over the register (batch 229)
SKELETON = re.compile(r"g.?n?l.?q")
NO_SENSE = ("性交", "侵犯", "交媾", "鞘")
# what the skeleton DOES list -- both dark on the other sense (batch 204)
RIVALS = {"gluq": "污垢", "gnluq": "防銹油", "gmluq": "黏貼",
          "glqan": "黏合", "hmgluq": "拔"}
PARENTHETICAL = ("glqani", "出草")    # batch 200's rule, refused on the gloss

WATCH = ("gnlqan", "shmqan", "gluq", "gnluq", "glqani", "hmgluq")

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
    """every gloss string the files carry, keyed on the modern word. Batch 230:
    a zero from ONE file is not a zero from the register, so both are read."""
    G = collections.defaultdict(list)
    for p in ("attested_gloss.json", "bible_gloss.json"):
        f = os.path.join(ORTH, p)
        if not os.path.exists(f):
            continue
        for k, v in json.load(io.open(f, encoding="utf-8")).items():
            G[k] += [str(x) for x in (v if isinstance(v, list) else [v])]
    return G


def audio_ids():
    ids = set()

    def walk(n):
        for x in (n.get("examples") or []):
            if x.get("a"):
                ids.add(x["a"])
        for s in (n.get("subs") or []):
            walk(s)
    for e in entries_json():
        walk(e)
    return ids


def card(E, hw):
    for e in E:
        if (e.get("hw") or "") == hw:
            return e
    return None


# ---- the instrument -------------------------------------------------------
HAN = re.compile(r"[一-鿿＀-￯]{2,}")
TOK = re.compile(r"[A-Za-zÀ-ſç'\"]+")


def refusals():
    """Every REFUSED/REFUSALS dict in the record, parsed rather than imported:
    a log's module body is not this batch's to execute."""
    out = collections.defaultdict(list)
    for name in REFUSAL_LOGS:
        p = os.path.join(HERE, name + ".py")
        if not os.path.exists(p):
            continue
        tree = ast.parse(io.open(p, encoding="utf-8").read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if not any(n in ("REFUSED", "REFUSALS") for n in names):
                continue
            if not isinstance(node.value, ast.Dict):
                continue
            for k, v in zip(node.value.keys, node.value.values):
                try:
                    kk, vv = ast.literal_eval(k), ast.literal_eval(v)
                except Exception:
                    continue
                if isinstance(kk, str) and isinstance(vv, str):
                    out[kk].append((name, vv))
    return out


def scopes(E, MM):
    """value -> [(card, the token's OWN gloss, every Chinese on the card)]."""

    def char_rules(w):
        w = re.sub(r"[’ʼ\"ʔ]", "'", w).lower()
        return w.replace("ł", "l").replace("ç", "x") \
                .replace("o", "u").replace("l", "r").replace("x", "h")

    def val(t):
        k = re.sub(r"[’ʼ\"ʔ]", "'", t).lower()
        return MM.get(k) or char_rules(k)

    def whole(e):
        out = [str(e.get("zh") or "")]
        for x in (e.get("examples") or []):
            out.append(str(x.get("zh") or ""))
        for s in (e.get("subs") or []):
            out.append(whole(s))
        return " ".join(out)

    S = collections.defaultdict(list)

    def walk(e, hw, all_zh):
        name = (e.get("hw") or e.get("form") or "").strip()
        for w in TOK.findall(name):
            S[val(w)].append((hw, str(e.get("zh") or ""), all_zh))
        for x in (e.get("examples") or []):
            zh = str(x.get("zh") or "")
            for w in TOK.findall(str(x.get("t") or "")):
                S[val(w)].append((hw, zh, all_zh))
        for s in (e.get("subs") or []):
            walk(s, hw, all_zh)

    for e in E:
        walk(e, (e.get("hw") or "").strip(), whole(e))
    return S


def stoplist(G):
    """batch 232: derive it, never hand-pick it."""
    f = collections.Counter()
    for v in G.values():
        f.update(c for c in set("".join(v)) if "一" <= c <= "鿿")
    return set(c for c, _ in f.most_common(STOP_DEPTH))


def sweep(E, MM, G):
    S, STOP = scopes(E, MM), stoplist(G)
    raw, gated = [], []
    for val in sorted(refusals()):
        here = S.get(val) or []
        if not here:
            continue
        for log, why in refusals()[val]:
            for run in sorted(set(HAN.findall(why))):
                if not any(run in s[2] for s in here):
                    continue          # a register gloss, not a quote of his
                if any(run in s[1] for s in here):
                    continue          # the refusal is about the right scope
                own = [s for s in here if run in s[2]][0]
                raw.append((log, val, run, own))
                if not (set(run) & set(own[1]) - STOP):
                    gated.append((log, val, run, own))
    return raw, gated, STOP


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
        d = pg.evaluate(r"""(WATCH) => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          let tot = 0, ok = 0;
          const sole = {}, T = {};
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) { ok++; }
              else {
                const bad = [...new Set(sp
                  .filter(s => !s.classList.contains('w-mod'))
                  .map(s => (s.textContent || '').trim().toLowerCase()))];
                if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
              }
              sp.forEach(s => {
                const t = (s.textContent || '').trim().toLowerCase();
                if (WATCH.indexOf(t) >= 0) {
                  T[t] = T[t] || [0, 0];
                  T[t][s.classList.contains('w-mod') ? 0 : 1]++;
                }
              });
            });
          });
          return {tot: tot, ok: ok, sole: sole, truku: T};
        }""", list(WATCH))
        b.close()
    return d


def main():
    E, MM, VER, G = entries_json(), modern_map(), verified(), register()
    d = measure()

    print("PAIRS %d / %d = %.4f%%   FLOOR %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], FLOOR))
    ck(d["ok"] >= FLOOR, "FLOOR %d pairs, got %d" % (FLOOR, d["ok"]))
    ck(d["tot"] == DENOM, "the denominator is %d, pinned %d"
       % (d["tot"], DENOM))
    ck(len(audio_ids()) == AUDIO_IDS,
       "the audio id set is %d, expected %d -- this batch writes no audio"
       % (len(audio_ids()), AUDIO_IDS))
    ck(len(MM) == MAP_KEYS, "the map has %d keys, pinned %d: batch 237 changes "
       "no spelling at all" % (len(MM), MAP_KEYS))

    # ---- section 1: the instrument reproduces --------------------------
    R = refusals()
    n_ref = sum(len(v) for v in R.values())
    print("\n1. %d refusals over %d values in %s"
          % (n_ref, len(R), "/".join(REFUSAL_LOGS)))
    ck(n_ref >= 75, "the record holds %d refusals in those dicts, expected at "
       "least 75 -- a refusal was DELETED, which the ledger cannot see"
       % n_ref)

    raw, gated, STOP = sweep(E, MM, G)
    print("   %d flagged, %d after the meaning-carrying character gate"
          % (len(raw), len(gated)))
    ck(len(raw) <= RAW_FLAGS,
       "the scope sweep flags %d refusals, pinned at most %d: a NEW refusal "
       "describes a token that is not the token it refuses"
       % (len(raw), RAW_FLAGS))
    ck(len(gated) <= GATED_FLAGS,
       "the gated sweep returns %d rows, pinned at most %d -- the new row is "
       "the one to read" % (len(gated), GATED_FLAGS))
    got = tuple(sorted(set(v for _, v, _, _ in gated)))
    ck(set(SCOPE_FAULTS) <= set(got),
       "the sweep no longer reaches %s; it is the positive control on the "
       "instrument, and losing it means the sweep is blind, not that the "
       "record is clean"
       % ", ".join(sorted(set(SCOPE_FAULTS) - set(got))))

    # batch 232: the stoplist is derived, and its depth is set by the record
    missing = [c for c in STOP_MUST if c not in STOP]
    ck(not missing, "the derived stoplist at depth %d has lost %s, which the "
       "record names as noise: the derivation moved"
       % (STOP_DEPTH, "".join(missing)))
    swallowed = [c for c in STOP_MUST_NOT if c in STOP]
    ck(not swallowed, "the derived stoplist now swallows %s, which this "
       "batch's argument scores ON: the gate would pass a real fault"
       % "".join(swallowed))

    # ---- section 2: the gnlqan repair ----------------------------------
    e = card(E, CARD)
    ck(e is not None, "his %s card is gone from entries.js" % CARD)
    zh = str((e or {}).get("zh") or "")
    for s in CARD_SENSES:
        ck(s in zh, "his %s headword no longer reads %s; the repair says the "
           "card carries three senses and the refusal searched the first"
           % (CARD, s))
    # the sense the refusal searched is on the HEADWORD, and only there --
    # that asymmetry is the whole repair, so assert both ends of it
    ck(OLD_PREMISE in zh, "his %s headword no longer carries %s, which is the "
       "sense dom214's refusal searched" % (CARD, OLD_PREMISE))

    # the token sits in an example, not on the headword
    scope_hit = []
    for sb in (e or {}).get("subs") or []:
        for x in (sb.get("examples") or []):
            if re.search(r"Gnl['’\"]?qan", str(x.get("t") or "")):
                scope_hit.append((sb.get("form"), str(x.get("zh") or "")))
    ck(len(scope_hit) == 1,
       "his Gnl'qan appears in %d example(s), expected exactly 1 -- the repair "
       "rests on the token having ONE scope" % len(scope_hit))
    if scope_hit:
        ck(TOKEN_SCOPE in scope_hit[0][1],
           "the example holding his Gnl'qan no longer says %s; its gloss reads "
           "%s" % (TOKEN_SCOPE, scope_hit[0][1][:40]))
        ck(OLD_PREMISE not in scope_hit[0][1],
           "the token's own scope now carries %s after all, which would retire "
           "the repair" % OLD_PREMISE)

    # 鞘 is in no gloss file: the old sentence quoted an unseeable source
    sheath = [k for k, v in G.items() if any(SHEATH in x for x in v)]
    print("2. %s -> %d register rows; the token's scope says %s"
          % (SHEATH, len(sheath), TOKEN_SCOPE))
    ck(not sheath,
       "%s now returns %d register rows (%s): the refusal's own test can see "
       "the sense at last, and the repair's second leg is retired"
       % (SHEATH, len(sheath), ", ".join(sorted(sheath)[:4])))

    # positive half -- name the form whose OWN gloss carries the character
    for w, ch in sorted(CARRIERS.items()):
        rows = G.get(w) or []
        ck(any(ch in x for x in rows),
           "%s no longer carries %s in its own gloss (%s); the positive half "
           "of the refusal names it as the word that has his sense"
           % (w, ch, (rows[0][:30] if rows else "absent")))

    # negative half -- as a regex, so it can honestly fail
    bad = []
    for k, v in G.items():
        if not SKELETON.search(k):
            continue
        for s in NO_SENSE:
            if any(s in x for x in v):
                bad.append("%s %s" % (k, s))
    ck(not bad, "a register key on his g...lq skeleton now carries his sense "
       "(%s) -- that is the news that re-opens the refusal"
       % ", ".join(sorted(bad)[:4]))
    ck("gnlqan" not in G and "gnlqan" not in verified(),
       "gnlqan is attested now; the refusal rested on its absence")

    for w, ch in sorted(RIVALS.items()):
        ck(any(ch in x for x in (G.get(w) or [])),
           "%s no longer glosses %s: the rivals on his skeleton are what make "
           "this a different-root refusal (batch 204)" % (w, ch))

    w, ch = PARENTHETICAL
    ck(any(ch in x for x in (G.get(w) or [])),
       "%s no longer glosses %s, so batch 200's parenthetical rule is no "
       "longer refused on the gloss and his G'qani (Gl'qani ?) wants re-reading"
       % (w, ch))

    # ---- the verdict is unchanged: pale, still blocking ----------------
    T = d["truku"]
    dark, pale = T.get("gnlqan", [0, 0])
    print("   gnlqan in .truku: %d dark / %d pale; sole-blocks %d pair(s)"
          % (dark, pale, d["sole"].get("gnlqan", 0)))
    ck(dark == 0 and pale > 0,
       "gnlqan renders %d dark / %d pale -- a premise repair is NOT a ruling, "
       "so a value that has gone dark means something else ruled it and this "
       "log's account of why it is pale is stale" % (dark, pale))
    ck(d["sole"].get("gnlqan", 0) >= 1,
       "gnlqan sole-blocks nothing now; the repair was written about a live "
       "blocker")

    print("\n%s" % ("PASS" if not fails else "FAIL"))
    for f in fails:
        print("FAIL %s" % f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
