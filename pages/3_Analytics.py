import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db

st.set_page_config(page_title="Dashboard Analitik", page_icon="📊", layout="wide")

st.title("Dashboard Analitik DPMPTSP")
st.markdown("### Analisis Data Perizinan Multi-Sektor")

# Period filter
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
with col1:
    period_type = st.selectbox(
        "Periode Analisis",
        options=['yearly', 'quarterly', 'monthly'],
        format_func=lambda x: {
            'yearly': 'Tahunan',
            'quarterly': 'Triwulan',
            'monthly': 'Bulanan'
        }[x],
        index=0,  # Default to yearly
        help="Pilih jenis periode untuk analisis data"
    )

# Get available years from database
available_years = db.get_available_years()

if not available_years:
    available_years = ['2025', '2024']  # Default years if no data

with col2:
    selected_year = st.selectbox(
        "Tahun",
        options=available_years,
        index=0,
        help="Pilih tahun untuk analisis"
    )

# Additional filters based on period type
if period_type == 'quarterly':
    with col3:
        selected_quarter = st.selectbox(
            "Triwulan",
            options=['TW1', 'TW2', 'TW3', 'TW4'],
            format_func=lambda x: {
                'TW1': 'TW1 (Jan-Mar)',
                'TW2': 'TW2 (Apr-Jun)',
                'TW3': 'TW3 (Jul-Sep)',
                'TW4': 'TW4 (Okt-Des)'
            }[x],
            help="Pilih triwulan"
        )
elif period_type == 'monthly':
    with col3:
        selected_month = st.selectbox(
            "Bulan",
            options=list(range(1, 13)),
            format_func=lambda x: {
                1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
                5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
                9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
            }[x],
            help="Pilih bulan"
        )

# Build period parameters
if period_type == 'yearly':
    period_params = {'type': 'yearly', 'year': selected_year}
elif period_type == 'quarterly':
    period_params = {'type': 'quarterly', 'year': selected_year, 'quarter': selected_quarter}
else:  # monthly
    period_params = {'type': 'monthly', 'year': selected_year, 'month': selected_month}

# Get analytics data with period filter
metrics = db.get_analytics_metrics(period=period_params)

# Metric Cards
st.subheader("Metrik Utama")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Rata-rata SLA",
        value=f"{metrics.get('avg_sla', 0)} Hari",
        help="Rata-rata waktu proses dari permohonan hingga izin terbit"
    )

with col2:
    st.metric(
        label="Jumlah Pelaku Usaha",
        value=metrics['jumlah_pelaku'],
        help="Jumlah pelaku usaha unik berdasarkan NIK"
    )

with col3:
    st.metric(
        label="Total NIB",
        value=metrics['total_nib'],
        help="Total aktivitas perizinan yang diproses"
    )



# Charts Section
col1, col2 = st.columns(2)

with col1:
    if metrics['risk_distribution']:
        # Prepare data for bar chart
        risk_labels = [item[0] for item in metrics['risk_distribution']]
        risk_counts = [item[1] for item in metrics['risk_distribution']]
        
        # Create DataFrame
        df_risk = pd.DataFrame({
            'Tingkat Resiko': risk_labels,
            'Jumlah': risk_counts
        })
        
        # Color mapping - professional government palette
        color_map = {
            'MENENGAH TINGGI': '#0369a1',  # Sky blue
            'TINGGI': '#0c4a6e',           # Dark blue
            'UMKU': '#115e59'              # Teal
        }
        
        colors = [color_map.get(label, '#475569') for label in risk_labels]
        
        fig_risk = go.Figure(data=[
            go.Bar(
                x=df_risk['Tingkat Resiko'],
                y=df_risk['Jumlah'],
                marker_color=colors,
                text=df_risk['Jumlah'],
                textposition='inside',
                textfont=dict(color='white', size=14, family='Arial Black')
            )
        ])
        
        fig_risk.update_layout(
            title={
                'text': 'Distribusi Tingkat Risiko',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
            },
            xaxis_title="Tingkat Risiko",
            yaxis_title="Jumlah Usaha",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_risk, width="stretch")
        
        # Summary text
        total = sum(risk_counts)
        if total > 0:
            st.caption(f"Total: {total} usaha terdata")
            for label, count in zip(risk_labels, risk_counts):
                percentage = (count / total) * 100
                st.caption(f"• {label}: {count} ({percentage:.1f}%)")
    else:
        st.info("Belum ada data resiko")

with col2:
    if metrics['kategori_distribution']:
        # Prepare data for pie chart
        kategori_labels = [item[0] for item in metrics['kategori_distribution']]
        kategori_counts = [item[1] for item in metrics['kategori_distribution']]
        
        # Create DataFrame
        df_kategori = pd.DataFrame({
            'Kategori': kategori_labels,
            'Jumlah': kategori_counts
        })
        
        # Color mapping - distinct professional colors
        color_discrete_map = {
            'Perizinan': '#0369a1',           # Sky blue
            'Perizinan Berusaha': '#0f766e',  # Dark teal
            'Non-Perizinan': '#1e3a5f'        # Navy blue
        }
        
        fig_kategori = px.pie(
            df_kategori,
            values='Jumlah',
            names='Kategori',
            color='Kategori',
            color_discrete_map=color_discrete_map,
            hole=0.4
        )
        
        fig_kategori.update_traces(
            textposition='inside',
            textinfo='value',
            textfont=dict(size=12)
        )
        
        fig_kategori.update_layout(
            title={
                'text': 'Distribusi Kategori Perizinan',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
            },
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_kategori, width="stretch")
        
        # Summary text
        total = sum(kategori_counts)
        if total > 0:
            st.caption(f"Total: {total} usaha terdata")
            for label, count in zip(kategori_labels, kategori_counts):
                percentage = (count / total) * 100
                st.caption(f"• {label}: {count} ({percentage:.1f}%)")
    else:
        st.info("Belum ada data kategori perizinan")

# Row 1.5: Jenis Dokumen Distribution (Full Width)
if metrics.get('jenis_dokumen_dist'):
    jenis_labels = [item[0] for item in metrics['jenis_dokumen_dist']]
    jenis_counts = [item[1] for item in metrics['jenis_dokumen_dist']]
    
    df_jenis_dok = pd.DataFrame({
        'Jenis Dokumen': jenis_labels,
        'Jumlah': jenis_counts
    })
    
    # Color mapping - professional government palette (cohesive blues/teals)
    color_map = {
        'Izin': '#0369a1',              # Sky blue
        'Persetujuan': '#0284c7',       # Light sky blue
        'UMKU': '#0d9488',              # Teal
        'Sertifikat Standar': '#14b8a6', # Light teal
        'Surat Keterangan': '#0891b2',  # Cyan
        'Laporan': '#06b6d4',           # Light cyan
        'Rekomendasi': '#22d3d1'        # Aqua
    }
    
    colors = [color_map.get(label, '#475569') for label in jenis_labels]
    
    fig_jenis_dok = go.Figure(data=[
        go.Bar(
            x=df_jenis_dok['Jenis Dokumen'],
            y=df_jenis_dok['Jumlah'],
            marker_color=colors,
            text=df_jenis_dok['Jumlah'],
            textposition='inside',
            textfont=dict(color='white', size=14, family='Arial Black')
        )
    ])
    
    fig_jenis_dok.update_layout(
        title={
            'text': 'Distribusi Jenis Dokumen',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
        },
        xaxis_title="Jenis Dokumen",
        yaxis_title="Jumlah",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_jenis_dok, width='stretch')
    
    # Summary
    total = sum(jenis_counts)
    if total > 0:
        cols = st.columns(len(jenis_labels))
        for idx, (label, count) in enumerate(zip(jenis_labels, jenis_counts)):
            with cols[idx]:
                percentage = (count / total) * 100
                st.caption(f"**{label}**: {count} ({percentage:.1f}%)")


# Row 2: Time Trend and Jenis Permohonan
col1, col2 = st.columns(2)

with col1:
    if metrics['time_trend']:
        # Time trend line chart
        months = [item[0] for item in metrics['time_trend']]
        counts = [item[1] for item in metrics['time_trend']]
        
        df_time = pd.DataFrame({
            'Bulan': months,
            'Jumlah': counts
        })
        
        fig_time = go.Figure(data=[
            go.Scatter(
                x=df_time['Bulan'],
                y=df_time['Jumlah'],
                mode='lines+markers+text',
                line=dict(color='#0369a1', width=3),
                marker=dict(size=10, color='#0369a1'),
                text=df_time['Jumlah'],
                textposition='top center',
                textfont=dict(size=12, color='white')
            )
        ])
        
        fig_time.update_layout(
            title={
                'text': 'Tren Pendaftaran per Bulan',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
            },
            xaxis_title="Bulan",
            yaxis_title="Jumlah Pendaftaran",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_time, width="stretch")
    else:
        st.info("Belum ada data tren waktu")

with col2:
    if metrics['jenis_permohonan_dist']:
        # Jenis Permohonan pie chart
        jenis_labels = [item[0] for item in metrics['jenis_permohonan_dist']]
        jenis_counts = [item[1] for item in metrics['jenis_permohonan_dist']]
        
        df_jenis = pd.DataFrame({
            'Jenis': jenis_labels,
            'Jumlah': jenis_counts
        })
        
        # Professional government palette
        color_map = {
            'Baru': '#0369a1',        # Sky blue
            'Perpanjangan': '#0891b2' # Cyan
        }
        
        fig_jenis = px.pie(
            df_jenis,
            values='Jumlah',
            names='Jenis',
            color='Jenis',
            color_discrete_map=color_map,
            hole=0.4
        )
        
        fig_jenis.update_traces(
            textposition='inside',
            textinfo='value',
            textfont=dict(size=12)
        )
        
        fig_jenis.update_layout(
            title={
                'text': 'Distribusi Jenis Permohonan',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
            },
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_jenis, width="stretch")
    else:
        st.info("Belum ada data jenis permohonan")

# Row 3: Geographic Distribution (Full Width)
if metrics['geo_distribution']:
    # Geographic bar chart
    locations = [item[0] for item in metrics['geo_distribution']]
    counts = [item[1] for item in metrics['geo_distribution']]
    
    df_geo = pd.DataFrame({
        'Lokasi': locations,
        'Jumlah': counts
    })
    
    fig_geo = go.Figure(data=[
        go.Bar(
            y=df_geo['Lokasi'],
            x=df_geo['Jumlah'],
            orientation='h',
            marker_color='#0369a1',  # Sky blue
            text=df_geo['Jumlah'],
            textposition='inside',
            textfont=dict(color='white', size=18, family='Arial Black'),
            textangle=0
        )
    ])
    
    fig_geo.update_layout(
        title={
            'text': 'Distribusi Geografis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white', 'family': 'Arial'}
        },
        xaxis_title="Jumlah Usaha",
        yaxis_title="Lokasi Usaha",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_geo, width="stretch")
else:
    st.info("Belum ada data geografis")

st.caption("Dashboard Analitik DPMPTS Provinsi Lampung")
