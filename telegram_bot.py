import os
import json
from telethon import TelegramClient
from telethon.sessions import StringSession

# دریافت اطلاعات از متغیرهای محیطی
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
telegram_session = os.getenv("TELEGRAM_SESSION")

# نام کانال یا یوزرنیم ربات را اینجا وارد کنید (بدون @)
channel_username = 'HATTRICK_CHANNEL'  # مثال: 'bbcPersian' یا 'username_bot'

def main():
    try:
        # اتصال به تلگرام
        client = TelegramClient(StringSession(telegram_session), int(api_id), api_hash)
        client.connect()
        
        print("Connecting to Telegram...")
        if not client.is_user_authorized():
            print("Failed to authorize session.")
            return

        print("Fetching last 5 posts...")
        posts = []
        
        # خواندن ۵ پیام آخر
        async def get_posts():
            # اگر کانال عمومی است:
            if channel_username.startswith('@'):
                entity = await client.get_entity(channel_username)
            else:
                entity = await client.get_entity(channel_username)
                
            messages = await client.get_messages(entity, limit=5)
            
            for msg in messages:
                if msg.text:
                    posts.append({
                        "id": msg.id,
                        "text": msg.text,
                        "date": str(msg.date)
                    })
        
        # اجرای تابع ناهمگام
        client.loop.run_until_complete(get_posts())
        
        # ذخیره در فایل JSON
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
            
        print(f"Success! {len(posts)} posts saved to posts.json")
        
        client.disconnect()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
