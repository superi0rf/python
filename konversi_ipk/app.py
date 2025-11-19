import streamlit as st

# Mengatur judul halaman aplikasi
st.title("Aplikasi Konversi Nilai Angka ke Huruf")
st.write("Masukkan nilai angka (0-100) untuk mendapatkan nilai huruf Anda.")

# Input angka menggunakan st.number_input
# min_value=0.0, max_value=100.0 untuk membatasi input
# format="%.2f" untuk menampilkan dua desimal, jika diperlukan
nilai = st.number_input(
    "Masukkan Nilai Anda:",
    min_value=0.0,
    max_value=100.0,
    step=0.01, # Opsional: memungkinkan input desimal
    value=50.0 # Nilai default awal
)

# Tombol untuk memicu kalkulasi
if st.button("Cek Nilai"):
    # Logika Cek Nilai
    
    # Cek nilai tidak valid (di luar rentang 0-100)
    # Catatan: st.number_input sudah membatasi rentang,
    # tapi cek ini tetap berguna jika batasan input diubah
    if nilai > 100 or nilai < 0:
        hasil = "Nilai Anda **tidak valid** (di luar rentang 0-100)"
    
    # Cek Nilai A (85-100)
    elif nilai >= 85:
        hasil = "Nilai Anda: **A** (Sangat Baik)"
    
    # Cek Nilai B (70-84.99...)
    elif nilai >= 70:
        hasil = "Nilai Anda: **B** (Baik)"
    
    # Cek Nilai C (55-69.99...)
    elif nilai >= 55:
        hasil = "Nilai Anda: **C** (Cukup)"
    
    # Cek Nilai D (40-54.99...)
    elif nilai >= 40:
        hasil = "Nilai Anda: **D** (Kurang)"
    
    # Sisanya adalah Nilai E (0-39.99...)
    else:
        hasil = "Nilai Anda: **E** (Gagal)"
    
    # Menampilkan hasil
    st.markdown(f"## Hasil: {hasil}")