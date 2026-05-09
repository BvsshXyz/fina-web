from pathlib import Path
import re

p = Path("public/index.html")
html = p.read_text()

# Hapus judul tebal di pesan
html = html.replace('<h2>Makasih banyak, sayang 🤍</h2>', '')
html = html.replace('<h2>Makasih banyakk, sayang 🤍</h2>', '')
html = html.replace('<h2>Makasih banyak, sayang</h2>', '')

# CSS popup balasan
css = r'''
    .reply-open-btn {
      margin: 22px auto 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 0;
      cursor: pointer;
      padding: 13px 18px;
      border-radius: 999px;
      color: white;
      font-weight: 950;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
      box-shadow: 0 16px 34px rgba(255, 79, 154, .22);
      transition: .22s ease;
    }

    .reply-open-btn:active {
      transform: scale(.96);
    }

    .reply-modal {
      position: fixed;
      inset: 0;
      z-index: 999999;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background: rgba(55, 18, 38, .55);
      backdrop-filter: blur(12px);
    }

    .reply-modal.open {
      display: flex;
    }

    .reply-card {
      width: min(92vw, 520px);
      max-height: 82vh;
      overflow-y: auto;
      position: relative;
      padding: 28px 22px;
      border-radius: 34px;
      background:
        radial-gradient(circle at top right, rgba(255, 127, 184, .16), transparent 30%),
        rgba(255, 255, 255, .94);
      box-shadow: 0 28px 90px rgba(255, 79, 154, .34);
      animation: replyPop .28s ease both;
      text-align: center;
    }

    .reply-card:before {
      content: "♡";
      position: absolute;
      right: 18px;
      top: 10px;
      color: #ffd3e7;
      font-size: 4.8rem;
      font-weight: 950;
      line-height: 1;
      transform: rotate(14deg);
      pointer-events: none;
    }

    .reply-card h3 {
      position: relative;
      z-index: 2;
      color: #3d1d2e;
      font-size: clamp(1.8rem, 6vw, 2.6rem);
      line-height: 1;
      letter-spacing: -.055em;
      margin-bottom: 16px;
    }

    .reply-card p {
      position: relative;
      z-index: 2;
      color: var(--muted);
      line-height: 1.85;
      font-weight: 700;
      font-size: 1rem;
      text-align: center;
    }

    .reply-close {
      position: sticky;
      bottom: 0;
      z-index: 3;
      width: 100%;
      margin-top: 20px;
      border: 0;
      cursor: pointer;
      padding: 13px 16px;
      border-radius: 999px;
      color: white;
      font-weight: 950;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
      box-shadow: 0 14px 30px rgba(255, 79, 154, .22);
    }

    @keyframes replyPop {
      from {
        opacity: 0;
        transform: scale(.94) translateY(16px);
      }
      to {
        opacity: 1;
        transform: scale(1) translateY(0);
      }
    }
'''

if ".reply-modal" not in html:
    html = html.replace("</style>", css + "\n  </style>", 1)

# Tambahkan tombol lihat balasan setelah isi pesan Finoyy
if 'id="openReplyBtn"' not in html:
    html = html.replace(
        '''          </p>
        </div>
      </div>
    </section>''',
        '''          </p>

          <button class="reply-open-btn" id="openReplyBtn" type="button">Lihat balasan ♡</button>
        </div>
      </div>
    </section>''',
        1
    )

# Tambah modal sebelum footer
reply_modal = r'''
  <div class="reply-modal" id="replyModal">
    <div class="reply-card">
      <h3>Balasan dari Bayuu</h3>
      <p>
        Iyaa sama-sama sayang. Aku juga mau terima kasih sama kamu karena udah hadir
        di kehidupan aku sekarang. Aku bakal usahain kamu sampai kita benar-benar
        bisa bareng, sampai jadi keluarga 🥹
        <br><br>
        Aku bangga banget punya kamu. Aku pengen sampai akhir tetap sama kamu terus.
        Kita bakal wujudin wishlist kita bareng-bareng.
        <br><br>
        Makasih juga sayang buat semua hal yang udah kamu lakuin buat aku.
      </p>
      <button class="reply-close" id="closeReplyBtn" type="button">Tutup</button>
    </div>
  </div>
'''

if 'id="replyModal"' not in html:
    html = html.replace("\n  <footer>", "\n" + reply_modal + "\n  <footer>", 1)

# Tambah JS popup
js = r'''
    const openReplyBtn = document.getElementById("openReplyBtn");
    const replyModal = document.getElementById("replyModal");
    const closeReplyBtn = document.getElementById("closeReplyBtn");

    if (openReplyBtn && replyModal) {
      openReplyBtn.addEventListener("click", () => {
        replyModal.classList.add("open");
        document.body.style.overflow = "hidden";
      });
    }

    function closeReplyModal() {
      if (!replyModal) return;
      replyModal.classList.remove("open");
      document.body.style.overflow = "";
    }

    if (closeReplyBtn) {
      closeReplyBtn.addEventListener("click", closeReplyModal);
    }

    if (replyModal) {
      replyModal.addEventListener("click", (e) => {
        if (e.target === replyModal) closeReplyModal();
      });
    }
'''

if "const openReplyBtn" not in html:
    html = html.replace("    function makeHeart() {", js + "\n    function makeHeart() {", 1)

p.write_text(html)
print("Selesai. Judul tebal dihapus dan popup balasan Bayuu ditambahkan.")
