import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify, session
from model import get_db_connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

projects_bp = Blueprint('projects', __name__)

# ==========================================
# 1. API UNTUK AMBIL DATA PROYEK (GET)
# ==========================================
@projects_bp.route('/', methods=['GET'])
def get_projects():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    # Hapus dictionary cursor agar tidak error di sistem Mac
    cursor.execute("SELECT id, title, description, project_url, repo_url, image_url FROM projects")
    rows = cursor.fetchall()
    
    projects = []
    for row in rows:
        projects.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'project_url': row[3],
            'repo_url': row[4],
            'image_url': row[5]
        })
        
    cursor.close()
    db.close()
    return jsonify(projects), 200

# ==========================================
# 2. API UNTUK TAMBAH PROYEK (POST)
# ==========================================
@projects_bp.route('/', methods=['POST'])
def add_project():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        project_url = request.form.get('project_url')
        repo_url = request.form.get('repo_url')
        
        if not title:
            return jsonify({"error": "Judul proyek wajib diisi!"}), 400

        # Cek apakah ada file gambar yang diunggah
        image_url = ""
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            file_to_upload = request.files['image_file']
            upload_result = cloudinary.uploader.upload(
                file_to_upload,
                folder="portfolio/projects"
            )
            image_url = upload_result.get("secure_url")
        else:
            return jsonify({"error": "File gambar wajib diunggah"}), 400

        db = get_db_connection()
        cursor = db.cursor()
        
        sql = """
            INSERT INTO projects (title, description, project_url, repo_url, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title, description, project_url, repo_url, image_url))
        db.commit() # Wajib untuk menyimpan ke TiDB
        
        cursor.close()
        db.close()

        return jsonify({"message": "Proyek berhasil disimpan & diunggah ke Cloudinary!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 3. API UNTUK EDIT PROYEK
# ==========================================
@projects_bp.route('/update/<int:project_id>', methods=['POST'])
def update_project(project_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        project_url = request.form.get('project_url')
        repo_url = request.form.get('repo_url')
        image_url = request.form.get('existing_image_url')

        # Jika user ganti gambar, upload ulang ke Cloudinary
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            file_to_upload = request.files['image_file']
            upload_result = cloudinary.uploader.upload(file_to_upload, folder="portfolio/projects")
            image_url = upload_result.get("secure_url")

        db = get_db_connection()
        cursor = db.cursor()
        
        sql = """
            UPDATE projects 
            SET title=%s, description=%s, project_url=%s, repo_url=%s, image_url=%s 
            WHERE id=%s
        """
        cursor.execute(sql, (title, description, project_url, repo_url, image_url, project_id))
        db.commit()
        
        cursor.close()
        db.close()

        return jsonify({"message": "Data proyek berhasil diperbarui!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 4. API UNTUK HAPUS PROYEK
# ==========================================
@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        db.commit()
        
        cursor.close()
        db.close()
        return jsonify({"message": "Proyek berhasil dihapus!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500