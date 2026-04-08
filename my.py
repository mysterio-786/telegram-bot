# import os
# import yt_dlp
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# BOT_TOKEN = "6256287443:AAG-XJqAKFVn8dNwlvNlR5F30siPFk9vvAk"

# user_data = {}

# # Google Drive Login
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)

# # Start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Send YouTube link 🎥")

# # URL receive
# async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_data[update.effective_chat.id] = update.message.text

#     keyboard = [
#         [InlineKeyboardButton("720p 🎥", callback_data="720")],
#         [InlineKeyboardButton("1080p 🎬", callback_data="1080")]
#     ]

#     await update.message.reply_text(
#         "Select video quality:",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )

# # Button click
# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     url = user_data.get(query.message.chat.id)

#     if not url:
#         await query.message.reply_text("Send link again ❌")
#         return

#     choice = query.data

#     await query.edit_message_text("Downloading... ⏳")

#     ydl_opts = {
#         'outtmpl': 'video.%(ext)s'
#     }

#     if choice == "720":
#         ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
#     elif choice == "1080":
#         ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'

#     # Download
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

#     # Get downloaded file
#     file_name = None
#     for f in os.listdir('.'):
#         if f.endswith(('.mp4', '.mkv', '.webm')):
#             file_name = f
#             break

#     if not file_name:
#         await query.message.reply_text("Download failed ❌")
#         return

#     file_size = os.path.getsize(file_name) / (1024 * 1024)

#     await query.message.reply_text(f"File size: {round(file_size,2)} MB")

#     # Send or upload
#     if file_size < 50:
#         await query.message.reply_document(document=open(file_name, "rb"))
#     else:
#         await query.message.reply_text("Uploading to Drive ☁️")

#         gfile = drive.CreateFile({'title': file_name})
#         gfile.SetContentFile(file_name)
#         gfile.Upload()

#         link = gfile['alternateLink']
#         await query.message.reply_text(f"Download link:\n{link}")

#     os.remove(file_name)

# # Run bot
# app = ApplicationBuilder().token(BOT_TOKEN).build()

# app.add_handler(CommandHandler("start", start))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
# app.add_handler(CallbackQueryHandler(button))

# print("Bot running...")
# app.run_polling()

# import yt_dlp
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# # 🔑 Apna bot token yaha daalo
# BOT_TOKEN = "6256287443:AAG-XJqAKFVn8dNwlvNlR5F30siPFk9vvAk"


# # 🎬 Video download function (FFmpeg ke bina)
# def download_video(url):
#     ydl_opts = {
#         'format': 'best[ext=mp4]',   # ✅ FFmpeg not required
#         'outtmpl': '%(title)s.%(ext)s'
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])


# # ▶️ Start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Send me a YouTube link 🎥")


# # 📩 Message handler
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     url = update.message.text

#     await update.message.reply_text("Downloading... ⏳")

#     try:
#         download_video(url)
#         await update.message.reply_text("Downloaded successfully ✅")
#     except Exception as e:
#         await update.message.reply_text(f"Error: {e}")


# # 🤖 Main function
# def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

#     print("Bot running... 🚀")
#     app.run_polling()


# if __name__ == "__main__":
#     main()

import yt_dlp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Apna bot token
BOT_TOKEN = "6256287443:AAG-XJqAKFVn8dNwlvNlR5F30siPFk9vvAk"


# 🎬 Download function (no ffmpeg needed)
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "video.mp4"


# ▶️ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send YouTube link 🎥")


# 📩 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Downloading... ⏳")

    try:
        file_path = download_video(url)

        await update.message.reply_text("Uploading to Telegram... 📤")

        # 📤 Send video
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video)

        # 🧹 Delete file after sending
        os.remove(file_path)

        await update.message.reply_text("Done ✅")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


# 🤖 Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running... 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()