import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# --- 1. Fungsi Perhitungan Statistik ---

def hitung_statistik(data):
    """Menghitung metrik statistik utama dari array data."""
    if len(data) == 0:
        return None
        
    df = pd.Series(data)
    
    # Menghitung Rata-rata, Median, Modus
    rata_rata = df.mean()
    median = df.median()
    
    # Modus: Menggunakan scipy.stats.mode, yang mengembalikan array
    try:
        modus_result = stats.mode(df)
        modus = modus_result.mode[0] if len(modus_result.mode) > 0 else "Tidak Ada"
    except:
        modus = df.mode().tolist()
        modus = modus[0] if len(modus) > 0 else "Tidak Ada"
    
    # Menghitung Sebaran
    rentang = df.max() - df.min()
    variansi = df.var()
    simpangan_baku = df.std()
    
    return {
        'Rata-rata (Mean)': rata_rata,
        'Median': median,
        'Modus': modus,
        'Rentang (Range)': rentang,
        'Variansi': variansi,
        'Simpangan Baku (Std Dev)': simpangan_baku
    }

# --- 2. Fungsi Visualisasi 3D dan Distribusi ---

def plot_distribusi(data, stats_results):
    """
    Membuat histogram sederhana dan visualisasi 3D sebaran nilai
    """
    fig = plt.figure(figsize=(12, 5))
    
    # ------------------
    # Plot 1: Histogram (Distribusi Nilai)
    # ------------------
    ax1 = fig.add_subplot(121)
    
    # Membuat bins berdasarkan rentang nilai (0-100)
    bins = np.arange(0, 101, 10) 
    
    ax1.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='#1f77b4')
    ax1.axvline(stats_results['Rata-rata (Mean)'], color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {stats_results["Rata-rata (Mean)"]:.2f}')
    ax1.axvline(stats_results['Median'], color='green', linestyle='dashed', linewidth=1.5, label=f'Median: {stats_results["Median"]:.2f}')
    
    ax1.set_title("Distribusi Nilai Ujian (Histogram)")
    ax1.set_xlabel("Nilai Ujian")
    ax1.set_ylabel("Frekuensi")
    ax1.set_xlim(0, 100)
    ax1.legend(loc='upper left')

    # ------------------
    # Plot 2: Scatter Plot 3D (Visualisasi Sebaran)
    # ------------------
    ax2 = fig.add_subplot(122, projection='3d')
    
    N = len(data)
    
    # Data 3D:
    # X = Nilai Ujian (Fokus)
    # Y = Indeks Siswa (Untuk memberi kedalaman/pemisahan visual)
    # Z = Jarak dari Rata-rata (Untuk memberi dimensi 3D, menunjukkan sebaran)
    
    x_vals = data
    y_vals = np.arange(N)
    z_vals = np.abs(data - stats_results['Rata-rata (Mean)']) / stats_results['Simpangan Baku (Std Dev)']
    
    # Keterangan Warna: Merah jika di bawah rata-rata, Biru jika di atas
    colors = ['r' if x < stats_results['Rata-rata (Mean)'] else 'b' for x in data]

    scatter = ax2.scatter(x_vals, y_vals, z_vals, c=colors, marker='o', alpha=0.8)

    ax2.set_xlabel("Nilai Ujian (X)")
    ax2.set_ylabel("Indeks Siswa (Y)")
    ax2.set_zlabel("Jarak Relatif dari Rata-rata (Z)")
    ax2.set_title("Sebaran Nilai 3D (Jarak dari Rata-rata)")
    
    st.pyplot(fig)
    

[Image of a Cartesian graph showing a plotted curve representing a mathematical function, demonstrating its shape, intercepts, and slope.]



# --- 3. UI Streamlit ---

st.set_page_config(page_title="Virtual Lab Statistika Ujian", layout="wide")

st.title("🧪 Virtual Lab: Analisis Statistika Nilai Ujian")
st.markdown("Eksplorasi **Rata-rata, Median, Modus, dan Simpangan Baku** dari sekumpulan nilai, serta visualisasi sebarannya dalam 3D.")

# --- SIDEBAR (Input Data) ---
st.sidebar.header("🛠️ Input Data Nilai")

data_source = st.sidebar.radio(
    "Sumber Data:",
    ('Input Manual (Teks)', 'Hasilkan Data Acak')
)

nilai_list = []
input_gagal = False

if data_source == 'Input Manual (Teks)':
    nilai_str = st.sidebar.text_area(
        "Masukkan Nilai Ujian (dipisahkan koma atau baris baru, rentang 0-100):",
        "75, 80, 65, 90, 85, 70, 78, 92, 60, 88"
    )
    
    try:
        # Membersihkan input dan mengkonversi ke float
        raw_values = nilai_str.replace('\n', ',').split(',')
        nilai_list = [float(v.strip()) for v in raw_values if v.strip()]
        
        # Validasi rentang nilai
        if not all(0 <= n <= 100 for n in nilai_list):
            st.sidebar.error("Pastikan semua nilai berada dalam rentang 0 hingga 100.")
            input_gagal = True
        
    except ValueError:
        st.sidebar.error("Input tidak valid. Harap masukkan angka saja.")
        input_gagal = True
        
elif data_source == 'Hasilkan Data Acak':
    jumlah_siswa = st.sidebar.slider("Jumlah Siswa (N)", 10, 200, 50)
    rata_rata_target = st.sidebar.slider("Rata-rata Target", 50, 90, 75)
    sebaran_target = st.sidebar.slider("Sebaran Target (Std Dev)", 5, 20, 10)
    
    # Hasilkan data acak (Distribusi Normal)
    np.random.seed(42) # Agar hasil konsisten
    random_data = np.random.normal(rata_rata_target, sebaran_target, jumlah_siswa)
    
    # Batasi nilai antara 0 dan 100
    random_data = np.clip(random_data, 0, 100)
    nilai_list = random_data.tolist()

# Konversi data ke array NumPy setelah validasi
data_ujian = np.array(nilai_list)

# --- TAMPILAN UTAMA ---

if len(data_ujian) < 2 or input_gagal:
    st.warning("Masukkan minimal 2 nilai yang valid (0-100) untuk memulai analisis statistik.")
    st.markdown(f"**Jumlah Data Saat Ini:** {len(data_ujian)}")
else:
    st.header("Hasil Analisis Statistik")
    
    # Hitung semua metrik
    stats_results = hitung_statistik(data_ujian)
    
    col1, col2, col3 = st.columns(3)
    
    # Kolom 1: Tendensi Sentral
    with col1:
        st.subheader("Tendensi Sentral (Pusat Data)")
        st.metric(label="Rata-rata (Mean)", value=f"{stats_results['Rata-rata (Mean)']:.2f}")
        st.metric(label="Median", value=f"{stats_results['Median']:.2f}")
        st.metric(label="Modus", value=str(stats_results['Modus']))
        
    # Kolom 2: Ukuran Sebaran
    with col2:
        st.subheader("Ukuran Sebaran (Variabilitas)")
        st.metric(label="Simpangan Baku (Std Dev)", value=f"{stats_results['Simpangan Baku (Std Dev)']:.2f}")
        st.metric(label="Variansi", value=f"{stats_results['Variansi']:.2f}")
        st.metric(label="Rentang (Range)", value=f"{stats_results['Rentang (Range)']:.2f}")

    # Kolom 3: Ringkasan Data
    with col3:
        st.subheader("Ringkasan Data")
        st.metric(label="Jumlah Siswa (N)", value=f"{len(data_ujian)}")
        st.metric(label="Nilai Tertinggi", value=f"{data_ujian.max():.2f}")
        st.metric(label="Nilai Terendah", value=f"{data_ujian.min():.2f}")

    st.markdown("---")
    
    # Visualisasi
    st.header("Visualisasi Data Nilai")
    st.markdown("Grafik di bawah menunjukkan **Distribusi Nilai** (Kiri) dan **Sebaran 3D** (Kanan).")
    
    plot_distribusi(data_ujian, stats_results)
    
    st.markdown("""
    **Penjelasan Visualisasi 3D:**
    * **Sumbu X (Nilai):** Posisi horizontal nilai ujian.
    * **Sumbu Y (Siswa):** Indeks siswa (hanya untuk memberikan pemisahan visual).
    * **Sumbu Z (Jarak Relatif):** Seberapa jauh nilai siswa tersebut dari Rata-rata ($\mu$), dinormalisasi oleh Simpangan Baku ($\sigma$). **Semakin tinggi** posisi pada sumbu Z, **semakin ekstrem** nilai siswa tersebut.
    """)
    
st.markdown("---")
st.caption("Dibuat dengan Python (NumPy, Pandas, Matplotlib) dan Streamlit.")
