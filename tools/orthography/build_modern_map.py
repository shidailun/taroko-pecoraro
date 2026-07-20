"""Build the word-level modern-spelling map for the Pecoraro dictionary app.

Pipeline (per distinct displayed Truku token):
  1. identity check    — original spelling already attested in the modern Truku
                         omnibus -> keep as-is (tier "id")
  2. candidate gen     — per-occurrence x>h / o>u / l>r branching, plus contextual
                         transforms (final -e>-i, -ae/-ai>-ay, -ao>-aw, -ea/-ia>-iya,
                         d>j before i, intervocalic u>w, e>i) applied on top
  3. attestation filter— candidate must exist in omnibus Words (strong) or as a
                         token of an omnibus Sentence (weak)
  4. gloss check       — Chinese gloss of the Pecoraro form vs the omnibus word's
                         Chinese gloss; a real overlap promotes to tier "A"
  5. tiering           — A  = Words-attested + gloss-confirmed
                         B  = unique attested candidate (no gloss available/needed)
                         C  = multiple attested candidates, gloss can't decide ->
                              NOT auto-applied; written to review file
Output:
  tools/orthography/modern_map.json   full evidence, all tiers incl. review
  site/modern_map.js                  window.MODERN_MAP, tiers id/A/B only
Superseded: site/keep_words.js (identity entries now live in the map).
"""
import json, re, unicodedata, collections, itertools, os, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
ENTRIES = os.path.join(BASE, "site", "entries.js")
OMNIDIR = r"C:/Users/user/OneDrive - Lingnan University/Desktop/SeediqPro/dictionaries/omnibus"
OMNIBUS = OMNIDIR + "/Truku_Omnibus.xlsx"
TGDAYA = OMNIDIR + "/Omnibus.xlsx"          # Tgdaya omnibus (Words: word col 1, 華語 col 5)
TODA = OMNIDIR + "/toda.xlsx"               # no header row: word col 0, 中文 col 1

OVERRIDE_KEYS = {
    "klui", "mklui", "nklui", "tklui", "sklui", "msklui", "psklui",
    "mnsklui", "snklui", "mnklui", "kui", "mskui", "kskui", "ktui", "kmtui",
    "mktui", "bkui", "bukui", "mukui", "mkui", "mkbukui", "bklui", "bq'lui",
    "tutui", "mtutui", "dui", "dmui", "mdui", "mddui", "pdui", "sdui",
    "mndui", "mpdui", "xbui", "xmbui", "pxbui", "xnbui", "m'xapui", "mapui",
}

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ'’ʼ]+")
ZH_RE = re.compile(r"[^一-鿿]")

def norm(w):
    # Pecoraro's ç is modern x (tunuç>tunux, otoç>utux) — map before NFD strips it
    w = (w or "").replace("ç", "x").replace("Ç", "X")
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = w.lower().replace("'", "").replace("’", "").replace("ʼ", "").replace("-", "")
    return re.sub(r"[^a-z]", "", w)

def zh_clean(s):
    return ZH_RE.sub("", s or "")

# ---------------- corpus ----------------
def load_corpus():
    src = open(ENTRIES, encoding="utf-8").read()
    src = src[src.index("window.ENTRIES =") + len("window.ENTRIES ="):].strip().rstrip(";")
    entries = json.loads(src)
    tokens = collections.Counter()       # lowercase raw token -> display frequency
    glosses = collections.defaultdict(set)   # norm(form) -> zh gloss strings
    families = []                        # per entry: list of member tokens (hw+subs)
    def take(text):
        for t in TOKEN_RE.findall(text or ""):
            tokens[t.lower()] += 1
    for e in entries:
        take(e.get("hw")); take(e.get("crossRef")); take(e.get("paradigm"))
        for x in e.get("examples", []): take(x.get("t"))
        hz = zh_clean(e.get("zh", ""))
        if e.get("hw") and hz: glosses[norm(e["hw"])].add(hz)
        fam = [t.lower() for t in TOKEN_RE.findall(e.get("hw") or "")]
        # paradigm lines (° gmalax, malax...) are inflections of THIS root — family
        for t in TOKEN_RE.findall(e.get("paradigm") or ""):
            fam.append(t.lower())
        for s in e.get("subs", []):
            take(s.get("form")); take(s.get("paradigm"))
            for x in s.get("examples", []): take(x.get("t"))
            sz = zh_clean(s.get("zh", ""))
            if s.get("form") and sz: glosses[norm(s["form"])].add(sz)
            for t in TOKEN_RE.findall(s.get("form") or ""):
                fam.append(t.lower())
            for t in TOKEN_RE.findall(s.get("paradigm") or ""):
                fam.append(t.lower())
        if len(fam) > 1:
            families.append(fam)
    return tokens, glosses, families

# ---------------- omnibus ----------------
def load_omnibus():
    import openpyxl
    wb = openpyxl.load_workbook(OMNIBUS, read_only=True, data_only=True)
    word_gloss = collections.defaultdict(set)    # norm -> zh glosses
    word_raw = {}                                # norm -> canonical modern spelling
    for r in wb["Words"].iter_rows(min_row=2, values_only=True):
        w, zh = r[1], r[2]
        if not w: continue
        toks = [t for t in re.split(r"[^A-Za-z']+", str(w)) if t]
        for i, t in enumerate(toks):
            n = norm(t)
            if not n: continue
            if n not in word_raw or (i == 0 and len(toks) == 1):
                word_raw[n] = t.lower()
            if zh:
                word_gloss[n].add(zh_clean(str(zh)))
    sent_raw = collections.Counter()             # (norm, raw) counts
    for r in wb["Sentences"].iter_rows(min_row=2, values_only=True):
        if not r[1]: continue
        for t in re.split(r"[^A-Za-z']+", str(r[1])):
            n = norm(t)
            if len(n) >= 2:
                sent_raw[(n, t.lower())] += 1
    sent_best = {}
    for (n, raw), c in sorted(sent_raw.items(), key=lambda kv: -kv[1]):
        sent_best.setdefault(n, raw)
    return word_raw, word_gloss, sent_best

# ---------------- sister dialects ----------------
def load_sisters():
    """Toda + Tgdaya lexicons, norm -> zh glosses. Used ONLY to validate which
    generated candidate is the right shape — never as a source of spellings.
    Toda orthography is Truku-like: index as-is plus an o>u fold. Tgdaya
    differs by regular correspondences (l>r, o>u, seediq>seejiq d>j / t>c
    before i), so each Tgdaya word indexes under every combination of those
    folds; when a Pecoraro token yields e.g. both an l- and an r-candidate with
    the same sister gloss, they tie and the token stays unmapped (review)
    rather than guessing."""
    import openpyxl

    def tg_folds(n):
        outs = {n}
        for f in (lambda w: w.replace("l", "r"),
                  lambda w: w.replace("o", "u"),
                  lambda w: re.sub(r"d(?=i)", "j", w),
                  lambda w: re.sub(r"t(?=i)", "c", w)):
            outs |= {f(w) for w in outs}
        return outs

    def strips(v):
        """Also index affix-stripped cores (>=5 chars) so a differently-derived
        cognate (Pecoraro baxang ~ Tgdaya qbahang/mbahang) can still validate
        the shared stem. Gloss agreement remains the gatekeeper."""
        outs = {v}
        for k in (1, 2, 3):
            if len(v) - k >= 5:
                outs.add(v[k:])
        return outs

    toda_g = collections.defaultdict(set)
    tg_g = collections.defaultdict(set)
    wb = openpyxl.load_workbook(TODA, read_only=True, data_only=True)
    for r in wb.worksheets[0].iter_rows(min_row=1, values_only=True):
        if not r or not r[0]: continue
        z = zh_clean(str(r[1] or ""))
        if not z: continue
        for tk in re.split(r"[^A-Za-z']+", str(r[0])):
            n = norm(tk)
            if len(n) >= 2:
                for base in (n, n.replace("o", "u")):
                    for v in strips(base):
                        toda_g[v].add(z)
    wb = openpyxl.load_workbook(TGDAYA, read_only=True, data_only=True)
    for r in wb["Words"].iter_rows(min_row=2, values_only=True):
        w, z = r[1], r[5]
        if not w: continue
        z = zh_clean(str(z or ""))
        if not z: continue
        for tk in re.split(r"[^A-Za-z']+", str(w)):
            n = norm(tk)
            if len(n) >= 2:
                for base in tg_folds(n):
                    for v in strips(base):
                        tg_g[v].add(z)
    return toda_g, tg_g

# ---------------- candidates ----------------
def branch_xol(n):
    idx = [i for i, c in enumerate(n) if c in "xol"]
    if len(idx) > 8:
        idx = idx[:8]
    outs = set()
    for bits in itertools.product((0, 1), repeat=len(idx)):
        w = list(n)
        for b, i in zip(bits, idx):
            if b: w[i] = {"x": "h", "o": "u", "l": "r"}[n[i]]
        outs.add("".join(w))
    return outs

def contextual(w, short):
    """Safe transforms: regular Truku sound/spelling correspondences."""
    outs = {w}
    subs = [("e", "i"), ("ae", "ay"), ("ai", "ay"), ("ao", "aw"),
            ("ia", "iya"), ("ea", "iya"), ("ui", "uy"), ("ui", "uwi"), ("o", "u"),
            ("wi", "uy")]
    for a, b in subs:
        if w.endswith(a):
            outs.add(w[: -len(a)] + b)
    # palatalization before i is regular — allow even for short tokens (adi > aji)
    outs.add(re.sub(r"d(?=i)", "j", w))
    outs.add(re.sub(r"t(?=i)", "c", w))
    # Pecoraro ao/oa = modern aw/ow/uwa (daolas>dowras, boax>buwax)
    outs.add(w.replace("ao", "aw"))
    outs.add(w.replace("ao", "ow"))
    outs.add(w.replace("oa", "uwa"))
    if not short:
        outs.add(re.sub(r"(?<=[aeiou])u(?=[aei])", "w", w))
        outs.add(re.sub(r"i(?=[aou])", "iy", w))
        outs.add(re.sub(r"e", "i", w))
    return outs

def aggressive(w):
    """Riskier transforms — mapped only with gloss proof."""
    outs = set()
    # Pecoraro writes epenthetic vowels modern Truku drops: kensat>knsat, daxa>dha
    for i, c in enumerate(w[:-1]):
        if c in "eau" and 0 < i < len(w) - 1:
            outs.add(w[:i] + w[i + 1:])
    # q/k are inconsistent in Pecoraro (kmpax>qmpah, betak>bitaq) — single swaps
    for i, c in enumerate(w):
        if c == "k":
            outs.add(w[:i] + "q" + w[i + 1:])
        elif c == "q":
            outs.add(w[:i] + "k" + w[i + 1:])
    return outs

def candidates(n):
    """Return {candidate: is_aggressive}."""
    short = len(n) <= 3
    outs = {}
    # two rounds of safe transforms so chains compose (xedao>hedaw>hidaw)
    layer = set()
    for b in branch_xol(n):
        layer |= contextual(b, short)
    safe = set(layer)
    for w in list(layer):
        if len(safe) > 4000:
            break
        safe |= contextual(w, short)
    for c in safe:
        outs.setdefault(c, False)
    if not short:
        for base in list(safe):
            if len(outs) > 8000:
                break
            for c in aggressive(base):
                outs.setdefault(c, True)
    outs.pop(n, None)
    return outs

def gloss_overlap(pec_glosses, omni_glosses):
    """Qualified gloss agreement score; >=2 counts as confirmed.
    Evidence only counts if the whole omnibus gloss is contained in the Pecoraro
    gloss (or vice versa — handles one-char glosses like 日/狗), or the longest
    common substring is >=2 chars AND covers >=20% of the omnibus gloss — a bare
    2-char overlap inside a long unrelated definition is coincidence, not proof
    (raki 哄孩子睡覺… vs laqi 孩子)."""
    best = 0
    for pz in pec_glosses:
        for oz in omni_glosses:
            if not oz: continue
            if oz in pz or pz in oz:
                best = max(best, max(2, min(len(pz), len(oz))))
                continue
            sm = difflib.SequenceMatcher(None, pz, oz, autojunk=False)
            m = sm.find_longest_match(0, len(pz), 0, len(oz))
            if m.size >= 2 and m.size / len(oz) >= 0.2 and m.size > best:
                best = m.size
    return best

def main():
    tokens, glosses, families = load_corpus()
    word_raw, word_gloss, sent_best = load_omnibus()
    words_set = set(word_raw)
    attested = words_set | set(sent_best)
    toda_g, tg_g = load_sisters()

    SUFFIXES = ("anay", "ani", "an", "un", "ay", "aw", "i")
    def sister_ev(c):
        """Sister-dialect glosses supporting candidate c — direct, or via the
        candidate's affix-stripped core (>=5 chars) against the stripped index."""
        gs = set(toda_g.get(c, ())) | set(tg_g.get(c, ()))
        for k in (1, 2, 3):
            if len(c) - k >= 5:
                v = c[k:]
                gs |= toda_g.get(v, set()) | tg_g.get(v, set())
        for sfx in SUFFIXES:
            if c.endswith(sfx) and len(c) - len(sfx) >= 5:
                v = c[: -len(sfx)]
                gs |= toda_g.get(v, set()) | tg_g.get(v, set())
                break
        return gs

    # measured correspondence odds (residual-pair counts): o>u and x>h are
    # near-universal (keeping them is the surprise), l usually STAYS l (382 keep
    # vs 70 change) — used only to break ties among equally-glossed candidates
    CH_KEEP = {"o": 0.8, "x": 0.8, "e": 0.5}
    CH_SWAP = {("o", "u"): 0.2, ("x", "h"): 0.2, ("l", "r"): 0.8, ("e", "i"): 0.4}
    def wdist(n, c):
        sm = difflib.SequenceMatcher(None, n, c, autojunk=False)
        cost = 0.0
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                cost += sum(CH_KEEP.get(ch, 0.0) for ch in n[i1:i2])
            elif op == "replace" and (i2 - i1) == (j2 - j1):
                cost += sum(CH_SWAP.get(p, 1.0) for p in zip(n[i1:i2], c[j1:j2]))
            else:
                cost += max(i2 - i1, j2 - j1)
        return cost

    def sister_pick(pool, pec_g, n):
        """pool: {candidate: sister gloss set}. Return the candidate whose
        sister-dialect gloss qualifies (gloss_overlap >= 2) and wins the field —
        gloss score first, then correspondence-weighted closeness to the
        Pecoraro shape n (fold aliases of one sister word would otherwise tie
        forever). A residual exact tie returns None."""
        if not pec_g:
            return None
        hits = []
        for c, gs in pool.items():
            if not gs:
                continue
            g = gloss_overlap(pec_g, gs)
            if g >= 2:
                hits.append((g, c))
        if not hits:
            return None
        hits.sort(key=lambda x: -x[0])
        top = [c for g, c in hits if g == hits[0][0]]
        if len(top) == 1:
            return top[0]
        top.sort(key=lambda c: wdist(n, c))
        return top[0] if wdist(n, top[0]) < wdist(n, top[1]) else None

    result = {}      # token -> record
    review = {}
    unmapped = []    # (token, freq, gloss) with no attested candidate
    tiers = collections.Counter()

    # hand-curated mappings (gloss-verified by a human/LLM pass) win over generated
    manual_path = os.path.join(HERE, "manual_map.json")
    manual = json.load(open(manual_path, encoding="utf-8")) if os.path.exists(manual_path) else {}

    # tier L: per-case adjudication of the C-review queue (gloss-checked one by one)
    llm_path = os.path.join(HERE, "llm_map.json")
    llm = json.load(open(llm_path, encoding="utf-8")) if os.path.exists(llm_path) else {}
    llm = {k: v for k, v in llm.items() if not k.startswith("_")}

    for t in sorted(tokens):
        if t in OVERRIDE_KEYS or len(t) < 2:
            continue
        n = norm(t)
        if not n or len(n) < 2:
            continue
        pec_g = glosses.get(n, set())

        # 0. manual curation wins
        if t in manual:
            result[t] = {"modern": manual[t], "tier": "M"}
            tiers["M"] += 1
            continue

        # 0b. adjudicated review cases
        if t in llm:
            result[t] = {"modern": llm[t], "tier": "L"}
            tiers["L"] += 1
            continue

        # 1. identity
        if n in attested:
            disp = word_raw.get(n, sent_best.get(n, n))
            result[t] = {"modern": t if disp == n else disp, "tier": "id"}
            tiers["id"] += 1
            continue

        # 2-3. generate + filter
        cmap = candidates(n)
        cands = [(c, agg) for c, agg in cmap.items() if c in attested]
        if not cands:
            # no Truku attestation — triangulate via Toda/Tgdaya cognates.
            # Identity (keep the Pecoraro spelling) competes as a candidate too.
            pool = {c: sister_ev(c) for c in cmap}
            pool[n] = sister_ev(n)
            pick = sister_pick(pool, pec_g, n)
            if pick is not None:
                disp = word_raw.get(pick, sent_best.get(pick, pick))
                result[t] = {"modern": t if disp == n else disp, "tier": "T"}
                tiers["T"] += 1
            else:
                tiers["none"] += 1
                unmapped.append((t, tokens[t], sorted(pec_g)[:1]))
            continue

        # 4. score
        scored = []
        for c, agg in sorted(cands):
            in_words = c in words_set
            g = gloss_overlap(pec_g, word_gloss.get(c, set())) if in_words else 0
            dist = sum(1 for a, b in zip(n, c) if a != b) + abs(len(n) - len(c))
            scored.append({"cand": c, "words": in_words, "gloss": g, "dist": dist, "agg": agg})
        # safety outranks gloss unless the gloss evidence is decisive: an
        # aggressive candidate must beat every safe candidate by >=2 gloss points
        safe_best_gloss = max([s["gloss"] for s in scored if not s["agg"]], default=-1)
        def rank(s):
            decisive = s["agg"] and s["gloss"] >= 2 and s["gloss"] >= safe_best_gloss + 2
            return (-s["gloss"] if (not s["agg"] or decisive) else 0,
                    s["agg"] and not decisive, s["agg"], not s["words"], s["dist"])
        scored.sort(key=rank)
        best = scored[0]
        disp = word_raw.get(best["cand"], sent_best.get(best["cand"], best["cand"]))
        safe = [s for s in scored if not s["agg"]]

        # 5. tier — aggressive candidates need gloss proof
        if best["words"] and best["gloss"] >= 2 and (
            len(scored) == 1 or best["gloss"] > scored[1]["gloss"] or scored[1]["dist"] > best["dist"]
        ):
            result[t] = {"modern": disp, "tier": "A"}
            tiers["A"] += 1
        elif len(safe) == 1:
            c = safe[0]
            d2 = word_raw.get(c["cand"], sent_best.get(c["cand"], c["cand"]))
            result[t] = {"modern": d2, "tier": "B"}
            tiers["B"] += 1
        elif safe:
            # ambiguous among safe candidates: prefer the plain-rules output
            rules_out = re.sub(r"[xol]", lambda m: {"x": "h", "o": "u", "l": "r"}[m.group(0)], n)
            hit = next((s for s in safe if s["cand"] == rules_out), None)
            if hit is not None:
                d2 = word_raw.get(rules_out, sent_best.get(rules_out, rules_out))
                result[t] = {"modern": d2, "tier": "B"}
                tiers["B-rules"] += 1
            else:
                # ambiguous among safe candidates — let a sister-dialect cognate
                # gloss break the tie (conservative: safe candidates only)
                pool = {s["cand"]: sister_ev(s["cand"]) for s in safe}
                pick = sister_pick(pool, pec_g, n)
                if pick is not None:
                    d2 = word_raw.get(pick, sent_best.get(pick, pick))
                    result[t] = {"modern": d2, "tier": "T"}
                    tiers["T"] += 1
                else:
                    review[t] = {"freq": tokens[t], "pec_gloss": sorted(pec_g)[:2], "cands": scored[:5]}
                    tiers["C-review"] += 1
        else:
            # only aggressive candidates: a sister-dialect gloss match counts as
            # the required gloss proof
            pool = {s["cand"]: sister_ev(s["cand"]) for s in scored}
            pick = sister_pick(pool, pec_g, n)
            if pick is not None:
                d2 = word_raw.get(pick, sent_best.get(pick, pick))
                result[t] = {"modern": d2, "tier": "T"}
                tiers["T"] += 1
            else:
                review[t] = {"freq": tokens[t], "pec_gloss": sorted(pec_g)[:2], "cands": scored[:5]}
                tiers["C-review"] += 1

    # ---- pass 2: root-consistency projection (tier P) ----
    # A resolved family member (tiers id/M/A/B) fixes the Pecoraro->modern
    # correspondence for its stem; unresolved members of the same entry family
    # (hw + subs + paradigm forms — NOT example tokens, which mix in unrelated
    # words) inherit it: candidate = convert(prefix) + modern_stem + convert(
    # suffix), allowing an m/n-type infix after the stem's first consonant.
    # Affix conversion is limited to the near-universal correspondences
    # (o>u, x>h, final -ai/-ao/-e). Projected forms are mostly unattested by
    # definition — the point is inheriting a verified stem, and protecting
    # already-modern derivatives from the blanket character rules.
    AFFIX_END = [("ai", "ay"), ("ao", "aw"), ("e", "i")]
    def affix_convert(a, final):
        a = a.replace("o", "u").replace("x", "h")
        if final:
            for src, dst in AFFIX_END:
                if a.endswith(src):
                    a = a[: -len(src)] + dst
                    break
        return a

    INFIXES = ("mn", "um", "nm", "m", "n")
    proposals = collections.defaultdict(set)     # token -> candidate modern forms
    for fam in families:
        resolved = []
        for m in set(fam):
            rec = result.get(m)
            if not rec:
                continue
            sp = norm(m)
            if len(sp) >= 3:
                resolved.append((sp, rec["modern"].lower()))
        if not resolved:
            continue
        resolved.sort(key=lambda x: -len(x[0]))
        for t in set(fam):
            if t in result or t in OVERRIDE_KEYS or len(t) < 2:
                continue
            n = norm(t)
            if len(n) < 3:
                continue
            for sp, sm in resolved:
                hit = None                       # (start, matched_len, modern_core)
                i = n.find(sp)
                if i >= 0:
                    hit = (i, len(sp), sm)
                else:
                    for inf in INFIXES:
                        i = n.find(sp[0] + inf + sp[1:])
                        if i >= 0:
                            hit = (i, len(sp) + len(inf), sm[0] + inf + sm[1:])
                            break
                if hit is None:
                    continue
                i, L, core = hit
                pre, suf = n[:i], n[i + L:]
                if len(pre) > 5 or len(suf) > 4:
                    continue
                proposals[t].add(affix_convert(pre, False) + core + affix_convert(suf, True))
                break                            # longest matching stem wins per family
    proj_att = proj_ambig = 0
    for t, cs in sorted(proposals.items()):
        if t in result:
            continue
        if len(cs) != 1:
            proj_ambig += 1
            continue
        cand = next(iter(cs))
        if cand in attested:
            disp = word_raw.get(cand, sent_best.get(cand, cand))
            proj_att += 1
        else:
            disp = t if cand == norm(t) else cand
        result[t] = {"modern": disp, "tier": "P"}
        tiers["P"] += 1
    tiers["none"] -= tiers["P"]
    unmapped = [u for u in unmapped if u[0] not in result]

    # ---- pass 3: keep-l guard (tier KL) ----
    # The app fallback applies o>u, l>r, x>h blindly. l>r is the "expensive"
    # rule — l usually stays l in Truku — and it wrongly corrupts derived forms
    # of l-keeping roots whose inflected surface form isn't itself in the omnibus
    # (llukus>rrukus though root lukus stays lukus; l'alang>r'arang though alang
    # stays alang). A whole-token dictionary check can't catch these because only
    # the ROOT is attested. So: strip affixes/reduplication; if a stripped root's
    # keep-l form is attested in the Words sheet while its l>r form is not, freeze
    # the token to its keep-l spelling (o>u, x>h, l untouched) instead of char-ruling.
    KL_PREF = ("mn", "kn", "pn", "tn", "gn", "sm", "nk", "pk", "sk", "tk", "mk",
               "dm", "sn", "ps", "pg", "km", "gm", "tm", "p", "s", "t", "n", "k",
               "m", "g", "d", "b", "q", "l", "x")
    def keep_l(s):     # modernize but leave l alone (matches app fallback minus l>r)
        return s.replace("o", "u").replace("x", "h")
    def l_to_r(s):
        return s.replace("o", "u").replace("l", "r").replace("x", "h")
    def kl_cores(n):
        outs = set()
        for p in KL_PREF:
            if n.startswith(p) and len(n) - len(p) >= 4:
                outs.add(n[len(p):].lstrip("'"))
        if "'" in n:
            outs.add(n.split("'", 1)[1].lstrip("'"))
            outs.add(n.rsplit("'", 1)[1])
        if len(n) >= 2 and n[0] == n[1]:              # de-reduplicate llukus>lukus
            outs.add(n[1:])
        return {c for c in outs if len(c) >= 4}
    kl = 0
    for t in sorted(tokens):
        if t in result or t in OVERRIDE_KEYS or len(t) < 2:
            continue
        n = norm(t)
        if "l" not in n or l_to_r(n) == keep_l(n):     # no l that l>r would change
            continue
        for c in kl_cores(n):
            if keep_l(c) != l_to_r(c) and keep_l(c) in words_set and l_to_r(c) not in attested:
                result[t] = {"modern": keep_l(t), "tier": "KL"}
                tiers["KL"] += 1
                review.pop(t, None)
                kl += 1
                break
    tiers["none"] -= sum(1 for u in unmapped if u[0] in result)
    unmapped = [u for u in unmapped if u[0] not in result]

    unmapped.sort(key=lambda x: -x[1])
    json.dump({"map": result, "review": review, "unmapped_top": unmapped[:400]},
              open(os.path.join(HERE, "modern_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    lines = []
    for t, rec in sorted(result.items()):
        lines.append('"%s":"%s"' % (t, rec["modern"]))
    with open(os.path.join(BASE, "site", "modern_map.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "// Generated by tools/orthography/build_modern_map.py — do not edit by hand.\n"
            "// token (lowercase, Pecoraro spelling) -> modern Truku spelling, for the\n"
            "// display-only modern-spelling toggle. Tiers: identity-attested, gloss-\n"
            "// confirmed (A), unique-candidate (B), root-projected (P). Ambiguous cases stay unmapped and\n"
            "// fall through to the character rules. Regenerate after entries.js changes.\n"
            "window.MODERN_MAP = {\n" + ",\n".join(lines) + "\n};\n"
        )

    print("tokens considered:", len(tokens))
    print("tier counts:", dict(tiers))
    print("mapped:", len(result), " review:", len(review))
    print("projection: %d mapped (of which %d attested), %d ambiguous-skipped"
          % (tiers["P"], proj_att, proj_ambig))
    print("keep-l guard: %d tokens frozen to keep-l (would have been wrongly l>r'd)" % kl)
    changed = sum(1 for t, r in result.items() if r["modern"] != t)
    print("mapped with actual spelling change:", changed)

if __name__ == "__main__":
    main()
