# -*- coding: utf-8 -*-
"""batch 235 — batch 175's hapax test, restricted to the words that block pairs.

Batch 175 ran it book-wide: hapax types with an edit-distance-1 neighbour
occurring >= 10 times, **592 of 7,216**, and called it NOISY and not a fix list
— rightly, because its top rows are `nai`/`ini`, `kala`/`kana`, real distinct
words one letter apart, and short types dominate. It also measured the
one-glyph-as-two class (`rinalox` -> `mnalox`) at 4 rows book-wide.

Neither was ever asked of the PALE. That is where the noise argument stops
applying: a hapax that is the sole blocker of a pair, with a frequent neighbour
of HIS OWN that renders dark, is batch 213's shape exactly — "ask whether the
string is even his before pricing a respelling" — and batch 229 found four glyph
misreadings among nine rows working it by hand.

Reverses the DOM's blocker VALUES back to his tokens first (batch 219): a
blocker named `shkun` may be a string that appears nowhere in `entries.js`.
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
ORTH = os.path.join(H, "tools", "orthography")
SITE = os.path.join(H, "site")
URL = "http://127.0.0.1:8765/index.html"
NEIGHBOUR_MIN = 10


def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def char_rules(w):
    return w.replace("o", "u").replace("l", "r").replace("x", "h")


def toks(E):
    """every Truku token he writes, with its occurrence count."""
    c = collections.Counter()
    for e in E:
        def add(s):
            for t in re.findall(r"[a-zA-Zç'\"à-ü]+", str(s or "")):
                c[t.lower()] += 1
        add(e.get("hw"))
        for x in e.get("examples") or []:
            add(x.get("t"))
        for sb in e.get("subs") or []:
            add(sb.get("form"))
            for x in sb.get("examples") or []:
                add(x.get("t"))
        for p in (e.get("paradigm") or []):
            add(p)
    return c


def ed1(a, b):
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    s, l = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(l)):
        if l[:i] + l[i + 1:] == s:
            return True
    return False


def glyph2(a, b):
    """ONE glyph of his read as two: exactly one char of the shorter string
    stands where two of the longer one do (batch 175's `rinalox` -> `mnalox`).
    Anything looser matches `ubai` against `uda` and the sweep is noise."""
    if abs(len(a) - len(b)) != 1:
        return False
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(s[:i] + l[i:i + 2] + s[i + 1:] == l for i in range(len(s)))


from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(URL)
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto(URL + "?q=%CC%81")
    pg.wait_for_timeout(22000)
    sole = pg.evaluate(r"""() => {
      const SEL = 'span.w-mod, span.w-unv, span.w-raw';
      const sole = {};
      document.querySelectorAll('#results > article.entry').forEach(c => {
        c.querySelectorAll('.truku').forEach(box => {
          const sp = [...box.querySelectorAll(SEL)];
          if (!sp.length || sp.every(s => s.classList.contains('w-mod'))) return;
          const bad = [...new Set(sp.filter(s => !s.classList.contains('w-mod'))
                        .map(s => (s.textContent||'').trim().toLowerCase()))];
          if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
        });
      });
      return sole;
    }""")
    b.close()

E = entries_json()
MM = modern_map()
C = toks(E)
FREQ = [w for w, n in C.items() if n >= NEIGHBOUR_MIN]
print("sole-blocker types %d over %d pairs | his types %d, %d occurring >= %d"
      % (len(sole), sum(sole.values()), len(C), len(FREQ), NEIGHBOUR_MIN))

# reverse the DOM's VALUES back to his tokens (batch 219)
back = collections.defaultdict(set)
for k, v in MM.items():
    back[v].add(k)
for t in C:
    if t not in MM:
        back[char_rules(t)].add(t)

rows = []
for val, npairs in sorted(sole.items(), key=lambda x: -x[1]):
    for his in sorted(back.get(val, ())):
        n = C.get(his, 0)
        if n == 0 or n > 2:            # batch 213: a book that repeats itself
            continue
        for nb in FREQ:
            if nb == his:
                continue
            if ed1(his, nb):
                rows.append((npairs, val, his, n, nb, C[nb], "d1"))
            elif glyph2(his, nb):
                rows.append((npairs, val, his, n, nb, C[nb], "glyph"))

print("\nrare blocker tokens with a frequent neighbour of HIS OWN: %d rows"
      % len(rows))
for npairs, val, his, n, nb, m, kind in sorted(rows, key=lambda r: (-r[0], -r[5])):
    print("  %-14s <- %-12s %dx  ~ %-12s %4dx  %-5s  blocks %d pair(s)  %s"
          % (val, his, n, nb, m, kind,
             npairs, MM.get(nb, char_rules(nb))))
