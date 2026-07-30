"""Did the charRules -ao rule land, and did it land ONLY there?

The app.js edit rewrites word-final `-ao` to `-aw` before the o>u replace, for the
unmapped remainder only. Two things to prove in the real DOM, not in a simulation:

  (a) the greens that motivated it now print -AW  -- tao, qnao, nilao, xubao,
      xnubao are the tokens deliberately left unverified, and they were printing
      a shape (-AU) the modern orthography does not use word-finally;
  (b) nothing else moved -- no GREEN span anywhere in the dictionary still ends
      in -AU, and no span ends -AW that is not either a map value or one of his
      -ao/-ai tokens. A rule that fires on shape fires on every shape.
"""
import io, json, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_selector(".entry")
    n = pg.eval_on_selector_all(".entry", "e => e.length")
    rows = pg.eval_on_selector_all(
        ".w-mod, .w-raw",
        "es => es.map(e => [e.className, e.textContent, e.dataset.ref || ''])")
    b.close()

print("%d cards, %d coloured spans" % (n, len(rows)))
au = collections.Counter()
aw = collections.Counter()
for cls, txt, ref in rows:
    w = txt.strip()
    if re.search(r"[aA][uU]$", w):
        au[(w.lower(), "green" if "w-raw" in cls else "brown")] += 1
    if re.search(r"[aA][wW]$", w):
        aw[(w.lower(), "green" if "w-raw" in cls else "brown")] += 1

print("\n-- (a) the five the edit was for --")
want = ["tao", "qnao", "nilao", "xubao", "xnubao"]
seen = {}
for cls, txt, ref in rows:
    k = (ref or txt).strip().lower().replace("\u2019", "'")
    if k in want:
        seen.setdefault(k, set()).add(
            (txt.strip(), "green" if "w-raw" in cls else "brown"))
for w in want:
    print("   %-10s %s" % (w, sorted(seen.get(w, [])) or "NOT ON PAGE"))

print("\n-- (b) every span still ending -AU --")
for (w, c), n2 in sorted(au.items(), key=lambda x: -x[1]):
    mapped = [k for k, v in MAP.items() if v.lower() == w]
    print("   %-14s %-6s %4d  map-value-of %s" % (w, c, n2, mapped[:3] or "-"))
if not au:
    print("   (none)")

green_aw = sum(n2 for (w, c), n2 in aw.items() if c == "green")
print("\n-- (b) -AW totals: %d green occ / %d brown occ, %d types --"
      % (green_aw, sum(n2 for (w, c), n2 in aw.items() if c == "brown"), len(aw)))
print("   green -aw types:", sorted(w for (w, c) in aw if c == "green"))
