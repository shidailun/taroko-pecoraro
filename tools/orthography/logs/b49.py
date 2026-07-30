"""Batch 49 -- the same sweep at MIN=1, twenty-six keys.

sib.py run down to single occurrences. Same shape as batch 48: a green form whose card
already carries a brown sibling, resolved by affix arithmetic rather than by lookup.

Attested at the far end:
  Llgan 移動的動作     -> llgan 1x  (lilu -> lilug from batch 46; klgan 215x 種類, lglgan, knlgan)
  Tsiiso / Tsiso 受驚嚇 -> cseisug 4x (kiso -> keisug 16x 要怕 brown)
  SNTO 談論－閒談      -> sntug 1x 說八卦  (msnto -> msntug landed in batch 48)
  YAQ 田裡的輕活       -> yak 1x    (miyaq -> miyak brown; he cross-refers MIYAQ himself)
  Q'QOL 挖鑿－雕刻     -> qur 4x    (q'mqol -> qmqur 3x and qnqolan -> qnquran brown)
  "MU 極細的粉－細塵   -> emu 37x   -- his initial ' before a labial is the schwa the W tier
      spells em-, and emu is 香蕉糕/糖 because it is what pounded grain flour becomes. His two
      examples are "mu basao 粉 and "mu d'xgal 塵土, both of them emu.

Blind, forced by a brown sibling:
  Blnaxan 後退的地點  -> brnahan   -- sbrnahan 4x carries the stem; blenax -> brinah 19x brown
  Kntblnaxan 忘恩負義 -> kntbrnahan -- and tbrinah 5x is glossed 背叛 exactly
  Tqoan 所受的冒犯    -> tquwan    (ptqoan -> ptquwan brown)
  Tkleun / Tkliyun 要倒入的東西 -> tqriun (tklean -> tqrian 7x 裝填 brown; only the focus moves)
  T"tuan 切成的塊     -> ttuan     -- sttuan 3x carries it; batch 48 put Ttuun on ttuun
  Yiaxan 到來         -> yyahan    -- his own variant Yeyaxan is already brown on yyahan
  Psyangun 要養肥的豬 -> psyangun  (siyang 107x 肉, knsyangan 13x, ksiyang 肥)
  Tmdilas             -> tmjiras   (tdilas -> tjiras, mtdilas -> mtjiras brown)
  Pkpnpong 使產生波紋 -> pkpnpung  (pnpong -> pnpung brown)
  Spitai 有臭蟲味     -> spitay    (pitai -> pitay 12x brown)
  T'nling 渾身是汗    -> tnring    (m'ling -> mring 13x 汗水; batch 48 took Mt'nling -> mtnring)
  Pkbuyo 使荒蕪－遮蔭 -> pkbuyu    (buyo -> buyu brown)
  LUT 重壓於上        -> rut       (mlut -> mrut 9x 按住, p'lut -> prut 壓 brown)
  UMUL 含在口中吸吮   -> umul      (mumul 含在嘴裡不咬碎 and mulun brown, unchanged)
  NYAQ 存在－居住－有 -> niq       (nyaqan -> niqan 2170x brown, as NYEQ took in batch 48)
  N'yano / DD'yano 你們的 -> nyanu / ddyanu (namo -> namu, d'yamo -> dyamu, yiano -> yianu brown)
  Bntudan 接合處      -> bntudan   (pltudan and pnltudan 3x brown; he calls it a variant of
      Pltudan himself, and nothing in the modern stem moves)

Held on this pass:
  ti 18x -- his own particle card. The joined forms were settled long ago and they do NOT
      agree: Titmaq -> tgtmaq and Tit'lo -> tgtru take the tg- of the standard (he notes
      himself that others say TGTMAQ, not TITMAQ), but Tityex -> cicih is a reduplicant. So
      ti- is resolved per word, and the bare proclitic has no word to be. It stays green.
  nta 20x -- 邀請前往. lita 48x 一起 is the meaning, but he uses both in ONE example,
      "Nta da! ... Kia! Lita da!", so they are two words for him and nta is unattested.
  lex 5x 幾乎－有點像 -- 幾乎 gives only srgsug, 差不多 only mgbaka; the modern equivalent
      is the mg- prefix, not a word.
  de 7x / la 5x / et 3x are French out of his own glosses (de la page précédente; Mikat et
      Ingai; Kndusan = La vie), not Truku at all.
  Knss'gan, Pntyusan, Tlqelan, Knlsan, Smpsaan, LUULA, Smilap -- two candidate shapes each and
      no gloss to choose, or a blind sibling to stand on.
"""
import json, sys, pickle
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MP = H + "tools/orthography/manual_map.json"
SPK = json.load(open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
O = pickle.load(open("omni.pkl", "rb"))
OMNI = {}
for w, g, _ in O[0]:
    OMNI.setdefault(w.lower(), g)
LEX = set(SPK) | set(OMNI)

FIX = {
    "llgan": "llgan", "tsiiso": "cseisug", "tsiso": "cseisug", "snto": "sntug",
    "yaq": "yak", "q'qol": "qur", "'mu": "emu",
    "blnaxan": "brnahan", "kntblnaxan": "kntbrnahan", "tqoan": "tquwan",
    "tkleun": "tqriun", "tkliyun": "tqriun", "t'tuan": "ttuan", "yiaxan": "yyahan",
    "psyangun": "psyangun", "tmdilas": "tmjiras", "pkpnpong": "pkpnpung",
    "spitai": "spitay", "t'nling": "tnring", "pkbuyo": "pkbuyu", "lut": "rut",
    "umul": "umul", "nyaq": "niq", "n'yano": "nyanu", "dd'yano": "ddyanu",
    "bntudan": "bntudan",
}
BLIND = {"brnahan", "kntbrnahan", "tquwan", "tqriun", "ttuan", "yyahan", "psyangun",
         "tmjiras", "pkpnpung", "spitay", "tnring", "pkbuyu", "rut", "umul", "niq",
         "nyanu", "ddyanu", "bntudan"}
for k, v in sorted(FIX.items()):
    assert v in LEX or v in BLIND, "unattested target not declared blind: %s -> %s" % (k, v)
G = json.load(open("green_true.json", encoding="utf-8"))
notgreen = [k for k in FIX if k not in G]
assert not notgreen, "already brown, would collide: %s" % notgreen
M = json.load(open(MP, encoding="utf-8"))
before = len(M)
M.update(FIX)
body = ",".join(json.dumps(k, ensure_ascii=False) + ": " + json.dumps(v, ensure_ascii=False)
                for k, v in sorted(M.items()))
open(MP, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d keys" % (before, len(M)))
won = 0
for k, v in sorted(FIX.items()):
    won += G.get(k, 0)
    print("   %-11s %-12s %4dx %-22s%s" % (k, v, SPK.get(v, 0), (OMNI.get(v) or "")[:22],
                                           "  BLIND" if v in BLIND else ""))
print("green occurrences claimed: %d over %d types" % (won, len(FIX)))
