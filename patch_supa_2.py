from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

js = r'''
    const PRIVATE_KEY = "finoyyxbayuu";
    const SUPABASE_URL = "https://mnxapzmboyzfcrfaknyr.supabase.co";
    const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ueGFwem1ib3l6ZmNyZmFrbnlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNjU2OTMsImV4cCI6MjA5Mzg0MTY5M30.rvd5AjvkUOpWn2S53yULRShbtuXguay1dvWBGdjXIgw";
    const SUPABASE_BUCKET = "finoyy";
    const MAX_UPLOAD_SIZE = 10 * 1024 * 1024;

    const supa = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

    const keyLock = document.getElementById("keyLock");
    const secretKeyInput = document.getElementById("secretKeyInput");
    const secretKeyBtn = document.getElementById("secretKeyBtn");
    const secretKeyError = document.getElementById("secretKeyError");

    function unlockSite() {
      if (keyLock) keyLock.classList.add("hide");
      localStorage.setItem("finoyy_private_key_ok", "yes");
    }

    if (localStorage.getItem("finoyy_private_key_ok") === "yes") {
      unlockSite();
    }

    if (secretKeyBtn) {
      secretKeyBtn.addEventListener("click", () => {
        const value = (secretKeyInput.value || "").trim();
        if (value === PRIVATE_KEY) {
          unlockSite();
        } else {
          secretKeyError.textContent = "Key salah, coba lagi ya.";
        }
      });
    }

    if (secretKeyInput) {
      secretKeyInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") secretKeyBtn.click();
      });
    }

    const uploadInput = document.getElementById("photoUploadInput");
    const uploadBtn = document.getElementById("uploadPhotoBtn");
    const uploadStatus = document.getElementById("uploadStatus");

    function sliderEls() {
      return {
        track: document.getElementById("sliderTrack"),
        dots: document.getElementById("sliderDots"),
        now: document.getElementById("slideNow"),
        total: document.getElementById("slideTotal")
      };
    }

    let galleryIndex = 0;

    function updateGallerySlider() {
      const els = sliderEls();
      if (!els.track) return;

      const slides = Array.from(els.track.querySelectorAll(".slide"));
      if (!slides.length) return;

      if (galleryIndex >= slides.length) galleryIndex = slides.length - 1;
      if (galleryIndex < 0) galleryIndex = 0;

      els.track.style.transform = "translateX(-" + (galleryIndex * 100) + "%)";

      if (els.now) els.now.textContent = String(galleryIndex + 1);
      if (els.total) els.total.textContent = String(slides.length);

      if (els.dots) {
        els.dots.innerHTML = "";
        slides.forEach((_, i) => {
          const dot = document.createElement("button");
          dot.type = "button";
          dot.className = i === galleryIndex ? "slider-dot active" : "slider-dot";
          dot.addEventListener("click", () => {
            galleryIndex = i;
            updateGallerySlider();
          });
          els.dots.appendChild(dot);
        });
      }
    }

    function addTools(slide, src, path) {
      if (!slide || slide.querySelector(".photo-tools")) return;

      const tools = document.createElement("div");
      tools.className = "photo-tools";

      const save = document.createElement("a");
      save.className = "gallery-action-btn";
      save.textContent = "Simpan";
      save.href = src;
      save.target = "_blank";
      save.download = path ? path.split("/").pop() : "foto-finoyy.jpg";
      tools.appendChild(save);

      if (path) {
        const del = document.createElement("button");
        del.type = "button";
        del.className = "gallery-action-btn delete";
        del.textContent = "Hapus";
        del.addEventListener("click", async (e) => {
          e.stopPropagation();
          if (!confirm("Hapus foto ini?")) return;

          del.textContent = "Menghapus...";
          const { error } = await supa.storage.from(SUPABASE_BUCKET).remove([path]);

          if (error) {
            alert("Gagal hapus: " + error.message);
            del.textContent = "Hapus";
            return;
          }

          slide.remove();
          updateGallerySlider();
        });

        tools.appendChild(del);
      }

      slide.appendChild(tools);
    }

    function setupStaticPhotos() {
      document.querySelectorAll("#galeri .slide img").forEach((img) => {
        addTools(img.closest(".slide"), img.src, "");
      });
    }

    async function loadUploadedPhotos() {
      const els = sliderEls();
      if (!els.track) return;

      const { data, error } = await supa.storage
        .from(SUPABASE_BUCKET)
        .list("", { limit: 100, sortBy: { column: "created_at", order: "desc" } });

      if (error) {
        if (uploadStatus) uploadStatus.textContent = "Gagal ambil foto: " + error.message;
        return;
      }

      document.querySelectorAll(".slide[data-uploaded='yes']").forEach((el) => el.remove());

      (data || []).filter(x => x.name).forEach((item) => {
        const pub = supa.storage.from(SUPABASE_BUCKET).getPublicUrl(item.name);
        const url = pub.data.publicUrl;

        const slide = document.createElement("div");
        slide.className = "slide";
        slide.dataset.uploaded = "yes";
        slide.innerHTML = '<img src="' + url + '" alt="Foto upload Finoyy">';

        addTools(slide, url, item.name);
        els.track.appendChild(slide);
      });

      setupStaticPhotos();
      updateGallerySlider();
    }

    if (uploadBtn) {
      uploadBtn.addEventListener("click", async () => {
        const file = uploadInput && uploadInput.files ? uploadInput.files[0] : null;

        if (!file) {
          uploadStatus.textContent = "Pilih foto dulu ya.";
          return;
        }

        if (!file.type.startsWith("image/")) {
          uploadStatus.textContent = "Yang boleh diunggah cuma foto.";
          return;
        }

        if (file.size > MAX_UPLOAD_SIZE) {
          uploadStatus.textContent = "Foto kebesaran. Maksimal 10 MB.";
          return;
        }

        uploadBtn.disabled = true;
        uploadBtn.textContent = "Mengunggah...";
        uploadStatus.textContent = "Lagi upload foto...";

        const ext = (file.name.split(".").pop() || "jpg").replace(/[^a-z0-9]/gi, "") || "jpg";
        const filename = "foto-" + Date.now() + "." + ext;

        const { error } = await supa.storage
          .from(SUPABASE_BUCKET)
          .upload(filename, file, {
            cacheControl: "3600",
            upsert: false,
            contentType: file.type
          });

        uploadBtn.disabled = false;
        uploadBtn.textContent = "Unggah foto";

        if (error) {
          uploadStatus.textContent = "Upload gagal: " + error.message;
          return;
        }

        uploadStatus.textContent = "Foto berhasil diunggah ♡";
        uploadInput.value = "";

        await loadUploadedPhotos();
      });
    }

    setupStaticPhotos();
    loadUploadedPhotos();
'''

if 'const PRIVATE_KEY = "finoyyxbayuu";' not in html:
    html = html.replace("    function makeHeart() {", js + "\n\n    function makeHeart() {")
else:
    print("JS Supabase sudah ada, tidak ditambah lagi.")

p.write_text(html)
print("Patch 2 selesai: JS Supabase masuk.")
