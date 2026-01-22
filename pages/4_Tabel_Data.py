import streamlit as st
import pandas as pd
from database import get_all_perizinan, update_perizinan

st.set_page_config(
    page_title="Tabel Data Perizinan",
    layout="wide"
)

def load_sektor():
    with open('a.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_jenis_dokumen_options(kategori):
    """Get jenis dokumen options based on kategori perizinan"""
    options = {
        'Perizinan': ['', 'Izin', 'Persetujuan'],
        'Perizinan Berusaha': ['', 'UMKU', 'Sertifikat Standar', 'Izin'],
        'Non-Perizinan': ['', 'Surat Keterangan', 'Laporan', 'Rekomendasi']
    }
    return options.get(kategori, [''])

def format_date(date_str):
    """Convert YYYY-MM-DD to DD/MM/YY"""
    if pd.isna(date_str) or not date_str:
        return ''
    try:
        from datetime import datetime
        dt = datetime.strptime(str(date_str).split(' ')[0], '%Y-%m-%d')
        return dt.strftime('%d/%m/%y')
    except:
        return str(date_str)

st.title("Tabel Data Perizinan")
st.markdown("---")

# Load data
data = get_all_perizinan()

if data:
    columns = [
        'ID', 'Sektor', 'Kategori', 'Nama Pengguna', 'NIB', 'Alamat',
        'Pemilik/Pengurus', 'Lokasi Usaha', 'Luas Lahan', 'KBLI', 'Jenis Usaha',
        'Resiko', 'Kapasitas', 'Jenis Permohonan', 'No. Permohonan', 'Tgl Permohonan',
        'No. & Tgl Perm. Rekom', 'No. & Tgl Rekomendasi',
        'No. Izin', 'Tgl Izin', 'Masa Berlaku', 'NPWP',
        'Telepon', 'Email', 'Keterangan', 'Jenis Dokumen', 'Created At', 'Updated At'
    ]
    
    # Database field names (for update)
    db_columns = [
        'id', 'sektor', 'kategori_perizinan', 'nama_pengguna_layanan', 'nib', 'alamat',
        'pemilik_pengurus', 'lokasi_usaha', 'luas_lahan_usaha', 'kbli', 'jenis_usaha',
        'resiko', 'kapasitas', 'jenis_permohonan', 'nomor_permohonan', 'tanggal_permohonan',
        'nomor_tanggal_permohonan_rekomendasi', 'nomor_tanggal_rekomendasi',
        'nomor_izin', 'tanggal_izin', 'masa_berlaku', 'npwp',
        'telepon', 'email', 'keterangan', 'jenis_dokumen', 'created_at', 'updated_at'
    ]
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # NOTE: Do NOT format dates here - keep YYYY-MM-DD for database compatibility
    # Dates will display as YYYY-MM-DD in the editor
    
    # Filter Section
    st.subheader("Filter Data")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sektor_list = ['Semua'] + load_sektor()
        selected_sektor = st.selectbox("Sektor", options=sektor_list)
    
    with col2:
        kategori_list = ['Semua', 'Perizinan', 'Perizinan Berusaha', 'Non-Perizinan']
        selected_kategori = st.selectbox("Kategori Perizinan", options=kategori_list)
    
    with col3:
        search_nama = st.text_input("Cari Nama")
    
    with col4:
        search_nib = st.text_input("Cari NIB")
    
    # Apply filters
    df_filtered = df.copy()
    
    if selected_sektor != 'Semua':
        df_filtered = df_filtered[df_filtered['Sektor'] == selected_sektor]
    
    if selected_kategori != 'Semua':
        df_filtered = df_filtered[df_filtered['Kategori'] == selected_kategori]
    
    if search_nama:
        df_filtered = df_filtered[df_filtered['Nama Pengguna'].str.contains(search_nama, case=False, na=False)]
    
    if search_nib:
        df_filtered = df_filtered[df_filtered['NIB'].str.contains(search_nib, case=False, na=False)]
    
    st.markdown("---")
    
    # Editable Data Table
    st.subheader("Data Perizinan")
    st.info("Klik cell untuk edit. Setelah selesai, klik 'Simpan Perubahan'.")
    
    # Columns that should not be editable
    disabled_cols = ['ID', 'Created At', 'Updated At']
    
    # Use data_editor for editable table
    # Note: Jenis Dokumen options depend on Kategori Perizinan
    # All options combined since per-row conditional isn't supported
    all_jenis_dokumen = ['', 'Izin', 'Persetujuan', 'UMKU', 'Sertifikat Standar', 'Surat Keterangan', 'Laporan', 'Rekomendasi']
    
    edited_df = st.data_editor(
        df_filtered,
        width='stretch',
        hide_index=True,
        disabled=disabled_cols,
        num_rows="fixed",
        column_config={
            "ID": st.column_config.NumberColumn("ID", disabled=True),
            "Sektor": st.column_config.SelectboxColumn("Sektor", options=load_sektor()),
            "Kategori": st.column_config.SelectboxColumn("Kategori", options=['Perizinan', 'Perizinan Berusaha', 'Non-Perizinan']),
            "Resiko": st.column_config.SelectboxColumn("Resiko", options=['', 'MENENGAH TINGGI', 'TINGGI', 'UMKU']),
            "Jenis Permohonan": st.column_config.SelectboxColumn("Jenis Permohonan", options=['', 'Baru', 'Perpanjangan']),
            "Jenis Dokumen": st.column_config.SelectboxColumn("Jenis Dokumen", options=all_jenis_dokumen),
            "Created At": st.column_config.TextColumn("Created At", disabled=True),
            "Updated At": st.column_config.TextColumn("Updated At", disabled=True),
        },
        key="data_editor"
    )
    
    st.caption(f"Total Data: {len(df_filtered)} baris")
    
    # Save Changes Button
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Simpan Perubahan", type="primary", width='stretch'):
            # Compare original and edited dataframes
            changes_made = 0
            errors = []
            
            for idx, edited_row in edited_df.iterrows():
                original_row = df_filtered.loc[idx]
                
                # Check if row was modified
                if not edited_row.equals(original_row):
                    try:
                        # Build data dict for update
                        row_id = int(edited_row['ID'])
                        update_data = {}
                        
                        for col_name, db_name in zip(columns, db_columns):
                            if db_name in ['id', 'created_at', 'updated_at']:
                                continue
                            value = edited_row[col_name]
                            # Convert to string, handle NaN
                            if pd.isna(value):
                                update_data[db_name] = ''
                            else:
                                update_data[db_name] = str(value)
                        
                        update_perizinan(row_id, update_data)
                        changes_made += 1
                    except Exception as e:
                        errors.append(f"ID {row_id}: {str(e)}")
            
            if changes_made > 0:
                st.success(f"Berhasil menyimpan {changes_made} perubahan!")
                st.rerun()
            elif errors:
                for err in errors:
                    st.error(err)
            else:
                st.info("Tidak ada perubahan yang terdeteksi.")

else:
    st.info("Belum ada data perizinan.")
