from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

js = r'''
    (() => {
      let index = 0;

      function els() {
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

      function slides() {
        const e = els();
        return e.track ? Array.from(e.track.querySelectorAll(".slide")) : [];
      }

      function render() {
        const e = els();
        const all = slides();
        if (!e.track || !all.length) return;

        if (index < 0) index = all.length - 1;
        if (index >= all.length) index = 0;

        e.track.style.transform = "translateX(-" + (index * 100) + "%)";

        if (e.now) e.now.textContent = String(index + 1);
        if (e.total) e.total.textContent = String(all.length);

        if (e.dots) {
          e.dots.innerHTML = "";
          all.forEach((_, i) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = i === index ? "slider-dot active" : "slider-dot";
            dot.addEventListener("click", () => {
              index = i;
              render();
            });
            e.dots.appendChild(dot);
          });
        }
      }

      function hardResetControls() {
        const e = els();
        if (!e.track) return;

        if (e.prev) {
          const prev2 = e.prev.cloneNode(true);
          e.prev.replaceWith(prev2);
          prev2.addEventListener("click", (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            index--;
            render();
          });
        }

        if (e.next) {
          const next2 = e.next.cloneNode(true);
          e.next.replaceWith(next2);
          next2.addEventListener("click", (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            index++;
            render();
          });
        }

        if (e.frame) {
          const frame2 = e.frame.cloneNode(true);
          e.frame.replaceWith(frame2);

          let startX = 0;

          frame2.addEventListener("touchstart", (ev) => {
            startX = ev.changedTouches[0].clientX;
          }, { passive: true });

          frame2.addEventListener("touchend", (ev) => {
            const endX = ev.changedTouches[0].clientX;
            const diff = endX - startX;

            if (Math.abs(diff) > 45) {
              if (diff < 0) index++;
              else index--;
              render();
            }
          }, { passive: true });
        }

        const freshTrack = document.getElementById("sliderTrack");
        if (freshTrack) {
          const obs = new MutationObserver(() => {
            const all = slides();
            if (index >= all.length) index = all.length - 1;
            render();
          });
          obs.observe(freshTrack, { childList: true });
        }

        render();
      }

      window.fixFinoyySlider = function () {
        hardResetControls();
        setTimeout(render, 300);
        setTimeout(render, 1000);
        setTimeout(render, 2500);
      };

      window.addEventListener("load", () => {
        setTimeout(window.fixFinoyySlider, 1800);
      });

      document.addEventListener("click", (ev) => {
        if (ev.target && ev.target.id === "uploadPhotoBtn") {
          setTimeout(window.fixFinoyySlider, 1800);
          setTimeout(render, 3200);
        }
      });
    })();
'''

if "fixFinoyySlider" not in html:
    html = html.replace("</script>", js + "\n  </script>", 1)

p.write_text(html)
print("Selesai. Kontrol slider lama ditimpa total.")
