import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, diff, Abs, Pow, sqrt, sin, cos, tan, log, exp, lambdify

# --- 1. Fungsi Analisis ---

# Define symbols outside of the function to be globally accessible for SymPy
x = symbols('x')

@st.cache_data
def analisis_fungsi(f_expr, var_x):
    """Menganalisis sifat fungsi (Ganjil/Genap) dan monotonisitas."""
    
    # Inisialisasi Hasil
    hasil = {}

    # 1. Analisis Sifat Ganjil / Genap (f(-x) vs f(x))
    try:
        f_neg_x = f_expr.subs(var_x, -var_x)
        
        if f_neg_x.equals(f_expr):
            hasil['sifat'] = "Genap (Even)"
            hasil['deskripsi_sifat'] = "Fungsi Genap: Grafik simetris terhadap sumbu Y. $f(-x) = f(x)$"
        elif f_neg_x.equals(-f_expr):
            hasil['sifat'] = "Ganjil (Odd)"
            hasil['deskripsi_sifat'] = "Fungsi Ganjil: Grafik simetris terhadap titik asal (0,0). $f(-x) = -f(x)$"
        else:
            hasil['sifat'] = "Bukan Ganjil & Bukan Genap (Neither)"
            hasil['deskripsi_sifat'] = "Grafik tidak simetris terhadap sumbu Y maupun titik asal."
            
    except Exception as e:
        hasil['sifat'] = "Analisis Sifat Gagal"
        hasil['deskripsi_sifat'] = f"Error saat analisis sifat: {e}"

    # 2. Analisis Monotonisitas (Turunan Pertama)
    try:
        f_prime = diff(f_expr, var_x)
        hasil['turunan'] = str(f_prime)
    except Exception:
        hasil['turunan'] = "Gagal menghitung turunan."

    return hasil

# --- 2. Fungsi Plotting ---

def plot_fungsi(f_expr, var_x, rentang):
    """Membuat plot visualisasi fungsi."""
    
    # Menggunakan lambdify untuk konversi SymPy ke fungsi numerik (numpy) yang cepat
    f_lambdified = lambdify(var_x, f_expr, 'numpy')
    
    # Buat rentang x
    x_vals = np.linspace(rentang[0], rentang[1], 500)
    
    # Hitung y (penanganan error: try-except untuk domain/error runtime)
    try:
        # Gunakan np.errstate untuk menekan peringatan (misalnya pembagian dengan nol)
        with np.errstate(divide='ignore', invalid='ignore'):
            y_vals = f_lambdified(x_vals)
            
        # Ganti nilai tak hingga (inf) dan nilai non-numerik (nan) dengan NaN agar plot tidak rusak
        y_vals[np.isinf(y_vals) | np.isnan(y_vals)] = np.nan
        
    except Exception:
        y_vals = np.full_like(x_vals, np.nan) # Jika gagal total, gunakan NaN
        st.warning("Gagal menghitung nilai fungsi untuk plotting.")


    # 4. Buat Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Penentuan Batas Plot Y (menghindari outlier)
    # Filter out NaN values before calculating quantiles
    valid_y = y_vals[~np.isnan(y_vals)]
    
    if len(valid_y) > 0:
        Q1 = np.quantile(valid_y, 0.25)
        Q3 = np.quantile(valid_y, 0.75)
        IQR = Q3 - Q1
        y_min_plot = Q1 - 2.5 * IQR # Menggunakan 2.5 IQR untuk rentang yang sedikit lebih lebar
        y_max_plot = Q3 + 2.5 * IQR
    else:
         y_min_plot = -10
         y_max_plot = 10
    
    ax.plot(x_vals, y_vals, label=f"${f_expr}$", color='blue')
    
    # Gambar sumbu X dan Y
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(color='lightgray', linestyle='--', linewidth=0.5)
    
    ax.set_title(f"Grafik Fungsi $f(x) = {f_expr}$")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_ylim(y_min_plot, y_max_plot) # Terapkan batas y
    ax.legend()
    st.pyplot(fig)
    

[Image of a Cartesian graph showing a plotted curve representing a mathematical function, demonstrating its shape, intercepts, and slope.]



# --- 3. UI Streamlit ---

st.set_page_config(page_title="Virtual Lab Analisis Fungsi", layout="wide")

st.title("🔬 Virtual Lab: Analisis Fungsi Matematika")
st.markdown("Eksplorasi **Nilai Fungsi**, **Sifat Ganjil/Genap**, dan **Monotonisitas (Increasing/Decreasing)** dari berbagai fungsi.")

# --- SIDEBAR (Interaksi Utama) ---
st.sidebar.header("🛠️ Input Fungsi & Pengaturan")

# Input Fungsi
f_str = st.sidebar.text_input(
    "Masukkan Fungsi $f(x)$: (Gunakan 'x' sebagai variabel. Contoh: x**3 - 3*x + 1, sin(x), 1/x)", 
    value="x**2 - 4"
)

# Rentang Plot
st.sidebar.subheader("Rentang Plot (Domain x)")
x_min = st.sidebar.slider("x Minimum", -20, 0, -5)
x_max = st.sidebar.slider("x Maksimum", 0, 20, 5)

# Input Nilai Fungsi
st.sidebar.subheader("Hitung Nilai Fungsi")
x_value = st.sidebar.number_input("Masukkan nilai $x$ (untuk mencari $f(x)$)", value=2.0)

# --- Proses Analisis Simbolis SymPy ---
try:
    # Mengizinkan fungsi matematika umum SymPy
    f_expr = sympify(f_str, locals={'sin':sin, 'cos':cos, 'tan':tan, 'log':log, 'exp':exp, 'Abs':Abs, 'sqrt':sqrt})
    valid_function = True
except Exception as e:
    valid_function = False
    st.error(f"Input fungsi tidak valid. Pastikan format penulisan benar (misal: x**2, bukan x^2). Error: {e}")


# --- TAMPILAN UTAMA ---

if valid_function:
    
    col1, col2 = st.columns([1, 1])

    # Kiri: Grafik
    with col1:
        st.subheader("🖼️ Grafik Fungsi")
        plot_fungsi(f_expr, x, (x_min, x_max))
        st.caption(f"Fungsi yang diplot: $f(x) = {f_expr}$")

    # Kanan: Hasil Anal
