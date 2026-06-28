/* Step-by-step process — advanced mobile swipe carousel.
   Native scroll-snap for swipe, synced dot indicators, and prev/next
   arrows with disabled states at the ends. Desktop shows the full grid. */
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
      var active = 0;

      function goTo(i) {
        i = Math.max(0, Math.min(steps.length - 1, i));
        if (steps[i]) steps[i].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
      function setActive(i) {
        active = i;
        dots.forEach(function (d, j) { d.classList.toggle('is-active', j === i); });
        if (prev) prev.disabled = i <= 0;
        if (next) next.disabled = i >= steps.length - 1;
      }

      dots.forEach(function (d, i) { d.addEventListener('click', function () { goTo(i); }); });
      if (prev) prev.addEventListener('click', function () { goTo(active - 1); });
      if (next) next.addEventListener('click', function () { goTo(active + 1); });

      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting && e.intersectionRatio >= 0.55) {
              var i = steps.indexOf(e.target);
              if (i >= 0) setActive(i);
            }
          });
        }, { root: track, threshold: [0.55] });
        steps.forEach(function (s) { io.observe(s); });
      } else {
        track.addEventListener('scroll', function () {
          var span = track.scrollWidth - track.clientWidth;
          var i = span > 0 ? Math.round(track.scrollLeft / span * (steps.length - 1)) : 0;
          setActive(Math.max(0, Math.min(steps.length - 1, i)));
        }, { passive: true });
      }
      setActive(0);
    });
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
