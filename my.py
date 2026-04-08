import os
import yt_dlp
from flask import Flask, request
from telegram import Bot, Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)
last_update_id = None

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global last_update_id

    try:
        update = Update.de_json(request.get_json(force=True), bot)

        # ✅ duplicate block
        if update.update_id == last_update_id:
            return "ok"
        last_update_id = update.update_id

        if update.message:
            chat_id = update.message.chat_id
            text = update.message.text

            if text == "/start":
                bot.send_message(chat_id, "Send me a YouTube link 🎥")
                return "ok"

            if "youtube.com" not in text and "youtu.be" not in text:
                bot.send_message(chat_id, "❌ Please send a valid YouTube link")
                return "ok"

            bot.send_message(chat_id, "Downloading... ⏳")

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video.%(ext)s',
                'noplaylist': True,
                'quiet': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as video:
                bot.send_video(chat_id, video)

            os.remove(filename)

    except Exception as e:
        print("ERROR:", e)
        try:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")
        except:
            pass

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
