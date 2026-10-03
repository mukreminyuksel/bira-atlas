# 🍺 Bira Atlası

Türkiye odaklı, Türkçe bira kataloğu ve kişisel koleksiyon uygulaması — [Viski Atlası](https://viski-atlas.netlify.app)'nın kardeşi.

- **547 bira**, 53 ülke, ~300 bira fabrikası: Türkiye (Efes, Tuborg ve Gara Guzu, Pablo, 3 Kafadar, SOMX, DAS… gibi craft'lar), Almanya/Avusturya/Çekya, Belçika/Hollanda, Britanya/İrlanda, Kuzey Amerika ve dünya.
- Ülke → bölge → bira fabrikası → bira ağacı, harita, fabrika kartları, bölge rehberleri, ~240 tadım notu.
- Listeler: Uzman Top 50, AI Tercihleri, Filtresizler Top 50, Türkiye Katmanları, Fiyat Hareketleri, Magazin.
- Kişisel: Elimde/Hedef listesi, tadım notları, Gurme seviyesi (stil ailesi kapsama vb.), tat radarı, "bu akşam ne içsem?", bütçe önerisi, boşluk analizi, karşılaştırma.
- Sosyal (Netlify'da): telefon + PIN ile bulut kaydı, tadım geceleri, davetle girilen kulüpler. GitHub Pages'te bu bölümler "yakında" olarak görünür.

## Veri ve fiyat politikası
- Katalog, bölge bölge web araştırmasıyla hazırlandı (Ekim 2026). Puanlar eleştirmen ve topluluk konsensüsünü yansıtan editoryal puanlardır.
- Fiyatlar Türkiye perakende referansıdır (belirtilen hacim için). Kaynağı bulunan fiyatlar `data/fiyatlar.json` içinde kaynak bağlantısıyla durur ve sitede "doğrulanmış" görünür; diğerleri tahmindir.
- `data/fiyatlar.json` sitede doğrudan GitHub'dan okunur; fiyat güncellemesi için yeniden yayın gerekmez.

## Yapı
- `index.html` — tek sayfalık uygulama (statik).
- `data/` — `fiyatlar.json`, `fabrikalar.json`, `bolgeler.json`, `tadim.json`, `konumlar.json`.
- `netlify/functions/` — `/api/sync` (bulut + telefon/PIN), `/api/gece` (tadım geceleri), `/api/kulup` (kulüpler); Netlify Blobs.
