#!/usr/bin/env python3
"""Build games.js + story.js untuk PS Database web."""
import json, re, os

os.makedirs('/home/hatch/workspace/ps-db', exist_ok=True)
BASE = '/home/hatch/workspace/ps-db/data'

def norm(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9 ]', '', t)
    return re.sub(r'\s+', ' ', t).strip()

# ---- 1. Load & normalisasi dataset ----
games = []  # [title, plat, year, dev, pub, link]
seen = set()
for fn, plat in [('PS2Games.json', 2), ('PS3Games.json', 3)]:
    data = json.load(open(f'{BASE}/{fn}', encoding='utf-8'))
    for g in data:
        title = (g.get('Game') or '').strip()
        if not title:
            continue
        key = (norm(title), plat)
        if key in seen:
            continue
        seen.add(key)
        year = str(g.get('Year') or '').strip()
        dev = (g.get('Dev') or '').strip()
        pub = (g.get('Publisher') or '').strip()
        link = (g.get('GameLink') or '').strip()
        games.append([title, plat, year, dev, pub, link])

games.sort(key=lambda x: norm(x[0]))
print(f'total unik: {len(games)} (PS2: {sum(1 for g in games if g[1]==2)}, PS3: {sum(1 for g in games if g[1]==3)})')

# ---- 2. Story picks (kurasi) ----
# badge: 'epik' = cerita super panjang, 'sinema' = sinematik kayak film
STORY = [
 # PS2 JRPG raksasa
 ("Persona 3 FES", "epik", "80-120 jam", "Misteri 'jam ke-25' tiap tengah malam. Lawan bayangan di Tartarus. Tema kematian & persahabatan, ada epilog The Answer."),
 ("Persona 4", "epik", "75-100 jam", "Kasus pembunuhan berantai di kota kecil Inaba. Masuk dunia dalam TV. Misteri + social sim."),
 ("Final Fantasy XII", "epik", "75-125 jam", "Intrik politik kerajaan Ivalice, perang antar kekaisaran. Dunia open-zone super luas."),
 ("Dragon Quest VIII", "epik", "75-100 jam", "Kutukan penyihir Dhoulmagus, selamatkan kerajaan Trodain. Klasik, charming, santai."),
 ("Star Ocean Till the End of Time", "epik", "75-105 jam", "Sci-fi epik antar galaksi dengan twist cerita legendaris. Post-game lebih panjang dari story."),
 ("Shin Megami Tensei Nocturne", "epik", "70-80 jam", "Dunia kiamat, bangun ulang realitas. Gelap, filosofis. Gameplay SULIT."),
 ("Suikoden V", "epik", "70-80 jam", "Kudeta kerajaan Falena. Rekrut 108 karakter. Drama politik."),
 ("Suikoden III", "epik", "60-70 jam", "Tiga sudut pandang perang Grassland, 108 karakter."),
 ("Final Fantasy X", "epik", "60-70 jam", "Ziarah Yuna melawan Sin. Cerita paling emosional di seri FF."),
 ("Xenosaga Episode I", "epik", "25-30 jam", "Sci-fi filosofis antar bintang. Bagian pertama trilogi epik."),
 ("Rogue Galaxy", "epik", "50-60 jam", "Bajak laut luar angkasa, petualangan planet ke planet."),
 ("Dark Cloud 2", "epik", "60-70 jam", "Rebuild dunia + time travel. Dua protagonis."),
 # PS2 action/adventure cerita kuat
 ("Metal Gear Solid 3 Snake Eater", "sinema", "16-20 jam", "Perang Dingin 1964, asal-usul Big Boss. Spionase terbaik PS2."),
 ("Grand Theft Auto San Andreas", "sinema", "30-40 jam", "CJ kembali ke Grove Street. Gangster saga era 90-an."),
 ("Okami", "sinema", "35-45 jam", "Dewi Amaterasu selamatkan Jepang mitologi. Visual tinta yang indah."),
 ("God of War II", "sinema", "12 jam", "Kratos vs dewa-dewa Olympus. Brutal + mitologi Yunani."),
 ("Kingdom Hearts II", "epik", "35-40 jam", "Sora + Disney + Final Fantasy melawan kegelapan."),
 ("Silent Hill 2", "sinema", "8-10 jam", "Horor psikologis terbaik sepanjang masa. Pendek tapi dalam."),
 ("Shadow of the Colossus", "sinema", "8-12 jam", "16 raksasa, 1 gadis, ending tak terlupakan."),
 # PS3
 ("Persona 5", "epik", "100+ jam", "Phantom Thieves curi 'hati' orang korup di Tokyo. JRPG modern terbaik."),
 ("Ni no Kuni Wrath of the White Witch", "epik", "40-60 jam", "Anak ke dunia sihir selamatkan ibu. Dibuat bareng Studio Ghibli."),
 ("Mass Effect 2", "sinema", "25-35 jam", "Komandan Shepard lawan Reapers, misi bunuh diri. Pilihan ngaruh ke sekuel."),
 ("Red Dead Redemption", "sinema", "20-30 jam", "Mantan bandit John Marston di akhir era Wild West. Ending legendaris."),
 ("Yakuza 4", "sinema", "20-25 jam", "Drama kriminal Jepang, 4 protagonis di Kamurocho. Kayak main film yakuza."),
 ("Tales of Berseria", "epik", "45-55 jam", "Anti-hero balas dendam. Cerita Tales paling kelam."),
 ("Valkyria Chronicles", "epik", "30-40 jam", "Taktik RPG setting PD II fiksi. Cerita perang yang manusiawi."),
 ("The Last of Us", "sinema", "15-20 jam", "Joel & Ellie di dunia post-apocalyptic. Cerita terbaik generasinya."),
 ("Metal Gear Solid 4", "sinema", "18-25 jam", "Penutup saga Solid Snake. Kayak main film."),
 ("BioShock", "sinema", "12-15 jam", "Kota bawah laut Rapture. Twist plot legendaris."),
 ("Heavy Rain", "sinema", "10-12 jam", "Thriller pembunuh Origami, 4 karakter, ending bercabang."),
 ("Batman Arkham City", "sinema", "12-15 jam", "Batman di penjara kota Gotham."),
 ("Assassin's Creed II", "sinema", "18-20 jam", "Ezio Auditore, Renaissance Italia."),
 ("inFamous 2", "sinema", "12-15 jam", "Superhero moral choice, ending ganda."),
 ("Demon's Souls", "epik", "40-50 jam", "Lore dalam & gelap dari dunia dan item. SULIT."),
 ("Dark Souls", "epik", "50-60 jam", "Penerus Demon's Souls. Dunia interconnected, lore misterius. SULIT."),
 ("Grand Theft Auto V", "sinema", "30+ jam", "Tiga kriminal di Los Santos."),
 ("Deus Ex Human Revolution", "sinema", "20-25 jam", "Cyberpunk konspirasi korporat."),
]

# ---- 3. Match story ke dataset ----
title_index = {}
for i, g in enumerate(games):
    title_index.setdefault(norm(g[0]), []).append(i)

matched, unmatched = {}, []
for stitle, badge, hours, desc in STORY:
    nkey = norm(stitle)
    hits = title_index.get(nkey, [])
    if not hits:
        # fallback: substring match
        cands = [i for i, g in enumerate(games) if nkey in norm(g[0])]
        # pilih yang paling mirip (selisih panjang terkecil)
        cands.sort(key=lambda i: abs(len(norm(games[i][0])) - len(nkey)))
        hits = cands[:1]
    if hits:
        for i in hits:
            matched[games[i][0]] = [badge, hours, desc]
    else:
        unmatched.append(stitle)

print(f'story matched: {len(matched)}, unmatched: {unmatched}')

# ---- 4. Tulis games.js & story.js ----
def js_str(s):
    return json.dumps(s, ensure_ascii=False)

with open('/home/hatch/workspace/ps-db/games.js', 'w', encoding='utf-8') as f:
    f.write('const GAMES=' + js_str(games) + ';')
with open('/home/hatch/workspace/ps-db/story.js', 'w', encoding='utf-8') as f:
    f.write('const STORY=' + js_str(matched) + ';')

import os as _os
print('games.js:', _os.path.getsize('/home/hatch/workspace/ps-db/games.js')//1024, 'KB')
print('story.js:', _os.path.getsize('/home/hatch/workspace/ps-db/story.js')//1024, 'KB')
