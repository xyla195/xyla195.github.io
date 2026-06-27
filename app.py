from flask import Flask, render_template
from config import Config
import os

app = Flask(__name__, 
            template_folder='.', # <-- UBAH JADI TITIK (.) BIAR FLASK MEMBACA ROOT FOLDER
            static_folder='Frontend')

app.secret_key = os.getenv("SECRET_KEY", "bukan_rahasia_123")

# ==========================================
# IMPORT BLUEPRINTS (LOGIKA BACKEND NYA)
# ==========================================
from Backend.Utama.utama import utama_bp
from Backend.Utama.contact import contact_bp # FIXED: Import file contact yang baru dibuat
from Backend.Admin.login import login_bp
from Backend.Admin.dashboard import dashboard_bp
from Backend.Admin.profiles import profiles_bp
from Backend.Admin.skills import skills_bp
from Backend.Admin.experience import experience_bp
from Backend.Admin.projects import projects_bp
from Backend.Admin.upload import upload_bp

# Registrasi Route ke Flask Application
app.register_blueprint(utama_bp)
app.register_blueprint(contact_bp, url_prefix='/api/contact') # FIXED: Register route contact
app.register_blueprint(login_bp, url_prefix='/admin')
app.register_blueprint(dashboard_bp, url_prefix='/admin')
app.register_blueprint(profiles_bp, url_prefix='/admin/api/profiles')
app.register_blueprint(skills_bp, url_prefix='/admin/api/skills')
app.register_blueprint(experience_bp, url_prefix='/admin/api/experience')
app.register_blueprint(projects_bp, url_prefix='/admin/api/projects')
app.register_blueprint(upload_bp, url_prefix='/admin/api')

if __name__ == '__main__':
    app.run(debug=True, port=5001)