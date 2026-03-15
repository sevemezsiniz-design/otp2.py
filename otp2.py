import asyncio
from telethon import TelegramClient, events
import re

# Yeni bilgileriniz
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"

client = TelegramClient('11userbot_session', api_id, api_hash)

# Ülke bayrakları ve kodları
ULKELER = {
    'VE': '🇻🇪',  # Venezuela
    'US': '🇺🇸',  # USA
    'DE': '🇩🇪',  # Germany
    'TR': '🇹🇷',  # Turkey
    'GB': '🇬🇧',  # United Kingdom
    'FR': '🇫🇷',  # France
    'IT': '🇮🇹',  # Italy
    'ES': '🇪🇸',  # Spain
    'RU': '🇷🇺',  # Russia
    'BR': '🇧🇷',  # Brazil
    'AR': '🇦🇷',  # Argentina
    'MX': '🇲🇽',  # Mexico
    'CA': '🇨🇦',  # Canada
    'AU': '🇦🇺',  # Australia
    'JP': '🇯🇵',  # Japan
    'KR': '🇰🇷',  # Korea
    'CN': '🇨🇳',  # China
    'IN': '🇮🇳',  # India
    'PK': '🇵🇰',  # Pakistan
    'SA': '🇸🇦',  # Saudi Arabia
}

async def mesajlari_sil(kanal):
    """Kanaldeki tüm mesajları sil"""
    try:
        sayac = 0
        async for mesaj in client.iter_messages(kanal):
            try:
                await mesaj.delete()
                sayac += 1
                await asyncio.sleep(0.5)
            except:
                pass
        print(f"✅ {sayac} mesaj silindi")
    except Exception as e:
        print(f"Silme hatası: {e}")

async def periyodik_temizlik(kanal):
    """Her 2 dakikada bir kanalı temizle"""
    while True:
        await asyncio.sleep(120)
        print("🧹 2 dakika doldu, kanal temizleniyor...")
        await mesajlari_sil(kanal)

def mesaj_formatla(orijinal_metin, kodlar):
    """Mesajı istenen formata dönüştür"""
    
    print(f"Orijinal metin: {orijinal_metin}")  # Debug için
    print(f"Bulunan kodlar: {kodlar}")  # Debug için
    
    # Varsayılan değerler
    ulke_kodu = "VE"
    ulke_bayragi = "🇻🇪"
    telefon = "****"
    ws_durumu = "WS"
    
    # Orijinal metinden bilgileri çıkar
    if orijinal_metin:
        # #DE gibi ülke kodunu bul
        ulke_bul = re.search(r'#([A-Z]{2})', orijinal_metin)
        if ulke_bul:
            ulke_kodu = ulke_bul.group(1)
            ulke_bayragi = ULKELER.get(ulke_kodu, f"#{ulke_kodu}")
            print(f"Ülke bulundu: {ulke_kodu} -> {ulke_bayragi}")
        
        # Telefon numarası ara (+49-PRBD-364 gibi)
        tel_bul = re.search(r'\+(\d{2})[^\d]*(\d+)', orijinal_metin)
        if tel_bul:
            ulke_kodu_tel = tel_bul.group(1)
            telefon_kismi = tel_bul.group(2)
            if len(telefon_kismi) >= 3:
                telefon = telefon_kismi[-3:]  # Son 3 haneyi al
            print(f"Telefon bulundu: +{ulke_kodu_tel} ...{telefon}")
        
        # WS veya PRBD durumunu bul
        if 'WS' in orijinal_metin:
            ws_durumu = "WS"
        elif 'PRBD' in orijinal_metin:
            ws_durumu = "PRBD"
    
    # Ana formatı oluştur - tam istediğin gibi
    ust_kisim = f"{ulke_bayragi}#{ulke_kodu} [{ws_durumu}]📞5842****{telefon}┨👍"
    
    # Alt çizgi (üst kısımla aynı uzunlukta)
    alt_cizgi = "─" * (len(ust_kisim) - 5)
    
    # Mesajı oluştur
    formatli_mesaj = f"──────────────╖ \n{ust_kisim}\n{alt_cizgi}╛\n💚 FREE🇵🇸PALESTINE 💚"
    
    # Kodları ekle (varsa)
    if kodlar and len(kodlar) > 0:
        formatli_mesaj += f"\n\n🔑 Kodlar:"
        for kod in kodlar:
            formatli_mesaj += f"\n🔑 {kod}"
    
    print(f"Oluşturulan mesaj: {formatli_mesaj}")  # Debug için
    return formatli_mesaj

async def main():
    await client.start()
    print("🤖 Bot başlatıldı...")
    
    try:
        hedef = await client.get_entity(hedef_link)
        sizin = await client.get_entity(sizin_link)
        print("✅ Kanallara bağlanıldı!")
        print(f"📥 Hedef: {hedef.title}")
        print(f"📤 Sizin kanal: {sizin.title}")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return

    asyncio.create_task(periyodik_temizlik(sizin))

    @client.on(events.NewMessage(chats=hedef))
    async def handler(event):
        msg = event.message
        text = msg.message or ""
        kodlar = []
        
        print(f"\n--- Yeni mesaj alındı! ID: {msg.id} ---")
        
        # Butonlardan kodları al (000-000 formatı)
        if msg.reply_markup:
            try:
                print("Butonlar bulundu, taranıyor...")
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        print(f"Buton metni: {btn.text}")
                        # 000-000 formatını ara (3 rakam - 3 rakam)
                        if btn.text and re.search(r'\d{3}-\d{3}', btn.text):
                            kodlar.append(btn.text)
                            print(f"Kod bulundu: {btn.text}")
            except Exception as e:
                print(f"Buton okuma hatası: {e}")
        
        # Ayrıca mesaj metninde de kod ara
        if text:
            metin_kodlari = re.findall(r'\d{3}-\d{3}', text)
            if metin_kodlari:
                for kod in metin_kodlari:
                    if kod not in kodlar:
                        kodlar.append(kod)
                        print(f"Metinde kod bulundu: {kod}")
        
        print(f"Toplam {len(kodlar)} kod bulundu")
        
        # Mesajı formatla
        formatli_mesaj = mesaj_formatla(text, kodlar)
        
        # Mesajı gönder
        if formatli_mesaj and formatli_mesaj.strip():
            try:
                await client.send_message(sizin, formatli_mesaj)
                print(f"✅ İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
            except Exception as e:
                print(f"❌ Gönderim hatası: {e}")
        else:
            print(f"⚠️ Boş mesaj atlandı: {msg.id}")

    print("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
    print("🚀 İlk temizlik 2 dakika sonra başlayacak")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot durduruldu.")
