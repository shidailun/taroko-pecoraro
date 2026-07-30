"""Batch 54: half-brown cards, finished off.

Every key here sits on a card whose root is already decided by brown siblings.
None of them is a research question; each is a slot that was skipped when the
family was mapped, which is the pattern CLAUDE.md finding (4) describes.

XOAI. The card already keeps his two spellings apart -- xoai/xowai are huway,
xway is hway (sgxwayun>sghwayun was mapped that way). So sgxway and sgxwayan
follow the hway stem, which the omnibus carries eleven times over (khwayi,
ghwayi 3x, ghwayun 7x, gnhwayan, pshwayi). pkxoayun is the -un of pkhuway, and
mpkxoai is the em-p- future of khuway, on the pattern of emphuway/empghuway.

BLENAX. brnah- is the stem: pbrnahi 3x, sbrnahan 4x, sbrnahun 2x, brnahun. His
pblnaxan and sblnaxon are already pbrnahan and sbrnahun, so pblnaxon and sblnaxe
are the same two suffixes on the same stem.

L'XEQ. rhiq 16x 'skin', qrhiq 'peeling'; his kl'xqan and ql'xqan are both already
qrhqan, so the -e and -on slots are qrhqi and qrhqun. He writes the initial both
ways himself, which is why two of his spellings land on one modern word.

STA"TO. sttuan 3x is attested and his sttoan is already mapped onto it, so the
stt- shape is the card's decision; sttui, sttuun and knsttuan keep it. smt'to
still held -- msta'to>msttu and snta'to>snteetu disagree with each other, and I
am not going to pick a side by construction.

PARO. sprui 9x and spruun 24x are both attested and both already mapped, so
sploan is spruan.

Two he equates himself. "Ludan bi (vl.: Luuda bi)" makes luuda rudan 380x, and
sbiyaq is his other spelling of sbiyao, already mapped to sbiyaw 281x.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # XOAI -- hway stem for his xway spellings, huway for his xoai ones
    "sgxway": "sghway", "sgxwayan": "sghwayan",
    "pkxoayun": "pkhuwayun", "mpkxoai": "empkhuway",
    # BLENAX
    "pblnaxon": "pbrnahun", "sblnaxe": "sbrnahi",
    # L'XEQ -- both his initials land on the one modern stem
    "kl'xqe": "qrhqi", "ql'xqe": "qrhqi",
    "kl'xqon": "qrhqun", "ql'xqon": "qrhqun",
    # STA"TO
    "knsttuan": "knsttuan", "sttui": "sttui", "sttuun": "sttuun",
    # PARO
    "sploan": "spruan",
    # his own variant tags
    "luuda": "rudan", "sbiyaq": "sbiyaw",
}

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("overriding %d earlier manual keys:" % len(clash))
    for k, (o, n) in sorted(clash.items()):
        print("   %-10s %s -> %s" % (k, o, n))
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch touches %d keys)" % (before, len(d), len(FIX)))
