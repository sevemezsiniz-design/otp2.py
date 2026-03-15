import asyncio
import os
from telethon import TelegramClient, events
import re

# Railway environment variables
api_id = int(os.environ.get('API_ID', 32778223))
api_hash = os.environ.get('API_HASH', 'ff44a946dbb1dcfd979409f41a69afc9')
hedef_link = os.environ.get('HEDEF_LINK', 'https://t.me/Black_4OTP_Group')
sizin_link = os.environ.get('SIZIN_LINK', 'https://t.me/+JN4ECzzv5SE4MWQ0')

# Session name for Railway persistence
session_name = os.environ.get('SESSION_NAME', '11userbot_session')

client = TelegramClient(session_name, api_id, api_hash)

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

def format_phone_number(text):
    """Telefon numarasını formatla"""
    # 5842**** formatını kontrol et
    tel_bul = re.search(r'5842\*{4}', text)
    if tel_bul:
        return "5842****"
    
    # Normal telefon numarası ara (ülke kodu+rakamlar)
    tel_normal = re.search(r'(\d{4,})', text.replace('*', ''))
    if tel_normal:
        numara = tel_normal.group(1)
        if len(numara) > 4:
            return f"{numara[:4]}****{numara[-4:]}"
        return numara
    
    return "****"

def get_country_code(text):
    """Ülke kodunu bul (#DE, #US, #TR vb.)"""
    ulke_bul = re.search(r'#([A-Z]{2})', text)
    if ulke_bul:
        return ulke_bul.group(1)
    return "DE"  # varsayılan

async def main():
    # Bağlantıyı kur
    await client.start()
    print("🤖 Bot başlatıldı...")
    print(f"API ID: {api_id}")
    
    try:
        hedef = await client.get_entity(hedef_link)
        sizin = await client.get_entity(sizin_link)
        print("✅ Kanallara bağlanıldı!")
        print(f"📥 Hedef: {hedef.title}")
        print(f"📤 Sizin kanal: {sizin.title}")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return

    # Periyodik temizlik görevini başlat
    asyncio.create_task(periyodik_temizlik(sizin))

    @client.on(events.NewMessage(chats=hedef))
    async def handler(event):
        msg = event.message
        
        # Sticker mesajlarını atla
        if msg.sticker or msg.document or msg.photo or msg.video or msg.gif or msg.audio or msg.voice:
            print("📸 Sticker/medya mesajı atlandı")
            return
        
        text = msg.message or ""
        
        # Boş mesajları atla
        if not text and not msg.reply_markup:
            return
        
        # KODLARI BUL (butonlardan)
        kodlar = []
        
        # 1. Butonlardan kodları al
        if msg.reply_markup:
            try:
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text and re.search(r'\d{3}-\d{3}', btn.text):
                            kod = btn.text.strip()
                            if kod not in kodlar:
                                kodlar.append(kod)
            except:
                pass
        
        # 2. Mesaj metninden kodları al
        if text:
            metin_kodlari = re.findall(r'\d{3}-\d{3}', text)
            for kod in metin_kodlari:
                if kod not in kodlar:
                    kodlar.append(kod)
        
        # Eğer kod bulunamazsa bu mesajı atla
        if not kodlar:
            print("⚠️ Kod bulunamadı, mesaj atlandı")
            return
        
        # Ülke kodunu bul
        ulke_kodu = get_country_code(text)
        
        # Telefon numarasını formatla
        telefon = format_phone_number(text)
        
        # MESAJI OLUŞTUR - İstenilen formatta
        yeni_mesaj = f"otp2:\n──────────────╖ \n{ulke_kodu}#{ulke_kodu} [WS]📞{telefon}┨👍\n──────────────╛\n💚 FREE🇵🇸PALESTINE 💚"
        
        # Kodları ekle
        if kodlar:
            yeni_mesaj += f"\n\n🔑 Kodlar:"
            for kod in kodlar:
                yeni_mesaj += f"\n🔑 {kod}"
        
        # Mesajı gönder
        try:
            await client.send_message(sizin, yeni_mesaj)
            print(f"✅ İletildi - Ülke: {ulce_kodu}, Kodlar: {len(kodlar)}")
        except Exception as e:
            print(f"❌ Gönderme hatası: {e}")

    print("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
    print("🚀 Railway'de çalışıyor...")
    
    # Railway'in beklemesi için sonsuz döngü
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot durduruldu.")
    except Exception as e:
        print(f"❌ Kritik hata: {e}")
