import asyncio
from telethon import TelegramClient, events
import re
import logging

# Loglama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ========== BİLGİLER ==========
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"
SESSION_NAME = '11userbot_session'

client = TelegramClient(SESSION_NAME, api_id, api_hash)

async def mesajlari_sil(kanal):
    try:
        sayac = 0
        async for mesaj in client.iter_messages(kanal):
            try:
                await mesaj.delete()
                sayac += 1
                await asyncio.sleep(0.5)
            except:
                pass
        if sayac > 0:
            logger.info(f"✅ {sayac} mesaj silindi")
    except Exception as e:
        logger.error(f"Silme hatası: {e}")

async def periyodik_temizlik(kanal):
    while True:
        await asyncio.sleep(120)
        logger.info("🧹 2 dakika doldu, kanal temizleniyor...")
        await mesajlari_sil(kanal)

async def main():
    logger.info("🤖 Bot başlatılıyor...")
    
    await client.start()
    logger.info("✅ Telegram'a bağlanıldı!")
    
    try:
        hedef = await client.get_entity(hedef_link)
        sizin = await client.get_entity(sizin_link)
        logger.info("✅ Kanallara bağlanıldı!")
    except Exception as e:
        logger.error(f"❌ Kanal bağlantı hatası: {e}")
        return

    asyncio.create_task(periyodik_temizlik(sizin))

    @client.on(events.NewMessage(chats=hedef))
    async def handler(event):
        msg = event.message
        
        # 1. MESAJ METNİ (varsa)
        mesaj_metni = msg.message or ""
        
        # 2. BUTON KODLARI (000-000 formatında)
        kodlar = []
        if msg.reply_markup:
            try:
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text and re.search(r'\d{3}-\d{3}', btn.text):
                            kodlar.append(btn.text)
            except:
                pass
        
        # 3. İLETİLECEK MESAJI OLUŞTUR (SADECE METİN + KODLAR)
        iletilecek = mesaj_metni
        
        # Kodları ekle (varsa)
        if kodlar:
            iletilecek += f"\n\n🔑 Kodlar:\n"
            for kod in kodlar:
                iletilecek += f"🔑 {kod}\n"
        
        # 4. GÖNDER (SADECE METİN VARSA)
        if iletilecek.strip():
            try:
                await client.send_message(sizin, iletilecek)
                logger.info(f"✅ İletildi: {msg.id} - Kod: {len(kodlar)} adet")
            except Exception as e:
                logger.error(f"❌ İletim hatası: {msg.id} - {e}")
        else:
            logger.info(f"⏭️ Atladı: {msg.id} (içerik yok)")

    logger.info("✨ Bot çalışıyor... (SADECE METİN + BUTON KODLARI)")
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot durduruldu.")
