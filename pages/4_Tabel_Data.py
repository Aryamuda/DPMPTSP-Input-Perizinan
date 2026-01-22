import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from database import get_all_perizinan, update_perizinan

st.set_page_config(
    page_title="Tabel Data Perizinan",
    layout="wide"
)

# Indonesian month names
BULAN_INDONESIA = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}

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
        dt = datetime.strptime(str(date_str).split(' ')[0], '%Y-%m-%d')
        return dt.strftime('%d/%m/%y')
    except:
        return str(date_str)

def format_date_full(date_str):
    """Convert YYYY-MM-DD to DD/MM/YYYY"""
    if pd.isna(date_str) or not date_str or str(date_str).strip() == '':
        return '-'
    try:
        dt = datetime.strptime(str(date_str).split(' ')[0], '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return str(date_str) if date_str else '-'

def format_date_indonesian(date_str):
    """Convert YYYY-MM-DD to 'DD Bulan YYYY' format"""
    if pd.isna(date_str) or not date_str or str(date_str).strip() == '':
        return ''
    try:
        dt = datetime.strptime(str(date_str).split(' ')[0], '%Y-%m-%d')
        return f"{dt.day} {BULAN_INDONESIA[dt.month]} {dt.year}"
    except:
        return str(date_str) if date_str else ''

def create_export_dataframe(df_source):
    """Transform database dataframe to export format"""
    export_data = []
    
    for idx, row in df_source.iterrows():
        # Combine nomor_permohonan + tanggal_permohonan
        nomor_perm = str(row['No. Permohonan']) if pd.notna(row['No. Permohonan']) and row['No. Permohonan'] else ''
        tgl_perm = row['Tgl Permohonan']
        tgl_perm_indo = format_date_indonesian(tgl_perm)
        
        if nomor_perm and tgl_perm_indo:
            nomor_tgl_permohonan = f"{nomor_perm} ({tgl_perm_indo})"
        elif nomor_perm:
            nomor_tgl_permohonan = nomor_perm
        else:
            nomor_tgl_permohonan = '-'
        
        export_row = {
            'ID': row['ID'],
            'Sektor': row['Sektor'] if pd.notna(row['Sektor']) else '-',
            'Jenis Perizinan': row['Kategori'] if pd.notna(row['Kategori']) else '-',
            'Nama Pengguna Layanan': row['Nama Pengguna'] if pd.notna(row['Nama Pengguna']) else '-',
            'NIB': row['NIB'] if pd.notna(row['NIB']) else '-',
            'Alamat': row['Alamat'] if pd.notna(row['Alamat']) else '-',
            'Pemilik/Pengurus': row['Pemilik/Pengurus'] if pd.notna(row['Pemilik/Pengurus']) else '-',
            'Gender': '-',  # Not in database
            'Lokasi Usaha': row['Lokasi Usaha'] if pd.notna(row['Lokasi Usaha']) else '-',
            'Luas Lahan': row['Luas Lahan'] if pd.notna(row['Luas Lahan']) else '-',
            'KBLI': row['KBLI'] if pd.notna(row['KBLI']) else '-',
            'Jenis Usaha': row['Jenis Usaha'] if pd.notna(row['Jenis Usaha']) else '-',
            'Risiko': row['Resiko'] if pd.notna(row['Resiko']) else '-',
            'Rencana Nilai Investasi': '-',  # Not in database
            'Kapasitas': row['Kapasitas'] if pd.notna(row['Kapasitas']) else '-',
            'Jenis Permohonan': row['Jenis Permohonan'] if pd.notna(row['Jenis Permohonan']) else '-',
            'Nomor & Tanggal Permohonan': nomor_tgl_permohonan,
            'Nomor & Tanggal Permohonan Rekom': row['No. & Tgl Perm. Rekom'] if pd.notna(row['No. & Tgl Perm. Rekom']) else '-',
            'Nomor & Tanggal Rekomendasi': row['No. & Tgl Rekomendasi'] if pd.notna(row['No. & Tgl Rekomendasi']) else '-',
            'Nomor Izin': row['No. Izin'] if pd.notna(row['No. Izin']) else '-',
            'Tanggal Izin': format_date_full(row['Tgl Izin']),
            'Masa Berlaku': format_date_full(row['Masa Berlaku']),
            'NPWP': row['NPWP'] if pd.notna(row['NPWP']) else '-',
            'Telepon': row['Telepon'] if pd.notna(row['Telepon']) else '-',
            'Email': row['Email'] if pd.notna(row['Email']) else '-',
            'Jenis Dokumen': row['Jenis Dokumen'] if pd.notna(row['Jenis Dokumen']) else '-',
            'Keterangan': row['Keterangan'] if pd.notna(row['Keterangan']) else '-',
        }
        export_data.append(export_row)
    
    return pd.DataFrame(export_data)

def generate_excel_export(df_export):
    """Generate Excel file with headers above column names"""
    output = BytesIO()
    
    current_year = datetime.now().year
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write data starting from row 5 (0-indexed: row 4)
        # This leaves rows 0-3 for title headers
        df_export.to_excel(writer, index=False, sheet_name='Data Perizinan', startrow=4)
        
        # Get the worksheet
        worksheet = writer.sheets['Data Perizinan']
        
        # Write title headers in rows 1-3
        worksheet.cell(row=1, column=1, value='DATA PENGGUNA LAYANAN PERIZINAN, PERIZINAN BERUSAHA, DAN NONPERIZINAN')
        worksheet.cell(row=2, column=1, value='YANG DITERBITKAN DINAS PENANAMAN MODAL DAN PELAYANAN TERPADU SATU PINTU PROVINSI LAMPUNG')
        worksheet.cell(row=3, column=1, value=f'TAHUN {current_year}')
        # Row 4 is empty (intentional gap)
        # Row 5 is column headers (written by to_excel)
        # Row 6+ is data
    
    return output.getvalue()

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
    st.info("Centang baris untuk menghapus. Klik cell untuk edit.")
    
    # Add checkbox column for selection
    df_with_select = df_filtered.copy()
    df_with_select.insert(0, 'Pilih', False)
    
    # Columns that should not be editable
    disabled_cols = ['ID', 'Created At', 'Updated At']
    
    # Use data_editor for editable table
    # Note: Jenis Dokumen options depend on Kategori Perizinan
    # All options combined since per-row conditional isn't supported
    all_jenis_dokumen = ['', 'Izin', 'Persetujuan', 'UMKU', 'Sertifikat Standar', 'Surat Keterangan', 'Laporan', 'Rekomendasi']
    
    edited_df = st.data_editor(
        df_with_select,
        use_container_width=True,
        hide_index=True,
        disabled=disabled_cols,
        num_rows="fixed",
        column_config={
            "Pilih": st.column_config.CheckboxColumn("Pilih", default=False),
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
    
    # Count selected rows
    selected_rows = edited_df[edited_df['Pilih'] == True]
    selected_count = len(selected_rows)
    
    st.caption(f"Total Data: {len(df_filtered)} baris | Terpilih: {selected_count} baris")
    
    # Action Buttons Row 1: Save and Delete
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col2:
        if st.button("Simpan Perubahan", type="primary", use_container_width=True):
            # Compare original and edited dataframes (excluding 'Pilih' column)
            changes_made = 0
            errors = []
            
            for idx, edited_row in edited_df.iterrows():
                original_row = df_with_select.loc[idx]
                
                # Check if row was modified (excluding Pilih column)
                edited_data = edited_row.drop('Pilih')
                original_data = original_row.drop('Pilih')
                
                if not edited_data.equals(original_data):
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
    
    with col3:
        # Delete button - only show if rows are selected
        if selected_count > 0:
            if st.button(f"Hapus {selected_count} Data", type="secondary", use_container_width=True):
                st.session_state.confirm_delete = True
                st.session_state.delete_ids = selected_rows['ID'].tolist()
    
    # Confirmation dialog for delete
    if st.session_state.get('confirm_delete', False):
        st.warning(f"⚠️ Yakin ingin menghapus {len(st.session_state.delete_ids)} data? Tindakan ini tidak dapat dibatalkan!")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Ya, Hapus", type="primary", use_container_width=True):
                from database import delete_perizinan
                deleted = 0
                for row_id in st.session_state.delete_ids:
                    try:
                        delete_perizinan(int(row_id))
                        deleted += 1
                    except Exception as e:
                        st.error(f"Gagal menghapus ID {row_id}: {e}")
                
                st.session_state.confirm_delete = False
                st.session_state.delete_ids = []
                st.success(f"Berhasil menghapus {deleted} data!")
                st.rerun()
        with col_no:
            if st.button("Batal", use_container_width=True):
                st.session_state.confirm_delete = False
                st.session_state.delete_ids = []
                st.rerun()
    
    st.markdown("---")
    
    # Action Buttons Row 2: Export
    st.subheader("Export Data")
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if len(df_filtered) > 0:
            export_df = create_export_dataframe(df_filtered)
            excel_data = generate_excel_export(export_df)
            
            st.download_button(
                label="Export ke Excel",
                data=excel_data,
                file_name=f"export_perizinan_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    st.info("Belum ada data perizinan.")

