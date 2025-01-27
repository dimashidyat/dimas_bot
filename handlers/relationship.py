from telegram import Update
from telegram.ext import CallbackContext
import random

# List pesan cinta
LOVE_MESSAGES = [
    "Cinta itu seperti kopi pagi, hangat dan menyemangati!",
    "Jangan lupa bilang 'Aku sayang kamu' ke orang tersayang hari ini.",
    "Hubungan yang sehat dimulai dari komunikasi yang baik."
]

# Kirim pesan cinta
def love_tips(update: Update, context: CallbackContext):
    message = random.choice(LOVE_MESSAGES)
    update.message.reply_text(message)
