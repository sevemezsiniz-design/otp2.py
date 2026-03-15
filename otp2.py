import asyncio
from telethon import TelegramClient, events
import re
import logging

# Loglama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ========== YENİ BİLGİLER ==========
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"
SESSION_NAME = '11userbot_session'

# İstemci oluştur
client = TelegramClient(SESSION_NAME, api_id, api_hash)

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
        if sayac > 0:
            logger.info(f"✅ {sayac} mesaj silindi")
    except Exception as e:
        logger.error(f"Silme hatası: {e}")

async def periyodik_temizlik(kanal):
    """Her 2 dakikada bir kanalı temizle"""
    while True:
        await asyncio.sleep(120)
        logger.info("🧹 2 dakika doldu, kanal temizleniyor...")
        await mesajlari_sil(kanal)

async def main():
    logger.info("🤖 Bot başlatılıyor...")
    
    # Telegram'a bağlan
    try:
        await client.start()
        logger.info("✅ Telegram'a bağlanıldı!")
    except Exception as e:
        logger.error(f"❌ Bağlantı hatası: {e}")
        return
    
    # Kanallara bağlan
    try:
        hedef = await client.get_entity(hedef_link)
        sizin = await client.get_entity(sizin_link)
        logger.info("✅ Kanallara bağlanıldı!")
        logger.info(f"📥 Hedef: {hedef.title}")
        logger.info(f"📤 Sizin kanal: {sizin.title}")
    except Exception as e:
        logger.error(f"❌ Kanal bağlantı hatası: {e}")
        return

    # Periyodik temizlik görevini başlat
    asyncio.create_task(periyodik_temizlik(sizin))

    @client.on(events.NewMessage(chats=hedef))
    async def handler(event):
        msg = event.message
        text = msg.message or ""
        kodlar = []
        
        # Butonlardan kodları al (000-000 formatı)
        if msg.reply_markup:
            try:
                for row in msg.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text and re.search(r'\d{3}-\d{3}', btn.text):
                            kodlar.append(btn.text)
            except:
                pass
        
        # SADECE METİN VE KODLARI İLET - MEDYA YOK!
        son_mesaj = text
        
        # Kodları ekle
        if kodlar:
            son_mesaj += f"\n\n🔑 Kodlar:\n"
            for kod in kodlar:
                son_mesaj += f"🔑 {kod}\n"
        
        # Mesajı gönder (SADECE METİN)
        try:
            if son_mesaj.strip():  # Boş değilse gönder
                await client.send_message(sizin, son_mesaj)
                logger.info(f"📨 İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
            else:
                logger.info(f"⏭️ Boş mesaj atlandı: {msg.id}")
            
        except Exception as e:
            logger.error(f"❌ İletim hatası: {e}")

    logger.info("✨ Bot çalışıyor... (SADECE METİN İLETİLİYOR, MEDYA YOK)")
    logger.info("🚀 İlk temizlik 2 dakika sonra başlayacak")
    
    try:
        await client.run_until_disconnected()
    finally:
        await client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Bot durduruldu.")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
