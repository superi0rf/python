import streamlit as st

def luas_persegi(sisi: float) -> float:
    if sisi < 0:
        raise ValueError("Sisi tidak boleh negatif.")
    return sisi * sisi

st.title("Kalkulator Luas Persegi")

s = st.number_input("Masukkan panjang sisi:", min_value=0.0, step=1.0)

if st.button("Hitung"):
    try:
        hasil = luas_persegi(s)
        st.success(f"Luas persegi = {hasil}")
    except ValueError as e:
        st.error(str(e))
