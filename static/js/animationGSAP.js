// GSAP + SplitText (Club) global usage
// Ensure DOM is ready and required globals are present
(function () {
  function runSplit(selector, optsChars, fromVars) {
    const el = document.querySelector(selector);
    if (!el) return;
    const split = new SplitText(selector, optsChars);
    const parts =
      (optsChars.type.includes("chars") ? split.chars : split.words) || [];
    if (parts.length) {
      gsap.from(parts, fromVars);
    }
  }

  function initAnimations() {
    if (!(window.gsap && window.SplitText)) {
      console.warn(
        "GSAP or SplitText is not available. Ensure /static/js/vendor/gsap/gsap.min.js and SplitText.min.js are loaded before animationGSAP.js"
      );
      return;
    }

    // Register plugin
    try {
      gsap.registerPlugin(SplitText);
    } catch (e) {}

    // Logo jumping animation
    const logotypeSamin = document.querySelector(".header__logo");
    if (logotypeSamin) {
      gsap.to(logotypeSamin, {
        y: 20,
        duration: 1,
        repeat: -1,
        yoyo: true,
        ease: "power1.inOut",
      });
    }

    // Support .hero-title (user snippet) and existing selectors
    runSplit(
      ".hero-title",
      { type: "chars,words" },
      { opacity: 0, y: 20, stagger: 0.03, duration: 0.6 }
    );

    // Title split animation
    runSplit(
      ".mright__header",
      { type: "chars" },
      { x: -100, autoAlpha: 0, stagger: { amount: 0.5, from: "end" } }
    );

    // Statement split animation
    runSplit(
      ".mright__statement",
      { type: "chars" },
      { y: 100, autoAlpha: 0, stagger: { amount: 0.5, from: "start" } }
    );

    // Commitment header
    runSplit(
      ".commitment__header",
      { type: "words" },
      { y: 100, autoAlpha: 0, stagger: { amount: 0.5, from: "end" } }
    );

    // Commitment text
    runSplit(
      ".commitment__text",
      { type: "words" },
      { y: 100, autoAlpha: 0, stagger: { amount: 0.9, from: "start" } }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAnimations);
  } else {
    initAnimations();
  }
})();
