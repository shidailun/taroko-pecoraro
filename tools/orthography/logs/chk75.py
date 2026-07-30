"""ngali and kyoxan: the same self-contradiction as pax, for the third and fourth
time. Verify ownership and attestation before writing.

NGALI 8x -- his 剩餘——多出的——額外的, surplus. The value is ngali 拿走；拿取 spk 27,
which is the TAKE word (his own MASPAT note glosses MANGALI as MA+NGALI＝拿！, so
that word is real and he uses it). But modern ngari is 剩餘;結餘 spk 31, and:
      his nngali        -> nngari 剩餘的 spk 19   ALREADY SHIPPED
      his sn'gali/sngali-> sngari 剩餘 spk 10     ALREADY SHIPPED
so the map already accepts the ngari root for the derived forms. The question is
purely whether the bare key belongs to the surplus card or the take card.

KYOXAN 9x -- his 對女人們—對女人—為女人, the oblique of KOYOX. The map already ships
      his koyox/koyoç/koyux -> kuyuh 女性;女人 spk 1196
      his dkoyox            -> dkuyuh 女人們 spk 63
while kyoxan sits on kyuhan spk 0 已擦傷, which is the rub/scrape root. Find what
the oblique of kuyuh actually looks like before proposing anything -- if it is not
on record this is a hold, like snax.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-34s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:34] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== the ngari / ngali split ===")
for w in ("ngari", "ngali", "nngari", "sngari", "gnari", "ngarian", "mngari",
          "angal", "mangal", "empngari"):
    show(w)

print("\n=== the oblique of kuyuh ===")
for w in ("kuyuhan", "kyuhan", "kuyuh", "dkuyuh", "kykuyuh", "knkuyuh", "skuyuh"):
    show(w)
print("   -- every omnibus word containing 'kuyuh' --")
for s, w in sorted({(SPK.get(w, 0), w) for w in OMNI if "kuyuh" in w}, reverse=True)[:10]:
    show(w, "      ")

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
print("\n########## who owns 'ngali' and 'kyoxan' ##########")
for target in ("ngali", "kyoxan"):
    print("\n-- %s --" % target)
    seen = []
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"),
                 (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            for w in TOK.findall(f or ""):
                if key(w) == target:
                    r = (hw[:16], kind, (g or "")[:48])
                    if r not in seen:
                        seen.append(r)
    for r in seen:
        print("   [%-16s] %-4s %s" % r)

print("\n########## his NGALI and KOYOX cards ##########")
for ent in E:
    hw = (ent.get("hw") or "")
    if not re.match(r"^(NGALI|KOYOX|KOYO\u00c7)", hw.upper()):
        continue
    print("\n--- %s  %s" % (hw, (ent.get("zh") or "")[:80]))
    for s in ent.get("subs", [])[:9]:
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("   sub %-13s -> %-11s %s" % (f[:13], MAP.get(kk, "(green)"),
                                            (s.get("zh") or "")[:42]))
