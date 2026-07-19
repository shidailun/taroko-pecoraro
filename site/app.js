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

  // ---------- search ----------
  function norm(s) {
    return (s || "")
      .toLowerCase()
      .replace(/[’ʼ]/g, "'")
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "");
  }

  function entryText(e) {
    var parts = [e.hw, e.fr, e.en, e.zh, e.paradigm || ""];
    (e.examples || []).forEach(function (x) { parts.push(x.t, x.fr, x.en, x.zh); });
    (e.subs || []).forEach(function (s) {
      parts.push(s.form, s.fr, s.en, s.zh, s.paradigm || "");
      (s.examples || []).forEach(function (x) { parts.push(x.t, x.fr, x.en, x.zh); });
    });
    return norm(parts.join("  "));
  }

  var INDEX = window.ENTRIES.map(function (e) {
    return { entry: e, text: entryText(e), hw: norm(e.hw) };
  });

  var HW_SET = {};
  window.ENTRIES.forEach(function (e) {
    HW_SET[norm(e.hw)] = true;
    (e.subs || []).forEach(function (s) { if (s.form) HW_SET[norm(s.form)] = true; });
  });

  var ALPHABET = (function () {
    var seen = {}, letters = [], hasSymbol = false;
    window.ENTRIES.forEach(function (e) {
      var c = norm(e.hw).charAt(0);
      if (/[a-z]/.test(c)) {
        c = c.toUpperCase();
        if (!seen[c]) { seen[c] = true; letters.push(c); }
      } else {
        hasSymbol = true;
      }
    });
    letters.sort();
    if (hasSymbol) letters.push("#");
    return letters;
  })();

  function filter(q) {
    q = norm(q.trim());
    if (!q) return window.ENTRIES;
    var starts = [], contains = [];
    INDEX.forEach(function (it) {
      if (it.hw.indexOf(q) === 0) starts.push(it.entry);
      else if (it.text.indexOf(q) !== -1) contains.push(it.entry);
    });
    return starts.concat(contains);
  }

  // ---------- render ----------
  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function linkifyTruku(text) {
    if (!text) return "";
    var parts = text.split(/([A-Za-zÀ-ÿ'’ʼ]+)/);
    var h = "";
    for (var i = 0; i < parts.length; i++) {
      var part = parts[i];
      if (i % 2 === 1 && HW_SET[norm(part)]) {
        h += '<span class="crossref-link" data-ref="' + esc(part) + '">' + esc(part) + "</span>";
      } else {
        h += esc(part);
      }
    }
    return h;
  }

  function tagHtml(tag) {
    if (!tag) return "";
    if (tag === "(R)" || tag === "(R.)") {
      return '<span class="tag root-tag" title="Root / racine">√</span>';
    }
    return '<span class="tag">' + esc(tag) + "</span>";
  }

  function glossHtml(obj) {
    var h = "";
    if (shown.fr && obj.fr) h += '<p class="gloss"><span class="lang-chip fr">FR</span>' + esc(obj.fr) + "</p>";
    if (shown.en && obj.en) h += '<p class="gloss"><span class="lang-chip en">EN</span>' + esc(obj.en) + "</p>";
    if (shown.zh && obj.zh) h += '<p class="gloss"><span class="lang-chip zh">中</span>' + esc(obj.zh) + "</p>";
    return h;
  }

  function examplesHtml(list) {
    if (!list || !list.length) return "";
    var h = '<div class="examples">';
    list.forEach(function (x) {
      h += '<div class="example"><div class="truku">§ ' + linkifyTruku(x.t) + "</div>";
      if (shown.fr && x.fr) h += '<p class="ex-gloss"><span class="lang-chip fr">FR</span>' + esc(x.fr) + "</p>";
      if (shown.en && x.en) h += '<p class="ex-gloss"><span class="lang-chip en">EN</span>' + esc(x.en) + "</p>";
      if (shown.zh && x.zh) h += '<p class="ex-gloss"><span class="lang-chip zh">中</span>' + esc(x.zh) + "</p>";
      h += "</div>";
    });
    return h + "</div>";
  }

  function entryHtml(e) {
    var h = '<article class="entry">';
    h += '<div class="hw-line"><span class="hw">' + esc(e.hw) + "</span>";
    h += tagHtml(e.tag);
    if (e.crossRef) h += ' <span class="tag">→ <span class="crossref-link" data-ref="' + esc(e.crossRef) + '">' + esc(e.crossRef) + "</span></span>";
    h += "</div>";
    if (e.paradigm) h += '<p class="paradigm">° ' + linkifyTruku(e.paradigm) + "</p>";
    h += glossHtml(e);
    h += examplesHtml(e.examples);
    (e.subs || []).forEach(function (s) {
      h += '<div class="subentry"><div class="hw-line"><span class="sub-form">' + linkifyTruku(s.form) + "</span></div>";
      if (s.paradigm) h += '<p class="paradigm">° ' + linkifyTruku(s.paradigm) + "</p>";
      h += glossHtml(s);
      h += examplesHtml(s.examples);
      h += "</div>";
    });
    if (e.truncated) h += '<p class="fine" style="color:var(--muted);font-size:0.82rem;margin:0.6rem 0 0;">⚠ Entry truncated in the scanned pilot pages. / 條目於掃描頁末中斷。</p>';
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
    h += introLangHtml("FR", "fr", shown.fr ? s.fr : "");
    h += introLangHtml("EN", "en", shown.en ? s.en : "");
    h += introLangHtml("中", "zh", shown.zh ? s.zh : "");
    return h + "</div>";
  }

  var results = document.getElementById("results");
  var searchBox = document.getElementById("search");

  function renderAlphabet() {
    var h = '<div class="alphabet-index">' +
      '<p class="alphabet-hint">Browse by first letter, or search above. / 依字母瀏覽,或於上方搜尋。</p>' +
      '<div class="alphabet-grid">';
    ALPHABET.forEach(function (letter) {
      h += '<button class="alphabet-btn" data-letter="' + letter + '">' + letter + "</button>";
    });
    h += "</div>" +
      '<button class="random-btn" data-action="random">🎲 Random word · 隨機詞條</button>' +
      "</div>";
    results.innerHTML = h;
  }

  function showLetter(letter) {
    var list = letter === "#"
      ? window.ENTRIES.filter(function (e) { return !/[a-z]/.test(norm(e.hw).charAt(0)); })
      : window.ENTRIES.filter(function (e) { return norm(e.hw).charAt(0) === letter.toLowerCase(); });
    searchBox.value = letter === "#" ? "" : letter;
    if (!list.length) {
      results.innerHTML = '<p class="no-results">No entries found. / 查無資料。</p>';
      return;
    }
    results.innerHTML = list.map(entryHtml).join("");
    window.scrollTo({ top: 0 });
  }

  function showRandomEntry() {
    var e = window.ENTRIES[Math.floor(Math.random() * window.ENTRIES.length)];
    searchBox.value = e.hw;
    results.innerHTML = entryHtml(e);
    window.scrollTo({ top: 0 });
  }

  function render() {
    if (!searchBox.value.trim()) {
      renderAlphabet();
      return;
    }
    var list = filter(searchBox.value);
    if (!list.length) {
      results.innerHTML = '<p class="no-results">No entries found. / 查無資料。</p>';
      return;
    }
    results.innerHTML = list.map(entryHtml).join("");
  }

  results.addEventListener("click", function (ev) {
    var t = ev.target;
    if (t.classList.contains("crossref-link")) {
      searchBox.value = t.getAttribute("data-ref");
      render();
      window.scrollTo({ top: 0 });
    } else if (t.classList.contains("alphabet-btn")) {
      showLetter(t.getAttribute("data-letter"));
    } else if (t.classList.contains("random-btn")) {
      showRandomEntry();
    }
  });

  searchBox.addEventListener("input", render);

  document.getElementById("btn-random").addEventListener("click", showRandomEntry);

  // ---------- sheet ----------
  var backdrop = document.getElementById("sheet-backdrop");
  var sheetContent = document.getElementById("sheet-content");

  var sheet = document.getElementById("sheet");

  function openSheet(html, wide) {
    sheetContent.innerHTML = html;
    sheet.classList.toggle("wide", !!wide);
    backdrop.classList.remove("hidden");
  }
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

  var PHOTOS = ["pecoraro5.jpg", "pecoraro2.jpg", "pecoraro1.jpg", "pecoraro3.jpg", "pecoraro4.jpg"];
  var PHOTO_CYCLE_MS = 5000;

  document.getElementById("btn-about").addEventListener("click", function () {
    stopPhotoCycle();
    var idx = 0;
    openSheet(
      "<h2>ⓘ Pecoraro Taroko</h2>" +
      '<img class="about-photo" src="' + PHOTOS[idx] + '" alt="Portrait of Ferdinando Pecoraro MEP">' +
      '<p class="fine photo-caption">Ferdinando Pecoraro MEP</p>' +
      "<p>Based on Ferdinando Pecoraro MEP's <em>Taroko–Français</em> dictionary " +
      "(<em>Essai de dictionnaire taroko-français</em>, SECMI, Paris, 1977).</p>" +
      "<p>本辭典以法國巴黎外方傳教會(MEP)神父 Ferdinando Pecoraro 所編之太魯閣語-法語辭典為基礎。</p>" +
      "<p>English and Chinese translations added from the French; draft, pending review by native speakers.</p>" +
      "<p>“Taroko” is the Japanese-era romanization of the people's own name, Truku, as spoken on Taiwan's east coast (Hualien). Pecoraro writes it “T’roko.”</p>" +
      "<p>「太魯閣」（Taroko）源自日治時期的羅馬拼音，是東台灣（花蓮）太魯閣族自稱「Truku」的另一種轉寫方式。貝科拉羅神父原文寫作「T'roko」。</p>" +
      "<p class=\"fine\">Digitized by Darryl Sterk, Associate Professor of Translation, Lingnan University.</p>" +
      "<p class=\"fine\">" + window.ENTRIES.length + " entries, digitized from all 398 pages</p>"
    );
    photoTimer = setInterval(function () {
      idx = (idx + 1) % PHOTOS.length;
      var img = sheetContent.querySelector(".about-photo");
      if (img) img.src = PHOTOS[idx];
    }, PHOTO_CYCLE_MS);
  });

  var INTRO_GROUPS = [
    { title: "Title Page", zh: "標題頁", pages: [1, 2, 3] },
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
    openSheet(h, true);
  });

  document.getElementById("btn-settings").addEventListener("click", function () {
    var h = "<h2>⚙ Languages · 語言</h2><p class=\"fine\">Choose which translations to show. Truku is always shown. / 選擇顯示的語言,太魯閣語恆顯示。</p>";
    LANGS.forEach(function (l) {
      h += '<label class="lang-option"><input type="checkbox" data-lang="' + l.key + '"' +
        (shown[l.key] ? " checked" : "") + "><span>" + l.label + "</span></label>";
    });
    openSheet(h);
    sheetContent.querySelectorAll("input[data-lang]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        shown[cb.getAttribute("data-lang")] = cb.checked;
        saveLangs();
        render();
      });
    });
  });

  // ---------- init ----------
  document.getElementById("entry-count").textContent = window.ENTRIES.length;
  var params = new URLSearchParams(location.search);
  if (params.get("q")) searchBox.value = params.get("q");
  render();
})();
