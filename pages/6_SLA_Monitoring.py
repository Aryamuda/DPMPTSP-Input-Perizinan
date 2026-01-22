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
    
    # Calculate stats for filtered data
    valid_sla = [d['sla_hari'] for d in filtered_data if d['sla_hari'] is not None]
    
    st.markdown("---")
    
    # Kategorisasi SLA
    cepat = [d for d in filtered_data if d['sla_hari'] is not None and d['sla_hari'] <= 7]
    normal = [d for d in filtered_data if d['sla_hari'] is not None and 8 <= d['sla_hari'] <= 14]
    lambat = [d for d in filtered_data if d['sla_hari'] is not None and 15 <= d['sla_hari'] <= 30]
    sangat_lambat = [d for d in filtered_data if d['sla_hari'] is not None and d['sla_hari'] > 30]
    belum_selesai = [d for d in filtered_data if d['sla_hari'] is None]
    
    # Dashboard Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_sla = round(sum(valid_sla) / len(valid_sla), 1) if valid_sla else 0
        st.metric("Rata-rata SLA", f"{avg_sla} Hari")
    
    with col2:
        st.metric("🟢 CEPAT", len(cepat), "≤ 7 Hari")
    
    with col3:
        st.metric("🟡 NORMAL", len(normal), "8-14 Hari")
    
    with col4:
        st.metric("🟠 LAMBAT", len(lambat), "15-30 Hari")
    
    with col5:
        st.metric("🔴 SANGAT LAMBAT", len(sangat_lambat), "> 30 Hari")
    
    st.markdown("---")
    
    # Sorting Options
    st.subheader("Urutkan Data")
    sort_option = st.radio(
        "Pilih Urutan",
        ["Tercepat (Ascending)", "Terlambat (Descending)"],
        horizontal=True
    )
    
    # Sort data
    valid_data = [d for d in filtered_data if d['sla_hari'] is not None]
    if sort_option == "Tercepat (Ascending)":
        valid_data.sort(key=lambda x: x['sla_hari'])
    else:
        valid_data.sort(key=lambda x: x['sla_hari'], reverse=True)
    
    st.markdown("---")
    
    # Tabs untuk kategori
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🟢 CEPAT", "🟡 NORMAL", "🟠 LAMBAT", "🔴 SANGAT LAMBAT", "⏳ BELUM SELESAI", "📊 SEMUA DATA"
    ])
    
    def render_items(items, status_color):
        if items:
            for idx, item in enumerate(items, 1):
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
                            if status_color == 'green':
                                st.success(f"**{item['sla_hari']} hari**")
                            elif status_color == 'yellow':
                                st.warning(f"**{item['sla_hari']} hari**")
                            elif status_color == 'orange':
                                st.warning(f"**{item['sla_hari']} hari**")
                            else:
                                st.error(f"**{item['sla_hari']} hari**")
                        else:
                            st.info("Belum selesai")
                    st.markdown("---")
        else:
            st.info("Tidak ada data dalam kategori ini.")
    
    with tab1:
        st.subheader(f"SLA Cepat - ≤ 7 Hari ({len(cepat)} Data)")
        cepat_sorted = sorted(cepat, key=lambda x: x['sla_hari'])
        render_items(cepat_sorted, 'green')
    
    with tab2:
        st.subheader(f"SLA Normal - 8-14 Hari ({len(normal)} Data)")
        normal_sorted = sorted(normal, key=lambda x: x['sla_hari'])
        render_items(normal_sorted, 'yellow')
    
    with tab3:
        st.subheader(f"SLA Lambat - 15-30 Hari ({len(lambat)} Data)")
        lambat_sorted = sorted(lambat, key=lambda x: x['sla_hari'])
        render_items(lambat_sorted, 'orange')
    
    with tab4:
        st.subheader(f"SLA Sangat Lambat - > 30 Hari ({len(sangat_lambat)} Data)")
        sangat_lambat_sorted = sorted(sangat_lambat, key=lambda x: x['sla_hari'], reverse=True)
        render_items(sangat_lambat_sorted, 'red')
    
    with tab5:
        st.subheader(f"Belum Selesai ({len(belum_selesai)} Data)")
        if belum_selesai:
            for idx, item in enumerate(belum_selesai, 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                        st.caption(f"Nomor Permohonan: {item['nomor_permohonan'] or '-'}")
                    with col2:
                        st.write(f"Permohonan: {format_date(item['tanggal_permohonan'])}")
                        st.write(f"Izin Terbit: -")
                    with col3:
                        st.info("⏳ Proses")
                    st.markdown("---")
        else:
            st.success("Semua perizinan sudah selesai!")
    
    with tab6:
        st.subheader(f"Semua Data ({len(valid_data)} Data)")
        render_items(valid_data, 'auto')

else:
    st.info("Belum ada data perizinan.")
