from pathlib import Path

p = Path("public/index.html")
html = p.read_text()

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
      background: rgba(255,255,255,.86);
      box-shadow: 0 24px 70px rgba(255,79,154,.22);
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

    .key-card input,
    .upload-row input {
      width: 100%;
      border: 0;
      outline: 0;
      padding: 14px 15px;
      border-radius: 18px;
      background: white;
      color: #5a2b42;
      font-weight: 800;
      margin-bottom: 10px;
    }

    .key-card button,
    .upload-btn,
    .gallery-action-btn {
      border: 0;
      cursor: pointer;
      border-radius: 999px;
      font-weight: 950;
    }

    .key-card button,
    .upload-btn {
      width: 100%;
      padding: 14px 16px;
      color: white;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
    }

    .key-error,
    .upload-status {
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
      background: rgba(255,255,255,.84);
      box-shadow: 0 16px 36px rgba(255,79,154,.12);
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
      background: rgba(255,255,255,.9);
      color: #bd3b7b;
      box-shadow: 0 10px 24px rgba(255,79,154,.16);
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
    html = html.replace('        <div class="slider-wrap">', upload_panel + '\n        <div class="slider-wrap">', 1)

p.write_text(html)
print("Patch 1 selesai: CSS, key lock, upload panel masuk.")
