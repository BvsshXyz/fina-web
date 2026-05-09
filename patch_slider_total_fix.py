from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

js = r'''
<script>
(() => {
  let index = 0;

  function getEls() {
    return {
      track: document.getElementById("sliderTrack"),
      frame: document.getElementById("sliderFrame"),
      dots: document.getElementById("sliderDots"),
      now: document.getElementById("slideNow"),
      total: document.getElementById("slideTotal"),
      prev: document.getElementById("prevSlide"),
      next: document.getElementById("nextSlide")
    };
  }

  function getSlides() {
    const { track } = getEls();
    if (!track) return [];
    return Array.from(track.querySelectorAll(".slide"));
  }

  function renderFinalSlider() {
    const { track, dots, now, total } = getEls();
    const slides = getSlides();

    if (!track || !slides.length) return;

    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;

    track.style.transform = "translateX(-" + (index * 100) + "%)";

    if (now) now.textContent = String(index + 1);
    if (total) total.textContent = String(slides.length);

    if (dots) {
      dots.innerHTML = "";

      slides.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = i === index ? "slider-dot active" : "slider-dot";
        dot.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
          index = i;
          renderFinalSlider();
        });
        dots.appendChild(dot);
      });
    }
  }

  function forceSliderControls() {
    const old = getEls();
    if (!old.track) return;

    if (old.prev) {
      const prev = old.prev.cloneNode(true);
      old.prev.replaceWith(prev);
      prev.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        index--;
        renderFinalSlider();
      });
    }

    if (old.next) {
      const next = old.next.cloneNode(true);
      old.next.replaceWith(next);
      next.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        index++;
        renderFinalSlider();
      });
    }

    const fresh = getEls();

    if (fresh.frame) {
      let startX = 0;

      fresh.frame.addEventListener("touchstart", (e) => {
        startX = e.changedTouches[0].clientX;
      }, { passive: true });

      fresh.frame.addEventListener("touchend", (e) => {
        const endX = e.changedTouches[0].clientX;
        const diff = endX - startX;

        if (Math.abs(diff) > 45) {
          if (diff < 0) index++;
          else index--;
          renderFinalSlider();
        }
      }, { passive: true });
    }

    const track = document.getElementById("sliderTrack");
    if (track) {
      const observer = new MutationObserver(() => {
        const slides = getSlides();
        if (index >= slides.length) index = slides.length - 1;
        renderFinalSlider();
      });

      observer.observe(track, { childList: true });
    }

    renderFinalSlider();
  }

  window.finalFinoyySliderFix = function () {
    forceSliderControls();
    renderFinalSlider();

    setTimeout(renderFinalSlider, 500);
    setTimeout(renderFinalSlider, 1200);
    setTimeout(renderFinalSlider, 2500);
    setTimeout(renderFinalSlider, 4000);
  };

  window.addEventListener("load", () => {
    setTimeout(window.finalFinoyySliderFix, 2200);
  });

  document.addEventListener("click", (e) => {
    if (e.target && e.target.id === "uploadPhotoBtn") {
      setTimeout(window.finalFinoyySliderFix, 1800);
      setTimeout(renderFinalSlider, 3500);
    }
  });
})();
</script>
'''

if "finalFinoyySliderFix" not in html:
    html = html.replace("</body>", js + "\n</body>", 1)
else:
    print("Patch final slider sudah ada.")

p.write_text(html)
print("Selesai. Counter slider akan baca semua slide, bukan cuma 6.")
