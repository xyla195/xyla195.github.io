from flask import Blueprint, request, jsonify
import cloudinary
import cloudinary.uploader
from config import Config

upload_bp = Blueprint('upload', __name__)

# Konfigurasi Cloudinary dari File .env via Config
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
    file_to_upload = request.files['file']
    if file_to_upload.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    try:
        # Proses upload ke Cloudinary
        upload_result = cloudinary.uploader.upload(file_to_upload, folder="portfolio_assets")
        # Mengembalikan URL gambar yang sukses di-upload
        return jsonify({'secure_url': upload_result['secure_url']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500