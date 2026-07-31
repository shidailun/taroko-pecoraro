"""The QTQOT family in his own text: every card, every form, every sentence.

His QDQDAN card says 參見 QTQOT and glosses 束縛/鐐銬/桎梏. His XILWI sentence says
Ngalun mo sq'tqot ka xilwi nii = I'll use this wire to handcuff him. Modern has
qdqut 鍊條;鐵鍊 and qdqji 要…鎖住. Before mapping a whole family onto qdqut, read
what he actually wrote -- which slot is the noun, which the verb, and whether
every green in the family is really the same word.
"""
import json, sys, re, io, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
s = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def tk(x):
    return (x.lower().replace("\u2019", "'").replace("\u02bc", "'")
            .replace('"', "'").replace("\u0294", "'").replace("\u0142", "l"))


PAT = re.compile(r"^s?q'?[dt]'?q[oiu]t")

print("=== cards whose headword or sub-form is in the family ===")
for e in E:
    for sb in [e] + e.get("subs", []):
        f = tk(sb.get("form") or sb.get("hw") or "")
        if not PAT.match(f):
            continue
        v = MM.get(f)
        print("\n %-12s -> %-14s  card %s" % (
            f, (v["modern"] + " [" + v["tier"] + "]") if v else "GREEN",
            e.get("hw")))
        print("    zh   : %s" % (sb.get("zh") or e.get("zh") or "")[:78])
        print("    fr   : %s" % (sb.get("fr") or e.get("fr") or "")[:78])
        for fld in ("tag", "paradigm", "crossRef"):
            if e.get(fld) or sb.get(fld):
                print("    %-5s: %s" % (fld, (sb.get(fld) or e.get(fld))[:70]))
        for x in sb.get("examples", []):
            print("    ex   : %-48s %s" % ((x.get("t") or "")[:48],
                                           (x.get("zh") or "")[:34]))

print("\n=== every occurrence of a family token anywhere in entries.js ===")
hits = collections.Counter()
where = collections.defaultdict(list)
for e in E:
    fields = [("hw", e.get("hw")), ("tag", e.get("tag")),
              ("paradigm", e.get("paradigm")), ("crossRef", e.get("crossRef"))]
    fields += [("ex", x.get("t")) for x in e.get("examples", [])]
    for sb in e.get("subs", []):
        fields += [("sub", sb.get("form")), ("sub.par", sb.get("paradigm")),
                   ("sub.cf", sb.get("crossRef"))]
        fields += [("ex", x.get("t")) for x in sb.get("examples", [])]
    for fld, txt in fields:
        for w in TOK.findall(txt or ""):
            k = tk(w)
            if PAT.match(k):
                hits[k] += 1
                where[k].append((e.get("hw"), fld))
for k, n in hits.most_common():
    v = MM.get(k)
    print(" %2dx %-12s %-16s %s" % (
        n, k, (v["modern"] + " [" + v["tier"] + "]") if v else "GREEN",
        " ".join("%s/%s" % w for w in where[k][:4])))
