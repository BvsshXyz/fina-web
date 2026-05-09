from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

js = r'''
    (() => {
      let finalGalleryIndex = 0;
      let finalGalleryReady = false;

      function finalEls() {
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

      function finalSlides() {
        const { track } = finalEls();
        if (!track) return [];
        return Array.from(track.querySelectorAll(".slide"));
      }

      function finalRender() {
        const { track, dots, now, total } = finalEls();
        const slides = finalSlides();
        if (!track || !slides.length) return;

        if (finalGalleryIndex < 0) finalGalleryIndex = slides.length - 1;
        if (finalGalleryIndex >= slides.length) finalGalleryIndex = 0;

        track.style.transform = "translateX(-" + (finalGalleryIndex * 100) + "%)";

        if (now) now.textContent = String(finalGalleryIndex + 1);
        if (total) total.textContent = String(slides.length);

        if (dots) {
          dots.innerHTML = "";
          slides.forEach((_, i) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = i === finalGalleryIndex ? "slider-dot active" : "slider-dot";
            dot.addEventListener("click", () => {
              finalGalleryIndex = i;
              finalRender();
            });
            dots.appendChild(dot);
          });
        }
      }

      function finalBindSlider() {
        if (finalGalleryReady) {
          finalRender();
          return;
        }

        const els = finalEls();
        if (!els.track) return;

        finalGalleryReady = true;

        if (els.prev) {
          const newPrev = els.prev.cloneNode(true);
          els.prev.parentNode.replaceChild(newPrev, els.prev);
          newPrev.addEventListener("click", () => {
            finalGalleryIndex--;
            finalRender();
          });
        }

        if (els.next) {
          const newNext = els.next.cloneNode(true);
          els.next.parentNode.replaceChild(newNext, els.next);
          newNext.addEventListener("click", () => {
            finalGalleryIndex++;
            finalRender();
          });
        }

        let startX = 0;
        if (els.frame) {
          els.frame.addEventListener("touchstart", (e) => {
            startX = e.changedTouches[0].clientX;
          }, { passive: true });

          els.frame.addEventListener("touchend", (e) => {
            const endX = e.changedTouches[0].clientX;
            const diff = endX - startX;

            if (Math.abs(diff) > 45) {
              if (diff < 0) finalGalleryIndex++;
              else finalGalleryIndex--;
              finalRender();
            }
          }, { passive: true });
        }

        const observer = new MutationObserver(() => {
          const slides = finalSlides();
          if (finalGalleryIndex >= slides.length) finalGalleryIndex = slides.length - 1;
          finalRender();
        });

        observer.observe(els.track, { childList: true });

        finalRender();
      }

      window.addEventListener("load", () => {
        setTimeout(finalBindSlider, 700);
        setTimeout(finalRender, 1600);
        setTimeout(finalRender, 3000);
      });

      document.addEventListener("click", (e) => {
        if (e.target && e.target.id === "uploadPhotoBtn") {
          setTimeout(finalRender, 1500);
          setTimeout(finalRender, 3000);
        }
      });
    })();
'''

if "finalBindSlider" not in html:
    html = html.replace("</script>", js + "\n  </script>", 1)

p.write_text(html)
print("Selesai. Slider sekarang dipaksa baca semua foto upload.")
