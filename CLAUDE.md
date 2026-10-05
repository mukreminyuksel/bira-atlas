# Bira Atlası — geliştirici notları

Türkçe bira kataloğu, stil rehberi ve kişisel bira günlüğü. Yayın: https://bira-atlas.pages.dev · Depo: `mukreminyuksel/bira-atlas` (`main`).

## Çalıştırma
- Yerel: `python3 -m http.server 8000`; 18 yaş onayı için `localStorage.setItem('bira_yas','1')`.
- **Katalog elle değil, araştırma dosyalarından üretilir:** `python3 arastirma/derle.py` → `index.html` içindeki `DATA`, `AI_GROUPS`, `FAMOUS`, `COUNTRY_ORDER` bloklarını ve `data/*.json` dosyalarını yeniden yazar. Ham veriyi `arastirma/` altında düzenle, `derle.py`'yi çalıştır, sonra commit et. (`index.html`'deki bu blokları elle değiştirme; bir sonraki derlemede ezilir.)

## Yapı
- `arastirma/` — bölge bölge ham araştırma JSON'ları (`turkiye*.json`, `almanya-cekya.json`, …), `stiller.json` (88 stil), `magazin.json`, `karakterler.json` (kurgu karakterleri), `zenginler.json`, `topluluk.json`, `tur2-bilgi.json` (düzeltme/ödül/tadım ekleri), `veri.py` (birleştirme ve kademe mantığı), `SPEC.md`.
- `data/` — `fabrikalar.json`, `bolgeler.json`, `tadim.json`, `konumlar.json`, `stiller.json`, `brewpublar.json`, `tarihce.json`, `lisans.json` (Tarım ve Orman Bakanlığı bira üretim izni listesi, 4 Ekim 2026), ve ortak dosyalar.
- Türkiye bölümü: lisanslı üretim yalnızca 8 ilde (resmî liste); Ankara'daki tek tesis Anadolu Efes Kahramankazan. Craft üretici/marka eşleşmeleri `lisans.json` içinde, "(muhtemelen)" olanlar kesin değil.
- `scripts/gorsel.mjs` (bira görseli, `img/sise/`).
- Magazin gruplarında **kurgu karakterleri**: eserde gerçekten geçen içki "📺/📖/🎮 Ekranda/Sayfada/Oyunda", yakıştırma "😄 Bizce" ile başlar; bu ayrımı koru.

## Veri dosyaları ve betikler
- `data/fiyatlar.json` — fiyat kayıtları (kaynak, güven, tarih). Elle düzenleme; aylık görev `scripts/fiyat-guncelle.mjs` ile yazar (`sec` → araştırılacaklar, `uygula dosya.json` → güvenlik kontrolleriyle yazar; şüpheli değişimleri reddeder).
- `data/baglantilar.json` — üreticilerin resmî site ve sosyal medya bağlantıları. `scripts/baglanti.mjs` (`sec` / `ekle` / `yok` / `kontrol` / `sil`). Yalnızca **resmî** hesaplar.
- `data/satis.json` — "Nereden Alınır" (yasal not, zincir, duty-free, butik); `data/topluluk.json` — kulüp, grup, festival, kanallar.

## Genel kurallar (bütün atlas siteleri için)
- **Dil:** Site metinleri, commit mesajları ve kullanıcıyla yazışma **Türkçe**. Kod ve değişken adları mevcut dosyadaki dile uysun.
- **Tek dosyalık uygulama:** Arayüz ve mantık `index.html` içinde (satır içi `<script>`); ortak yardımcılar `raf.js`. Derleme adımı yok. Sözdizimi kontrolü: `node -e "const s=require('fs').readFileSync('index.html','utf8');[...s.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].forEach(x=>new Function(x[1]));console.log('ok')"` (**non-greedy** regex; sayfada birden fazla `<script>` var).
- **Önbellek:** Sayfa ya da veri değiştirince `sw.js` içindeki `CACHE` adındaki sürüm numarasını artır (ör. `…-v38` → `…-v39`). Artırmazsan kullanıcılar eski sürümü görür.
- **Yayın:** `main`'e push = Cloudflare Pages otomatik yayın (build komutu yok, çıktı dizini `/`). PR gerekmez. Veri deposu KV bağlaması `wrangler.toml` içinde, adı `VERI`.
- **Sunucu tarafı:** `api/*.ts` platformdan bağımsız çekirdek, `functions/api/*.ts` Cloudflare katmanı (KV: `api/kv.ts`). Uç noktalar: `/api/sync` (bulut kodu + telefon/PIN), `/api/gece` (tadım geceleri), `/api/kulup` (kulüpler), `/api/barkod` (Raf Asistanı barkod sözlüğü). Yerelde denemek için `npx wrangler pages dev .`; saf mantık testi için `node --experimental-strip-types` ile `api/*.ts` içindeki `isle(req, depo)` bellek içi sahte depoyla çağrılabilir.
- **Gizlilik ilkeleri (bozma):** Telefon ve PIN düz metin saklanmaz (SHA-256 özeti); bulut kodu ve PIN ekranda varsayılan **gizli** (👁 düğmesi); tadım gecesinde başkalarının puanı oylama bitmeden gizli; GoatCounter çerezsiz sayaçtır, kişisel veri yok.
- **Veri dürüstlüğü (en önemli kural):**
  - Uydurma bilgi, fiyat, puan ya da ödül **yok**. Emin olunmayan alan boş bırakılır; fiyatı kaynaksız olan "tahmin" diye işaretlenir.
  - Gerçek kişiler hakkında yalnızca kamuya açık ve kaynağı gösterilebilen bilgi. Özel hayat, sağlık, bağımlılık, paparazzi/özel fotoğraftan çıkarım **yok**. Türkiye'den yaşayan gerçek kişi (iş insanı, ünlü) magazin listelerine eklenmez.
  - Untappd, BeerAdvocate, RateBeer, Whiskybase, Vivino, CellarTracker gibi sitelerden veri **kazınmaz**.
  - Giriş, captcha, bot koruması ya da yaş doğrulama kapısı olan sayfalar **aşılmaz**; açılmıyorsa atlanır.
  - Türk sitelerini okurken `WebFetch` çalışmaz: `curl -sL -m 25 -A 'Mozilla/5.0' URL` kullan.
  - Türkiye'de alkolün internetten tüketiciye satışı yasaktır: "internetten satın al" bağlantısı verilmez; yalnızca fiziksel mağaza, duty-free ve markanın kendi sitesi.
- **Commit mesajı:** Türkçe, ne ve neden. Sonuna şu iki satır eklenir (yapay zekâ ile yapılan işlerde):
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  Claude-Session: <oturum bağlantısı>
  ```
- **Otomatik görevler (Claude Routines) bu depolara kendiliğinden push eder:** fiyat (ayın 1-6'sı, siteye göre), görseller (3-4'ü, viski ve bira), üretici bağlantıları (ayın 5'i, hepsi). **Çalışmaya başlamadan önce `git pull`.** Bu görevler yalnızca kendi veri dosyasına dokunur (`data/fiyatlar.json`, `data/gorseller.json` + `img/`, `data/baglantilar.json`).
- **Kardeş siteler:** viski-atlas, bira-atlas, raki-atlas, sarap-atlas (hepsi `*.pages.dev`). Ortak parçalar (api, raf.js, kardeş bağlantı kutusu, göz düğmesi, filtre yapıları) siteler arasında kopyadır; birinde yapılan ortak bir düzeltme genelde diğerlerine de gerekir. Yol haritası: `docs/ONERILER.md`.
- **localStorage anahtarları site önekli** (`viski_`, `bira_`, `raki_`, `sarap_`); ayrı alan adlarında çakışmaz ama önekleri değiştirme, kayıtlı kullanıcı verisi kaybolur.
