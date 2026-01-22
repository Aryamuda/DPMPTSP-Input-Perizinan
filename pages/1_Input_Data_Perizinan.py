import streamlit as st
from database import insert_perizinan, search_field_suggestions
from datetime import datetime

# Konfigurasi page
st.set_page_config(
    page_title="Input Data Perizinan",
    page_icon="",
    layout="wide"
)

# Load daftar sektor dari file
def load_sektor():
    with open('a.txt', 'r', encoding='utf-8') as f:
        sektor_list = [line.strip() for line in f.readlines() if line.strip()]
    return sektor_list

# Fungsi untuk create text input dengan autocomplete
def text_input_with_autocomplete(label, field_name, key, is_textarea=False, height=100):
    """Text input dengan inline autocomplete suggestions"""
    
    # Check if there's a pending value to set
    pending_key = f'{key}_pending'
    if pending_key in st.session_state:
        # Set the value before widget creation
        st.session_state[key] = st.session_state[pending_key]
        del st.session_state[pending_key]
    
    # Display input field
    if is_textarea:
        current_value = st.text_area(label, key=key, height=height)
    else:
        current_value = st.text_input(label, key=key)
    
    # Show suggestions if user typed >= 2 characters
    if len(current_value) >= 2:
        suggestions = search_field_suggestions(field_name, current_value, limit=3)
        
        if suggestions:
            # Display suggestions right below the input
            cols = st.columns(len(suggestions))
            for idx, suggestion in enumerate(suggestions):
                with cols[idx]:
                    # Truncate long text for button display
                    display_text = suggestion if len(suggestion) <= 35 else suggestion[:32] + "..."
                    if st.button(f"✓ {display_text}", key=f'{key}_sugg_{idx}', width="stretch", type="secondary"):
                        # Store suggestion in pending state
                        st.session_state[pending_key] = suggestion
                        st.rerun()
    
    return current_value

# Inisialisasi session state
if 'sektor_confirmed' not in st.session_state:
    st.session_state.sektor_confirmed = False
if 'selected_sektor' not in st.session_state:
    st.session_state.selected_sektor = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Header
st.title("Input Data Perizinan")
st.markdown("---")

# Load daftar sektor
sektor_list = load_sektor()

# Section 1: Pemilihan Sektor
st.header("Langkah 1: Pilih Sektor")

if not st.session_state.sektor_confirmed:
    selected_sektor = st.selectbox(
        "Pilih Sektor/Dinas",
        options=sektor_list,
        help="Pilih sektor yang sesuai dengan permohonan perizinan"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Konfirmasi Sektor", type="primary"):
            st.session_state.selected_sektor = selected_sektor
            st.session_state.sektor_confirmed = True
            st.rerun()
    
    st.info("Silakan pilih sektor dan klik tombol Konfirmasi Sektor untuk melanjutkan ke form input data.")
    
else:
    # Tampilkan sektor yang dipilih
    st.success(f"Sektor terpilih: **{st.session_state.selected_sektor}**")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Ubah Sektor"):
            st.session_state.sektor_confirmed = False
            st.session_state.selected_sektor = None
            st.rerun()
    
    st.markdown("---")
    
    # Section 2: Form Input Data
    st.header("Langkah 2: Input Data Perizinan")
    
    # Input fields dengan autocomplete
    nama_pengguna = text_input_with_autocomplete("Nama Pengguna Layanan", "nama_pengguna_layanan", "nama_pengguna")
    nib = text_input_with_autocomplete("NIB", "nib", "nib")
    alamat = text_input_with_autocomplete("Alamat", "alamat", "alamat", is_textarea=True, height=100)
    pemilik_pengurus = text_input_with_autocomplete("Pemilik/Pengurus", "pemilik_pengurus", "pemilik")
    lokasi_usaha = text_input_with_autocomplete("Lokasi Usaha", "lokasi_usaha", "lokasi")
    luas_lahan = text_input_with_autocomplete("Luas Lahan Usaha", "luas_lahan_usaha", "luas")
    kbli = text_input_with_autocomplete("KBLI", "kbli", "kbli")
    jenis_usaha = text_input_with_autocomplete("Jenis Usaha", "jenis_usaha", "jenis")
    
    resiko = st.selectbox("Resiko", ["", "MENENGAH TINGGI", "TINGGI", "UMKU"], key="resiko")
    
    kapasitas = text_input_with_autocomplete("Kapasitas", "kapasitas", "kapasitas")
    jenis_permohonan = st.selectbox("Jenis Permohonan", ["", "Baru", "Perpanjangan"], key="jenis_perm")
    nomor_permohonan = text_input_with_autocomplete("Nomor Permohonan", "nomor_permohonan", "nomor_perm")
    tanggal_permohonan = st.date_input("Tanggal Permohonan", value=None, key="tgl_perm")
    nomor_tanggal_permohonan_rekomendasi = text_input_with_autocomplete("No. & Tgl Permohonan Rekomendasi", "nomor_tanggal_permohonan_rekomendasi", "nomor_tgl_perm_rek")
    nomor_tanggal_rekomendasi = text_input_with_autocomplete("No. & Tgl Rekomendasi", "nomor_tanggal_rekomendasi", "nomor_tgl_rek")
    nomor_izin = text_input_with_autocomplete("Nomor Izin", "nomor_izin", "nomor_izin")
    tanggal_izin = st.date_input("Tanggal Izin", value=None, key="tgl_izin")
    tanggal_berlaku_hingga = st.date_input("Berlaku Hingga", value=None, key="tgl_berlaku_hingga")
    npwp = text_input_with_autocomplete("NPWP", "npwp", "npwp")
    telepon = text_input_with_autocomplete("Telepon", "telepon", "telepon")
    email = text_input_with_autocomplete("Email", "email", "email")
    keterangan = text_input_with_autocomplete("Keterangan", "keterangan", "keterangan")
    
    st.markdown("---")
    
    # Kategori Perizinan
    kategori_perizinan = st.radio(
        "Pilih Kategori Perizinan *",
        options=["Perizinan", "Perizinan Berusaha", "Non-Perizinan"],
        index=None,
        key="kategori"
    )
    
    # Jenis Dokumen - conditional based on kategori
    jenis_dokumen_options = {
        'Perizinan': ['', 'Izin', 'Persetujuan'],
        'Perizinan Berusaha': ['', 'UMKU', 'Sertifikat Standar', 'Izin'],
        'Non-Perizinan': ['', 'Surat Keterangan', 'Laporan', 'Rekomendasi']
    }
    
    if kategori_perizinan:
        jenis_dokumen = st.selectbox(
            "Jenis Dokumen",
            options=jenis_dokumen_options.get(kategori_perizinan, ['']),
            key="jenis_dok"
        )
    else:
        jenis_dokumen = ''
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        submit_button = st.button("Simpan Data", type="primary", width="stretch")
    
    if submit_button:
        # Validasi minimal
        if not kategori_perizinan:
            st.error("Kategori Perizinan harus dipilih.")
        elif not nama_pengguna:
            st.error("Nama Pengguna Layanan harus diisi.")
        else:
            # Siapkan data untuk disimpan
            data = {
                'sektor': st.session_state.selected_sektor,
                'kategori_perizinan': kategori_perizinan,
                'nama_pengguna_layanan': nama_pengguna,
                'nib': nib,
                'alamat': alamat,
                'pemilik_pengurus': pemilik_pengurus,
                'lokasi_usaha': lokasi_usaha,
                'luas_lahan_usaha': luas_lahan,
                'kbli': kbli,
                'jenis_usaha': jenis_usaha,
                'resiko': resiko,
                'kapasitas': kapasitas,
                'jenis_permohonan': jenis_permohonan,
                'nomor_permohonan': nomor_permohonan,
                'tanggal_permohonan': str(tanggal_permohonan) if tanggal_permohonan else '',
                'nomor_tanggal_permohonan_rekomendasi': nomor_tanggal_permohonan_rekomendasi,
                'nomor_tanggal_rekomendasi': nomor_tanggal_rekomendasi,
                'nomor_izin': nomor_izin,
                'tanggal_izin': str(tanggal_izin) if tanggal_izin else '',
                'masa_berlaku': str(tanggal_berlaku_hingga) if tanggal_berlaku_hingga else '',
                'npwp': npwp,
                'telepon': telepon,
                'email': email,
                'keterangan': keterangan,
                'jenis_dokumen': jenis_dokumen
            }
            
            try:
                insert_perizinan(data)
                st.success("Data perizinan berhasil disimpan.")
                
                # Clear all fields
                for key in list(st.session_state.keys()):
                    if key not in ['sektor_confirmed', 'selected_sektor']:
                        del st.session_state[key]
                
                st.rerun()
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menyimpan data: {str(e)}")
