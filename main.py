from telegram.ext import Updater, CommandHandler
from config import TOKEN
from handlers.study import start_quiz
from handlers.health import health_tracker
from handlers.reminders import set_reminder
from handlers.pempek import pempek_report
from handlers.relationship import love_tips
import logging

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/error.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Start command
def start(update, context):
    update.message.reply_text(
        "Halo Dimas! Ketik /help untuk melihat daftar fitur bot ini."
    )

# Help command
def help_command(update, context):
    update.message.reply_text("""
Fitur yang tersedia:
- /mulai: Latihan soal kebangsaan
- /pempek: Laporan penjualan pempek
- /workout: Tracker workout harian
- /reminder: Atur pengingat
- /relationship: Tips dan ide hubungan
- /help: Lihat daftar fitur
    """)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('mulai', start_quiz))
    dp.add_handler(CommandHandler('workout', health_tracker))
    dp.add_handler(CommandHandler('reminder', set_reminder))
    dp.add_handler(CommandHandler('pempek', pempek_report))
    dp.add_handler(CommandHandler('relationship', love_tips))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
