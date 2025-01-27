from telegram import Update
from telegram.ext import CallbackContext, JobQueue
import datetime

# Set Reminder
def set_reminder(update: Update, context: CallbackContext):
    args = context.args

    if len(args) < 2:
        update.message.reply_text(
            "Format salah. Gunakan: /reminder <waktu> <pesan>. Contoh: /reminder 07:00 Belajar soal."
        )
        return

    waktu = args[0]
    pesan = " ".join(args[1:])

    try:
        # Parse waktu ke datetime
        jam, menit = map(int, waktu.split(":"))
        now = datetime.datetime.now()
        target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)

        # Kalau waktu udah lewat, tambah 1 hari
        if target < now:
            target += datetime.timedelta(days=1)

        # Tambahkan job ke JobQueue
        context.job_queue.run_once(
            reminder_callback,
            target - now,
            context={"chat_id": update.message.chat_id, "pesan": pesan},
        )

        update.message.reply_text(f"Pengingat disetel untuk {waktu}: {pesan}")
    except ValueError:
        update.message.reply_text("Format waktu salah. Gunakan HH:MM (contoh: 07:00).")

# Callback untuk mengirim pengingat
def reminder_callback(context: CallbackContext):
    job_data = context.job.context
    chat_id = job_data["chat_id"]
    pesan = job_data["pesan"]

    context.bot.send_message(chat_id=chat_id, text=f"⏰ Pengingat: {pesan}")
