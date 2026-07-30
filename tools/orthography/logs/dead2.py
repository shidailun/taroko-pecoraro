"""The eight dead keys with NO twin: what did the adjudicator mean, and is the
word they were aiming at still green? Match on norm() (marks and diacritics gone)
first, then on a looser near-shape, and report the colour of every candidate.
"""
import json, io, sys, re, subprocess, collections
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography")
import build_modern_map as B

S = "C:/dev/formosan/seediq/taroko-pecoraro/site/"
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"


def parse_map(text):
    a = text.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    return json.loads(text[a:text.index("\n};", a) + 2])


MAP = parse_map(io.open(S + "modern_map.js", encoding="utf-8").read())
OLD = parse_map(subprocess.run(["git", "show", "HEAD:site/modern_map.js"],
                               cwd="C:/dev/formosan/seediq/taroko-pecoraro",
                               capture_output=True).stdout.decode("utf-8"))
app = io.open(S + "app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
tokens = B.load_corpus()[0]
manual = json.load(io.open(H + "manual_map.json", encoding="utf-8"))
llm = json.load(io.open(H + "llm_map.json", encoding="utf-8"))

print("mpkuda' at HEAD: %r   now: %r" % (OLD.get("mpkuda'"), MAP.get("mpkuda'")))
print()

DEAD = ["byequn", "mnudus", "nani", "pstana", "ska'nan", "smtana", "stana",
        "tibilaq", "qeuni", "sanao"]


def colour(t):
    return ("MAP" if t in MAP else "OVERRIDE" if t in OV
            else "CLITIC" if t in CL else "GREEN")


for k in DEAD:
    val = manual.get(k) or llm.get(k)
    nk = B.norm(k)
    near = sorted(t for t in tokens
                  if abs(len(B.norm(t)) - len(nk)) <= 2
                  and (B.norm(t) in nk or nk in B.norm(t)
                       or B.norm(t)[1:] == nk[1:] and len(nk) > 4))
    print("%-9s -> %-9s" % (k, val))
    for t in near[:8]:
        print("      %-12s %2dx  %-8s %s"
              % (t, tokens[t], colour(t), MAP.get(t) or OV.get(t) or ""))
    if not near:
        print("      (nothing near)")
