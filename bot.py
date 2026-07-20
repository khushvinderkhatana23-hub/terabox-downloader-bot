import os
import telebot
import requests

# Token automatic Render website se connect ho jayega
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hi! Mujhe TeraBox ka video link bhejiye, main aapko download link nikal kar doonga.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    if "terabox" in url or "nephobox" in url:
        status = bot.reply_to(message, "⏳ Video fetch ho raha hai, thoda intezar karein...")
        
        try:
            # TeraBox Free API Link
            api_url = f"https://workers.dev{url}"
            data = requests.get(api_url).json()
            
            if "download_url" in data:
                video_url = data["download_url"]
                bot.send_message(chat_id=message.chat.id, text=f"🎬 **Aapka Video Download Link:**\n\n[Yahan Click Karke Video Download Karein]({video_url})", parse_mode="Markdown")
                bot.delete_message(message.chat.id, status.message_id)
            else:
                bot.edit_message_text("❌ Video nahi mila. Kripya valid TeraBox link check karein.", message.chat.id, status.message_id)
        except:
            bot.edit_message_text("⚠️ Server down hai, thodi der baad dobara koshish karein.", message.chat.id, status.message_id)
    else:
        bot.reply_to(message, "❌ Ye TeraBox link nahi hai. Kripya sahi link bhejiye.")

if __name__ == "__main__":
    print("Bot chalu ho gaya hai...")
    bot.infinity_polling()
  
