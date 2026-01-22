import sqlite3
import os
from datetime import datetime

DB_PATH = "perizinan.db"

def init_database():
    """Inisialisasi database dan tabel"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabel data perizinan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perizinan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sektor TEXT NOT NULL,
        kategori_perizinan TEXT NOT NULL,
        nama_pengguna_layanan TEXT,
        nib TEXT,
        alamat TEXT,
        pemilik_pengurus TEXT,
        lokasi_usaha TEXT,
        luas_lahan_usaha TEXT,
        kbli TEXT,
        jenis_usaha TEXT,
        resiko TEXT,
        kapasitas TEXT,
        jenis_permohonan TEXT,
        nomor_permohonan TEXT,
        tanggal_permohonan TEXT,
        nomor_tanggal_permohonan_rekomendasi TEXT,
        nomor_tanggal_rekomendasi TEXT,
        nomor_izin TEXT,
        tanggal_izin TEXT,
        masa_berlaku TEXT,
        npwp TEXT,
        telepon TEXT,
        email TEXT,
        keterangan TEXT,
        jenis_dokumen TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def insert_perizinan(data):
    """Insert data perizinan baru"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO perizinan (
        sektor, kategori_perizinan, nama_pengguna_layanan, nib, alamat, pemilik_pengurus,
        lokasi_usaha, luas_lahan_usaha, kbli, jenis_usaha, resiko,
        kapasitas, jenis_permohonan, nomor_permohonan, tanggal_permohonan,
        nomor_tanggal_permohonan_rekomendasi,
        nomor_tanggal_rekomendasi, nomor_izin, tanggal_izin,
        masa_berlaku, npwp, telepon, email, keterangan, jenis_dokumen
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['sektor'], data['kategori_perizinan'], data['nama_pengguna_layanan'], data['nib'],
        data['alamat'], data['pemilik_pengurus'], data['lokasi_usaha'],
        data['luas_lahan_usaha'], data['kbli'], data['jenis_usaha'],
        data['resiko'], data['kapasitas'], data['jenis_permohonan'],
        data['nomor_permohonan'], data['tanggal_permohonan'],
        data['nomor_tanggal_permohonan_rekomendasi'],
        data['nomor_tanggal_rekomendasi'],
        data['nomor_izin'], data['tanggal_izin'], data['masa_berlaku'],
        data['npwp'], data['telepon'], data['email'], data.get('keterangan', ''), data.get('jenis_dokumen', '')
    ))
    
    conn.commit()
    conn.close()

def get_all_perizinan(sektor=None):
    """Ambil semua data perizinan, optional filter by sektor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if sektor:
        cursor.execute("SELECT * FROM perizinan WHERE sektor = ? ORDER BY created_at DESC", (sektor,))
    else:
        cursor.execute("SELECT * FROM perizinan ORDER BY created_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    return rows

def get_perizinan_by_id(id):
    """Ambil data perizinan by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM perizinan WHERE id = ?", (id,))
    row = cursor.fetchone()
    
    conn.close()
    return row

def update_perizinan(id, data):
    """Update data perizinan"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE perizinan SET
        sektor = ?, kategori_perizinan = ?, nama_pengguna_layanan = ?, nib = ?, alamat = ?,
        pemilik_pengurus = ?, lokasi_usaha = ?, luas_lahan_usaha = ?,
        kbli = ?, jenis_usaha = ?, resiko = ?, kapasitas = ?,
        jenis_permohonan = ?, nomor_permohonan = ?, tanggal_permohonan = ?,
        nomor_tanggal_permohonan_rekomendasi = ?,
        nomor_tanggal_rekomendasi = ?, nomor_izin = ?,
        tanggal_izin = ?, masa_berlaku = ?, npwp = ?, telepon = ?, email = ?,
        keterangan = ?, jenis_dokumen = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (
        data['sektor'], data['kategori_perizinan'], data['nama_pengguna_layanan'], data['nib'],
        data['alamat'], data['pemilik_pengurus'], data['lokasi_usaha'],
        data['luas_lahan_usaha'], data['kbli'], data['jenis_usaha'],
        data['resiko'], data['kapasitas'], data['jenis_permohonan'],
        data['nomor_permohonan'], data['tanggal_permohonan'],
        data['nomor_tanggal_permohonan_rekomendasi'],
        data['nomor_tanggal_rekomendasi'],
        data['nomor_izin'], data['tanggal_izin'], data['masa_berlaku'],
        data['npwp'], data['telepon'], data['email'], data.get('keterangan', ''), data.get('jenis_dokumen', ''), id
    ))
    
    conn.commit()
    conn.close()

def delete_perizinan(id):
    """Hapus data perizinan"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM perizinan WHERE id = ?", (id,))
    
    conn.commit()
    conn.close()

def search_field_suggestions(field_name, search_term, limit=3):
    """Search suggestions untuk field tertentu"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Validasi field name untuk keamanan
    valid_fields = [
        'nama_pengguna_layanan', 'nib', 'alamat', 'pemilik_pengurus',
        'lokasi_usaha', 'luas_lahan_usaha', 'kbli', 'jenis_usaha',
        'kapasitas', 'jenis_permohonan', 'nomor_permohonan',
        'nomor_permohonan_rekomendasi', 'nomor_tanggal_rekomendasi',
        'nomor_izin', 'masa_berlaku', 'npwp', 'telepon', 'email', 'keterangan'
    ]
    
    if field_name not in valid_fields:
        conn.close()
        return []
    
    # Query untuk mendapatkan distinct values yang mengandung search term
    query = f"""
    SELECT DISTINCT {field_name}
    FROM perizinan
    WHERE {field_name} LIKE ? AND {field_name} IS NOT NULL AND {field_name} != ''
    ORDER BY {field_name}
    LIMIT ?
    """
    
    cursor.execute(query, (f'%{search_term}%', limit))
    results = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return results


def get_available_years():
    """Get list of available years from perizinan data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT DISTINCT strftime('%Y', tanggal_permohonan) as year 
    FROM perizinan 
    WHERE tanggal_permohonan IS NOT NULL AND tanggal_permohonan != '' 
    ORDER BY year DESC
    """
    
    cursor.execute(query)
    years = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return years

def get_analytics_metrics(period=None):
    """
    Get analytics metrics based on period filter
    period dict:
    - type: 'yearly', 'quarterly', 'monthly'
    - year: 'YYYY'
    - quarter: 'TW1', 'TW2', 'TW3', 'TW4' (optional)
    - month: 1-12 (optional)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Base WHERE clause
    where_clauses = ["tanggal_permohonan IS NOT NULL", "tanggal_permohonan != ''"]
    params = []
    
    if period:
        # Filter by year
        if 'year' in period:
            where_clauses.append("strftime('%Y', tanggal_permohonan) = ?")
            params.append(str(period['year']))
            
        # Filter by specific period type
        if period['type'] == 'monthly' and 'month' in period:
            where_clauses.append("CAST(strftime('%m', tanggal_permohonan) AS INTEGER) = ?")
            params.append(period['month'])
            
        elif period['type'] == 'quarterly' and 'quarter' in period:
            q_map = {
                'TW1': ['01', '02', '03'],
                'TW2': ['04', '05', '06'],
                'TW3': ['07', '08', '09'],
                'TW4': ['10', '11', '12']
            }
            months = q_map.get(period['quarter'], [])
            if months:
                placeholders = ','.join(['?'] * len(months))
                where_clauses.append(f"strftime('%m', tanggal_permohonan) IN ({placeholders})")
                params.extend(months)
    
    where_sql = " AND ".join(where_clauses)
    
    metrics = {}
    
    # 1. Jumlah Pelaku Usaha (Count Distinct Nama - All data)
    cursor.execute("SELECT COUNT(DISTINCT nama_pengguna_layanan) FROM perizinan")
    metrics['jumlah_pelaku'] = cursor.fetchone()[0] or 0
    
    # 2. Total NIB (Count Distinct NIB - All data)
    cursor.execute("SELECT COUNT(DISTINCT nib) FROM perizinan")
    metrics['total_nib'] = cursor.fetchone()[0] or 0
    
    # 3. Average Process Time (SLA) - Only records with valid dates
    cursor.execute("""
        SELECT AVG(julianday(tanggal_izin) - julianday(tanggal_permohonan))
        FROM perizinan 
        WHERE tanggal_izin IS NOT NULL AND tanggal_izin != ''
        AND tanggal_permohonan IS NOT NULL AND tanggal_permohonan != ''
    """)
    metrics['avg_sla'] = round(cursor.fetchone()[0] or 0, 1)

    # 4. Risk Distribution (All data)
    cursor.execute("""
        SELECT resiko, COUNT(*) 
        FROM perizinan 
        WHERE resiko IS NOT NULL AND resiko != ''
        GROUP BY resiko
        ORDER BY COUNT(*) DESC
    """)
    metrics['risk_distribution'] = cursor.fetchall()
    
    # 4. Kategori Distribution (All data, not filtered by date)
    cursor.execute("""
        SELECT kategori_perizinan, COUNT(*) 
        FROM perizinan 
        WHERE kategori_perizinan IS NOT NULL AND kategori_perizinan != ''
        GROUP BY kategori_perizinan
        ORDER BY COUNT(*) DESC
    """)
    metrics['kategori_distribution'] = cursor.fetchall()
    
    # 5. Time Trend (All data with valid dates)
    cursor.execute("""
        SELECT strftime('%Y-%m', tanggal_permohonan) as month, COUNT(*) 
        FROM perizinan 
        WHERE tanggal_permohonan IS NOT NULL AND tanggal_permohonan != ''
        GROUP BY month
        ORDER BY month
    """)
    metrics['time_trend'] = cursor.fetchall()
    
    # 6. Jenis Permohonan Distribution (All data)
    cursor.execute("""
        SELECT jenis_permohonan, COUNT(*) 
        FROM perizinan 
        WHERE jenis_permohonan IS NOT NULL AND jenis_permohonan != ''
        GROUP BY jenis_permohonan
        ORDER BY COUNT(*) DESC
    """)
    metrics['jenis_permohonan_dist'] = cursor.fetchall()
    
    # 7. Geo Distribution (All data, Top 10)
    cursor.execute("""
        SELECT lokasi_usaha, COUNT(*) 
        FROM perizinan 
        WHERE lokasi_usaha IS NOT NULL AND lokasi_usaha != ''
        GROUP BY lokasi_usaha
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)
    metrics['geo_distribution'] = cursor.fetchall()
    
    # 8. Jenis Dokumen Distribution (All data, not filtered by date)
    cursor.execute("""
        SELECT jenis_dokumen, COUNT(*) 
        FROM perizinan 
        WHERE jenis_dokumen IS NOT NULL AND jenis_dokumen != ''
        GROUP BY jenis_dokumen
        ORDER BY COUNT(*) DESC
    """)
    metrics['jenis_dokumen_dist'] = cursor.fetchall()
    
    conn.close()
    return metrics
