import asyncio
from telethon import TelegramClient, events
import re
import os
import tempfile

# Yeni bilgileriniz
api_id = 31622121
api_hash = '2fac726d7fd3d96e26fb4fec7cb62e70'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+RjZf45yOFt0yYzc0"

client = TelegramClient('11userbot_session', api_id, api_hash)

async def mesajlari_sil(kanal):
    """Kanaldeki tüm mesajları sil"""
    try:
        sayac = 0
        async for mesaj in client.iter_messages(kanal):
            try:
                await mesaj.delete()
                sayac += 1
                await asyncio.sleep(0.5)  # Rate limit koruması
            except:
                pass
        print(f"✅ {sayac} mesaj silindi")
    except Exception as e:
        print(f"Silme hatası: {e}")

async def periyodik_temizlik(kanal):
    """Her 2 dakikada bir kanalı temizle"""
    while True:
        await asyncio.sleep(120)  # 2 dakika = 120 saniye
        print("🧹 2 dakika doldu, kanal temizleniyor...")
        await mesajlari_sil(kanal)

async def main():
    await client.start()
    print("🤖 Bot başlatıldı...")
    
    # Linkleri entity'ye çevir
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
        
        # Mesajı gönder - DÜZELTİLMİŞ VERSİYON
        try:
            if msg.media:
                # Medyayı geçici olarak indir
                try:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        medya_yolu = await msg.download_media(file=temp_file.name)
                        
                        # İndirilen medyayı gönder
                        await client.send_file(
                            sizin, 
                            file=medya_yolu, 
                            caption=son_mesaj[:1024] if son_mesaj else None
                        )
                        
                        # Geçici dosyayı sil
                        if medya_yolu and os.path.exists(medya_yolu):
                            os.unlink(medya_yolu)
                            
                except Exception as media_error:
                    print(f"⚠️ Medya indirilemedi, sadece metin gönderiliyor: {media_error}")
                    # Medya gönderilemezse sadece metni gönder
                    if son_mesaj:
                        await client.send_message(sizin, f"📝 *Medyasız iletilen mesaj:*\n\n{son_mesaj}")
            else:
                # Sadece metin mesajı
                if son_mesaj:
                    await client.send_message(sizin, son_mesaj)
                else:
                    await client.send_message(sizin, "📨 *Boş mesaj iletildi*")
                    
            print(f"📨 İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
        except Exception as e:
            print(f"❌ İletim hatası: {e}")

    print("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
    print("🚀 İlk temizlik 2 dakika sonra başlayacak")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot durduruldu.")
