from telegram import Update
from telegram.ext import CallbackContext
import json

# File tempat menyimpan data pempek
DATA_FILE = 'data/pempek_data.json'

# Load data pempek dari file JSON
def load_pempek_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Simpan data pempek ke file JSON
def save_pempek_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Tambahkan laporan penjualan pempek
def pempek_report(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    args = context.args

    if len(args) < 2:
        update.message.reply_text(
            "Format salah. Gunakan: /pempek <jenis_pempek> <jumlah>. Contoh: /pempek kapal_selam 5"
        )
        return

    jenis_pempek = args[0]
    jumlah = int(args[1])

    # Load data lama
    data = load_pempek_data()
    if user_id not in data:
        data[user_id] = {}

    if jenis_pempek not in data[user_id]:
        data[user_id][jenis_pempek] = 0

    # Tambahkan jumlah pempek
    data[user_id][jenis_pempek] += jumlah
    save_pempek_data(data)

    update.message.reply_text(
        f"Berhasil menambahkan {jumlah} {jenis_pempek} ke laporan."
    )

# Tampilkan laporan penjualan
def show_pempek_report(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    data = load_pempek_data()

    if user_id not in data or not data[user_id]:
        update.message.reply_text("Belum ada laporan penjualan.")
        return

    report = "Laporan Penjualan Pempek:\n"
    for jenis, jumlah in data[user_id].items():
        report += f"- {jenis}: {jumlah}\n"

    update.message.reply_text(report)
