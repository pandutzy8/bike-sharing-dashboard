import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Analisis Bike Sharing",
    page_icon="🚲",
    layout="wide"
)

# Fungsi untuk memuat dan membersihkan data
@st.cache_data
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    
    # Konversi tipe data tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping label cuaca
    weather_map = {
        1: 'Clear/Few Clouds',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    }
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)
    
    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# ==========================================
# SIDEBAR / FILTER DATA
# ==========================================
st.sidebar.title("🚲 Filter Analisis")

# Filter Tahun
year_option = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=[2011, 2012],
    index=1
)

# Filter Rentang Tanggal
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter Data berdasarkan Input Sidebar
filtered_day_df = day_df[
    (day_df['dteday'].dt.year == year_option) &
    (day_df['dteday'].dt.date >= start_date) &
    (day_df['dteday'].dt.date <= end_date)
]

filtered_hour_df = hour_df[
    (hour_df['dteday'].dt.year == year_option) &
    (hour_df['dteday'].dt.date >= start_date) &
    (hour_df['dteday'].dt.date <= end_date)
]

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown(f"**Menampilkan Data Tahun {year_option}**")

# Ringkasan Performa (Metric Cards)
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rentals = filtered_day_df['cnt'].sum()
    st.metric("Total Penyewaan", f"{total_rentals:,}")

with col2:
    avg_daily_rentals = int(filtered_day_df['cnt'].mean()) if not filtered_day_df.empty else 0
    st.metric("Rata-rata Harian", f"{avg_daily_rentals:,}")

with col3:
    registered_rentals = filtered_day_df['registered'].sum()
    st.metric("Pengguna Terdaftar", f"{registered_rentals:,}")

with col4:
    casual_rentals = filtered_day_df['casual'].sum()
    st.metric("Pengguna Kasual", f"{casual_rentals:,}")

st.divider()

# ==========================================
# VISUALISASI PERTANYAAN 1
# ==========================================
st.subheader("1. Pengaruh Cuaca Terhadap Rata-rata Penyewaan Sepeda Harian")

if not filtered_day_df.empty:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(
        x='weather_label', 
        y='cnt', 
        data=filtered_day_df, 
        estimator=lambda x: sum(x)/len(x) if len(x) > 0 else 0,
        errorbar=None,
        palette='Blues_d',
        ax=ax1
    )
    ax1.set_xlabel("Kondisi Cuaca")
    ax1.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax1.set_title(f"Rata-rata Penyewaan Harian berdasarkan Cuaca ({year_option})")
    st.pyplot(fig1)
else:
    st.warning("Data tidak tersedia untuk rentang tanggal ini.")

st.divider()

# ==========================================
# VISUALISASI PERTANYAAN 2
# ==========================================
st.subheader("2. Pola Penyewaan Sepeda per Jam: Hari Kerja vs Hari Libur")

if not filtered_hour_df.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    sns.lineplot(
        data=filtered_hour_df, 
        x='hr', 
        y='cnt', 
        hue='workingday', 
        palette={0: 'orange', 1: 'blue'}, 
        marker='o',
        ax=ax2
    )
    ax2.set_xlabel("Jam (00:00 - 23:00)")
    ax2.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax2.set_xticks(range(0, 24))
    ax2.set_title("Pola Jam Penyewaan Sepeda per Jam")
    
    # Penyesuaian Legenda
    ax2.legend(
        title='Tipe Hari', 
        labels=['Hari Libur / Weekend', 'Hari Kerja']
    )
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)
else:
    st.warning("Data jam tidak tersedia untuk filter saat ini.")

# Footnote
st.caption("Proyek Analisis Data - Bike Sharing Dataset")