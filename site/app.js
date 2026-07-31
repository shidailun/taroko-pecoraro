(function () {
  var LANGS = [
    { key: "fr", label: "Français" },
    { key: "en", label: "English" },
    { key: "zh", label: "中文" }
  ];
  var STORE_KEY = "taroko_pecoraro_langs_v1";

  var shown = loadLangs();

  function loadLangs() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && typeof parsed === "object") return parsed;
      }
    } catch (e) {}
    return { fr: true, en: true, zh: true };
  }

  function saveLangs() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(shown)); } catch (e) {}
  }

  // Modern-spelling toggle: display-only conversion of Pecoraro's 1977 orthography
  // to approximate modern Truku spelling. Rules are cross-checked against a modern
  // Truku dictionary (413 same-meaning word pairs found via Chinese-gloss matching,
  // then character-aligned) — only the strong, consistent patterns are applied;
  // i→y and q/k were excluded as inconsistent in the source data. Source data in
  // entries.js is never modified, only the rendered text.
  var SPELLING_KEY = "taroko_pecoraro_spelling_v1";
  var SPELLING_MAP = { x: "h", o: "u", l: "r", X: "H", O: "U", L: "R" };
  var spellingModern = loadSpelling();

  // Word-final "ui" cross-check (2026-07-19): checked every headword/sub-form in the
  // corpus ending in -ui against the modern Truku corpus, entry by entry — no blanket
  // rule, since the outcome depends on the root: some take -uwi, some -uy, some -uuy,
  // some (grammatical imperative-mood "-ui", e.g. GTUI = "gtui" in the modern corpus
  // too) don't change at all, and several forms have no confirmed modern counterpart
  // and are left as-is. See conversation log for the full per-root evidence.
  var WORD_OVERRIDES = {
    "klui": "kluwi", "mklui": "mkluwi", "nklui": "nkluwi", "tklui": "tkluwi",
    "sklui": "skluwi", "msklui": "mskluwi", "psklui": "pskluwi",
    "mnsklui": "mnskluwi", "snklui": "snkluwi", "mnklui": "mnkluwi",
    "kui": "kuwi",
    "mskui": "mskuy", "kskui": "kskuy",
    "ktui": "ktuy", "kmtui": "kmtuy", "mktui": "mktuy",
    "bkui": "bkuy", "bukui": "bkuy", "mukui": "mkuy", "mkui": "mkuy",
    "mkbukui": "mkbkuy",
    "bklui": "bkluy", "bq'lui": "bkluy",
    "tutui": "tutuy", "mtutui": "mtutuy",
    "dui": "duuy", "dmui": "dmuuy", "mdui": "mduuy", "mddui": "mdduuy",
    "pdui": "pduuy", "sdui": "sduuy", "mndui": "mnduuy",
    "xbui": "hbuy", "xmbui": "hmbuy", "pxbui": "phbuy", "xnbui": "hnbuy",
    // mpdui and m'xapui (mapui - mapwi) were dropped from this table on
    // 2026-07-31 so MODERN_MAP governs them, because both were wrong. "mpduuy"
    // is 0× against empduuy 3× 要握, and word-initial mp- before a labial is the
    // documented schwa class (emp- 50 types, mp- 0). "mapwi" is worse than
    // unattested — it is one of HIS OWN three spellings in the same sentence,
    // m'xapui (mapui - mapwi), so modern mode was printing Pecoraro at the user.
    // The sentence is "boil the fruits of this tree and they liquefy" (KSIA,
    // Mksia 液化), i.e. 煮 — mhapuy 124× 在煮.
    // His emphatic particle O (headword, 517 occurrences) is the modern topic
    // marker u — confirmed by the user 2026-07-28. The character rule already
    // produced "u"; this records that the spelling is verified, not guessed.
    "o": "u",
    // His one-letter affix cards, 2026-07-31. K, P, N, M, S, T, D and G head
    // prefix entries ("préfixe très productif…"), A heads a particle entry
    // (A sao bi iso 這都多虧了你) and I the note that it survives only in I TYEX.
    // The letter is cited in its own card and inside his morphological
    // parentheses — Psalu (P + SALU), ( N + DUP (DUK)), Skparo (S.+ K + PARO) —
    // and modern Truku writes every one of these prefixes with the same letter,
    // so each is an identity. build_modern_map.py drops keys shorter than two
    // characters, so manual_map.json cannot reach them; this table is the only
    // one that can. Identity here is not a no-op: it is the difference between
    // a checked spelling and a rule-guess, which is what the colour reports.
    // NOT included, deliberately: "l" and "r". Page R's only two book tokens
    // are the French root marker "(R)" and the l inside his French remark about
    // TBNAO ("le L étant escamoté ?") — his prose, not his Truku. And the
    // French "à" needs no exclusion, since wordKey() keeps the diacritic, so
    // the key "a" cannot reach it.
    "k": "k", "i": "i", "p": "p", "n": "n", "m": "m",
    "a": "a", "s": "s", "t": "t", "d": "d", "g": "g",
    // His TI is the modern ordinal/superlative prefix tg-, and he says so
    // himself on ST'MAQ: 「其他人在相同語境、相同意思下說 TGTMAQ 而非 TITMAQ」.
    // CLITIC_JOIN already carries nine of these pairs off his own text —
    // ti malu→tgmalu, ti bilaq→tgbilaq, ti t'lo→tgtru, ti spat→tgspat … — and
    // joinClitics() runs BEFORE this table is consulted, so those nine are
    // untouched; what is left is the three places a bare TI reaches the screen
    // (his TI headword card, his example TI Longat, and TYEX's sub Tityex).
    // It cannot live in manual_map.json: the generator drops any value with no
    // aeiou in it (the vowelless-output gate), and "tg" has none.
    "ti": "tg"
  };

  function loadSpelling() {
    try { return localStorage.getItem(SPELLING_KEY) === "modern"; } catch (e) { return false; }
  }

  function saveSpelling() {
    try { localStorage.setItem(SPELLING_KEY, spellingModern ? "modern" : "original"); } catch (e) {}
  }

  // Two characters of his carry no case, and both tests below used to read them
  // as though they did.
  //   His typewriter has no capital form of the diacritic vowels, so a word he
  // typed in capitals keeps a lowercase one inside it — NATSö against TANSÖ four
  // cards away. `sample === sample.toUpperCase()` fails for the first and passes
  // for the second, so one value printed NATSU and the other Natsu: 12 token
  // types / 18 spans, eleven of them already mapped and so already printing
  // Bnuwar, Qrut, Ilus, Iyus, Lbak, Srus, Shus, Tbuur, Hatsu, Hrus in the middle
  // of an all-capital headword row.
  //   His elision mark is the same problem at position 0, and much larger:
  // `"` equals its own uppercase, so `sample[0] === sample[0].toUpperCase()` is
  // true for every mark-initial word and the value came back capitalized. 16
  // types / 142 occurrences of his own lowercase text, led by "lu → Elug 83×
  // ("Suqi bi hrus ka Elug qmpahan ta"), "bi → Biyi 14× and "qan → Ekan 10×
  // ("Ini Ekan ka qrut mu").
  // So the case of a word is read off its CASED characters only, and a word
  // with none of them takes the value as written.
  var CASELESS = /[äëïöü'’ʼ"ʔ]/g;
  function matchCase(sample, target) {
    var cased = sample.replace(CASELESS, "");
    if (!cased) return target;
    if (cased === cased.toUpperCase()) return target.toUpperCase();
    if (cased[0] === cased[0].toUpperCase()) return target[0].toUpperCase() + target.slice(1);
    return target;
  }

  // modern_map.js (generated by tools/orthography/build_modern_map.py) maps
  // ~3000 corpus tokens to modern spellings cross-checked against the Truku
  // omnibus (identity-attested words like malu/do/lukus stay unchanged; the
  // rest are gloss-confirmed or unique attested candidates). Tokens not in the
  // map fall through to the character rules.
  var MODERN_MAP = window.MODERN_MAP || {};
  var LEXICAL_SUBS = window.LEXICAL_SUBS || {};

  // Pecoraro types two elision marks, ' and ", and both sit inside a word:
  // page 47 has BL'NGA and B"LO four lines apart, and Tmb"lo / knta"to / pn"lu
  // keep the double mark right through a paradigm. So " is a word character
  // everywhere, and folds to ' for every lookup — a tokenizer that breaks on it
  // turns one word into two fragments and judges each of them separately.
  // ł (Małi, małan, małun) is a barred l he uses to keep those forms apart from
  // MAI, and ʔ is a glottal stop — a third spelling of the elision mark. Both sit
  // outside À-ÿ, so a token class that stops at ÿ cuts małi into "ma" + "i" and
  // judges the halves separately. Fold ł to l and ʔ to ' for every lookup.
  var TRUKU_TOKEN = /([A-Za-zÀ-ÿłŁʔ'’ʼ"]+)/;
  var TRUKU_TOKEN_G = /[A-Za-zÀ-ÿłŁʔ'’ʼ"]+/g;
  var TRUKU_LETTER = /[A-Za-zÀ-ÿłŁ]/;

  function wordKey(word) {
    return (word || "").toLowerCase().replace(/[’ʼ"ʔ]/g, "'").replace(/ł/g, "l");
  }

  // The modern alphabet, for words: letters and the elision mark, nothing else.
  var PLAIN_WORD = /^[A-Za-z']+$/;

  function modernize(word) {
    if (!word) return word;
    var key = wordKey(word);
    // Already modern — the proclitic join built it. See CLITIC_JOIN.
    if (Object.prototype.hasOwnProperty.call(CLITIC_FORMS, key)) return word;
    if (Object.prototype.hasOwnProperty.call(WORD_OVERRIDES, key)) {
      return matchCase(word, WORD_OVERRIDES[key]);
    }
    if (Object.prototype.hasOwnProperty.call(MODERN_MAP, key)) {
      var target = MODERN_MAP[key];
      // target === key means "modern spelling = his spelling", so his own
      // capitals and apostrophes are kept rather than rebuilt from the key.
      // That only holds if he wrote it in the modern alphabet: wordKey folds
      // ł to l, so Małi keys to mali and maps to mali, and handing back the
      // word untouched put a barred l on screen in modern spelling.
      return target === key && PLAIN_WORD.test(word) ? word : matchCase(word, target);
    }
    return charRules(word);
  }

  // The character-rule fallback, for words the map doesn't cover.
  //
  // Pecoraro's ç is modern x (tunuç → tunux), so it is parked before the rules
  // run and restored after — otherwise the x it becomes would be swept on to h.
  // Every other diacritic he uses marks a vowel quality modern Truku simply does
  // not write, and the map agrees wherever it has an opinion: lämil → ramil,
  // diyán → jiyan, kúxeng → quhing, isò → isu, kmtöting → kmtucing, mpq'löt →
  // mpkrut. So they are dropped, and ö/ò fall to u through the ordinary o rule.
  // Without this an unmapped word kept its diaeresis and put a letter on screen
  // that is not in the alphabet — "Tensö" in modern spelling.
  function charRules(word) {
    var out = word.replace(/ç/g, "\u0001").replace(/Ç/g, "\u0002");
    // NFD only splits marks off letters that HAVE a decomposition; ł is a
    // barred l in its own right and ʔ a letter, so both survive the strip and
    // reach the screen. Fold them to l and ' — l then takes the ordinary l rule.
    out = out.replace(/ł/g, "l").replace(/Ł/g, "L");
    // Both his elision marks go, rather than folding to '. He writes ' and "
    // where he heard a schwa; modern Truku writes nothing there — that is why it
    // spells dxgal, mkla, tmlung. One token in the 39,889 of the three modern
    // corpora contains an apostrophe, and it is a typo. So wa"lo is modern waru,
    // not WA"RU, and the generator strips the same marks from every tier's output
    // for the mapped words.
    out = out.replace(/['’ʼ"ʔ]/g, "");
    out = out.normalize("NFD").replace(/[̀-ͯ]/g, "");
    // Word-final -ao is -aw, not -au. Measured: of the 280 mapped keys ending in
    // -ao, 267 have a value ending -aw, and the modern corpora hold 2,407 types
    // ending -aw against 4 ending -au (two of which also occur spelled -aw). So
    // the o>u rule below, which is right everywhere else, is wrong in exactly
    // this slot and prints a shape the orthography does not use word-finally.
    // Must run BEFORE the SPELLING_MAP replace, or the o is already gone.
    out = out.replace(/([aA])([oO])$/, function (m, a, o) {
      return a + (o === "O" ? "W" : "w");
    });
    out = out.replace(/[xolXOL]/g, function (c) { return SPELLING_MAP[c]; });
    return out.replace(/\u0001/g, "x").replace(/\u0002/g, "X");
  }

  function dispTruku(word) {
    return spellingModern ? modernize(word) : word;
  }

  // ---------- proclitics ----------
  // Modern Truku writes a few unstressed particles joined to the word they lean
  // on; Pecoraro spaces them. That is word DIVISION, not spelling, so nothing
  // keyed on single tokens can reach it — modernize() sees one word at a time and
  // never its neighbour, and mapping ti→tg alone would put "tg malu" on screen,
  // which is not modern Truku either. So the join runs on the text, before it is
  // cut into words, and only where the joined form is a word someone attests.
  //
  // A closed hand-checked list, not a productive rule. His Ti is the modern tg-
  // prefix and joins to almost anything, but his Ti longat and Ti tyex would give
  // tgrngat and tgcih, which neither corpus has, so those two stay as he set them.
  // Counts are occurrences in the book; each target is checked against
  // spoken_truku.json and truku_dict.json. He half-saw this himself — he brackets
  // his own "Ti malu" as "(TIMALU (?))".
  var CLITIC_JOIN = {
    "a sao": "asaw",          // 18  因著 spk 91 — "grâce à - par la faute de"
    "a tyex": "acih",         //  6  差一點 spk 8 — "s'en falloir de peu"
    "ti malu": "tgmalu",      //  3  那樣好的 spk 24
    "ti bilaq": "tgbilaq",    //  2  小的 spk 44
    "ti mangali": "tgmngari", //  2  spk 2
    "ti tmaq": "tgtmaq",      //  2  spk 9
    "ti t'lo": "tgtru",       //  2  第三 spk 25
    "ti basi": "tgbasi",      //  1  比較酸 spk 3
    "ti ima": "tgima",        //  1  spk 4
    "ti spat": "tgspat",      //  1  第四 spk 19
    "ti b'xgai": "tgbhgay"    //  1  比較白 — dictionary only, spk 0
  };

  // A joined form is already modern, so modernize() has to hand it back untouched
  // and respellable() has to own it. Without both, the word we just built would be
  // run through the character rules and then coloured green for not being in a map.
  var CLITIC_FORMS = {};
  Object.keys(CLITIC_JOIN).forEach(function (k) { CLITIC_FORMS[CLITIC_JOIN[k]] = 1; });

  // The leading group keeps the clitic from matching the tail of a longer word:
  // without it the "ti" of "smnati sao" would join. The table lookup is the real
  // gate — only "a" and "ti" have keys, so the other two-letter words he writes
  // constantly (ka, ni, so, mo, ko, da, bi, ta) never fire.
  var CLITIC_RE = /(^|[^A-Za-zÀ-ÿłŁʔ'’ʼ"])([A-Za-z]{1,2}) ([A-Za-zÀ-ÿłŁʔ'’ʼ"]+)/g;

  // matchCase can't do this one: the clitic is often a lone "A", and a single
  // capital letter reads as all-caps, so it would return ASAW for his "A sao".
  // The case of the pair as a whole is what decides.
  function clitiCase(cl, w, target) {
    var both = cl + w;
    if (both === both.toUpperCase()) return target.toUpperCase();
    if (cl[0] === cl[0].toUpperCase()) return target[0].toUpperCase() + target.slice(1);
    return target;
  }

  function joinClitics(s) {
    return s.replace(CLITIC_RE, function (all, pre, cl, w) {
      var j = CLITIC_JOIN[wordKey(cl) + " " + wordKey(w)];
      return j ? pre + clitiCase(cl, w, j) : all;
    });
  }

  // Word-wise modernization of a whole string. Same token split as linkifyTruku
  // (apostrophes are part of a token: bq'lui, m'xapui), so the result is exactly
  // what the modern-spelling toggle puts on screen — which is the point: the
  // search index has to contain whatever the reader can see.
  function modernizeText(s) {
    if (!s) return "";
    // The join is first, and unconditional: this function builds the modern key
    // set as well as modern display text, so joining here is what makes tgmalu
    // findable in search and files "A sao" under A-s-a-w in the letter listing.
    return joinClitics(s).replace(TRUKU_TOKEN_G, function (w) { return modernize(w); });
  }

  // Display form of a whole string (headword, sub-form): multi-word forms like
  // "A sao" need the token-wise pass, not a single map lookup on the whole string.
  function dispText(s) {
    return spellingModern ? modernizeText(s) : (s || "");
  }

  // ---------- search ----------
  function norm(s) {
    return (s || "")
      .toLowerCase()
      .replace(/[’ʼ"ʔ]/g, "'")
      .replace(/ł/g, "l")
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  // Pecoraro often writes a word twice, the second spelling in brackets:
  // "Pklilu (Plilu ?)", "L'NGLONG (LNGLONG)", "Mpsnabao (=Mpslnabao)". Both halves
  // are real spellings — either can be what a reader types and what his own example
  // sentences use — but the key was the whole string, so neither half matched
  // anything. Returns the spellings as written; callers norm() what they need.
  function variants(raw) {
    var out = [];
    (raw || "").split(/[()=?]/).forEach(function (p) {
      var v = p.trim();
      if (v && /[A-Za-zÀ-ÿ]/.test(v) && out.indexOf(v) === -1) out.push(v);
    });
    return out;
  }

  // The A–Z index wants a stricter test than variants(). Splitting on ()=? and
  // keeping every piece with a letter in it files his French apparatus as
  // headwords: "Xndilan (R. = XDIL ? - vl. = contraction de SXNDILAN ?)" puts
  // "contraction de SXNDILAN" under C and "R." under R — letter C had three cards
  // and two were that. But rejecting junk is only half of it, because ~30 of those
  // pieces have a REAL form inside an apparatus phrase, filed under the apparatus
  // word's letter instead of its own: "R. DUI" is DUI under R, "vl. Ldludan" is
  // Ldludan under V. So split further on the separators he uses inside a bracket,
  // strip the words that INTRODUCE a citation, and keep what survives as a word.
  // A piece may hold one space — "Ti tmaq", "TA NA" are his clitic forms, not prose.
  var AL_SPLIT = /[()=?,;:!]|\s-\s|\s-(?=[A-Z])/;
  var AL_LEAD = /^(?:(?:de|du|des|la|le|les|pour|par|var|vl|vr|cf|nb|sy|syn|r|meme|même|est-ce|et|ou|souvent|entendu|contraction|parfois|aussi|abr)\b\s*[.:]?\s*)+/i;
  var AL_TRAIL = /\s+(?:et|ou|de|du|des|la|le|les)$/i;
  var AL_APPARATUS = /^(?:r|vl|vr|var|cf|nb|sy|syn|ant|lit|fig|note|id|pl|sg|ex)$/i;
  var AL_WORD = "A-Za-zÀ-ÿłŁʔ'’ʼ\"";
  var AL_FORM = new RegExp("^[" + AL_WORD + "]+(?: [" + AL_WORD + "]+)?$");
  // French that can survive the strip and must never earn a slot. Read off these
  // two fields, not guessed at — his apparatus vocabulary is small and closed.
  var AL_FRENCH = {};
  ("nique bouche vie suite rouge produit qui peau crane crâne scie relation image " +
   "terme sans doute pluriel travers tordu inconnue tres peu bonte bonté beaute " +
   "beauté hotte remarque probable serait avec derive dérivé variante une chinois " +
   "mots ces cette forme suivante uniquement connu dans sens faire venir passer " +
   "passe fermer suie reduit réduit probablement rougeur volant savoir connaissance " +
   "matin non page").split(" ").forEach(function (w) { AL_FRENCH[w] = true; });

  function indexVariants(raw) {
    var out = [];
    (raw || "").split(AL_SPLIT).forEach(function (p) {
      var v = (p || "").trim().replace(AL_LEAD, "").replace(AL_TRAIL, "")
        .replace(/^[\s.,:;\-!]+|[\s.,:;\-!]+$/g, "");
      if (!v || !AL_FORM.test(v)) return;
      var bare = v.replace(/[^A-Za-zÀ-ÿłŁ]/g, "");
      if (bare.length < 2 || AL_APPARATUS.test(bare) || AL_FRENCH[bare.toLowerCase()]) return;
      if (out.indexOf(v) === -1) out.push(v);
    });
    return out;
  }

  // Which piece is the primary depends on the filter, so addForm can no longer
  // take it positionally: filtering can drop piece 0 ("A tyex" beside its bracketed
  // "Atyex"), and a slice(1) then eats a real alias. Skip the head by identity
  // instead. Punctuation and his two elision marks fold — "PU !" and M'wa"la are
  // their own head, not a second row — but the space does not, since "A tyex" and
  // "Atyex" really are two spellings.
  function aliasSlot(s) {
    return norm(s).replace(/[^a-z' ]/g, "").replace(/\s+/g, " ").trim();
  }

  // In modern spelling his two tries at a word often converge: "L'NGLONG (LNGLONG)"
  // is LNGLUNG twice over, and a bracket around a word's own spelling is noise. So
  // the form is shown once — unless the spellings really do stay apart (Pklilu /
  // Plilu), where the bracket is still telling the reader something.
  function collapsed(raw) {
    var vs = variants(raw);
    if (vs.length < 2) return raw || "";
    var first = norm(modernizeText(vs[0]));
    for (var i = 1; i < vs.length; i++) {
      if (norm(modernizeText(vs[i])) !== first) return raw;
    }
    return vs[0];
  }

  // The same convergence, but inside a sentence. "Ya adi sako bsklun (bsqlun) walo
  // xo!" — the bracket is his own second try at the word, and in modern spelling
  // both halves are bsqrun, so the line printed "bsqrun (bsqrun)": a bracket
  // distinguishing a word from itself. 75 example sentences do this. The bracket
  // goes only when it holds a single word that lands on the same modern spelling
  // as the word in front of it; where the two really stay apart — mkudus
  // (mk'udus), Babao (baba), ki (=baki) — it is still telling the reader
  // something, and 228 of them do.
  // The trailing (?) is his, and it can sit either inside the bracket or beside
  // the word: "Spqaya (spkaya (?))", "poqan (p'oqan(?))". It qualifies the guess,
  // so when the guess turns out to be the same word it goes with the bracket.
  var INLINE_VARIANT =
    /([A-Za-zÀ-ÿłŁʔ'’ʼ"]+)\s*\(\s*=?\s*([A-Za-zÀ-ÿłŁʔ'’ʼ"]+)\s*\??\s*(?:\(\s*\??\s*\))?\s*\)/g;
  function collapseInline(s) {
    return s.replace(INLINE_VARIANT, function (all, first, inner) {
      return norm(modernize(first)) === norm(modernize(inner)) ? first : all;
    });
  }

  // A written form as it should stand on screen: collapsed in modern spelling, and
  // exactly as Pecoraro set it otherwise.
  function formText(raw) {
    return spellingModern ? collapsed(raw) : (raw || "");
  }

  // Headwords, sub-forms and ° paradigm lines are word lists, not sentences, so
  // they take the spacing fixes only. He types his brackets loosely — "Spadyaq
  // ( Sppadyaq )", "Knta'to ( Knt"to ?)" — and the query mark belongs to the word
  // it queries, not to the space before it. The .?. placeholder is left alone.
  function tidyForm(s) {
    if (!s) return "";
    return s.replace(/\s+/g, " ")
      .replace(/\(\s+/g, "(")
      .replace(/\s+([)\]?!,;.])/g, "$1")
      .replace(/([,;])(?=[^\s])/g, "$1 ")
      // The template writes its own ° in front of a paradigm line, and some of
      // his lines carry one too — "° °Qmada, qada, ...".
      .replace(/^(?:°\s*)+/, "")
      // "(vl.Tkliyan)" — his variant abbreviations run straight into the form.
      // Only these, by name: his circumfix notation K...AN must keep its dots.
      .replace(/\b(vl|vr|var|cf|nb)\.(?=[A-Za-zÀ-ÿ])/gi, "$1. ")
      // "(qdani)qdai" is two alternative forms and wants a space; "(k)tai" is ONE
      // word with an optional segment and must not be split. Length tells them
      // apart — a whole word in the bracket, not a lone consonant.
      .replace(/\(([^()]{3,})\)(?=[A-Za-zÀ-ÿ])/g, "($1) ")
      // The mirror of it, which this path never had: "Tbiun(tbiyun)" is the same
      // two-alternative-forms shape read from the other side. Same length guard,
      // and for the same reason — it also keeps "Smwayai(?)" together.
      .replace(/([A-Za-zÀ-ÿ0-9,])\(([^()]{3,})\)/g, "$1 ($2)")
      .trim();
  }

  function entryText(e) {
    var parts = [e.hw, e.fr, e.en, e.zh, e.paradigm || ""];
    (e.examples || []).forEach(function (x) { parts.push(x.t, x.fr, x.en, x.zh); });
    (e.subs || []).forEach(function (s) {
      parts.push(s.form, s.fr, s.en, s.zh, s.paradigm || "");
      (s.examples || []).forEach(function (x) { parts.push(x.t, x.fr, x.en, x.zh); });
    });
    return norm(parts.join("  "));
  }

  // Truku-only text, for the modern-spelling index. The glosses are left out on
  // purpose: modernize() falls back to character rules for tokens it doesn't know,
  // which would turn French "Palissade" into "Parissade" and invent matches.
  function trukuText(e) {
    var parts = [e.hw, e.paradigm || ""];
    (e.examples || []).forEach(function (x) { parts.push(x.t); });
    (e.subs || []).forEach(function (s) {
      parts.push(s.form, s.paradigm || "");
      (s.examples || []).forEach(function (x) { parts.push(x.t); });
    });
    return parts.join("  ");
  }

  // Every entry carries a second key set in modern spelling, so a query in either
  // orthography finds it. Kept null when modernization is a no-op for that string,
  // which is the common case (identity-attested words) — one less scan per query.
  function alt(originalNorm, raw) {
    var m = norm(modernizeText(raw));
    return m === originalNorm ? null : m;
  }

  // Every spelling one written form can be looked up by: as Pecoraro wrote it, each
  // of his bracketed variants, and the modern form of each. Deduped, and usually
  // just one string — the extra keys only appear where the two orthographies differ
  // or he offered a second spelling.
  function keySet(raw) {
    var out = [];
    function push(k) { if (k && out.indexOf(k) === -1) out.push(k); }
    push(norm(raw));
    push(norm(modernizeText(raw)));
    variants(raw).forEach(function (v) { push(norm(v)); push(norm(modernizeText(v))); });
    return out;
  }

  var INDEX = window.ENTRIES.map(function (e) {
    var forms = [];
    (e.subs || []).forEach(function (s) {
      if (s.form) forms = forms.concat(keySet(s.form));
    });
    return {
      entry: e,
      text: entryText(e),
      hws: keySet(e.hw),
      forms: forms,
      mtext: alt(norm(trukuText(e)), trukuText(e))
    };
  });

  // Exact keys are claimed first and aliases only fill the gaps, so a real headword
  // always beats another form's bracketed variant or a modern spelling that happens
  // to collide with it.
  var HW_LOOKUP = {};
  (function () {
    var aliases = [];
    function put(k, rec) { if (k && !HW_LOOKUP[k]) HW_LOOKUP[k] = rec; }
    function index(raw, rec) {
      put(norm(raw), rec);
      keySet(raw).forEach(function (k) { aliases.push([k, rec]); });
    }
    window.ENTRIES.forEach(function (e) {
      index(e.hw, { hw: e.hw, fr: e.fr, en: e.en, zh: e.zh });
      (e.subs || []).forEach(function (s) {
        if (s.form) index(s.form, { hw: s.form, fr: s.fr, en: s.en, zh: s.zh, parentHw: e.hw });
      });
    });
    aliases.forEach(function (a) { put(a[0], a[1]); });
  })();

  // ---------- flat form index ----------
  // Pecoraro organizes by root: derived forms live inside their root's entry as
  // `subs`, so a form like `kmpax` (under root `qpax`) had no alphabetical slot of
  // its own and was unreachable from the A–Z row. FORMS gives every headword AND
  // sub-form a position under its own initial. Root organization is kept as the
  // storage shape — this is a second index over it, not a flattening: in a letter
  // listing a root still renders as a full entry card, while a sub-form renders as
  // a one-line stub pointing back at its root (what a print dictionary would set
  // as a cross-reference at that alphabetical slot).
  // Each form carries both spellings: `key` as Pecoraro wrote it, `mkey` as the
  // modern toggle displays it. A form must sit under the initial it is shown
  // under, or pressing X in modern mode returns a screen of H-words.
  var FORMS = (function () {
    var out = [];
    var ei = 0;
    function add(raw, label, entry, sub, alias) {
      var key = norm(raw);
      // mkey is the modern *displayed* spelling, brackets already collapsed, so a
      // row sorts and files under the word the reader actually sees.
      var mkey = norm(modernizeText(collapsed(raw)));
      out.push({
        key: key, mkey: mkey === key ? null : mkey,
        // ei is the entry's position in window.ENTRIES. An A–Z row opens its entry
        // by that index, not by searching for its own label: the headwords S, M and
        // A are single letters, and re-searching them returned 1,685 cards.
        label: label, entry: entry, sub: sub, alias: !!alias, ei: ei
      });
    }
    // A bracketed variant earns its own slot, labelled with just that spelling:
    // Plilu belongs under P in its own right, not only buried inside the string
    // "Pklilu (Plilu ?)" filed under P-k.
    function addForm(raw, entry, sub) {
      add(raw, raw, entry, sub, false);
      var head = aliasSlot(variants(raw)[0] || raw);
      indexVariants(raw).forEach(function (v) {
        if (aliasSlot(v) !== head) add(v, v, entry, sub, true);
      });
    }
    window.ENTRIES.forEach(function (e, i) {
      ei = i;
      addForm(e.hw, e, null);
      (e.subs || []).forEach(function (s) { if (s.form) addForm(s.form, e, s); });
    });
    // LILU lists both "Plilu" and "Pklilu (Plilu ?)", so the bracket would set a
    // second Plilu row beside the real one. Drop an alias whose spelling the same
    // entry already fills; a collision with a *different* entry is real and stays.
    var taken = {};
    out.forEach(function (f) { if (!f.alias) taken[f.key + " " + f.entry.hw] = true; });
    return out.filter(function (f) { return !f.alias || !taken[f.key + " " + f.entry.hw]; });
  })();

  function formKey(f) {
    return spellingModern && f.mkey ? f.mkey : f.key;
  }

  function initial(f) {
    var c = formKey(f).charAt(0);
    return /[a-z]/.test(c) ? c.toUpperCase() : "#";
  }

  // Both orderings are built once; the toggle picks one. Sorting by the spelling
  // actually on screen is what makes a listing read alphabetically.
  function sortedBy(keyFn) {
    return FORMS.slice().sort(function (a, b) {
      var x = keyFn(a), y = keyFn(b);
      return x < y ? -1 : x > y ? 1 : 0;
    });
  }
  var FORMS_ORIG = sortedBy(function (f) { return f.key; });
  // Modern spelling can merge an alias into the form it varies from — L'NGLONG and
  // LNGLONG are one word today — and the letter would otherwise list it twice.
  // Only FORMS_MOD is filtered: in Pecoraro's own spelling they are two spellings
  // and both deserve their slot.
  var FORMS_MOD = (function () {
    var taken = {};
    function slot(f) { return (f.mkey || f.key) + " " + f.entry.hw; }
    FORMS.forEach(function (f) { if (!f.alias) taken[slot(f)] = true; });
    return sortedBy(function (f) { return f.mkey || f.key; })
      .filter(function (f) { return !f.alias || !taken[slot(f)]; });
  })();

  function activeForms() {
    return spellingModern ? FORMS_MOD : FORMS_ORIG;
  }

  // Recomputed rather than cached: the letters themselves change with the toggle
  // (Pecoraro has an X row, modern Truku does not).
  function currentAlphabet() {
    var seen = {}, letters = [], hasSymbol = false;
    FORMS.forEach(function (f) {
      var c = initial(f);
      if (c === "#") hasSymbol = true;
      else if (!seen[c]) { seen[c] = true; letters.push(c); }
    });
    letters.sort();
    if (hasSymbol) letters.push("#");
    return letters;
  }

  function filter(q) {
    q = norm(q.trim());
    if (!q) return window.ENTRIES;
    // Five tiers. The word itself outranks every word that merely begins with it —
    // typing `mu` must reach MO before M'KAI (MUKAI ?) — and a sub-form match used
    // to fall into `contains`, so a derived form ranked below every unrelated root
    // starting with the same letters.
    var isHw = [], isForm = [], starts = [], subStarts = [], contains = [];
    function prefixes(list) {
      return list.some(function (f) { return f.indexOf(q) === 0; });
    }
    function has(list) {
      return list.indexOf(q) !== -1;
    }
    INDEX.forEach(function (it) {
      if (has(it.hws)) isHw.push(it.entry);
      else if (has(it.forms)) isForm.push(it.entry);
      else if (prefixes(it.hws)) starts.push(it.entry);
      else if (prefixes(it.forms)) subStarts.push(it.entry);
      else if (it.text.indexOf(q) !== -1 || (it.mtext && it.mtext.indexOf(q) !== -1)) contains.push(it.entry);
    });
    return isHw.concat(isForm, starts, subStarts, contains);
  }

  // ---------- audio ----------
  // TTS clips (24 kHz mono MP3) hosted on Cloudflare R2. Each headword / sub-form /
  // example that has an `a` field plays R2_BASE + a + ".mp3".
  var R2_BASE = "https://pub-cfb8a502c24b46eab5705b01efb315c2.r2.dev/";
  // Clips are cached `immutable` for a year. The example audio was re-synthesized
  // with the native Truku voice (truku3 model + White Dog narrator), replacing the
  // old renditions under the SAME keys, so bump this to bust stale browser/edge copies.
  var AUDIO_VER = "v6";
  var audioEl = new Audio();
  var playingBtn = null;

  function stopAudio() {
    audioEl.pause();
    if (playingBtn) { playingBtn.classList.remove("playing"); playingBtn = null; }
  }

  function playClip(id, btn) {
    if (playingBtn === btn) { stopAudio(); return; }
    stopAudio();
    audioEl.src = R2_BASE + encodeURIComponent(id) + ".mp3?v=" + AUDIO_VER;
    playingBtn = btn;
    btn.classList.add("playing");
    audioEl.play().catch(function () { stopAudio(); });
  }
  audioEl.addEventListener("ended", stopAudio);
  audioEl.addEventListener("error", stopAudio);

  // The clips are a native reading of the MODERN spelling. Offering them beside
  // Pecoraro's 1977 orthography would put a pronunciation in his mouth that his
  // page does not spell, so in his mode there is simply no button to press.
  function audioBtn(id) {
    if (!id || !spellingModern) return "";
    return '<button class="audio-btn" data-audio="' + esc(id) +
      '" title="Play audio / 播放" aria-label="Play audio">🔊</button>';
  }

  // ---------- the spelling switch, scattered through the page ----------
  // √ (root), ° (form list) and § (example) already sit beside the very lines
  // whose spelling is in question, so they ARE the switch: tapping any of them
  // flips the whole page — and every search after it — between Pecoraro's
  // spelling and the modern one, with no trip back to Settings. Settings keeps
  // the same switch for anyone who looks for it there.
  function spellMark(sym, what, cls) {
    return '<button class="spell-toggle ' + (cls || "") + '" title="' + esc(what) +
      " · " + (spellingModern
        ? "modern spelling — tap for Pecoraro’s (1977) / 現代拼寫,點按切換為原文拼寫"
        : "Pecoraro’s spelling (1977) — tap for modern / 原文拼寫,點按切換為現代拼寫") +
      '" aria-label="Switch spelling / 切換拼寫法">' + sym + "</button>";
  }

  // ---------- render ----------
  // The double quote has to be escaped as well, because " is one of Pecoraro's
  // two elision marks and so appears inside words: SBU", "LU and T"TO are real
  // headwords, and each was closing its own data-ref="…" attribute early.
  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // ---------- typography ----------
  // Spacing, capitals and final stops are Pecoraro's typing habits, not his
  // linguistics: the same page has "ka iso ! T'mlong" and "ka isu, mkla", and 3,901
  // of his 5,437 example sentences simply stop without a period. Normalized at
  // display time, by the conventions of the language being set — entries.js keeps
  // the book's own text, exactly like the modern-spelling toggle.
  var NNBSP = " "; // French high punctuation: a space that can't wrap
  var CJK = "㐀-鿿豈-﫿々〆";
  var ABBR = /(?:^|[\s(])(n\.b|nb|n|e\.g|i\.e|cf|vr|vl|var|litt|fig|etc|no|st|mgr|dr|min|max|env|ca|approx|abbr|c\.à\.d|c-à-d)\.$/i;

  function tidyLatin(t, french) {
    t = t.replace(/\s+/g, " ").trim();
    if (!t) return t;
    // "? ... Take" becomes "? … Take", but "K...AN" is his circumfix notation, not
    // an ellipsis, so the dots have to be free-standing to count.
    t = t.replace(/(^|[\s.,;:!?])\.\.\.(?=\s|$)/g, "$1…");
    // He also writes an ellipsis with two dots ("=..Il me l'a accordé"); after a
    // word it is a stray second stop instead ("etc..", handled below).
    t = t.replace(/(^|[^A-Za-zÀ-ÿ.])\.\.(?!\.)/g, "$1…");
    // A matched pair of straight quotes is a real quotation ("matinalité",
    // "morning-ness") and takes the marks of the language. It has to be settled
    // here, before glossCites(), because what makes an unpaired " a Truku word
    // is precisely that it is NOT one of these. Both ends must sit at a word
    // boundary — his elision mark is glued to a letter on the inside (B"lo).
    //
    // Not enough on its own: the mark also OPENS a word ("QAN = ekan) and CLOSES
    // one (Ma"), and a line carrying both reads as a matched pair — `"qan n'xali !
    // Ma" so psola sadyaq!` was being set as “qan n'xali ! Ma”, which pulls the
    // mark off ekan and leaves a bare green qan. Only the lexicon separates the
    // two: a quoted French word is not a Truku word, so if either end is a form
    // the map knows, these are two elisions and not a quotation.
    t = t.replace(/(^|[^A-Za-zÀ-ÿ])"([^"]{1,60})"(?![A-Za-zÀ-ÿ])/g,
      function (all, pre, inner) {
        var open = /^[A-Za-zÀ-ÿłŁʔ'’ʼ"]+/.exec('"' + inner);
        var close = /[A-Za-zÀ-ÿłŁʔ'’ʼ"]+$/.exec(inner);
        if ((open && respellable(open[0])) ||
            (close && respellable(close[0] + '"'))) return all;
        return pre + (french ? "«" + inner + "»" : "“" + inner + "”");
      });
    t = t.replace(/\s+([,;:!?%.])/g, "$1");
    t = t.replace(/([A-Za-zÀ-ÿ])\.\.(?!\.)/g, "$1.");                  // "etc.." → "etc."
    t = t.replace(/\.([!?])/g, "$1");   // he sometimes types both ("ka … nami. !")
    t = t.replace(/([,;:])(?=[^\s\d)\]»"'’…])/g, "$1 ");
    // He also runs a stop straight into the next word — every case in the corpus
    // is one of his abbreviations ("(vl.uxai ko", "Vr.LALAE") or a missed space
    // after a bang ("Ya kiso!Plnglngun"). A letter is required on BOTH sides so
    // his circumfix notation K...AN, where the dots have no letter before them,
    // is left alone.
    t = t.replace(/([A-Za-zÀ-ÿ][.!])(?=[A-Za-zÀ-ÿ])/g, function (m, p, off, s) {
      // …except a dotted abbreviation, which is one word with stops inside it.
      // Splitting "i.e." into "i. e." also hid it from the ABBR guard below,
      // so the capital came back too: "(the “gorillas”, i. E. Bodyguards)".
      if (/(?:^|[\s(])[A-Za-zÀ-ÿ]\.$/.test(s.slice(0, off + 2)) &&
          /^[A-Za-zÀ-ÿ]\./.test(s.slice(off + 2))) return m;
      return p + " ";
    });
    // "...(pbl'xun)mo xkawas" — a bracket he closes without letting go.
    t = t.replace(/\)(?=[A-Za-zÀ-ÿ0-9])/g, ") ");
    t = t.replace(/\(\s+/g, "(").replace(/\s+\)/g, ")");
    // The length guard is for "fiancé(e)" and "relative(s)" — a bracketed suffix
    // belongs to its word. Two letters is a WORD, though: his particles ka, na, ta
    // get glued when the right margin runs out ("qlaqel(ka) xana", page 288), and
    // they are separate words. Letters only, so his query marks "(?)" and "(??)"
    // stay put — the mark belongs to the word it queries, as in tidyForm.
    t = t.replace(/([A-Za-zÀ-ÿ0-9,])\(([^()]{3,}|[A-Za-zÀ-ÿ]{2})\)/g, "$1 ($2)");
    t = t.replace(/\s*…\s*/g, " … ").replace(/\s+/g, " ").trim();
    t = t.replace(/… ([,;:.!?])/g, "…$1");
    t = t.replace(/\(\s+/g, "(").replace(/\s+\)/g, ")");   // again: the ellipsis pass re-spaces
    // French sets a space before high punctuation — after a word only, so his "(??)"
    // query marks don't get pried apart.
    if (french) {
      // Twice: the pass consumes the character it matched, so in "« Impedimenta »!"
      // the » is eaten spacing itself and the ! that follows is never reached.
      t = t.replace(/([A-Za-zÀ-ÿ0-9)\]»"'’])\s*([;:!?»])/g, "$1" + NNBSP + "$2");
      t = t.replace(/([A-Za-zÀ-ÿ0-9)\]»"'’])\s*([;:!?»])/g, "$1" + NNBSP + "$2");
      t = t.replace(/«\s*/g, "«" + NNBSP);
    }
    t = t.replace(/^([a-zà-ÿ])/, function (c) { return c.toUpperCase(); });
    // A new sentence takes a capital, unless the stop belongs to one of his
    // abbreviations (nb. / vr. / e.g.), which is mid-sentence.
    t = t.replace(/([.!?…])(\s+)([a-zà-ÿ])/g, function (m, p, sp, c, off, s) {
      if (p === "." && ABBR.test(s.slice(0, off + 1))) return m;
      return p + sp + c.toUpperCase();
    });
    t = t.replace(/[\s–—-]+$/, "");                                     // dangling dashes
    t = t.replace(/([!?])\s*\.(?=\s|$)/g, "$1");   // a stop after a query mark is his slip
    if (/[A-Za-zÀ-ÿ0-9'’]$/.test(t)) t += ".";
    return t;
  }

  function tidyZh(t) {
    t = t.replace(/\s+/g, " ").trim();
    if (!t) return t;
    var map = { ",": "，", ";": "；", ":": "：", "!": "！", "?": "？" };
    // A closing full-width bracket ends a Chinese clause as surely as a character
    // does, so the mark that follows it is full-width too — his 賭氣嗎）? .
    t = t.replace(new RegExp("([" + CJK + "）」』])\\s*([,;:!?])", "g"), function (m, c, p) { return c + map[p]; });
    t = t.replace(new RegExp("([" + CJK + "])\\s*\\.(?=\\s|$)", "g"), "$1。");
    // Brackets convert as a pair, judged by what is inside them, so a half-width
    // closer can't survive a full-width opener.
    var inner = new RegExp("[" + CJK + "]");
    t = t.replace(/\(([^()]*)\)/g, function (m, body) {
      return inner.test(body) ? "（" + body.trim() + "）" : m;
    });
    // …and once more now that the brackets are full-width, since the mark being
    // judged may be sitting right after one that only just converted.
    t = t.replace(/([）」』])\s*([,;:!?])/g, function (m, c, p) { return c + map[p]; });
    // A space only vanishes between two Chinese characters: a Latin word set inside
    // Chinese keeps the spaces around it (參見 QDALAN), which is the convention.
    t = t.replace(new RegExp("([" + CJK + "])\\s+(?=[" + CJK + "])", "g"), "$1");
    t = t.replace(/\s*([，、。；：！？）」』])\s*/g, "$1");
    t = t.replace(/([（「『])\s*/g, "$1");
    t = t.replace(/\.\s*\.\s*\./g, "……").replace(/\.\.(?!\.)/g, "…");
    t = t.replace(/(^|[^A-Za-zÀ-ÿ])"([^"]{1,60})"(?![A-Za-zÀ-ÿ])/g, "$1「$2」");
    t = t.replace(/([！？!?])\s*[。.](?![.。])/g, "$1");   // a stop after a query mark is his slip
    if (!/[。！？」』）)…]$/.test(t)) t += "。";
    return t;
  }

  function tidy(s, lang) {
    if (!s) return "";
    return lang === "zh" ? tidyZh(s) : tidyLatin(s, lang === "fr");
  }

  // A word in an example is linked when it resolves in either orthography. The
  // token side matters as much as the index side: Pecoraro's prose does not always
  // match his own headwords — the examples say `mu` where the entry is `MO` — and
  // the modern spelling is where the two converge.
  function lookupWord(w) {
    return HW_LOOKUP[norm(w)] || HW_LOOKUP[norm(modernize(w))] || null;
  }

  // Colour now says which orthography is on screen, not what is tappable: a word
  // we can respell in modern Truku is brown, and one we can't stays green even
  // inside a modern line, so the green words are exactly what is left to do.
  // "Can respell" means the curated map has the word — a character-rule guess
  // (o→u, l→r, x→h applied blind) is not a spelling anyone has vouched for.
  function respellable(word) {
    var key = wordKey(word);
    return Object.prototype.hasOwnProperty.call(WORD_OVERRIDES, key) ||
      Object.prototype.hasOwnProperty.call(MODERN_MAP, key) ||
      Object.prototype.hasOwnProperty.call(CLITIC_FORMS, key);
  }

  // Tier X: the modern entry is a different WORD, not a different spelling of
  // his word — Q'NAO "garlic" is simply gone and qusul carries the meaning now.
  // The toggle promises spelling, so a substitution has to declare itself:
  // modern mode prints QUSUL (Q'NAO), the substitute in the modern colour and
  // his own word beside it in his. Pecoraro mode is untouched — there is
  // nothing to disclose when his spelling is what's on screen.
  //
  // The bracket is a DISCLOSURE, so it is owed only where something was actually
  // substituted. Tier X also holds affix articles whose modern spelling is his own
  // (`kn`, `sn`, `tn`, `dd`, `gn`, `mk`, `sk`) — they live here rather than in
  // manual_map.json only because the generator's vowelless-output gate would drop
  // them, and for those the bracket printed "KN (KN)", telling the reader his word
  // is no longer used while showing it unchanged beside itself.
  function lexicalSub(word) {
    if (!Object.prototype.hasOwnProperty.call(LEXICAL_SUBS, wordKey(word))) {
      return false;
    }
    return wordKey(modernize(word)) !== wordKey(word);
  }

  // Pecoraro's own editorial hand, set inside his Truku lines. These are French
  // abbreviations, not Truku words: vr. = voir, vl. = vel (Latin "or"), var. =
  // variante, R. = racine. Left to the ordinary path they were tokenized as
  // words, coloured green as if they were 147 more things left to verify, and run
  // through the character rules — which turned "vl." into "vr.", an abbreviation
  // that means something else entirely.
  //
  // They are recognized by name, not by shape. A trailing period is no signal at
  // all: 519 dotted tokens in his Truku lines are ordinary words ending a sentence
  // or a ° list (taon., lmuon., psloon.), so anything general enough to catch vl.
  // would swallow those too. R. is the one that must also match case — a lone
  // capital R is his root mark, and there is no Truku word it could be.
  // His apparatus abbreviations — Latin and French shorthand a reader today has no
  // reason to know. `vl.` is *vel*, "or", and it is in the book 215 times (vr. 229,
  // var. 199, R. 632). Until now the only explanation was a hover `title` written in
  // French and English, which gave a Chinese reader nothing and a touch reader
  // nothing at all. Held one field per language so the tap bubble can follow the ⚙
  // toggle and the title string can be built from the same source.
  var META_ABBR = {
    vl: { full: "vel", fr: "ou", en: "or", zh: "或" },
    vr: { full: "voir", fr: "voir", en: "see", zh: "參見" },
    "var": { full: "variante", fr: "variante", en: "variant", zh: "變體" },
    r: { full: "racine", fr: "racine", en: "root", zh: "詞根" },
    sy: { full: "synonyme", fr: "synonyme", en: "synonym", zh: "同義詞" },
    nb: { full: "nota bene", fr: "à noter", en: "note", zh: "註" }
  };
  function metaAbbr(part, after) {
    if (after.charAt(0) !== ".") return null;
    // Only a CAPITAL R is his root mark; a lowercase "r." is French prose.
    if (part !== "R" && part.toLowerCase() === "r") return null;
    return Object.prototype.hasOwnProperty.call(META_ABBR, part.toLowerCase())
      ? META_ABBR[part.toLowerCase()] : null;
  }
  // The title attribute is the mouse fallback; the tap bubble is the real
  // explanation, since a phone never sees a title at all.
  function abbrTitle(a) {
    return a.full + " — " + a.fr + " / " + a.en + " / " + a.zh;
  }

  // Every Truku word is wrapped, whether or not it links, because the wrapper is
  // what carries its spelling status. noLink is for headwords, which are the
  // entry the reader is already on.
  function linkifyTruku(text, noLink, prose) {
    if (!text) return "";
    if (spellingModern) text = joinClitics(collapseInline(text));
    var parts = text.split(TRUKU_TOKEN);
    var h = "";
    for (var i = 0; i < parts.length; i++) {
      var part = parts[i];
      // A run of bare elision marks is punctuation, not a word to judge.
      if (i % 2 === 0 || !TRUKU_LETTER.test(part)) { h += esc(part); continue; }
      if (prose && Object.prototype.hasOwnProperty.call(prose, part.toLowerCase())) {
        h += '<span class="meta-abbr">' + esc(part) + "</span>";
        continue;
      }
      var meta = metaAbbr(part, parts[i + 1] || "");
      if (meta) {
        h += '<span class="meta-abbr" tabindex="0" data-abbr="' + esc(part.toLowerCase()) +
          '" title="' + esc(abbrTitle(meta)) + '">' + esc(part) + "</span>";
        continue;
      }
      var cls = respellable(part) ? "w-mod" : "w-raw";
      var linked = !noLink && lookupWord(part);
      if (linked) cls += " crossref-link";
      h += '<span class="' + cls + '"' + (linked ? ' data-ref="' + esc(part) + '"' : "") +
        ">" + esc(dispTruku(part)) + "</span>";
      if (spellingModern && lexicalSub(part)) {
        h += ' <span class="w-orig" title="Pecoraro’s word, no longer used">(' +
          esc(part) + ")</span>";
      }
    }
    return h;
  }

  // The root mark is rarely alone in the tag. "(R. = BKUI ?)", "( = R. ?)",
  // "(BQ'LI) (R)" are all root notes with his hedging wrapped round them, and only
  // the two bare forms were ever recognized — the other ~200 printed "R." into the
  // page as though it were a Truku word. Now anything holding a lone R gets the √,
  // and whatever else the tag holds goes through the Truku path: coloured, linked,
  // and collapsed when it is only his second spelling of the headword.
  var ROOT_MARK = /(^|[\s(=-])R\.?(?=$|[\s)?=.-])/;
  // He often marks the root twice in one tag — "( = R.? de KMPAUX ?) (R. = KPAUX ?)"
  // — so the strip has to be global, and the French "de" that links the mark to the
  // form it proposes goes with it: alone in a bracket it would be tokenized and
  // coloured as a Truku word, which it is not.
  var ROOT_MARK_G = /(^|[\s(=-])R\.?(?=$|[\s)?=.-])/g;
  var TAG_FRENCH = /(^|[\s(=-])d[eu](?=\s)/g;

  // About thirty of his root tags are not a form at all but a remark in French —
  // "(QALAO est plus probable)", "(Serait ce la R. de MIYAQ ?)", "(R. = UDA =
  // passer; MUDA = qui passe ?)". Every word in them was being tokenized as Truku,
  // coloured, and respelled. The tags are a closed set of 344 strings, so this is
  // the whole French vocabulary that occurs in them, read off the data; the Truku
  // forms standing beside it (QALAO, MIYAQ, Bsukan, Skleqe) keep the word treatment.
  var TAG_PROSE = {};
  ("de du des la le les ce cette et en un une avec sans dans sous tous plus peu " +
   "très doute pluriel travers tordu inconnue probable probablement parfois " +
   "relation scie souvent réduit à fermer suie passer qui passe uniquement connu " +
   "forme suivante dérivé dérivés précédent contraction faire venir manger " +
   "variante étant escamoté placés terme semble vraie chinois chinoise est " +
   "serait préfixe bébé peau entourer taroko").split(" ").forEach(function (w) {
    TAG_PROSE[w] = 1;
  });

  // His French does not stay in the tags. It gets into a sub-form's bracket —
  // "Pqaya (Est-ce de la R. QAYA ?)", "Pqboan (= contraction pour: PQBBOAN ?)" —
  // and four example lines under AN are not examples at all but French gloss
  // pairs, "Malu = Beau, bien; Knmlaan = beauté, bonté". Tokenized as Truku, the
  // char rules ran on French and printed it back as fake Truku: PRUDUIT,
  // CUNTRACTIUN, SAVUIR, CUNNAISSANCE. Six words were worse than mangled — the
  // curated map claimed them, so they came out BROWN, asserting a verified modern
  // spelling for a French word: ne→ni (which is his own word for "and"),
  // pour→puur, page→pagi, nique→niqi, non→nun, matin→macin.
  //
  // A separate set from TAG_PROSE, not a reuse of it, for two measured reasons:
  // UN is one of his headwords, so the French "un" that TAG_PROSE needs would
  // grey an entry; and vl./var. are already named by metaAbbr, which gives them
  // a tooltip the prose branch would take away. Everything here was read off the
  // form and example fields, and every occurrence of every one of these words in
  // them is French — 49 occurrences, no Truku word among them.
  // The list was read off the fields once and was not closed: four more were still
  // rendering as fake Truku, and the two the map had claimed came out BROWN —
  // "Rougeur" as RUUGEUR and "(=Volant)" as VULANT, both asserting a verified modern
  // Truku spelling for a French word. Read off the DOM, not off the map: a word here
  // is intercepted before respellable() is asked, so no map entry has to be deleted
  // for the page to be right, and the generated tiers would put it back anyway.
  var FORM_PROSE = {};
  ("de la le et est ce qui plus souvent parfois contraction même il ne pas non " +
   "pour suite page précédente rarement entendu faudrait vouloir nique porter " +
   "hotte beau bien beauté bonté savoir connaissance vivant vie matin " +
   "produit matinalité bouche rouge rougeur volant"
  ).split(" ").forEach(function (w) {
    FORM_PROSE[w] = 1;
  });
  // A bracket in a root tag is his second try at the word, and the whole-tag test
  // below only drops it when EVERY word in the tag is the headword again. Two
  // patterns slip past that and print a bracket distinguishing a word from itself:
  // he lists both his spellings in one bracket — "(TNG'I – T'NGI)", "(= BU? - = BU?)"
  // — which converge to one modern word, and he pairs a redundant bracket with an
  // informative one, "(QRHIQ?) (= RHIQ = Peau)", where only the first is noise.
  // variants() cannot see either: it splits on ()=? and not on his dash, so a
  // two-spelling bracket reaches it as a single string. So work bracket by bracket,
  // dedupe the segments that converge, and drop a bracket that has nothing left to
  // say. Measured over all 443 root-mark tags: 14 brackets, and modern mode only —
  // in his own spelling the two halves really are different words on the page.
  var TAG_SEG_DASH = /\s*[–—]\s*|\s+-\s+/;
  var TAG_SEG_TRIM = /^[\s=]+|[\s?]+$/g;
  var TAG_SEG_META = /\b(?:vr|vl|var|nb|sy)\.\s*/gi;
  function tagSegKey(seg) {
    var w = seg.replace(TAG_SEG_META, "").replace(TAG_SEG_TRIM, "");
    return /[A-Za-zÀ-ÿ]/.test(w) ? norm(modernizeText(w)) : "";
  }
  // how much a segment actually says: "= TGILA ?" and "Vr. TGILA" are the same
  // number of characters, but only one of them names a relationship
  function tagSegSize(seg) {
    return seg.replace(/[\s=?]/g, "").length;
  }
  function collapseTagBrackets(rest, hw) {
    var head = norm(modernizeText(variants(hw)[0] || hw));
    return rest.replace(/\(([^()]*)\)/g, function (whole, inner) {
      var segs = inner.split(TAG_SEG_DASH), keep = [], seen = [];
      for (var i = 0; i < segs.length; i++) {
        var k = tagSegKey(segs[i]), seg = segs[i].trim(), at = seen.indexOf(k);
        // no word in it, or the headword again
        if (!k || k === head) continue;
        // already listed: of two spellings of one modern word keep the fuller
        // line, so GILA's "(= TGILA? - Vr. TGILA)" still says variante
        if (at !== -1) {
          if (tagSegSize(seg) > tagSegSize(keep[at])) keep[at] = seg;
          continue;
        }
        seen.push(k);
        keep.push(seg);
      }
      return keep.length ? "(" + keep.join(" – ") + ")" : " ";
    });
  }

  function tagHtml(tag, hw) {
    if (!tag) return "";
    var root = spellMark("√", "Root / racine", "tag root-tag");
    if (tag === "(R)" || tag === "(R.)") return root;
    if (!ROOT_MARK.test(tag)) return '<span class="tag">' + esc(tag) + "</span>";
    var rest = tag.replace(/\(\s*R\.?\s*\)/g, " ").replace(ROOT_MARK_G, "$1").replace(TAG_FRENCH, "$1");
    // What survives once the mark is out is often only his uncertainty — "(= ??)",
    // "( = ? )" — which the √ already implies. Print the remainder only when there
    // is an actual word in it, and not when that word is the headword again.
    rest = rest.replace(/\(\s*[=?\s.-]*\)/g, " ").replace(/\s+/g, " ").trim();
    if (!TRUKU_LETTER.test(rest)) return root;
    if (spellingModern && hw) {
      var vs = variants(rest), same = vs.length > 0;
      for (var i = 0; i < vs.length; i++) {
        if (norm(modernizeText(vs[i])) !== norm(modernizeText(variants(hw)[0] || hw))) same = false;
      }
      if (same) return root;
      rest = collapseTagBrackets(rest, hw).replace(/\s+/g, " ").trim();
      if (!TRUKU_LETTER.test(rest)) return root;
    }
    return root + ' <span class="tag">' + linkifyTruku(tidyForm(rest), false, TAG_PROSE) + "</span>";
  }

  // A gloss is never run word-by-word through modernize() — the character rules
  // would turn French "Palissade" into "Parissade" — but his definitions are
  // full of Truku all the same: cross-references (See T"TO), and forms cited to
  // build up a sense (B"lo babwi = piglet). Those were left frozen in his
  // spelling inside an otherwise modern page.
  //
  // A token carrying his second elision mark " is the one part of a gloss that
  // can be claimed safely: no French, English or Chinese word has a word-
  // internal double quote, and tidy() has already converted the real quotations
  // to « » / “ ” / 「 」. That is 102 occurrences across the three languages,
  // 30 types, every one of them Truku, no false positives.
  //
  // The apostrophe cannot be recruited the same way (l'occasion, don't), and
  // "is it a headword?" is far worse — it claims a, I, on, do, un, ta, ma, si,
  // 10,819 occurrences of ordinary French and English prose. So the rule stops
  // at the double quote, deliberately.
  // ---------- names inside the glosses ----------
  // A name reaches this book in as many as four spellings. The Truku line prints
  // Pixan; his French renders it in French orthography as Pirhanne; the English
  // we translated from the French inherited that; and the Chinese invented a
  // character transliteration of its own, differently almost every time — Mikat
  // is 米卡特, 米卡茲 and 米查特 in three separate sentences, Sibal is 錫巴爾,
  // 希巴爾, 希巴 and 希霸, Liwis is 利維斯, 里維斯 and 利威斯. None of those can be
  // matched to the word standing in the Truku line above them, which is the one
  // thing an example sentence is for. One gloss manages to print both Iban and
  // Ibanne for the same man in the same sentence.
  //
  // So in OUR columns — English and Chinese — a Truku name is written the way his
  // Truku line writes it, and goes through linkifyTruku() like any other Truku
  // word: it follows the spelling toggle, takes the word colours, and links to
  // his entry (nearly all of these are headwords in his own names appendix, which
  // is where each target below comes from). The French column is untouched. That
  // one is his own text, and Pirhanne is what he printed.
  //
  // Biblical and Chinese names are deliberately absent from both tables: Cristo →
  // 基督, Yordan → 約旦, Maria → 馬利亞, Jes → 耶穌 are translations of a name, not
  // transliterations of a Truku word, and they stay as they are.
  //
  // His French conventions, for reading the left column: ou = u, rh = his x,
  // dj = his d before i, tch = his ti, ss = s, sh = his ç, tz/ts = t, ï = i,
  // final -nne = -n, final -oui = -wi.
  var GLOSS_NAMES = {
    "ibanne": "Iban", "djian": "Diyan", "djiro": "Diro", "perho": "Pexo",
    "pissao": "Pisao", "pirhanne": "Pixan", "tchirhong": "Tixong",
    "rhidé": "Xide", "micatz": "Mikat", "mikatz": "Mikat", "kouni": "Kuni",
    "ouilang": "Wilang", "opish": "Opiç", "tagarhan": "Tagaxan",
    "libish": "Libiç", "lirhang": "Lixang", "tanarh": "Tanax",
    "talanne": "Talan", "sikatz": "Sikat", "iminne": "Imin", "aoui": "Awi",
    "ioual": "Iwal", "atorh": "Atox", "pilinne": "Pilin", "pirinne": "Pilin",
    "tainne": "Tain", "tchiminne": "Timin", "akitz": "Akit", "akits": "Akit",
    "mihalashi": "Mixalasi", "otoun": "Otun", "atoui": "Atwi",
    "apoui": "Apwi", "rhoyo": "Xoyo", "djiko": "Diko", "efunan": "Efunang",
    "iboqh": "Iboq", "tsiakang": "Tyakang", "bica": "Bika", "yoshi": "Yosi",
    "lubaq": "Lübaq", "liwice": "Liwis", "taossen": "Taosen",
    // D'XO, and it was reaching the page green in all three languages. His
    // Truku line writes the man `Pasang` — "Snd'xgan kari Pasang mo ka kia" —
    // while his French, and so our English and Chinese after it, write
    // Passan (ss = s, final -n for his -ng, both his own conventions above).
    // GLOSS_NAMES_ZH held the French spelling as its Truku value, which put
    // `passan` in GLOSS_NAME_FORMS with nothing to map it: the page linkified
    // a form the book does not contain. Now our two columns print his Truku
    // word, which the map already spells, and the French keeps Passan as
    // plain text — it is his own sentence, and nothing here rewrites that.
    "passan": "Pasang"
  };

  // "Autumn" is deliberately not here. The English of SPADAO reads "at Autumn's
  // place" for a Truku line that says Otun — but his own French reads "chez
  // Automne", so that one is his rendering and the English is a faithful
  // translation of it. Claiming it would also have wrecked KLPOXAN, whose gloss
  // opens "Autumn." because the word it defines *is* autumn. The Chinese of
  // SPADAO writes 秋（Otun）, and the bracket rule below is enough to fix it.

  // Deliberately NOT here: Laoken/Laokeng, Micat/Mikat, Libix/Libiç, Pilin/Pirin.
  // Those are two spellings Pecoraro himself uses in the Truku column, so they are
  // his variation, not the translation's, and nothing on this side should flatten
  // them.
  var GLOSS_NAMES_ZH = {
    "米卡茲": "Mikat", "米卡特": "Mikat", "米查特": "Mikat", "印愛": "Ingai",
    "英蓋": "Ingai", "利維斯": "Liwis", "里維斯": "Liwis", "利威斯": "Liwis",
    "錫丹": "Sitang", "希淡": "Sitang", "錫巴爾": "Sibal", "希巴爾": "Sibal",
    "希巴": "Sibal", "希霸": "Sibal", "希卡特": "Sikat", "皮林": "Pilin",
    "塔蘭": "Talan", "塔納赫": "Tanax", "塔納": "Tanax", "納提": "Nati",
    "阿推": "Atwi", "艾可": "Eco", "伊亨": "Ixeng", "奇比": "Cibi",
    "阿金": "Akin", "伊瓦爾": "Iwal", "伊瓦": "Iwal", "達陶": "Tato",
    "吉羅": "Diro", "吉揚": "Diyan", "伊敏": "Imin", "烏敏": "Umin",
    "巴東": "Patong", "阿吉": "Akit", "碧卡": "Bika", "伊班": "Iban",
    "伊博": "Iboq", "拉拜": "Labai", "勞肯": "Laoken", "拉歐丹": "Laotan",
    "里桑": "Lixang", "羅比雅": "Lobyaq", "巴拉斯": "Palas", "帕桑": "Pasang",
    "佩爾侯": "Pexo", "比少": "Pisao", "希保": "Sipao", "地旺": "Tiwang",
    "秋": "Otun"
  };

  // 秋 is the ordinary Chinese word for autumn — 秋天 is in a gloss about the
  // seasons — so it counts as a name only where the sentence itself brackets it.
  var ZH_NAME_PAREN_ONLY = { "秋": 1 };

  var ZH_NAME_KEYS = Object.keys(GLOSS_NAMES_ZH).sort(function (a, b) {
    return b.length - a.length;          // 伊瓦爾 must be tried before 伊瓦
  });
  var ZH_NAME_ANY = ZH_NAME_KEYS.join("|");
  var ZH_NAME_BARE = new RegExp(ZH_NAME_KEYS.filter(function (k) {
    return !Object.prototype.hasOwnProperty.call(ZH_NAME_PAREN_ONLY, k);
  }).join("|"), "g");
  // Where the Chinese already prints 漢字（Latin）, the translation is documenting
  // its own transliteration, and the Latin beside it wins — in either order. That
  // is accurate per sentence in a way no table can be: he writes the same man
  // Laoken in one example and Laokeng in the next, and 勞肯（Laoken） /
  // 勞肯（Laokeng） keep his own spelling each time.
  var ZH_NAME_HL = new RegExp("(?:" + ZH_NAME_ANY + ")\\s*[（(]\\s*([A-Za-zÀ-ÿ]+)\\s*[）)]", "g");
  var ZH_NAME_LH = new RegExp("([A-Za-zÀ-ÿ]+)\\s*[（(]\\s*(?:" + ZH_NAME_ANY + ")\\s*[）)]", "g");

  // The Truku spellings the tables produce, so the token loop below knows to hand
  // them to linkifyTruku — otherwise the name we just repaired would sit in the
  // gloss as plain uncoloured text that ignores the toggle.
  var GLOSS_NAME_FORMS = {};
  [GLOSS_NAMES, GLOSS_NAMES_ZH].forEach(function (t) {
    Object.keys(t).forEach(function (k) { GLOSS_NAME_FORMS[wordKey(t[k])] = 1; });
  });

  function glossNames(text, lang) {
    if (!text || lang === "fr") return text;
    if (lang === "zh") {
      text = text.replace(ZH_NAME_HL, "$1").replace(ZH_NAME_LH, "$1")
        .replace(ZH_NAME_BARE, function (m) { return GLOSS_NAMES_ZH[m]; });
    }
    return text.replace(TRUKU_TOKEN_G, function (w) {
      // An English possessive rides along on the token (Sibal's) and is not part
      // of the name.
      var poss = /['’]s$/.test(w) ? w.slice(-2) : "";
      var n = GLOSS_NAMES[wordKey(poss ? w.slice(0, -2) : w)];
      return n ? n + poss : w;
    });
  }

  // A form he cites while ARGUING ABOUT HOW TO SPELL IT. The double-quote signal
  // is right that these are Truku, and respelling them is still wrong: X'LO's note
  // reads "Faut-il écrire : Xlo'an ? Xlo"an ?" and modernize() sends both sides to
  // one word, so the question loses its two answers; D'XO asks "D'XOG ?, ou bien :
  // D'XO" ?" and MA glosses "MAUSA (ou : M"USA)". His letters ARE the content
  // there, and the toggle has nothing to offer a sentence about orthography.
  //
  // Not expressible as an identity map entry: modernize() hands a key back
  // untouched only when it matches PLAIN_WORD, which excludes `"`, so these would
  // fall through to matchCase and have the `"` normalized to `'` — flattening the
  // Xlo'an/Xlo"an contrast, which is the whole remark. Keyed through wordKey(), so
  // one key covers both of his marks. All four occur ONLY in these gloss slots
  // (checked over every string field in entries.js: 15 spans, 3 cards, one citation
  // rendered per language), so nothing else on the site can be reached by this.
  //
  // 2026-07-31: a fifth, and it earns its place a slightly different way. The
  // whole of "SIG's gloss is `("SYU = GSIG) Furoncle.` — an equation between
  // three spellings of one word, and only ONE of its two right-hand sides
  // carries the `"`. So GSIG is plain text and `"SYU` was the single coloured
  // word on the card, printed SYU in modern mode because charRules() drops his
  // mark. Respelling half of an equation about spellings states nothing; the
  // modern lexicon has no syu-shaped word for it either (esig 膿 12× is what
  // the headword itself becomes, and `syu` in speech is 2 unglossed tokens).
  // Verbatim puts both sides of his equals sign back on the same footing.
  // Its key is `'syu`, wordKey() having folded the `"`; it occurs in these
  // three gloss slots and nowhere else in the book.
  var CITE_VERBATIM = { "m'usa": 1, "xlo'": 1, "xlo'an": 1, "d'xo'": 1,
                        "'syu": 1 };

  // cites = trust the double-quote signal. True for the definition glosses, where
  // it was measured: 102 occurrences, 30 types, every one Truku. NOT true for the
  // example glosses, which are running prose and do quote ordinary words —
  // "matinalité", "manger", "gorillas", "Innontation" all carry a double quote
  // that tidyLatin left unpaired, and claiming those as Truku is the exact failure
  // the rule was drawn narrowly to avoid. Names are safe in both, being a closed
  // hand-checked list rather than a signal.
  function glossCites(text, lang, cites) {
    text = glossNames(text, lang);
    // No early return on "no double quote" any more: a name that was already
    // spelled his way needs linkifying too, and only the split can find it.
    var parts = text.split(TRUKU_TOKEN);
    var h = "";
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      var isName = i % 2 === 1 &&
        Object.prototype.hasOwnProperty.call(GLOSS_NAME_FORMS,
          wordKey(/['’]s$/.test(p) ? p.slice(0, -2) : p));
      if (i % 2 === 1 &&
          Object.prototype.hasOwnProperty.call(CITE_VERBATIM, wordKey(p))) {
        // Plain text in both modes: neither colour is honest about a spelling
        // being weighed rather than used, and the link is not wanted either —
        // Xlo"an is a proposal, not an entry to look up.
        h += esc(p);
      } else if (i % 2 === 1 && (isName ||
          (cites && p.indexOf('"') >= 0 && TRUKU_LETTER.test(p)))) {
        // An English possessive rides along on the token ("Laon's) and is not
        // part of the Truku word, so it is set outside the span.
        var poss = /['’]s$/.exec(p);
        if (poss) { h += linkifyTruku(p.slice(0, -2)) + esc(p.slice(-2)); }
        else { h += linkifyTruku(p); }
      } else {
        h += esc(p);
      }
    }
    return h;
  }

  function glossHtml(obj) {
    var h = "";
    if (shown.fr && obj.fr) h += '<p class="gloss"><span class="lang-chip fr">FR</span>' + glossCites(tidy(obj.fr, "fr"), "fr", true) + "</p>";
    if (shown.en && obj.en) h += '<p class="gloss"><span class="lang-chip en">EN</span>' + glossCites(tidy(obj.en, "en"), "en", true) + "</p>";
    if (shown.zh && obj.zh) h += '<p class="gloss"><span class="lang-chip zh">中</span>' + glossCites(tidy(obj.zh, "zh"), "zh", true) + "</p>";
    return h;
  }

  function examplesHtml(list) {
    if (!list || !list.length) return "";
    var h = '<div class="examples">';
    list.forEach(function (x) {
      h += '<div class="example"><div class="truku">' + spellMark("§", "Example / exemple") +
        " " + linkifyTruku(tidy(x.t, "tr"), false, FORM_PROSE) + audioBtn(x.a) + "</div>";
      if (shown.fr && x.fr) h += '<p class="ex-gloss"><span class="lang-chip fr">FR</span>' + glossCites(tidy(x.fr, "fr"), "fr") + "</p>";
      if (shown.en && x.en) h += '<p class="ex-gloss"><span class="lang-chip en">EN</span>' + glossCites(tidy(x.en, "en"), "en") + "</p>";
      if (shown.zh && x.zh) h += '<p class="ex-gloss"><span class="lang-chip zh">中</span>' + glossCites(tidy(x.zh, "zh"), "zh") + "</p>";
      h += "</div>";
    });
    return h + "</div>";
  }

  function entryHtml(e) {
    var h = '<article class="entry">';
    h += '<div class="hw-line"><span class="hw">' + linkifyTruku(tidyForm(formText(e.hw)), true) + "</span>";
    h += audioBtn(e.a);
    h += tagHtml(e.tag, e.hw);
    if (e.crossRef) {
      // "VR. PAUX" — his own see-also, mark and all. The mark was travelling into
      // the link's own text and into data-ref, so the arrow pointed at a headword
      // called "VR. PAUX", which no entry is. Strip it for the lookup and keep it
      // on screen in the editorial hand.
      var xr = e.crossRef.replace(/^\s*vr\.?\s*/i, "");
      var xm = xr === e.crossRef ? "" : '<span class="meta-abbr" title="voir / see">vr.</span> ';
      h += ' <span class="tag">→ ' + xm + xr.split(",").map(function (part) {
        // He sends the reader to more than one form at a time — "QDALAN, QDALUN" —
        // and the whole string was one dead link, because no entry is called that.
        var t = part.trim();
        if (!t) return "";
        // "ces mots." is French, "L'PAN (note)" a form with a remark attached.
        // Neither is a word to colour or respell — "mots" was reaching the screen
        // as "muts" — so anything with a space that names no entry stays editorial.
        if (/\s/.test(t) && !lookupWord(t)) {
          return '<span class="meta-abbr">' + esc(t) + "</span>";
        }
        // The arrow can point at its own headword. Modernizing both sides collapses
        // his doublet into one word — that is the map working — and 24 of these
        // reach a genuinely different entry, so "GHAK → GHAK" on G'XAK is a live
        // link to G'XAP, not a bug to delete. A root tag in the same position IS
        // dropped (see tagHtml), because a tag alternative is this entry's own
        // second try and navigates nowhere. Here the two cards do differ, and in
        // modern mode his spelling is the only thing that still tells them apart,
        // so keep the link and label it in his hand rather than repeat the headword.
        var self = spellingModern &&
          norm(modernizeText(t)) === norm(modernizeText(variants(e.hw)[0] || e.hw));
        if (self) {
          return '<span class="crossref-link xref-his" data-ref="' + esc(t) +
            '" title="His spelling / son orthographe">' + esc(formText(t)) + "</span>";
        }
        return '<span class="crossref-link ' + (respellable(t) ? "w-mod" : "w-raw") +
          '" data-ref="' + esc(t) + '">' + esc(dispText(formText(t))) + "</span>";
      }).join(", ") + "</span>";
    }
    h += "</div>";
    if (e.paradigm) h += '<p class="paradigm">' + spellMark("°", "Forms / formes") + " " + linkifyTruku(tidyForm(e.paradigm)) + "</p>";
    h += glossHtml(e);
    h += examplesHtml(e.examples);
    (e.subs || []).forEach(function (s) {
      h += '<div class="subentry"><div class="hw-line"><span class="sub-form">' + linkifyTruku(tidyForm(formText(s.form)), false, FORM_PROSE) + "</span>" + audioBtn(s.a) + "</div>";
      if (s.paradigm) h += '<p class="paradigm">' + spellMark("°", "Forms / formes") + " " + linkifyTruku(tidyForm(s.paradigm)) + "</p>";
      h += glossHtml(s);
      h += examplesHtml(s.examples);
      h += "</div>";
    });
    if (e.truncated) h += '<p class="fine" style="color:var(--muted);font-size:0.82rem;margin:0.6rem 0 0;">⚠ Entry truncated in the scanned pilot pages. / 條目於掃描頁末中斷。</p>';
    return h + "</article>";
  }

  // The one-line contexts have room for a single gloss, and French is the source
  // language, not the one most readers here want: English first, then Chinese, and
  // French only when it is the sole one enabled. (A full entry still shows every
  // enabled language, in fr/en/zh order.)
  function oneGloss(s) {
    if (shown.en && s.en) return '<span class="lang-chip en">EN</span>' + esc(tidy(s.en, "en"));
    if (shown.zh && s.zh) return '<span class="lang-chip zh">中</span>' + esc(tidy(s.zh, "zh"));
    if (shown.fr && s.fr) return '<span class="lang-chip fr">FR</span>' + esc(tidy(s.fr, "fr"));
    return "";
  }

  // One-line cross-reference stub for a sub-form standing at its own alphabetical
  // slot; the whole card opens the root entry it belongs to.
  function stubHtml(f) {
    var s = f.sub || f.entry;
    var g = oneGloss(s);
    // data-ref carries the displayed spelling, so the search box echoes what the
    // reader tapped; either orthography resolves to the same entry now.
    var label = dispText(formText(f.label));
    var h = '<article class="entry stub" data-ref="' + esc(label) + '">';
    h += '<div class="hw-line"><span class="hw stub-hw">' + linkifyTruku(tidyForm(formText(f.label)), true) + "</span>";
    h += audioBtn(s.a);
    h += '<span class="tag stub-parent">→ ' + linkifyTruku(tidyForm(formText(f.entry.hw)), true) + "</span></div>";
    if (g) h += '<p class="gloss stub-gloss">' + g + "</p>";
    return h + "</article>";
  }

  // An alias slot is a pointer, never a second copy of the entry: without this a
  // bracketed headword like "L'NGLONG (LNGLONG)" would set two full cards under L.
  function formHtml(f) {
    return f.sub || f.alias ? stubHtml(f) : entryHtml(f.entry);
  }

  // A letter listing is an INDEX, not a run of entries. Rendering roots as full
  // cards put 259 of them under S carrying 804 example sentences — 225,000
  // characters on one scroll — and mixed two densities on one page, so the
  // headwords a reader is scanning for sat buried inside other entries' examples.
  // A dictionary page works because the eye lands on a column of headwords; this
  // gives every form one line, root and sub-form alike, and opens the card on tap.
  // The two differ only in what the line says about itself: a root stands on its
  // own, a sub-form is indented and names the root it belongs to. (Reuses the
  // .entry.stub class so the existing click handler already opens it.)
  function indexRowHtml(f) {
    var isRoot = !f.sub && !f.alias;
    var s = f.sub || f.entry;
    var g = oneGloss(s);
    var label = dispText(formText(f.label));
    var h = '<article class="entry stub idx ' + (isRoot ? "idx-root" : "idx-sub") +
      '" data-entry="' + f.ei + '" data-ref="' + esc(label) + '">';
    h += '<div class="hw-line"><span class="hw stub-hw">' +
      linkifyTruku(tidyForm(formText(f.label)), true) + "</span>";
    h += audioBtn(s.a);
    if (!isRoot) {
      h += '<span class="tag stub-parent">→ ' +
        linkifyTruku(tidyForm(formText(f.entry.hw)), true) + "</span>";
    }
    h += "</div>";
    if (g) h += '<p class="gloss stub-gloss">' + g + "</p>";
    return h + "</article>";
  }

  function introTextHtml(text) {
    return text
      .split(/\n\n+/)
      .map(function (p) { return "<p>" + esc(p).replace(/\n/g, "<br>") + "</p>"; })
      .join("");
  }

  function introLangHtml(label, cls, text) {
    if (!text) return "";
    return '<div class="intro-block"><span class="lang-chip ' + cls + '">' + label + "</span>" + introTextHtml(text) + "</div>";
  }

  function introSectionHtml(s) {
    var h = '<div class="intro-section">';
    if (s.image) h += '<img class="intro-image" src="intro-images/' + esc(s.image) + '" alt="Scanned page ' + s.page + '">';
    // Figure/table pages: show only the scanned figure, no transcribed text.
    if (s.type === "table_image") return h + "</div>";
    h += introLangHtml("TR", "tr", s.tr);  // Taroko original — always shown, like the dictionary
    h += introLangHtml("FR", "fr", shown.fr ? s.fr : "");
    h += introLangHtml("EN", "en", shown.en ? s.en : "");
    h += introLangHtml("中", "zh", shown.zh ? s.zh : "");
    return h + "</div>";
  }

  var results = document.getElementById("results");
  var searchBox = document.getElementById("search");

  // The letter currently on screen, so a spelling toggle can re-bucket it instead
  // of silently turning the listing into a search for the letter itself.
  var currentLetter = null;
  var currentFirst = null;

  function renderAlphabet() {
    // Home = the cover hero (search + A–Z + tools overlaid on it); results area empties.
    stopAudio();
    currentLetter = null;
    document.body.classList.add("home");
    results.innerHTML = "";
  }

  function showLetter(letter) {
    hidePreview();
    stopAudio();
    document.body.classList.remove("home");
    // Letter listings run over the sorted form index, so derived forms appear at
    // their own initial (as stubs) interleaved with the roots under that letter.
    var list = activeForms().filter(function (f) { return initial(f) === letter; });
    currentLetter = letter;
    currentFirst = list[0] || null;
    searchBox.value = letter === "#" ? "" : letter;
    if (!list.length) {
      results.innerHTML = '<p class="no-results">No entries found. / 查無資料。</p>';
      return;
    }
    var roots = 0;
    list.forEach(function (f) { if (!f.sub && !f.alias) roots++; });
    results.innerHTML =
      '<p class="letter-head"><span class="letter-head-l">' +
      esc(letter === "#" ? "#" : letter) + "</span>" +
      list.length + " forms · " + roots + " entries / " +
      list.length + " 個詞形 · " + roots + " 條目</p>" +
      list.map(indexRowHtml).join("");
    window.scrollTo({ top: 0 });
  }

  // One named entry on screen, with no search behind it. `openEntry()` cannot do
  // this job for an A–Z row: it puts the label in the box and searches, and his
  // headwords S, M and A are single letters, so tapping the S row asked for every
  // card containing an s.
  function showEntry(e, refText) {
    hidePreview();
    stopAudio();
    currentLetter = null;
    document.body.classList.remove("home");
    searchBox.value = refText;
    results.innerHTML = entryHtml(e);
    window.scrollTo({ top: 0 });
  }

  function showRandomEntry() {
    var e = window.ENTRIES[Math.floor(Math.random() * window.ENTRIES.length)];
    showEntry(e, e.hw);
  }

  function render() {
    hidePreview();
    stopAudio();
    if (!searchBox.value.trim()) {
      renderAlphabet();
      return;
    }
    currentLetter = null;
    document.body.classList.remove("home");
    var list = filter(searchBox.value);
    if (!list.length) {
      results.innerHTML = '<p class="no-results">No entries found. / 查無資料。</p>';
      return;
    }
    results.innerHTML = list.map(entryHtml).join("");
  }

  function openEntry(ref) {
    hidePreview();
    searchBox.value = ref;
    render();
    window.scrollTo({ top: 0 });
  }

  results.addEventListener("click", function (ev) {
    var sm = ev.target.closest ? ev.target.closest(".spell-toggle") : null;
    if (sm) {
      ev.stopPropagation();
      setSpelling(!spellingModern);
      return;
    }
    var ab = ev.target.closest ? ev.target.closest(".audio-btn") : null;
    if (ab) {
      ev.stopPropagation();
      playClip(ab.getAttribute("data-audio"), ab);
      return;
    }
    // Checked before the stub, because an abbreviation can sit inside one.
    var ma = ev.target.closest ? ev.target.closest(".meta-abbr[data-abbr]") : null;
    if (ma) {
      ev.stopPropagation();
      showAbbr(ma);
      return;
    }
    // An A–Z row knows which entry it stands for, so it opens that one directly.
    var row = ev.target.closest ? ev.target.closest(".entry.idx[data-entry]") : null;
    if (row) {
      var e = window.ENTRIES[+row.getAttribute("data-entry")];
      if (e) { showEntry(e, row.getAttribute("data-ref")); return; }
    }
    // A stub card is a pointer, not an entry: one tap opens the root it belongs to.
    var stub = ev.target.closest ? ev.target.closest(".entry.stub") : null;
    if (stub) {
      openEntry(stub.getAttribute("data-ref"));
      return;
    }
    var t = ev.target.closest ? ev.target.closest(".crossref-link") : null;
    if (t) {
      clearTimeout(previewTimer);
      var ref = t.getAttribute("data-ref");
      // First tap shows the gloss; a second tap on the same word opens the entry.
      var showing = !wordPreview.classList.contains("hidden") &&
        wordPreview.getAttribute("data-ref") === norm(ref);
      if (showing) openEntry(ref);
      else showPreview(t);
      return;
    }
    if (ev.target.classList.contains("alphabet-btn")) {
      showLetter(ev.target.getAttribute("data-letter"));
    } else if (ev.target.classList.contains("random-btn")) {
      showRandomEntry();
    }
  });

  // Tap anywhere else dismisses the gloss preview (mobile has no mouseout).
  document.addEventListener("click", function (ev) {
    var onLink = ev.target.closest &&
      ev.target.closest(".crossref-link, .meta-abbr[data-abbr]");
    if (!onLink && !wordPreview.contains(ev.target)) hidePreview();
  });

  // ---------- home navigation ----------
  function goHome() {
    hidePreview();
    closeSheet();
    searchBox.value = "";
    render();
    searchBox.focus();
    window.scrollTo({ top: 0 });
  }

  // Re-render after a settings change. A letter listing stays a letter listing
  // (calling render() would turn it into a search for the letter), and since a
  // word can move between letters under the modern toggle — xbui under X becomes
  // hbuy under H — it follows the words that were on screen rather than sitting
  // on a letter that may now be empty.
  // The body carries the orthography, because the § marker, the punctuation and
  // an example's left rule are coloured by the mode rather than by any one word.
  function applySpellingClass() {
    document.body.classList.toggle("spelling-modern", spellingModern);
  }

  function rerender() {
    applySpellingClass();
    if (currentLetter) showLetter(currentFirst ? initial(currentFirst) : currentLetter);
    else render();
  }

  // The one place the orthography changes, whether it was a √ / ° / § in the
  // middle of the page or the radio in Settings. Tapping a marker halfway down a
  // long entry must not throw the reader back to the top, so the scroll position
  // is held across the re-render; and the clip that may be playing is a reading
  // of the modern spelling, so leaving that mode stops it.
  function setSpelling(modern) {
    if (spellingModern === modern) return;
    spellingModern = modern;
    saveSpelling();
    if (!modern) stopAudio();
    var y = window.pageYOffset;
    rerender();
    window.scrollTo(0, y);
  }

  // ---------- hover word preview ----------
  var wordPreview = document.getElementById("word-preview");
  var previewTimer = null;

  function hidePreview() {
    clearTimeout(previewTimer);
    wordPreview.classList.add("hidden");
  }

  function previewGlossHtml(w) {
    var g = oneGloss(w);
    return g ? '<p class="wp-gloss">' + g + "</p>" : "";
  }

  function showPreview(link) {
    var w = lookupWord(link.getAttribute("data-ref"));
    if (!w) return;
    var h = '<div><span class="wp-hw">' + linkifyTruku(tidyForm(formText(w.hw)), true) + "</span>";
    if (w.parentHw) h += '<span class="wp-parent">→ ' + esc(dispText(formText(w.parentHw))) + "</span>";
    h += "</div>" + previewGlossHtml(w) + '<p class="wp-hint">Tap again for full entry · 再點一次查看完整條目</p>';
    wordPreview.setAttribute("data-ref", norm(link.getAttribute("data-ref")));
    wordPreview.innerHTML = h;
    wordPreview.classList.remove("hidden");
    placePreview(link);
  }

  function placePreview(anchor) {
    var r = anchor.getBoundingClientRect();
    var pw = wordPreview.offsetWidth, ph = wordPreview.offsetHeight;
    var left = Math.min(Math.max(8, r.left), window.innerWidth - pw - 8);
    var top = r.bottom + 8;
    if (top + ph > window.innerHeight - 8) top = r.top - ph - 8;
    wordPreview.style.left = left + "px";
    wordPreview.style.top = Math.max(8, top) + "px";
  }

  // Same bubble, different content: what one of his abbreviations means, in every
  // language the reader has enabled. Never carries a data-ref — it is an
  // explanation, not a word, and there is no entry to open on a second tap.
  function showAbbr(el) {
    var a = META_ABBR[el.getAttribute("data-abbr")];
    if (!a) return;
    var h = '<div><span class="wp-hw">' + esc(el.textContent) + '.</span>' +
      '<span class="wp-parent wp-abbr-full">' + esc(a.full) + "</span></div>";
    if (shown.fr) h += '<p class="wp-gloss"><span class="lang-chip fr">FR</span>' + esc(a.fr) + "</p>";
    if (shown.en) h += '<p class="wp-gloss"><span class="lang-chip en">EN</span>' + esc(a.en) + "</p>";
    if (shown.zh) h += '<p class="wp-gloss"><span class="lang-chip zh">中</span>' + esc(a.zh) + "</p>";
    wordPreview.removeAttribute("data-ref");
    wordPreview.innerHTML = h;
    wordPreview.classList.remove("hidden");
    placePreview(el);
  }

  results.addEventListener("mouseover", function (ev) {
    var link = ev.target.closest && ev.target.closest(".crossref-link");
    if (!link || link.contains(ev.relatedTarget)) return;
    clearTimeout(previewTimer);
    previewTimer = setTimeout(function () { showPreview(link); }, 200);
  });
  results.addEventListener("mouseout", function (ev) {
    var link = ev.target.closest && ev.target.closest(".crossref-link");
    if (!link || link.contains(ev.relatedTarget)) return;
    hidePreview();
  });

  // Search only when the user presses Return (or taps the keyboard's Go/Search key).
  // Live-searching on every keystroke made the first character yank the page from the
  // cover to results before you'd finished typing. Clearing the box still goes home.
  searchBox.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") { ev.preventDefault(); render(); }
  });
  searchBox.addEventListener("input", function () {
    if (!searchBox.value.trim()) render();
  });

  document.getElementById("btn-random").addEventListener("click", showRandomEntry);
  document.getElementById("btn-home").addEventListener("click", goHome);

  // ---------- sheet ----------
  var backdrop = document.getElementById("sheet-backdrop");
  var sheetContent = document.getElementById("sheet-content");

  var sheet = document.getElementById("sheet");
  var sheetHome = document.getElementById("sheet-home");

  function openSheet(html, wide, showHome) {
    sheetContent.innerHTML = html;
    sheet.classList.toggle("wide", !!wide);
    if (sheetHome) sheetHome.classList.toggle("hidden", !showHome);
    backdrop.classList.remove("hidden");
  }
  if (sheetHome) sheetHome.addEventListener("click", goHome);
  var photoTimer = null;
  function stopPhotoCycle() {
    if (photoTimer) { clearInterval(photoTimer); photoTimer = null; }
  }

  function closeSheet() { backdrop.classList.add("hidden"); stopPhotoCycle(); }

  document.getElementById("sheet-close").addEventListener("click", closeSheet);
  backdrop.addEventListener("click", function (ev) {
    if (ev.target === backdrop) closeSheet();
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") closeSheet();
  });

  // A–Z as a sheet, the only entry point: the strip that used to run along the
  // bottom of the cover was an opaque band over the byline, and it was out of
  // reach from a listing anyway. The grid also fits every letter at a tappable
  // size, which a wrapped strip could not. Built per open — follows the toggle.
  document.getElementById("btn-alpha").addEventListener("click", function () {
    stopPhotoCycle();
    var h = "<h2>🔤 Browse A–Z · 依字母瀏覽</h2>" +
      '<div class="alphabet-index">' +
      '<p class="alphabet-hint">Pick a first letter. Derived forms are listed at their own letter, pointing back to their root. / 選擇首字母。派生詞形列於各自的字母下,並標示其詞根。</p>' +
      '<div class="alphabet-grid">' +
      currentAlphabet().map(function (l) {
        return '<button class="alphabet-btn" data-letter="' + l + '">' + l + "</button>";
      }).join("") +
      "</div></div>";
    // No home icon: it sits over this sheet's (longer) heading, and closing
    // already returns you to the listing, which has its own home button.
    openSheet(h, false, false);
  });

  // Delegated once — openSheet replaces the sheet's contents, not the container,
  // so binding per open would stack a listener each time.
  sheetContent.addEventListener("click", function (ev) {
    if (!ev.target.classList.contains("alphabet-btn")) return;
    closeSheet();
    showLetter(ev.target.getAttribute("data-letter"));
  });

  // Ordered by his apparent age, so the cycle runs as a life: the young priest at
  // the altar, then the missionary years, then old age, and the memorial at Wanrong
  // last. The file numbers are the order they were added, not the order they show in.
  var PHOTOS = [
    "pecoraro5.jpg",  // saying Mass — clean-shaven, youngest
    "pecoraro6.jpg",  // in the village with the baskets — cropped hair, light beard
    "pecoraro2.jpg",  // dressing a wound — the nurse's work, auburn hair and beard
    "pecoraro7.jpg",  // with the goat kid and the boys — fuller beard, beret
    "pecoraro1.jpg",  // on the hillside above the valley — white-haired
    "pecoraro3.jpg",  // garlanded among the people — oldest
    "pecoraro4.jpg"   // his memorial in Wanrong Township
  ];
  var PHOTO_CYCLE_MS = 5000;

  document.getElementById("btn-about").addEventListener("click", function () {
    stopPhotoCycle();
    var idx = 0;
    openSheet(
      (
      '<img class="about-photo" src="' + PHOTOS[idx] + '" alt="Portrait of Ferdinando Pecoraro MEP">' +
      '<p class="fine photo-caption">Ferdinando Pecoraro MEP</p>' +
      "<p>This digital edition is based on Ferdinando Pecoraro's Taroko–French dictionary, " +
      "<em>Essai de dictionnaire taroko-français</em> (SECMI, Paris, 1977). Pecoraro was a priest of the Paris Foreign Missions Society " +
      "(Missions Étrangères de Paris, M.E.P.), a French Catholic missionary institute; hence the initials after his name.</p>" +
      "<p>本辭典以法國巴黎外方傳教會(MEP)神父 Ferdinando Pecoraro 所編之太魯閣語-法語辭典為基礎。</p>" +
      "<p>English and Chinese translations added from the French; draft, pending review by native speakers.</p>" +
      "<p>“Taroko” is the Japanese-era romanization of the people's own name, Truku, as spoken on Taiwan's east coast (Hualien). Pecoraro writes it “T’roko.”</p>" +
      "<p>「太魯閣」（Taroko）源自日治時期的羅馬拼音，是東台灣（花蓮）太魯閣族自稱「Truku」的另一種轉寫方式。貝科拉羅神父原文寫作「T'roko」。</p>" +
      "<p>This is a root-word dictionary: entries are organized by root (racine), not by every inflected or derived form. Grammatical particles and verb-conjugated forms appearing in example sentences may not have their own headword.</p>" +
      "<p>本辭典以詞根（root word）為主要條目，並非收錄每一個詞形變化。例句中出現的語法助詞或動詞變位形式，可能沒有獨立詞條。</p>" +
      "<p>Cross-referencing against a modern-orthography Truku corpus confirmed that the example-sentence words without their own headword are almost entirely inflected or derived forms of roots already in the dictionary (as noted above), or the same word under a different spelling; genuine lexical gaps are very few.</p>" +
      "<p>經與現代太魯閣語語料庫比對，證實例句中未設獨立詞條的詞彙，絕大多數為已收錄詞根的屈折或派生形式（如上所述），或同詞的不同拼寫；真正的詞彙缺口極少。</p>" +
      "<p class=\"fine\">Digitized by Darryl Sterk, Associate Professor of Translation, Lingnan University.</p>" +
      "<p class=\"fine\">由嶺南大學翻譯系副教授石岱崙數位化整理。</p>" +
      "<p class=\"fine\">" + window.ENTRIES.length + " entries, digitized from all 398 pages.</p>" +
      "<p class=\"fine\">共收錄 " + window.ENTRIES.length + " 條詞條,數位化自全書 398 頁。</p>"
      ), false, true);
    photoTimer = setInterval(function () {
      idx = (idx + 1) % PHOTOS.length;
      var img = sheetContent.querySelector(".about-photo");
      if (img) img.src = PHOTOS[idx];
    }, PHOTO_CYCLE_MS);
  });

  var INTRO_GROUPS = [
    { title: "Foreword to the Taroko", zh: "太魯閣語致詞", pages: [4] },
    { title: "Dedication", zh: "獻詞", pages: [5] },
    { title: "Introduction: The Tayal Peoples", zh: "導論:泰雅族群", pages: [6] },
    { title: "Preface: How This Dictionary Came About", zh: "前言:本書緣起", pages: [7, 8, 9, 10] },
    { title: "Notes", zh: "註釋", pages: [11] },
    { title: "On the Dictionary & the Taroko Language", zh: "詞典體例與太魯閣語說明", pages: [12, 13, 14, 15, 16, 17] },
    { title: "Conventional Signs", zh: "慣用符號", pages: [18] },
    { title: "Sample Texts", zh: "例文", pages: [19] },
    { title: "Phonology Tables", zh: "音韻系統表", pages: [20] },
    { title: "Proposed Orthography", zh: "建議拼寫法", pages: [21] }
  ];

  document.getElementById("btn-intro").addEventListener("click", function () {
    stopPhotoCycle();
    var byPage = {};
    (window.INTRO || []).forEach(function (s) { byPage[s.page] = s; });
    var h = "<h2>📖 Introduction · 導言</h2>" +
      "<p class=\"fine\">Pecoraro's own preface, dedication, and notes on Taroko orthography and phonology (1977). " +
      "English and Chinese translated from the French; draft, pending review by native speakers.</p>";
    INTRO_GROUPS.forEach(function (g, i) {
      h += '<details class="intro-group"' + (i === 0 ? " open" : "") + '>' +
        '<summary>' + esc(g.title) + ' <span class="group-zh">' + esc(g.zh) + "</span></summary>" +
        '<div class="intro-group-body">';
      g.pages.forEach(function (p) {
        if (byPage[p]) h += introSectionHtml(byPage[p]);
      });
      h += "</div></details>";
    });
    openSheet(h, true, true);
  });

  document.getElementById("btn-settings").addEventListener("click", function () {
    var h = "<h2>⚙ Languages · 語言</h2><p class=\"fine\">Choose which translations to show. Truku is always shown. / 選擇顯示的語言,太魯閣語恆顯示。</p>";
    LANGS.forEach(function (l) {
      h += '<label class="lang-option"><input type="checkbox" data-lang="' + l.key + '"' +
        (shown[l.key] ? " checked" : "") + "><span>" + l.label + "</span></label>";
    });
    h += '<h2 style="margin-top:1.1rem">Spelling · 拼寫法</h2>' +
      '<p class="fine">Word-by-word conversion cross-checked against a modern Truku dictionary (~3,000 words verified by attestation and Chinese gloss); other words use approximate character rules (o→u, l→r, x→h). Not proofread; Pecoraro\'s original spelling is authoritative. Search accepts either spelling whichever setting is on. / 逐詞轉換,約3,000詞已比對現代太魯閣語詞典(拼寫與華語詞義雙重驗證);其餘詞使用近似字母規則(o→u、l→r、x→h)。未經校對,貝科拉羅原文拼寫為準。無論設定為何,搜尋皆可使用兩種拼寫。</p>' +
      '<label class="lang-option"><input type="radio" name="spelling" value="original"' +
      (spellingModern ? "" : " checked") + "><span>Pecoraro's spelling (1977) / 原文拼寫</span></label>" +
      '<label class="lang-option"><input type="radio" name="spelling" value="modern"' +
      (spellingModern ? " checked" : "") + "><span>Modern Truku spelling (approx.) / 現代拼寫(近似)</span></label>";
    openSheet(h, false, true);
    sheetContent.querySelectorAll("input[data-lang]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        shown[cb.getAttribute("data-lang")] = cb.checked;
        saveLangs();
        rerender();
      });
    });
    sheetContent.querySelectorAll("input[name=\"spelling\"]").forEach(function (rb) {
      rb.addEventListener("change", function () {
        setSpelling(rb.value === "modern");
      });
    });
  });

  // ---------- init ----------
  var countEl = document.getElementById("entry-count");
  if (countEl) countEl.textContent = window.ENTRIES.length;
  var params = new URLSearchParams(location.search);
  if (params.get("q")) searchBox.value = params.get("q");
  applySpellingClass();
  render();
})();
