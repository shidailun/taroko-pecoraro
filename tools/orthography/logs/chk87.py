"""dom66 reports FAILURES 2, both on the AYO card. Confirm they are the cascade
they look like, not damage.

Correcting ayo>ayug re-derived his m'ayo and mpa'ayo through generative tiers:
mayu>mayug and empaayu>empaayug. dom66 asserts neighbours are UNCHANGED, so a
legitimate re-derivation trips it -- exactly what psdxalan>psdharan did in batch
65. Check the slots really are the stream sense, and that the live DOM prints the
new forms.
"""
import io, sys, json, re, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
for k in ("ayo", "m'ayo", "mpa'ayo", "ayos", "ayus", "ayong"):
    print("   %-11s -> %s" % (k, MAP.get(k, "(green)")))

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("m'ayo", "mpa'ayo"):
    print("\n### every slot spelling %r (now %s)" % (target, MAP.get(target)))
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            if any(key(w) == target for w in TOK.findall(f or "")):
                print("   [%-12s] %-4s %-30s %s" % (hw[:12], kind, (f or "")[:30],
                                                    (g or "")[:50]))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto("http://127.0.0.1:8765/")
    pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.goto("http://127.0.0.1:8765/?q=AYO", wait_until="networkidle")
    txt = pg.inner_text("body")
    b.close()
print("\n=== live AYO card, modern mode ===")
i = txt.find("AYO")
print(txt[i:i + 700] if i >= 0 else txt[:600])
for w in ("ayug", "mayug", "empaayug", r"\bayu\b", r"\bmayu\b", "empaayu\\b"):
    print("   %-12s present in DOM: %s" % (w, bool(re.search(w, txt, re.I))))
