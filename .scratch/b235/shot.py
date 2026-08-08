# -*- coding: utf-8 -*-
"""Exercise the translator sheet the way a translator will, and refuse a page
whose script did not even parse. The escaping bug that flattened `L.join('\\n')`
into a real line break was invisible in every screenshot: the page LOOKED
right, and every button was dead."""
import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
p = os.path.abspath(".scratch/b235/translator.html").replace("\\", "/")
bad = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 900, "height": 1500},
                        permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error"
          else None)
    pg.goto("file:///" + p)
    pg.wait_for_timeout(700)
    if errs:
        bad = 1
        print("JS ERRORS:", errs[:3])

    N = pg.eval_on_selector_all(".answer textarea", "e => e.length")
    print("answer boxes:", N, "| counter:", pg.text_content("#cnt"))
    print("stamp:", pg.eval_on_selector(
        ".sheet", "e => e.dataset.build + ' / ' + e.dataset.qset"))
    print("empty panel:", pg.input_value("#out")[:14])
    pg.screenshot(path=".scratch/b235/shot_top.png")

    # two answers, then the panel must carry both, in his spelling
    pg.fill("#a1", "測試拼法")
    pg.fill("#a3", "沒聽過")
    pg.wait_for_timeout(250)
    txt = pg.input_value("#out")
    print("counter:", pg.text_content("#cnt"),
          "| panel lines:", len(txt.strip().split("\n")),
          "| both present:", "測試拼法" in txt and "沒聽過" in txt)
    print("panel head:", repr(txt.split("\n")[0]))
    print("done marks:", pg.eval_on_selector_all(".q-item.done", "e=>e.length"))

    # jump-to-next lands on an UNANSWERED one
    pg.click("#next")
    pg.wait_for_timeout(400)
    print("next ->", pg.evaluate(
        "document.activeElement.id + ' empty=' + "
        "(document.activeElement.value==='')"))

    # the copy path, and the clipboard actually holding it
    pg.click("#copy")
    pg.wait_for_timeout(400)
    print("copy says:", pg.text_content("#msg")[:24])
    # Windows hands back CRLF from the clipboard whatever was written to it,
    # so compare the text and not the line endings.
    cb = pg.evaluate("navigator.clipboard.readText()")
    print("clipboard matches panel:",
          cb.replace("\r\n", "\n").strip() == txt.strip())

    # select-all leaves the whole thing selected for a manual copy
    pg.click("#sel")
    pg.wait_for_timeout(200)
    print("selected chars:", pg.evaluate(
        "(function(o){return o.selectionEnd-o.selectionStart})"
        "(document.getElementById('out'))"), "of", len(txt))

    # the save button stays hidden where the capability is absent
    print("download hidden without capability:",
          pg.eval_on_selector("#dl", "e => e.hidden"))

    # survives a reload
    pg.reload()
    pg.wait_for_timeout(500)
    print("after reload:", pg.text_content("#cnt"),
          "| kept:", pg.input_value("#a1"),
          "| panel restored:", "測試拼法" in pg.input_value("#out"))
    pg.evaluate("document.getElementById('send').scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.screenshot(path=".scratch/b235/shot_send.png")

    # themes both ways, then a phone
    for th in ("dark", "light"):
        pg.evaluate("document.documentElement.dataset.theme='%s'" % th)
        pg.wait_for_timeout(150)
        print(th, "bg:", pg.evaluate(
            "getComputedStyle(document.body).backgroundColor"))
    pg.evaluate("document.documentElement.removeAttribute('data-theme')")
    pg.set_viewport_size({"width": 380, "height": 900})
    pg.wait_for_timeout(300)
    print("narrow no h-scroll:", pg.evaluate(
        "document.body.scrollWidth<=document.body.clientWidth"))
    pg.screenshot(path=".scratch/b235/shot_narrow.png")

    # storage refused -> the banner has to appear and the count start at 0
    ctx2 = b.new_context(viewport={"width": 900, "height": 1200})
    pg2 = ctx2.new_page()
    pg2.add_init_script(
        "Object.defineProperty(window,'localStorage',{get(){throw new "
        "Error('denied')}});")
    e2 = []
    pg2.on("pageerror", lambda e: e2.append(str(e)))
    pg2.goto("file:///" + p)
    pg2.wait_for_timeout(600)
    print("no-storage: banner=%s | still usable=%s | errors=%d"
          % (pg2.eval_on_selector_all(".warn", "e=>e.length") == 1,
             pg2.eval_on_selector_all(".answer textarea", "e=>e.length") == N,
             len(e2)))
    pg2.fill("#a1", "x")
    pg2.wait_for_timeout(200)
    print("no-storage still counts:", pg2.text_content("#cnt"))

    b.close()
print("CONTROL: js errors on the main page ->", "FAIL" if bad else "none")
