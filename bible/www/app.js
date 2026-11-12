(function () {
  var data = window.KRV;
  if (!data) return;

  var books = data.books;
  var byId = {};
  books.forEach(function (book, index) {
    book.index = index;
    byId[book.i] = book;
  });

  var titleEl = document.getElementById("title");
  var readEl = document.getElementById("read");
  var prevBtn = document.getElementById("prev");
  var nextBtn = document.getElementById("next");
  var sheet = document.getElementById("sheet");
  var sheetTitle = document.getElementById("sheet-title");
  var sheetBody = document.getElementById("sheet-body");
  var currentName = "books";
  var place = loadPlace();

  function loadPlace() {
    var boot = window.KRV_BOOT;
    var place = { v: data.v, id: boot.id, ch: boot.ch, verse: "" };
    try {
      var saved = JSON.parse(localStorage.getItem("krv") || "null");
      if (saved && saved.v === data.v && byId[saved.id]) place = saved;
    } catch (e) {}
    return place;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function chapterHtml(verses) {
    return verses.map(function (verse) {
      return '<p class="v" id="v-' + verse.n + '"><sup>' + escapeHtml(verse.n) + "</sup>" + escapeHtml(verse.t) + "</p>";
    }).join("");
  }

  function showChapter(id, chapter, verse) {
    var book = byId[id];
    var verses = book.c[chapter - 1];
    place = {
      v: data.v,
      id: id,
      ch: chapter,
      verse: verse || "",
      title: book.n + " " + chapter + "장",
      html: chapterHtml(verses)
    };
    titleEl.textContent = place.title;
    readEl.innerHTML = place.html;
    document.title = place.title + " · 개역한글";
    var prevBook = chapter === 1 ? books[book.index - 1] : book;
    var nextBook = chapter === book.c.length ? books[book.index + 1] : book;
    prevBtn.disabled = !prevBook;
    nextBtn.disabled = !nextBook;
    try { localStorage.setItem("krv", JSON.stringify(place)); } catch (e) {}
    if (verse) {
      var el = document.getElementById("v-" + verse);
      if (el) {
        el.classList.add("here");
        var top = el.getBoundingClientRect().top + window.pageYOffset - document.querySelector(".bar").offsetHeight - 8;
        window.scrollTo(0, top);
      }
    } else {
      readEl.scrollTop = 0;
      window.scrollTo(0, 0);
    }
    closeSheet();
  }

  function step(dir) {
    var book = byId[place.id];
    var chapter = place.ch + dir;
    if (chapter >= 1 && chapter <= book.c.length) {
      showChapter(book.i, chapter, "");
      return;
    }
    var neighbor = books[book.index + dir];
    if (!neighbor) return;
    showChapter(neighbor.i, dir < 0 ? neighbor.c.length : 1, "");
  }

  function openSheet(name) {
    currentName = name;
    sheet.hidden = false;
    document.querySelectorAll(".tabs button").forEach(function (button) {
      button.setAttribute("aria-current", button.dataset.sheet === name ? "true" : "false");
    });
    if (name === "books") renderBooks();
    if (name === "search") renderSearch();
    if (name === "type") renderType();
    if (name === "about") renderAbout();
    var focus = sheetBody.querySelector("input, button");
    if (focus) focus.focus();
  }

  function closeSheet() {
    sheet.hidden = true;
    currentName = "";
    document.querySelectorAll(".tabs button").forEach(function (button) {
      button.setAttribute("aria-current", "false");
    });
  }

  function renderBooks() {
    sheetTitle.textContent = "책";
    var html = "";
    var group = "";
    books.forEach(function (book) {
      if (book.g !== group) {
        group = book.g;
        html += '<p class="group-label">' + group + "</p><div class=\"books\">";
      }
      var current = book.i === place.id ? ' aria-current="true"' : "";
      html += '<button type="button" data-book="' + book.i + '"' + current + ">" + book.n + "</button>";
      var next = books[book.index + 1];
      if (!next || next.g !== group) html += "</div>";
    });
    sheetBody.innerHTML = html;
  }

  function renderChapters(id) {
    var book = byId[id];
    sheetTitle.textContent = book.n;
    var html = '<p><button type="button" class="back-books">책 목록</button></p><div class="chapters">';
    for (var i = 1; i <= book.c.length; i++) {
      var current = book.i === place.id && i === place.ch ? ' aria-current="true"' : "";
      html += '<button type="button" data-ch="' + i + '"' + current + ">" + i + "</button>";
    }
    html += "</div>";
    sheetBody.innerHTML = html;
    sheetBody.dataset.book = id;
  }

  function renderSearch() {
    sheetTitle.textContent = "찾기";
    sheetBody.innerHTML = '<form class="search"><input id="q" type="search" placeholder="창 1:1 또는 단어" enterkeyhint="search" autocomplete="off"><button type="submit">찾기</button></form><div id="hits"><p class="hint">책 이름과 장, 절을 적거나 본문 단어를 적습니다.</p></div>';
    sheetBody.querySelector("form").addEventListener("submit", function (event) {
      event.preventDefault();
      runSearch(sheetBody.querySelector("#q").value);
    });
  }

  function namesOf(book) {
    var names = [book.n, book.a, book.i];
    (book.k || []).forEach(function (name) { names.push(name); });
    return names;
  }

  function findBook(token) {
    var query = token.replace(/\s+/g, "");
    var found = null;
    books.forEach(function (book) {
      namesOf(book).forEach(function (name) {
        if (name.replace(/\s+/g, "") === query) found = book;
      });
    });
    return found;
  }

  function runSearch(raw) {
    var query = raw.trim();
    var hits = document.getElementById("hits");
    if (!query) {
      hits.innerHTML = '<p class="hint">책 이름과 장, 절을 적거나 본문 단어를 적습니다.</p>';
      return;
    }
    var ref = query.match(/^(.+?)\s*(\d+)\s*(?:장)?\s*[:：.]\s*(\d+)\s*절?$/);
    var chapterOnly = query.match(/^(.+?)\s*(\d+)\s*장?$/);
    if (ref || chapterOnly) {
      var parts = ref || chapterOnly;
      var book = findBook(parts[1]);
      if (book) {
        var chapter = Number(parts[2]);
        var verse = ref ? parts[3] : "";
        if (chapter >= 1 && chapter <= book.c.length) {
          showChapter(book.i, chapter, verse);
          return;
        }
      }
    }
    var needle = query.replace(/\s+/g, "");
    var rows = [];
    for (var b = 0; b < books.length && rows.length < 40; b++) {
      var bookItem = books[b];
      for (var c = 0; c < bookItem.c.length && rows.length < 40; c++) {
        var verses = bookItem.c[c];
        for (var v = 0; v < verses.length; v++) {
          if (verses[v].t === "(없음)") continue;
          if (verses[v].t.replace(/\s+/g, "").indexOf(needle) !== -1) {
            rows.push({ book: bookItem, ch: c + 1, verse: verses[v] });
            if (rows.length === 40) break;
          }
        }
      }
    }
    if (!rows.length) {
      hits.innerHTML = '<p class="hint">찾지 못했습니다.</p>';
      return;
    }
    hits.innerHTML = rows.map(function (row) {
      return '<button type="button" class="hit" data-id="' + row.book.i + '" data-ch="' + row.ch + '" data-v="' + row.verse.n + '"><b>' +
        row.book.a + " " + row.ch + ":" + row.verse.n + "</b>" + escapeHtml(row.verse.t) + "</button>";
    }).join("");
  }

  function renderType() {
    sheetTitle.textContent = "글자";
    var current = getComputedStyle(document.documentElement).getPropertyValue("--size").trim();
    var sizes = ["18", "21", "25", "30"];
    var labels = ["작게", "보통", "크게", "아주 크게"];
    sheetBody.innerHTML = '<div class="sizes">' + sizes.map(function (size, index) {
      var on = current.indexOf(size) === 0 ? ' aria-current="true"' : "";
      return '<button type="button" data-size="' + size + '"' + on + ">" + labels[index] + "</button>";
    }).join("") + "</div>";
  }

  function renderAbout() {
    sheetTitle.textContent = "안내";
    sheetBody.innerHTML = [
      "<div class=\"about\">",
      "<p>앱을 열면 지난번에 읽던 장이 나옵니다. 처음에는 창세기 1장입니다. 읽던 위치와 글자 크기는 이 기기에만 남습니다.</p>",
      "<h3>본문</h3>",
      "<p>성경전서 개역한글판. 대한성서공회, 1961년 7월 10일 발행. 저작재산권 보호기간은 2011년 12월 31일에 끝났습니다. 본문의 철자와 절 번호는 바꾸지 않았습니다.</p>",
      "<p>난외주와 소제목은 넣지 않았습니다. 원문에서 절이 붙어 있으면 번호도 「1-2」처럼 붙어 있고, 본문이 없는 절은 「(없음)」으로 나타납니다.</p>",
      "<h3>개인정보</h3>",
      "<p>계정을 만들지 않습니다. 개발자에게 읽기 기록이 전송되지 않습니다. 광고와 결제가 없습니다.</p>",
      "<p>문의 ceo@stargateedu.co.kr · 주식회사 별의문</p>",
      "</div>"
    ].join("");
  }

  prevBtn.addEventListener("click", function () { step(-1); });
  nextBtn.addEventListener("click", function () { step(1); });
  document.getElementById("open-books").addEventListener("click", function () { openSheet("books"); });
  document.getElementById("open-search").addEventListener("click", function () { openSheet("search"); });
  document.getElementById("open-type").addEventListener("click", function () { openSheet("type"); });
  document.getElementById("open-about").addEventListener("click", function () { openSheet("about"); });
  document.getElementById("close-sheet").addEventListener("click", closeSheet);

  sheetBody.addEventListener("click", function (event) {
    var bookBtn = event.target.closest("[data-book]");
    if (bookBtn && !event.target.closest("[data-ch]")) {
      var chosen = byId[bookBtn.dataset.book];
      if (chosen.c.length === 1) showChapter(chosen.i, 1, "");
      else renderChapters(chosen.i);
      return;
    }
    var chapterBtn = event.target.closest("[data-ch]");
    if (chapterBtn) {
      showChapter(sheetBody.dataset.book, Number(chapterBtn.dataset.ch), "");
      return;
    }
    if (event.target.closest(".back-books")) renderBooks();
    var sizeBtn = event.target.closest("[data-size]");
    if (sizeBtn) {
      var size = sizeBtn.dataset.size;
      document.documentElement.style.setProperty("--size", size + "px");
      try { localStorage.setItem("krv-size", size); } catch (e) {}
      renderType();
    }
    var hit = event.target.closest(".hit");
    if (hit) showChapter(hit.dataset.id, Number(hit.dataset.ch), hit.dataset.v);
  });

  window.bibleBack = function () {
    if (!sheet.hidden) {
      closeSheet();
      return true;
    }
    return false;
  };

  var book = byId[place.id];
  prevBtn.disabled = place.ch === 1 && book.index === 0;
  nextBtn.disabled = place.ch === book.c.length && book.index === books.length - 1;
  document.title = (place.title || titleEl.textContent) + " · 개역한글";

  var params = new URLSearchParams(location.search);
  var ref = params.get("r");
  if (ref) {
    var match = ref.match(/^([a-z0-9]+)\.(\d+)(?:\.([0-9]+(?:-[0-9]+)?))?$/);
    if (match && byId[match[1]] && Number(match[2]) >= 1 && Number(match[2]) <= byId[match[1]].c.length) {
      showChapter(match[1], Number(match[2]), match[3] || "");
    }
  } else if (params.get("sheet")) {
    openSheet(params.get("sheet"));
  }
  if (params.get("selftest") === "1") {
    var report = [];
    showChapter("jhn", 3, "16");
    report.push(readEl.textContent.indexOf("독생자를 주셨으니") === -1 ? "john-fail" : "john-ok");
    openSheet("search");
    runSearch("태초");
    report.push(document.querySelector(".hit") ? "search-ok" : "search-fail");
    showChapter("gen", 1, "");
    report.push(titleEl.textContent === "창세기 1장" ? "home-ok" : "home-fail");
    openSheet("books");
    report.push(sheet.hidden ? "sheet-fail" : "sheet-ok");
    document.documentElement.setAttribute("data-selftest", report.join(" "));
  }

  if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0 && !location.search) {
    navigator.serviceWorker.register("./sw.js").catch(function () {});
  }
})();
