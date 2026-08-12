// Shows a "this is the old site, we moved" notice when NOT on the new
// *.shidailun.com Cloudflare domain (i.e. still on the legacy Netlify site,
// or a Netlify deploy preview). Silent on shidailun.com and on local dev.
// New-site host comes from this <script>'s data-new-host attribute so this
// file is byte-identical across every migrated app.
(function () {
  var h = location.hostname;
  var local = h === "localhost" || h === "127.0.0.1" || h === "::1" || h === "" ||
              h.indexOf("192.168.") === 0 || h.indexOf("10.") === 0;
  if (local || h.indexOf(".shidailun.com") !== -1) return;
  var newHost = document.currentScript && document.currentScript.getAttribute("data-new-host");
  if (!newHost) return;

  var bar = document.createElement("div");
  bar.style.cssText =
    "background:#2f2a25;color:#f4f1ec;font:13px/1.6 system-ui,-apple-system,'Noto Sans TC'," +
    "'PingFang TC','Microsoft JhengHei',sans-serif;text-align:center;padding:10px 14px;";
  bar.appendChild(document.createTextNode("這是舊版網站，內容不會再更新。"));
  var a = document.createElement("a");
  a.href = "https://" + newHost + "/";
  a.textContent = "前往新版 →";
  a.style.cssText = "color:#ffd54a;text-decoration:underline;font-weight:700;margin-left:6px;";
  bar.appendChild(a);
  document.body.insertBefore(bar, document.body.firstChild);
})();
