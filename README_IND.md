# Sistem Informasi Perizinan DPMPTSP

Aplikasi manajemen data perizinan berbasis web untuk Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu Provinsi Lampung.

## Fitur

- **Input Data**: Memasukkan data perizinan baru dengan autocomplete
- **Masa Berlaku**: Memantau status masa berlaku perizinan (mendukung fitur seumur hidup terkalibrasi)
- **SLA Monitoring**: Memantau ketepatan waktu penyelesaian
- **Tabel Data**: Melihat, memfilter, dan mengedit data dalam bentuk tabel interaktif
- **Import Data**: Mengimpor data dari file Excel secara otomatis dengan *data mapping*
- **Dashboard**: Visualisasi dan analitik data (berbasis Tahun, Bulan, TW, dll)

### Pembaruan Terbaru (Maret 2026)
- Penambahan opsi **Risiko** ("RENDAH", "MENENGAH RENDAH")
- Penambahan opsi **Jenis Permohonan** ("Perubahan")
- Penambahan isian teks fleksibel untuk **Masa Berlaku**
- Standardisasi parameter masa berlaku seumur hidup menjadi **"Selama Pelaku Usaha Menjalankan Kegiatan Usaha"**
- Penambahan kolom **Rencana Nilai Investasi**

## Instalasi

### Prasyarat
- Python 3.8+
- pip

### Langkah Instalasi

```bash
# Clone atau download repository
cd path/to/folder

# Install dependensi
pip install streamlit pandas openpyxl plotly

# Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## Struktur Folder

```
/
├── app.py                 # Entry point aplikasi
├── database.py            # Fungsi database SQLite
├── perizinan.db           # Database SQLite
├── a.txt                  # Daftar sektor
├── extractor.py           # Ekstraksi data Excel (standalone)
└── pages/
    ├── Home.py            # Halaman beranda
    ├── 1_Input_Data.py    # Form input perizinan
    ├── 2_Data_Perizinan.py# Data masa berlaku
    ├── 3_Analytics.py     # Dashboard analitik
    ├── 4_Tabel_Data.py    # Tabel data editable
    ├── 5_Import_Data.py   # Import dari Excel
    └── 6_SLA_Monitoring.py# Monitoring SLA
```

## Teknologi

- Streamlit (Frontend)
- SQLite (Database)
- Pandas (Data Processing)
- Plotly (Visualisasi)

## Lisensi

Internal use only - DPMPTSP Provinsi Lampung
