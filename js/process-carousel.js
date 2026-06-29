/* Step-by-step process — mobile swipe carousel.

   Navigation INTENT (arrows + dots) is an explicit `index`, kept separate from
   the OBSERVED scroll position. While a programmatic scroll is in flight we set
   `navigating` and ignore the scroll listener, so rapid taps each decrement /
   increment by exactly one and always reach the ends. When the scroll settles,
   or when the user free-swipes, we re-sync `index` from the real position.
   Desktop shows the full CSS grid (nav hidden via @media min-width:768px). */
(function () {
  function init() {
    document.querySelectorAll('[data-proc]').forEach(function (wrap) {
      var track = wrap.querySelector('.proc-scroll');
      if (!track) return;
      var steps = Array.prototype.slice.call(track.querySelectorAll('.proc-step'));
      if (!steps.length) return;
      var dots = Array.prototype.slice.call(wrap.querySelectorAll('.proc-dot'));
      var prev = wrap.querySelector('.proc-prev');
      var next = wrap.querySelector('.proc-next');

      var last = steps.length - 1;
      var index = 0;          // navigation intent / current step
      var navigating = false; // true while a programmatic scroll is animating
      var raf = 0, settle = 0;

      function clamp(i) { return Math.max(0, Math.min(last, i)); }

      // Index whose centre is closest to the track viewport centre (free-swipe).
      function nearestIndex() {
        var tr = track.getBoundingClientRect();
        var centre = tr.left + tr.width / 2;
        var best = 0, bestDist = Infinity;
        for (var i = 0; i < steps.length; i++) {
          var r = steps[i].getBoundingClientRect();
          var d = Math.abs((r.left + r.width / 2) - centre);
          if (d < bestDist) { bestDist = d; best = i; }
        }
        return best;
      }

      // scrollLeft that centres step i within the track, clamped to range.
      function targetFor(i) {
        var s = steps[i];
        var t = track.scrollLeft +
          (s.getBoundingClientRect().left - track.getBoundingClientRect().left) -
          (track.clientWidth - s.offsetWidth) / 2;
        return Math.max(0, Math.min(t, Math.max(0, track.scrollWidth - track.clientWidth)));
      }

      function render() {
        for (var j = 0; j < dots.length; j++) {
          dots[j].classList.toggle('is-active', j === index);
          dots[j].setAttribute('aria-current', j === index ? 'true' : 'false');
        }
        if (prev) prev.disabled = index <= 0;
        if (next) next.disabled = index >= last;
      }

      // Release the nav lock once scrolling has stopped, then trust the real position.
      function armSettle() {
        clearTimeout(settle);
        settle = setTimeout(function () {
          navigating = false;
          index = nearestIndex();
          render();
        }, 350);
      }

      function goTo(i) {
        index = clamp(i);
        render();                       // immediate, responsive UI
        navigating = true;
        var left = targetFor(index);
        if (track.scrollTo) track.scrollTo({ left: left, behavior: 'smooth' });
        else track.scrollLeft = left;
        armSettle();
      }

      dots.forEach(function (d, i) { d.addEventListener('click', function () { goTo(i); }); });
      if (prev) prev.addEventListener('click', function () { goTo(index - 1); });
      if (next) next.addEventListener('click', function () { goTo(index + 1); });

      track.addEventListener('scroll', function () {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          if (navigating) { armSettle(); return; } // ignore our own animation; wait for it to settle
          index = nearestIndex();                  // user free-swipe → live sync
          render();
        });
      }, { passive: true });

      // Snappier settle where supported.
      if ('onscrollend' in window) {
        track.addEventListener('scrollend', function () {
          if (!navigating) return;
          clearTimeout(settle);
          navigating = false;
          index = nearestIndex();
          render();
        });
      }

      window.addEventListener('resize', function () {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          if (navigating) return;
          index = nearestIndex();
          render();
        });
      }, { passive: true });

      render(); // first step active, prev disabled
    });
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
