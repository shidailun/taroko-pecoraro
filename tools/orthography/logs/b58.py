"""Batch 58: the rest of the half-brown list, and two brown words that were wrong.

halfbrown.py's ranking again -- for every green token, the brown sibling on the
SAME card whose key shares the longest run of letters -- but this pass ran the
whole list through look.py first, which searches the GLOSS rather than the shape.
That is what turned up the two corrections below; a sibling can only tell you what
the card already believes, and the card can be wrong.

TWO BROWN WORDS THAT NAME A DIFFERENT WORD. Both are homograph traps, and both were
found by reading the modern gloss instead of trusting the existing value.

 - `tnbolox` shipped as `tnbruh`, which the omnibus glosses "「bruh」進入過的人" --
   the man who has ENTERED, from the sound-word bruh. His Tnbolox is 已自立的人,
   已與本家分開的人. The card's own root is bolox>burux 單獨 (pbolox>pburux is
   already brown, and the omnibus glosses pburux 讓…獨自 outright). tnburux.
 - `xolao` sat green on the SECOND XELAO card, and green there is the tell. There
   are two XELAO cards: 咳嗽 and 供躺臥者蓋用的覆蓋物. `hiraw` is 咳嗽;咳痰 and is
   right on the first; `hilaw` is the blanket -- philaw 蓋上被子, mhilaw 用…蓋被子,
   tnhilaw 被子的主人 -- and the card's own Mxelao is already brown as mhilaw. So
   xolao (his spelling in "Nyeqan xolao so?" 你有被子嗎) is hilaw.
   NOTE, not fixed here: the key `xelao` is ONE key and both cards hold that token,
   so the blanket card's headword prints HIRAW and cannot be made to print HILAW by
   a flat map. WORD_OVERRIDES is flat too. A homograph split needs a per-card
   mechanism that does not exist yet; recording it rather than papering over it.

THE REST, in the same three kinds as batch 57.

1. His own two spellings of one token -- and in nine of these he prints the pair
   himself, in parentheses or after "vl.", so the equation is his and not mine:
   Qnqogo (knqogo), Kn'uaan (Knwuaan), mpslxlax (mpslexlax), tsgsutun (tsgasut),
   Pblxun (pbl'xun), lnglngan (lnglongan), llixao (vl. lxlixao),
   and lnngat beside lnnngat in one breath -- "Ima ka lnnngat! Ini ko lnngat ka
   yako!". mpad'gal/mpad'xgal and tityeq/tityex are the same class one card apart.

2. The sibling names the root and the slot is a regular affix on it: shgun after
   s'xgan>shgan (his own paradigm line), puqi after kmpoqon>kmpuqun, tkuyi after
   ktuyan>tkuyan (and kmtuy 收割 42x), qhdi after kxdo>qhdu, pbruxun after
   pbolox>pburux, ptbnahani after ptbnaxon>ptbnahun, pstrmai after pstloma>pstruma
   (truma 下面 99x), csgsutun after tsgasut>csgasut, drnai after dlnani>drnani
   (向…禱告 -- and his line is "Dlnai ta tmaan xo?" 我們去求爸爸), emptbagun after
   ptbago>ptbagu (emptbagu 會燒焦), pnmu/nmu/nnmu/mmu after mpn'mu>empnmu.

3. And six the omnibus names outright, by gloss, where the sibling was only the
   thread that led there: pousal>empusal 二十 142x; tblae>tbalay 填平;平息;平的,
   which is his "把所有的凸起都弄平" word for word; splan>sprang 故意, his "你好像
   是故意要去被車子壓"; botak>bitaq 直到, his "Tgaon miso botak ska xedao" 我會等你
   到中午; idau>idaw 米飯 109x beside his own m'idao>midaw; dmkblenux>dmkbreenux,
   glossed 住在平地的人, which is his word for word. sktadaw follows skbayan
   "已故（已死亡的）「Bayan」（人名）" exactly, and tadaw is 71x in speech.
   gn'lu>gneelug 開闢的路 completes the "LU set beside pn'lu>pneelug.

FROZEN (kind 3 of batch 57 -- the family is frozen and charRules was printing a
fake word beside its brown siblings): slap and smilap beside slapi 切掉 (SRAP,
SMIRAP), sqti beside sqtun 要切斷, dmt'basyaq beside dmt'sapat>dmtsapat and beside
batch 57's own basyaq freeze.

HELD, with the reason, because a real word is not yet the right word:
 - upsk'la. pskla 使趕上 5x is a 0.91 shape match and his gloss is 就能趕上, but the
   leading `u` is not a Truku prefix and not a thing he writes: the whole book has
   THREE u+CC tokens (upsk'la, ukwi, umyaq), one occurrence each. That is a
   transcription defect, and the memory is explicit -- fix the transcription, not
   the spelling map. Same for `dnqpax` 工人, which wants dmqeepah 農民們: his
   typewriter m reads as n, so the token is dmqpax and the repair belongs upstream.
   Recorded as transcription candidates, not mapped.
 - gqoaq 搖頭. The card ships gmqoaq>gmquwaq, but quwaq is 洞口 161x -- a mouth, not
   a shaking head. The sibling may itself be wrong; not following it.
 - luula 公開地. The card ships ntluula>ntreura, but `ura` 公開、清白 is attested and
   ntreura is not. Another sibling under suspicion.
 - mpaba'ba 癰. Follows ba'ba>babaw, but babaw is 上面/後來. Same suspicion.
 - ptlyaon (ptriya unattested), psnnai (he marks it "(?)" himself), ktii (kcii
   unattested; kciyan 收成期 is), pausa, psaanak, siipa, npamanu, daxani, ttidyal,
   maidang, plilyes, pbbagi, xandolu, tinalu, imnglong, mpgdolo, kiiso/isoka
   (scan joins, and freezing a scan artifact would call it verified).
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # two brown words that named a different word
    "tnbolox": "tnburux",            # was tnbruh 「bruh」進入過的人
    "xolao": "hilaw",                # 被子, not hiraw 咳嗽
    # 1. his own two spellings of one token
    "knqogo": "qnqgu",               # Qnqogo (knqogo)
    "knwuaan": "knuwaan",            # Kn'uaan (Knwuaan)
    "mpslexlax": "empslhlah",        # mpslxlax (mpslexlax)
    "lnglngan": "lnglungan",         # lnglngan (lnglongan); 心裡 383x
    "lxlixao": "llihaw",             # llixao (vl. lxlixao)
    "lnnngat": "rnngat",             # beside lnngat in one line
    "mpad'gal": "empaadxgal",        # his mpad'xgal, same gloss
    "tityeq": "cicih",               # his tityex; 一些 124x
    "dmnsuwai": "mnswayi",           # his dmnswai; 兄弟姊妹 347x
    # 2. the sibling names the root
    "s'xgun": "shgun",               # °Smaxo, saxo, s'xgi, s'xgan, s'xgun
    "poqe": "puqi",                  # kmpoqon>kmpuqun
    "tkui": "tkuyi",                 # ktuyan>tkuyan; kmtuy 42x
    "kxdi": "qhdi",                  # kxdo>qhdu 完成
    "pbl'xun": "pbruxun", "pblxun": "pbruxun",   # pbolox>pburux 讓…獨自
    "ptbnxani": "ptbnahani",         # ptbnaxon>ptbnahun
    "pstlmai": "pstrmai",            # pstloma>pstruma; truma 下面 99x
    "tsgsutun": "csgsutun",          # tsgasut>csgasut
    "dlnai": "drnai",                # dlnani>drnani 向…禱告
    "mptbagun": "emptbagun",         # ptbago>ptbagu; emptbagu 會燒焦
    "gn'lu": "gneelug",              # pn'lu>pneelug; 開闢的路
    "pn'mu": "pnmu", "n'mu": "nmu", "nn'mu": "nnmu", "m'mu": "mmu",
    "sia": "qsiya",                  # the KSIA family: ksia>qsiya, 水 525x
    # 3. the omnibus names it outright, by gloss
    "pousal": "empusal",             # 二十 142x
    "tblae": "tbalay",               # 填平;平息;平的
    "splan": "sprang",               # 故意
    "botak": "bitaq",                # 直到 321x
    "idau": "idaw",                  # 米飯 109x; his m'idao>midaw
    "dmkblenux": "dmkbreenux",       # 住在平地的人
    "sktadao": "sktadaw",            # skbayan 已故的「Bayan」; tadaw 71x
    # frozen: the family is frozen and charRules was printing a fake word
    "slap": "slap", "smilap": "smilap",              # slapi 切掉;  SRAP/SMIRAP
    "sqti": "sqti",                                  # sqtun 要切斷
    "dmt'basyaq": "dmtbasyaq",                       # dmt'sapat>dmtsapat
}
# refuse to write anything lexical_map.json has already vetoed -- the b57 lesson:
# adjudicated = (manual|llm) - lex_block, so a null there silently discards the key
lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
blocked = sorted(k for k in FIX if k in lex and not lex[k])
if blocked:
    print("!! lex_block would discard these -- withdrawing: %s" % blocked)
    for k in blocked:
        FIX.pop(k)

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("overriding %d earlier manual keys:" % len(clash))
    for k, (o, n) in sorted(clash.items()):
        print("   %-12s %s -> %s" % (k, o, n))
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch touches %d keys)" % (before, len(d), len(FIX)))
