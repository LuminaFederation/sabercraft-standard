/* The hero background clip is by far the heaviest asset on the homepage, and
   nothing on the page depends on it. So the markup ships without a src: the
   poster image stands in, and the clip is only fetched here, after the window
   load event has fired and the browser is otherwise idle. That keeps it out of
   the critical path entirely rather than merely deprioritising it.

   It is also skipped outright for readers who have asked for reduced motion,
   and on connections that report Save-Data or 2g. */
(function () {
  "use strict";

  function startHeroVideo() {
    var video = document.querySelector(".lumina-hero__video[data-src]");
    if (!video) {
      return;
    }

    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (connection && (connection.saveData || /(^|-)2g$/.test(connection.effectiveType || ""))) {
      return;
    }

    var load = function () {
      video.src = video.dataset.src;
      video.removeAttribute("data-src");
      video.load();

      var played = video.play();
      if (played && typeof played.catch === "function") {
        // Autoplay can still be refused; the poster remains in place if so.
        played.catch(function () {});
      }
    };

    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(load, { timeout: 3000 });
    } else {
      window.setTimeout(load, 300);
    }
  }

  if (document.readyState === "complete") {
    startHeroVideo();
  } else {
    window.addEventListener("load", startHeroVideo);
  }
})();
