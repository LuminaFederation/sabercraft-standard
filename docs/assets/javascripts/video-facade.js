/* Small YouTube embeds carry more player chrome than picture: the channel
   avatar, the title bar, the share button and the "Watch on YouTube" pill are
   all sized for a full-width player, and at a third of the content column they
   cover most of the frame. So the page ships the poster image and a play
   button of its own, and the player is only built here, once a reader asks
   for it.

   The markup is a plain link to the video, so with JavaScript off the poster
   still opens the video on YouTube. */
(function () {
  "use strict";

  function player(id, title) {
    var frame = document.createElement("iframe");
    /* autoplay, because the click that swapped this in was the request to
       play; without it the reader has to click a second time. */
    frame.src = "https://www.youtube.com/embed/" + encodeURIComponent(id) + "?autoplay=1";
    frame.title = title;
    frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    frame.allowFullscreen = true;
    return frame;
  }

  function initVideoFacades() {
    var posters = document.querySelectorAll(".video-aside__poster[data-video]");
    Array.prototype.forEach.call(posters, function (poster) {
      poster.addEventListener("click", function (event) {
        /* Modified clicks are the reader asking for a new tab or window;
           leave those to the browser and the href. */
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) {
          return;
        }
        event.preventDefault();
        var frame = player(poster.dataset.video, poster.dataset.title || "");
        poster.parentNode.replaceChild(frame, poster);
        frame.focus();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVideoFacades);
  } else {
    initVideoFacades();
  }
})();
