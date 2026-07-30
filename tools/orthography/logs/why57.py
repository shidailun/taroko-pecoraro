"""Why do `sao` on LOQ and `page` on PARO fail the neighbour hold?

Print every field of the two cards that holds the token, so the answer comes from
his text rather than from a guess about the renderer.
"""
import json, io, sys, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
TOK = re.compile("[A-Za-zÀ-ÿłŁʔ'’ʼ\"]+")

app = io.open(H + "site/app.js", encoding="utf-8").read()
PROSE = set()
for name in ("FORM_PROSE", "TAG_PROSE"):
    i = app.index("var %s = {}" % name)
    j = app.index('.split(" ")', i)
    for s in re.findall(r'"([^"]*)"', app[i:j]):
        PROSE |= set(s.split())

e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for ent in E:
    hw = ent.get("hw") or ""
    if hw.split()[0] not in ("LOQ", "PARO"):
        continue
    want = "sao" if hw.split()[0] == "LOQ" else "page"
    print("=== %s   (%r in FORM_PROSE/TAG_PROSE: %s)" % (hw, want, want in PROSE))
    fs = [("hw", hw), ("para", ent.get("paradigm")), ("tag", ent.get("tag"))]
    fs += [("ex", x.get("t")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fs += [("form", s.get("form")), ("para", s.get("paradigm"))]
        fs += [("ex", x.get("t")) for x in s.get("examples", [])]
    for tag, f in fs:
        if f and any(t.lower() == want for t in TOK.findall(f)):
            print("   %-5s %s" % (tag, f))
