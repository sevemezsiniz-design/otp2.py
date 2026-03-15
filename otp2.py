import asyncio
from telethon import TelegramClient, events
import re
import random

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
        
        # Telefon numarası ara
        tel_bul = re.search(r'(\+?\d{10,})', orijinal_metin)
        if tel_bul:
            tel = tel_bul.group(1)
            # Son 4 haneyi al, başını maskele
            if len(tel) >= 4:
                telefon = tel[-4:]
        
        # WS veya benzeri durumları bul
        if 'WS' in orijinal_metin:
            ws_durumu = "WS"
        elif 'PRBD' in orijinal_metin:
            ws_durumu = "PRBD"
    
    # Ana formatı oluştur
    ust_kisim = f"{ulke_bayragi}#{ulke_kodu} [{ws_durumu}]📞5842****{telefon}┨👍"
    
    # Alt çizgi (uzunluğa göre ayarla)
    alt_cizgi = "─" * (len(ust_kisim) - 10)  # Biraz ayarlama
    
    # Mesajı oluştur
    formatli_mesaj = f"──────────────╖ \n{ust_kisim}\n{alt_cizgi}╛\n💚 FREE🇵🇸PALESTINE 💚"
    
    # Kodları ekle
    if kodlar:
        formatli_mesaj += f"\n\n🔑 Kodlar:\n"
        for kod in kodlar:
            formatli_mesaj += f"🔑 {kod}\n"
    
    return formatli_mesaj.strip()

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
        
        # Butonlardan kodları al
        if msg.reply_markup:
            try:
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text and re.search(r'\d{3}-\d{3}', btn.text):
                            kodlar.append(btn.text)
            except:
                pass
        
        # Mesajı formatla
        formatli_mesaj = mesaj_formatla(text, kodlar)
        
        # Mesajı gönder (boş değilse)
        if formatli_mesaj and formatli_mesaj.strip():
            try:
                await client.send_message(sizin, formatli_mesaj)
                
                # Log
                if kodlar:
                    print(f"📨 İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
                else:
                    print(f"📨 İletildi: {msg.id} (Kodsuz)")
                    
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
