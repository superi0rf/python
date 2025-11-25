import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Fungsi Perhitungan Volume dan Luas Permukaan ---

# Kubus
def hitung_kubus(s):
    volume = s ** 3
    luas_permukaan = 6 * (s ** 2)
    return volume, luas_permukaan

# Balok
def hitung_balok(p, l, t):
    volume = p * l * t
    luas_permukaan = 2 * (p*l + p*t + l*t)
    return volume, luas_permukaan

# Tabung
def hitung_tabung(r, t):
    phi = np.pi
    volume = phi * (r ** 2) * t
    luas_permukaan = 2 * phi * r * (r + t)
    return volume, luas_permukaan

# Bola
def hitung_bola(r):
    phi = np.pi
    volume = (4/3) * phi * (r ** 3)
    luas_permukaan = 4 * phi * (r ** 2)
    return volume, luas_permukaan

# Kerucut
def hitung_kerucut(r, t):
    phi = np.pi
    # Hitung garis pelukis (s) menggunakan Pythagoras
    s = np.sqrt(r**2 + t**2)
    volume = (1/3) * phi * (r ** 2) * t
    luas_permukaan = phi * r * (r + s)
    return volume, luas_permukaan

# --- 2. Fungsi Visualisasi (Dihapus/Disederhanakan) ---
# Fungsi plot_bangun_ruang dihapus karena visualisasi 3D yang kompleks
# lebih baik digantikan dengan st.image (seperti yang sudah Anda lakukan di sidebar).

# --- 3. UI Streamlit ---

st.set_page_config(page_title="Virtual Lab Geometri Bangun Ruang", layout="wide")

st.title("⚗️ Virtual Lab Geometri: Volume & Luas Permukaan")
st.markdown("Interaktif menghitung **Volume** dan **Luas Permukaan** berbagai bangun ruang dengan mengubah dimensinya.")

# --- SIDEBAR (Interaksi Utama) ---
st.sidebar.header("🔧 Pengaturan Bangun Ruang")

# Pilihan Bangun Ruang
bangun_ruang = st.sidebar.selectbox(
    "Pilih Bangun Ruang:",
    ['Kubus', 'Balok', 'Tabung', 'Bola', 'Kerucut']
)

# Area untuk input dimensi
st.sidebar.markdown("---")
st.sidebar.subheader(f"Input Dimensi {bangun_ruang}")

volume = 0
luas_permukaan = 0
image_url = "" # Variabel untuk menyimpan URL gambar
dimensi_detail = "" # Variabel untuk detail dimensi

# Logika Input Berdasarkan Pilihan
if bangun_ruang == 'Kubus':
    s = st.sidebar.number_input("Sisi (s) [cm]", min_value=1.0, value=5.0, step=0.5)
    volume, luas_permukaan = hitung_kubus(s)
    st.sidebar.markdown(f"**Rumus Volume:** $V = s^3$")
    st.sidebar.markdown(f"**Rumus Luas Permukaan:** $LP = 6 \\times s^2$")
    image_url = "https://i.imgur.com/g8oH7vO.png"
    dimensi_detail = f"Bangun ruang dengan 6 sisi berbentuk persegi yang sama besar, setiap rusuk berukuran **{s} cm**."

elif bangun_ruang == 'Balok':
    p = st.sidebar.number_input("Panjang (p) [cm]", min_value=1.0, value=6.0, step=0.5)
    l = st.sidebar.number_input("Lebar (l) [cm]", min_value=1.0, value=4.0, step=0.5)
    t = st.sidebar.number_input("Tinggi (t) [cm]", min_value=1.0, value=3.0, step=0.5)
    volume, luas_permukaan = hitung_balok(p, l, t)
    st.sidebar.markdown(f"**Rumus Volume:** $V = p \\times l \\times t$")
    st.sidebar.markdown(f"**Rumus Luas Permukaan:** $LP = 2(pl + pt + lt)$")
    image_url = "https://i.imgur.com/v8tT7wW.png"
    dimensi_detail = f"Bangun ruang dengan panjang **{p} cm**, lebar **{l} cm**, dan tinggi **{t} cm**."

elif bangun_ruang == 'Tabung':
    r = st.sidebar.number_input("Jari-jari (r) [cm]", min_value=0.1, value=4.0, step=0.5)
    t = st.sidebar.number_input("Tinggi (t) [cm]", min_value=0.1, value=10.0, step=0.5)
    volume, luas_permukaan = hitung_tabung(r, t)
    st.sidebar.markdown(f"**Rumus Volume:** $V = \\pi r^2 t$")
    st.sidebar.markdown(f"**Rumus Luas Permukaan:** $LP = 2\\pi r(r + t)$")
    image_url = "https://i.imgur.com/8N4X0C1.png"
    dimensi_detail = f"Bangun ruang dengan alas lingkaran berjari-jari **{r} cm** dan tinggi **{t} cm**."
    
elif bangun_ruang == 'Bola':
    r = st.sidebar.number_input("Jari-jari (r) [cm]", min_value=0.1, value=5.0, step=0.5)
    volume, luas_permukaan = hitung_bola(r)
    st.sidebar.markdown(f"**Rumus Volume:** $V = \\frac{4}{3} \\pi r^3$")
    st.sidebar.markdown(f"**Rumus Luas Permukaan:** $LP = 4 \\pi r^2$")
    image_url = "https://i.imgur.com/Q2y1v8e.png"
    dimensi_detail = f"Bangun ruang berbentuk bulat sempurna dengan jari-jari **{r} cm**."
    
elif bangun_ruang == 'Kerucut':
    r = st.sidebar.number_input("Jari-jari (r) [cm]", min_value=0.1, value=3.0, step=0.5)
    t = st.sidebar.number_input("Tinggi (t) [cm]", min_value=0.1, value=4.0, step=0.5)
    s = np.sqrt(r**2 + t**2)
    volume, luas_permukaan = hitung_kerucut(r, t)
    st.sidebar.markdown(f"**Rumus Volume:** $V = \\frac{1}{3} \\pi r^2 t$")
    st.sidebar.markdown(f"**Rumus Luas Permukaan:** $LP = \\pi r(r + s)$")
    st.sidebar.markdown(f"*Garis Pelukis (s) = {s:.2f} cm*")
    image_url = "https://i.imgur.com/c6FjH5G.png"
    dimensi_detail = f"Bangun ruang dengan alas lingkaran berjari-jari **{r} cm** dan tinggi tegak **{t} cm**."

# Tampilkan gambar di sidebar setelah semua input dimensi
if image_url:
    st.sidebar.markdown("---")
    st.sidebar.image(image_url, caption=bangun_ruang)
    
# --- TAMPILAN UTAMA (Hasil & Visualisasi) ---

st.header(f"Hasil Perhitungan untuk **{bangun_ruang}**")

# Kolom untuk pemisahan konten
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Hasil Perhitungan")
    st.markdown(f"**Volume ($V$):**")
    st.success(f"## {volume:,.2f} cm³")
    
    st.markdown(f"**Luas Permukaan ($LP$):**")
    st.info(f"## {luas_permukaan:,.2f} cm²")
    
    st.markdown("---")
    st.subheader("📝 Catatan Edukasi")
    st.write(f"Siswa dapat memahami bahwa perubahan pada satu dimensi (misalnya jari-jari atau tinggi) akan sangat mempengaruhi **Volume** maupun **Luas Permukaan**.")
    if bangun_ruang in ['Tabung', 'Kerucut', 'Bola']:
         st.markdown("Perhitungan melibatkan nilai **$\pi \\approx 3.14159$**.")

with col2:
    st.subheader("🖼️ Ilustrasi Bangun Ruang")
    # Tampilkan gambar di main area juga agar siswa bisa fokus ke ilustrasi sambil melihat hasil
    if image_url:
        st.image(image_url, caption=f"Skema {bangun_ruang}")
    
    st.markdown("---")
    st.subheader("Detail Dimensi")
    st.markdown(dimensi_detail)

st.markdown("---")
st.caption("Dibuat dengan Python dan Streamlit. Nilai dihitung secara real-time berdasarkan input dimensi.")
