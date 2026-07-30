"""Every green token, with the BROWN siblings on its own card.

Finding (4): half a paradigm mapped is a green flag -- if the headword and three
sub-forms are brown and one -an/-un nominal is green, the modern shape is affix
arithmetic on a sibling, not a fresh lookup. This lists the arithmetic for all of
them at once so a batch can be adjudicated in bulk instead of card by card.
"""
import json, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

t = open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

app = open(H + "site/app.js", encoding="utf-8").read()
KEY = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:')


def tbl(name):
    i = app.index("var %s = {" % name)
    j = app.index("\n  };", i)
    return set(KEY.findall(app[i:j]))


KNOWN = set(MAP) | tbl("WORD_OVERRIDES") | tbl("CLITIC_FORMS")
GREEN = json.load(open("green_true.json", encoding="utf-8"))

s = open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
SPLIT = re.compile(r"[\s,\.;:!\?\(\)\[\]\u2014\u2013\-/=]+")


def tk(x):
    return (x or "").lower().replace("\u2019", "'").replace("\u02bc", "'") \
                            .replace('"', "'").replace("\u0294", "'").replace("\u0142", "l")


def first(x):
    for w in SPLIT.split(x or ""):
        if w:
            return tk(w)
    return ""


MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 2
out = []
for e in E:
    hw = e.get("hw") or ""
    forms = [(e.get("form") or hw, e.get("zh") or "")] + \
            [(sb.get("form") or "", sb.get("zh") or "") for sb in e.get("subs", [])]
    rows = [(first(f), f, z) for f, z in forms if f]
    green = [(k, f, z) for k, f, z in rows if k in GREEN and GREEN.get(k, 0) >= MIN]
    brown = [(k, MAP.get(k, "?")) for k, f, z in rows if k in KNOWN]
    if green and brown:
        out.append((len(brown), hw, green, brown))

out.sort(reverse=True)
for n, hw, green, brown in out:
    print("\n%-14s brown: %s" % (hw[:14], "  ".join("%s>%s" % (k, v) for k, v in brown[:7])))
    for k, f, z in green:
        print("      GREEN %-16s x%-3d %s" % (f[:16], GREEN.get(k, 0), z[:50]))
print("\n%d cards with a green form and at least one brown sibling" % len(out))
