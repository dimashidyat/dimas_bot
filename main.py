from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN
import json
import logging

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('logs/error.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Start Command
def start(update, context):
    update.message.reply_text(
        "Halo Dimas, selamat datang di bot belajar supermu! Ketik /help untuk lihat fitur yang tersedia."
    )

# Help Command
def help_command(update, context):
    update.message.reply_text("""
Fitur yang tersedia:
- /mulai: Mulai latihan soal
- /progress: Cek progres belajar
- /motivasi: Dapatkan motivasi harian
- /help: Lihat daftar perintah
    """)

# Load Soal
def load_soal():
    with open('data/soal.json', 'r') as f:
        return json.load(f)

# Mulai Soal
def mulai(update, context):
    soal = load_soal()
    nomor = 1
    context.user_data['soal'] = soal
    context.user_data['nomor'] = nomor
    context.user_data['benar'] = 0
    soal_pertama = soal[nomor - 1]['pertanyaan']
    update.message.reply_text(f"Soal {nomor}: {soal_pertama}")

# Jawab Soal
def jawab(update, context):
    user_jawaban = update.message.text
    soal = context.user_data.get('soal')
    nomor = context.user_data.get('nomor', 1)
    if not soal or nomor > len(soal):
        update.message.reply_text("Latihan sudah selesai. Ketik /mulai untuk ulang.")
        return

    soal_sekarang = soal[nomor - 1]
    if user_jawaban.lower() == soal_sekarang['jawaban'].lower():
        context.user_data['benar'] += 1
        update.message.reply_text("Benar!")
    else:
        update.message.reply_text(f"Salah! Jawaban yang benar: {soal_sekarang['jawaban']}")

    context.user_data['nomor'] += 1
    nomor = context.user_data['nomor']
    if nomor <= len(soal):
        soal_berikutnya = soal[nomor - 1]['pertanyaan']
        update.message.reply_text(f"Soal {nomor}: {soal_berikutnya}")
    else:
        skor = context.user_data['benar']
        total = len(soal)
        update.message.reply_text(f"Latihan selesai! Skor kamu: {skor}/{total}")

# Progres Belajar
def progress(update, context):
    skor = context.user_data.get('benar', 0)
    total = len(context.user_data.get('soal', []))
    update.message.reply_text(f"Progres kamu: {skor}/{total} soal benar.")

# Motivasi Harian
def motivasi(update, context):
    quotes = [
        "Semangat pagi! Setiap langkah kecil mendekatkan kamu ke impian besar.",
        "Jangan menyerah. Kesuksesan hanya untuk mereka yang gigih.",
        "Belajar hari ini, sukses selamanya!"
    ]
    import random
    update.message.reply_text(random.choice(quotes))

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('mulai', mulai))
    dp.add_handler(CommandHandler('progress', progress))
    dp.add_handler(CommandHandler('motivasi', motivasi))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, jawab))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
