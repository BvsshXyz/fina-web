from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

# Tambah Supabase SDK
sdk = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n'
if "@supabase/supabase-js" not in html:
    html = html.replace("  <script>", "  " + sdk + "  <script>", 1)

css = r'''
    .key-lock {
      position: fixed;
      inset: 0;
      z-index: 9999999;
      display: grid;
      place-items: center;
      padding: 20px;
      background: linear-gradient(135deg, #fff7fb, #ffddeb);
    }

    .key-lock.hide {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .key-card {
      width: min(92vw, 420px);
      padding: 28px 22px;
      border-radius: 34px;
      text-align: center;
      background: rgba(255, 255, 255, .82);
      box-shadow: 0 24px 70px rgba(255, 79, 154, .22);
    }

    .key-icon {
      width: 74px;
      height: 74px;
      margin: 0 auto 16px;
      display: grid;
      place-items: center;
      border-radius: 24px;
      color: white;
      font-size: 2rem;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
    }

    .key-card h2 {
      color: #3d1d2e;
      font-size: 2rem;
      margin-bottom: 10px;
    }

    .key-card p {
      color: var(--muted);
      font-weight: 700;
      line-height: 1.6;
      margin-bottom: 16px;
    }

    .key-card input {
      width: 100%;
      border: 0;
      outline: 0;
      padding: 15px 16px;
      border-radius: 20px;
      background: white;
      color: #5a2b42;
      font-weight: 850;
      font-size: 1rem;
      margin-bottom: 12px;
    }

    .key-card button,
    .upload-btn,
    .gallery-action-btn {
      border: 0;
      cursor: pointer;
      border-radius: 999px;
      font-weight: 950;
    }

    .key-card button {
      width: 100%;
      padding: 14px 16px;
      color: white;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
    }

    .key-error {
      min-height: 24px;
      margin-top: 10px;
      color: #e6377d;
      font-weight: 850;
    }

    .upload-panel {
      position: relative;
      z-index: 5;
      max-width: 760px;
      margin: 0 auto 16px;
      padding: 16px;
      border-radius: 28px;
      background: rgba(255, 255, 255, .82);
      box-shadow: 0 16px 36px rgba(255, 79, 154, .12);
    }

    .upload-panel h3 {
      color: #bd3b7b;
      margin-bottom: 8px;
    }

    .upload-panel p {
      color: var(--muted);
      font-weight: 700;
      line-height: 1.5;
      margin-bottom: 12px;
      font-size: .95rem;
    }

    .upload-row {
      display: grid;
      gap: 10px;
    }

    .upload-row input {
      width: 100%;
      border: 0;
      outline: 0;
      padding: 13px 14px;
      border-radius: 18px;
      background: white;
      color: #5a2b42;
      font-weight: 750;
    }

    .upload-btn {
      padding: 13px 16px;
      color: white;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
    }

    .upload-status {
      min-height: 22px;
      color: #bd3b7b;
      font-weight: 850;
      margin-top: 10px;
    }
css += r'''
    .photo-tools {
      position: absolute;
      left: 14px;
      right: 14px;
      bottom: 14px;
      z-index: 30;
      display: flex;
      gap: 8px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .gallery-action-btn {
      padding: 9px 12px;
      background: rgba(255, 255, 255, .9);
      color: #bd3b7b;
      box-shadow: 0 10px 24px rgba(255, 79, 154, .16);
      font-size: .88rem;
    }

    .gallery-action-btn.delete {
      color: #e6377d;
    }

    #galeri .slide {
      position: relative !important;
    }

    #galeri .slide img {
      cursor: zoom-in;
    }

    .slider-track {
      display: flex !important;
      transition: transform .45s ease !important;
    }

    .slider-track .slide {
      min-width: 100% !important;
      flex: 0 0 100% !important;
    }
'''

if ".key-lock" not in html:
    html = html.replace("</style>", css + "\n  </style>", 1)

lock_html = r'''
  <div class="key-lock" id="keyLock">
    <div class="key-card">
      <div class="key-icon">♡</div>
      <h2>Khusus Finoyy</h2>
      <p>Masukin key dulu ya. Yang bisa buka cuma yang punya key.</p>
      <input id="secretKeyInput" type="password" placeholder="Masukkan key rahasia">
      <button id="secretKeyBtn" type="button">Buka halaman</button>
      <div class="key-error" id="secretKeyError"></div>
    </div>
  </div>
'''

if 'id="keyLock"' not in html:
    html = html.replace("<body>", "<body>\n" + lock_html, 1)

upload_panel = r'''
        <div class="upload-panel">
          <h3>Unggah foto baru</h3>
          <p>Upload pap/random Finoyy di sini. Maksimal 10 MB per foto.</p>
          <div class="upload-row">
            <input type="file" id="photoUploadInput" accept="image/*">
            <input type="text" id="photoCaptionInput" placeholder="Caption opsional">
            <button class="upload-btn" id="uploadPhotoBtn" type="button">Unggah foto</button>
          </div>
          <div class="upload-status" id="uploadStatus"></div>
        </div>
'''

if 'id="photoUploadInput"' not in html:
    html = html.replace(
        '        <div class="slider-wrap">',
        upload_panel + '\n        <div class="slider-wrap">',
        1
    )

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
js += r'''
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

        const ext = (file.name.split(".").pop() || "jpg").replace(/[^a-z0-9]/gi, "");
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

if "const PRIVATE_KEY = \"finoyyxbayuu\";" not in html:
    html = html.replace("    function makeHeart() {", js + "\n\n    function makeHeart() {")

p.write_text(html)
print("Selesai. Supabase upload gallery sudah dipasang.")
