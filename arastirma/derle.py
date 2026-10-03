# Araştırma dosyalarından kataloğu yeniden üretir:
#   index.html içindeki DATA, AI_GROUPS, FAMOUS, FLAGS, COUNTRY_ORDER, REP_CAT, REP_PROF blokları
#   data/fabrikalar.json, bolgeler.json, tadim.json, konumlar.json, stiller.json, brewpublar.json
#   data/fiyatlar.json'a yalnızca henüz kaydı olmayan kaynaklı fiyatlar eklenir (haftalık görevin kayıtları korunur)
# Kullanım: python3 arastirma/derle.py
import json, os, re, sys, collections
KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import veri

SITE = os.path.dirname(KOK)
HTML = os.path.join(SITE, 'index.html')
s = open(HTML, encoding='utf-8').read()

def blok(bas, son, yeni):
    global s
    i = s.index(bas); j = s.index(son, i) + len(son)
    s = s[:i] + yeni + s[j:]

def oku(ad, var=None):
    p = os.path.join(KOK, ad)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else var

data, AI, fiy, konum, bolgeler, fabrikalar, tadim = veri.uret()
ids = {d['id'] for d in data}

# --- 2. tur bilgi düzeltmeleri, ödüller, ek tadım notları ---
bilgi = oku('tur2-bilgi.json', {})
byid = {d['id']: d for d in data}
for dz in bilgi.get('duzeltme', []):
    d = byid.get(dz.get('id'))
    if d and dz.get('alan') in ('abv', 'ibu', 'stil', 'hacim') and dz.get('yeni') not in (None, ''):
        d[dz['alan']] = dz['yeni']
for od in bilgi.get('odul', []):
    d = byid.get(od.get('id'))
    if d and od.get('uz'):
        d['uz'] = od['uz'] if not d['uz'] else (d['uz'] if od['uz'] in d['uz'] else d['uz'] + ' · ' + od['uz'])
for k, v in bilgi.get('tadim', {}).items():
    if k in ids and k not in tadim:
        tadim[k] = {x: v[x] for x in ('b', 'd', 'f', 's') if v.get(x)}

# --- Stil eşleşmesi (stil rehberi) ---
stiller = oku('stiller.json', {})
esl = stiller.get('eslesme', {})
for d in data:
    if esl.get(d['id']):
        d['sid'] = esl[d['id']]

# --- DATA ---
satirlar = []
for ulke in sorted({d['ulke'] for d in data}):
    satirlar.append('// ===== ' + ulke.upper() + ' =====')
    satirlar += [json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ',' for d in data if d['ulke'] == ulke]
blok('const DATA = [', '\n];', 'const DATA = [\n' + '\n'.join(satirlar) + '\n];')
blok('const AI_GROUPS = ', ';\n', 'const AI_GROUPS = ' + json.dumps(AI, ensure_ascii=False) + ';\n')

# --- Bayraklar ve ülke sırası ---
ulkeler = sorted({d['ulke'] for d in data}, key=lambda u: -sum(1 for d in data if d['ulke'] == u))
ulkeler.remove('Türkiye'); ulkeler.insert(0, 'Türkiye')
blok("const COUNTRY_ORDER=", "\n", "const COUNTRY_ORDER=" + json.dumps(ulkeler, ensure_ascii=False) + ";\n")

# --- Magazin ---
mag = oku('magazin.json', {})
pid = {veri.sade(d['ad']): d['id'] for d in data}
TAKMA = {'chimay blue': 'Chimay Bleue (Grande Réserve)', 'cantillon gueuze 100 lambic bio': 'Cantillon Classic Gueuze',
         'paulaner original munchner hell': 'Paulaner Münchner Hell', 'iron maiden trooper': 'Robinsons Trooper'}
def bul_id(ad):
    a = veri.sade(TAKMA.get(veri.sade(ad), ad))
    if a in pid: return pid[a]
    for k, v in pid.items():
        if a and (k.startswith(a) or a.startswith(k)) and min(len(a), len(k)) >= 5: return v
    return None
fam = []
for m in mag.get('magazin', []):
    picks = [x for x in (bul_id(p) for p in m.get('picks', [])) if x]
    if picks:
        fam.append({'g': m['g'], 'e': m.get('e', '🍺'), 'ad': m['ad'], 'rol': m.get('rol', ''), 'blurb': m.get('blurb', ''), 'picks': list(dict.fromkeys(picks))})
blok('const FAMOUS=', '];', 'const FAMOUS=' + json.dumps(fam, ensure_ascii=False, indent=0) + ';')

# --- Temsilci biralar (boşluk analizi) ---
UL = {'kolay': 3, 'tekel': 3, 'craft': 2, 'zor': -2, 'yurtdisi': -5}
def ilk(pred):
    c = sorted([d for d in data if pred(d)], key=lambda d: -(d['puan'] + UL[d['bul']]))
    return c[0]['id'] if c else ''
REP_CAT = {a: ilk(lambda d, a=a: d['tur'] == a) for a in veri.AILELER}
blok('const REP_CAT=', '\n', 'const REP_CAT=' + json.dumps(REP_CAT, ensure_ascii=False) + ';\n')

open(HTML, 'w', encoding='utf-8').write(s)

# --- data/*.json ---
def yaz(ad, obj):
    json.dump(obj, open(os.path.join(SITE, 'data', ad), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
mevcut = json.load(open(os.path.join(SITE, 'data', 'fiyatlar.json'), encoding='utf-8'))
for k, v in fiy.items():
    if k not in mevcut['fiyatlar'] and k in ids:
        mevcut['fiyatlar'][k] = v
mevcut['fiyatlar'] = {k: v for k, v in sorted(mevcut['fiyatlar'].items()) if k in ids}
yaz('fiyatlar.json', mevcut)
yaz('konumlar.json', konum); yaz('bolgeler.json', bolgeler); yaz('fabrikalar.json', fabrikalar); yaz('tadim.json', tadim)
if stiller.get('stiller'):
    yaz('stiller.json', {'stiller': stiller['stiller'], 'srm_renk': stiller.get('srm_renk', {})})
bp = oku('turkiye2.json', {}).get('brewpublar')
if bp:
    yaz('brewpublar.json', {'brewpublar': [b for b in bp if b.get('durum') != 'kapandı']})
print(len(data), 'bira ·', len(tadim) - 1, 'tadım notu ·', len(fam), 'magazin ·', len(mevcut['fiyatlar']), 'kaynaklı fiyat ·',
      sum(1 for d in data if d.get('sid')), 'stil eşleşmesi')
