"""The green work list: source tokens, minus everything the page intercepts.

green3.py subtracts the three curated tables but not FORM_PROSE / TAG_PROSE, so it
kept ranking his French editorial words -- de, la, ce, est, qui -- as work to do
when the page has been painting them meta-abbr all along. This subtracts those
too, and prints what each token currently renders as, so the ranking is by what a
reader actually sees unverified.
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    j = app.index("\n  };", i)
    return dict(PAIR.findall(app[i:j]))


def wordlist(var):
    """the ("a b c " + "d e f").split(" ") literal that fills a prose table"""
    i = app.index("var %s = {}" % var)
    seg = app[i:app.index('.split(" ")', i)]
    return set(re.findall(r"[^\s\"+]+", seg[seg.index('("'):]))


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
    return "".join(SM.get(c, c) for c in re.sub(MARKS, "", w))


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

print("FORM_PROSE %d  TAG_PROSE %d  META_ABBR %d" % (len(FP), len(TP), len(META)))
print("STORED green after prose: %d types  %d occurrences\n"
      % (len(cnt), sum(cnt.values())))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
for k, c in cnt.most_common(N):
    hw, gl = where[k]
    print("%2dx %-14s prints %-14s [%s] %s" % (c, k, cr(k).upper(), hw, (gl or "")[:38]))
json.dump(cnt, io.open("green_work.json", "w", encoding="utf-8"), ensure_ascii=False)
