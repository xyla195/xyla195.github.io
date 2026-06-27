import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()

class Config:
    # TiDB Database Configuration
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 4000))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_CA_PATH = os.getenv("DB_CA_PATH")

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Resend Email Configuration
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")