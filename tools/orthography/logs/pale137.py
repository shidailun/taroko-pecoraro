# -*- coding: utf-8 -*-
"""What is the pale 2,576 made of, asked of the DOM and then of the evidence.

palemake.py decomposed it by SUFFIX and found the paradigm is not where the mass
is. This asks the sharper question: for every pale word actually on screen, what
does the evidence say, and is any of it pale by mistake?

  BUG        the exact modern string IS in attested_modern.json -- it should be
             dark and something in build_verified.py is not reaching it
  corpus     not in the omnibus, but the ILRDF parquets have it at freq >= 2
  hapax      corpus has it exactly once
  nothing    no witness anywhere

Writes pale137.json so later passes can work the list without a browser.
"""
import io, json, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
URL = "http://127.0.0.1:8765/?q=%CC%81"
PALE = """() => {
  const r = {};
  for (const n of document.querySelectorAll('span.w-unv')) {
    const t = n.textContent.trim().toLowerCase();
    if (t) r[t] = (r[t] || 0) + 1;
  }
  return r; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    pg.goto(URL)
    pg.wait_for_timeout(6000)
    pale = pg.evaluate(PALE)
    b.close()

with io.open(os.path.join(HERE, "pale137.json"), "w", encoding="utf-8",
             newline="\n") as f:
    json.dump(pale, f, ensure_ascii=False, indent=0, sort_keys=True)

att = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                            encoding="utf-8")))
pq = json.load(io.open(os.path.join(ORTH, "parquet_truku_freq.json"),
                       encoding="utf-8"))
mp = json.load(io.open(os.path.join(ORTH, "modern_map.json"),
                       encoding="utf-8"))["map"]
by_val = {}
for t, rec in mp.items():
    by_val.setdefault(rec["modern"].lower(), []).append(rec["tier"])

buckets = collections.Counter()
occ = collections.Counter()
lists = collections.defaultdict(list)
for w, n in pale.items():
    if w in att:
        k = "BUG-attested"
    elif pq.get(w, 0) >= 2:
        k = "corpus>=2"
    elif pq.get(w, 0) == 1:
        k = "corpus hapax"
    else:
        k = "no witness"
    buckets[k] += 1
    occ[k] += n
    lists[k].append((n, w, "/".join(sorted(set(by_val.get(w, ["?"]))))))

print("pale types %d   occurrences %d" % (len(pale), sum(pale.values())))
print()
print("%-14s %6s %8s" % ("bucket", "types", "occ"))
for k, v in buckets.most_common():
    print("%-14s %6d %8d" % (k, v, occ[k]))
print()
for k in ("BUG-attested", "corpus>=2", "corpus hapax", "no witness"):
    if not lists[k]:
        continue
    print("--- %s, heaviest 25 ---" % k)
    for n, w, tier in sorted(lists[k], reverse=True)[:25]:
        print("   %-20s %4d   tier %s" % (w, n, tier))
    print()

# Where the mass is by TIER, over the whole pale list.
t = collections.Counter()
to = collections.Counter()
for w, n in pale.items():
    key = "/".join(sorted(set(by_val.get(w, ["?"]))))
    t[key] += 1
    to[key] += n
print("pale by the tier that produced the spelling:")
for k, v in to.most_common(15):
    print("   %-10s %4d types %6d occ" % (k, t[k], v))
