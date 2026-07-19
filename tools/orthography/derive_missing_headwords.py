import json, openpyxl, unicodedata, collections, re

SCRATCH = r"C:/Users/user/AppData/Local/Temp/claude/C--dev-formosan-seediq/c9019950-6676-4f9c-827b-5410d342331e/scratchpad"

def norm(w):
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return w.lower()

MAP = {"x": "h", "o": "u", "l": "r"}
def modernize(n):
    return re.sub(r"[xol]", lambda m: MAP[m.group(0)], n)

wb = openpyxl.load_workbook(
    r"C:/Users/user/OneDrive - Lingnan University/Desktop/SeediqPro/dictionaries/omnibus/Truku_Omnibus.xlsx",
    read_only=True, data_only=True,
)
ws = wb["Words"]
rows = list(ws.iter_rows(min_row=2, values_only=True))

pos_lookup = collections.defaultdict(lambda: collections.Counter())
zh_lookup = collections.defaultdict(list)
for r in rows:
    word, zh, pos = r[1], r[2], r[4]
    if not word:
        continue
    n = norm(word)
    if pos:
        pos_lookup[n][pos] += 1
    if zh:
        zh_lookup[n].append(zh)

missing = json.load(open(SCRATCH + "/missing_headwords_grouped.json", encoding="utf-8"))

FUNCTION_POS = {"代名詞", "連接詞", "介詞", "助詞", "數詞", "疑問詞", "感嘆詞", "連詞"}

rows_out = []
recovered = []
for count, n, form in missing:
    poses = pos_lookup.get(n)
    matched_via = "exact"
    if not poses:
        mn = modernize(n)
        if mn != n:
            poses = pos_lookup.get(mn)
            if poses:
                matched_via = "modernized"
    zh = zh_lookup.get(n) or zh_lookup.get(modernize(n))
    if poses:
        top_pos = poses.most_common(1)[0][0]
        kind = "function" if top_pos in FUNCTION_POS else "content"
        zh_sample = zh[0] if zh else ""
        rows_out.append((count, form, kind, top_pos, zh_sample, matched_via))
        if matched_via == "modernized" and kind == "content":
            recovered.append((count, form, top_pos, zh_sample))
    else:
        rows_out.append((count, form, "unknown", "", "", ""))

json.dump(rows_out, open(SCRATCH + "/missing_annotated2.json", "w", encoding="utf-8"), ensure_ascii=False)

content = [r for r in rows_out if r[2] == "content"]
unknown = [r for r in rows_out if r[2] == "unknown"]
function = [r for r in rows_out if r[2] == "function"]
print("function-word matches:", len(function), "occurrences:", sum(r[0] for r in function))
print("content-word matches (real gap candidates):", len(content), "occurrences:", sum(r[0] for r in content))
print("unknown (no match at all, even after modernizing):", len(unknown), "occurrences:", sum(r[0] for r in unknown))
print()
print("newly recovered via orthography-normalized match:", len(recovered), "occurrences:", sum(r[0] for r in recovered))
print()
print("=== top newly-recovered content-word gap candidates ===")
recovered.sort(key=lambda r: -r[0])
for count, form, pos, zh in recovered[:60]:
    print(count, form, "|", pos, "|", zh)
