"""Batch 53: two whole cards were mapped to the wrong root, and both say so.

GAO. Modern Truku ablauts the choose root -- gaaw bare, geeg- before a suffix:
geegi 'yao xuan', geegan 'tiao le', geegun 2x, psgeegi 5x, psgeegan 4x, psgeegun.
That is his GAO / g'g- alternation, letter for letter, and it means every suffixed
slot on the card was mapped to a made-up gg- string (ggi, ggan, ggun, gngan,
psggi) when the real word was on record all along. gn'gan is the clincher:
gneegan 11x 'fenlei; fen hao' against his Gn'gan 'yizuo de xuanze - bei xuanzhong
zhi wu'. He also brackets Psgagan (psg'gan) himself, so those two are one slot.

GAGWI. His headword note names the variant: (bianti G'GUI). So g'gui is gagwi is
geeguy, m'gui is magwi is gmeeguy 21x -- he brackets that pair too, in the Magwi
gloss and again inside an example, "magwi (m'gui)". Same for mpg'gui, which his
Mpgagwi entry brackets, and for guyun, where his example writes the equation out:
"guyun (= gguyun)", and gguyun is already geuyun. mkmagwi was pointing at
mkgmeeguy, which exists nowhere; mkmgeeguy 'xiang yao toutou de' is his gloss.

OTOç. The card is utux 'ling' throughout -- he derives Motoç from it in his own
note, "(lai zi cigen Otoç?)" -- but four slots were mapped onto putuh 'duan', a
different root that merely looks the same after x>h. muutux is 'jingshenbing',
his Motoç 'cuoluan de ling - fengkuang de'; peutux is 'shi...cuoluan', and the
omnibus sentence Dmeegul muhing peutux seejiq ka prwayun dha = 'they are people
who manipulate others' is his P'otoç 'ba ren shua de tuantuanzhuan - qipian -
yunong' exactly; peeutux 'xuyi shi zhi cuowu' is his Paotoç, the future. mp'otoç
merges into peutux the way m'wa'la merged into empweela in batch 51.

The three suffixed slots (ptuxi, ptuxan, ptuxun) are inflectional completions,
not lookups: no -i/-an/-un form of this stem is attested. They are named anyway
because leaving them green is not neutral -- charRules prints PTUHI and PTUHAN,
which are real words of the OTHER root, so the reader currently shows 'cut it
off' where he wrote 'fool him'.

KALIP. His tag settles the initial: "(parfois: QALIP)". His own paradigm settles
the rest -- bare KALIP with p, suffixed KLIB- with b, which is final devoicing,
and the suffixed forms are already qribi/qriban/qribun. So the stem is qrib- and
the bare slot is qrip: 36 words in the omnibus end in p, exactly one ends in b.
No bare or AF form of this root is attested (nor of qrap), so qrip/qmrip and
qrap/qmrap are stem-shape claims, flagged as such.

Held. patuxun and pntuxan on OTOç -- pntuxan 'xianjing - guiji' is a noun and may
be a separate lexeme, and patuxun hangs off paotoç, whose own -un is unattested.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # GAO -- the choose root ablauts gaaw / geeg-
    "g'gi": "geegi", "g'gan": "geegan", "g'gun": "geegun",
    "gn'gan": "gneegan", "psg'gi": "psgeegi",
    "psg'gan": "psgeegan", "psgagan": "psgeegan", "psg'gun": "psgeegun",
    # GAGWI -- the variants he brackets himself
    "g'gui": "geeguy", "m'gui": "gmeeguy", "mpg'gui": "mpgeeguy",
    "guyun": "geuyun", "mkmagwi": "mkmgeeguy",
    # OTOç -- utux, not putuh
    "moto\u00e7": "muutux", "p'oto\u00e7": "peutux", "mp'oto\u00e7": "peutux",
    "paoto\u00e7": "peeutux",
    "ptuxi": "peutuxi", "ptuxan": "peutuxan", "ptuxun": "peutuxun",
    # KLUULUS -- pkrrusi 3x, pkrrusun 1x decide the rest
    "pkllusun": "pkrrusun", "pkllusan": "pkrrusan", "pnkllusan": "pnkrrusan",
    # KALIP / K'LAP -- stem from the attested suffixed forms
    "kalip": "qrip", "kmalip": "qmrip", "mkalip": "mqrip", "pkalip": "pqrip",
    "k'lap": "qrap", "kmlap": "qmrap",
    # leftovers whose siblings are already brown
    "tsaon": "tsaun", "klulu": "klulug",
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
