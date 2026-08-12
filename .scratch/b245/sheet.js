(function () {
  var K = 'pecoraro_translator_v1';
  // Two answers per word now, so a key is his spelling AND which question it
  // answers: `tbilan|1` is how his word is written today, `tbilan|2` is what
  // is said instead. The bare key is the b243 sheet's, where the two ran
  // together -- MIGRATE2 moves those into the column they actually answered,
  // by the classification printed on the page beside each one (data-prevkind
  // is not consulted: the build already sorted them, and re-deciding it here
  // in the browser would be a second implementation of the same test).
  //
  // A `respell` or `gone` answer is NOT carried over. It is printed on the
  // page, above the boxes, as what he said last time -- putting it back in
  // question one would read as though we had accepted it, and question one is
  // exactly what this sheet is re-asking.
  var MIGRATE2 = MIGRATE2_TABLE;
  // Answers are stored under HIS OWN SPELLING, never under the question
  // number. The first build keyed them on the textarea's id (a1, a2, ...),
  // which is a position: rule one word and every answer below it silently
  // re-attaches to a different question. His spelling is the join key this
  // project already uses everywhere else -- it is what pairs the rendered
  // page back to entries.js for the audio wiring, for the same reason.
  //
  // The FIRST published sheet's own id -> word table (qset 91aca4f). A fixed
  // historical fact, kept so that anyone who answered THAT sheet still keeps
  // their answers: positional key -> his spelling -> the column below.
  var MIGRATE = {a1:"ksudan",a2:"mqlaq",a3:"tbilan",a4:"gaqat",a5:"gnl'qan",a6:"loai",a7:"ptatwi",a8:"qadi",a9:"sl'xqon",a10:"tibasyaq",a11:"ayoq",a12:"dmbasyaq",a13:"mpxlakux",a14:"mpslangan",a15:"glaqon",a16:"xbugi",a17:"xlakux",a18:"kaxoi",a19:"kakox",a20:"kkakox",a21:"kndoto",a22:"knxgun",a23:"kyoqan",a24:"lg'loq",a25:"mkaxoi",a26:"mngusyex",a27:"mslangan",a28:"msyuling",a29:"mtmago",a30:"mtmoxong",a31:"nalong",a32:"nkl\"lu",a33:"nplikut",a34:"pg'go",a35:"pnnano",a36:"pnngoan",a37:"pnlngut",a38:"pnslngiyan",a39:"plngut",a40:"psqgo",a41:"qlap",a42:"qlaq",a43:"q'loq",a44:"qnadi",a45:"qntq'dan",a46:"likut",a47:"lmngut",a48:"lngiyan",a49:"lngutan",a50:"sape",a51:"sdangan",a52:"sxmqan",a53:"sm",a54:"sm'mul",a55:"sn'mul",a56:"snoqo",a57:"snxelan",a58:"sqlaq",a59:"sloweq",a60:"syuling",a61:"tbiyun",a62:"teumuk",a63:"tnbian",a64:"tnlikut",a65:"ubai",a66:"ulang",a67:"yiano",a68:"dmt'basyaq",a69:"dmt'sapat",a70:"klikut",a71:"nlikut",a72:"snuk",a73:"tbasyaq",a74:"txey"};
  // The build stamp, the question-set digest and the return
  // address ride on `.sheet`: the page is published inside a
  // <body> this file does not write, so there is no body
  // attribute to hang them on.
  var META = document.querySelector('.sheet').dataset;
  // Only the ANSWER boxes. `#out` is a textarea too, and counting it would
  // report 75 questions and put the summary inside its own summary.
  var T = [].slice.call(document.querySelectorAll('.answer textarea'));
  var out = document.getElementById('out');
  var msg = document.getElementById('msg');
  var saved = {}, storable = true;

  // Whether storage WORKS, not whether the API exists: a private window and
  // several in-app browsers expose localStorage and throw on write. Nothing
  // else on this page could tell them their afternoon's work will vanish.
  try {
    localStorage.setItem(K + '_t', '1');
    localStorage.removeItem(K + '_t');
    saved = JSON.parse(localStorage.getItem(K) || '{}');
    // Two one-time moves, in the order the sheets were published: positional
    // key -> his spelling (never by position), then his spelling -> the
    // question that answer actually belonged to. Both are idempotent, and a
    // key already carrying a `|` is left alone, so re-opening this page does
    // not re-migrate what it migrated last time.
    var moved = {}, old = 0, two = 0;
    Object.keys(saved).forEach(function (k) {
      if (/^a\d+$/.test(k)) { old++; if (MIGRATE[k]) moved[MIGRATE[k]] = saved[k]; }
      else moved[k] = saved[k];
    });
    var moved2 = {};
    Object.keys(moved).forEach(function (k) {
      if (k.indexOf('|') >= 0) { moved2[k] = moved[k]; return; }
      two++;
      if (MIGRATE2[k]) moved2[k + '|' + MIGRATE2[k]] = moved[k];
    });
    if (old || two) {
      saved = moved2;
      localStorage.setItem(K, JSON.stringify(saved));
    }
  } catch (e) { storable = false; }

  function say(s) { msg.textContent = s || ''; }

  // The two boxes of one word, by question number. Built from the DOM rather
  // than from the numbering, so a build that ever emits a word with only one
  // of the two still groups correctly instead of pairing across rows.
  function pair(item) {
    var q = {};
    [].slice.call(item.querySelectorAll('.answer textarea')).forEach(
      function (t) { q[t.dataset.q] = t; });
    return q;
  }
  var ITEMS = [].slice.call(document.querySelectorAll('.q-item'))
    .filter(function (i) { return i.querySelector('.answer textarea'); });

  function text() {
    // The returned sheet must keep the two questions apart on the page too --
    // if it comes back as one list of words, the adjudication is back to
    // guessing which question each line answered, which is the whole fault
    // this build exists to remove. One block per word, each answer labelled.
    var L = [], n1 = 0, n2 = 0;
    ITEMS.forEach(function (it) {
      var q = pair(it), a = q['1'], b = q['2'];
      var v1 = a ? a.value.trim() : '', v2 = b ? b.value.trim() : '';
      if (!v1 && !v2) return;
      if (v1) n1++;
      if (v2) n2++;
      var t = a || b;
      // Number, his word, our guess only where it differs. The number lets a
      // reply be matched back even if a later build renumbers the sheet —
      // that is what the 題組 digest in the header is for.
      L.push(t.dataset.n + '. ' + t.dataset.his
             + ((a && a.dataset.w) ? '（暫定 ' + a.dataset.w + '）' : ''));
      if (v1) L.push('    問一 今天怎麼寫：' + v1.replace(/\s+/g, ' '));
      if (v2) L.push('    問二 今天怎麼說：' + v2.replace(/\s+/g, ' '));
    });
    if (!n1 && !n2) return '';
    return '太魯閣語現代拼寫請教單（分兩題）— 回答\n'
         + '問一 ' + n1 + ' 條 · 問二 ' + n2 + ' 條 · 全部 ' + ITEMS.length
         + ' 個詞\n'
         + '版本 ' + META.build
         + ' · 題組 ' + META.qset + '\n\n'
         + L.join('\n');
  }

  function refresh() {
    var n1 = 0, n2 = 0;
    ITEMS.forEach(function (it) {
      var q = pair(it);
      var f1 = !!(q['1'] && q['1'].value.trim());
      var f2 = !!(q['2'] && q['2'].value.trim());
      if (f1) n1++;
      if (f2) n2++;
      // Only 問一 marks a row done: 問二 is recorded and never spells his
      // page, so a row carrying only that answer is still a row we are
      // asking about, and gets its own quieter mark.
      it.classList.toggle('done', f1);
      it.classList.toggle('part', !f1 && f2);
    });
    document.getElementById('cnt').innerHTML =
      '問一 <b>' + n1 + '</b> / ' + ITEMS.length
      + '　·　問二 <b>' + n2 + '</b>';
    out.value = text() || '（還沒有填任何一條。填好的答案會自動出現在這裡。）';
  }

  function grow(t) {
    t.style.height = 'auto';
    t.style.height = (t.scrollHeight + 2) + 'px';
  }

  // his spelling AND the question number, unless the build ever emits that
  // pair twice -- then the row number is appended, so a duplicate degrades to
  // positional for that pair alone rather than making two boxes share one
  // answer. The build asserts uniqueness of his spelling as well; this is the
  // belt to that braces.
  var HIS = {};
  T.forEach(function (t) {
    var b = t.dataset.his + '|' + t.dataset.q;
    HIS[b] = (HIS[b] || 0) + 1;
  });
  function key(t) {
    var b = t.dataset.his + '|' + t.dataset.q;
    return HIS[b] > 1 ? b + '~' + t.dataset.n : b;
  }

  function save() {
    var o = {};
    T.forEach(function (t) { if (t.value.trim()) o[key(t)] = t.value; });
    try { localStorage.setItem(K, JSON.stringify(o)); } catch (e) {}
    refresh();
  }

  T.forEach(function (t) {
    if (saved[key(t)]) t.value = saved[key(t)];
    t.addEventListener('input', function () { save(); grow(t); });
    if (t.value) grow(t);
  });
  refresh();

  if (!storable) {
    var w = document.createElement('p');
    w.className = 'warn';
    w.innerHTML = '<b>注意：</b>這個瀏覽器不會幫您保存進度'
      + '（可能是無痕視窗，或是從別的 App 裡面開啟的）。'
      + '關掉這一頁，填過的內容就會不見 — 請一次填完，'
      + '並且<b>馬上用最下面的方式回傳</b>。';
    document.querySelector('.intro').appendChild(w);
  }
  window.addEventListener('beforeunload', function (e) {
    if (!storable && text()) { e.preventDefault(); e.returnValue = ''; }
  });

  document.getElementById('next').addEventListener('click', function () {
    // 問一 first, everywhere, before any 問二 -- the button is how a reader
    // walks the sheet, and walking it question-by-question would spend the
    // afternoon on the column that cannot spell his page.
    var t = T.filter(function (x) {
      return x.dataset.q === '1' && !x.value.trim();
    })[0] || T.filter(function (x) { return !x.value.trim(); })[0];
    if (!t) {
      document.getElementById('send').scrollIntoView({ block: 'start' });
      say('全部都填完了，可以回傳了。');
      return;
    }
    t.closest('.q-item').scrollIntoView({ block: 'start' });
    t.focus();
  });

  document.getElementById('go').addEventListener('click', function () {
    document.getElementById('send').scrollIntoView({ block: 'start' });
  });

  document.getElementById('sel').addEventListener('click', function () {
    if (!text()) { say('還沒有填任何一條。'); return; }
    out.focus();
    out.setSelectionRange(0, out.value.length);
    say('已經全部選起來了 — 現在按 Ctrl+C（手機請長按，選「複製」）。');
  });

  document.getElementById('copy').addEventListener('click', function () {
    var s = text();
    if (!s) { say('還沒有填任何一條。'); return; }
    // Three rungs, because the top one is blocked in exactly the browsers a
    // shared link tends to open in: the async clipboard, then the legacy
    // command, then the text selected and the reader told to copy it.
    function fell() {
      out.focus();
      out.setSelectionRange(0, out.value.length);
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      say(ok ? '已複製，貼到訊息或電子郵件裡寄給我們就好。'
             : '這個瀏覽器不讓網頁自己複製 — 上面的字已經幫您選起來了，'
               + '請手動複製（Ctrl+C，手機請長按選「複製」）。');
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(s).then(function () {
        say('已複製，貼到訊息或電子郵件裡寄給我們就好。');
      }, fell);
    } else { fell(); }
  });

  document.getElementById('mail').addEventListener('click', function () {
    var s = text();
    if (!s) { say('還沒有填任何一條。'); return; }
    // A mailto body is length-capped by the OS and the mail client, and the
    // failure is silent truncation, which would lose answers without saying
    // so. Past the cap the letter opens empty and says to paste.
    var big = s.length > 1200;
    var body = big ? '（回答比較長，請把網頁上那一格的內容貼在這裡。）\n\n' : s;
    location.href = 'mailto:' + META.mail
      + '?subject=' + encodeURIComponent('太魯閣語現代拼寫 — 回答')
      + '&body=' + encodeURIComponent(body);
    say(big ? '信件開好了，但內容太長沒辦法自動帶入 — 請先按「複製」再貼進信裡。'
            : '信件開好了，直接寄出就可以。');
  });

  var dl = document.getElementById('dl');
  if (window.claude && window.claude.downloads) {
    dl.hidden = false;
    dl.addEventListener('click', function () {
      var s = text();
      if (!s) { say('還沒有填任何一條。'); return; }
      window.claude.downloads.save({
        filename: 'taroko-answers.txt', data: s
      }).then(function () {
        say('檔案存好了，把它附在信裡寄給我們就行。');
      }, function (e) {
        say(e && e.code === 'declined' ? '沒有存檔。'
                                       : '存檔失敗 — 請改用「複製」或「全選」。');
      });
    });
  }

  document.getElementById('clr').addEventListener('click', function () {
    if (!text()) { say('本來就是空的。'); return; }
    var n = T.filter(function (t) { return t.value.trim(); }).length;
    if (!confirm('確定要清除全部 ' + n + ' 條回答嗎？這個動作沒辦法復原。')) return;
    T.forEach(function (t) { t.value = ''; t.style.height = 'auto'; });
    save();
    say('已清除。');
  });
})();
