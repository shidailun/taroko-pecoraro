"""The wrong-brown audit, over the whole map instead of nine cards.

Batch 62 came from one new column: not "is this key mapped" but "is the value it
was given a real modern word, and does that word mean what his card means".
Three cards failed it the moment I looked -- S'LUT pointed at "getting fat" and
"blunt blade", TABE at "come down". Those had been brown, claiming to be
verified, for the whole review. Nine cards is a keyhole; this is the same test on
all 7128 keys.

The flag is deliberately narrow, because a homograph is not a defect:
 - the VALUE must be attested in the omnibus with a substantive gloss. An
   unattested value asserts nothing about meaning and is a different problem (the
   ~526 blind identities), already tracked.
 - the map must have CHOSEN the value -- value != charRules(key). If the value is
   just his own shape run through the letter rules, the entry is a respelling and
   the fact that some unrelated modern word shares the shape is an accident, not
   a claim. That is exactly why tbiyan 下來 on the TABE card is recorded and not
   "fixed": his plough word did not survive, and its regular respelling collides.
 - the two glosses must share NO content character. Grammatical filler (的之了是
   在有不人物等) is stripped first, or every gloss would overlap with every other.

Ranked by his occurrence count, because the standing instruction is frequency
order and because a wrong brown on a 20x word misleads twenty times.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
# ALL glosses per word, not the first. setdefault cost the first two runs their
# credibility: babuy came back as 睡懶覺 and elug as 行事, because the omnibus has
# several rows per word and the pig and the road were in the rows being dropped.
# A modern word only has to mean what he means in ONE of its senses.
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

# charRules, mirrored from site/app.js -- see green6.py for why this must be kept
# in step: an out-of-date mirror ranks work by a rendering the reader never sees
MARKS = "['\u2019\u02bc\"\u0294]"
SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    w = re.sub(MARKS, "", w).replace("\u0142", "l")
    w = re.sub(r"a[oO]$", "aw", w)
    return "".join(SM.get(c, c) for c in w)


CJK = re.compile(r"[\u4e00-\u9fff]")
# Only genuine function characters. The first cut stopped 一, 人, 是, 也 and the
# numerals as "filler", which is exactly backwards for a dictionary: it made
# kingal 一—單位 against 一個；一頂 and sadyaq 人／人們 against 人品 look like they
# shared nothing, when the shared character WAS the definition. Stop what carries
# no meaning on its own, and nothing else.
STOP = set("的之了在有不會個們這那和與或為使被所以又就都再更太最能可要用者樣子件把讓"
           "很地得而且如於及等某每各種類方面時候情形")


def content(g):
    return {c for c in CJK.findall(g or "")} - STOP


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
cnt = collections.Counter()
gloss, card = {}, {}
for ent in E:
    hw, top = ent.get("hw") or "", ent.get("zh") or ""
    # DEFINITIONAL slots only, and only their FIRST token. The first cut of this
    # audit took the richest gloss a key was seen with anywhere, which handed
    # every key that appears in a long example the TRANSLATION OF THAT SENTENCE
    # as its meaning -- so daxa>dha 二（數目）, which is simply right, was flagged
    # against a paragraph about SISIL birds and omens. A sentence is not a
    # definition, and a word inside a sentence is not being defined by it.
    defs = [(ent.get("hw"), top), (ent.get("paradigm"), top)]
    for s in ent.get("subs", []):
        sg = s.get("zh") or top
        defs += [(s.get("form"), sg), (s.get("paradigm"), sg)]
    for f, g in defs:
        w = TOK.findall(f or "")
        if not w:
            continue
        k = key(w[0])
        if len(content(g)) > len(content(gloss.get(k, ""))):
            gloss[k], card[k] = g, hw
    # counts still come from everywhere, including examples -- frequency is how
    # often the reader meets the token, not how often he defines it
    every = defs + [(x.get("t"), "") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        every += [(x.get("t"), "") for x in s.get("examples", [])]
    for f, _g in every:
        for w in TOK.findall(f or ""):
            cnt[key(w)] += 1

flagged = []
for k, v in MAP.items():
    if k not in cnt:
        continue
    senses = OMNI.get(v) or []
    if not senses or v == cr(k):
        continue
    a_ = content(gloss.get(k, ""))
    b_ = set().union(*[content(g) for g in senses]) if senses else set()
    if len(a_) < 1 or len(b_) < 1 or (a_ & b_):
        continue
    flagged.append((cnt[k], k, v, " | ".join(dict.fromkeys(senses)),
                    gloss.get(k, ""), card.get(k, "")))

flagged.sort(reverse=True)
print("%d mapped keys assert an attested modern word whose gloss shares no "
      "content character with his\n" % len(flagged))
for c, k, v, mg, hg, hw in flagged[:70]:
    print("x%-3d %-14s -> %-14s spk %-4s [%-12s]" % (c, k, v, SPK.get(v, 0), hw[:12]))
    print("       his    %s" % hg[:64])
    print("       modern %s" % mg[:64])
json.dump([[c, k, v, mg, hg, hw] for c, k, v, mg, hg, hw in flagged],
          io.open("wrongbrown.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\n(full list in wrongbrown.json)")
