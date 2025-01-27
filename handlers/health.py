from telegram import Update
from telegram.ext import CallbackContext
import json

# File tempat menyimpan data workout
WORKOUT_FILE = 'data/user_data.json'

# Load data workout dari file JSON
def load_workout_data():
    try:
        with open(WORKOUT_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Simpan data workout ke file JSON
def save_workout_data(data):
    with open(WORKOUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Tambahkan workout
def health_tracker(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    args = context.args

    if len(args) < 2:
        update.message.reply_text(
            "Format salah. Gunakan: /workout <jenis_workout> <durasi>. Contoh: /workout push_up 15"
        )
        return

    jenis_workout = args[0]
    durasi = int(args[1])

    # Load data lama
    data = load_workout_data()
    if user_id not in data:
        data[user_id] = {}

    if jenis_workout not in data[user_id]:
        data[user_id][jenis_workout] = 0

    # Tambahkan durasi workout
    data[user_id][jenis_workout] += durasi
    save_workout_data(data)

    update.message.reply_text(
        f"Berhasil menambahkan {durasi} menit untuk {jenis_workout}."
    )

# Tampilkan laporan workout
def show_workout_report(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    data = load_workout_data()

    if user_id not in data or not data[user_id]:
        update.message.reply_text("Belum ada catatan workout.")
        return

    report = "Laporan Workout Harian:\n"
    for jenis, durasi in data[user_id].items():
        report += f"- {jenis}: {durasi} menit\n"

    update.message.reply_text(report)
