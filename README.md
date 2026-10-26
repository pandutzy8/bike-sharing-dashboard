# 🚲 Bike Sharing Analysis Dashboard

Dashboard interaktif untuk menganalisis data penyewaan sepeda berdasarkan pengaruh kondisi cuaca serta pola penggunaan berdasarkan waktu harian.

## ✨ Fitur

- Analisis jumlah penyewaan sepeda berdasarkan kondisi cuaca.
- Visualisasi tren penyewaan berdasarkan jam, hari, dan musim.
- Dashboard interaktif menggunakan Streamlit.
- Menampilkan insight untuk membantu memahami pola penggunaan layanan bike sharing.

---

## 📁 Struktur Proyek

```text
proyek_analisis_data/
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Environment

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Pipenv (Shell/Terminal)

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data

pipenv install
pipenv shell

pip install -r requirements.txt
```

---

## ▶️ Menjalankan Dashboard

Masuk ke folder dashboard dan jalankan perintah berikut:

```bash
cd dashboard
streamlit run dashboard.py
```

Setelah berhasil dijalankan, aplikasi dapat diakses melalui browser pada alamat:

```text
http://localhost:8501
```

---

## 📦 Dependencies

Library utama yang digunakan dalam proyek ini:

- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn

Untuk menginstal seluruh dependensi:

```bash
pip install -r requirements.txt
```

---

## 📊 Dataset

Dataset yang digunakan berasal dari **Bike Sharing Dataset** yang berisi informasi mengenai:

- Jumlah penyewaan sepeda harian dan per jam.
- Kondisi cuaca.
- Musim (season).
- Hari kerja dan hari libur.
- Variabel lingkungan lainnya yang memengaruhi jumlah penyewaan.

---

## 👨‍💻 Author

**Muhammad Pandu Tri Kurniawan**

Proyek Analisis Data - Bike Sharing Dashboard.
