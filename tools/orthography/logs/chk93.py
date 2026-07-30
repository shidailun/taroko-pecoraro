"""Follow-ups from chk92, plus two of my own regexes that were wrong.

I searched for 鍋 and 舔 with SIMPLIFIED codepoints (U+9505, U+8202) against a
traditional-character dictionary, so those two rows returned zero for the wrong
reason. Redone here with the traditional forms.

  x'li/xm'li  -- confirm the hrig family really is 倒入 and not only 倒出來
  pusyaq      -- mnspusiq and mnegpusiq are both glossed 眼屎; is bare pusiq there?
  nilao       -- ngiraw 香菇 is one letter from NIRAW and matches his description
                 (cultivated, growing on tree trunks). But he writes ng elsewhere
                 (longao, sdongan, kmpoling), which is the argument against.
  xubao       -- hbagan 被割傷 spk 5 against his 割－撕裂－深深地抓傷
  ssiban      -- 吸吮/舔, with the right characters this time
  nuxul       -- its ONE slot is 給你的孩子穿暖和一點吧, which is warm, not 豪雨.
                 If that is right the shipped nuxul>nuhur is a wrong brown, and
                 tnoxol must not be built on top of it.
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


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-13s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


def gl(chars, note=""):
    rx = re.compile("[" + chars + "]")
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss [%s] %s -> %d" % (chars, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-13s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


print("======== HRIG -- is the root 倒入 as well as 倒出?")
om(r"hrig", "every hrig word")

print("\n======== PUSIQ -- eye discharge")
om(r"pusiq|psiq|pusyaq", "pusiq shapes")

print("\n======== NGIRAW / NIRAW -- the fungus")
om(r"ngiraw|niraw|nilaw|riwa$|qihung", "fungus shapes")
print("    his own ng- spellings, to see whether he writes ng at all:")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
hw = [ent.get("hw") or "" for ent in E]
ng = [h for h in hw if re.match(r"^NG", h)]
ni = [h for h in hw if re.match(r"^NI", h)]
print("      headwords starting NG: %d  %s" % (len(ng), ng[:12]))
print("      headwords starting NI: %d  %s" % (len(ni), ni[:12]))

print("\n======== HBAG -- slashing with a blunt tool")
om(r"hbag|hbng|hnbag", "hbag family")

print("\n======== SSIBAN -- suck / lick, traditional characters")
gl("\u5438\u542e\u8214", "吸 吮 舔")

print("\n======== 鍋 with the traditional character")
gl("\u934b", "鍋")

print("\n======== NUXUL -- warm, or heavy rain?")
for ent in E:
    for s in [ent] + ent.get("subs", []):
        for x in s.get("examples", []) or []:
            t = x.get("t") or ""
            if re.search(r"nuxul|noxul|nuxol", t, re.I):
                print("    [%-10s] %-46s %s"
                      % ((ent.get("hw") or "")[:10], t[:46], (x.get("zh") or "")[:44]))
    if re.search(r"nuxul|noxul|nuxol", (ent.get("hw") or "") + (ent.get("paradigm") or ""), re.I):
        print("    HEADWORD %s  %s" % (ent.get("hw"), (ent.get("zh") or "")[:50]))
gl("\u6696", "暖")
