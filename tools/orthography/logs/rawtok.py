"""What raw token(s) produce a given key, and in which field."""
import json, io, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
# Must be the BUILDER's token class, character for character. Mine omitted U+0294
# (his glottal stop), so `Mpkuda\u0294` came back as a bare `Mpkuda` -- a key the census
# does not hold -- and the batch chased a token that does not exist.
TOK = re.compile("[A-Za-z\u00c0-\u00ff\u0142\u0141\u0294'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
want = {k.lower() for k in sys.argv[1:]}
seen = collections.Counter()
where = collections.defaultdict(set)
for ent in E:
    fs = [("hw", ent.get("hw")), ("para", ent.get("paradigm"))]
    fs += [("ex", x.get("t")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        fs += [("form", s.get("form")), ("para", s.get("paradigm"))]
        fs += [("ex", x.get("t")) for x in s.get("examples", [])]
    for tag, f in fs:
        if not f:
            continue
        for w in TOK.findall(f):
            if key(w) in want:
                seen[(key(w), w, tag)] += 1
                where[key(w)].add(ent.get("hw") or "")
for (k, w, tag), n in sorted(seen.items()):
    print("%-12s raw=%-14r %-5s x%d   %s" % (k, w, tag, n, sorted(where[k])[:3]))
for k in sorted(want - set(where)):
    print("%-12s NOT FOUND" % k)
