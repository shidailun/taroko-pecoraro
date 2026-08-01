# -*- coding: utf-8 -*-
"""The About sheet's new paragraph, read off the rendered page.

It states a figure (91.3%), and a figure in prose rots the moment the next
batch lands, so this asserts the prose against the DOM the ⚙ sheet is
measured from -- not against itself.
"""
import re
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)
    print(("  ok   " if cond else "  FAIL ") + msg)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    pg.goto(URL)
    pg.wait_for_timeout(6000)
    counts = pg.evaluate("""() => {
      const o = {};
      for (const c of ['w-mod','w-unv','w-raw'])
        o[c] = document.querySelectorAll('span.'+c).length;
      return o;
    }""")
    pg.click("#btn-about")
    pg.wait_for_timeout(400)
    about = pg.inner_text("#sheet-content")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    pg.click("#btn-settings")
    pg.wait_for_timeout(400)
    settings = pg.inner_text("#sheet-content")
    b.close()

tot = sum(counts.values())
pct = 100.0 * counts["w-mod"] / tot
print("measured %d/%d = %.2f%%" % (counts["w-mod"], tot, pct))

print("\n--- the About sheet says what the colours mean")
for s in ["dark brown", "pale brown", "深棕色", "淺棕色", "⚙"]:
    check(s in about, "About mentions %s" % s)
check("personal name" in about and "人名" in about,
      "About names the commonest reason a word stays pale")

print("\n--- and its figure is the one the page actually shows")
m = re.findall(r"9\d\.\d(?=%)", about)
check(len(m) == 2, "About states the rate twice, EN and ZH (%s)" % m)
for x in m:
    check(abs(float(x) - pct) < 0.05, "About says %s%%, page is %.2f%%" % (x, pct))

print("\n--- the settings sheet still carries the exact counts")
for n in ["40,617", "4,466", "3,832", "2,088", "44,475",
          "40,617 詞次", "3,832 詞次"]:
    check(n in settings, "settings sheet says %s" % n)
check(str(counts["w-mod"]) == "40617" and str(counts["w-unv"]) == "3832",
      "and those counts are the DOM's own (%s)" % counts)

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
