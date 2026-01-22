import streamlit as st
from database import init_database

# Inisialisasi database
init_database()

# Konfigurasi page global
st.set_page_config(
    page_title="Sistem Perizinan DPMPTSP",
    layout="wide"
)

# Definisi Halaman (Navigation)
# Anda bisa mengubah "title" di sini untuk mengubah nama di Sidebar!
pages = [
    st.Page("pages/Home.py", title="Beranda"),
    st.Page("pages/1_Input_Data_Perizinan.py", title="Input Pendaftaran"),
    st.Page("pages/2_Data_Perizinan.py", title="Masa Berlaku"),
    st.Page("pages/6_SLA_Monitoring.py", title="SLA Monitoring"),
    st.Page("pages/4_Tabel_Data.py", title="Tabel Data"),
    st.Page("pages/5_Import_Data.py", title="Import Data"),
    st.Page("pages/3_Analytics.py", title="Dashboard"),
]

# Setup Navigation
pg = st.navigation(pages)

# Jalankan Halaman
pg.run()

