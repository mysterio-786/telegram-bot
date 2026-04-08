import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔐 Token from Render Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a YouTube link 🎥")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Downloading... ⏳")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send file
        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
