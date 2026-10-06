/* Viewcut landing — VSL player, chapters, proof slots, WhatsApp contact */
(function () {
  // Numéro WhatsApp au format international sans "+" (wa.me/32467679694)
  var WHATSAPP = "32467679694";
  /* langue de la page (<html data-lang>) + chaînes générées par le JS */
  var LANG = document.documentElement.getAttribute("data-lang") === "en" ? "en" : "fr";
  var STR = {
    fr: {
      copied: "Copié ✓",
      enlarge: "agrandir",
      lbTitle: "Capture en plein écran",
      lbAlt: "Capture Instagram agrandie",
      prev: "Capture précédente",
      next: "Capture suivante",
      close: "Fermer",
      shotFallback: "Capture Instagram",
      play: "Lecture",
      pause: "Pause",
      unmute: "Rétablir le son",
      mute: "Couper le son",
      waFallback: "Numéro WhatsApp à renseigner (assets/app.js → WHATSAPP)"
    },
    en: {
      copied: "Copied ✓",
      enlarge: "enlarge",
      lbTitle: "Fullscreen screenshot",
      lbAlt: "Enlarged Instagram screenshot",
      prev: "Previous screenshot",
      next: "Next screenshot",
      close: "Close",
      shotFallback: "Instagram screenshot",
      play: "Play",
      pause: "Pause",
      unmute: "Unmute",
      mute: "Mute",
      waFallback: "WhatsApp number to fill in (assets/app.js → WHATSAPP)"
    }
  }[LANG];
  var chaptersData = null;
  var video = document.getElementById("vsl-video");
  var missing = document.getElementById("vsl-missing");

  /* icônes SVG (pas d'emoji : rendu identique sur toutes les plateformes) */
  var IC_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg>';
  var IC_PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>';
  var IC_VOL_ON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>';
  var IC_VOL_OFF = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.06l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';

  function fmt(sec) {
    sec = Math.max(0, Math.floor(sec));
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ":" + (s < 10 ? "0" + s : s);
  }

  function seekTo(t) {
    if (!video) return;
    video.currentTime = t + 0.05;
    video.play().catch(function () {});
  }

  function closePanel() {
    var panel = document.getElementById("chapters-panel");
    var btn = document.getElementById("chapters-btn");
    if (panel) panel.hidden = true;
    if (btn) btn.setAttribute("aria-expanded", "false");
  }

  function renderChapters() {
    var ol = document.getElementById("chapters");
    var chbar = document.getElementById("chbar");
    if (!ol || !chaptersData) return;
    var set = chaptersData[LANG] || chaptersData.fr || chaptersData;
    var total = set.total || (set.chapters[set.chapters.length - 1].t + 10);
    ol.innerHTML = "";
    if (chbar) chbar.innerHTML = "";
    set.chapters.forEach(function (c, i) {
      var li = document.createElement("li");
      var b = document.createElement("button");
      b.type = "button";
      b.dataset.t = c.t;
      b.innerHTML = '<span class="t mono"></span><span class="n"></span>';
      b.querySelector(".t").textContent = c.tc;
      b.querySelector(".n").textContent = c.title;
      b.addEventListener("click", function () { seekTo(c.t); closePanel(); });
      li.appendChild(b);
      ol.appendChild(li);

      /* segment de chapitre sur la barre du lecteur (style YouTube) */
      if (chbar) {
        var segStart = c.t;
        var segEnd = i + 1 < set.chapters.length ? set.chapters[i + 1].t : total;
        var seg = document.createElement("button");
        seg.type = "button";
        seg.className = "chseg";
        seg.dataset.t = c.t;
        seg.style.left = (segStart / total * 100) + "%";
        seg.style.width = ((segEnd - segStart) / total * 100) + "%";
        seg.setAttribute("aria-label", c.tc + " — " + c.title);
        seg.addEventListener("click", function () { seekTo(c.t); });
        chbar.appendChild(seg);
      }
    });
    var dur = document.getElementById("vsl-duration");
    if (dur) dur.textContent = set.duration;
    var dur2 = document.getElementById("ch-duration");
    if (dur2) dur2.textContent = set.duration;
    var copy = document.getElementById("copy-chapters");
    if (copy) copy.dataset.text = set.chapters.map(function (c) {
      return c.tc + " " + c.title;
    }).join("\n") + "\n";
    markActive();
  }

  function markActive() {
    if (!video || !chaptersData) return;
    var set = chaptersData[LANG] || chaptersData.fr || chaptersData;
    var t = video.currentTime;
    var current = null;
    set.chapters.forEach(function (c) { if (t + 0.25 >= c.t) current = c.t; });
    document.querySelectorAll("#chapters button").forEach(function (b) {
      b.classList.toggle("on", Number(b.dataset.t) === current);
    });
    document.querySelectorAll("#chbar .chseg").forEach(function (s) {
      s.classList.toggle("on", Number(s.dataset.t) === current);
    });
  }

  function initProof() {
    var slots = [];
    document.querySelectorAll(".shot[data-src]").forEach(function (slot) { slots.push(slot); });
    if (!slots.length) return;
    var loaded = [];

    var loadSlot = function (slot) {
      if (slot.dataset.loading || slot.dataset.loaded) return;
      slot.dataset.loading = "1";
      var idx = loaded.findIndex(function (e) { return e.slot === slot; });
      var img = new Image();
      img.alt = slot.dataset.alt || "";
      img.decoding = "async";
      img.onload = function () {
        slot.dataset.loaded = "1";
        slot.appendChild(img);
        var ph = slot.querySelector(".ph");
        if (ph) ph.remove();
        slot.classList.add("has-img");
        slot.setAttribute("role", "button");
        slot.setAttribute("tabindex", "0");
        slot.setAttribute("aria-label", (img.alt || STR.shotFallback) + " — " + STR.enlarge);
        var open = function () { openLightbox(idx); };
        slot.addEventListener("click", open);
        slot.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); }
        });
      };
      img.src = slot.dataset.src;
    };

    /* ordre de la galerie = ordre du DOM (indépendant du temps de chargement) */
    slots.forEach(function (slot) { loaded.push({ slot: slot, src: slot.dataset.src }); });
    proofShots = loaded;

    /* chargement différé : les captures sous la ligne de flottaison n'embarquent
       rien tant que la section Preuves n'approche pas (règle performance du skill) */
    var loadAll = function () { slots.forEach(loadSlot); };
    var grid = document.querySelector(".proof-grid");
    if ("IntersectionObserver" in window && grid) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { io.disconnect(); loadAll(); }
        });
      }, { rootMargin: "400px 0px" });
      io.observe(grid);
    } else {
      loadAll();
    }
  }

  /* ---- captures en plein écran ---- */
  var proofShots = [];
  var lb = null, lbIdx = 0, lbLastFocus = null, lbPushed = false;

  function ensureLb() {
    if (lb) return lb;
    lb = document.createElement("div");
    lb.className = "lb";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", STR.lbTitle);
    lb.innerHTML =
      '<img alt="' + STR.lbAlt + '" />' +
      '<button class="lb-btn lb-prev" type="button" aria-label="' + STR.prev + '">&#10094;</button>' +
      '<button class="lb-btn lb-next" type="button" aria-label="' + STR.next + '">&#10095;</button>' +
      '<button class="lb-btn lb-close" type="button" aria-label="' + STR.close + '">&#10005;</button>' +
      '<div class="lb-count mono"></div>';
    document.body.appendChild(lb);
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
    lb.querySelector(".lb-close").addEventListener("click", function () { closeLb(); });
    lb.querySelector(".lb-prev").addEventListener("click", function () { lbStep(-1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { lbStep(1); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("on")) return;
      if (e.key === "Escape") { closeLb(); return; }
      if (e.key === "ArrowLeft") { lbStep(-1); return; }
      if (e.key === "ArrowRight") { lbStep(1); return; }
      /* piège à focus : Tab reste dans la boîte ouverte */
      if (e.key === "Tab") {
        var f = [
          lb.querySelector(".lb-prev"),
          lb.querySelector(".lb-next"),
          lb.querySelector(".lb-close")
        ];
        var i = f.indexOf(document.activeElement);
        e.preventDefault();
        var n = e.shiftKey ? (i <= 0 ? f.length - 1 : i - 1) : (i + 1) % f.length;
        f[n].focus();
      }
    });
    /* bouton Retour du navigateur ferme la visionneuse (et rien d'autre) */
    document.addEventListener("popstate", function () {
      if (lb && lb.classList.contains("on") && lbPushed) {
        lbPushed = false;
        closeLb(true);
      }
    });
    return lb;
  }

  function openLightbox(i) {
    if (!proofShots.length) return;
    var wasOpen = !!(lb && lb.classList.contains("on"));
    lbIdx = (i + proofShots.length) % proofShots.length;
    var el = ensureLb();
    var entry = proofShots[lbIdx];
    var im = el.querySelector("img");
    im.src = entry.src;
    im.alt = (entry.slot && entry.slot.dataset.alt) || STR.lbAlt;
    el.querySelector(".lb-count").textContent = (lbIdx + 1) + " / " + proofShots.length;
    if (wasOpen) return;
    lbLastFocus = document.activeElement;
    el.classList.add("on");
    document.body.style.overflow = "hidden";
    el.querySelector(".lb-close").focus();
    if (!lbPushed) {
      try { history.pushState({ vcLb: 1 }, ""); lbPushed = true; } catch (err) {}
    }
  }

  function closeLb(fromPop) {
    if (!lb || !lb.classList.contains("on")) return;
    lb.classList.remove("on");
    document.body.style.overflow = "";
    if (lbLastFocus && lbLastFocus.focus) {
      try { lbLastFocus.focus(); } catch (err) {}
    }
    if (!fromPop && lbPushed) {
      lbPushed = false;
      try { history.back(); } catch (err) {}
    }
  }

  function lbStep(d) { openLightbox(lbIdx + d); }

  function wireWhatsApp() {
    document.querySelectorAll("a[data-wa]").forEach(function (a) {
      if (WHATSAPP) {
        var text = a.dataset.waText ? "?text=" + encodeURIComponent(a.dataset.waText) : "";
        a.href = "https://wa.me/" + WHATSAPP + text;
        a.rel = "noopener";
        a.target = "_blank";
      } else {
        a.href = "#final";
        a.title = STR.waFallback;
      }
    });
  }

  function wireLangSwitch() {
    /* garde l'ancre de section (#pricing…) en changeant de langue */
    document.querySelectorAll(".lang-switch a").forEach(function (a) {
      a.addEventListener("click", function (e) {
        var h = location.hash;
        if (h && h.length > 1) {
          e.preventDefault();
          location.href = a.getAttribute("href") + h;
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    wireWhatsApp();
    wireLangSwitch();
    var copy = document.getElementById("copy-chapters");
    if (copy) copy.addEventListener("click", function () {
      var done = function () {
        var old = copy.innerHTML;
        copy.textContent = STR.copied;
        setTimeout(function () { copy.innerHTML = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(copy.dataset.text || "").then(done, done);
      } else { done(); }
    });

    /* panneau chapitres intégré au lecteur */
    var chBtn = document.getElementById("chapters-btn");
    var chPanel = document.getElementById("chapters-panel");
    if (chBtn && chPanel) {
      chBtn.addEventListener("click", function () {
        var willOpen = chPanel.hidden;
        chPanel.hidden = !willOpen;
        chBtn.setAttribute("aria-expanded", willOpen ? "true" : "false");
      });
      document.addEventListener("click", function (e) {
        if (chPanel.hidden) return;
        if (chPanel.contains(e.target) || chBtn.contains(e.target)) return;
        closePanel();
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && !chPanel.hidden) closePanel();
      });
    }

    if (video) {
      var player = document.getElementById("player");
      var btnPlay = document.getElementById("btn-play");
      var icPlay = btnPlay ? btnPlay.querySelector(".ic-play") : null;
      var bigPlay = document.getElementById("big-play");
      var tCur = document.getElementById("t-cur");
      var tDur = document.getElementById("t-dur");
      var scrub = document.getElementById("scrub");
      var scrubPlayed = document.getElementById("scrub-played");
      var scrubKnob = document.getElementById("scrub-knob");
      var tip = document.getElementById("chtip");
      var volEl = document.getElementById("vol");
      var btnMute = document.getElementById("btn-mute");
      var icVol = btnMute ? btnMute.querySelector(".ic-vol") : null;
      var btnSpeed = document.getElementById("btn-speed");
      var btnFs = document.getElementById("btn-fs");
      var RATES = [1, 1.2, 1.5, 2];
      var DEFAULT_RATE = 1.2;
      var idleTimer = null;
      var dragging = false;

      var toggleFs = function () {
        if (document.fullscreenElement) { document.exitFullscreen(); return; }
        if (video.requestFullscreen) video.requestFullscreen();
        else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
      };

      function setRate(r) {
        video.playbackRate = r;
        if (btnSpeed) btnSpeed.textContent = (Math.round(r * 100) / 100) + "\u00d7";
      }

      function togglePlay() {
        if (video.paused || video.ended) video.play().catch(function () {});
        else video.pause();
        showCtrl();
      }

      function syncPlay() {
        var playing = !video.paused && !video.ended;
        if (player) player.classList.toggle("playing", playing);
        if (icPlay) icPlay.innerHTML = playing ? IC_PAUSE : IC_PLAY;
        if (btnPlay) btnPlay.setAttribute("aria-label", playing ? STR.pause : STR.play);
        if (playing) showCtrl();
        else showCtrl(true);
      }

      function syncTime() {
        var d = video.duration, c = video.currentTime || 0;
        if (tCur) tCur.textContent = fmt(c);
        if (tDur && d && isFinite(d)) tDur.textContent = fmt(Math.round(d));
        var pct = d && isFinite(d) ? (c / d) * 100 : 0;
        if (scrubPlayed) scrubPlayed.style.width = pct + "%";
        if (scrubKnob) scrubKnob.style.left = pct + "%";
      }

      function syncVol() {
        if (icVol) icVol.innerHTML = video.muted || video.volume === 0 ? IC_VOL_OFF : IC_VOL_ON;
        if (btnMute) btnMute.setAttribute("aria-label", video.muted || video.volume === 0 ? STR.unmute : STR.mute);
        if (volEl && document.activeElement !== volEl) volEl.value = video.muted ? 0 : video.volume;
      }

      function showCtrl(stay) {
        if (!player) return;
        player.classList.remove("idle");
        if (idleTimer) clearTimeout(idleTimer);
        idleTimer = null;
        if (stay || video.paused || video.ended) return;
        var panel = document.getElementById("chapters-panel");
        idleTimer = setTimeout(function () {
          if (panel && !panel.hidden) return;
          if (!video.paused && !video.ended) player.classList.add("idle");
        }, 2600);
      }

      function chapterAt(t) {
        if (!chaptersData) return null;
        var set = chaptersData[LANG] || chaptersData.fr || chaptersData;
        var found = null;
        set.chapters.forEach(function (c) { if (t + 0.25 >= c.t) found = c; });
        return found;
      }

      function scrubRatio(e) {
        var rect = scrub.getBoundingClientRect();
        return Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      }

      function seekRatio(r) {
        var d = video.duration;
        if (d && isFinite(d)) video.currentTime = r * d;
      }

      function updateTip(e) {
        if (!tip || !scrub) return;
        var r = scrubRatio(e);
        var d = video.duration || 0;
        if (!d || !isFinite(d)) { tip.hidden = true; return; }
        var c = chapterAt(r * d);
        tip.textContent = fmt(r * d) + (c ? " \u00b7 " + c.title : "");
        var rect = scrub.getBoundingClientRect();
        var x = rect.left + r * rect.width - (player ? player.getBoundingClientRect().left : 0);
        x = Math.max(64, Math.min(x, (player ? player.clientWidth : rect.width) - 64));
        tip.style.left = x + "px";
        tip.hidden = false;
      }

      if (scrub) {
        scrub.addEventListener("pointerdown", function (e) {
          if (e.target.classList && e.target.classList.contains("chseg")) return;
          dragging = true;
          try { scrub.setPointerCapture(e.pointerId); } catch (err) {}
          seekRatio(scrubRatio(e));
          updateTip(e);
          showCtrl();
        });
        scrub.addEventListener("pointermove", function (e) {
          if (dragging) seekRatio(scrubRatio(e));
          updateTip(e);
          showCtrl();
        });
        var endDrag = function (e) {
          if (!dragging) return;
          dragging = false;
          try { scrub.releasePointerCapture(e.pointerId); } catch (err) {}
        };
        scrub.addEventListener("pointerup", endDrag);
        scrub.addEventListener("pointercancel", endDrag);
        scrub.addEventListener("pointerleave", function () {
          if (!dragging && tip) tip.hidden = true;
        });
        scrub.addEventListener("click", function (e) {
          if (e.target.classList && e.target.classList.contains("chseg")) return;
          video.play().catch(function () {});
        });
      }

      if (btnPlay) btnPlay.addEventListener("click", togglePlay);
      if (bigPlay) bigPlay.addEventListener("click", togglePlay);
      if (video) video.addEventListener("click", togglePlay);

      if (btnSpeed) btnSpeed.addEventListener("click", function () {
        var i = 0;
        for (var k = 0; k < RATES.length; k++) {
          if (Math.abs(video.playbackRate - RATES[k]) < 0.01) i = k;
        }
        setRate(RATES[(i + 1) % RATES.length]);
        showCtrl();
      });

      if (volEl) volEl.addEventListener("input", function () {
        video.muted = false;
        video.volume = Number(volEl.value);
      });
      if (btnMute) btnMute.addEventListener("click", function () {
        video.muted = !video.muted;
        if (!video.muted && video.volume === 0) video.volume = 1;
      });
      if (btnFs) btnFs.addEventListener("click", toggleFs);

      if (player) {
        player.addEventListener("mousemove", function () { showCtrl(); });
        player.addEventListener("pointerdown", function () { showCtrl(); });
        player.addEventListener("mouseleave", function () {
          if (!video.paused && !video.ended && player) player.classList.add("idle");
        });
      }

      function playerInView() {
        if (!player) return false;
        var r = player.getBoundingClientRect();
        var vh = window.innerHeight || 800;
        return r.bottom > vh * 0.25 && r.top < vh * 0.8;
      }

      document.addEventListener("keydown", function (e) {
        var tag = (e.target.tagName || "").toLowerCase();
        if (tag === "input" || tag === "textarea") return;
        var chPanel = document.getElementById("chapters-panel");
        if (e.key === " " || e.key === "k" || e.key === "K") {
          if (tag === "button") return;
          if (!playerInView()) return;
          e.preventDefault();
          togglePlay();
        } else if (e.key === "ArrowLeft") {
          if (!playerInView()) return;
          e.preventDefault();
          video.currentTime = Math.max(0, video.currentTime - 5);
          showCtrl();
        } else if (e.key === "ArrowRight") {
          if (!playerInView()) return;
          e.preventDefault();
          video.currentTime = Math.min(video.duration || 1e9, video.currentTime + 5);
          showCtrl();
        } else if (e.key === "m" || e.key === "M") {
          video.muted = !video.muted;
          showCtrl();
        } else if (e.key === "f" || e.key === "F") {
          toggleFs();
        } else if (e.key === "Escape" && chPanel && !chPanel.hidden) {
          closePanel();
        }
      });

      video.addEventListener("play", syncPlay);
      video.addEventListener("pause", syncPlay);
      video.addEventListener("ended", syncPlay);
      video.addEventListener("ratechange", function () {
        if (btnSpeed) btnSpeed.textContent = (Math.round(video.playbackRate * 100) / 100) + "\u00d7";
      });
      video.addEventListener("volumechange", syncVol);

      video.addEventListener("timeupdate", function () {
        markActive();
        syncTime();
      });
      video.addEventListener("loadedmetadata", function () {
        if (missing) missing.hidden = true;
        setRate(DEFAULT_RATE);
        syncTime();
        syncPlay();
        syncVol();
      });
      video.addEventListener("durationchange", syncTime);
      var baseSrc = video.getAttribute("src");
      var tries = 0;
      video.addEventListener("error", function () {
        if (tries < 3) {
          tries += 1;
          setTimeout(function () {
            video.src = baseSrc + "?r=" + tries + "&t=" + new Date().getTime();
            video.load();
          }, 1200);
          return;
        }
        if (missing) missing.hidden = false;
      });
      video.addEventListener("dblclick", toggleFs);
      if (video.error) tries = 0;
      video.load();
      syncVol();
      syncTime();
    }

    fetch("assets/chapters.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { chaptersData = j; renderChapters(); })
      .catch(function () {});

    initProof();
  });
})();
