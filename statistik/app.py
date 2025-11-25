import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide")

## 🚀 Virtual Lab Statistika: Analisis Nilai Ujian 3D

st.title("📊 Virtual Lab Statistika: Analisis Nilai Ujian")
st.markdown("### Eksplorasi Data Nilai Ujian secara Interaktif dalam 3 Dimensi")

# --- Input Data Simulasi ---
st.sidebar.header("⚙️ Pengaturan Data Simulasi")

# Parameter input untuk data
jumlah_siswa = st.sidebar.slider("Jumlah Siswa (N)", 10, 200, 50)
nilai_min = st.sidebar.slider("Nilai Minimum", 0, 50, 40)
nilai_max = st.sidebar.slider("Nilai Maksimum", 50, 100, 95)
tingkat_kesulitan = st.sidebar.selectbox(
    "Tingkat Kesulitan Ujian (Simulasi Distribusi)", 
    ["Mudah (Skew Kiri)", "Normal", "Sulit (Skew Kanan)"]
)

# --- Generasi Data ---
def generate_data(n, v_min, v_max, skew_type):
    # Simulasi nilai dengan distribusi tertentu
    if skew_type == "Normal":
        # Distribusi Normal (bell curve)
        mu, sigma = (v_min + v_max) / 2, (v_max - v_min) / 6
        data = np.random.normal(mu, sigma, n)
    elif skew_type == "Mudah (Skew Kiri)":
        # Banyak siswa mendapat nilai tinggi
        data = np.random.beta(a=5, b=2, size=n) * (v_max - v_min) + v_min
    else: # Sulit (Skew Kanan)
        # Banyak siswa mendapat nilai rendah
        data = np.random.beta(a=2, b=5, size=n) * (v_max - v_min) + v_min
    
    # Pastikan nilai berada di rentang [nilai_min, nilai_max] dan dibulatkan
    data = np.clip(data, v_min, v_max).astype(int)
    
    df = pd.DataFrame({
        'Nama Siswa': [f'Siswa_{i+1}' for i in range(n)],
        'Nilai Ujian': data
    })
    return df

df = generate_data(jumlah_siswa, nilai_min, nilai_max, tingkat_kesulitan)

# --- Perhitungan Statistika Deskriptif ---
mean_val = df['Nilai Ujian'].mean()
median_val = df['Nilai Ujian'].median()
mode_val = df['Nilai Ujian'].mode()
std_val = df['Nilai Ujian'].std()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rata-rata (Mean) 🧠", f"{mean_val:.2f}")
with col2:
    st.metric("Nilai Tengah (Median) 🎯", f"{median_val:.2f}")
with col3:
    # Handle multiple modes or no mode easily
    st.metric("Modus (Mode) 🏆", f"{mode_val.iloc[0] if not mode_val.empty else 'N/A'}")
with col4:
    st.metric("Standar Deviasi (SD) 📏", f"{std_val:.2f}")

st.dataframe(df.head(), use_container_width=True)

st.subheader("Visualisasi Interaktif 3D")

# --- Visualisasi 3D (Histogram 3D atau Scatter Plot) ---
# Kita akan membuat DataFrame untuk visualisasi 3D yang lebih kaya
# Asumsi: Siswa diberi ID (1D), Nilai Ujian (2D), Frekuensi (3D - Tinggi bar)

# Data untuk visualisasi frekuensi
nilai_counts = df['Nilai Ujian'].value_counts().reset_index()
nilai_counts.columns = ['Nilai Ujian', 'Frekuensi']
nilai_counts['Kategori'] = pd.cut(nilai_counts['Nilai Ujian'], 
                                   bins=[0, 70, 80, 100], 
                                   labels=['Kurang (<70)', 'Cukup (70-80)', 'Baik (>80)'], 
                                   right=False)

# Tambahkan sumbu Z buatan agar bisa divisualisasikan 3D
# Sumbu Z bisa merepresentasikan 'Kategori' atau 'Frekuensi' itu sendiri.
# Kita pakai Frekuensi untuk Z, dan Nilai untuk X, Kategori untuk Y (Warna)

fig = px.scatter_3d(
    nilai_counts, 
    x='Nilai Ujian', 
    y='Kategori', # Gunakan Kategori sebagai sumbu Y untuk pemisahan visual
    z='Frekuensi', 
    color='Kategori', # Gunakan warna untuk membedakan kategori
    size='Frekuensi', # Ukuran marker berdasarkan frekuensi
    hover_data=['Nilai Ujian', 'Frekuensi'],
    title="Distribusi Nilai Ujian dalam Ruang 3D"
)

# Sesuaikan tampilan
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=30),
    scene = dict(
        xaxis_title='Nilai Ujian',
        yaxis_title='Kategori Nilai',
        zaxis_title='Frekuensi Kemunculan'
    )
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
**💡 Cara Membaca Visualisasi 3D:**
1.  **Sumbu X (Nilai Ujian):** Menunjukkan skor yang diperoleh siswa.
2.  **Sumbu Y (Kategori Nilai):** Memisahkan data berdasarkan kelompok nilai (Kurang, Cukup, Baik).
3.  **Sumbu Z (Frekuensi):** Menunjukkan berapa banyak siswa yang mendapatkan nilai tersebut.
4.  **Interaksi:** Klik dan seret plot untuk memutar dan melihat distribusi dari berbagai sudut!
""")
