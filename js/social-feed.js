/* Wolves Removals — Facebook social-post feed component.
   Renders the carousel + lightbox from a fallback list embedded in the page, then
   tries to replace it with LIVE posts from /api/social (a Cloudflare Pages Function
   that calls the Facebook Graph API). If the function isn't deployed or the fetch
   fails, the fallback posts stay — so the section never breaks. */
(function () {
  "use strict";
  function fallbackPosts() {
    var el = document.getElementById("social-fallback");
    if (!el) return [];
    try { return JSON.parse(el.textContent || "[]"); } catch (e) { return []; }
  }
  document.addEventListener("alpine:init", function () {
    window.Alpine.data("socialFeed", function () {
      return {
        open: false,
        active: 0,
        posts: fallbackPosts(),
        async init() {
          try {
            var r = await fetch("/api/social", { cache: "no-store" });
            if (!r.ok) return;
            var data = await r.json();
            if (data && Array.isArray(data.posts) && data.posts.length) {
              this.posts = data.posts;
            }
          } catch (e) { /* keep fallback */ }
        }
      };
    });
  });
})();
