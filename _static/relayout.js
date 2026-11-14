// Re-run reveal.js layout when a slide's content changes height.
//
// jsphinx expands a code snippet to the whole file in place (the eye icon).
// reveal.js scales each slide to fit the viewport and caches that scale, so the
// expanded code overflows until something triggers a relayout (e.g. navigating
// away and back). Watching the slides for DOM changes and calling
// Reveal.layout() keeps the slide fitted the moment the code expands.
(function () {
  function relayout() {
    if (window.Reveal && typeof Reveal.layout === "function") {
      Reveal.layout();
    }
  }

  function install() {
    var slides = document.querySelector(".reveal .slides");
    if (!slides) {
      return setTimeout(install, 200); // reveal not mounted yet
    }
    var timer;
    // childList only: Reveal.layout() mutates styles, not child nodes, so this
    // never re-triggers itself. The debounce lets Prism finish re-highlighting
    // the freshly inserted code before we measure it.
    var observer = new MutationObserver(function () {
      clearTimeout(timer);
      timer = setTimeout(relayout, 30);
    });
    observer.observe(slides, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }
})();
