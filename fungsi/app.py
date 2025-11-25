import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, diff, Abs, Pow, sqrt, sin, cos, tan, log, exp, lambdify

# --- 1. Fungsi Analisis & Data ---

# Define symbols outside of the function to be globally accessible for SymPy
x = symbols('x')

@st.cache_data
def analisis_fungsi(f_expr, var_x):
    """Menganalisis sifat fungsi (Ganjil/Genap) dan monotonisitas."""
    
    hasil = {}
    
    # 1. Analisis Sifat Ganjil / Genap
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

@st.cache_data
def generate_plot_data(f_expr, var_x, rentang_min, rentang_max):
    """Menghasilkan data numerik (x, y) untuk plotting. Fungsi ini di-cache."""
    
    f_lambdified = lambdify(var_x, f_expr, 'numpy')
    x_vals = np.linspace(rentang_min, rentang_max, 500)
    
    try:
        with np.errstate(divide='ignore', invalid='ignore'):
            y_vals = f_lambdified(x_vals)
            
        y_vals[np.isinf(y_vals) | np.isnan(y_vals)] = np.nan
        
        # Penentuan Batas Plot Y (IQR untuk menghindari outlier)
        valid_y = y_vals[~np.isnan(y_vals)]
        
        if len(valid_y) > 0:
            Q1 = np.quantile(valid_y, 0.25)
            Q3 = np.quantile(valid_y, 0.75)
            IQR = Q3 - Q1
            y_min_plot = Q1 - 2.5 * IQR
            y_max_plot = Q3 + 2.5 * IQR
        else:
             y_min_plot = -10
             y_max_plot = 10
             
        return x_vals, y_vals, y_min_plot, y_max_plot
        
    except Exception:
        # Jika gagal total, kembalikan nilai default/NaN
        return np.full(500, np.nan), np.full(500, np.nan), -10, 10 

# --- 2. Fungsi Plotting ---

def plot_fungsi(f_expr, var_x, rentang):
    """Membuat plot visualisasi fungsi."""
    
    # Memanggil fungsi cache untuk mendapatkan data plot
    x_vals, y_vals, y_min_plot, y_max_plot = generate_plot_data(f_expr, var_x, rentang[0], rentang[1])
    
    if np.all(np.isnan(y_vals)):
        st.warning("Gagal menghitung nilai fungsi untuk plotting dalam rentang ini.")
        
    # 4. Buat Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
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



# ---------------------------------------------------------------------
## 🧠 UI Streamlit Utama
# ---------------------------------------------------------------------

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

    # Kanan: Hasil Analisis
    with col2:
        st.subheader("📊 Hasil Analisis")
        
        # 1. Hitung Nilai Fungsi
        try:
            f_at_x = f_expr.subs(x, x_value)
            st.metric(
                label=f"Nilai Fungsi $f({x_value})$",
                value=f"{f_at_x.evalf():.4f}"
            )
        except Exception:
            st.warning(f"Gagal menghitung $f({x_value})$ (mungkin di luar domain atau nilai tak hingga).")

        st.markdown("---")
        
        # 2. Analisis Sifat (Ganjil/Genap & Monotonisitas)
        analisis = analisis_fungsi(f_expr, x)
        
        st.subheader("⭐ Sifat Fungsi (Ganjil/Genap)")
        st.info(f"**{analisis.get('sifat')}**")
        st.markdown(analisis.get('deskripsi_sifat'))
        
        st.subheader("📈 Analisis Monotonisitas")
        st.code(f"f'(x) = {analisis.get('turunan')}", language='latex')
        st.markdown("""
        * **Increasing** (Naik): Jika $f'(x) > 0$.
        * **Decreasing** (Turun): Jika $f'(x) < 0$.
        * **Konstan/Titik Kritis:** Jika $f'(x) = 0$.
        """)
        st.warning("Analisis monotonisitas memerlukan evaluasi $f'(x)$ pada interval. Gunakan turunan di atas dan grafik di samping untuk menentukan interval fungsi naik atau turun.")
    
st.markdown("---")
st.caption("Dibuat dengan Python (SymPy dan Streamlit). Alat ini membantu memvisualisasikan sifat-sifat fungsi secara instan.")
