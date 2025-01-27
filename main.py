from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers.study import start_quiz
from handlers.health import health_tracker
from handlers.reminders import set_reminder
from handlers.pempek import pempek_report
from handlers.relationship import love_tips
import logging

# Setup Logging
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
async def start(update: Update, context):
    await update.message.reply_text(
        "Halo Dimas! Ketik /help untuk melihat daftar fitur bot ini."
    )

# Help command
async def help_command(update: Update, context):
    await update.message.reply_text("""
Fitur yang tersedia:
- /mulai: Latihan soal kebangsaan
- /pempek: Laporan penjualan pempek
- /workout: Tracker workout harian
- /reminder: Atur pengingat
- /relationship: Tips dan ide hubungan
- /help: Lihat daftar fitur
    """)

# Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('mulai', start_quiz))
    app.add_handler(CommandHandler('workout', health_tracker))
    app.add_handler(CommandHandler('reminder', set_reminder))
    app.add_handler(CommandHandler('pempek', pempek_report))
    app.add_handler(CommandHandler('relationship', love_tips))

    # Start bot
    app.run_polling()

if __name__ == "__main__":
    main()
