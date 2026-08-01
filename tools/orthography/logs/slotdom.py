# -*- coding: utf-8 -*-
"""Does a paradigm slot have a page, and can the reader reach it?

The feature is generated, so the check has to be the reader's own path: find
KUGUS, click the word on his ° line, and read what comes up. Also asks the two
questions the change could have broken -- the A-Z listing (slot rows are merged
into it) and the spelling toggle (which now has to follow a row that is not a
FORMS record).
"""
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

U = "http://127.0.0.1:8765"
fail = []
def ck(name, got, want=True):
    ok = (got == want) if want is not True else bool(got)
    print("%-52s %s   %s" % (name, "ok " if ok else "FAIL", got))
    if not ok:
        fail.append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.add_init_script("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    # 1. the root card, and its ° line
    pg.goto(U + "/?q=kugus")
    pg.wait_for_timeout(1500)
    par = pg.locator("article.entry p.paradigm").first
    ck("KUGUS ° line present", par.count() > 0)
    print("   ° line:", par.inner_text())
    links = pg.evaluate("""() => Array.from(
        document.querySelectorAll('article.entry p.paradigm .slot-link'))
        .map(s => [s.textContent, s.getAttribute('data-slot')])""")
    print("   slot links on it:", links)
    ck("° line offers >= 2 slot links", len(links) >= 2)

    # 2. tap one, ONE tap, and read the card
    pg.locator("article.entry p.paradigm .slot-link").last.click()
    pg.wait_for_timeout(600)
    card = pg.locator("article.entry.slot")
    ck("one tap opens a slot card", card.count() == 1)
    txt = card.inner_text() if card.count() else ""
    print("---- slot card ----\n" + txt + "\n-------------------")
    ck("card names a focus/焦點", "focus" in txt or "焦點" in txt)
    ck("card carries the generated-form note", "does not define" in txt)
    ck("card names its root", pg.locator(".slot-parent").count() == 1)
    ck("card shows its own ° line", pg.locator("article.entry.slot p.paradigm").count() == 1)
    own = pg.evaluate("""() => document.querySelectorAll(
        'article.entry.slot p.paradigm .slot-link').length""")
    print("   slot links on its own ° line:", own)
    exs = pg.locator("article.entry.slot .conc-row").count()
    print("   example sentences borrowed:", exs)

    # 3. the root link at the top goes back
    pg.locator(".slot-parent").click()
    pg.wait_for_timeout(600)
    ck("root link returns to a real entry",
       pg.locator("article.entry.slot").count() == 0
       and pg.locator("article.entry").count() > 0)

    # 4. a sentence elsewhere in the book links word by word
    pg.goto(U + "/?q=kgusi")
    pg.wait_for_timeout(1200)
    ck("kgusi resolves to a slot card", pg.locator("article.entry.slot").count() == 1)
    n = pg.locator("article.entry.slot .conc-row").count()
    ck("kgusi carries its example sentences", n > 0)
    print("   kgusi examples:", n)

    # 5. the A-Z listing merges them
    pg.goto(U + "/")
    pg.wait_for_timeout(1200)
    pg.click("#btn-alpha")
    pg.wait_for_timeout(500)
    pg.get_by_text("K", exact=True).last.click()
    pg.wait_for_timeout(1500)
    rows = pg.locator(".entry.idx-slot").count()
    head = pg.locator(".letter-head").inner_text()
    ck("letter K holds slot rows", rows > 0)
    print("   K head:", head, " slot rows", rows)
    ordered = pg.evaluate("""() => {
        const r = Array.from(document.querySelectorAll('article.entry.idx'));
        return r.map(e => (e.querySelector('.stub-hw, .hw') || e).textContent.trim());
    }""")
    srt = sorted(ordered, key=lambda s: s.lower())
    ck("the merged column is alphabetical", ordered == srt)
    if ordered != srt:
        for a, c in zip(ordered, srt):
            if a != c:
                print("   first divergence: got %r want %r" % (a, c)); break

    # 6. the toggle follows a slot page rather than dropping it
    pg.goto(U + "/?q=kgusi")
    pg.wait_for_timeout(1200)
    before = pg.locator("article.entry.slot .hw").inner_text()
    # The ° mark on the card IS the toggle (spellMark / .spell-toggle).
    pg.locator("article.entry.slot .spell-toggle").first.click()
    pg.wait_for_timeout(800)
    after_n = pg.locator("article.entry.slot").count()
    after = pg.locator("article.entry.slot .hw").inner_text() if after_n else ""
    ck("toggling keeps the slot card", after_n == 1)
    print("   headword modern %r -> pecoraro %r" % (before, after))

    b.close()

print()
ck("page errors", len(errs), 0)
if errs:
    print(errs[:5])
print("FAILURES: %d %s" % (len(fail), fail))
