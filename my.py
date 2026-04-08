import os
import yt_dlp
import asyncio
from flask import Flask, request
from telegram import Bot, Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat_id
        text = update.message.text

        # Start command
        if text == "/start":
            asyncio.run(bot.send_message(chat_id, "Send me a YouTube link 🎥"))
            return "ok"

        asyncio.run(bot.send_message(chat_id, "Downloading... ⏳"))

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as video:
                asyncio.run(bot.send_video(chat_id, video))

            os.remove(filename)

       except Exception as e:
           asyncio.run(bot.send_message(
               chat_id,
               "❌ This video can't be downloaded (YouTube restriction).\nTry another video 👍"))

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
