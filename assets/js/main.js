/* NAF Properties Limited — site interactions (no dependencies) */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Open every new page at the top ----------
     Browsers and embedded previews can carry the previous scroll position
     into the next page. Start each fresh visit at the top, unless the link
     points at a section (e.g. services.html#lease-of-facilities) or the
     visitor pressed Back/Forward, where returning to their place is expected. */
  const navEntry = performance.getEntriesByType ? performance.getEntriesByType("navigation")[0] : null;
  const isBackForward = !!navEntry && navEntry.type === "back_forward";
  let hashTarget = null;
  try { hashTarget = location.hash.length > 1 ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null; } catch (_) {}
  if (!isBackForward && !hashTarget) {
    const jumpTop = () => {
      const root = document.documentElement, prev = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      window.scrollTo(0, 0);
      root.style.scrollBehavior = prev;
    };
    jumpTop();
    window.addEventListener("load", () => { jumpTop(); setTimeout(jumpTop, 60); }, { once: true });
  }

  /* ---------- Toast ---------- */
  const toast = $("#toast");
  let toastTimer;
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
  }

  /* ---------- Header shadow + back to top ---------- */
  const header = $(".site-header");
  const toTop = $(".to-top");
  const onScroll = () => {
    const y = window.scrollY;
    header && header.classList.toggle("scrolled", y > 40);
    if (toTop) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      toTop.classList.toggle("show", y > 320);
      toTop.style.setProperty("--p", max > 0 ? Math.min(1, y / max).toFixed(3) : 0);
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  const goTop = (e) => { e && e.preventDefault(); window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }); };
  toTop && toTop.addEventListener("click", goTop);
  $$("[data-top]").forEach((a) => a.addEventListener("click", goTop));

  /* ---------- Dropdown (touch / keyboard) ---------- */
  $$(".has-dropdown > button").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const li = btn.parentElement;
      const open = !li.classList.contains("open");
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", () => $$(".has-dropdown.open").forEach((li) => { li.classList.remove("open"); $("button", li).setAttribute("aria-expanded", "false"); }));

  /* ---------- Generic overlay (drawer / modal) helpers ---------- */
  let lastFocus = null;
  function openOverlay(el) {
    lastFocus = document.activeElement;
    el.classList.add("open");
    el.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    const f = $("input, select, textarea, button:not(.modal-backdrop)", $(".modal-dialog, .drawer-panel", el) || el);
    setTimeout(() => f && f.focus(), 60);
  }
  function closeOverlay(el) {
    el.classList.remove("open");
    el.setAttribute("aria-hidden", "true");
    if (!$(".modal.open, .drawer.open")) document.body.style.overflow = "";
    lastFocus && lastFocus.focus && lastFocus.focus();
  }
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = $$(".modal.open, .drawer.open").pop();
    open && closeOverlay(open);
  });
  $$("[data-close]").forEach((b) => b.addEventListener("click", () => closeOverlay(b.closest(".modal, .drawer"))));

  /* ---------- Mobile drawer ---------- */
  const drawer = $("#drawer");
  $$("[data-menu]").forEach((b) => b.addEventListener("click", () => drawer && openOverlay(drawer)));

  /* ---------- Book-a-visit modal ---------- */
  const bookModal = $("#book-modal");
  $$("[data-book]").forEach((b) =>
    b.addEventListener("click", (e) => {
      e.preventDefault();
      if (!bookModal) return;
      if (drawer && drawer.classList.contains("open")) closeOverlay(drawer);
      const estate = b.getAttribute("data-book");
      const sel = $("#bv-estate");
      if (sel && estate) sel.value = estate;
      resetForm($("form", bookModal));
      openOverlay(bookModal);
    })
  );

  /* ---------- Forms: validate + success state ----------
     Front-end only. To go live, POST these fields to the existing
     /message endpoint (name, email, phone, report, category, page + _token). */
  function resetForm(form) {
    if (!form) return;
    form.hidden = false;
    const ok = form.parentElement.querySelector(".form-success");
    if (ok) ok.hidden = true;
  }
  function validate(form) {
    let valid = true;
    $$("input, select, textarea", form).forEach((el) => {
      const err = el.parentElement.querySelector(".err");
      let msg = "";
      const v = el.value.trim();
      if (el.required && !v) msg = "Please fill in this field.";
      else if (el.type === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Enter an email address like name@example.com.";
      else if (el.type === "tel" && v && v.replace(/\D/g, "").length < 10) msg = "Enter a phone number with at least 10 digits.";
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg;
      if (msg && valid) { valid = false; el.focus(); }
    });
    return valid;
  }
  $$("form[data-form]").forEach((form) => {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validate(form)) return;
      const ok = form.parentElement.querySelector(".form-success");
      const nameField = form.querySelector("[name=name]");
      if (ok) {
        const who = $("[data-who]", ok);
        if (who && nameField) who.textContent = nameField.value.trim().split(" ")[0] || "there";
        form.hidden = true;
        ok.hidden = false;
        form.reset();
      } else {
        form.reset();
        showToast("Thanks — we’ve received your details.");
      }
    });
    $$("input, select, textarea", form).forEach((el) => el.addEventListener("input", () => {
      if (el.getAttribute("aria-invalid") === "true") { el.setAttribute("aria-invalid", "false"); const err = el.parentElement.querySelector(".err"); if (err) err.textContent = ""; }
    }));
  });
  $$("[data-reset-form]").forEach((b) => b.addEventListener("click", () => resetForm(b.closest(".form-success").parentElement.querySelector("form"))));

  /* ---------- Scroll-driven estate backdrop ----------
     Every section with data-bg="file.jpg" owns a backdrop image. The image
     belonging to the section at the middle of the viewport fades in; sheets
     (no data-bg) keep the last image. The active image drifts with scroll
     progress and, on desktop, follows the pointer slightly. */
  const bd = $(".backdrop");
  const rail = $(".tour-rail");
  if (bd) {
    const imgs = new Map($$("img", bd).map((im) => [im.dataset.key, im]));
    const secs = $$("[data-bg]");
    const railLinks = rail ? $$("a", rail) : [];
    let current = null, ticking = false;
    const setBg = (key) => {
      if (key === current || !imgs.has(key)) return;
      imgs.forEach((im, k) => im.classList.toggle("active", k === key));
      current = key;
    };
    const update = () => {
      ticking = false;
      const mid = window.innerHeight * 0.5;
      let best = null;
      for (const sec of secs) {
        const r = sec.getBoundingClientRect();
        if (r.top <= mid) best = sec; else break;
      }
      best = best || secs[0];
      if (!best) return;
      setBg(best.dataset.bg);
      if (!reduceMotion) {
        const r = best.getBoundingClientRect();
        const prog = Math.min(1, Math.max(0, (mid - r.top) / Math.max(r.height, 1)));
        bd.style.setProperty("--py", ((0.5 - prog) * 50).toFixed(1) + "px");
      }
      if (rail) {
        const inTour = best.classList.contains("chapter");
        rail.classList.toggle("show", inTour && best.getBoundingClientRect().bottom > mid);
        railLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + best.id));
      }
    };
    const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener("scroll", req, { passive: true });
    window.addEventListener("resize", req);
    update();
    if (!reduceMotion && window.matchMedia("(pointer: fine)").matches) {
      window.addEventListener("pointermove", (ev) => {
        bd.style.setProperty("--mx", ((ev.clientX / window.innerWidth - 0.5) * -28).toFixed(1) + "px");
        bd.style.setProperty("--my", ((ev.clientY / window.innerHeight - 0.5) * -18).toFixed(1) + "px");
      }, { passive: true });
    }
  }

  /* ---------- Reveal on scroll ---------- */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const rio = new IntersectionObserver((ents) => ents.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); rio.unobserve(en.target); }
    }), { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach((el) => rio.observe(el));
  } else reveals.forEach((el) => el.classList.add("in"));

  /* ---------- Count-up stats (final values are in the HTML) ---------- */
  const counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        const el = en.target, end = +el.dataset.count, t0 = performance.now(), dur = 1400;
        const fmt = (n) => n.toLocaleString("en-NG");
        const tick = (t) => {
          const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          el.textContent = fmt(Math.round(end * e));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    counters.forEach((c) => io.observe(c));
  }

  /* ---------- Filters (communities / portfolio) ---------- */
  $$("[data-filter-group]").forEach((wrap) => {
    const target = $(wrap.dataset.filterGroup);
    if (!target) return;
    const items = $$("[data-tags]", target);
    const count = $(".result-count", wrap);
    const empty = $(".empty-state", target.parentElement);
    const state = {};
    const apply = () => {
      let n = 0;
      items.forEach((it) => {
        const tags = it.dataset.tags.split(" ");
        const ok = Object.values(state).every((v) => v === "all" || tags.includes(v));
        it.hidden = !ok;
        if (ok) n++;
      });
      if (count) count.textContent = n + (n === 1 ? " result" : " results");
      if (empty) empty.classList.toggle("show", n === 0);
    };
    $$(".filter-btn", wrap).forEach((b) => {
      const key = b.dataset.key || "k";
      if (b.getAttribute("aria-pressed") === "true") state[key] = b.dataset.value;
      b.addEventListener("click", () => {
        $$(`.filter-btn[data-key="${key}"]`, wrap).forEach((o) => o.setAttribute("aria-pressed", "false"));
        b.setAttribute("aria-pressed", "true");
        state[key] = b.dataset.value;
        apply();
      });
    });
    // Deep link: communities.html#abuja or #commercial
    const hash = location.hash.replace("#", "").toLowerCase();
    if (hash) {
      const btn = $(`.filter-btn[data-value="${hash}"]`, wrap);
      btn && btn.click();
    }
    apply();
  });
  $$("[data-reset-filters]").forEach((b) => b.addEventListener("click", () => {
    $$(".filter-btn[data-value='all']").forEach((x) => x.click());
  }));

  /* ---------- Home finder → communities ---------- */
  const finder = $("#finder");
  finder && finder.addEventListener("submit", (e) => {
    e.preventDefault();
    const city = $("#f-city").value, type = $("#f-type").value;
    location.href = "communities.html" + (city !== "all" ? "#" + city : type !== "all" ? "#" + type : "");
  });

  /* ---------- Lightbox ---------- */
  const lb = $("#lightbox");
  if (lb) {
    const img = $("img", lb), title = $("figcaption strong", lb), text = $("figcaption span", lb);
    let group = [], idx = 0;
    const render = () => {
      const g = group[idx];
      img.src = g.dataset.full || $("img", g).src;
      img.alt = $("img", g) ? $("img", g).alt : "";
      title.textContent = g.dataset.title || "";
      text.textContent = g.dataset.text || "";
      $$(".lb-nav", lb).forEach((n) => (n.hidden = group.length < 2));
    };
    $$("[data-lightbox]").forEach((el) => el.addEventListener("click", () => {
      group = $$(`[data-lightbox="${el.dataset.lightbox}"]`).filter((x) => !x.hidden);
      idx = group.indexOf(el);
      render();
      openOverlay(lb);
    }));
    $(".lb-nav.prev", lb).addEventListener("click", () => { idx = (idx - 1 + group.length) % group.length; render(); });
    $(".lb-nav.next", lb).addEventListener("click", () => { idx = (idx + 1) % group.length; render(); });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("open") || group.length < 2) return;
      if (e.key === "ArrowRight") { idx = (idx + 1) % group.length; render(); }
      if (e.key === "ArrowLeft") { idx = (idx - 1 + group.length) % group.length; render(); }
    });
  }

  /* ---------- Copy buttons ---------- */
  $$("[data-copy]").forEach((b) => b.addEventListener("click", () => {
    const val = b.dataset.copy;
    const done = () => showToast("Copied: " + val);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(val).then(done).catch(() => fallbackCopy(val, done));
    } else fallbackCopy(val, done);
  }));
  function fallbackCopy(val, done) {
    const t = document.createElement("textarea");
    t.value = val; t.style.position = "fixed"; t.style.opacity = "0";
    document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); done(); } catch (_) { showToast(val); }
    t.remove();
  }

  /* ---------- Services index highlight ---------- */
  const idxLinks = $$(".svc-index a");
  if (idxLinks.length && "IntersectionObserver" in window) {
    const map = new Map(idxLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const io2 = new IntersectionObserver((ents) => ents.forEach((en) => {
      if (en.isIntersecting) { idxLinks.forEach((a) => a.classList.remove("active")); const a = map.get(en.target.id); a && a.classList.add("active"); }
    }), { rootMargin: "-40% 0px -55% 0px" });
    $$(".svc-row").forEach((r) => io2.observe(r));
  }

  /* ---------- Contact topic from link (contact.html#quote, #diaspora) ---------- */
  const topic = $("#c-topic");
  if (topic && location.hash) {
    const opt = $(`option[data-hash="${location.hash.slice(1)}"]`, topic);
    if (opt) { topic.value = opt.value; const m = $("#message"); m && m.scrollIntoView(); }
  }

  /* ---------- Minimum date on date fields ---------- */
  const today = new Date().toISOString().slice(0, 10);
  $$("input[type=date]").forEach((d) => d.setAttribute("min", today));
})();
