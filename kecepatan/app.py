import streamlit as st

def hitung_kecepatan(jarak_km: float, waktu_jam: float) -> float:
    """Menghitung kecepatan rata-rata (km/jam)."""
    if jarak_km < 0:
        raise ValueError("Jarak tidak boleh negatif.")
    if waktu_jam <= 0:
        raise ValueError("Waktu harus lebih besar dari nol.")
    return jarak_km / waktu_jam

st.title("Kalkulator Kecepatan Rata-rata")

jarak = st.number_input("Masukkan jarak tempuh (km):", min_value=0.0, step=1.0)
waktu = st.number_input("Masukkan waktu tempuh (jam):", min_value=0.0, step=0.1)

if st.button("Hitung Kecepatan"):
    try:
        hasil = hitung_kecepatan(jarak, waktu)
        st.success(f"Kecepatan rata-rata: {hasil:.2f} km/jam")
    except ValueError as e:
        st.error(str(e))
