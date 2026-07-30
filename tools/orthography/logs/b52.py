"""Batch 52: four paradigms found by searching his glosses, not his word shapes.

DGIYAL. He writes the answer on his own headword: DDIYAL （或：DGIYAL）＝戰勝.
dgiyal 勝利, dmgiyal 24x 征服, mdgiyal 會贏, and dnegyalan 6x is his Dndyalan
（贏得的）勝利－勝利的時間、地點 slot for slot.

GDURUG. His KDOLO 生產—分娩 against modern gdurug: mgdurug 生產了, maagdurug
生產順利, ggdurug 生產過程, empgdurug 要坐月子. What settles it is the locative --
his Kd'lgan 分娩的時間、地點 is gdrgan 6x 坐月子, the same slot in the same shape,
which independently confirms that his k- answers to the modern g- right through
the paradigm (kdolo/gdurug, kdlgan/gdrgan).

RUSAQ. SMUSYAQ 混濁的（水）；泥濘的水 is msrusaq 8x 水混濁 (also rmusaq 使污水混濁,
smrsaqan 2x 已混濁, rusaq 污水). His sm- and the modern ms- are the same two
affixes in the other order; nothing else in the omnibus glosses turbid water.

QBUBU. qbobo>qbubu, mqbobo>mqbubu and pqbobo>pqbubu are already brown, so his
Pqboan 被（用帽子）蓋住之物／人 is pqbuan 被帶帽子 -- the gloss is his, verbatim.

Held. The L'NGUT family (l'ngut, lngut, lmngut, lngutan, plngut, mplngut, 9x)
is a real gap, not a spelling: rngut and lngut are absent from every corpus, and
modern Truku says pregnancy with mshjil 65x 'heavy' (knshjilan 5x 懷孕,
srjingan 剛懷孕的). That covers his Lngutan 被受孕－懷孕 but not his causatives
Lmngut / Plngut 使受孕, for which only pshjil 1x exists, unglossed. Nulled in
lexical_map with the evidence rather than forced into a substitution, so no
tier can claim them later.
"""
import json, io, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # DDIYAL (= his own DGIYAL)
    "ddiyal": "dgiyal", "dmdiyal": "dmgiyal", "mddiyal": "mdgiyal",
    "dndyalan": "dnegyalan",
    # KDOLO -> gdurug
    "dolo": "gdurug", "kdolo": "gdurug", "mdolo": "mgdurug",
    "mpkdolo": "empgdurug", "kdlgan": "gdrgan",
    # odds
    "smusyaq": "msrusaq", "pqbboan": "pqbuan",
}
BLOCK = ["l'ngut", "lngut", "lmngut", "lngutan", "plngut", "mplngut"]
NOTE = (
    "L'NGUT (LNGUT) 使受孕（用於人類）－受孕, with Lmngut, Lngutan, Plngut, Mplngut. "
    "rngut and lngut are absent from the omnibus, from the spoken corpus and from "
    "truku_dict; there is no reflex of this root at all. Modern Truku says pregnancy "
    "with mshjil 65x, literally 'heavy' -- knshjilan 5x huaiyun, srjingan gang huaiyun de. "
    "That is a substitute for his Lngutan bei shouyun-huaiyun, but not for the causatives "
    "Lmngut / Plngut shi shouyun, where only pshjil 1x exists and is unglossed. Half a "
    "paradigm is not a substitution, so nothing is named: null, frozen out of every tier, "
    "left green.")

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch adds %d)" % (before, len(d), len(FIX)))

q = H + "lexical_map.json"
lx = json.load(io.open(q, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
lx["_lngut"] = NOTE
for k in BLOCK:
    lx[k] = None
body = ",\n ".join("%s: %s" % (json.dumps(k, ensure_ascii=False),
                               json.dumps(v, ensure_ascii=False))
                   for k, v in lx.items())
io.open(q, "w", encoding="utf-8", newline="\n").write("{\n " + body + "\n}\n")
print("lexical_map: %d keys (%d blocks added)"
      % (len([k for k in lx if not k.startswith("_")]), len(BLOCK)))
