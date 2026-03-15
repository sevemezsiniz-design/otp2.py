import asyncio
from telethon import TelegramClient, events
import re
import os
import tempfile
import logging

# Loglama ekleyelim
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Yeni bilgileriniz
api_id = 31622121
api_hash = '2fac726d7fd3d96e26fb4fec7cb62e70'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+RjZf45yOFt0yYzc0"

# Session dosyası için tam yol
SESSION_NAME = '11userbot_session'
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

async def connect_with_retry():
    """Bağlantıyı dene, başarısız olursa tekrar dene"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await client.connect()
            if await client.is_user_authorized():
                return True
            else:
                await client.start()
                return True
        except Exception as e:
            logger.error(f"Bağlantı denemesi {attempt + 1}/{max_retries} başarısız: {e}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                logger.info(f"{wait_time} saniye bekleniyor...")
                await asyncio.sleep(wait_time)
            else:
                return False

async def main():
    logger.info("🤖 Bot başlatılıyor...")
    
    # Bağlantıyı dene
    if not await connect_with_retry():
        logger.error("❌ Telegram'a bağlanılamadı!")
        return
    
    # Linkleri entity'ye çevir
    try:
        hedef = await client.get_entity(hedef_link)
        sizin = await client.get_entity(sizin_link)
        logger.info("✅ Kanallara bağlanıldı!")
        logger.info(f"📥 Hedef: {hedef.title}")
        logger.info(f"📤 Sizin kanal: {sizin.title}")
    except Exception as e:
        logger.error(f"❌ Bağlantı hatası: {e}")
        return

    # Periyodik temizlik görevini başlat
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
        
        # Mesajı hazırla
        son_mesaj = text
        if kodlar:
            son_mesaj += f"\n\n🔑 Kodlar:\n" + "\n".join(kodlar)
        
        # Mesajı gönder
        try:
            if msg.media:
                try:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        medya_yolu = await msg.download_media(file=temp_file.name)
                        
                        await client.send_file(
                            sizin, 
                            file=medya_yolu, 
                            caption=son_mesaj[:1024] if son_mesaj else None
                        )
                        
                        if medya_yolu and os.path.exists(medya_yolu):
                            os.unlink(medya_yolu)
                            
                except Exception as media_error:
                    logger.warning(f"⚠️ Medya indirilemedi, sadece metin gönderiliyor")
                    if son_mesaj:
                        await client.send_message(sizin, f"📝 *Medyasız iletilen mesaj:*\n\n{son_mesaj}")
            else:
                if son_mesaj:
                    await client.send_message(sizin, son_mesaj)
                else:
                    await client.send_message(sizin, "📨 *Boş mesaj iletildi*")
                    
            logger.info(f"📨 İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
        except Exception as e:
            logger.error(f"❌ İletim hatası: {e}")

    logger.info("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
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
