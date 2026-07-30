"""Generate-and-test over the greens, using the correspondences his orthography
is now KNOWN to use rather than a blind edit distance.

Every detector so far has worked from a distance metric or a gloss overlap, and
both are noisy in the same way: they rank string coincidences (nta against 他的)
alongside real matches. This one goes the other direction. His spelling system is
partly known -- each rule below was established by keys already shipped and
human-checked -- so expand a green through EVERY combination of those rules and
keep only the expansions that are attested modern words. A hit is then not "close
to" a modern word; it IS one, reachable from his spelling by rules he demonstrably
follows. The gloss is printed beside it so the meaning still has to agree.

  x -> h    hrig, hbagun, hiyi        x -> x    uxul 暖和 (modern keeps x too)
  l -> r    the charRules default     l -> l    the keep-l guard, 28 tokens
  o -> u    charRules                 -ao -> -aw  longao>lungaw, niyao>ngiyaw
  n -> ng   NYAO/NIYAO > ngiyaw, established in batch 68
  y -> i    pusyaq>pusiq, kyoxan      e -> e/i
  +g        x'li>hrig, ayo>ayug -- he drops final velars
  ' -> nothing / e                    his schwa
  qo -> qu, c -> c/ts

Cap the product per token so a long word cannot blow up; report what was skipped
rather than dropping it silently.
"""
import io, sys, json, pickle, re, collections, itertools
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
MARKS = "['\u2019\u02bc\"\u0294]"


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, g))

# per-character alternatives. A single char may expand to a two-char string (n->ng)
ALT = {
    "x": ["h", "x"],
    "l": ["r", "l"],
    "o": ["u", "o"],
    "n": ["n", "ng"],
    "y": ["y", "i"],
    "e": ["e", ""],
    "'": ["", "e", "u"],
    "c": ["c", "s"],
}
CAP = 6000


def expand(tok):
    """Every string reachable from his token by the known correspondences."""
    pools = [ALT.get(ch, [ch]) for ch in tok]
    n = 1
    for p in pools:
        n *= len(p)
    if n > CAP:
        return None
    out = set()
    for combo in itertools.product(*pools):
        s = "".join(combo)
        out.add(s)
        out.add(s + "g")          # he drops final velars: x'li>hrig, ayo>ayug
        out.add(s + "q")
        if s.endswith("aw"):
            out.add(s[:-2] + "aw")
        if s.endswith("u"):
            out.add(s[:-1] + "aw")
    return out


MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
greens = sorted({t for t in his if t not in MAP and len(his[t]) >= MIN and len(t) > 2},
                key=lambda t: -len(his[t]))
print("greens at >=%d slots: %d types" % (MIN, len(greens)))

skipped, hits = [], []
for t in greens:
    cands = expand(t)
    if cands is None:
        skipped.append(t)
        continue
    found = [(SPK.get(c, 0), c) for c in cands if c in OMNI and c != t]
    if found:
        hits.append((len(his[t]), t, sorted(found, reverse=True)))

print("skipped (too many expansions): %d  %s" % (len(skipped), skipped[:8]))
print("greens with at least one ATTESTED expansion: %d\n" % len(hits))

for n, t, found in sorted(hits, reverse=True):
    hw, kind, g = his[t][0]
    print("%2dx %-14s [%-11s] %s" % (n, t, hw[:11], (g or "")[:56]))
    for s, c in found[:6]:
        print("        %-14s spk %-5d %s" % (c, s, " | ".join(dict.fromkeys(OMNI[c]))[:52]))
