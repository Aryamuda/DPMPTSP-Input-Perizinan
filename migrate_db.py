"""
Skrip migrasi database perizinan.db
Tujuan: Update semua data lama yang menggunakan 'Seumur Hidup' 
        menjadi 'Selama Pelaku Usaha Menjalankan Kegiatan Usaha'

Jalankan sekali saja setelah pull dari VPS:
    python migrate_db.py
"""
import sqlite3

DB_PATH = "perizinan.db"

OLD_LIFETIME_VALUES = [
    "Seumur Hidup",
    "seumur hidup",
    "SEUMUR HIDUP",
]

NEW_LIFETIME_VALUE = "Selama Pelaku Usaha Menjalankan Kegiatan Usaha"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_updated = 0
    for old_val in OLD_LIFETIME_VALUES:
        cursor.execute(
            "UPDATE perizinan SET masa_berlaku = ? WHERE masa_berlaku = ?",
            (NEW_LIFETIME_VALUE, old_val)
        )
        count = cursor.rowcount
        if count > 0:
            print(f"  Updated {count} row(s) dari '{old_val}' -> '{NEW_LIFETIME_VALUE}'")
            total_updated += count
    
    conn.commit()
    conn.close()
    
    if total_updated == 0:
        print("Tidak ada data yang perlu dimigrasi.")
    else:
        print(f"\nTotal {total_updated} baris berhasil diupdate.")

if __name__ == "__main__":
    print("=== Migrasi Database Perizinan ===")
    print(f"DB: {DB_PATH}\n")
    migrate()
    print("\nMigrasi selesai. Anda sekarang bisa push ke VPS.")
