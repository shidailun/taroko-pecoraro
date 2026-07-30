"""French apparatus leaking into the respeller.

green_near turned up two green tokens that are not Truku words at all: rouge on
the AN card, which the reader prints as RUUGE, and var on BIYOQ. FORM_PROSE,
TAG_PROSE and metaAbbr grey his French apparatus BEFORE respellable() runs, so
anything they miss gets charRules applied to it and appears as a green Truku
word. RUUGE is French rouge with the o>u rule applied to it.

Print the slots, then sweep the whole green list for more of the same: tokens
that are French or Latin rather than Truku. The tell is a letter or sequence
Truku does not use -- c before a front vowel, f, v, z, ou, oi, gn -- or simple
membership in a small list of words his apparatus actually uses.
"""
import io, sys, json, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), ent.get("fr"), "hw"),
             (ent.get("paradigm"), ent.get("zh"), ent.get("fr"), "par")]
    slots += [(x.get("t"), x.get("zh"), x.get("fr"), "ex")
              for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), s.get("fr"), "sub")]
        slots += [(x.get("t"), x.get("zh"), x.get("fr"), "ex")
                  for x in s.get("examples", [])]
    for f, g, fr, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, f, g, fr))

for target in ("rouge", "var"):
    print("### every slot spelling %r" % target)
    for hw, kind, f, g, fr in his.get(target, []):
        print("   [%-12s] %-4s form=%r" % (hw[:12], kind, (f or "")[:52]))
        print("        zh %s" % (g or "")[:74])
        print("        fr %s" % (fr or "")[:74])

# a Truku word cannot contain these
FOREIGN = re.compile(r"[fvz]|ou|oi|gn|ce$|que$|eu")
KNOWN = {"rouge", "var", "cf", "sic", "id", "idem", "ibid", "etc", "vel",
         "blanc", "noir", "jaune", "vert", "bleu", "gris", "brun"}
print("\n### green tokens that look French or Latin rather than Truku")
n = 0
for k, rows in sorted(his.items(), key=lambda kv: -len(kv[1])):
    if k in MAP or k in LEX:
        continue
    if k in KNOWN or (len(k) > 2 and FOREIGN.search(k)):
        n += 1
        hw, kind, f, g, fr = rows[0]
        print("%3dx %-14s [%-12s] %-4s %s" % (len(rows), k, hw[:12], kind,
                                              (fr or g or "")[:56]))
print("   (%d such tokens)" % n)
