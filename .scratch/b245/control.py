# -*- coding: utf-8 -*-
"""Drive the built sheet and check the four things that could silently break.

Every leg has to be able to REFUSE (batch 234): each one is run against a page
state where it must pass AND, where the assertion is about a field, against the
same string written to the wrong field, which must not pass.
"""
import io
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
PAGE = pathlib.Path(H, ".scratch", "b245", "translator.html").as_uri()
PREV = json.loads(io.open(os.path.join(H, ".scratch/b245/prev.json"),
                          encoding="utf-8").read())
K = "pecoraro_translator_v1"
bad = 0


def fail(msg):
    global bad
    bad += 1
    print("FAIL %s" % msg)


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()

    # ---- 1. the page is the two-question page ------------------------------
    pg.goto(PAGE)
    d = pg.evaluate("""() => ({
      items: document.querySelectorAll('.q-item').length,
      q1: document.querySelectorAll('.answer textarea[data-q="1"]').length,
      q2: document.querySelectorAll('.answer textarea[data-q="2"]').length,
      prev: document.querySelectorAll('p.prev').length,
      cnt: document.getElementById('cnt').textContent,
      qset: document.querySelector('.sheet').dataset.qset})""")
    if not (d["items"] == d["q1"] == d["q2"] == 46):
        fail("boxes: %s" % d)
    if d["prev"] != 46:
        fail("previous-answer panels %d, want 46" % d["prev"])
    if "問一" not in d["cnt"] or "問二" not in d["cnt"]:
        fail("the counter does not name the two questions: %r" % d["cnt"])
    if d["qset"] == "91aca4f":
        fail("the question-set digest is b243's: a returned sheet could not "
             "be told from the previous one")

    # ---- 2. the two boxes store separately ---------------------------------
    pg.evaluate("""() => {
      const a = document.querySelector('.answer textarea[data-q="1"]');
      const it = a.closest('.q-item');
      const bb = it.querySelector('.answer textarea[data-q="2"]');
      const set = (t, v) => { t.value = v;
        t.dispatchEvent(new Event('input', {bubbles: true})); };
      set(a, 'SPELL-ONE'); set(bb, 'SAY-TWO');
      window.__his = a.dataset.his; }""")
    st = pg.evaluate("() => [JSON.parse(localStorage.getItem('%s')||'{}'),"
                     " window.__his]" % K)
    store, his = st
    if store.get(his + "|1") != "SPELL-ONE" or store.get(his + "|2") != "SAY-TWO":
        fail("the two answers did not store under separate keys: %s"
             % {k: v for k, v in store.items() if k.startswith(his)})
    if store.get(his) is not None:
        fail("a bare key is still being written: the columns would re-merge")

    # ---- 3. the output text keeps them apart -------------------------------
    out = pg.evaluate("() => document.getElementById('out').value")
    if "問一" not in out or "問二" not in out:
        fail("the returned text does not label the two questions:\n%s"
             % out[:200])
    if "SPELL-ONE" not in out or "SAY-TWO" not in out:
        fail("an answer is missing from the returned text")
    # the wrong-field control: the label must belong to the answer under it
    lines = [ln.strip() for ln in out.splitlines()]
    if not any(ln.startswith("問一") and "SPELL-ONE" in ln for ln in lines):
        fail("問一's answer is not on 問一's line")
    if not any(ln.startswith("問二") and "SAY-TWO" in ln for ln in lines):
        fail("問二's answer is not on 問二's line")

    # ---- 4. the b243 answers migrate into the column they answered ---------
    # Seeded with one of each kind, under the OLD bare key, exactly as a
    # browser that answered the previous sheet holds them.
    seed = {}
    want = {}
    for kind in ("meaning", "respell", "gone"):
        k = next((h for h, v in sorted(PREV.items()) if v["kind"] == kind),
                 None)
        if not k:
            continue
        seed[k] = "OLD-" + kind
        want[k] = kind
    pg.evaluate("s => localStorage.setItem('%s', JSON.stringify(s))" % K, seed)
    pg.goto(PAGE)
    after = pg.evaluate("() => JSON.parse(localStorage.getItem('%s')||'{}')" % K)
    for k, kind in want.items():
        if kind == "meaning":
            if after.get(k + "|2") != "OLD-meaning":
                fail("a 問二 answer did not migrate: %r -> %s"
                     % (k, {a: b for a, b in after.items() if a.startswith(k)}))
            if after.get(k + "|1"):
                fail("a 問二 answer landed in 問一 (%r)" % k)
        else:
            if any(a.startswith(k) for a in after):
                fail("a %s answer was restored into a box (%r): question one "
                     "would read as accepted" % (kind, k))
    # idempotence: a second load must not migrate the migrated keys again
    pg.goto(PAGE)
    again = pg.evaluate("() => JSON.parse(localStorage.getItem('%s')||'{}')" % K)
    if again != after:
        fail("the migration is not idempotent: %s -> %s" % (after, again))

    # ---- controls: each leg must be able to refuse -------------------------
    ctl = 0
    pg.evaluate("() => localStorage.clear()")
    pg.goto(PAGE)
    # (a) an answer typed into 問二 must NOT satisfy the 問一 assertion
    pg.evaluate("""() => {
      const it = document.querySelector('.q-item');
      const bb = it.querySelector('.answer textarea[data-q="2"]');
      bb.value = 'ONLY-TWO';
      bb.dispatchEvent(new Event('input', {bubbles: true}));
      window.__his = bb.dataset.his; }""")
    s2 = pg.evaluate("() => JSON.parse(localStorage.getItem('%s')||'{}')" % K)
    h2 = pg.evaluate("() => window.__his")
    if s2.get(h2 + "|1"):
        ctl += 1
        print("CONTROL a: writing 問二 also filled 問一")
    # (b) the row must read as part-done, not done
    cls = pg.evaluate("() => document.querySelector('.q-item').className")
    if "done" in cls.replace("part", ""):
        ctl += 1
        print("CONTROL b: a 問二-only row is marked done — the sheet would "
              "report answers it does not have")
    # (c) a seeded key that is in NO migration table must vanish, not persist
    pg.evaluate("() => localStorage.setItem('%s', "
                "JSON.stringify({zzzznotaword: 'x'}))" % K)
    pg.goto(PAGE)
    if pg.evaluate("() => JSON.parse(localStorage.getItem('%s')||'{}')"
                   ".zzzznotaword" % K):
        ctl += 1
        print("CONTROL c: an unknown bare key survived the migration")
    print("CONTROLS %s" % ("all behaved" if ctl == 0 else "%d MISBEHAVED"
                           % ctl))
    bad += ctl
    b.close()

print("%d assertions failed" % bad)
