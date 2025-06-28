import os
import time
import subprocess
import sys

# Gerekli modül ve paketleri kontrol ve kur
def termux_gerekli_paketleri_yukle():
    print("[✔] Termux paketleri kontrol ediliyor...")
    for paket in ["termux-api"]:
        os.system(f"pkg install -y {paket} >/dev/null 2>&1")

def pip_modul_kontrol_yukle(modul_adi):
    try:
        __import__(modul_adi)
    except ImportError:
        print(f"[+] {modul_adi} yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", modul_adi])

termux_gerekli_paketleri_yukle()
pip_modul_kontrol_yukle("instaloader")

import instaloader
from instaloader import Profile

def e_h_input(soru):
    cevap = input(f"{soru} (e/h): ").strip().lower()
    return cevap == "e"

# === GİRİŞ ===
print("\n📸 Instagram Takipçi/Takip Değişiklik Takibi")
kullanici_adi = input("👤 İzlenecek kullanıcı adı: ").strip()

print("\n🔔 Hangi uyarılar olsun?")
tts = e_h_input("📢 Sesli (TTS) konuşma olsun mu?")
bildirim = e_h_input("🔔 Bildirim gösterilsin mi?")
titreşim = e_h_input("📳 Titreşim olsun mu?")

kontrol_araligi = 0.5
dosya_adi = "degisiklik.txt"

# Uyarı fonksiyonu
def uyar(mesaj):
    if bildirim:
        os.system(f'termux-notification --title "Instagram Uyarı" --content "{mesaj}" --priority high --sound')
    if titreşim:
        os.system("termux-vibrate -d 300")
    if tts:
        os.system(f'termux-tts-speak "{mesaj}"')

# Instaloader başlat
L = instaloader.Instaloader()

# Profil bilgisini al
def kullanici_bilgisi(kadi):
    try:
        profil = Profile.from_username(L.context, kadi)
        return {
            "followers": profil.followers,
            "followees": profil.followees,
            "posts": profil.mediacount
        }
    except Exception as e:
        if "Failed to resolve" in str(e):
            print("[!] Ağ hatası (DNS çözümleyemedi). Bekleniyor...")
            time.sleep(10)
        else:
            print(f"[!] Hata oluştu: {e}")
        return None

# Başlangıç bilgisi
print(f"\n🔎 {kullanici_adi} için bilgi alınıyor...")
onceki = kullanici_bilgisi(kullanici_adi)
if not onceki:
    print("[×] Kullanıcıya ulaşılamadı. Çıkılıyor.")
    exit()

print(f"✅ Takip başladı... (her {kontrol_araligi}s'de kontrol)")

# Döngü
while True:
    time.sleep(kontrol_araligi)
    yeni = kullanici_bilgisi(kullanici_adi)
    if not yeni:
        continue

    log = f"\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    degisim_var = False

    if yeni["followers"] != onceki["followers"]:
        fark = yeni["followers"] - onceki["followers"]
        log += f"👥 Takipçi: {onceki['followers']} ➡ {yeni['followers']} ({'+' if fark>0 else ''}{fark})\n"
        uyar(f"Takipçi sayısı {'arttı' if fark>0 else 'azaldı'}!")
        degisim_var = True

    if yeni["followees"] != onceki["followees"]:
        fark = yeni["followees"] - onceki["followees"]
        log += f"🔄 Takip edilen: {onceki['followees']} ➡ {yeni['followees']} ({'+' if fark>0 else ''}{fark})\n"
        uyar(f"Takip edilen kişi {'arttı' if fark>0 else 'azaldı'}!")
        degisim_var = True

    if yeni["posts"] != onceki["posts"]:
        fark = yeni["posts"] - onceki["posts"]
        log += f"🖼️ Gönderi: {onceki['posts']} ➡ {yeni['posts']} ({'+' if fark>0 else ''}{fark})\n"
        uyar("Yeni gönderi paylaşıldı!" if fark > 0 else "Gönderi silindi!")
        degisim_var = True

    if degisim_var:
        with open(dosya_adi, "a", encoding="utf-8") as f:
            f.write(log)
        print(log.strip())

    onceki = yeni
