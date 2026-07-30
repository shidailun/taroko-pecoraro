"""green_gloss with a rare-CHARACTER index, because the bigram index has a blind
spot that has now cost two clearances.

green_gloss matched his gloss to modern glosses on shared two-character Chinese
words. That is the right filter for precision, and it silently fails whenever the
two dictionaries choose different characters for the same thing:

    his 帳篷   vs   the omnibus 帳棚      -> koobu cleared as ABSENT in batch 67,
                                             wrongly; kowbu 帳棚 spk 6 is right there
    my  鍋     vs   the corpus 鍋 (U+934B) -> a hand-typed simplified codepoint,
                                             81 words invisible

One shared character is much weaker evidence than a shared word -- but only when
the character is common. 人, 的, 很 carry no content; 篷, 屎, 菇, 獠 carry a great
deal. So index by single character and keep only characters carried by at most
RARE modern words, which is the same distinctiveness test green_gloss applied to
bigrams, one level down. Then a variant pair like 帳棚/帳篷 still meets at 帳.

Usage: python green_uni.py [MINSLOT] [LO] [HI] [RARE]
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
HAN = re.compile(r"[\u4e00-\u9fff]")
MARKS = "['\u2019\u02bc\"\u0294]"
SMALL = {"x": "h", "o": "u", "l": "r"}


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


def cr(w):
    w = re.sub(MARKS, "", w).replace("\u0142", "l")
    w = re.sub(r"a[oO]$", "aw", w)
    return "".join(SMALL.get(c, c) for c in w)


def dist(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, g))

# index modern words by single character, spoken words only -- an unattested
# modern headword is no better evidence than his transcription
BYCH = collections.defaultdict(set)
for w, gs in OMNI.items():
    if SPK.get(w, 0) < 1:
        continue
    for g in gs:
        for ch in set(HAN.findall(g)):
            BYCH[ch].add(w)

MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 60
RARE = int(sys.argv[4]) if len(sys.argv) > 4 else 12

greens = sorted({t for t in his if t not in MAP and len(his[t]) >= MIN and len(t) > 2},
                key=lambda t: (-len(his[t]), t))
print("greens at >=%d slots: %d   rare-char cutoff: carried by <=%d spoken words"
      % (MIN, len(greens), RARE))

out = []
for t in greens:
    # his gloss for the HEADWORD slot if there is one, else the first slot
    gl = ""
    for hw, kind, g in his[t]:
        if kind in ("hw", "sub") and g:
            gl = g
            break
    if not gl:
        continue
    cand = collections.defaultdict(set)
    for ch in set(HAN.findall(gl)):
        ws = BYCH.get(ch) or ()
        if not ws or len(ws) > RARE:
            continue
        for w in ws:
            cand[w].add(ch)
    if not cand:
        continue
    p = cr(t)
    ranked = sorted(cand.items(), key=lambda kv: (dist(p, kv[0]) - 2 * len(kv[1]), -SPK.get(kv[0], 0)))
    out.append((len(his[t]), t, p, gl, ranked[:5]))

print("greens with a rare-character match: %d\n" % len(out))
for n, t, p, gl, ranked in sorted(out, reverse=True)[LO:HI]:
    print("%2dx %-13s prints %-13s %s" % (n, t, p.upper(), gl[:54]))
    for w, chs in ranked:
        print("        d=%d %-13s spk %-5d [%s] %s"
              % (dist(p, w), w, SPK.get(w, 0), "".join(sorted(chs)),
                 " | ".join(dict.fromkeys(OMNI[w]))[:44]))
