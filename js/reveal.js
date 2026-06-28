// Scroll-reveal: add `.is-in` to `.reveal-lr` elements when they enter the viewport, so
// they slide in from the left (CSS handles the transition; stagger via inline delay).
(function () {
  var els = document.querySelectorAll('.reveal-lr:not(.is-in)');
  if (!els.length) return;
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (el) { io.observe(el); });
})();
