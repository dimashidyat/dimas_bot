from telegram import Update
from telegram.ext import CallbackContext
import json

# Load soal dari file JSON
def load_soal():
    with open('data/soal.json', 'r') as f:
        return json.load(f)

def start_quiz(update: Update, context: CallbackContext):
    soal = load_soal()
    context.user_data['soal'] = soal
    context.user_data['nomor'] = 1
    context.user_data['benar'] = 0

    soal_pertama = soal[0]['pertanyaan']
    update.message.reply_text(f"Soal 1: {soal_pertama}")

def jawab_quiz(update: Update, context: CallbackContext):
    user_jawaban = update.message.text
    soal = context.user_data.get('soal', [])
    nomor = context.user_data.get('nomor', 1)

    if nomor > len(soal):
        update.message.reply_text("Latihan selesai. Ketik /mulai untuk ulang.")
        return

    soal_sekarang = soal[nomor - 1]
    if user_jawaban.lower() == soal_sekarang['jawaban'].lower():
        context.user_data['benar'] += 1
        update.message.reply_text("Benar!")
    else:
        update.message.reply_text(f"Salah! Jawaban: {soal_sekarang['jawaban']}")

    context.user_data['nomor'] += 1
    if context.user_data['nomor'] <= len(soal):
        soal_berikutnya = soal[context.user_data['nomor'] - 1]['pertanyaan']
        update.message.reply_text(f"Soal {context.user_data['nomor']}: {soal_berikutnya}")
    else:
        skor = context.user_data['benar']
        total = len(soal)
        update.message.reply_text(f"Latihan selesai! Skor: {skor}/{total}")
