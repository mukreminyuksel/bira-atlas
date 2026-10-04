# 🍺 Bira Atlası

Türkiye odaklı, Türkçe bira kataloğu ve kişisel bira günlüğü — [Viski Atlası](https://viski-atlas.netlify.app)'nın kardeşi.
Yayın: https://mukreminyuksel.github.io/bira-atlas/ (Cloudflare Pages'e taşınınca bulut/sosyal bölümler açılacak).

## İçerik
- **1150+ bira**, 74 ülke; Türkiye'den 150'ye yakın bira (Efes, Tuborg, Bomonti ve Gara Guzu, 3 Kafadar, SOMX, DAS, à santé, Kubau, Knidos… gibi craft'lar), KKTC.
- **88 stillik Türkçe Stil Rehberi**: renk (SRM), IBU, alkol aralığı, bardak, servis sıcaklığı, tarihçe, beklenen tatlar, sofra eşleşmesi; biraların çoğu bir stile bağlı.
- Fabrika kartları, ~180 bölge rehberi, 700+ tadım notu, 2024–2026 yarışma madalyaları (World Beer Cup, European Beer Star, Brussels Beer Challenge, World Beer Awards).
- **Türkiye Craft**: şehir şehir üreticiler, bira evleri, ev biracıları ve şehirlerin bira tarihi (Ankara AOÇ 1934 vb.).
- **Topluluk**: festivaller, kulüpler, Instagram/Facebook/forum/YouTube kanalları (aktiflik durumuyla).
- **Magazin**: ünlüler, bira yazarları, efsanevi hikâyeler, kurgu karakterleri ("📺/📖 eserde geçer" / "😄 bizce" ayrımıyla).

## Kişisel bölümler
- **Denedim / Deneyeceğim** listesi (bira günlüğü + alışveriş listesi), tadım notları ve kişisel puan.
- **Gurme & Pasaport**: 100 üzerinden bira gurme puanı (stil çeşitliliği, aile kapsama, ülke keşfi, kalite, zorlu stiller, Türk craft desteği, tadım notları) ve stil damgaları.
- **Bana Özel**: tat radarı, sıradaki bira önerisi, "bu akşam ne içsem?"; **Yemek & Bira** (15 sofra, her bira kartında "Yanında ne iyi gider?"); bütçe önerisi, boşluk analizi, karşılaştırma.
- Keşfet'te ülkeye ya da stile göre ağaç, harita, bulunabilirlik filtreleri (Türkiye'de bulunur / market / tekel / craft / nadiren / yurt dışı).
- Sosyal (sunuculu yayında): telefon + PIN ile tek giriş ve bulut kaydı, tadım geceleri, davetle girilen kulüpler.

## Veri ve fiyat politikası
- Katalog bölge bölge web araştırmasıyla hazırlandı (Ekim 2026); ham araştırma dosyaları `arastirma/` altında, katalog `python3 arastirma/derle.py` ile yeniden üretilir.
- Puanlar eleştirmen/topluluk konsensüsünü yansıtan editoryal puanlardır. Untappd/BeerAdvocate/RateBeer'den veri çekilmez.
- Fiyatlar Türkiye perakende referansıdır (belirtilen hacim için). Kaynaklı fiyatlar `data/fiyatlar.json`'da kaynak bağlantısıyla durur ve sitede "doğrulanmış" görünür; diğerleri tahmindir.
- Fiyatlar **her ay** otomatik güncellenir (Claude Routine, `scripts/fiyat-guncelle.mjs`); dosya sitede doğrudan GitHub'dan okunur, yeniden yayın gerekmez.
- Ziyaret istatistiği: GoatCounter (çerezsiz) — https://bira-atlas.goatcounter.com

## Yapı
- `index.html` — tek sayfalık uygulama (statik).
- `data/` — `fiyatlar.json`, `fabrikalar.json`, `bolgeler.json`, `tadim.json`, `konumlar.json`, `stiller.json`, `brewpublar.json`, `tarihce.json`, `topluluk.json`.
- `arastirma/` — bölge araştırmaları, magazin, karakterler, stiller ve `derle.py`.
- `api/` — sunucu mantığı (platformdan bağımsız): `/api/sync` (bulut + telefon/PIN), `/api/gece` (tadım geceleri), `/api/kulup` (kulüpler).
- `functions/api/` — Cloudflare Pages katmanı (Workers KV, bağlama adı `VERI`); `netlify/functions/` — Netlify katmanı (Netlify Blobs).
