from flask import Blueprint, request, jsonify, session
from model import get_db_connection

profiles_bp = Blueprint('profiles', __name__)

@profiles_bp.route('/', methods=['GET'])
def get_profile():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    if not db:
        return jsonify({'error': 'Gagal koneksi database'}), 500
        
    cursor = db.cursor()
    cursor.execute("SELECT * FROM profiles LIMIT 1")
    profile = cursor.fetchone()
    cursor.close()
    db.close()
    
    return jsonify(profile or {}), 200

@profiles_bp.route('/', methods=['POST'])
def save_profile():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or request.form
    name = data.get('name')
    title = data.get('title')
    bio = data.get('bio')
    photo_url = data.get('photo_url')
    cv_url = data.get('cv_url')
    email = data.get('email')
    phone = data.get('phone')
    location = data.get('location')

    if not name or not title:
        return jsonify({'error': 'Nama dan Title wajib diisi!'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM profiles LIMIT 1")
    existing = cursor.fetchone()
    
    if existing:
        query = """
            UPDATE profiles 
            SET name=%s, title=%s, bio=%s, photo_url=%s, cv_url=%s, email=%s, phone=%s, location=%s 
            WHERE id=%s
        """
        # FIXED: Panggil existing[0] karena fetchone() me-return Tuple
        cursor.execute(query, (name, title, bio, photo_url, cv_url, email, phone, location, existing[0]))
    else:
        query = """
            INSERT INTO profiles (name, title, bio, photo_url, cv_url, email, phone, location) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, title, bio, photo_url, cv_url, email, phone, location))
        
    db.commit() # FIXED: Tambahan commit wajib untuk nyimpen
    cursor.close()
    db.close()
    return jsonify({'message': 'Profil berhasil diperbarui!'}), 200