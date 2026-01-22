import streamlit as st
from database import init_database

# Inisialisasi database (idempotent, safe to call)
init_database()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Sistem Informasi Perizinan</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu Provinsi Lampung</div>', unsafe_allow_html=True)

st.markdown("---")

# Konten utama
st.header("Selamat Datang")

st.write("""
Sistem Informasi Perizinan ini dirancang untuk mengelola dan memproses data perizinan 
dari berbagai sektor di Provinsi Lampung. Sistem ini mencakup:
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fitur Utama")
    st.write("""
    - Input dan pengelolaan data perizinan
    - Manajemen data per sektor
    - Penyimpanan data terstruktur
    - Pencarian dan filter data
    """)

with col2:
    st.subheader("Sektor yang Dilayani")
    st.write("""
    - Dinas Perhubungan
    - Dinas Perkebunan
    - Dinas Peternakan dan Kesehatan Hewan
    - Dinas Energi dan Sumber Daya Mineral
    - Dan 15 sektor lainnya
    """)

st.markdown("---")

st.info("Silakan pilih menu di sidebar.")
