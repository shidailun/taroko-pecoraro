"""Does the modern dictionary contain a BETTER word than the one we took?

audit2 reads the never-gloss-checked tiers in frequency order. audit4 checks each
card for internal coherence. Neither asks the question that actually decides these
~2400 blind browns, which is the one the whole review keeps coming back to: look
it up in the modern dictionary.

So ask it mechanically. For each key on a tier that never consulted a gloss:

  1. HIS meaning = the Chinese glosses of every slot where the token occurs.
  2. The SHIPPED value's meaning = its glosses in the omnibus.
  3. If those two share a two-character Chinese word, the value already matches
     his sense and the key is dropped. Bigrams, not single characters: 祖母, 剩餘,
     取暖, 蝸牛 are words; 的, 人, 子 are noise that would match anything.
  4. Otherwise hunt the omnibus for a word that (a) IS within edit distance 2 of
     what charRules would print for his token -- i.e. a plausible respelling of
     what he actually wrote, not a free-associated synonym -- and (b) DOES share
     a bigram with his gloss, and (c) is better attested than the shipped value.

That is exactly the pax shape stated as a query: his pax, charRules pah, omnibus
paah at spk 591 glossed 從, his gloss 從——自——由…起. It is also the shape of pai>
payi (祖母) and loan>ruwan (內部). Each of those took an evening of reading to
find; this finds the class.

The known false-positive classes still apply and are the reason every hit is read
before anything is written: synonym wording (his 壞的 against the omnibus 不好
shares no bigram), his personal-name entries, and his two-card homographs where
one card's sense is served and the other is not.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
TIER = {k: v["tier"] for k, v in MM.items()}
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

MARKS = "['\u2019\u02bc\"\u0294]"
SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    w = re.sub(MARKS, "", w).replace("\u0142", "l")
    w = re.sub(r"a[oO]$", "aw", w)
    return "".join(SM.get(c, c) for c in w)


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
CJK = re.compile(r"[\u4e00-\u9fff]+")
# characters too common to carry meaning on their own or in a bigram
STOP = set("\u7684\u4e86\u662f\u5728\u6709\u4eba\u4e0d\u4e00\u500b\u6211\u4f60"
           "\u4ed6\u5011\u9019\u90a3\u4e4b\u548c\u8207\u6216\u4e5f\u5c31\u628a"
           "\u5230\u53bb\u4f86\u505a\u7269\u4e8b\u6642\u5730\u65b9\u5f0f\u8005"
           "\u4f7f\u88ab\u6240\u53ca\u7b49\u5176\u800c\u4ee5\u70ba\u4e2d\u4e0a"
           "\u4e0b\u5927\u5c0f\u5df2\u8981\u6703\u80fd\u53ef\u5f97\u5f88\u592a")


def bigrams(text):
    out = set()
    for run in CJK.findall(text or ""):
        for i in range(len(run) - 1):
            b = run[i:i + 2]
            if b[0] not in STOP or b[1] not in STOP:
                out.add(b)
    return out


def lev(a, b, cap=2):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def clean(g):
    g = re.sub(r"\uff08\u8a3b[^\uff09]*\uff09?", "", g or "")
    return re.sub(r"\s+", " ", re.sub(r"\u53c3\u898b.*$", "", g)).strip()


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


# ---- his meaning, per key ------------------------------------------------
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)   # key -> [(gloss, headword, kind)]
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((clean(g), hw, kind))

# ---- candidate index, bucketed by length --------------------------------
BYLEN = collections.defaultdict(list)
for w in OMNI:
    BYLEN[len(w)].append(w)

# tiers that never consulted a gloss (A required one; M/J/N/C-review are human)
BLIND_TIERS = {"id", "B", "B-rules", "P", "R", "D", "E", "G", "V", "W", "T",
               "L", "KL", "S", "X"}
MINSLOT = int(sys.argv[1]) if len(sys.argv) > 1 else 3
hits = []
for k, slots in his.items():
    if k not in MAP or TIER.get(k) not in BLIND_TIERS:
        continue
    if k in LEX:
        continue
    if len(slots) < MINSLOT:
        continue
    # HIS meaning comes from headword/sub/paradigm slots ONLY. In an example
    # slot the gloss is the whole sentence's translation, so every function
    # word in it would inherit the sentence's bigrams and match anything.
    hisb = set()
    for g, _, kind in slots:
        if kind != "ex":
            hisb |= bigrams(g)
    if not hisb:
        continue
    v = MAP[k].lower()
    valb = set()
    for g in OMNI.get(v, []):
        valb |= bigrams(g)
    if hisb & valb:            # the shipped value already carries his sense
        continue
    target = cr(k)
    # scale the edit cap to length: at 2 edits a two-letter particle is within
    # reach of half the dictionary, and the match means nothing.
    cap = max(1, min(2, len(target) // 3))
    best = []
    for L in range(len(target) - 2, len(target) + 3):
        for w in BYLEN.get(L, ()):
            if w == v:
                continue
            wb = set()
            for g in OMNI[w]:
                wb |= bigrams(g)
            shared = hisb & wb
            if not shared:
                continue
            if lev(target, w, cap) > cap:
                continue
            if SPK.get(w, 0) <= SPK.get(v, 0):
                continue
            best.append((SPK.get(w, 0), w, shared))
    if not best:
        continue
    best.sort(reverse=True)
    hits.append((len(slots), k, v, TIER[k], SPK.get(v, 0), target, best[:3],
                 slots[0][1],
                 "; ".join(dict.fromkeys(g for g, _, kd in slots if kd != "ex"))[:70],
                 " | ".join(dict.fromkeys(OMNI.get(v) or []))[:36] or "-- BLIND --"))

hits.sort(key=lambda r: -r[0])
print("%d keys where the omnibus holds a nearer word that matches his gloss "
      "and the shipped one does not (>=%d slots)\n" % (len(hits), MINSLOT))
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 30
for n, k, v, ti, spk, target, best, hw, hg, vg in hits[LO:HI]:
    print("%3dx [%-14s] %-13s -> %-13s %-2s spk%-5d  (charRules %s)"
          % (n, hw[:14], k, v, ti, spk, target))
    print("      his %s" % hg)
    print("      val %s" % vg)
    for s, w, sh in best:
        print("      CAND %-13s spk %-5d %-30s  shares %s"
              % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:30], "".join(sorted(sh))[:20]))
