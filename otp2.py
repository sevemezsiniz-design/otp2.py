import asyncio
from telethon import TelegramClient, events
import re

# Yeni bilgileriniz
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"

client = TelegramClient('11userbot_session', api_id, api_hash)

# Ülke bayrakları
ULKELER = {
    'VE': '🇻🇪', 'US': '🇺🇸', 'DE': '🇩🇪', 'TR': '🇹🇷', 'GB': '🇬🇧',
    'FR': '🇫🇷', 'IT': '🇮🇹', 'ES': '🇪🇸', 'RU': '🇷🇺', 'BR': '🇧🇷',
    'AR': '🇦🇷', 'MX': '🇲🇽', 'CA': '🇨🇦', 'AU': '🇦🇺', 'JP': '🇯🇵',
    'KR': '🇰🇷', 'CN': '🇨🇳', 'IN': '🇮🇳', 'PK': '🇵🇰', 'SA': '🇸🇦',
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
        
        # KODLARI BUL (önce butonlarda, sonra metinde)
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
        
        # ÜLKE KODUNU BUL
        ulke_kodu = "VE"  # varsayılan
        if text:
            # #VE, #DE, #US gibi kodları ara
            ulke_bul = re.search(r'#([A-Z]{2})', text)
            if ulke_bul:
                ulke_kodu = ulke_bul.group(1)
        
        # TELEFON NUMARASININ SON RAKAMLARINI BUL
        son_rakamlar = "****"
        if text:
            # 5842**** formatını ara
            tel_bul = re.search(r'5842\*{4}', text)
            if tel_bul:
                son_rakamlar = "****"
            else:
                # Veya normal telefon numarası ara
                rakam_bul = re.search(r'(\d{4})$', text.replace('*', ''))
                if rakam_bul:
                    son_rakamlar = rakam_bul.group(1)
        
        # MESAJI OLuŞTUR
        bayrak = ULKELER.get(ulke_kodu, '🇻🇪')
        
        # Ana mesaj
        yeni_mesaj = f"──────────────╖ \n{bayrak}#{ulke_kodu} [WS]📞5842{son_rakamlar}┨👍\n───────────────╛\n💚 FREE🇵🇸PALESTINE 💚"
        
        # Kodları ekle
        if kodlar:
            yeni_mesaj += f"\n\n🔑 Kodlar:"
            for kod in kodlar:
                yeni_mesaj += f"\n🔑 {kod}"
        
        # Mesajı gönder
        try:
            await client.send_message(sizin, yeni_mesaj)
            print(f"✅ İletildi - Ülke: {ulke_kodu}, Kodlar: {len(kodlar)}")
        except Exception as e:
            print(f"❌ Hata: {e}")

    print("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot durduruldu.")
