from pathlib import Path
import re

p = Path("public/index.html")
html = p.read_text()

# Ganti nama menu Quotes jadi Pesan
html = html.replace('data-page="quotes">Quotes', 'data-page="quotes">Pesan')

# Ganti tombol beranda "Buka quotes"
html = html.replace('Buka quotes', 'Baca pesan')

# Ganti section Tentang Dia
new_tentang = r'''
    <section class="page" id="tentang">
      <div class="panel">
        <div class="head">
          <small>Tentang Dia</small>
          <h2>Ini beberapa hal kecil tentang Finoyy</h2>
        </div>

        <div class="cards">
          <div class="card">
            <div class="icon">🌷</div>
            <h3>Nama panggilannya</h3>
            <p>
              Dia bisa dipanggil Fina, Pina, Pin, atau Finoyy. Tapi dari semua
              panggilan itu, tetap orangnya sama: lucu, manis, dan punya tempat
              sendiri di hati Bayuu.
            </p>
          </div>

          <div class="card">
            <div class="icon">🍜</div>
            <h3>Makanan favorit</h3>
            <p>
              Fina suka bakso, mie yeyenn, dan seblak. Jadi kalau suatu hari
              dia bilang pengen jajan, tiga nama ini wajib masuk daftar pertama.
            </p>
          </div>

          <div class="card">
            <div class="icon">🧋</div>
            <h3>Minuman favorit</h3>
            <p>
              Minuman favoritnya boba milk tea. Minuman manis buat orang yang
              juga manis, walaupun kadang suka bilang “hmm” atau “ga”.
            </p>
          </div>

          <div class="card">
            <div class="icon">💗</div>
            <h3>Warna favorit</h3>
            <p>
              Warna favoritnya pinkkyy. Makanya halaman ini dibuat penuh pink,
              biar rasanya dekat sama hal yang dia suka.
            </p>
          </div>

          <div class="card">
            <div class="icon">🎮</div>
            <h3>Hobby</h3>
            <p>
              Hobby Fina itu main game dan tidur. Simpel, tapi tetap lucu kalau
              itu tentang dia.
            </p>
          </div>

          <div class="card">
            <div class="icon">🤍</div>
            <h3>Hal kecil tentang dia</h3>
            <p>
              Dari cara dia ngomong, cara dia perhatian, sampai hal random yang
              dia lakuin, semuanya punya versi lucunya sendiri.
            </p>
          </div>
        </div>
      </div>
    </section>
'''

html, n1 = re.subn(
    r'\n    <section class="page" id="tentang">.*?\n    </section>',
    '\n' + new_tentang,
    html,
    count=1,
    flags=re.S
)

# Ganti section Quotes jadi Pesan buat Bayuu
new_pesan = r'''
    <section class="page" id="quotes">
      <div class="panel">
        <div class="head">
          <small>Pesan buat Bayuu</small>
          <h2>Dari Finoyy, buat Bayuu</h2>
        </div>

        <div class="letter">
          <h2>Makasih banyak, sayang 🤍</h2>
          <p>
            Makasii banyakk sayangg untukk semuaa hall kecil ataupunn besarr
            yang udahh kamuu usahainn buat akuu, untuk sabar mu, untukk kabarr
            yangg selalu kamuu usahain. Dari situ aku ngerasaa diperjuangkan.
            <br><br>
            Tauu gaa kebahagianku di tahun inii apaa? Bersamamu dengan segala
            versii baikmuu. Tetepp samaa akuu okeii? Kitaa wujud in wishh listt
            kitaa barengg.
            <br><br>
            Makasii banyakk yaa sayangg untukk semuanyaa 🤍
          </p>
        </div>
      </div>
    </section>
'''

html, n2 = re.subn(
    r'\n    <section class="page" id="quotes">.*?\n    </section>',
    '\n' + new_pesan,
    html,
    count=1,
    flags=re.S
)

p.write_text(html)

print("Tentang Dia diganti:", bool(n1))
print("Quotes diganti jadi Pesan:", bool(n2))
