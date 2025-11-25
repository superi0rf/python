import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Konfigurasi Halaman dan Data Sampel ---
st.set_page_config(
    layout="wide", 
    page_title="Lab Statistika 3D Interaktif", 
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_sample_data():
    """Memuat atau membuat data sampel untuk demonstrasi."""
    np.random.seed(42) # Agar hasilnya konsisten
    n_samples = 100
    
    # Variabel dengan korelasi positif moderat
    var_x = np.random.normal(loc=100, scale=15, size=n_samples) # Misalnya, Usia
    var_y = var_x * 0.7 + np.random.normal(loc=10, scale=5, size=n_samples) # Misalnya, Pendapatan
    
    # Variabel Z (mungkin sedikit korelasi negatif dengan X)
    var_z = 150 - (var_x * 0.5) + np.random.normal(loc=0, scale=10, size=n_samples) # Misalnya, Jam Tidur

    data = {
        'Usia': var_x,
        'Pendapatan': var_y,
        'Jam_Tidur': var_z,
        # Variabel Kategorikal untuk warna
        'Kota': np.random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan'], n_samples) 
    }
    return pd.DataFrame(data)

df_default = load_sample_data()

# --- Fungsi Utama Aplikasi ---

def main_app():
    
    st.title("🌌 Lab Statistika 3D: Eksplorasi Data Multivariat")
    st.markdown("Pilih tiga variabel (X, Y, Z) untuk divisualisasikan dalam ruang 3D dan analisis korelasinya.")
    st.markdown("---")
    
    # --- Sidebar: Kontrol Interaktif & Unggah Data ---
    
    st.sidebar.header("Kontrol Visualisasi")
    
    # Pilihan Sumber Data
    data_source = st.sidebar.radio(
        "Pilih Sumber Data:", 
        ("Data Sampel", "Unggah Data Sendiri (.csv)")
    )
    
    df = df_default
    
    if data_source == "Unggah Data Sendiri (.csv)":
        uploaded_file = st.sidebar.file_uploader("Unggah file CSV Anda", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.sidebar.success("Data berhasil dimuat!")
            except Exception as e:
                st.sidebar.error(f"Terjadi kesalahan saat memuat file: {e}")
                st.sidebar.info("Menggunakan Data Sampel.")

    # Memastikan hanya kolom numerik yang tersedia
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    if len(numeric_cols) < 3:
        st.error("Dataset harus memiliki minimal 3 kolom numerik untuk visualisasi 3D.")
        st.stop()

    # Inisialisasi default index
    default_indices = [0, 1, 2] 
    
    # Pemilihan Variabel Sumbu
    st.sidebar.subheader("Pilih Sumbu Data (X, Y, Z)")
    x_axis = st.sidebar.selectbox(
        "Sumbu X (Variabel 1):", 
        numeric_cols, 
        index=default_indices[0]
    )
    y_axis = st.sidebar.selectbox(
        "Sumbu Y (Variabel 2):", 
        numeric_cols, 
        index=default_indices[1] if len(numeric_cols)>1 else default_indices[0]
    )
    z_axis = st.sidebar.selectbox(
        "Sumbu Z (Variabel 3):", 
        numeric_cols, 
        index=default_indices[2] if len(numeric_cols)>2 else default_indices[0]
    )
    
    # Variabel Kategorikal untuk Warna (Opsional)
    color_col = st.sidebar.selectbox(
        "Warna Titik (Opsional - Variabel Kategorikal):", 
        ['Tidak Ada'] + categorical_cols
    )
    
    # --- Layout Utama ---
    
    col1, col2 = st.columns([4, 1.5])

    # --- Kolom 1: Visualisasi 3D ---
    with col1:
        st.header("📈 Visualisasi Scatter Plot 3D Interaktif")
        
        try:
            # Menggunakan Plotly Express untuk 3D Scatter Plot
            color_param = color_col if color_col != 'Tidak Ada' else None
            
            fig = px.scatter_3d(
                df,
                x=x_axis,
                y=y_axis,
                z=z_axis,
                color=color_param,
                opacity=0.7,
                title=f'Pola Hubungan: {x_axis} vs {y_axis} vs {z_axis}',
                height=650
            )
            
            fig.update_layout(scene_zaxis_title=z_axis, scene_yaxis_title=y_axis, scene_xaxis_title=x_axis)
            fig.update_traces(marker=dict(size=5))
            
            # Tampilkan Plotly Chart
            st.plotly_chart(fig, use_container_width=True)
            # 

        except Exception as e:
            st.error(f"Gagal membuat plot. Pastikan kolom yang dipilih valid. Detail Error: {e}")

    # --- Kolom 2: Analisis Korelasi ---
    with col2:
        st.header("🔢 Analisis Korelasi")
        st.info("Koefisien Korelasi Pearson ($r$) antar pasangan variabel (nilai antara -1 dan +1).")
        
        # Hitung dan tampilkan Korelasi
        if all(col in df.columns for col in [x_axis, y_axis, z_axis]):
            
            # Pastikan kolom yang dipilih adalah numerik
            df_corr = df[[x_axis, y_axis, z_axis]].copy()
            
            corr_matrix = df_corr.corr(numeric_only=True)
            
            corr_xy = corr_matrix.loc[x_axis, y_axis]
            corr_xz = corr_matrix.loc[x_axis, z_axis]
            corr_yz = corr_matrix.loc[y_axis, z_axis]
            
            st.markdown(f"### Pasangan Variabel")
            
            st.metric(
                label=f"({x_axis} & {y_axis})", 
                value=f"{corr_xy:.4f}",
                delta=f"{'Kuat' if abs(corr_xy) > 0.7 else 'Sedang' if abs(corr_xy) > 0.3 else 'Lemah'}"
            )
            st.metric(
                label=f"({x_axis} & {z_axis})", 
                value=f"{corr_xz:.4f}",
                delta=f"{'Kuat' if abs(corr_xz) > 0.7 else 'Sedang' if abs(corr_xz) > 0.3 else 'Lemah'}"
            )
            st.metric(
                label=f"({y_axis} & {z_axis})", 
                value=f"{corr_yz:.4f}",
                delta=f"{'Kuat' if abs(corr_yz) > 0.7 else 'Sedang' if abs(corr_yz) > 0.3 else 'Lemah'}"
            )
            
    st.markdown("---")
    
    # --- Penjelasan Konsep ---
    st.header("🧠 Panduan Konsep Statistika")
    st.markdown("""
* **Scatter Plot 3D:** Titik-titik data dalam ruang tiga dimensi. Interaktivitas Plotly memungkinkan siswa untuk memutar plot, **melihat kluster** (pengelompokan), dan **memahami tren** dari berbagai sudut pandang.
* **Koefisien Korelasi ($r$):** Mengukur **kualitas hubungan linear** antara dua variabel.
    * Nilai $r$ positif $\rightarrow$ Kedua variabel bergerak ke arah yang sama (saat satu naik, yang lain cenderung naik).
    * Nilai $r$ negatif $\rightarrow$ Kedua variabel bergerak ke arah yang berlawanan (saat satu naik, yang lain cenderung turun).
    * Nilai $r$ mendekati 0 $\rightarrow$ Hubungan linear lemah atau tidak ada.
""")
    
if __name__ == "__main__":
    main_app()
