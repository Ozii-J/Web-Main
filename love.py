# -*- coding: utf-8 -*-
"""
Web ajakan jalan untuk pacar - versi kucing & love
Cara pakai:
    python -m pip install flask
    python app.py
Buka http://127.0.0.1:5000
"""
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ====== UBAH BAGIAN INI ======
NAMA_PACAR = "Eka"
NAMA_KAMU = "Ozii"
NOMOR_WA = "6282241190292"          # nomor kamu, format 62..., tanpa + dan spasi
PILIHAN_TEMPAT = ["Makan malam 🍜", "Nonton bioskop 🍿", "Kopi & ngobrol ☕", "Jalan-jalan sore 🌇"]
PILIHAN_WAKTU = ["Sabtu sore", "Sabtu malam", "Minggu pagi", "Minggu sore"]
PESAN_PEMBUKA = "Udah lama kita nggak keluar berdua. Sabtu ini kosong nggak? 🥺"
# =============================

PAGE = """
<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>💌 Ada yang mau ngajak {{ nama }} jalan</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root{ --bg:#f3e3ee; --ink:#2a1a33; --paper:#fff8f2; --pink:#e8476a; --teal:#1f7a7a; }
  *{box-sizing:border-box}
  html,body{height:100%;margin:0}
  body{
    background:var(--bg); color:var(--ink);
    font-family:"Bricolage Grotesque",system-ui,sans-serif;
    display:grid; place-items:center; padding:20px; overflow-x:hidden;
  }
  .ticket{
    width:min(440px,100%); background:var(--paper); border-radius:18px; position:relative; z-index:2;
    box-shadow:0 18px 40px rgba(42,26,51,.18);
  }
  .ticket::before,.ticket::after{
    content:""; position:absolute; top:52%; width:28px; height:28px; border-radius:50%;
    background:var(--bg); transform:translateY(-50%);
  }
  .ticket::before{left:-14px} .ticket::after{right:-14px}
  .top{padding:28px 28px 22px; text-align:center}
  .bottom{padding:24px 28px 30px; border-top:2px dashed #d9bfd0; min-height:190px}
  .cat{font-size:5rem; line-height:1; display:block; margin-bottom:6px; transition:transform .2s}
  .cat.pop{transform:scale(1.25) rotate(-8deg)}
  h1{font-size:2rem; line-height:1.15; margin:0 0 10px; font-weight:800}
  p{margin:0; line-height:1.5}
  .small{font-size:.9rem; opacity:.7; margin-bottom:8px}
  .row{display:flex; gap:12px; flex-wrap:wrap; justify-content:center; position:relative; min-height:56px}
  button,.btn{
    font:inherit; font-weight:600; border:0; border-radius:12px; padding:14px 22px;
    cursor:pointer; text-decoration:none; display:inline-block; text-align:center;
  }
  .yes{background:var(--pink); color:#fff; font-size:1.1rem; transition:transform .15s}
  .no{background:#e6d6e0; color:var(--ink)}
  .no.run{position:fixed; z-index:5; transition:left .15s, top .15s}
  button:focus-visible,select:focus-visible,.btn:focus-visible{outline:3px solid var(--teal); outline-offset:2px}
  label{display:block; font-weight:600; margin:14px 0 6px}
  select{width:100%; font:inherit; padding:12px; border-radius:10px; border:2px solid #d9bfd0; background:#fff}
  .wa{background:var(--teal); color:#fff; margin-top:18px; width:100%}
  .hidden{display:none}
  .counter{font-size:.95rem; margin-top:14px; min-height:1.4em; text-align:center; font-weight:600}
  .plan-title{text-align:center; font-size:1.2rem}

  /* hati & kucing melayang di latar */
  .float{position:fixed; bottom:-60px; z-index:1; pointer-events:none; animation:up linear forwards}
  @keyframes up{ to{ transform:translateY(-115vh) rotate(25deg); opacity:0 } }
  @media (prefers-reduced-motion: reduce){ .float{display:none} .cat,.yes{transition:none} }
</style>
</head>
<body>
<main class="ticket">
  <section class="top">
    <span class="cat" id="cat">😺</span>
    <p class="small">💌 Untuk {{ nama }}, dari {{ kamu }}</p>
    <h1>Jalan berdua, yuk? 💕</h1>
    <p>{{ pembuka }}</p>
  </section>

  <section class="bottom" id="ask">
    <div class="row" id="row">
      <button class="yes" id="yes">Mau dong 😻</button>
      <button class="no" id="no">Nggak 🙄</button>
    </div>
    <p class="counter" id="counter">Ada pacarmu yang lagi nungguin jawabanmu 🐾</p>
  </section>

  <section class="bottom hidden" id="plan">
    <p class="plan-title"><strong>Yeay!! Pacarmu jingkrak-jingkrak 🎉🐱</strong><br>Tinggal pilih rencananya ya</p>
    <label for="tempat">Mau ke mana? 🗺️</label>
    <select id="tempat">{% for t in tempat %}<option>{{ t }}</option>{% endfor %}</select>
    <label for="waktu">Kapan? 🕒</label>
    <select id="waktu">{% for w in waktu %}<option>{{ w }}</option>{% endfor %}</select>
    <a class="btn wa" id="send" href="#">Kirim jawabanmu lewat WhatsApp 💬</a>
  </section>
</main>

<script>
const NOMOR = "{{ nomor }}";
const no = document.getElementById('no'), yes = document.getElementById('yes');
const cat = document.getElementById('cat'), counter = document.getElementById('counter');

// makin sering klik "Nggak", pacarmu makin sedih
const moods = [
  ["😿", "Yakin nih? Kucingnya mulai sedih... 🥺"],
  ["🙀", "Eh tombolnya kabur lho! 🏃"],
  ["😾", "Kucingnya ngambek 😤"],
  ["😭", "Hiks... kucingnya nangis 💔"],
  ["🥹", "Udah, pencet 'Mau dong' aja, please 🥺👉👈"]
];
let tries = 0;

function sparkle(chars, n){
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce) return;
  for(let i=0;i<n;i++){
    const s = document.createElement('span');
    s.className = 'float';
    s.textContent = chars[Math.floor(Math.random()*chars.length)];
    s.style.left = Math.random()*100 + 'vw';
    s.style.fontSize = (18 + Math.random()*28) + 'px';
    s.style.animationDuration = (5 + Math.random()*5) + 's';
    document.body.appendChild(s);
    setTimeout(() => s.remove(), 10500);
  }
}
sparkle(['💕','💗','🐱','💖','🐾'], 10);
setInterval(() => sparkle(['💕','💗','🐱','💖','🐾','😻'], 1), 900);

function dodge(e){
  e.preventDefault();
  const m = moods[Math.min(tries, moods.length-1)];
  tries++;
  cat.textContent = m[0]; counter.textContent = m[1];
  cat.classList.add('pop'); setTimeout(() => cat.classList.remove('pop'), 200);
  no.classList.add('run');
  const pad = 16, w = no.offsetWidth, h = no.offsetHeight;
  no.style.left = pad + Math.random()*(innerWidth - w - 2*pad) + 'px';
  no.style.top  = pad + Math.random()*(innerHeight - h - 2*pad) + 'px';
  // tombol "Mau" makin besar, biar makin menggoda
  yes.style.transform = 'scale(' + Math.min(1 + tries*0.12, 1.7) + ')';
}
no.addEventListener('mouseenter', dodge);
no.addEventListener('touchstart', dodge, {passive:false});
no.addEventListener('click', dodge);

yes.addEventListener('click', () => {
  no.classList.add('hidden');
  document.getElementById('ask').classList.add('hidden');
  document.getElementById('plan').classList.remove('hidden');
  cat.textContent = '😻';
  sparkle(['💖','💕','😻','🎉','🐱','✨','💗'], 40);
  updateLink();
});
function updateLink(){
  const t = document.getElementById('tempat').value, w = document.getElementById('waktu').value;
  const text = "Aku mau! 😻💕 Kita " + t.toLowerCase() + " ya, " + w.toLowerCase() + ". 🐾";
  document.getElementById('send').href = "https://wa.me/" + NOMOR + "?text=" + encodeURIComponent(text);
}
document.getElementById('tempat').addEventListener('change', updateLink);
document.getElementById('waktu').addEventListener('change', updateLink);
</script>
</body>
</html>
"""


@app.route("/")
def index():
    # ?untuk=Nama untuk mengganti nama lewat link, contoh: /?untuk=Dinda
    nama = request.args.get("untuk", NAMA_PACAR)
    return render_template_string(
        PAGE, nama=nama, kamu=NAMA_KAMU, nomor=NOMOR_WA,
        pembuka=PESAN_PEMBUKA, tempat=PILIHAN_TEMPAT, waktu=PILIHAN_WAKTU,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)