import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Fungsi Transformasi ---

def translasi(titik, vektor_t):
    """Melakukan translasi titik. Titik dan Vektor_T adalah array [x, y]"""
    return titik + vektor_t

def rotasi(titik, sudut_deg, pusat=np.array([0, 0])):
    """Melakukan rotasi titik terhadap pusat (default 0,0)"""
    sudut_rad = np.deg2rad(sudut_deg)
    matriks_rotasi = np.array([
        [np.cos(sudut_rad), -np.sin(sudut_rad)],
        [np.sin(sudut_rad), np.cos(sudut_rad)]
    ])
    
    # Translasi titik ke pusat (jika pusat bukan [0,0]), rotasi, lalu translasi kembali
    titik_pusat = titik - pusat
    titik_baru_pusat = np.dot(matriks_rotasi, titik_pusat.T).T
    titik_baru = titik_baru_pusat + pusat
    return titik_baru

def refleksi(titik, sumbu):
    """Melakukan refleksi titik terhadap sumbu x, y, atau garis y=x, y=-x"""
    x, y = titik
    if sumbu == 'sumbu X':
        return np.array([x, -y])
    elif sumbu == 'sumbu Y':
        return np.array([-x, y])
    elif sumbu == 'y = x':
        return np.array([y, x])
    elif sumbu == 'y = -x':
        return np.array([-y, -x])
    else:
        return titik

def dilatasi(titik, faktor_skala, pusat=np.array([0, 0])):
    """Melakukan dilatasi titik terhadap pusat (default 0,0)"""
    # Translasi titik ke pusat, dilatasi, lalu translasi kembali
    titik_pusat = titik - pusat
    titik_baru_pusat = titik_pusat * faktor_skala
    titik_baru = titik_baru_pusat + pusat
    return titik_baru

# --- 2. Fungsi Plotting ---

def plot_transformasi(titik_awal, titik_akhir, judul):
    """Membuat plot visualisasi transformasi"""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Pastikan batasan plot cukup besar
    all_points = np.vstack([titik_awal, titik_akhir])
    min_val = np.min(all_points) - 2
    max_val = np.max(all_points) + 2
    
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    
    # Gambar sumbu X dan Y
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(color='lightgray', linestyle='--', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    
    # Plot titik awal (merah)
    ax.plot(titik_awal[0], titik_awal[1], 'ro', label='Titik Awal')
    # Plot titik akhir (biru)
    ax.plot(titik_akhir[0], titik_akhir[1], 'bo', label='Titik Akhir')
    
    # Beri label koordinat
    ax.text(titik_awal[0], titik_awal[1] + 0.5, f'A({titik_awal[0]}, {titik_awal[1]})', color='red')
    ax.text(titik_akhir[0], titik_akhir[1] + 0.5, f'A\'({titik_akhir[0]}, {titik_akhir[1]})', color='blue')
    
    ax.set_title(judul)
    ax.legend()
    st.pyplot(fig)

# --- 3. UI Streamlit ---

st.set_page_config(page_title="Virtual Lab Transformasi Geometri", layout="wide")

st.title("🔬 Virtual Lab Transformasi Geometri")
st.markdown("Eksplorasi interaktif **Translasi**, **Rotasi**, **Refleksi**, dan **Dilatasi**.")

st.sidebar.header("🔧 Pengaturan Titik & Transformasi")

# Input Titik Awal
st.sidebar.subheader("Titik Awal A(x, y)")
x_awal = st.sidebar.number_input("Koordinat X:", value=2, step=1)
y_awal = st.sidebar.number_input("Koordinat Y:", value=3, step=1)
titik_awal = np.array([x_awal, y_awal])

# Pilih Jenis Transformasi
operasi = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ['Translasi', 'Rotasi', 'Refleksi', 'Dilatasi']
)

# Inisialisasi titik_akhir
titik_akhir = titik_awal
judul_plot = f"Visualisasi Transformasi: {operasi}"

# Logika Kontrol Berdasarkan Pilihan
if operasi == 'Translasi':
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parameter Translasi (Vektor T)")
    tx = st.sidebar.slider("Pergeseran X (Tx)", -10, 10, 2)
    ty = st.sidebar.slider("Pergeseran Y (Ty)", -10, 10, -1)
    vektor_t = np.array([tx, ty])
    titik_akhir = translasi(titik_awal, vektor_t)
    judul_plot += f"\n$T = ({tx}, {ty})$"
    st.sidebar.info(f"Rumus: $A'(x', y') = A(x+T_x, y+T_y)$")

elif operasi == 'Rotasi':
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parameter Rotasi")
    sudut = st.sidebar.slider("Sudut Rotasi (derajat)", -360, 360, 90, 5)
    pusat_x = st.sidebar.number_input("Pusat Rotasi X", value=0, step=1)
    pusat_y = st.sidebar.number_input("Pusat Rotasi Y", value=0, step=1)
    pusat = np.array([pusat_x, pusat_y])
    titik_akhir = rotasi(titik_awal, sudut, pusat)
    judul_plot += f"\n{sudut}° terhadap Pusat $P({pusat_x}, {pusat_y})$"
    st.sidebar.info(f"Rotasi menggunakan matriks: Matriks Rotasi $\\times$ Titik")

elif operasi == 'Refleksi':
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parameter Refleksi")
    sumbu_refleksi = st.sidebar.selectbox(
        "Pilih Sumbu/Garis Refleksi",
        ['sumbu X', 'sumbu Y', 'y = x', 'y = -x']
    )
    titik_akhir = refleksi(titik_awal, sumbu_refleksi)
    judul_plot += f"\nTerhadap Garis: {sumbu_refleksi}"
    
    rumus = ""
    if sumbu_refleksi == 'sumbu X':
        rumus = "$A'(x', y') = A(x, -y)$"
    elif sumbu_refleksi == 'sumbu Y':
        rumus = "$A'(x', y') = A(-x, y)$"
    elif sumbu_refleksi == 'y = x':
        rumus = "$A'(x', y') = A(y, x)$"
    elif sumbu_refleksi == 'y = -x':
        rumus = "$A'(x', y') = A(-y, -x)$"
    st.sidebar.info(f"Rumus: {rumus}")


elif operasi == 'Dilatasi':
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parameter Dilatasi")
    faktor_k = st.sidebar.slider("Faktor Skala (k)", -3.0, 3.0, 1.5, 0.1)
    pusat_x = st.sidebar.number_input("Pusat Dilatasi X", value=0, step=1)
    pusat_y = st.sidebar.number_input("Pusat Dilatasi Y", value=0, step=1)
    pusat = np.array([pusat_x, pusat_y])
    titik_akhir = dilatasi(titik_awal, faktor_k, pusat)
    judul_plot += f"\n$k = {faktor_k}$ terhadap Pusat $P({pusat_x}, {pusat_y})$"
    st.sidebar.info(f"Rumus terhadap $P(0,0)$: $A'(x', y') = A(kx, ky)$")

# --- 4. Tampilkan Hasil ---

col1, col2 = st.columns([2, 1])

with col1:
    plot_transformasi(titik_awal, titik_akhir, judul_plot)
    

with col2:
    st.subheader("📝 Hasil Perhitungan")
    st.markdown(f"**Titik Awal $A$:** $({titik_awal[0]}, {titik_awal[1]})$")
    st.markdown(f"**Transformasi:** **{operasi}**")
    st.markdown(f"**Titik Akhir $A'$:** $({titik_akhir[0]:.2f}, {titik_akhir[1]:.2f})$")

    st.markdown("---")
    st.subheader("💡 Konsep Dasar")
    if operasi == 'Translasi':
        st.write("Translasi adalah pergeseran setiap titik sejauh dan searah yang sama.")
    elif operasi == 'Rotasi':
        st.write("Rotasi adalah perputaran setiap titik pada bidang datar mengelilingi titik pusat tertentu.")
    elif operasi == 'Refleksi':
        st.write("Refleksi (pencerminan) adalah transformasi yang memindahkan setiap titik pada bidang datar ke bayangan cerminnya.")
    elif operasi == 'Dilatasi':
        st.write("Dilatasi (perkalian) adalah transformasi yang mengubah ukuran, memperbesar atau memperkecil, suatu bangun tetapi tidak mengubah bentuknya.")

st.markdown("---")
st.caption("Dibuat dengan Python dan Streamlit. Siswa dapat mencoba berbagai input untuk memvisualisasikan bagaimana koordinat berubah.")
