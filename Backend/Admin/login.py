from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Jika admin mengakses halaman login via Browser (GET)
    if request.method == 'GET':
        # Jika ternyata sudah login, langsung alihkan ke dashboard
        if session.get('logged_in'):
            return redirect(url_for('dashboard.dashboard_home'))
        return render_template('frontend/Admin/login.html')

    # Jika frontend/admin menekan tombol submit form login (POST)
    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username dan password wajib diisi!'}), 400

    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Gagal koneksi ke database'}), 500
        
    cursor = db.cursor()
    
    # Cek kecocokan username dan password di tabel admin_users (TiDB)
    # Catatan: Sesuai instruksi, akun default-nya adalah admin / admin123
    query = "SELECT * FROM admin_users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    admin = cursor.fetchone()
    
    cursor.close()
    db.close()

    if admin:
        # Jika data cocok, buat session login
        session['logged_in'] = True
        session['username'] = admin['username']
        return jsonify({'message': 'Login berhasil!', 'redirect': url_for('dashboard.dashboard_home')}), 200
    else:
        # Jika salah
        return jsonify({'error': 'Username atau password salah!'}), 401


@login_bp.route('/logout', methods=['GET'])
def logout():
    # Hapus semua data session untuk logout
    session.clear()
    return redirect(url_for('login.login'))