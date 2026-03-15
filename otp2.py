import asyncio
from telethon import TelegramClient, events
import re

# Yeni bilgileriniz
api_id = 32778223
api_hash = 'ff44a946dbb1dcfd979409f41a69afc9'
hedef_link = "https://t.me/Black_4OTP_Group"
sizin_link = "https://t.me/+JN4ECzzv5SE4MWQ0"

client = TelegramClient('11userbot_session', api_id, api_hash)

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
        
        # Eğer sticker varsa, 💚 emojisi ekle
        if msg.sticker:
            # Sticker varsa ve metin boşsa sadece 💚 gönder
            if son_mesaj.strip():  # Metin varsa
                son_mesaj = f"💚 {son_mesaj}"
            else:  # Metin yoksa sadece 💚
                son_mesaj = "💚"
            
            await client.send_message(sizin, son_mesaj)
            print(f"📨 Sticker 💚 ile değiştirildi - Mesaj ID: {msg.id}")
        else:
            # Normal mesaj gönder (boş değilse)
            if son_mesaj.strip():  # Metin varsa
                await client.send_message(sizin, son_mesaj)
                print(f"📨 İletildi: {msg.id} - Kodlar: {len(kodlar)} adet")
            else:
                # Boş mesaj varsa görmezden gel
                print(f"⚠️ Boş mesaj atlandı: {msg.id}")

    print("✨ Bot çalışıyor... (Her 2 dakikada bir kanal temizlenecek)")
    print("🚀 İlk temizlik 2 dakika sonra başlayacak")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot durduruldu.")
