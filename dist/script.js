/* ==========================================================================
   Wolves Storage Sussex — script.js  (vanilla JS, no dependencies)
   Powers every interactive element across all 10 pages.
   Everything is feature-detected and null-safe so a page that doesn't use a
   given widget simply skips it.
   ========================================================================== */
(function () {
  "use strict";

  /* If Tailwind's CDN is present, remove the offline-fallback flag.
     We optimistically assume online; a tiny check below confirms. */
  document.documentElement.classList.remove("no-tw");

  var onReady = function (fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  };

  onReady(function () {
    /* ---- Detect whether Tailwind actually applied; if not, add fallback --- */
    try {
      var probe = document.createElement("div");
      probe.className = "hidden";
      document.body.appendChild(probe);
      var applied = getComputedStyle(probe).display === "none";
      document.body.removeChild(probe);
      if (!applied) {
        document.documentElement.classList.add("no-tw");
        var note = document.querySelector(".offline-note");
        if (note) note.removeAttribute("hidden");
      }
    } catch (e) { /* ignore */ }

    /* ---- Footer year ----------------------------------------------------- */
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });

    /* ---- Sticky header shadow ------------------------------------------- */
    var header = document.querySelector(".site-header");
    if (header) {
      var onScroll = function () {
        header.classList.toggle("is-stuck", window.scrollY > 8);
        var btt = document.querySelector(".back-to-top");
        if (btt) btt.classList.toggle("is-visible", window.scrollY > 480);
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }

    /* ---- Active nav link by current filename ----------------------------- */
    var here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll("[data-nav] a[href]").forEach(function (a) {
      var target = a.getAttribute("href").split("/").pop();
      if (target === here) {
        a.classList.add("is-active");
        a.setAttribute("aria-current", "page");
        var parentToggle = a.closest(".has-dropdown");
        if (parentToggle) {
          var t = parentToggle.querySelector(".nav-top");
          if (t) t.classList.add("is-active");
        }
      }
    });

    /* ---- Mobile menu ----------------------------------------------------- */
    var menu = document.querySelector("[data-mobile-menu]");
    /* NOTE: there are TWO [data-menu-toggle] buttons — the header hamburger AND
       the ✕ inside the panel. Wire ALL of them (querySelectorAll, not querySelector). */
    var toggles = document.querySelectorAll("[data-menu-toggle]");
    var headerBurger = document.querySelector("header [data-menu-toggle]");
    var setMenu = function (open) {
      if (!menu) return;
      menu.classList.toggle("translate-x-full", !open);
      menu.classList.toggle("opacity-0", !open);
      menu.classList.toggle("pointer-events-none", !open);
      document.body.classList.toggle("modal-open", open);
      toggles.forEach(function (t) { t.setAttribute("aria-expanded", open ? "true" : "false"); });
      if (headerBurger) headerBurger.classList.toggle("is-open", open);
    };
    toggles.forEach(function (t) {
      t.addEventListener("click", function () {
        /* open if currently closed (panel still has translate-x-full), else close */
        setMenu(menu ? menu.classList.contains("translate-x-full") : false);
      });
    });
    if (menu) {
      /* close when a nav link is tapped */
      menu.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () { setMenu(false); });
      });
      /* close when tapping the dark backdrop (first child) or pressing Escape */
      menu.addEventListener("click", function (e) {
        if (e.target === menu || e.target === menu.firstElementChild) setMenu(false);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && !menu.classList.contains("translate-x-full")) setMenu(false);
      });
    }

    /* ---- Mobile accordion sub-menus + touch dropdowns -------------------- */
    document.querySelectorAll("[data-submenu-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var parent = btn.closest(".has-dropdown") || btn.parentElement;
        if (parent) parent.classList.toggle("is-open");
      });
    });

    /* ---- Smooth scroll for in-page anchors ------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      a.addEventListener("click", function (e) {
        var t = document.querySelector(id);
        if (!t) return;
        e.preventDefault();
        var top = t.getBoundingClientRect().top + window.scrollY - 84;
        window.scrollTo({ top: top, behavior: "smooth" });
      });
    });

    /* ---- Reveal on scroll ------------------------------------------------ */
    var reveals = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && reveals.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add("in"); });
    }

    /* ---- Animated counters ---------------------------------------------- */
    var counters = document.querySelectorAll("[data-counter]");
    if ("IntersectionObserver" in window && counters.length) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target, target = parseFloat(el.getAttribute("data-counter")) || 0;
          var suffix = el.getAttribute("data-suffix") || "";
          var prefix = el.getAttribute("data-prefix") || "";
          var dur = 1400, start = null;
          var step = function (ts) {
            if (!start) start = ts;
            var p = Math.min((ts - start) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = prefix + (Math.round(target * eased)).toLocaleString() + suffix;
            if (p < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
          cio.unobserve(el);
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    }

    /* ---- Testimonial / generic carousel ---------------------------------- */
    document.querySelectorAll("[data-carousel]").forEach(function (root) {
      var track = root.querySelector(".carousel__track");
      var slides = root.querySelectorAll(".carousel__slide");
      var dotsWrap = root.querySelector(".carousel__dots");
      var prev = root.querySelector("[data-carousel-prev]");
      var next = root.querySelector("[data-carousel-next]");
      if (!track || slides.length === 0) return;
      var i = 0, timer = null;
      var dots = [];
      if (dotsWrap) {
        slides.forEach(function (_, idx) {
          var b = document.createElement("button");
          b.className = "carousel__dot" + (dotsWrap.hasAttribute("data-dark") ? " dot-dark" : "");
          b.setAttribute("aria-label", "Go to slide " + (idx + 1));
          b.addEventListener("click", function () { go(idx); reset(); });
          dotsWrap.appendChild(b); dots.push(b);
        });
      }
      var go = function (n) {
        i = (n + slides.length) % slides.length;
        track.style.transform = "translateX(" + (-i * 100) + "%)";
        dots.forEach(function (d, idx) { d.classList.toggle("is-active", idx === i); });
      };
      var auto = function () { timer = setInterval(function () { go(i + 1); }, 6000); };
      var reset = function () { if (timer) clearInterval(timer); auto(); };
      if (prev) prev.addEventListener("click", function () { go(i - 1); reset(); });
      if (next) next.addEventListener("click", function () { go(i + 1); reset(); });
      root.addEventListener("mouseenter", function () { if (timer) clearInterval(timer); });
      root.addEventListener("mouseleave", reset);
      /* swipe */
      var x0 = null;
      root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      root.addEventListener("touchend", function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 40) { go(dx < 0 ? i + 1 : i - 1); reset(); }
        x0 = null;
      });
      go(0); auto();
    });

    /* ---- Accordion (FAQ) ------------------------------------------------- */
    document.querySelectorAll("[data-accordion] .accordion__item").forEach(function (item) {
      var btn = item.querySelector(".accordion__btn");
      var panel = item.querySelector(".accordion__panel");
      if (!btn || !panel) return;
      btn.addEventListener("click", function () {
        var open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        panel.style.maxHeight = open ? panel.scrollHeight + "px" : null;
      });
    });

    /* ---- Quote modal ----------------------------------------------------- */
    var modal = document.querySelector("[data-modal='quote']");
    var openModal = function (open) {
      if (!modal) return;
      if (open) { modal.hidden = false; requestAnimationFrame(function () { modal.classList.add("is-open"); }); }
      else { modal.classList.remove("is-open"); setTimeout(function () { modal.hidden = true; }, 250); }
      document.body.classList.toggle("modal-open", open);
    };
    document.querySelectorAll("[data-modal-open]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.preventDefault();
        setMenu(false);   /* close mobile menu first so the shared body scroll-lock has one owner */
        openModal(true);
      });
    });
    if (modal) {
      modal.querySelectorAll("[data-modal-close]").forEach(function (b) {
        b.addEventListener("click", function () { openModal(false); });
      });
      modal.addEventListener("click", function (e) { if (e.target === modal) openModal(false); });
    }
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { openModal(false); closeLightbox(); }
    });

    /* ---- Forms: fake submit with success message ------------------------- */
    document.querySelectorAll("form[data-fake-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        /* basic validation */
        var ok = true;
        form.querySelectorAll("[required]").forEach(function (field) {
          var valid = field.value.trim() !== "" &&
            (field.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value));
          field.classList.toggle("ring-2", !valid);
          field.classList.toggle("ring-red-400", !valid);
          if (!valid) ok = false;
        });
        if (!ok) return;
        var success = form.querySelector("[data-form-success]");
        var fields = form.querySelector("[data-form-fields]");
        if (success) {
          if (fields) fields.style.display = "none"; else form.reset();
          success.hidden = false;
          success.scrollIntoView({ behavior: "smooth", block: "center" });
        } else {
          form.reset();
          alert("Thank you! Your request has been received. We'll be in touch within 24 hours.");
        }
        /* auto-close the modal version after a moment */
        if (form.closest("[data-modal='quote']")) {
          setTimeout(function () {
            openModal(false);
            if (fields) fields.style.display = "";
            if (success) success.hidden = true;
            form.reset();
          }, 3200);
        }
      });
    });

    /* ---- Image gallery lightbox ----------------------------------------- */
    var lb = document.querySelector("[data-lightbox]");
    var lbImg = lb ? lb.querySelector("img") : null;
    var galleryImgs = Array.prototype.slice.call(document.querySelectorAll("[data-gallery] img, img.gallery-thumb"));
    var lbIndex = 0;
    var openLightbox = function (idx) {
      if (!lb || !lbImg || !galleryImgs.length) return;
      lbIndex = (idx + galleryImgs.length) % galleryImgs.length;
      var src = galleryImgs[lbIndex].getAttribute("data-full") || galleryImgs[lbIndex].src;
      lbImg.src = src;
      lbImg.alt = galleryImgs[lbIndex].alt || "";
      lb.hidden = false; document.body.classList.add("modal-open");
    };
    var closeLightbox = function () {
      if (!lb) return; lb.hidden = true; document.body.classList.remove("modal-open");
    };
    galleryImgs.forEach(function (img, idx) {
      img.classList.add("gallery-thumb");
      img.addEventListener("click", function () { openLightbox(idx); });
    });
    if (lb) {
      lb.querySelectorAll("[data-lightbox-close]").forEach(function (b) {
        b.addEventListener("click", closeLightbox);
      });
      var lbPrev = lb.querySelector("[data-lightbox-prev]");
      var lbNext = lb.querySelector("[data-lightbox-next]");
      if (lbPrev) lbPrev.addEventListener("click", function (e) { e.stopPropagation(); openLightbox(lbIndex - 1); });
      if (lbNext) lbNext.addEventListener("click", function (e) { e.stopPropagation(); openLightbox(lbIndex + 1); });
      lb.addEventListener("click", function (e) { if (e.target === lb) closeLightbox(); });
    }

    /* ---- Image fallback: if a remote photo fails (e.g. offline), swap to a
       local branded SVG placeholder so the layout still looks intentional. --- */
    document.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function handle() {
        var fb = img.getAttribute("data-fallback");
        img.removeEventListener("error", handle); /* prevent loops */
        if (fb && img.src.indexOf(fb) === -1) { img.src = fb; }
        else { img.classList.add("with-fallback"); img.style.objectFit = "cover"; }
      });
    });

    /* ---- Cookie banner --------------------------------------------------- */
    var cookie = document.querySelector("[data-cookie]");
    if (cookie) {
      var KEY = "wss_cookie_ok";
      var stored = null;
      try { stored = localStorage.getItem(KEY); } catch (e) {}
      if (stored === "1") cookie.classList.add("is-hidden");
      else cookie.classList.remove("is-hidden");
      cookie.querySelectorAll("[data-cookie-accept]").forEach(function (b) {
        b.addEventListener("click", function () {
          cookie.classList.add("is-hidden");
          try { localStorage.setItem(KEY, "1"); } catch (e) {}
        });
      });
    }

    /* ---- Back to top ----------------------------------------------------- */
    var btt = document.querySelector("[data-back-to-top]");
    if (btt) btt.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
})();
