# Panduan Pengguna - Sistem Informasi Perizinan DPMPTSP

## Daftar Isi
1. [Persyaratan Sistem](#persyaratan-sistem)
2. [Cara Instalasi](#cara-instalasi)
3. [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
4. [Panduan Menggunakan Fitur](#panduan-menggunakan-fitur)
5. [Troubleshooting (Mengatasi Masalah)](#troubleshooting)

---

## Persyaratan Sistem

Sebelum memulai, pastikan komputer Anda memiliki:
- **Sistem Operasi**: Windows 10 atau lebih baru
- **RAM**: Minimal 4 GB
- **Ruang Penyimpanan**: Minimal 500 MB ruang kosong
- **Koneksi Internet**: Untuk proses instalasi

---

## Cara Instalasi

### Langkah 1: Install Python

1. Buka browser (Chrome, Edge, atau Firefox)
2. Kunjungi: **https://www.python.org/downloads/**
3. Klik tombol kuning **"Download Python 3.x.x"**
4. Setelah file terdownload, **klik 2x** untuk membuka installer
5. **PENTING**: Centang kotak **"Add Python to PATH"** di bagian bawah
6. Klik **"Install Now"**
7. Tunggu hingga selesai, lalu klik **"Close"**

### Langkah 2: Download Aplikasi

1. Download folder aplikasi dari sumber yang diberikan (USB/email/link)
2. **Extract** (klik kanan → "Extract All") ke lokasi yang mudah diingat
   - Contoh: `C:\Perizinan` atau `D:\AplikasiPerizinan`

### Langkah 3: Install Dependensi

1. Buka **File Explorer**
2. Pergi ke folder aplikasi (contoh: `C:\Perizinan`)
3. Klik pada **address bar** di atas (tempat tertulis lokasi folder)
4. Ketik `cmd` lalu tekan **Enter**
5. Akan muncul jendela hitam (Command Prompt)
6. Ketik perintah berikut lalu tekan **Enter**:
   ```
   pip install streamlit pandas openpyxl plotly
   ```
7. Tunggu hingga proses selesai (muncul tulisan "Successfully installed...")

---

## Cara Menjalankan Aplikasi

### Setiap Kali Ingin Menggunakan Aplikasi:

1. Buka **File Explorer**
2. Pergi ke folder aplikasi (contoh: `C:\Perizinan`)
3. Klik pada **address bar** di atas
4. Ketik `cmd` lalu tekan **Enter**
5. Di jendela hitam, ketik:
   ```
   streamlit run app.py
   ```
6. Tekan **Enter**
7. Browser akan terbuka otomatis dengan aplikasi
8. Jika tidak terbuka, buka browser dan ketik: **http://localhost:8501**

### Cara Menutup Aplikasi:
1. Tutup tab browser
2. Di jendela hitam (Command Prompt), tekan **Ctrl + C**
3. Tutup jendela hitam

---

## Panduan Menggunakan Fitur

### Beranda
Halaman pembuka yang menampilkan informasi umum tentang sistem.

---

### ➕ Input Pendaftaran
Untuk memasukkan data perizinan baru.

**Cara Menggunakan:**
1. Klik menu **"Input Pendaftaran"** di sidebar (panel kiri)
2. **Langkah 1**: Pilih sektor/dinas dari dropdown, lalu klik **"Konfirmasi Sektor"**
3. **Langkah 2**: Isi data perizinan:
   - Nama Pengguna Layanan (wajib)
   - NIB
   - Alamat
   - Dan field lainnya sesuai kebutuhan
4. Pilih **Kategori Perizinan** (Perizinan/Perizinan Berusaha/Non-Perizinan)
5. Pilih **Jenis Dokumen** sesuai kategori
6. Klik **"Simpan Data"**

**Tips**: Saat mengetik, sistem akan menampilkan saran otomatis dari data yang sudah ada. Klik saran untuk mengisi otomatis.

---

### Masa Berlaku
Untuk melihat daftar perizinan berdasarkan status masa berlaku.

**Cara Menggunakan:**
1. Klik menu **"Masa Berlaku"** di sidebar
2. Gunakan filter di bagian atas untuk menyaring data berdasarkan:
   - Sektor
   - Status masa berlaku
   - Rentang tanggal
3. Data akan ditampilkan sesuai filter yang dipilih

---

### SLA Monitoring
Untuk memantau Service Level Agreement (ketepatan waktu) penyelesaian perizinan.

**Cara Menggunakan:**
1. Klik menu **"SLA Monitoring"** di sidebar
2. Lihat kategori-kategori SLA:
   - Tepat waktu
   - Mendekati deadline
   - Terlambat
3. Gunakan filter untuk mempersempit pencarian

---

### Tabel Data
Untuk melihat dan mengedit semua data perizinan dalam bentuk tabel.

**Cara Menggunakan:**
1. Klik menu **"Tabel Data"** di sidebar
2. Gunakan filter di atas tabel untuk mencari data tertentu
3. **Untuk mengedit data**:
   - Klik langsung pada sel yang ingin diubah
   - Ketik nilai baru
   - Klik **"Simpan Perubahan"**

**Catatan**: Kolom ID dan Sektor tidak dapat diubah.

---

### Import Data
Untuk mengimpor data dari file Excel.

**Cara Menggunakan:**
1. Klik menu **"Import Data"** di sidebar
2. Klik **"Browse files"** atau seret file Excel ke area upload
3. Sistem akan menampilkan preview data mentah
4. Periksa pemetaan kolom (mapping) yang ditampilkan
5. Jika sudah benar, klik **"Import Data"**
6. Tunggu proses selesai

**Format File yang Didukung**: `.xlsx` (Excel)

---

### Dashboard
Untuk melihat visualisasi dan analitik data perizinan.

**Cara Menggunakan:**
1. Klik menu **"Dashboard"** di sidebar
2. Lihat berbagai grafik dan statistik:
   - Jumlah perizinan per sektor
   - Distribusi kategori perizinan
   - Distribusi jenis dokumen
   - Dan metrik lainnya
3. Gunakan filter untuk menyaring data yang ditampilkan di grafik

---

## Troubleshooting

### Masalah: "Python tidak ditemukan"
**Solusi**: 
- Pastikan Python sudah terinstall dengan benar
- Pastikan Anda mencentang "Add Python to PATH" saat instalasi
- Restart komputer setelah instalasi

### Masalah: "Module not found" / "No module named..."
**Solusi**: 
Jalankan ulang perintah instalasi:
```
pip install streamlit pandas openpyxl plotly
```

### Masalah: Aplikasi tidak mau dibuka
**Solusi**:
1. Pastikan tidak ada aplikasi lain yang menggunakan port 8501
2. Coba jalankan perintah:
   ```
   streamlit run app.py --server.port 8502
   ```
3. Buka browser dengan alamat: **http://localhost:8502**

### Masalah: Data tidak tersimpan
**Solusi**:
1. Pastikan semua field wajib sudah diisi
2. Pastikan format tanggal sudah benar
3. Periksa pesan error yang muncul

### Masalah: File Excel tidak bisa diimport
**Solusi**:
1. Pastikan format file adalah `.xlsx` (bukan `.xls`)
2. Pastikan file tidak sedang dibuka di Excel
3. Periksa apakah nama kolom sesuai dengan format yang diharapkan

---

## Kontak Bantuan

Jika mengalami kendala yang tidak dapat diatasi, hubungi:
- **Tim IT**: [Sesuaikan dengan kontak yang tersedia]
- **Email**: [Sesuaikan dengan email yang tersedia]

---

*Dokumen ini dibuat untuk membantu pengguna non-teknis dalam mengoperasikan Sistem Informasi Perizinan DPMPTSP.*
