import os
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

# 1. Fungsi Load Data dengan Clustering (Manual Grouping / Binning)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    day_path = os.path.join(current_dir, 'day.csv')
    hour_path = os.path.join(current_dir, 'hour.csv')
    
    if not os.path.exists(day_path):
        day_path = os.path.join(current_dir, '..', 'data', 'day.csv')
        hour_path = os.path.join(current_dir, '..', 'data', 'hour.csv')

    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)

    # Konversi tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Label Cuaca
    weather_map = {
        1: 'Clear/Few Clouds',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Severe Weather'
    }
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_map)
    
    # --- PENERAPAN ANALISIS LANJUTAN (CLUSTERING / MANUAL GROUPING & BINNING) ---
    # Binning Kategori Permintaan (Demand)
    bins = [0, 2000, 5000, 10000]
    labels = ['Low Demand', 'Medium Demand', 'High Demand']
    day_df['demand_category'] = pd.cut(day_df['cnt'], bins=bins, labels=labels)

    # Grouping Kategori Waktu Harian
    def hour_group(hour):
        if 0 <= hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'

    hour_df['time_of_day'] = hour_df['hr'].apply(hour_group)
    
    return day_df, hour_df

# Load dataset
day_df, hour_df = load_data()

# 2. Sidebar Filter
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=[2011, 2012],
    default=[2011, 2012]
)

# Convert yr (0: 2011, 1: 2012)
year_map = {2011: 0, 2012: 1}
selected_years = [year_map[y] for y in year_filter]
filtered_day_df = day_df[day_df['yr'].isin(selected_years)]
filtered_hour_df = hour_df[hour_df['yr'].isin(selected_years)]

# 3. Header Dashboard
st.title("🚲 Bike Sharing Data Analysis Dashboard")
st.markdown("---")

# 4. Ringkasan Metrik
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Penyewaan Casual", f"{filtered_day_df['casual'].sum():,}")
with col3:
    st.metric("Penyewaan Registered", f"{filtered_day_df['registered'].sum():,}")

st.markdown("---")

# =========================================================
# BAGIAN 1: PERTANYAAN BISNIS UTAMA
# =========================================================
st.subheader("📊 Analisis Pertanyaan Utama")

col_biz1, col_biz2 = st.columns(2)

with col_biz1:
    st.write("**1. Pengaruh Cuaca terhadap Total Penyewaan**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=filtered_day_df, x='weather_label', y='cnt', palette='viridis', ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

with col_biz2:
    st.write("**2. Tren Penyewaan Sepeda berdasarkan Jam**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=filtered_hour_df, x='hr', y='cnt', hue='workingday', palette='Set1', ax=ax)
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

st.markdown("---")

# =========================================================
# BAGIAN 2: ANALISIS LANJUTAN (CLUSTERING / BINNING)
# =========================================================
st.subheader("📌 Analisis Lanjutan: Pengelompokan Data (Clustering / Binning)")

col_adv1, col_adv2 = st.columns(2)

with col_adv1:
    st.write("**1. Distribusi Kategori Permintaan (Demand Category)**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_day_df, x='demand_category', palette='Blues', ax=ax)
    ax.set_xlabel("Kategori Demand")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)

with col_adv2:
    st.write("**2. Rata-rata Penyewaan berdasarkan Kategori Waktu Harian**")
    time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
    time_avg = filtered_hour_df.groupby('time_of_day')['cnt'].mean().reindex(time_order).reset_index()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=time_avg, x='time_of_day', y='cnt', palette='Oranges', ax=ax)
    ax.set_xlabel("Waktu Hari")
    ax.set_ylabel("Rata-rata Penyewaan / Jam")
    st.pyplot(fig)
