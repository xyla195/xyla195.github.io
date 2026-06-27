from flask import Blueprint, request, jsonify, session
from model import get_db_connection

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/', methods=['GET'])
def get_skills():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor() 
    cursor.execute("SELECT id, name, percentage, category FROM skills")
    rows = cursor.fetchall()
    
    skills = []
    for row in rows:
        skills.append({
            'id': row[0],
            'name': row[1],
            'percentage': row[2],
            'category': row[3]
        })
        
    cursor.close()
    db.close()
    return jsonify(skills), 200

@skills_bp.route('/', methods=['POST'])
def create_skill():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or request.form
    name = data.get('name')
    percentage = data.get('percentage')
    category = data.get('category')

    if not name or not percentage:
        return jsonify({'error': 'Nama skill dan persentase wajib diisi!'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO skills (name, percentage, category) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, percentage, category))
    db.commit() 
    cursor.close()
    db.close()
    return jsonify({'message': 'Skill berhasil ditambahkan!'}), 201

@skills_bp.route('/<int:id>', methods=['PUT', 'POST'])
def update_skill(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or request.form
    name = data.get('name')
    percentage = data.get('percentage')
    category = data.get('category')

    db = get_db_connection()
    cursor = db.cursor()
    query = "UPDATE skills SET name=%s, percentage=%s, category=%s WHERE id=%s"
    cursor.execute(query, (name, percentage, category, id))
    db.commit() 
    cursor.close()
    db.close()
    return jsonify({'message': 'Skill berhasil diubah!'}), 200

@skills_bp.route('/<int:id>', methods=['DELETE'])
def delete_skill(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM skills WHERE id=%s", (id,))
    db.commit() 
    cursor.close()
    db.close()
    return jsonify({'message': 'Skill berhasil dihapus!'}), 200