import streamlit as st
from database import get_all_perizinan
import pandas as pd
from datetime import datetime

# Konfigurasi page
st.set_page_config(
    page_title="Monitoring SLA Perizinan",
    layout="wide"
)

def format_date(date_str):
    """Convert YYYY-MM-DD to DD/MM/YY"""
    if not date_str:
        return '-'
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%y')
    except:
        return date_str

def hitung_sla(tanggal_permohonan, tanggal_izin):
    """Hitung SLA dalam hari"""
    if not tanggal_permohonan or not tanggal_izin:
        return None
    try:
        dt_permohonan = datetime.strptime(tanggal_permohonan, '%Y-%m-%d')
        dt_izin = datetime.strptime(tanggal_izin, '%Y-%m-%d')
        delta = dt_izin - dt_permohonan
        return delta.days
    except:
        return None

def load_sektor():
    with open('a.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Header
st.title("Monitoring SLA Perizinan")
st.markdown("---")

# Load semua data
data = get_all_perizinan()

if data:
    columns = [
        'id', 'sektor', 'kategori_perizinan', 'nama_pengguna_layanan', 'nib', 'alamat',
        'pemilik_pengurus', 'lokasi_usaha', 'luas_lahan_usaha', 'kbli', 'jenis_usaha',
        'resiko', 'kapasitas', 'jenis_permohonan', 'nomor_permohonan', 'tanggal_permohonan',
        'nomor_tanggal_permohonan_rekomendasi', 'nomor_tanggal_rekomendasi',
        'nomor_izin', 'tanggal_izin', 'masa_berlaku', 'npwp',
        'telepon', 'email', 'keterangan', 'created_at', 'updated_at', 'jenis_dokumen'
    ]
    
    data_list = []
    for row in data:
        data_dict = dict(zip(columns, row))
        sla = hitung_sla(data_dict['tanggal_permohonan'], data_dict['tanggal_izin'])
        data_dict['sla_hari'] = sla
        data_list.append(data_dict)
    
    # Filter Section
    st.subheader("Filter Data")
    col1, col2 = st.columns(2)
    
    with col1:
        sektor_list = ['Semua'] + load_sektor()
        selected_sektor = st.selectbox("Sektor", options=sektor_list)
    
    with col2:
        kategori_list = ['Semua', 'Perizinan', 'Perizinan Berusaha', 'Non-Perizinan']
        selected_kategori = st.selectbox("Kategori Perizinan", options=kategori_list)
    
    # Apply filters
    filtered_data = data_list.copy()
    
    if selected_sektor != 'Semua':
        filtered_data = [d for d in filtered_data if d['sektor'] == selected_sektor]
    
    if selected_kategori != 'Semua':
        filtered_data = [d for d in filtered_data if d['kategori_perizinan'] == selected_kategori]
    
    st.markdown("---")
    
    # Simple Data Display
    st.subheader(f"Data Perizinan ({len(filtered_data)} Data)")
    
    if filtered_data:
        for idx, item in enumerate(filtered_data, 1):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                    st.caption(f"Nomor Izin: {item['nomor_izin'] or '-'}")
                with col2:
                    st.write(f"Permohonan: {format_date(item['tanggal_permohonan'])}")
                    st.write(f"Izin Terbit: {format_date(item['tanggal_izin'])}")
                with col3:
                    if item['sla_hari'] is not None:
                        st.info(f"**{item['sla_hari']} hari**")
                    else:
                        st.warning("⏳ Proses")
                st.markdown("---")
    else:
        st.info("Tidak ada data yang sesuai filter.")

else:
    st.info("Belum ada data perizinan.")
