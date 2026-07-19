import json, openpyxl, unicodedata, re, collections, difflib

SCRATCH = r"C:/Users/user/AppData/Local/Temp/claude/C--dev-formosan-seediq/c9019950-6676-4f9c-827b-5410d342331e/scratchpad"
entries = json.load(open(SCRATCH + "/pecoraro_entries.json", encoding="utf-8"))

PUNCT_RE = re.compile(r"[^一-鿿]")
def zh_clean(s):
    return PUNCT_RE.sub("", s or "")

def norm(w):
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = w.lower().replace("'", "")
    return re.sub(r"[^a-z]", "", w)

pec_zh = []
for e in entries:
    z = zh_clean(e.get("zh", ""))
    if z:
        pec_zh.append((e["hw"], z))

wb = openpyxl.load_workbook(
    r"C:/Users/user/OneDrive - Lingnan University/Desktop/SeediqPro/dictionaries/omnibus/Truku_Omnibus.xlsx",
    read_only=True, data_only=True,
)
ws = wb["Words"]
rows = list(ws.iter_rows(min_row=2, values_only=True))
modern = []
for r in rows:
    word, zh = r[1], r[2]
    zc = zh_clean(zh)
    if word and zc and len(zc) >= 2:
        modern.append((word, zc))

bigram_index = collections.defaultdict(set)
for i, (hw, z) in enumerate(pec_zh):
    for j in range(len(z)-1):
        bigram_index[z[j:j+2]].add(i)

pairs = []
for word, zc in modern:
    bigrams = [zc[j:j+2] for j in range(len(zc)-1)]
    cand_sets = [bigram_index.get(bg, set()) for bg in bigrams if bg in bigram_index]
    if not cand_sets:
        continue
    cand = set.intersection(*cand_sets) if len(cand_sets) == len(bigrams) else set.union(*cand_sets)
    for i in cand:
        hw, z = pec_zh[i]
        if zc in z:
            pairs.append((hw, word, zc, z))

print("gloss-match candidate pairs:", len(pairs))

# now filter to pairs where normalized spelling is reasonably close (real correspondence, not homonym coincidence)
def edit_distance(a, b):
    if a == b: return 0
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0]*len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j]+1, cur[j-1]+1, prev[j-1]+cost)
        prev = cur
    return prev[-1]

close_pairs = []
for hw, word, zc, z in pairs:
    a, b = norm(hw), norm(word)
    if not a or not b:
        continue
    d = edit_distance(a, b)
    maxlen = max(len(a), len(b))
    if d <= max(2, maxlen * 0.4):
        close_pairs.append((hw, word, d, zc))

print("close-spelling gloss-confirmed pairs:", len(close_pairs))
json.dump(pairs, open(SCRATCH + "/gloss_pairs_all.json", "w", encoding="utf-8"))
json.dump(close_pairs, open(SCRATCH + "/gloss_pairs_close.json", "w", encoding="utf-8"))

for hw, word, d, zc in close_pairs[:40]:
    print(hw, "->", word, "| d=", d, "|", zc)
