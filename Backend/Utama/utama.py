from flask import Blueprint, render_template, request, jsonify
from model import get_db_connection
import resend
from config import Config

utama_bp = Blueprint('utama', __name__)

# Konfigurasi Resend API Key
resend.api_key = Config.RESEND_API_KEY

@utama_bp.route('/')
def index():
    db = get_db_connection()
    if not db:
        return "Gagal koneksi ke database cloud.", 500
        
    try:
        cursor = db.cursor()
        
        # Ambil data dari TiDB untuk ditampilkan secara dinamis
        cursor.execute("SELECT * FROM profiles LIMIT 1")
        profile = cursor.fetchone()
        
        cursor.execute("SELECT * FROM skills")
        skills = cursor.fetchall()
        
        cursor.execute("SELECT * FROM experiences")
        experiences = cursor.fetchall()
        
        # Ambil data proyek (Ini yang akan dikirim ke halaman depan!)
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        
    except Exception as e:
        print(f"Error saat mengambil data untuk halaman utama: {e}")
        profile, skills, experiences, projects = None, [], [], []
    finally:
        cursor.close()
        db.close()
    
    # Merender file index.html yang berada langsung di root direktori templates/portofolio/
    return render_template('index.html', profile=profile, skills=skills, experiences=experiences, projects=projects)

@utama_bp.route('/contact', methods=['POST'])
def contact():
    data = request.get_json() or request.form
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject', 'Pesan Kontak Baru Portofolio')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'Semua field wajib diisi!'}), 400

    db = get_db_connection()
    
    try:
        cursor = db.cursor()
        
        # 1. Simpan pesan ke Database TiDB
        query = "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, subject, message))
        db.commit()  # PENTING: Wajib commit agar data benar-benar tersimpan di database
        
        # 2. Kirim notifikasi Email menggunakan Resend
        params = {
            "from": "onboarding@resend.dev",
            "to": "priskilavivo@gmail.com",
            "subject": f"Kontak Baru: {subject}",
            "html": f"<p><strong>Nama:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Pesan:</strong> {message}</p>",
        }
        resend.Emails.send(params)
        
        return jsonify({'message': 'Pesan berhasil disimpan dan email terkirim!'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500
    finally:
        if db: 
            cursor.close()
            db.close()