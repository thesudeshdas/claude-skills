/* research docs: shared behaviour for every /research page.
 * Loaded in <head> without defer so the saved theme applies before paint.
 * Builds the topbar, toc, progress bar, copy buttons, doc switcher and
 * newer/older links, so docs only carry their content. No animation beyond
 * CSS transitions. */
(function () {
  var KEY = "research-theme";
  var root = document.documentElement;
  var BASE = ((document.currentScript || {}).src || "").replace(/[^/]*$/, "");

  function saved() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function apply(mode) {
    if (mode === "light" || mode === "dark") root.setAttribute("data-theme", mode);
    else root.removeAttribute("data-theme");
  }
  apply(saved());

  function slug(text) {
    return text.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section";
  }

  function topbar() {
    var bar = document.createElement("header");
    bar.className = "topbar";
    var title = document.title || "";
    var type = (document.querySelector('meta[name="research:type"]') || {}).content || "";
    bar.innerHTML =
      '<div class="wrap">' +
      '<nav class="crumb"><a href="index.html">research</a><span class="sep">/</span>' +
      (type ? '<span class="type" data-type="' + type + '">' + type + "</span>" : "") +
      '<span class="here"></span></nav>' +
      '<div class="bar-right">' +
      '<div class="doc-switch"><button type="button" class="doc-switch-btn" aria-expanded="false" aria-haspopup="true" title="other research (press /)">' +
      'docs <span aria-hidden="true">▾</span></button></div>' +
      '<div class="theme-toggle" role="group" aria-label="theme">' +
      '<button data-mode="system">auto</button><button data-mode="light">light</button><button data-mode="dark">dark</button>' +
      "</div></div></div>";
    bar.querySelector(".here").textContent = document.querySelector("main.content") ? title : "";
    document.body.prepend(bar);

    var progress = document.createElement("div");
    progress.className = "progress";
    progress.innerHTML = "<span></span>";
    document.body.prepend(progress);

    var buttons = bar.querySelectorAll(".theme-toggle button");
    function sync() {
      var cur = saved() || "system";
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.mode === cur)); });
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var mode = b.dataset.mode;
        try {
          if (mode === "system") localStorage.removeItem(KEY);
          else localStorage.setItem(KEY, mode);
        } catch (e) {}
        apply(mode);
        sync();
      });
    });
    sync();

    var fill = progress.firstChild;
    function onScroll() {
      var max = document.documentElement.scrollHeight - innerHeight;
      fill.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + "%";
    }
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  function toc() {
    var nav = document.querySelector("nav.toc");
    var heads = document.querySelectorAll("section.block > h2, section.block > .sec-head h2");
    if (!heads.length) { if (nav) nav.remove(); return; }
    var used = {};
    var list = document.createElement("ol");
    var links = [];
    heads.forEach(function (h) {
      var sec = h.closest("section");
      if (!sec.id) {
        var id = slug(h.textContent), n = id, i = 2;
        while (used[n] || document.getElementById(n)) n = id + "-" + i++;
        sec.id = n;
      }
      used[sec.id] = true;
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + sec.id;
      a.textContent = h.dataset.toc || h.textContent;
      li.appendChild(a);
      list.appendChild(li);
      links.push({ a: a, sec: sec });
    });
    if (!nav) return;
    nav.innerHTML = '<span class="eyebrow">on this page</span>';
    nav.appendChild(list);

    if (!("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) { l.a.classList.toggle("active", l.sec === e.target); });
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    links.forEach(function (l) { io.observe(l.sec); });
  }

  function copyButtons() {
    document.querySelectorAll("pre").forEach(function (pre) {
      var btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.type = "button";
      btn.textContent = "copy";
      btn.addEventListener("click", function () {
        var text = (pre.querySelector("code") || pre).innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = "copied";
          setTimeout(function () { btn.textContent = "copy"; }, 1200);
        });
      });
      pre.appendChild(btn);
    });
  }

  function footer() {
    if (document.querySelector(".foot") || !document.querySelector("main.content")) return;
    var created = (document.querySelector('meta[name="research:date"]') || {}).content || "";
    var f = document.createElement("footer");
    f.className = "foot wrap";
    f.innerHTML = '<span><a href="index.html">all research</a></span><span class="mono"></span>';
    f.lastChild.textContent = created;
    document.body.appendChild(f);
  }

  /* ---------- other research ----------
   * _assets/docs.js (written by index.py) lists every doc. Loaded as a
   * script so it works from file:// as well as the local server. */
  function loadDocs(done) {
    if (window.RESEARCH_DOCS) return done(window.RESEARCH_DOCS);
    var s = document.createElement("script");
    s.src = BASE + "docs.js?v=" + Date.now();
    s.onload = function () { done(window.RESEARCH_DOCS || []); };
    s.onerror = function () { done([]); };
    document.head.appendChild(s);
  }

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  function here() {
    return decodeURIComponent(location.pathname.split("/").pop() || "index.html");
  }

  function docSwitcher(docs) {
    var wrap = document.querySelector(".doc-switch");
    if (!wrap) return;
    var btn = wrap.querySelector(".doc-switch-btn");
    var cur = here();
    var menu = document.createElement("div");
    menu.className = "doc-menu";
    menu.hidden = true;
    menu.innerHTML =
      '<input type="search" class="doc-search" placeholder="find research" aria-label="find research">' +
      '<div class="doc-list" role="list"></div>' +
      '<a class="doc-all" href="index.html">all research →</a>';
    wrap.appendChild(menu);
    var input = menu.querySelector("input"), list = menu.querySelector(".doc-list");

    function draw(filter) {
      var f = (filter || "").toLowerCase().trim();
      var hits = docs.filter(function (d) {
        return !f || (d.title + " " + d.type + " " + d.project + " " + d.date).toLowerCase().indexOf(f) > -1;
      });
      list.innerHTML = hits.length ? hits.map(function (d) {
        return '<a role="listitem" href="' + esc(d.file) + '"' + (d.file === cur ? ' aria-current="page"' : "") + ">" +
          '<span class="doc-title">' + esc(d.title) + "</span>" +
          '<span class="doc-meta"><span class="type" data-type="' + esc(d.type) + '">' + esc(d.type) + "</span>" +
          "<span>" + esc(d.date) + "</span>" + (d.project ? "<span>" + esc(d.project) + "</span>" : "") + "</span></a>";
      }).join("") : '<p class="muted doc-empty">' + (docs.length ? "no match" : "no doc list yet, run index.py") + "</p>";
    }
    function show(open) {
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      if (open) { input.value = ""; draw(""); input.focus(); }
    }
    btn.addEventListener("click", function () { show(menu.hidden); });
    input.addEventListener("input", function () { draw(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { var a = list.querySelector("a:not([aria-current])"); if (a) location.href = a.href; }
      if (e.key === "ArrowDown") { e.preventDefault(); var first = list.querySelector("a"); if (first) first.focus(); }
    });
    list.addEventListener("keydown", function (e) {
      var a = document.activeElement;
      if (e.key === "ArrowDown" && a.nextElementSibling) { e.preventDefault(); a.nextElementSibling.focus(); }
      if (e.key === "ArrowUp") { e.preventDefault(); (a.previousElementSibling || input).focus(); }
    });
    document.addEventListener("click", function (e) { if (!wrap.contains(e.target)) show(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { show(false); btn.focus(); }
      var t = e.target.tagName;
      if (e.key === "/" && t !== "INPUT" && t !== "TEXTAREA" && !e.metaKey && !e.ctrlKey) { e.preventDefault(); show(true); }
    });
  }

  function docNav(docs) {
    var main = document.querySelector("main.content");
    if (!main) return;
    var cur = here(), i = -1;
    docs.forEach(function (d, n) { if (d.file === cur) i = n; });
    if (i < 0) return;
    var newer = docs[i - 1], older = docs[i + 1];
    if (!newer && !older) return;
    function card(d, label, cls) {
      return '<a class="card ' + cls + '" href="' + esc(d.file) + '"><span class="eyebrow">' + label + "</span>" +
        "<h3>" + esc(d.title) + '</h3><span class="meta"><span class="type" data-type="' + esc(d.type) + '">' +
        esc(d.type) + '</span><span class="chip">' + esc(d.date) + "</span></span></a>";
    }
    var nav = document.createElement("nav");
    nav.className = "doc-nav";
    nav.setAttribute("aria-label", "more research");
    nav.innerHTML = (newer ? card(newer, "← newer", "newer") : "") + (older ? card(older, "older →", "older") : "");
    main.appendChild(nav);
  }


  /* ---------- mark and ask ----------
   * Select text → "ask about this" → the question goes to the local research
   * server, and the claude session that wrote this doc (watching via
   * Monitor) answers it. Answers show up in the panel. Opened from file://
   * (no server), the question is copied as a prompt to paste instead. */
  function ask() {
    var main = document.querySelector("main.content");
    if (!main) return;
    var doc = location.pathname.split("/").pop();
    var live = location.protocol.indexOf("http") === 0;
    var thread = [], pollTimer = null, quote = "", section = "";

    function esc(t) {
      return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
    }
    function rich(t) {
      return esc(t).split(/\n{2,}/).map(function (p) {
        return "<p>" + p.replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>") + "</p>";
      }).join("");
    }

    var pop = document.createElement("button");
    pop.type = "button";
    pop.className = "ask-pop";
    pop.textContent = "ask about this";
    pop.hidden = true;
    document.body.appendChild(pop);

    var fab = document.createElement("button");
    fab.type = "button";
    fab.className = "ask-fab";
    fab.innerHTML = '<span>ask</span><b hidden></b>';
    document.body.appendChild(fab);

    var panel = document.createElement("aside");
    panel.className = "ask-panel";
    panel.hidden = true;
    panel.innerHTML =
      '<div class="ask-head"><span class="eyebrow">ask claude</span><span class="ask-status"></span>' +
      '<button type="button" class="ask-close" aria-label="close">×</button></div>' +
      '<div class="ask-thread"></div>' +
      '<form class="ask-form"><blockquote class="ask-quote" hidden></blockquote>' +
      '<textarea rows="3" placeholder="ask anything about this doc"></textarea>' +
      '<div class="ask-row"><span class="muted ask-hint"></span><button type="submit" class="ask-send">send</button></div></form>';
    document.body.appendChild(panel);

    var q = function (sel) { return panel.querySelector(sel); };
    var box = q("textarea"), quoteEl = q(".ask-quote"), list = q(".ask-thread"), status = q(".ask-status"), hint = q(".ask-hint");
    hint.textContent = live ? "goes to the claude session that wrote this" : "opened as a file, so it's copied for you to paste";

    function sectionOf(node) {
      var sec = node && (node.nodeType === 1 ? node : node.parentElement);
      sec = sec && sec.closest("section");
      var h = sec && sec.querySelector("h2");
      return h ? h.textContent.trim() : "";
    }

    document.addEventListener("mouseup", function (e) {
      if (panel.contains(e.target) || e.target === pop) return;
      setTimeout(function () {
        var sel = getSelection();
        var text = sel && String(sel).trim();
        if (!text || text.length < 3 || !main.contains(sel.anchorNode)) { pop.hidden = true; return; }
        var r = sel.getRangeAt(0).getBoundingClientRect();
        pop.style.top = (scrollY + r.bottom + 8) + "px";
        pop.style.left = Math.max(8, Math.min(scrollX + r.left + r.width / 2 - 60, innerWidth - 140)) + "px";
        pop.hidden = false;
        pop.dataset.quote = text.slice(0, 2000);
        pop.dataset.section = sectionOf(sel.anchorNode);
      }, 0);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { pop.hidden = true; panel.hidden = true; }
    });

    function open(withQuote, withSection) {
      quote = withQuote || "";
      section = withSection || "";
      quoteEl.hidden = !quote;
      quoteEl.textContent = quote;
      panel.hidden = false;
      pop.hidden = true;
      box.focus();
      if (live) refresh();
    }
    pop.addEventListener("mousedown", function (e) { e.preventDefault(); });
    pop.addEventListener("click", function () { open(pop.dataset.quote, pop.dataset.section); });
    fab.addEventListener("click", function () { panel.hidden ? open("", "") : (panel.hidden = true); });
    q(".ask-close").addEventListener("click", function () { panel.hidden = true; });
    box.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) q(".ask-form").requestSubmit();
    });

    function render(listening) {
      status.textContent = live ? (listening ? "session listening" : "no session listening, it'll wait") : "";
      status.className = "ask-status " + (listening ? "on" : "off");
      list.innerHTML = thread.map(function (t) {
        return '<div class="ask-item">' +
          (t.quote ? '<blockquote class="ask-quote">' + esc(t.quote) + "</blockquote>" : "") +
          '<p class="ask-q">' + esc(t.question) + "</p>" +
          (t.answer ? '<div class="ask-a">' + rich(t.answer) + "</div>" : '<p class="ask-wait">waiting for claude…</p>') +
          "</div>";
      }).join("");
      var pending = thread.filter(function (t) { return !t.answer; }).length;
      var badge = fab.querySelector("b");
      badge.hidden = !pending;
      badge.textContent = pending;
      list.scrollTop = list.scrollHeight;
      clearTimeout(pollTimer);
      if (pending || !panel.hidden) pollTimer = setTimeout(refresh, pending ? 2500 : 8000);
    }
    function refresh() {
      fetch("/api/thread?doc=" + encodeURIComponent(doc)).then(function (r) { return r.json(); }).then(function (d) {
        thread = d.thread || [];
        render(d.listening);
      }).catch(function () { status.textContent = "server is off"; status.className = "ask-status off"; });
    }

    q(".ask-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var question = box.value.trim();
      if (!question) return;
      if (!live) {
        var prompt = 'question about my research doc "' + document.title + '" (~/research/' + doc + ")" +
          (section ? ", section: " + section : "") + "\n\n" + (quote ? "> " + quote.replace(/\n/g, "\n> ") + "\n\n" : "") + question;
        navigator.clipboard.writeText(prompt).then(function () { hint.textContent = "copied. paste it into the claude session"; });
        return;
      }
      var send = q(".ask-send");
      send.disabled = true;
      fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc: doc, section: section, quote: quote, question: question })
      }).then(function (r) { return r.json(); }).then(function () {
        box.value = ""; quote = ""; section = ""; quoteEl.hidden = true;
        refresh();
      }).catch(function () { hint.textContent = "couldn't reach the server. ask claude to reopen the doc"; })
        .then(function () { send.disabled = false; });
    });

    if (live) refresh();
  }

  document.addEventListener("DOMContentLoaded", function () {
    topbar();
    toc();
    copyButtons();
    footer();
    ask();
    loadDocs(function (docs) {
      docSwitcher(docs);
      docNav(docs);
    });
  });
})();
