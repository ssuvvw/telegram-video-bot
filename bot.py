import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "twitter.com" in url or "x.com" in url:
        await update.message.reply_text("⏳ جاري التحميل...")

        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await update.message.reply_video(video=open('video.mp4', 'rb'))
            os.remove("video.mp4")

        except:
            await update.message.reply_text("❌ ما قدرت أحمل الفيديو")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()