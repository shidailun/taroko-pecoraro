"""Batch 51: three families and the leftovers of the apostrophe-initial class.

WEELA. His WA'LA 'in front - to lead' is modern weela 6x 前(先)鋒, and every slot
he wrote has an attested modern twin: pweela 8x 事先, tweela 前導, empweela 2x
領導者;猴群的前導, dempweela 1x. m'wa'la is glossed 在前者－引領者(？) -- his own
question mark -- and that is empweela's gloss exactly, so it merges with mpwa'la
the way tkleun/tkliyun merged into tqriun. mtwa'la is held: mt- is a live modern
prefix but mtweela is attested nowhere, so naming it would be construction.

GEALU. sgealu 23x 可憐 and pgealu 3x 要憐愛 against his GAALU 憐憫.

X'DYEQ. His second spelling of the far root. Every dxyaq-spelled slot is already
brown (d'xyaq>thiyaq, mdxyaq>mthiyaq), so the x'dyeq-spelled ones are the same
words: thiyaq 43x. Held: x'mdyeq, pdx'dyeq, pdxdyeq, ptx'dyeq -- no brown twin
and no attested tmhiyaq / pdthiyaq to point at.

MORISAKA. morisaka>murisaka is already brown (tier N) and dmorisaka>dmurisaka
followed it; mk- and nk- + place name is the modern ethnonym (mkbranaw 2x 重光的
人), so these are arithmetic on a decided sibling.

'SIG. The apostrophe-initial class has three members left. esig 12x 膿 with
teesigan 2x 長膿包 and maaesig 2x 變成膿包 is his "SIG 癤子（癰）, and 'siu is the
variant he flags himself ("SYU = GSIG), used once, of the same referent.
'mu stays blocked -- see lexical_map.

Held with reasons: mnnaspat 八次 (mn- + numeral is the modern pattern -- mndha,
mntru 4x, mnrima 12x, mnspat 4x -- and his Mnnaspat is Mnmaspat under his own
typewriter m/n, but no 八次 form is attested in any corpus); knss'gan (he keeps
kns'gan 令人恐懼的地方 and knss'gan 令人害怕的能力 apart, and only knsgan is on
record); smpsaan, tipyaq/tepyaq/tbilan (?? in his own gloss), wakat 犬齒, likut
藉口 -- nothing in the omnibus glosses any of them.
"""
import json, io, sys, os
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # WA'LA -> weela
    "wa'la": "weela", "pwa'la": "pweela", "twa'la": "tweela",
    "mpwa'la": "empweela", "m'wa'la": "empweela", "dmpwa'la": "dempweela",
    # GAALU -> gealu
    "sgaalu": "sgealu", "pgaalu": "pgealu",
    # X'DYEQ -> thiyaq
    "x'dyeq": "thiyaq", "dxdyeq": "thiyaq", "mx'dyeq": "mthiyaq",
    # MORISAKA
    "mkmorisaka": "mkmurisaka", "nkmorisaka": "nkmurisaka",
    # apostrophe-initial leftovers
    "'sig": "esig", "'siu": "esig",
    # sibling arithmetic off a brown paradigm
    "mpkuda'": "mpkudaw", "pntyusan": "pnteayusan", "knkbyanan": "knegbiyan",
}

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("already mapped differently:", clash)
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch adds %d keys)" % (before, len(d), len(FIX)))
