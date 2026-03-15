import asyncio
from telethon import TelegramClient, events, connection
import re
import os
import tempfile
import logging
import socket

# Loglama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Yeni bilgileriniz
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"

# Session adı
SESSION_NAME = '11userbot_session'

async def test_connection():
    """Basit socket testi"""
    try:
        socket.create_connection(("149.154.167.92", 443), timeout=5)
        logger.info("✅ Socket bağlantısı başarılı")
        return True
    except Exception as e:
        logger.error(f"❌ Socket bağlantı hatası: {e}")
        return False

async def connect_with_different_dcs():
    """Farklı DC'leri dene - DÜZELTİLDİ"""
    dcs = [
        ("149.154.167.92", 443),   # DC 2 - tırnaklar eklendi
        ("149.154.175.50", 443),   # DC 4 - tırnaklar eklendi
        ("91.108.56.100", 443),    # DC 5 - tırnaklar eklendi
    ]

    for ip, port in dcs:
        try:
            logger.info(f"Bağlanılıyor: {ip}:{port}")
            client = TelegramClient(
                SESSION_NAME,
                api_id,
                api_hash,
                connection=connection.ConnectionTcpFull,
                connection_retries=3,
                timeout=10
            )
            await client.connect()
            if await client.is_user_authorized():
                logger.info(f"✅ Bağlantı başarılı: {ip}:{port}")
                return client
            else:
                await client.start()
                return client
        except Exception as e:
            logger.warning(f"❌ {ip}:{port} başarısız: {e}")
            continue

    return None

async def mesajlari_sil(kanal, client):
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

async def periyodik_temizlik(kanal, client):
    """Her 2 dakikada bir kanalı temizle"""
    while True:
        await asyncio.sleep(120)
        logger.info("🧹 2 dakika doldu, kanal temizleniyor...")
        await mesajlari_sil(kanal, client)

async def main():
    logger.info("🤖 Bot başlatılıyor...")

    # Önce socket testi yap
    if not await test_connection():
        logger.error("❌ İnternet bağlantısı yok!")
        return

    # Farklı DC'leri dene
    client = await connect_with_different_dcs()
    if not client:
        logger.error("❌ Hiçbir DC'ye bağlanılamadı!")
        return

    logger.info("✅ Telegram'a bağlanıldı!")

    # Linkleri entity'ye çevir
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
    asyncio.create_task(periyodik_temizlik(sizin, client))

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
