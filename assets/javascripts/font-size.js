/* Reader-controlled text size.

   A pair of buttons in the header steps a multiplier on the root font size.
   Material sizes body copy, headings, tables, admonitions and the navigation
   in rem, so one multiplier moves all of them together; the matching rules
   live in docs/assets/stylesheets/sabercraft.css.

   The choice is remembered across pages and visits, and re-applied in the
   head by a short snippet in overrides/main.html so the page never paints at
   one size and then jumps to another. That snippet and this file share the
   storage key below. */
(function () {
  "use strict";

  var STORAGE_KEY = "sc-font-scale";

  /* Fixed steps rather than free zoom: 100% to 150% is the range over which
     the three-column layout still holds together on a laptop screen. */
  var STEPS = [1, 1.15, 1.3, 1.5];

  function readStep() {
    var stored;
    try {
      stored = window.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      /* Private browsing and blocked storage are not worth failing over. */
      return 0;
    }
    var index = STEPS.indexOf(parseFloat(stored));
    return index === -1 ? 0 : index;
  }

  function writeStep(index) {
    try {
      window.localStorage.setItem(STORAGE_KEY, String(STEPS[index]));
    } catch (error) {
      /* As above: the size still applies for this page view. */
    }
  }

  function button(modifier, label) {
    var el = document.createElement("button");
    el.type = "button";
    el.className = "sc-fontsize__btn sc-fontsize__btn--" + modifier;
    el.textContent = "A";
    el.setAttribute("aria-label", label);
    el.setAttribute("title", label);
    return el;
  }

  function initFontSize() {
    var header = document.querySelector(".md-header__inner");
    if (!header) {
      return;
    }

    var step = readStep();

    var group = document.createElement("div");
    group.className = "sc-fontsize";
    group.setAttribute("role", "group");
    group.setAttribute("aria-label", "Text size");

    var down = button("down", "Decrease text size");
    var up = button("up", "Increase text size");

    /* Sighted readers see the page resize; this is how everyone else knows
       the button did something. */
    var status = document.createElement("span");
    status.className = "sc-fontsize__status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");

    function apply(announce) {
      document.documentElement.style.setProperty("--sc-font-scale", STEPS[step]);

      /* At either end the button keeps its place and its focus; it just has
         nothing left to do. */
      down.setAttribute("aria-disabled", step === 0 ? "true" : "false");
      up.setAttribute("aria-disabled", step === STEPS.length - 1 ? "true" : "false");

      if (announce) {
        status.textContent = "Text size " + Math.round(STEPS[step] * 100) + "%";
      }
    }

    function move(delta) {
      var next = step + delta;
      if (next < 0 || next > STEPS.length - 1) {
        return;
      }
      step = next;
      writeStep(step);
      apply(true);
    }

    down.addEventListener("click", function () {
      move(-1);
    });

    up.addEventListener("click", function () {
      move(1);
    });

    group.appendChild(down);
    group.appendChild(up);
    group.appendChild(status);

    /* Sits with the other header controls, ahead of the light/dark toggle. */
    var palette = header.querySelector("[data-md-component=palette]");
    if (palette) {
      header.insertBefore(group, palette);
    } else {
      header.appendChild(group);
    }

    apply(false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFontSize);
  } else {
    initFontSize();
  }
})();
