import pymysql
from config import Config

def get_db_connection():
    """
    Fungsi untuk membuat dan mengembalikan koneksi ke database TiDB Cloud.
    Menggunakan konfigurasi SSL/TLS jika sertifikat CA disediakan.
    """
    try:
        # Menyiapkan konfigurasi SSL jika path CA_PATH terisi di .env
        ssl_config = None
        if Config.DB_CA_PATH:
            ssl_config = {'ssl': {'ca': Config.DB_CA_PATH}}
            
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            ssl=ssl_config,
            cursorclass=pymysql.cursors.DictCursor, # Hasil query otomatis berformat Dictionary (key-value)
            autocommit=True # Otomatis nge-save setiap ada perubahan data (INSERT/UPDATE/DELETE)
        )
        return connection
    except Exception as e:
        print(f"Error saat mencoba koneksi ke TiDB Cloud: {e}")
        return None