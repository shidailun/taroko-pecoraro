# -*- coding: utf-8 -*-
"""The sheet at a real desktop width, top and a question card and the return
panel. The narrow pass already exists; this is the other end."""
import os, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
p = os.path.abspath(".scratch/b235/translator.html").replace("\\", "/")
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900},
                        device_scale_factor=1)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///" + p)
    pg.wait_for_timeout(700)
    print("js errors:", errs[:2] or "none")
    print("body width:", pg.evaluate("document.body.clientWidth"),
          "| sheet width:", pg.eval_on_selector(
              ".sheet", "e => Math.round(e.getBoundingClientRect().width)"))
    print("h-scroll:", pg.evaluate(
        "document.body.scrollWidth > document.body.clientWidth"))
    pg.screenshot(path=".scratch/b235/desk_top.png")
    pg.evaluate("document.querySelectorAll('.q-item')[0]"
                ".scrollIntoView({block:'start'})")
    pg.wait_for_timeout(250)
    pg.screenshot(path=".scratch/b235/desk_q1.png")
    b.close()
