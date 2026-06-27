-- 1. Tabel untuk Akun Admin (Login)
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Berisi password (bisa plaintext/hash sesuai kenyamanan coding lo nanti)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel data Profil
CREATE TABLE IF NOT EXISTS profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL, -- Contoh: "Fullstack Web Developer"
    bio TEXT,
    photo_url VARCHAR(255),       -- Diisi URL gambar dari Cloudinary nanti
    cv_url VARCHAR(255),          -- Opsional jika ada link CV
    email VARCHAR(100),
    phone VARCHAR(20),
    location VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Tabel data Skill
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,     -- Contoh: "Python", "HTML", "CSS"
    percentage INT NOT NULL,       -- Nilai 1-100 untuk bar progress
    category VARCHAR(50)           -- Contoh: "Frontend", "Backend", "Others"
);

-- 4. Tabel data Pengalaman (Experience)
CREATE TABLE IF NOT EXISTS experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,   -- Jabatan, contoh: "Junior Developer Intern"
    company VARCHAR(100) NOT NULL, -- Nama Perusahaan
    start_date VARCHAR(50) NOT NULL, -- Contoh: "Januari 2024"
    end_date VARCHAR(50) NOT NULL,   -- Contoh: "Desember 2024" atau "Sekarang"
    description TEXT
);

-- 5. Tabel data Proyek (Projects)
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),       -- Diisi URL gambar hasil upload Cloudinary
    project_url VARCHAR(255),     -- Link live demo web (opsional)
    repo_url VARCHAR(255)         -- Link GitHub (opsional)
);

-- 6. Tabel data Kontak / Pesan Masuk (Contact)
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(150),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Insert Akun Admin Default (Sesuai dengan instruksi login di pdf)
INSERT INTO admin_users (username, password) 
VALUES ('admin', 'admin123')
ON DUPLICATE KEY UPDATE username=username;