# -*- coding: utf-8 -*-
"""Batch 178: back navigation. Verdict lines only, no card bodies."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

B = "http://127.0.0.1:8765/"
ok = fail = 0


def t(name, cond, extra=""):
    global ok, fail
    if cond:
        ok += 1
        print("PASS  %s" % name)
    else:
        fail += 1
        print("FAIL  %s   %s" % (name, extra))


def kind(pg):
    """What is on screen, in one word."""
    return pg.evaluate("""() => {
      if (document.body.classList.contains('home')) return 'home';
      if (document.querySelector('.letter-head')) return 'letter:' +
        document.querySelector('.letter-head-l').textContent.trim();
      const c = document.querySelectorAll('#results > article');
      if (c.length === 1) {
        const a = c[0];
        if (a.classList.contains('slot')) return 'slot';
        if (a.classList.contains('word')) return 'word';
        return 'entry:' + (a.querySelector('.hw') || {textContent:''}).textContent.trim();
      }
      return 'search:' + c.length; }""")


with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context()
    ctx.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg = ctx.new_page()

    # --- 1. ?l= deep link, and an A-Z row opens its card ---
    pg.goto(B + "?l=B")
    pg.wait_for_timeout(2500)
    t("?l=B renders the listing", kind(pg).startswith("letter:B"), kind(pg))
    h0 = pg.evaluate("history.length")
    pg.eval_on_selector("#results .entry.idx[data-entry]", "e => e.click()")
    pg.wait_for_timeout(400)
    k_entry = kind(pg)
    t("A-Z row opens one card", k_entry.startswith("entry:"), k_entry)
    t("...and pushed exactly one entry",
      pg.evaluate("history.length") == h0 + 1, pg.evaluate("history.length"))
    t("...and the URL is shareable",
      "?q=" in pg.url, pg.url)
    pg.go_back()
    pg.wait_for_timeout(500)
    t("BACK returns to the B listing", kind(pg).startswith("letter:B"), kind(pg))
    t("...with ?l= back in the bar", "?l=B" in pg.url, pg.url)
    pg.go_forward()
    pg.wait_for_timeout(500)
    t("FORWARD returns to the card", kind(pg) == k_entry, kind(pg))

    # --- 2. the spelling toggle is a redraw, not a navigation ---
    h1 = pg.evaluate("history.length")
    tog = pg.query_selector("#results .spell-toggle")
    if tog:
        tog.click()
        pg.wait_for_timeout(400)
        t("toggle pushes nothing", pg.evaluate("history.length") == h1,
          pg.evaluate("history.length"))
        t("...and keeps the same card on screen",
          kind(pg).startswith("entry:"), kind(pg))
        tog2 = pg.query_selector("#results .spell-toggle")
        if tog2:
            tog2.click()
            pg.wait_for_timeout(400)
    else:
        print("SKIP  no spell-toggle on this card")

    # --- 3. a slot link is one tap; back leaves it ---
    pg.goto(B + "?l=S")
    pg.wait_for_timeout(2500)
    row = pg.query_selector("#results .entry.idx-slot[data-slot]")
    if row:
        h2 = pg.evaluate("history.length")
        row.click()
        pg.wait_for_timeout(400)
        t("slot row opens the slot card", kind(pg) == "slot", kind(pg))
        t("...one history entry", pg.evaluate("history.length") == h2 + 1)
        pg.go_back()
        pg.wait_for_timeout(500)
        t("BACK out of a slot card", kind(pg).startswith("letter:S"), kind(pg))
    else:
        print("SKIP  no slot row under S")

    # --- 4. crossref is two taps and one history entry ---
    pg.goto(B + "?q=BAGA")
    pg.wait_for_timeout(2500)
    start = kind(pg)
    cr = pg.query_selector("#results .crossref-link[data-ref]")
    if cr:
        h3 = pg.evaluate("history.length")
        cr.click(); pg.wait_for_timeout(300)
        t("first tap on a crossref navigates nothing", kind(pg) == start, kind(pg))
        pg.query_selector("#results .crossref-link[data-ref]").click()
        pg.wait_for_timeout(500)
        t("second tap navigates", kind(pg) != start, kind(pg))
        t("...one history entry", pg.evaluate("history.length") == h3 + 1,
          pg.evaluate("history.length"))
        pg.go_back()
        pg.wait_for_timeout(500)
        t("BACK out of a crossref", kind(pg) == start, kind(pg))
    else:
        print("SKIP  no crossref on BAGA")

    # --- 5. typing is one navigation, not one per keystroke ---
    pg.goto(B)
    pg.wait_for_timeout(2000)
    t("bare URL is home", kind(pg) == "home", kind(pg))
    h4 = pg.evaluate("history.length")
    pg.fill("#search", "baga")
    pg.press("#search", "Enter")
    pg.wait_for_timeout(600)
    pg.fill("#search", "bagan")
    pg.press("#search", "Enter")
    pg.wait_for_timeout(600)
    pg.fill("#search", "bagu")
    pg.press("#search", "Enter")
    pg.wait_for_timeout(600)
    t("three searches = one history entry",
      pg.evaluate("history.length") == h4 + 1, pg.evaluate("history.length"))
    pg.go_back()
    pg.wait_for_timeout(600)
    t("BACK from a search reaches home", kind(pg) == "home", kind(pg))

    # --- 6. a word-page link is one tap, and Back leaves it ---
    pg.goto(B + "?q=mnkyayung")
    pg.wait_for_timeout(2500)
    t("a word page ranks first from ?q=",
      pg.evaluate("(document.querySelector('#results > article')||{className:''})"
                  ".className.indexOf('word') >= 0"))
    pg.goto(B + "?q=KYAYONG")
    pg.wait_for_timeout(2500)
    start2 = kind(pg)
    wl = pg.query_selector("#results .word-link[data-word]")
    if wl:
        h5 = pg.evaluate("history.length")
        wl.click(); pg.wait_for_timeout(500)
        t("word link opens the word page", kind(pg) == "word", kind(pg))
        t("...one history entry", pg.evaluate("history.length") == h5 + 1)
        pg.go_back(); pg.wait_for_timeout(500)
        t("BACK out of a word page", kind(pg) == start2, kind(pg))
    else:
        print("SKIP  no word link on KYAYONG")

    # --- 6b. the in-app Back button: shown only where it does something ---
    pg.goto(B + "?l=B")
    pg.wait_for_timeout(2500)
    vis = lambda: pg.eval_on_selector("#btn-back", "e => e.offsetParent !== null")
    t("no Back at the head of the trail", not vis())
    pg.eval_on_selector("#results .entry.idx[data-entry]", "e => e.click()")
    pg.wait_for_timeout(400)
    t("Back appears after one tap", vis())
    deep = kind(pg)
    pg.eval_on_selector("#btn-back", "e => e.click()")
    pg.wait_for_timeout(600)
    t("Back button returns to the listing", kind(pg).startswith("letter:B"), kind(pg))
    t("...and hides itself again", not vis())

    # --- 7. no card-count regression: the whole dictionary still renders ---
    pg.goto(B + "?q=%CC%81")
    pg.wait_for_timeout(15000)
    n = pg.evaluate("document.querySelectorAll('#results > article.entry').length")
    t("whole-dictionary census still 1967 cards", n == 1967, n)

    br.close()

print("\n%d pass, %d fail" % (ok, fail))
