import streamlit as st
from database import get_all_perizinan
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi page
st.set_page_config(
    page_title="Monitoring Masa Berlaku Izin",
    layout="wide"
)

def hitung_sisa_hari(expired_date):
    """Hitung sisa hari hingga expired"""
    if not expired_date:
        return None
    today = datetime.now()
    delta = expired_date - today
    return delta.days

def format_date(date_str):
    """Convert YYYY-MM-DD to DD/MM/YY"""
    if not date_str:
        return '-'
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%y')
    except:
        return date_str

# Header
st.title("Monitoring Masa Berlaku Izin")
st.markdown("---")

# Load semua data
data = get_all_perizinan()

if data:
    # Convert to list of dicts
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
        # Parse masa berlaku langsung sebagai tanggal
        try:
            expired_date = datetime.strptime(data_dict['masa_berlaku'], '%Y-%m-%d') if data_dict['masa_berlaku'] else None
        except:
            expired_date = None
        
        sisa_hari = hitung_sisa_hari(expired_date)
        
        data_dict['tanggal_expired'] = expired_date
        data_dict['sisa_hari'] = sisa_hari
        data_list.append(data_dict)
    
    # Kategorisasi
    kritis = [d for d in data_list if d['sisa_hari'] is not None and 0 <= d['sisa_hari'] <= 30]
    perhatian = [d for d in data_list if d['sisa_hari'] is not None and 31 <= d['sisa_hari'] <= 90]
    expired = [d for d in data_list if d['sisa_hari'] is not None and d['sisa_hari'] < 0]
    aman = [d for d in data_list if d['sisa_hari'] is not None and d['sisa_hari'] > 90]
    
    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 KRITIS", len(kritis), "≤ 30 Hari", delta_color="inverse")
    
    with col2:
        st.metric("🟡 PERHATIAN", len(perhatian), "31-90 Hari", delta_color="off")
    
    with col3:
        st.metric("⚫ EXPIRED", len(expired), "Sudah Habis", delta_color="inverse")
    
    with col4:
        st.metric("🟢 AMAN", len(aman), "> 90 Hari", delta_color="normal")
    
    st.markdown("---")
    
    # Sorting Options
    st.header("Urutkan Data")
    sort_option = st.radio(
        "Pilih Urutan",
        ["Terdekat Expired (Ascending)", "Terbaru Expired (Descending)"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Sort data
    valid_data = [d for d in data_list if d['sisa_hari'] is not None]
    if sort_option == "Terdekat Expired (Ascending)":
        valid_data.sort(key=lambda x: x['sisa_hari'])
    else:
        valid_data.sort(key=lambda x: x['sisa_hari'], reverse=True)
    
    # Tabs untuk kategori
    tab1, tab2, tab3, tab4 = st.tabs(["🔴 KRITIS", "🟡 PERHATIAN", "⚫ EXPIRED", "🟢 SEMUA DATA"])
    
    with tab1:
        st.subheader(f"Izin Kritis - Expired ≤ 30 Hari ({len(kritis)} Data)")
        if kritis:
            kritis_sorted = sorted(kritis, key=lambda x: x['sisa_hari'])
            for idx, item in enumerate(kritis_sorted, 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                        st.caption(f"Nomor Izin: {item['nomor_izin']}")
                    with col2:
                        st.write(f"Tanggal Izin: {format_date(item['tanggal_izin'])}")
                        st.write(f"Masa Berlaku: {format_date(item['masa_berlaku'])}")
                    with col3:
                        st.error(f"**{item['sisa_hari']} hari lagi**")
                    st.markdown("---")
        else:
            st.info("Tidak ada izin dalam kategori kritis.")
    
    with tab2:
        st.subheader(f"Izin Perhatian - Expired 31-90 Hari ({len(perhatian)} Data)")
        if perhatian:
            perhatian_sorted = sorted(perhatian, key=lambda x: x['sisa_hari'])
            for idx, item in enumerate(perhatian_sorted, 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                        st.caption(f"Nomor Izin: {item['nomor_izin']}")
                    with col2:
                        st.write(f"Tanggal Izin: {format_date(item['tanggal_izin'])}")
                        st.write(f"Masa Berlaku: {format_date(item['masa_berlaku'])}")
                    with col3:
                        st.warning(f"**{item['sisa_hari']} hari lagi**")
                    st.markdown("---")
        else:
            st.info("Tidak ada izin dalam kategori perhatian.")
    
    with tab3:
        st.subheader(f"Izin Expired ({len(expired)} Data)")
        if expired:
            expired_sorted = sorted(expired, key=lambda x: x['sisa_hari'], reverse=True)
            for idx, item in enumerate(expired_sorted, 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                        st.caption(f"Nomor Izin: {item['nomor_izin']}")
                    with col2:
                        st.write(f"Tanggal Izin: {format_date(item['tanggal_izin'])}")
                        st.write(f"Masa Berlaku: {format_date(item['masa_berlaku'])}")
                    with col3:
                        st.error(f"**Expired {abs(item['sisa_hari'])} hari lalu**")
                    st.markdown("---")
        else:
            st.success("Tidak ada izin yang expired.")
    
    with tab4:
        st.subheader(f"Semua Data Izin ({len(valid_data)} Data)")
        for idx, item in enumerate(valid_data, 1):
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{idx}. {item['nama_pengguna_layanan']}**")
                    st.caption(f"Nomor Izin: {item['nomor_izin']}")
                with col2:
                    st.write(f"Tanggal Izin: {format_date(item['tanggal_izin'])}")
                    st.write(f"Masa Berlaku: {format_date(item['masa_berlaku'])}")
                with col3:
                    if item['sisa_hari'] < 0:
                        st.error(f"**Expired {abs(item['sisa_hari'])} hari lalu**")
                    elif item['sisa_hari'] <= 30:
                        st.error(f"**{item['sisa_hari']} hari lagi**")
                    elif item['sisa_hari'] <= 90:
                        st.warning(f"**{item['sisa_hari']} hari lagi**")
                    else:
                        st.success(f"**{item['sisa_hari']} hari lagi**")
                st.markdown("---")

else:
    st.info("Belum ada data perizinan.")
