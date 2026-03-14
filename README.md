# DPMPTSP Permit Information System

A web-based permit management web application for the Lampung Province Department of Investment and One-Stop Integrated Services.

## Features

- **Data Entry**: Input new permit data with text autocomplete features.
- **Validity Monitoring**: Monitor the validity status of permits (supports calibrated lifetime logic).
- **SLA Monitoring**: Monitor completion timeframes against Service Level Agreements.
- **Data Table**: View, filter, and edit data in an interactive table format.
- **Data Import**: Automatically import data from Excel files using intelligent data mapping.
- **Dashboard**: Data analytics and visualization (Yearly, Monthly, Quarterly basis, etc.).

### Recent Updates (March 2026)
- Added new **Risk Options** ("RENDAH", "MENENGAH RENDAH").
- Added new **Permit Type Option** ("Perubahan").
- Changed the **Validity Date (Masa Berlaku)** field to a flexible free-text input.
- Standardized the lifetime validity parameter to **"Selama Pelaku Usaha Menjalankan Kegiatan Usaha"**.
- Added the **Investment Plan Value (Rencana Investasi)** column.

## Installation

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

```bash
# Clone or download the repository
cd path/to/folder

# Install dependencies
pip install streamlit pandas openpyxl plotly

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Folder Structure

```
/
├── app.py                 # Application entry point
├── database.py            # SQLite database functions
├── perizinan.db           # SQLite database
├── a.txt                  # List of sectors
├── extractor.py           # Excel data extraction (standalone)
└── pages/
    ├── Home.py            # Homepage
    ├── 1_Input_Data.py    # Permit entry form
    ├── 2_Data_Perizinan.py# Validity data / Monitoring
    ├── 3_Analytics.py     # Analytics dashboard
    ├── 4_Tabel_Data.py    # Editable data table
    ├── 5_Import_Data.py   # Excel import tool
    └── 6_SLA_Monitoring.py# SLA monitoring
```

## Technology Stack

- **Frontend**: Streamlit
- **Database**: SQLite
- **Data Processing**: Pandas
- **Visualization**: Plotly

## License

Internal use only - DPMPTSP Provinsi Lampung
