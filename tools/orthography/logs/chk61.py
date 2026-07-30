"""The matcher's top rows, run through the half-brown test before believing any.

greenmatch2 scores shape x gloss and nothing else -- it cannot tell a cognate from
a coincidence, and it happily proposed psmrata for his swatan (軍隊 by gloss, a
Japanese loan by history) and kmptuhan for his kdapan (寡婦 by gloss, but that
value is already the answer to his KPTOXAN, batch 32). What settles a row is the
FAMILY: if his card's siblings are already mapped, the root has been decided and
the green form only has to join them.

Five rows, each with: his card, every key of his the map already answered, and the
modern root by shape.
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
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


CASES = [
    ("maidang  遺失", r"^MAIDANG|^MEIDANG", r"aidang|eidang", r"ridang|rdang"),
    ("bsqlol   鍋底燒焦", r"^BSQLOL", r"bsqlol|sqlol", r"sqrul|bsqrul|sqrur"),
    ("ptlyaon  使旋轉", r"^PTLYAON|^TLYA|^LYAON", r"tlya|lyaon|tlyaun", r"striya|triya|stryai"),
    ("lnbu     浸泡", r"^LNBU|^L'NBU|^LBU", r"lnbu|lmbu|nlbu", r"rbug|rnbug|rmbug"),
    ("x'lyeq   撕裂", r"^X'LYEQ|^XG'LYEQ", r"lyeq", r"gliq|hgliq|negliq"),
]

for label, cardpat, keypat, shape in CASES:
    print("\n" + "=" * 74)
    print("== %s" % label)
    cp = re.compile(cardpat)
    for ent in E:
        if not cp.match((ent.get("hw") or "").upper()):
            continue
        print("   hw %s %s  |  %s"
              % (ent.get("hw"), ent.get("tag") or "", (ent.get("zh") or "-")[:52]))
        for x in ent.get("examples", []):
            print("   § %-48s %s" % (x.get("t", "")[:48], (x.get("zh") or "")[:34]))
        for s in ent.get("subs", []):
            print("   - %-16s %s" % (s.get("form", ""), (s.get("zh") or "")[:46]))
            for x in s.get("examples", []):
                print("       § %-44s %s"
                      % (x.get("t", "")[:44], (x.get("zh") or "")[:32]))
    kp = re.compile(keypat)
    print("   -- his keys already answered --")
    got = 0
    for k in sorted(MAP):
        if kp.search(k):
            print("      %-14s -> %-14s omni %-22s spk %s"
                  % (k, MAP[k], (OMNI.get(MAP[k]) or "-")[:22], SPK.get(MAP[k], 0)))
            got += 1
    if not got:
        print("      (none)")
    blk = [k for k in LEX if kp.search(k) and not LEX[k]]
    if blk:
        print("      LEXNULL:", blk)
    print("   -- modern by shape /%s/ --" % shape)
    r, n = re.compile(shape), 0
    for w in ALL:
        if r.search(w):
            print("      %-16s %-32s spk %s"
                  % (w, (OMNI.get(w) or "-")[:32], SPK.get(w, 0)))
            n += 1
            if n >= 20:
                print("      ...")
                break
    if not n:
        print("      (nothing)")
