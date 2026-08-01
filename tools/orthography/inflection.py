# -*- coding: utf-8 -*-
"""Is this unlisted value a regular inflection of a listed root?

The verified test used to be literal: a modern value counts only if that exact
string is one of the 40,760 types in attested_modern.json. That treats the
modern dictionary as if it listed every form of every word, and it does not —
it lists the forms someone happened to record. `qriban` is absent while its own
siblings `qribun` 剪成 and `qribi` 要剪下 are present; that is a LISTING gap, not
a lexical gap, and calling it unverified tells the reader the wrong thing.

So a value is also verified when it is an attested root wearing one of the
paradigm slots every Truku verb has:

  AF          m- prefix, or the -m- infix after the first consonant
  PF          -un
  LF          -an
  referential s-
  causative   p-
  preterite   n- prefix, or the -n- infix after the first consonant
  imperative  -i -ay -aw -ani -anay -aneyi

and the stacks those build (pn-, sn-, mn-, sp-, psn-, emp-). The suffixes -un
and -an swallow a root-final vowel, so that is allowed for as well.

Nothing else. Not kn-, not tm-, not two prefixes from outside the list — those
are derivation, and a derived word can mean something its root does not. The
doubled onset is excluded for the same reason even though it looks like the
obvious next class: batch 20 measured that mm-, pp-, tt- and ss- are live
modern PREFIXES, so a doubled initial is only sometimes a reduplication
(`ssapah` is "all the houses", not "a house"), and modern marks the human
plural with d- anyway (`dseejiq` 288×).

**Shape alone is not enough, and this is the whole reason the module reads
glosses.** His SISUN is SAIS 縫, to sew — and it decomposes perfectly as
`sisi`+`-un`, where `sisi` is 用來濾酒的工具, a rattan wine strainer. Same
letters, unrelated word, and calling the value verified would assert that an
invention is real modern Truku. So the root's modern gloss must agree with HIS
Chinese for the word: one shared two-character run, or one shared single
character that is not a structural particle. Agreement is deliberately loose —
his Chinese is a 1977 French dictionary rendered into Chinese and will not use
the modern dictionary's wording — but it kills the coincidences: `smisu` off
the pronoun `misu` 你, `ingay` and `banan` off glossless fragments.

Names and loans are excluded outright. A name has no modern dictionary entry to
be missing from, so "regular inflection of an attested root" is not a statement
anyone can make about one — `talan` is a man, and shape alone verified him as
`tali`+`-an` [靠]. Tiers N and J are frozen populations everywhere else in the
generator; this rule is no different.
"""
import collections, io, json, os, re

D = os.path.dirname(os.path.abspath(__file__))
H = os.path.normpath(os.path.join(D, "..", ".."))
TOK = re.compile(r"[A-Za-zÀ-ÿłŁʔ'’\"]+")
HAN = re.compile(r"[一-鿿]+")
NAMETAG = re.compile(r"name\s*\(|emprunt|\(J")
VOW = "aeiou"

PRE = ["", "m", "em", "n", "mn", "p", "pn", "s", "sn", "sp", "spn", "ps", "psn",
       "pp", "emp", "mnp", "snp", "np", "smn", "pm"]
SUF = ["", "un", "an", "i", "ay", "aw", "ani", "anay", "aneyi"]
# The suffixes that end in a vowel of their own — see vouched()'s fourth guard.
VSUF = ("i", "ay", "aw", "ani", "anay", "aneyi")

# Characters that carry no meaning on their own, so sharing one is not
# agreement. Without this, 的 and 是 confirm anything against anything.
#
# 子 is here for the same reason and it is not obvious: it is the noun
# classifier of 種子 seed, 果子 fruit, 釘子 nail, 日子 day, 梳子 comb, 李子 plum
# and 卵子 ovum, so on its own it confirms anything against anything too. It
# alone was holding up four claims — `snkmalu` and `spkmalu` decomposed onto
# `kalu` 梳子 when his word is `malu` 好, and `stmaqun` matched 刀子砍樹的聲音
# against his 把你的李子壓碎.
#
# 已 joined them in batch 114: it is the perfective marker and nothing else, so
# 已知道的 "already known" confirmed his （已完成的）攀登 "(completed) climbing"
# against `gnkla` 知道 to know, two words with no sense in common at all.
STOP = set("的了是我你他她們個很不一有在要中上下大小人這那和與或也就都再又只之"
           "為所以及者其於由對從把被讓使做作用能會可時樣事物子已")

# Both wordlists talk ABOUT words, and that metalanguage is not meaning: his
#「這會是 MIYAQ 的詞根嗎？」and the modern「為「empmiyak 要忙家務事」的詞根」share
# the run 的詞 and the character 根 while sharing no sense at all. These are
# EXCISED from a gloss before its characters are read, rather than subtracted
# from the result — dropping the bigram alone leaves a bare 根 behind, and
# putting 根 in STOP would take it away from 根源 and 樹根, where it is the
# whole meaning (it was holding up `snpusu` 根基 by itself).
BOILER = re.compile("的詞根|詞根|動詞形|動詞|名詞|同上|之詞|形式|參見|前項|衍生|詞形")

# Ruled out of scope by hand over batches 100–109. The tier logs cover names
# the digitization tagged, but a name reached only through an example sentence
# never got a tag — OTUN 秋（Otun）家 and TAOLAN 陶蘭 are in his sentences only.
HAND_NAMES = """sibal liwis mikat ingay lauken tatu talan banan lobyaq lubyaq
opic upih sikat imin timin tain pilin akit dloan lautan hidi eku tsay puti
stbaku mici dcristu tensu semento kodyo kaityo diko diku cristo yordan xelyo
xatso xaibyo tanso tenso tagahan murisaka mkmurisaka sitang efunang aman atwi
atuh denki banasi otun utun taolan taulan""".split()

# Read one by one out of vouched()'s whole output — 56 values, which is small
# enough to check by hand and too important not to. Two survived the gloss gate
# on a character that is doing no work:
#   tbuur   his 黃瓜 a cucumber, vouched by `emptbuur` 專找地瓜皮的人 — 地瓜 is a
#           sweet potato, and 瓜 alone is the same kind of classifier as 子.
#   tcingi  his 掉落－下降－出生, vouched by `tcingan` 打鐵店 — `tucing` carries
#           both 打 to strike and 掉落 to fall, and the blacksmith's shop says
#           nothing about the falling sense his entry is about.
HAND_NOT_VOUCHED = set("tbuur tcingi".split())

# vouched_root()'s whole output read the same way — 69 values, batch 114. Three
# are wrong and no gate reaches them, because the defect is in the ROOT, not in
# the gloss:
#   nnalu   his 好、良善（過去式）. The root `nalu` is a phantom: `nmalu` is the
#   empnalu preterite of `malu` 好 and `snalu` the perfective of `smalu` 做, two
#           different words that happen to strip to the same four letters, so
#           the two-supporter guard was satisfied by conflating them.
#   nilaq   his entry is the edible tree mushroom, and it agreed with `mnilaq`
#           起屑 to flake only on the 起 of 令人想起海藻 "recalls seaweed".
HAND_NOT_ROOTED = set("nnalu empnalu nilaq".split())

# sistered()'s whole output read the same way — batch 115. The rule reads no
# gloss at all, so the way it goes wrong is the homonym: his word is a
# different word that happens to wear the same letters as a slot of an
# attested paradigm.
#   qurun   his Q'QOL 挖鑿－雕刻 to gouge, sistered by `quri` 有關 and `quray`,
#   quran   which are the paradigm of a word about being ABOUT something. The
#           whole family was on the wrong stem — modern 開鑿;雕刻 is `gmqur`,
#           with a g — and batch 115 remaps it rather than verifying it.
HAND_NOT_SISTERED = set("qurun quran".split())


def _read(p):
    return io.open(p, encoding="utf-8").read()


def wkey(w):
    return w.lower().replace('"', "'").replace("’", "'")


class Inflection(object):
    def __init__(self, lex, mp):
        """lex: the attested type set. mp: MODERN_MAP, his key -> modern value."""
        self.lex = lex
        self.gl = json.load(io.open(os.path.join(D, "attested_gloss.json"),
                                    encoding="utf-8"))
        self.inv = collections.defaultdict(list)
        for k, v in mp.items():
            self.inv[v].append(k)
        s = _read(os.path.join(H, "site", "entries.js"))
        entries = json.loads(s[s.index("["):s.rindex("]") + 1])
        self.his = self._his_glosses(entries)
        self.slot = self._his_glosses(entries, slots_only=True)
        self.par = self._paradigm_tokens(entries)
        self.frozen = self._frozen(entries, mp)

    @staticmethod
    def _paradigm_tokens(entries):
        """Every token he printed in a ° paradigm line — the slots he himself
        declares are one word's inflections. sistered()'s gate."""
        out = set()
        for e in entries:
            for f in [e.get("paradigm")] + [sb.get("paradigm")
                                            for sb in e.get("subs", [])]:
                for m in TOK.finditer(f or ""):
                    out.add(wkey(m.group(0)))
        return out

    # ---- his Chinese, per token, from every field that reaches the screen ---
    def _his_glosses(self, entries, slots_only=False):
        """slots_only drops the example sentences, keeping only the Chinese he
        attached to a word AS a word — a headword, sub-form or paradigm gloss.

        A sentence gloss describes a whole clause and shares a character with
        almost anything, which is tolerable when the rest of the evidence chain
        is short and not when it is long: see vouched_root()."""
        his = collections.defaultdict(set)

        def feed(txt, zh):
            if txt and zh:
                for m in TOK.finditer(txt):
                    his[wkey(m.group(0))].add(zh)

        for e in entries:
            zh = e.get("zh") or ""
            for f in ("hw", "paradigm", "crossRef"):
                feed(e.get(f), zh)
            for x in ([] if slots_only else e.get("examples", [])):
                feed(x.get("t"), x.get("zh") or zh)
            for sb in e.get("subs", []):
                szh = sb.get("zh") or zh
                feed(sb.get("form"), szh)
                feed(sb.get("paradigm"), szh)
                for x in ([] if slots_only else sb.get("examples", [])):
                    feed(x.get("t"), x.get("zh") or szh)
        return his

    def _frozen(self, entries, mp):
        out = set(HAND_NAMES)
        for log in ("tier_n_log.txt", "tier_j_log.txt"):
            for ln in io.open(os.path.join(D, log), encoding="utf-8"):
                p = ln.split()
                if len(p) >= 2 and not ln.startswith("#"):
                    out.add(p[1])
        for e in entries:
            if not NAMETAG.search(e.get("tag") or ""):
                continue
            forms = [e.get("hw")] + [sb.get("form") for sb in e.get("subs", [])]
            for f in forms:
                for m in TOK.finditer(f or ""):
                    k = wkey(m.group(0))
                    if k in mp:
                        out.add(mp[k])
        return out

    # ---- gloss agreement ---------------------------------------------------
    @staticmethod
    def _chars(zhs):
        one, two = set(), set()
        for z in zhs:
            for run in HAN.findall(z):
                for seg in BOILER.split(run):
                    one |= set(seg) - STOP
                    two |= {seg[j:j + 2] for j in range(len(seg) - 1)}
        return one, two

    def _agrees(self, his_zhs, root):
        rg = self.gl.get(root)
        if not rg or not his_zhs:
            return None
        h1, h2 = self._chars(his_zhs)
        r1, r2 = self._chars(rg)
        if h2 & r2:
            return sorted(h2 & r2)[0]
        if h1 & r1:
            return sorted(h1 & r1)[0]
        return None

    # ---- the paradigm ------------------------------------------------------
    def roots(self, v):
        """(root, prefix, suffix, slot) for every attested root inflecting to v."""
        out = []
        for p in PRE:
            if not v.startswith(p):
                continue
            b0 = v[len(p):]
            if len(b0) < 3:
                continue
            stems = [(b0, False)]
            if len(b0) > 3 and b0[0] not in VOW and b0[1] in "mn":
                stems.append((b0[0] + b0[2:], True))       # the -m-/-n- infix
            for st, infixed in stems:
                for sf in SUF:
                    if sf and not st.endswith(sf):
                        continue
                    r = st[:len(st) - len(sf)] if sf else st
                    if len(r) < 3:
                        continue
                    cands = [r]
                    if sf in ("un", "an", "ani", "anay", "aneyi"):
                        cands += [r + c for c in VOW]      # the swallowed vowel
                    for c in cands:
                        if c in self.lex and c != v:
                            slot = "-".join(x for x in (
                                p, "infix" if infixed else "", sf) if x)
                            out.append((c, p, sf, slot or "bare"))
        return out

    def _his(self, v, slots_only=False):
        src = self.slot if slots_only else self.his
        out = set()
        for k in self.inv.get(v) or []:
            out |= src.get(k, set())
        return out

    def regular(self, v):
        """(root, prefix, suffix, slot, the character the two glosses share),
        or None. Picks the analysis with the least affixation."""
        if v in self.frozen:
            return None
        his = self._his(v)
        best = None
        for c, p, sf, slot in self.roots(v):
            sh = self._agrees(his, c)
            if not sh:
                continue
            cost = len(p) + len(sf)
            if best is None or cost < best[0]:
                best = (cost, (c, p, sf, slot, sh))
        return best[1] if best else None

    # ---- the inverse: a root nobody wrote down bare -------------------------
    def derived(self, v):
        """{attested word: (prefix, suffix, whether v's last vowel survived)}.

        Every attested word that is v wearing one paradigm affix, or a stack.
        The third field matters because the -un/-an branch drops v's own final
        vowel, so such a supporter witnesses the STEM and says nothing about the
        vowel the value ends in.
        """
        out = {}
        for p in PRE:
            for s in SUF:
                if not p and not s:
                    continue
                for w, whole in (
                        (p + v + s, True),
                        # the -m-/-n- infix goes inside a consonant-initial root
                        ((v[0] + p + v[1:] + s, True)
                         if p in ("m", "n") and v[:1] not in VOW else (None, 0)),
                        # -un/-an swallow the root's last vowel
                        ((p + v[:-1] + s, False)
                         if s and v[-1:] in VOW else (None, 0))):
                    if w and w in self.lex:
                        out.setdefault(w, (p, s, whole))
        return out

    def vouched(self, v):
        """(supporting word, the shared character), or None.

        regular() verifies a form by finding its ROOT in the wordlist. This is
        the mirror case, and `xal` is the clean one: the citation form is 0×
        — his own headword note says so, 從未見過此簡單形式 — while `pxal` 147×,
        `msxal`, `smxal`, `snxal`, `pnxal` and `sxali` are all there. A root
        that only ever surfaces affixed is a listing gap of the purest kind,
        and a paradigm around it is stronger evidence than one bare listing.

        Same three guards as regular(), for the same reasons. Two supporters
        wearing DIFFERENT affixes, because one is a substring coincidence
        waiting to happen; four characters minimum, because a three-letter
        string is inside everything; and the gloss must agree, which is what
        separates `nasu` — vouched on shape alone by the conjunction `nasi`
        如果 — from the real ones.

        The agreement may come from any ONE supporter. Most of a paradigm is
        glossless in the wordlist, so requiring all of them would be requiring
        the listing gap not to exist.

        A fourth guard, and it is the one this rule can go wrong without.
        Supporters reached by the -un/-an branch have dropped the value's own
        final vowel, so they witness the STEM and are silent about the vowel the
        value ends in. That vowel needs a witness of one kind or the other:

          either a supporter carries v WHOLE — `mkmpeysa` for `kmpeysa`,
          `qmnaya` for `qnaya`, `tmnbru` for `tnbru` — which is what licenses
          their swallowed supporters `kmpeysun` / `qnayun` / `tnbraw`, since a
          root ending in -a really does lose it before a suffix;

          or the final vowel is itself a paradigm suffix, and then the sister
          slots replacing it is the morphology rather than a coincidence:
          `paqi` beside `paqan` / `paqun` / `paqaw`, `ltudi` beside `ltudan`.
          An imperative can have no whole supporter — nothing affixes an
          imperative — so requiring one would throw away the clearest claims
          the rule makes.

        With neither, nothing attests the value's last letter and the paradigm
        on offer is as likely to belong to another word: `biyu` was vouched by
        `biyaw` 109×, `sbiyaw` 281×, `nbiyaw` 快速樣子 and `pbiyi`, which are
        the paradigm of `biyaw` 快 — the word his sentence actually uses
        (你的傷口很快就會痊癒), and now what the map says for `biyo`.
        """
        if v in self.frozen or v in HAND_NOT_VOUCHED or len(v) < 4 or v in self.lex:
            return None
        d = self.derived(v)
        if len(set(d.values())) < 2:
            return None
        if not v.endswith(VSUF) and not any(w[2] for w in d.values()):
            return None
        his = self._his(v)
        for w in sorted(d, key=lambda w: (len(w), w)):
            sh = self._agrees(his, w)
            if sh:
                return (w, sh)
        return None

    # ---- the two composed: a regular slot of a root nobody wrote down bare --
    def vouched_root(self, v):
        """(root, prefix, suffix, supporter, shared char) or None.

        regular() over a root that vouched() would accept rather than one the
        wordlist lists. `pspuhun` is the shape: `spuh` is never listed bare, but
        `spuhun`, `spuhan`, `spuhi`, `snpuhan`, `pspuhan` 醫院 and `pnspuhan`
        被治療過 are, and his gloss for the value is 使人施行醫治 — the -un
        sister of a slot the wordlist does list, off a root it does not. `natas`
        (n- on `atas`, which batch 113 vouched through `matas` 寫字) and
        `prijil` (p- on `rijil`, through `mrijil` 使彎曲) are the same.

        The evidence chain is one step longer than either rule alone: neither
        the value nor its root is listed, and the gloss agreement has to be
        taken against a SUPPORTER, because an unlisted root has no gloss of its
        own to agree with. So the gate is tighter at the other end — his Chinese
        must be a gloss he attached to the word AS a word, never one belonging
        to an example sentence. A sentence gloss describes a whole clause and
        shares a character with almost anything: it is what let `sktama`
        已故的父親 agree with `kmtama` 信奉上帝 on the 信 of an unrelated
        sentence, when the real morphology is `sk-` 'the late' on `tama` 父.

        The root is held to vouched()'s guards 1, 2 and 4 and to its four-letter
        floor, which is what keeps `snaah` out — the case that prompted the rule
        and does not survive it, since `naah` reaches only `pnaah`.
        """
        if v in self.frozen or v in HAND_NOT_ROOTED:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for p in PRE:
            if not p or not v.startswith(p):
                continue
            b0 = v[len(p):]
            if len(b0) < 4:
                continue
            stems = [b0]
            if len(b0) > 4 and b0[0] not in VOW and b0[1] in "mn":
                stems.append(b0[0] + b0[2:])
            for st in stems:
                for sf in SUF:
                    if sf and not st.endswith(sf):
                        continue
                    c = st[:len(st) - len(sf)] if sf else st
                    if len(c) < 4 or c in self.lex or c in self.frozen or c == v:
                        continue
                    d = self.derived(c)
                    if len(set(d.values())) < 2:
                        continue
                    if not c.endswith(VSUF) and not any(w[2] for w in d.values()):
                        continue
                    for w in sorted(d, key=lambda w: (len(w), w)):
                        sh = self._agrees(his, w)
                        if sh:
                            cost = len(p) + len(sf)
                            if best is None or cost < best[0]:
                                best = (cost, (c, p, sf, w, sh))
                            break
        return best[1] if best else None

    # ---- the sister slots: a paradigm the wordlist writes with other suffixes
    def sistered(self, v):
        """(prefix, stem, suffix, [the sisters]) or None.

        `lmuan` is the case, and it is the one shape the four rules above
        cannot state. It is the -an slot of his LAMU 收集 paradigm — his own
        line reads °Lmamu, lamu, lmui, lmuan, lmuon — and the wordlist lists
        `lmui` and `lmuun`, the -i and -un slots of that same stem, but not it.
        regular() reaches it, because `lmu` IS listed, and then refuses on the
        gloss: the listed `lmu` is 碎粒 a crumb, a homonym, and the two sisters
        that would settle it carry no gloss at all. Most of a paradigm is
        glossless, so that is not an accident of this word — it is the normal
        state of the evidence.

        The claim here is about morphology and not about meaning: a stem the
        wordlist writes with two different paradigm suffixes takes the third.
        Two supporters wearing DIFFERENT suffixes under the SAME prefix,
        because one is a substring coincidence waiting to happen.

        No gloss gate — there is usually no gloss to read — so the guard is at
        the other end, and it is his: **the value must be a word he printed in
        a ° paradigm line**. That is his own statement that it is an
        inflectional slot rather than a word in its own right, and it is what
        keeps the nouns out. `sapi` 小鋤頭, a small hoe, decomposes as
        `sap`+`-i` beside the attested `sapan` and `sapaw` 舖床 — a hoe
        verified as the imperative of spreading a bed. His SAPE is a headword
        and appears in nobody's paradigm, so the gate refuses it; so are
        `ptasaw` (his 使沉澱澄清, against the paradigm of `ptas` 寫;紋面) and
        `srciqun`.

        The gate is not sufficient by itself — a slot of his can still be a
        homonym of a slot of theirs, which is what HAND_NOT_SISTERED is for —
        but 11 of the 49 shapes this rule finds are refused by it outright, and
        every one of the 11 is either a noun or a different root.
        """
        if v in self.frozen or v in HAND_NOT_SISTERED or v in self.lex:
            return None
        if not any(k in self.par for k in (self.inv.get(v) or [])):
            return None
        best = None
        for p in PRE:
            if not v.startswith(p):
                continue
            b = v[len(p):]
            for sf in SUF:
                if not sf or not b.endswith(sf) or len(b) - len(sf) < 3:
                    continue
                st = b[:len(b) - len(sf)]
                sis = sorted(p + st + s2 for s2 in SUF
                             if s2 and s2 != sf and p + st + s2 in self.lex)
                if len(sis) < 2:
                    continue
                cost = len(p) + len(sf)
                if best is None or cost < best[0]:
                    best = (cost, (p, st, sf, sis))
        return best[1] if best else None
