import streamlit as st

def urutkan_tiga_bilangan(a: float, b: float, c: float):
    return sorted([a, b, c])

st.title("Pengurutan Tiga Bilangan")

a = st.number_input("Masukkan bilangan pertama:", step=1.0)
b = st.number_input("Masukkan bilangan kedua:", step=1.0)
c = st.number_input("Masukkan bilangan ketiga:", step=1.0)

if st.button("Urutkan"):
    hasil = urutkan_tiga_bilangan(a, b, c)
    st.success(f"Urutan dari yang terkecil: {hasil[0]}, {hasil[1]}, {hasil[2]}")
