import os
import resend
from flask import Blueprint, request, jsonify
from model import get_db_connection

contact_bp = Blueprint('contact', __name__)

# Mengambil API Key dari .env
resend.api_key = os.getenv("RESEND_API_KEY")

@contact_bp.route('/', methods=['POST'])
def send_message():
    try:
        # Mengambil data dari frontend (bisa format JSON atau Form)
        data = request.get_json() or request.form
        name = data.get('name')
        sender_email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, sender_email, subject, message]):
            return jsonify({'error': 'Semua field wajib diisi!'}), 400

        # --- OPSIONAL: Simpan ke Database TiDB ---
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                (name, sender_email, subject, message)
            )
            db.commit()
            cursor.close()
            db.close()
        except Exception as db_err:
            print("Info: Gagal simpan ke DB (Mungkin tabel 'messages' belum ada). Error:", db_err)
            pass # Lanjut kirim email walaupun gagal simpan ke database

        # --- FUNGSI UTAMA: Kirim Email via Resend ---
        # PENTING: Karena ini akun gratis, "to" WAJIB sama dengan email yang lo pake daftar Resend.com
        target_email = "priskilavivo@gmail.com" 

        html_content = f"""
        <h3>Pesan Baru dari Web Portofolio</h3>
        <p><strong>Nama Pengirim:</strong> {name}</p>
        <p><strong>Email Pengirim:</strong> {sender_email}</p>
        <p><strong>Subjek:</strong> {subject}</p>
        <p><strong>Isi Pesan:</strong><br>{message}</p>
        """

        # Eksekusi pengiriman
        r = resend.Emails.send({
            "from": "onboarding@resend.dev", # Wajib pakai domain bawaan resend untuk akun gratis
            "to": target_email,
            "subject": f"Portofolio - {subject}",
            "html": html_content
        })

        return jsonify({'message': 'Sukses! Pesan berhasil disimpan dan email terkirim!'}), 200

    except Exception as e:
        print("Resend Error:", str(e))
        return jsonify({'error': str(e)}), 500