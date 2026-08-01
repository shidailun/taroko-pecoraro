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

# Characters that carry no meaning on their own, so sharing one is not
# agreement. Without this, 的 and 是 confirm anything against anything.
STOP = set("的了是我你他她們個很不一有在要中上下大小人這那和與或也就都再又只之"
           "為所以及者其於由對從把被讓使做作用能會可時樣事物")

# Ruled out of scope by hand over batches 100–109. The tier logs cover names
# the digitization tagged, but a name reached only through an example sentence
# never got a tag — OTUN 秋（Otun）家 and TAOLAN 陶蘭 are in his sentences only.
HAND_NAMES = """sibal liwis mikat ingay lauken tatu talan banan lobyaq lubyaq
opic upih sikat imin timin tain pilin akit dloan lautan hidi eku tsay puti
stbaku mici dcristu tensu semento kodyo kaityo diko diku cristo yordan xelyo
xatso xaibyo tanso tenso tagahan murisaka mkmurisaka sitang efunang aman atwi
atuh denki banasi otun utun taolan taulan""".split()


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
        self.frozen = self._frozen(entries, mp)

    # ---- his Chinese, per token, from every field that reaches the screen ---
    def _his_glosses(self, entries):
        his = collections.defaultdict(set)

        def feed(txt, zh):
            if txt and zh:
                for m in TOK.finditer(txt):
                    his[wkey(m.group(0))].add(zh)

        for e in entries:
            zh = e.get("zh") or ""
            for f in ("hw", "paradigm", "crossRef"):
                feed(e.get(f), zh)
            for x in e.get("examples", []):
                feed(x.get("t"), x.get("zh") or zh)
            for sb in e.get("subs", []):
                szh = sb.get("zh") or zh
                feed(sb.get("form"), szh)
                feed(sb.get("paradigm"), szh)
                for x in sb.get("examples", []):
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
            for seg in HAN.findall(z):
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

    def regular(self, v):
        """(root, prefix, suffix, slot, the character the two glosses share),
        or None. Picks the analysis with the least affixation."""
        if v in self.frozen:
            return None
        his = set()
        for k in self.inv.get(v) or []:
            his |= self.his.get(k, set())
        best = None
        for c, p, sf, slot in self.roots(v):
            sh = self._agrees(his, c)
            if not sh:
                continue
            cost = len(p) + len(sf)
            if best is None or cost < best[0]:
                best = (cost, (c, p, sf, slot, sh))
        return best[1] if best else None
