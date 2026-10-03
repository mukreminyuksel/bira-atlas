# arastirma/ altındaki bölge dosyalarını birleştirip Bira Atlası verisini üretir: DATA satırları (JS) + data/*.json
import json, glob, os, re, collections, unicodedata

KOK = os.path.dirname(os.path.abspath(__file__))
HEDEF = '/home/user/bira-atlas'
BUGUN = '2026-10-03'

# Bira kaynak dosyaları (bölge araştırmaları + ekler); stiller/magazin/tur2 dosyaları ayrı okunur
BOLGE_DOSYALARI = ['turkiye.json', 'turkiye2.json', 'turkiye3.json', 'almanya-cekya.json', 'belcika-hollanda.json', 'britanya-irlanda.json',
                   'amerika.json', 'dunya.json', 'ek.json', 'stil-ek.json', 'genis-almanya.json', 'genis-belcika.json', 'genis-amerika.json', 'genis-dunya.json']

def yukle():
    biralar, fab, bol, kon, tad, trf = [], {}, {}, {}, {}, {}
    gor = set()
    for ad in BOLGE_DOSYALARI:
        f = os.path.join(KOK, ad)
        if not os.path.exists(f):
            continue
        d = json.load(open(f))
        d['biralar'] = [b for b in d.get('biralar', []) if b['id'] not in gor and not gor.add(b['id'])]
        biralar += d.get('biralar', [])
        fab.update(d.get('fabrikalar', {}))
        bol.update(d.get('bolgeler', {}))
        kon.update(d.get('konumlar', {}))
        tad.update(d.get('tadim', {}))
        trf.update(d.get('trFiyatlar', {}))
    return biralar, fab, bol, kon, tad, trf

def sade(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in s if not unicodedata.combining(c))).strip()

AILELER = ['Lager & Pilsner', 'Koyu Lager & Bock', 'Buğday', 'Pale Ale & IPA', 'Belçika & Manastır',
           'Stout & Porter', 'Ekşi & Vahşi', 'İngiliz & İrlanda Ale', 'Güçlü & Fıçı Yıllanmış', 'Özel & Diğer']

def uret():
    biralar, fab, bol, kon, tad, trf = yukle()
    # Türkiye ajanının ithal bira fiyatlarını (gerçek kaynaklı olanları) adla eşleştir
    trs = {sade(k): v for k, v in trf.items() if v.get('tur') == 'tr_raf' and v.get('tl')}
    for b in biralar:
        if b.get('fiyatTur') in ('tr_raf', 'tr_craft'):
            continue
        a = sade(b['ad'])
        for k, v in trs.items():
            if k == a or (len(k) > 6 and (k == a or a.startswith(k) and abs(len(a) - len(k)) < 6)):
                if '50 cl' in k and b.get('hacim') != 50:
                    continue
                b.update(tl=v['tl'], hacim=v.get('hacim') or b.get('hacim'), fiyatTur='tr_raf', fiyatKaynak=v.get('kaynak', ''),
                         bul='market' if v.get('bul') in (None, 'market') else v['bul'])
                break
    # Fabrika seviyesi: en iyi birasının puanına göre
    enIyi = collections.defaultdict(int)
    for b in biralar:
        enIyi[b['fab']] = max(enIyi[b['fab']], b.get('puan') or 0)
    def sev(f):
        p = enIyi[f]
        return 'Premium' if p >= 92 else '2' if p >= 86 else '3'
    BUL = {'market': 'kolay', 'tekel': 'tekel', 'craft': 'craft', 'zor': 'zor', 'yurtdisi': 'yurtdisi'}
    data = []
    for b in biralar:
        data.append({
            'id': b['id'], 'ad': b['ad'], 'dam': b['fab'], 'ulke': b['ulke'], 'bolge': b['bolge'], 'sev': sev(b['fab']),
            'tur': b['aile'] if b['aile'] in AILELER else 'Özel & Diğer', 'stil': b.get('stil', ''),
            'abv': b.get('abv') or 0, 'ibu': b.get('ibu') or 0, 'hacim': b.get('hacim') or 33, 'tl': b.get('tl') or 0,
            'bul': BUL.get(b.get('bul'), 'zor'), 'puan': b.get('puan') or 0, 'uz': b.get('uz', '') or '',
            'ai': 0, 'kat': 0, 'ncf': 1 if b.get('filtresiz') else 0, 'not': b.get('not', ''),
        })
    # AI tercihleri: her stil ailesinden Türkiye'de bulunabilirliği gözeterek en yüksek puanlılar (toplam 25)
    kota = {'Lager & Pilsner': 3, 'Koyu Lager & Bock': 2, 'Buğday': 3, 'Pale Ale & IPA': 3, 'Belçika & Manastır': 3,
            'Stout & Porter': 3, 'Ekşi & Vahşi': 2, 'İngiliz & İrlanda Ale': 2, 'Güçlü & Fıçı Yıllanmış': 2, 'Özel & Diğer': 2}
    kota['Özel & Diğer'] = 0
    ulas = {'kolay': 3, 'tekel': 3, 'craft': 2, 'zor': -2, 'yurtdisi': -5}
    AI = {}
    sira = 1
    for aile in AILELER:
        aday = sorted([d for d in data if d['tur'] == aile and d['ulke'] != 'Türkiye'], key=lambda d: -(d['puan'] + ulas[d['bul']] * 1.5))
        for d in aday[:kota[aile]]:
            d['ai'] = sira; AI[d['id']] = aile; sira += 1
    for d in sorted([d for d in data if d['ulke'] == 'Türkiye'], key=lambda d: -d['puan'])[:2]:
        d['ai'] = sira; AI[d['id']] = 'Türkiye'; sira += 1
    # Türkiye katmanları
    trde = [d for d in data if d['bul'] in ('kolay', 'tekel') and d['tl'] and d['ulke'] != 'Türkiye']
    k1 = sorted(trde, key=lambda d: -((d['puan'] - 70) / (d['tl'] / 100)))[:8]
    k1 += sorted([d for d in data if d['ulke'] == 'Türkiye' and d['tl'] and d['bul'] != 'yurtdisi'], key=lambda d: -((d['puan'] - 70) / (d['tl'] / 100)))[:7]
    for d in k1: d['kat'] = 1
    k2 = sorted([d for d in data if d['bul'] in ('kolay', 'tekel', 'craft') and not d['kat'] and d['puan'] >= 86 and d['tl']], key=lambda d: -d['puan'])[:14]
    for d in k2: d['kat'] = 2
    k3 = sorted([d for d in data if d['bul'] in ('craft', 'zor') and not d['kat'] and d['puan'] >= 92 and d['tl']], key=lambda d: -d['puan'])[:12]
    for d in k3: d['kat'] = 3
    # Gerçek kaynaklı fiyatlar → data/fiyatlar.json (sitede "doğrulanmış" görünür)
    fiy = {}
    for b in biralar:
        if b.get('fiyatTur') in ('tr_raf', 'tr_craft') and b.get('tl'):
            fiy[b['id']] = {'tl': b['tl'], 'tarih': BUGUN, 'tur': b['fiyatTur'], 'guven': 'orta', 'kaynak': b.get('fiyatKaynak', ''),
                            'not': 'İlk araştırma (arama özetlerinden)', 'gecmis': [[BUGUN, b['tl']]]}
    # Konumlar
    konum = {'_aciklama': "Harita konumları [enlem, boylam]. bolgeler: 'ülke|bölge' → bölge merkezi. damlar: bira fabrikası → yaklaşık konum.",
             'bolgeler': {k: v['konum'] for k, v in bol.items() if v.get('konum')}, 'damlar': kon}
    bolgeler = {'_aciklama': "Bölge rehberleri. Anahtar 'ülke|bölge'. k: karakter, t: bilgi, i: ipucu."}
    for k, v in bol.items():
        bolgeler[k] = {x: v[x] for x in ('k', 't', 'i') if v.get(x)}
    fabrikalar = {'_aciklama': "Bira fabrikası kartları. Anahtar = DATA'daki 'dam'. k: kuruluş, s: sahibi, y: yer, stil: ev stili, h: hikâye."}
    fabrikalar.update(fab)
    tadim = {'_aciklama': 'Tadım notları (b: burun, d: damak, f: bitiş, s: servis).'}
    tadim.update({k: v for k, v in tad.items() if any(x['id'] == k for x in data)})
    return data, AI, fiy, konum, bolgeler, fabrikalar, tadim

if __name__ == '__main__':
    data, AI, fiy, *_ = uret()
    print(len(data), 'bira;', len(fiy), 'gerçek fiyat;', len(AI), 'AI;', collections.Counter(d['kat'] for d in data))
