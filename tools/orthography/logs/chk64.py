"""Four leads from chk63, each of which looks like a WRONG BROWN, not a green.

chk63 printed a column I had not been printing: whether the shipped value is
itself attested, and with what gloss. Three cards came back with brown values
whose modern gloss contradicts his:

  TABE  犁 (plough)      -> tbiyan, and modern tbiyan means 下來 "come down".
                            A pure shape match with an unrelated meaning. And his
                            own headword says 犁（同義詞＝SAKOL）-- he NAMES the
                            other word, and modern has exactly one: sakur 犁.
  S'LUT 黏附 (adhere)    -> slut 剛開始肥 "starting to get fat", ms'lut>msrut
                            刀鋒鈍了 "blade gone blunt", ps'lut>psrut 很不鋒利.
                            Three values, two unrelated meanings, zero adhesion.
  KSIA  變成水 (liquefy) -> mksia>mqsiya is BLIND, while msqsiya 溶化成水（液體）
                            is attested spk 4 and matches his gloss exactly.
                            Well formed is not attested.

So this asks the questions that decide them:
 1. does he have a SAKOL card of his own, and what did the map give it? (if
    tabe>sakur merges two of his headwords onto one modern word, I want to see
    that happening before I do it, not after)
 2. what IS modern for 黏 / 黏著 / 貼?
 3. the whole qsiya family, and the whole sakur family, by gloss not by shape
 4. is bare ttuan attested, and what does lexical_map say about ttuun?
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

print("== 1. his SAKOL card, and every key of his shaped sakol/sakor ==")
for ent in E:
    hw = (ent.get("hw") or "").upper()
    if hw.startswith("SAKOL") or hw.startswith("SAKUL") or hw.startswith("SAKOR"):
        print("   hw %-16s %s" % (ent.get("hw"), (ent.get("zh") or "-")[:56]))
        for s in ent.get("subs", []):
            print("     - %-16s %s" % (s.get("form", ""), (s.get("zh") or "")[:46]))
for k in sorted(MAP):
    if re.search(r"sak[ou][lr]", k):
        print("   MAP %-14s -> %-14s omni %-20s spk %s"
              % (k, MAP[k], (OMNI.get(MAP[k]) or "-")[:20], SPK.get(MAP[k], 0)))

print("\n== 2. modern by gloss: 犁 / 黏 / 貼 / 液化 ==")
for label, terms in [("\u7281 plough", ("\u7281",)),
                     ("\u9ecf/\u8cbc adhere", ("\u9ecf", "\u8cbc", "\u9ecf\u8457",
                                               "\u7dca\u9760", "\u63a5\u5408")),
                     ("\u6db2\u5316 liquefy", ("\u6eb6\u5316", "\u5316\u6210\u6c34",
                                               "\u6c34\u6c6a", "\u591a\u6c41"))]:
    print("   -- %s --" % label)
    seen = set()
    for w, g, _ in ROWS:
        if w and g and any(z in g for z in terms) and w.lower() not in seen:
            seen.add(w.lower())
            print("      %-18s %-34s spk %s" % (w, g[:34], SPK.get(w.lower(), 0)))
            if len(seen) >= 18:
                print("      ...")
                break
    if not seen:
        print("      (nothing)")

print("\n== 3. every modern word shaped sakur / qsiya ==")
for pat in (r"sakur", r"qsiya"):
    print("   -- /%s/ --" % pat)
    r = re.compile(pat)
    for w in ALL:
        if r.search(w):
            print("      %-18s %-32s spk %s" % (w, (OMNI.get(w) or "-")[:32], SPK.get(w, 0)))

print("\n== 4. the ttu- cut stem: bare forms, and the lexical_map veto ==")
for w in ALL:
    if re.match(r"^k?s?n?ttu(an|un|i|)$", w):
        print("   %-16s %-32s spk %s" % (w, (OMNI.get(w) or "-")[:32], SPK.get(w, 0)))
for k in ("ttuun", "_ttuun", "t'to", "ta'to", "t\"tuan", "stbako", "_stbako"):
    if k in LEX:
        print("   LEX %-12s = %s" % (k, json.dumps(LEX[k], ensure_ascii=False)[:200]))
for k in LEX:
    if "ttu" in k.lower() or "tbako" in k.lower():
        print("   LEX* %-12s = %s" % (k, json.dumps(LEX[k], ensure_ascii=False)[:300]))
