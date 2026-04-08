import os
import yt_dlp
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

        if text == "/start":
            bot.send_message(chat_id, "Send me a YouTube link 🎥")
            return "ok"

        bot.send_message(chat_id, "Downloading... ⏳")

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.%(ext)s',
            'noplaylist': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as video:
                bot.send_video(chat_id, video)

            os.remove(filename)

        except Exception as e:
            bot.send_message(chat_id, f"Error: {e}")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
