"""Regenerate the greenmatch input from the CURRENT green list.

greenmatch2 reads green2.json, which is stale in two ways that both waste the
lookup: it predates ~15 batches of writes, and it predates the FORM_PROSE /
TAG_PROSE subtraction, so its top rows are his French apparatus (vl 72x, vr 62x)
which the page has been painting meta-abbr all along. Rebuild it with green6's
collection -- three curated tables plus the prose sets subtracted -- and with
green6's CORRECTED charRules mirror, so the shape axis compares against what the
reader actually sees.

Schema kept identical to green2.json ([count, key, charrule, hw, gloss]) so
greenmatch2 runs on it unchanged.
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


def wordlist(name):
    i = app.index("var %s = " % name)
    return set(re.findall(r'"([^"]+)"', app[i:app.index(";", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
FP, TP = wordlist("FORM_PROSE"), wordlist("TAG_PROSE")
META = set(re.findall(r'"([a-z]+)"\s*:', app[app.index("var META_ABBR"):
                                             app.index("var META_ABBR") + 900]))
SKIP = FP | TP | META | {"vl", "vr", "var", "r", "nb", "sy"}
MARKS = "['\u2019\u02bc\"\u0294]"
SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    w = re.sub(MARKS, "", w)
    w = re.sub(r"a[oO]$", "aw", w)          # the app.js rule added this session
    return "".join(SM.get(c, c) for c in w)


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
cnt, where = collections.Counter(), {}
for ent in E:
    hw, gl = ent.get("hw"), (ent.get("zh") or ent.get("fr") or "")
    slots = [(ent.get("hw"), gl), (ent.get("paradigm"), gl)]
    slots += [(x.get("t"), gl) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        sg = s.get("zh") or s.get("fr") or gl
        slots += [(s.get("form"), sg), (s.get("paradigm"), sg)]
        slots += [(x.get("t"), sg) for x in s.get("examples", [])]
    for f, g2 in slots:
        for w in TOK.findall(f or ""):
            k = key(w)
            if len(k) < 2 or k in OV or k in MAP or k in CL or k in SKIP:
                continue
            cnt[k] += 1
            where.setdefault(k, (hw, g2))

rows = [[c, k, cr(k), where[k][0], where[k][1]] for k, c in cnt.most_common()]
json.dump(rows, io.open("green2.json", "w", encoding="utf-8"), ensure_ascii=False)
print("green2.json rewritten: %d types, %d occurrences"
      % (len(rows), sum(r[0] for r in rows)))
