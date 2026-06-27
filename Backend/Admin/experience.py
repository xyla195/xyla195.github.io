from flask import Blueprint, request, jsonify, session
from model import get_db_connection

experience_bp = Blueprint('experience', __name__)

@experience_bp.route('/', methods=['GET'])
def get_experiences():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM experiences")
    experiences = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(experiences), 200

@experience_bp.route('/', methods=['POST'])
def create_experience():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or request.form
    title = data.get('title')
    company = data.get('company')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')

    if not title or not company or not start_date or not end_date:
        return jsonify({'error': 'Semua field tanggal dan posisi wajib diisi!'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO experiences (title, company, start_date, end_date, description) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (title, company, start_date, end_date, description))
    db.commit() # FIXED: Tambahan commit agar masuk ke database
    cursor.close()
    db.close()
    return jsonify({'message': 'Pengalaman berhasil ditambahkan!'}), 201

@experience_bp.route('/<int:id>', methods=['PUT', 'POST'])
def update_experience(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or request.form
    title = data.get('title')
    company = data.get('company')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')

    db = get_db_connection()
    cursor = db.cursor()
    query = "UPDATE experiences SET title=%s, company=%s, start_date=%s, end_date=%s, description=%s WHERE id=%s"
    cursor.execute(query, (title, company, start_date, end_date, description, id))
    db.commit() # FIXED: Tambahan commit
    cursor.close()
    db.close()
    return jsonify({'message': 'Pengalaman berhasil diubah!'}), 200

@experience_bp.route('/<int:id>', methods=['DELETE'])
def delete_experience(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM experiences WHERE id=%s", (id,))
    db.commit() # FIXED: Tambahan commit
    cursor.close()
    db.close()
    return jsonify({'message': 'Pengalaman berhasil dihapus!'}), 200