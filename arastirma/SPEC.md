# Bira Atlası — veri araştırma şartnamesi

"Bira Atlası", Türkiye'deki bira meraklıları için Türkçe bir bira kataloğu (kardeş site: viski-atlas.netlify.app).
Bugünün tarihi: Ekim 2026. Her ajan kendisine verilen BÖLGE için aşağıdaki JSON dosyasını üretir.

## Kurallar
- Gerçek, şu an üretilen (ya da yakın zamana kadar üretilmiş, tanınmış) biralar. Uydurma bira, uydurma fabrika YOK.
- Web araması (WebSearch) ve sayfa okuma (WebFetch) kullan. Yaş doğrulama kapılarını, bot korumasını
  aşmaya çalışma; Untappd/RateBeer/BeerAdvocate'i kazıma (scrape) — arama sonuçlarındaki bilgileri ve
  üretici sitelerini kullan. Emin olmadığın alanı boş bırak ya da `"guven":"tahmin"` işaretle.
- Tüm açıklamalar TÜRKÇE, kısa ve doğal. Marka/bira adları özgün yazımıyla.
- Seçim ölçütü: (1) Türkiye'de bulunabilenler öncelikli (Migros, Carrefour, Macrocenter, Getir, tekel, craft
  dükkanları/birahaneler), (2) dünyaca bilinen klasikler ve stil referansları, (3) meraklının "mutlaka dene"
  listesindeki ikonlar. Her stil ailesinden temsil olsun.

## Çıktı dosyası
`/tmp/claude-0/-home-user-viski-atlas/2a88b075-3c7c-5c77-9d4f-349a62689e42/scratchpad/bira/<dosya>.json`
Geçerli JSON (yorum yok). Yazdıktan sonra `python3 -c "import json;json.load(open('...'))"` ile doğrula.

```json
{
  "biralar": [
    {
      "id": "kucuk-harf-tireli-benzersiz",        // ör. "weihenstephaner-hefeweissbier"
      "ad": "Weihenstephaner Hefeweissbier",
      "fab": "Weihenstephan",                      // bira fabrikası (kartlarla aynı yazım)
      "ulke": "Almanya",                           // Türkçe ülke adı
      "bolge": "Bavyera",                          // ülke içi bölge/şehir (harita ve ağaç için)
      "stil": "Hefeweizen",                        // özgün stil adı (BJCP'ye yakın)
      "aile": "Buğday",                            // AŞAĞIDAKİ LİSTEDEN BİRİ
      "abv": 5.4,
      "ibu": 14,                                   // biliniyorsa, yoksa alanı yazma
      "hacim": 50,                                 // cl, Türkiye'de/en yaygın satılan ambalaj
      "tl": 145,                                   // Ekim 2026 Türkiye yaklaşık raf fiyatı (o hacim için, TL)
      "fiyatTur": "tr_raf",                        // tr_raf (TR mağaza/market), tr_craft (TR craft dükkan/birahane perakende), tahmin (TR yoksa yurt dışı fiyat × kur ya da kıyas)
      "fiyatKaynak": "https://...",                // fiyatı gördüğün sayfa (tahmin ise boş)
      "bul": "market",                             // market | tekel | craft | zor | yurtdisi
      "puan": 88,                                  // 70-100, eleştirmen + topluluk konsensüsünü yansıtan editoryal puan
      "filtresiz": 1,                              // filtrelenmemiş/bulanık ise 1 (hefeweizen, NEIPA, kellerbier, şişede mayalı Belçika...)
      "uz": "",                                    // önemli ödül/liste notu: "World Beer Cup 2024 altın", "RateBeer en iyi 100" vb. (kısa)
      "not": "Muz ve karanfil; dünyanın en eski fabrikasından buğday klasiği"   // ≤ 90 karakter
    }
  ],
  "fabrikalar": {
    "Weihenstephan": {"k": 1040, "s": "Bavyera eyaleti", "y": "Freising, Bavyera", "stil": "Bavyera buğday ve lager", "h": "2-3 cümlelik kısa hikâye"}
  },
  "bolgeler": {
    "Almanya|Bavyera": {"k": "bölgenin bira karakteri, 2-3 cümle", "t": "kısa tarih/bilgi", "i": "yeni başlayana ipucu", "konum": [48.4, 11.7]}
  },
  "konumlar": { "Weihenstephan": [48.395, 11.728] },      // fabrika → [enlem, boylam], şehir düzeyi yeter
  "tadim": {
    "weihenstephaner-hefeweissbier": {"b": "burun", "d": "damak", "f": "bitiş", "s": "servis: bardak, sıcaklık, yemek eşleşmesi"}
  }
}
```

### `aile` değerleri (yalnızca bunlar)
`Lager & Pilsner` · `Koyu Lager & Bock` · `Buğday` · `Pale Ale & IPA` · `Belçika & Manastır` ·
`Stout & Porter` · `Ekşi & Vahşi` · `İngiliz & İrlanda Ale` · `Güçlü & Fıçı Yıllanmış` · `Özel & Diğer`

### Hedefler (bölge başına)
- `biralar`: verilen sayı kadar (±10%).
- `fabrikalar`: listedeki her `fab` için bir kart (emin olunan alanlar).
- `bolgeler`: listedeki her `ulke|bolge` için rehber + yaklaşık merkez konumu.
- `konumlar`: her fabrika için.
- `tadim`: en önemli/popüler biraların en az %40'ı için.

Fiyat notu: Türkiye'de ÖTV yüzünden fiyatlar hızlı değişir; "2026 bira fiyatları", "Migros bira", "Carrefour bira"
gibi aramalarla en güncel rakamı bul. Bulamazsan benzer ürünlerden makul tahmin yaz ve `fiyatTur:"tahmin"`.
Bitirince son mesajında: kaç bira, kaç fabrika, kaç tanesinin fiyatı gerçek kaynaklı (tahmin olmayan) — kısa özet.
