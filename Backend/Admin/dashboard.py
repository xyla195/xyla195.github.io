import os
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from werkzeug.utils import secure_filename
from model import get_db_connection

# IMPORT LIBRARY CLOUDINARY BARU
import cloudinary
import cloudinary.uploader

dashboard_bp = Blueprint('dashboard', __name__)

# ====================================================================
# KONFIGURASI CLOUDINARY
# ====================================================================
# Silakan ganti value di bawah ini sesuai dengan yang ada di Dashboard Cloudinary milikmu.
# Atau jika kamu sudah setting di .env / app.py, baris ini bisa membaca dari os.environ.
cloudinary.config( 
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'ISI_CLOUD_NAME_MU_DISINI'), 
    api_key = os.environ.get('CLOUDINARY_API_KEY', 'ISI_API_KEY_MU_DISINI'), 
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'ISI_API_SECRET_MU_DISINI'),
    secure = True
)

# ====================================================================
# RUTE 1: HALAMAN DASHBOARD UTAMA (UNTUK STATISTIK)
# ====================================================================
@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard_home():
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))
    
    db = get_db_connection()
    stats = {'skills': 0, 'experiences': 0, 'projects': 0, 'contacts': 0}
    
    if db:
        cursor = db.cursor() 
        try:
            cursor.execute("SELECT COUNT(*) FROM skills")
            res = cursor.fetchone()
            stats['skills'] = res[0] if isinstance(res, (tuple, list)) else list(res.values())[0]
            
            cursor.execute("SELECT COUNT(*) FROM experiences")
            res = cursor.fetchone()
            stats['experiences'] = res[0] if isinstance(res, (tuple, list)) else list(res.values())[0]
            
            cursor.execute("SELECT COUNT(*) FROM projects")
            res = cursor.fetchone()
            stats['projects'] = res[0] if isinstance(res, (tuple, list)) else list(res.values())[0]
            
            cursor.execute("SELECT COUNT(*) FROM contacts")
            res = cursor.fetchone()
            stats['contacts'] = res[0] if isinstance(res, (tuple, list)) else list(res.values())[0]
        except Exception as e:
            print(f"Gagal mengambil statistik dashboard: {e}")
        finally:
            cursor.close()
            db.close()

    return render_template('admin/dashboard.html', username=session.get('username'), stats=stats)


# ====================================================================
# RUTE 2: HALAMAN MANAGEMENT CRUD (PROFIL & SKILL)
# ====================================================================
@dashboard_bp.route('/', methods=['GET'])
def admin_manage():
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))
        
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT name, title, bio, photo_url, email, location FROM profiles WHERE id = 1")
    row_profile = cursor.fetchone()
    profile = None
    
    if row_profile:
        if isinstance(row_profile, dict):
            profile = row_profile
        else:
            profile = {
                'name': row_profile[0],
                'title': row_profile[1],
                'bio': row_profile[2],
                'photo_url': row_profile[3],
                'email': row_profile[4],
                'location': row_profile[5]
            }
    
    cursor.execute("SELECT id, name, percentage FROM skills")
    rows_skills = cursor.fetchall()
    skills = []
    
    for row in rows_skills:
        if isinstance(row, dict):
            skills.append(row)
        else:
            skills.append({
                'id': row[0],
                'name': row[1],
                'percentage': row[2]
            })
    
    cursor.close()
    db.close()
    
    return render_template('admin/profiles.html', 
                           username=session.get('username'),
                           profile=profile, 
                           skills=skills)


# ====================================================================
# RUTE 3: HALAMAN MANAGEMENT CRUD PENGALAMAN
# ====================================================================
@dashboard_bp.route('/experiences', methods=['GET'])
def admin_experiences():
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))
        
    db = get_db_connection()
    cursor = db.cursor()
    experiences = []
    
    try:
        cursor.execute("SELECT * FROM experiences")
        columns = [desc[0].lower() for desc in cursor.description]
        rows = cursor.fetchall()
        
        for r in rows:
            if isinstance(r, dict):
                item = dict(r)
                for k in list(item.keys()):
                    if any(x in k for x in ['year', 'per', 'dur', 'tah', 'waktu', 'start']):
                        item['start_date'] = item[k]
                        item['start'] = item[k]
                if 'start_date' not in item: item['start_date'] = ''
                if 'end_date' not in item: item['end_date'] = ''
                if 'description' not in item: item['description'] = ''
                experiences.append(item)
            else:
                item = {}
                for idx, col in enumerate(columns):
                    item[col] = r[idx]
                
                if 'id' not in item and len(r) > 0: item['id'] = r[0]
                if 'title' not in item and len(r) > 1: item['title'] = r[1]
                if 'company' not in item and len(r) > 2: item['company'] = r[2]
                if 'start_date' not in item:
                    item['start_date'] = r[3] if len(r) > 3 else ''
                if 'end_date' not in item:
                    item['end_date'] = r[4] if len(r) > 4 else ''
                if 'description' not in item:
                    item['description'] = r[5] if len(r) > 5 else ''
                
                experiences.append(item)
    except Exception as e:
        print(f"Error sistem saat membaca data pengalaman: {e}")
        experiences = []
    finally:
        cursor.close()
        db.close()
        
    return render_template('admin/experiences.html', username=session.get('username'), experiences=experiences)


# ====================================================================
# RUTE 4: HALAMAN MANAGEMENT CRUD PROYEK
# ====================================================================
@dashboard_bp.route('/projects', methods=['GET'])
def admin_projects():
    if not session.get('logged_in'):
        return redirect(url_for('login.login'))
        
    db = get_db_connection()
    cursor = db.cursor()
    projects = []
    
    try:
        cursor.execute("SELECT * FROM projects")
        columns = [desc[0].lower() for desc in cursor.description]
        rows = cursor.fetchall()
        
        for r in rows:
            if isinstance(r, dict):
                item = dict(r)
                for k in list(item.keys()):
                    if 'desc' in k:
                        item['description'] = item[k]
                projects.append(item)
            else:
                item = {}
                for idx, col in enumerate(columns):
                    item[col] = r[idx]
                
                for col in columns:
                    if 'desc' in col:
                        item['description'] = item[col]
                        break
                
                if 'description' not in item and len(r) > 2:
                    item['description'] = r[2]
                
                if 'id' not in item and len(r) > 0: item['id'] = r[0]
                if 'title' not in item and len(r) > 1: item['title'] = r[1]
                
                projects.append(item)
    except Exception as e:
        print(f"Sistem otomatis mengamankan error proyek: {e}")
        projects = []
    finally:
        cursor.close()
        db.close()
        
    return render_template('admin/projects.html', username=session.get('username'), projects=projects)


# ====================================================================
# API PROFIL: SIMPAN PERUBAHAN PROFIL & REVISI REKAYASA INTEGRASI CLOUDINARY
# ====================================================================
@dashboard_bp.route('/api/profiles/update', methods=['POST'])
def api_update_profile():
    if not session.get('logged_in'):
        return jsonify({'message': 'Silakan login terlebih dahulu'}), 401
        
    name = request.form.get('name')
    title = request.form.get('title')
    bio = request.form.get('bio')
    email = request.form.get('email')
    location = request.form.get('location')
    existing_photo_url = request.form.get('existing_photo_url')
    
    photo_url = existing_photo_url if existing_photo_url else ''
    
    file = None
    if 'photo_file' in request.files:
        file = request.files['photo_file']
    elif 'photo_url' in request.files:
        file = request.files['photo_url']
        
    if file and file.filename != '':
        try:
            # INTEGRASI UTAMA: Upload stream file langsung ke Cloudinary Assets
            upload_result = cloudinary.uploader.upload(
                file,
                folder="portfolio_assets"  # Otomatis membuat folder ini di Cloudinary kamu
            )
            
            # Ambil URL HTTPS Secure resmi dari Cloudinary untuk disimpan ke database TiDB
            photo_url = upload_result.get('secure_url')
            print(f"Sukses upload Cloudinary! URL: {photo_url}")
            
        except Exception as e:
            print(f"Gagal melakukan upload berkas ke Cloudinary: {e}")
            return jsonify({'message': f'Gagal upload ke Cloudinary: {e}'}), 500
                
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM profiles WHERE id = 1")
        if cursor.fetchone():
            cursor.execute("""
                UPDATE profiles 
                SET name=%s, title=%s, bio=%s, email=%s, location=%s, photo_url=%s 
                WHERE id = 1
            """, (name, title, bio, email, location, photo_url))
        else:
            cursor.execute("""
                INSERT INTO profiles (id, name, title, bio, email, location, photo_url) 
                VALUES (1, %s, %s, %s, %s, %s, %s)
            """, (name, title, bio, email, location, photo_url))
        db.commit()
        return jsonify({'message': 'Profil dan Foto sukses di-upload ke Cloudinary & TiDB Cloud!'}), 200
    except Exception as e:
        return jsonify({'message': f'Gagal update profil ke TiDB Cloud: {e}'}), 500
    finally:
        cursor.close()
        db.close()


# ====================================================================
# API SKILL: TAMBAH DAN HAPUS SKILL
# ====================================================================
@dashboard_bp.route('/api/skills/', methods=['POST'])
def api_add_skill():
    if not session.get('logged_in'):
        return jsonify({'message': 'Silakan login terlebih dahulu'}), 401
        
    data = request.json
    name = data.get('name')
    percentage = data.get('percentage')
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO skills (name, percentage) VALUES (%s, %s)", (name, percentage))
        db.commit()
        return jsonify({'message': 'Skill berhasil ditambahkan!'}), 200
    except Exception as e:
        return jsonify({'message': f'Gagal tambah skill: {e}'}), 500
    finally:
        cursor.close()
        db.close()

@dashboard_bp.route('/api/skills/<int:id>', methods=['DELETE'])
def api_delete_skill(id):
    if not session.get('logged_in'):
        return jsonify({'message': 'Silakan login terlebih dahulu'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM skills WHERE id = %s", (id,))
        db.commit()
        return jsonify({'message': 'Skill berhasil dihapus!'}), 200
    except Exception as e:
        return jsonify({'message': f'Gagal hapus skill: {e}'}), 500
    finally:
        cursor.close()
        db.close()


# ====================================================================
# API PENGALAMAN (API PROYEK SUDAH DIHAPUS AGAR TIDAK BENTROK)
# ====================================================================
@dashboard_bp.route('/api/experiences/', methods=['POST'])
def api_add_experience():
    if not session.get('logged_in'):
        return jsonify({'message': 'Silakan login terlebih dahulu'}), 401
    
    data = request.json
    title = data.get('title')
    company = data.get('company')
    years = data.get('years', '')
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM experiences LIMIT 1")
        columns = [desc[0].lower() for desc in cursor.description]
        
        cols_to_insert = ['title', 'company']
        vals_to_insert = [title, company]
        
        kolom_mulai = None
        for col in columns:
            if any(x in col for x in ['start_date', 'year', 'per', 'dur', 'tah', 'waktu', 'start']):
                kolom_mulai = col
                break
                
        if kolom_mulai:
            cols_to_insert.append(kolom_mulai)
            vals_to_insert.append(years)
            
        if 'end_date' in columns:
            cols_to_insert.append('end_date')
            vals_to_insert.append('-')
            
        if 'description' in columns:
            cols_to_insert.append('description')
            vals_to_insert.append('-')
            
        placeholders = ', '.join(['%s'] * len(cols_to_insert))
        col_names = ', '.join(cols_to_insert)
        query = f"INSERT INTO experiences ({col_names}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(vals_to_insert))
        db.commit()
    except Exception as e:
        return jsonify({'message': f'Gagal menyimpan ke database: {e}'}), 500
    finally:
        cursor.close()
        db.close()
        
    return jsonify({'message': 'Data pengalaman berhasil ditambahkan!'}), 200

@dashboard_bp.route('/api/experiences/<int:id>', methods=['DELETE'])
def api_delete_experience(id):
    if not session.get('logged_in'):
        return jsonify({'message': 'Silakan login terlebih dahulu'}), 401
        
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM experiences WHERE id = %s", (id,))
        db.commit()
    except Exception as e:
        return jsonify({'message': f'Error hapus data: {e}'}), 500
    finally:
        cursor.close()
        db.close()
    
    return jsonify({'message': 'Data pengalaman berhasil dihapus!'}), 200