import streamlit as st
import numpy as np
import pandas as pd # Menggunakan pandas untuk tampilan data yang lebih rapi

# --- 1. Fungsi Perhitungan ---

def hitung_diskon_persentase(harga_awal, diskon_persen):
    """Menghitung nilai diskon dan harga setelah diskon."""
    nilai_diskon = harga_awal * (diskon_persen / 100)
    harga_akhir = harga_awal - nilai_diskon
    return nilai_diskon, harga_akhir

def hitung_bunga_sederhana(pokok, suku_bunga_tahunan, waktu_tahun):
    """Menghitung bunga dan total pengembalian (Misal: Pinjaman Modal)."""
    bunga = pokok * (suku_bunga_tahunan / 100) * waktu_tahun
    total_bayar = pokok + bunga
    return bunga, total_bayar

# --- 2. UI Streamlit ---

st.set_page_config(page_title="Virtual Lab Aritmetika Bisnis Ternak", layout="wide")

st.title("💰 Virtual Lab: Aritmetika Dasar Bisnis Hewan Ternak")
st.markdown("Eksplorasi perhitungan **Persentase**, **Diskon**, **Suku Bunga**, dan **Perbandingan Harga** dalam konteks penjualan hewan ternak.")

# --- SIDEBAR (Interaksi Utama) ---
st.sidebar.header("🛠️ Input Data Penjualan & Modal")

# Data Harga Satuan (untuk perbandingan)
data_harga = {
    'Sapi Qurban': 20_000_000,
    'Kambing Etawa': 3_500_000,
    'Ayam Petelur': 50_000,
    'Kuda Poni': 15_000_000
}

# Pilihan Skenario
skenario = st.sidebar.selectbox(
    "Pilih Skenario Perhitungan:",
    ['1. Perhitungan Diskon & Persentase', '2. Perbandingan Harga Per Unit (Value)', '3. Perhitungan Bunga Modal']
)

# --- 4. TAMPILAN UTAMA BERDASARKAN SKENARIO ---

st.markdown("---")

if skenario == '1. Perhitungan Diskon & Persentase':
    
    st.header("1️⃣ Diskon Penjualan dan Persentase Laba/Rugi")
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.subheader("Input Transaksi")
        jenis_hewan = st.selectbox("Jenis Hewan", list(data_harga.keys()))
        harga_jual_awal = st.number_input("Harga Jual Awal (Rp)", min_value=1000, value=data_harga[jenis_hewan], step=10000)
        diskon_persen = st.slider("Persentase Diskon (%)", 0.0, 50.0, 10.0, step=0.5)
        harga_modal = st.number_input("Harga Beli/Modal (Rp)", min_value=1000, value=int(harga_jual_awal * 0.8), step=10000)

    # Lakukan Perhitungan
    nilai_diskon, harga_akhir = hitung_diskon_persentase(harga_jual_awal, diskon_persen)
    
    laba_rugi_nominal = harga_akhir - harga_modal
    laba_rugi_persen = (laba_rugi_nominal / harga_modal) * 100 if harga_modal != 0 else 0

    with col_output:
        st.subheader("Hasil Perhitungan")
        
        # Diskon
        st.metric(
            label=f"Harga Setelah Diskon ({diskon_persen:.1f}%)",
            value=f"Rp {harga_akhir:,.0f}",
            delta=f"-Rp {nilai_diskon:,.0f} (Diskon)"
        )
        
        # Laba/Rugi
        status = "Laba" if laba_rugi_nominal > 0 else "Rugi" if laba_rugi_nominal < 0 else "Impás (Break Even)"
        st.metric(
            label=f"Laba / Rugi",
            value=f"Rp {laba_rugi_nominal:,.0f}",
            delta=f"{laba_rugi_persen:+.2f}% ({status})",
            delta_color="normal" if laba_rugi_nominal >= 0 else "inverse"
        )
        st.markdown("---")
        st.info(f"**Konsep:** Diskon mengurangi harga jual. Laba/Rugi dihitung dari Harga Jual Akhir dikurangi Harga Modal. Persentase laba/rugi dihitung terhadap Harga Modal.")

elif skenario == '2. Perbandingan Harga Per Unit (Value)':
    
    st.header("2️⃣ Perbandingan Harga Per Unit")
    st.markdown("Skenario ini membantu peternak membandingkan *nilai* (harga per unit berat) dari berbagai komoditas atau paket penjualan.")
    
    # Input Data Perbandingan
    st.subheader("Input Harga & Satuan")
    
    # Hewan 1
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Produk A (Misal: Sapi)")
        nama_a = st.text_input("Nama Produk A", value="Sapi Jumbo 500kg")
        harga_a = st.number_input("Harga Jual A (Rp)", min_value=1000, value=25_000_000, key='harga_a')
        unit_a = st.number_input("Unit (Misal: Kg Berat Hidup)", min_value=1.0, value=500.0, step=1.0, key='unit_a')
        
    # Hewan 2
    with col_b:
        st.markdown("#### Produk B (Misal: Kambing)")
        nama_b = st.text_input("Nama Produk B", value="Paket 5 Ekor Kambing")
        harga_b = st.number_input("Harga Jual B (Rp)", min_value=1000, value=18_000_000, key='harga_b')
        unit_b = st.number_input("Unit (Misal: Jumlah Ekor)", min_value=1.0, value=5.0, step=1.0, key='unit_b')

    # Perhitungan Perbandingan
    harga_per_unit_a = harga_a / unit_a
    harga_per_unit_b = harga_b / unit_b
    
    df_perbandingan = pd.DataFrame({
        'Produk': [nama_a, nama_b],
        'Harga Jual': [f"Rp {harga_a:,.0f}", f"Rp {harga_b:,.0f}"],
        'Unit': [f"{unit_a:,.1f}", f"{unit_b:,.1f}"],
        'Harga per Unit (Nilai)': [f"Rp {harga_per_unit_a:,.0f}", f"Rp {harga_per_unit_b:,.0f}"]
    })
    
    st.markdown("---")
    st.subheader("Tabel Perbandingan Nilai")
    st.dataframe(df_perbandingan, hide_index=True, use_container_width=True)
    
    if harga_per_unit_a < harga_per_unit_b:
        pilihan_terbaik = nama_a
    elif harga_per_unit_b < harga_per_unit_a:
        pilihan_terbaik = nama_b
    else:
        pilihan_terbaik = "Keduanya memiliki nilai per unit yang sama."
        
    st.success(f"**Kesimpulan Nilai:** Berdasarkan harga per unit, **{pilihan_terbaik}** menawarkan nilai yang lebih baik (harga per unit lebih rendah).")
    st.info("Konsep: Harga per unit (value) membantu menentukan produk mana yang paling efisien dari sisi biaya per satuan.")

elif skenario == '3. Perhitungan Bunga Modal':
    
    st.header("3️⃣ Perhitungan Bunga Modal (Suku Bunga Sederhana)")
    st.markdown("Skenario ini mensimulasikan perhitungan bunga pinjaman modal usaha atau simpanan sederhana.")
    
    col_input_bunga, col_output_bunga = st.columns(2)
    
    with col_input_bunga:
        st.subheader("Input Pinjaman Modal")
        pokok_pinjaman = st.number_input("Pokok Pinjaman Modal (Rp)", min_value=100000, value=50_000_000, step=100000)
        suku_bunga_tahunan = st.slider("Suku Bunga Tahunan (%)", 1.0, 30.0, 10.0, step=0.5)
        waktu_tahun = st.slider("Jangka Waktu (Tahun)", 1.0, 5.0, 1.0, step=0.5)
        
    # Lakukan Perhitungan Bunga
    bunga, total_bayar = hitung_bunga_sederhana(pokok_pinjaman, suku_bunga_tahunan, waktu_tahun)
    
    with col_output_bunga:
        st.subheader("Hasil Perhitungan Bunga")
        
        st.metric(label="Pokok Pinjaman", value=f"Rp {pokok_pinjaman:,.0f}")
        st.metric(
            label="Total Bunga yang Dibayar",
            value=f"Rp {bunga:,.0f}",
            delta=f"{suku_bunga_tahunan}% per tahun"
        )
        st.metric(
            label="Total Pengembalian (Pokok + Bunga)",
            value=f"Rp {total_bayar:,.0f}"
        )
        st.markdown("---")
        st.info(f"**Rumus:** Bunga = Pokok $\\times$ Suku Bunga $\\times$ Waktu. Ini adalah perhitungan bunga sederhana (tanpa majemuk).")
        
st.markdown("---")
st.caption("Dibuat dengan Python dan Streamlit. Aplikasi ini adalah alat bantu edukasi, bukan penasihat keuangan.")
