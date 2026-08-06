# -*- coding: utf-8 -*-
"""[batch 222] Price the twice-carded queue before working any of it.

`twice211.py` enumerates the headwords he carded TWICE, where a token-keyed map
can serve only ONE of the two senses and the other card renders dark and wrong.
It reports the flag. It does not report the COST of fixing one, and the cost is
the whole decision — batch 205 refused DIMA and QALO because "a remap would
paint four correct sentences wrong to fix three heads".

So count. For each flagged token, walk every occurrence in the book and file it
under the card it sits on:

  SERVED   renders on the card whose sense the map value already carries
  ORPHAN   renders on the card the map value does NOT carry -- dark and wrong
  OTHER    renders anywhere else, sense unknown from position alone

A remap is worth pricing only where ORPHAN > SERVED + OTHER. Everything else is
batch 205's refusal, and this prints it as a number instead of an argument.

OTHER is not noise to be ignored: it is the term that decides most rows, and it
cannot be resolved from position — it needs his Chinese, one sentence at a time.
It is on the LEFT of the test, not printed beside it: the first version compared
ORPHAN against SERVED alone and reported seven payable rows, of which `iso→isu`
你 had OTHER=146 and `daxa→dha` 二 had OTHER=263. A favourable SERVED/ORPHAN
split is not a favourable total.

Two limits, both recorded rather than patched, because batch 222 closed the queue:

  - the count includes tokens inside his parenthesised apparatus. His
    `Pqaya (Est-ce de la R. QAYA ?)` contributes a second `qaya` to the ORPHAN
    column that is a French cross-reference, not a Truku claim (batch 208). Read
    the occurrences before trusting a 2.
  - a SERVED/ORPHAN split is scored on the map value's register row, and a row
    is not the register's answer — the family is (batch 200). `qaya`'s bare row
    reads 工具;財物 and manufactured an orphan out of his 妨礙 card, which the
    register in fact serves through `qmaya` 阻礙, `qyaan` 被擋住 and `pqaya` 掛.

    python tools/orthography/logs/twiceprice.py
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

TOK = re.compile(r"[A-Za-zÀ-ɏ'’ʼ\"]+")
HAN = re.compile(r"[一-鿿]")
# his parenthesised notes -- apparatus, stripped before any gloss scoring
NOTE = re.compile(r"[（(][^）)]*[）)]")

s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
mp = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
a = mp.index("window.MODERN_MAP = {")
MM = dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                     mp[a:mp.index("\n};", a) + 2], re.M))
g = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"),
                      encoding="utf-8"))


def wordkey(w):                        # app.js wordKey(), exactly
    return re.sub(r'[’ʼ"ʔ]', "'",
                  (w or "").lower()).replace("ł", "l")


def val(raw):
    k = wordkey(raw)
    v = MM.get(k)
    if v is None:
        v = k.replace("o", "u").replace("l", "r").replace("x", "h")
    return v


def G(w):
    v = g.get(w)
    return " ".join(v) if isinstance(v, list) else (v or "")


# --- the twice-carded class: a HEADWORD string carded on two different roots
by_hw = collections.defaultdict(list)
for i, e in enumerate(E):
    hw = wordkey((e.get("hw") or "").strip())
    if hw:
        by_hw[hw].append(i)
TWICE = {k: v for k, v in by_hw.items() if len(v) > 1}


def card_tokens(e):
    """every occurrence of any token on this card, headword and examples"""
    out = []
    f = e.get("hw") or e.get("form") or ""
    out.extend(TOK.findall(f))
    for x in (e.get("examples") or []):
        out.extend(TOK.findall(x.get("t") or ""))
    for sb in (e.get("subs") or []):
        out.extend(card_tokens(sb))
    return out


rows = []
for hw, idxs in sorted(TWICE.items()):
    v = val(hw)
    gl = G(v)
    if not HAN.search(gl):
        continue                       # no register gloss -> nothing to serve
    chars = set(HAN.findall(gl))
    # which card does the map value's gloss actually carry? Score against his
    # DEFINITION, not his apparatus: his parenthesised notes are prose about the
    # word and routinely contain 人/名/樹 incidentally (batch 218 -- a gloss
    # score can land on the apparatus). Unstripped, `xalong`'s 松樹 card scored
    # as SERVED by a value glossed 人名（男）, on the 人 of 太魯閣人.
    served, orphan = [], []
    for i in idxs:
        zh = NOTE.sub("", (E[i].get("zh") or ""))
        (served if (set(HAN.findall(zh)) & chars) else orphan).append(i)
    if not served or not orphan:
        continue                       # serves both, or neither -- not the shape
    ns = sum(1 for i in served for t in card_tokens(E[i]) if wordkey(t) == hw)
    no = sum(1 for i in orphan for t in card_tokens(E[i]) if wordkey(t) == hw)
    inside = set(served) | set(orphan)
    other = 0
    for j, e in enumerate(E):
        if j in inside:
            continue
        other += sum(1 for t in card_tokens(e) if wordkey(t) == hw)
    rows.append((no - ns, hw, v, ns, no, other,
                 (E[served[0]].get("zh") or "")[:14],
                 (E[orphan[0]].get("zh") or "")[:14]))

rows.sort(key=lambda r: (r[4] - r[3] - r[5], r[0]), reverse=True)
print("%-12s %-12s %5s %6s %6s  %-14s %-14s"
      % ("his token", "renders as", "SERV", "ORPHAN", "OTHER", "served sense",
         "orphan sense"))
worth = 0
for d, hw, v, ns, no, other, zs, zo in rows:
    pays = no > ns + other
    flag = "  <-- ORPHAN beats SERVED+OTHER" if pays else ""
    worth += 1 if pays else 0
    print("%-12s %-12s %5d %6d %6d  %-14s %-14s%s"
          % (hw, v, ns, no, other, zs, zo, flag))
print("\n%d twice-carded tokens flagged, %d where a remap could pay"
      % (len(rows), worth))
