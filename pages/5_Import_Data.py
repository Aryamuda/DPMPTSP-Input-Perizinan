import streamlit as st
import pandas as pd
import re
from datetime import datetime
from database import insert_perizinan

# Page config is handled by app.py

def load_sektor():
    with open('a.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def clean_nib(value):
    """Strip 'NIB.' prefix from NIB values"""
    if pd.isna(value):
        return ''
    text = str(value).strip()
    # Remove common prefixes
    text = re.sub(r'^NIB\.?\s*', '', text, flags=re.IGNORECASE)
    return text

def parse_nomor_tanggal(value):
    """Parse combined 'Nomor Permohonan : XXX (DD Month YYYY)' format"""
    if pd.isna(value) or not str(value).strip():
        return '', ''
    
    text = str(value).strip()
    nomor = ''
    tanggal = ''
    
    # Extract nomor permohonan
    nomor_match = re.search(r'(?:Nomor\s*Permohonan\s*:\s*)?([A-Z0-9\-]+)', text, re.IGNORECASE)
    if nomor_match:
        nomor = nomor_match.group(1)
    
    # Extract date in parentheses or after the nomor
    date_match = re.search(r'\((\d{1,2}\s+\w+\s+\d{4})\)', text)
    if date_match:
        tanggal = date_match.group(1)
    
    return nomor, tanggal

def parse_indonesian_date(date_str):
    """Convert Indonesian date format to YYYY-MM-DD"""
    if pd.isna(date_str) or not str(date_str).strip():
        return ''
    
    text = str(date_str).strip()
    
    # Month mapping
    months = {
        'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
        'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
    }
    
    # Try to parse "DD Month YYYY" format
    match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', text, re.IGNORECASE)
    if match:
        day = match.group(1).zfill(2)
        month_name = match.group(2).lower()
        year = match.group(3)
        month = months.get(month_name, '01')
        return f"{year}-{month}-{day}"
    
    return text  # Return as-is if can't parse


# Main UI
st.title("Import Data Perizinan (Format PKL)")
st.markdown("---")

# Step 1: Batch Configuration
st.header("1. Konfigurasi Batch")
st.info("Nilai ini akan diterapkan untuk SEMUA data yang di-import.")

col1, col2 = st.columns(2)
with col1:
    sektor_list = load_sektor()
    batch_sektor = st.selectbox("Sektor", options=sektor_list)
with col2:
    batch_kategori = st.selectbox(
        "Kategori Perizinan",
        options=["Perizinan", "Perizinan Berusaha", "Non-Perizinan"]
    )

st.markdown("---")

# Step 2: File Upload
st.header("2. Upload File Excel")
uploaded_file = st.file_uploader("Upload file Excel format PKL", type=['xlsx', 'xls'])

if uploaded_file:
    # Load Excel and select sheet
    xl = pd.ExcelFile(uploaded_file)
    sheet_names = xl.sheet_names
    
    # Try to find PKL sheet
    pkl_sheets = [s for s in sheet_names if 'PKL' in s.upper()]
    default_sheet = pkl_sheets[0] if pkl_sheets else sheet_names[0]
    
    selected_sheet = st.selectbox(
        "Pilih Sheet",
        options=sheet_names,
        index=sheet_names.index(default_sheet) if default_sheet in sheet_names else 0
    )
    
    # Read raw data
    df_raw = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)
    
    st.markdown("---")
    
    # Step 3: Header Detection
    st.header("3. Konfigurasi Header")
    
    col1, col2 = st.columns(2)
    with col1:
        header_row = st.number_input("Baris Header (0-indexed)", min_value=0, max_value=10, value=4)
    with col2:
        data_start_row = st.number_input("Baris Data Pertama", min_value=1, max_value=15, value=5)
    
    # Extract headers and data
    headers = list(df_raw.iloc[header_row])
    df_data = df_raw.iloc[data_start_row:].copy()
    df_data.columns = headers
    df_data = df_data.reset_index(drop=True)
    
    # Filter out empty rows (where NO column is empty or NaN)
    no_col = headers[0]  # First column is typically NO
    df_data = df_data[df_data[no_col].notna() & (df_data[no_col].astype(str).str.strip() != '')]
    
    st.success(f"Ditemukan {len(df_data)} baris data")
    
    # Preview raw data
    with st.expander("Preview Data Mentah", expanded=False):
        st.dataframe(df_data.head(10), width='stretch')
    
    st.markdown("---")
    
    # Step 4: Column Mapping
    st.header("4. Mapping Kolom")
    
    # Define expected PKL columns and their database mappings
    pkl_mapping = {
        'NAMA PENGGUNA LAYANAN': 'nama_pengguna_layanan',
        'NIB': 'nib',
        'ALAMAT PERUSAHAAN': 'alamat',
        'PEMILIK / PENGURUS': 'pemilik_pengurus',
        'LOKASI USAHA': 'lokasi_usaha',
        'LUAS LAHAN USAHA': 'luas_lahan_usaha',
        'KBLI': 'kbli',
        'JENIS USAHA': 'jenis_usaha',
        'RESIKO': 'resiko',
        'KAPASITAS': 'kapasitas',
        'JENIS PERMOHONAN': 'jenis_permohonan',
        'NOMOR DAN TANGGAL PERMOHONAN': 'nomor_tanggal_permohonan',  # Will be split
        'NOMOR DAN TANGGAL PERMOHONAN REKOMENDASI': 'nomor_tanggal_permohonan_rekomendasi',
        'NOMOR DAN TANGGAL REKOMENDASI': 'nomor_tanggal_rekomendasi',
        'NOMOR IZIN': 'nomor_izin',
        'TANGGAL IZIN': 'tanggal_izin',
        'MASA BERLAKU': 'masa_berlaku',
        'NPWP': 'npwp',
        'TELPON': 'telepon',
        'EMAIL': 'email',
        'KETERANGAN': 'keterangan'
    }
    
    # Auto-match columns
    col_mapping = {}
    available_cols = ['[Tidak Ada]'] + list(headers)
    
    cols_ui = st.columns(3)
    
    for idx, (pkl_col, db_field) in enumerate(pkl_mapping.items()):
        with cols_ui[idx % 3]:
            # Try to auto-match
            default_idx = 0
            for i, h in enumerate(headers):
                if h and pkl_col.lower() in str(h).lower():
                    default_idx = i + 1  # +1 because of [Tidak Ada]
                    break
            
            selected = st.selectbox(
                pkl_col,
                options=available_cols,
                index=default_idx,
                key=f"map_{db_field}"
            )
            
            if selected != '[Tidak Ada]':
                col_mapping[db_field] = selected
    
    st.markdown("---")
    
    # Step 5: Preview Processed Data
    st.header("5. Preview Data Final")
    
    processed_records = []
    
    for idx, row in df_data.iterrows():
        record = {
            'sektor': batch_sektor,
            'kategori_perizinan': batch_kategori,
        }
        
        for db_field, excel_col in col_mapping.items():
            value = row.get(excel_col, '')
            
            # Special processing
            if db_field == 'nib':
                value = clean_nib(value)
            elif db_field == 'nomor_tanggal_permohonan':
                nomor, tanggal = parse_nomor_tanggal(value)
                record['nomor_permohonan'] = nomor
                record['tanggal_permohonan'] = parse_indonesian_date(tanggal)
                continue
            elif db_field == 'nomor_tanggal_permohonan_rekomendasi':
                # Keep as combined field
                combined_value = str(value).strip() if pd.notna(value) else ''
                if combined_value in ['nan', '-', 'NaN']:
                    combined_value = ''
                record['nomor_tanggal_permohonan_rekomendasi'] = combined_value
                continue
            elif db_field == 'nomor_tanggal_rekomendasi':
                # Keep as combined field in nomor_tanggal_rekomendasi
                combined_value = str(value).strip() if pd.notna(value) else ''
                if combined_value in ['nan', '-', 'NaN']:
                    combined_value = ''
                record['nomor_tanggal_rekomendasi'] = combined_value
                continue
            elif db_field in ['tanggal_izin', 'masa_berlaku']:
                value = parse_indonesian_date(value)
            else:
                value = str(value).strip() if pd.notna(value) else ''
                if value in ['nan', '-', 'NaN']:
                    value = ''
            
            record[db_field] = value
        
        # Ensure all required fields exist
        all_fields = [
            'nama_pengguna_layanan', 'nib', 'alamat', 'pemilik_pengurus',
            'lokasi_usaha', 'luas_lahan_usaha', 'kbli', 'jenis_usaha', 'resiko',
            'kapasitas', 'jenis_permohonan', 'nomor_permohonan', 'tanggal_permohonan',
            'nomor_tanggal_permohonan_rekomendasi',
            'nomor_tanggal_rekomendasi', 'nomor_izin', 'tanggal_izin',
            'masa_berlaku', 'npwp', 'telepon', 'email', 'keterangan'
        ]
        for field in all_fields:
            if field not in record:
                record[field] = ''
        
        processed_records.append(record)
    
    # Display preview
    if processed_records:
        preview_df = pd.DataFrame(processed_records)
        
        # Show key columns for preview
        preview_cols = ['nama_pengguna_layanan', 'nib', 'nomor_izin', 'tanggal_izin', 'masa_berlaku', 'keterangan']
        available_preview = [c for c in preview_cols if c in preview_df.columns]
        
        st.dataframe(preview_df[available_preview], width='stretch')
        st.caption(f"Total: {len(processed_records)} records siap diimport")
        
        # Full preview
        with st.expander("Lihat Semua Kolom"):
            st.dataframe(preview_df, width='stretch')
        
        st.markdown("---")
        
        # Step 6: Import
        st.header("6. Import ke Database")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Import Data", type="primary", width='stretch'):
                progress = st.progress(0)
                status = st.empty()
                
                success_count = 0
                error_count = 0
                errors = []
                
                for i, record in enumerate(processed_records):
                    try:
                        insert_perizinan(record)
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {i+1}: {str(e)}")
                    
                    progress.progress((i + 1) / len(processed_records))
                    status.text(f"Processing {i+1}/{len(processed_records)}...")
                
                progress.empty()
                status.empty()
                
                if success_count > 0:
                    st.success(f"Berhasil mengimport {success_count} data!")
                
                if error_count > 0:
                    st.error(f"Gagal mengimport {error_count} data")
                    with st.expander("Detail Error"):
                        for err in errors:
                            st.text(err)
