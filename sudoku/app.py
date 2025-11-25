import streamlit as st
import numpy as np

# --- 1. Logika Sudoku ---

def is_valid_move(board, row, col, num):
    """Memeriksa apakah angka 'num' valid di posisi (row, col) berdasarkan aturan Sudoku."""
    
    # Cek Baris
    if num in board[row]:
        return False
    
    # Cek Kolom
    if num in board[:, col]:
        return False
        
    # Cek Kotak 3x3
    start_row = row - row % 3
    start_col = col - col % 3
    
    for i in range(3):
        for j in range(3):
            if board[start_row + i, start_col + j] == num:
                return False
                
    return True

def generate_sudoku(difficulty=30):
    """
    Membuat papan Sudoku yang sudah terpecahkan dan kemudian menghapus
    sejumlah angka (berdasarkan kesulitan) untuk membuat soal.
    """
    # 1. Buat papan kosong
    board = np.zeros((9, 9), dtype=int)
    
    # 2. Isi papan secara rekursif (hanya menginisialisasi beberapa sel awal)
    def solve_board(b):
        """Fungsi rekursif untuk menyelesaikan papan"""
        for i in range(9):
            for j in range(9):
                if b[i, j] == 0:
                    for num in np.random.permutation(np.arange(1, 10)):
                        if is_valid_move(b, i, j, num):
                            b[i, j] = num
                            if solve_board(b):
                                return True
                            b[i, j] = 0  # Backtrack
                    return False
        return True
    
    # Inisialisasi sudut kiri atas agar selalu terpecahkan
    for i in range(3):
        for j in range(3):
            board[i, j] = (i * 3 + j) % 9 + 1
            
    solve_board(board)
    
    # Simpan solusi lengkap
    solution = np.copy(board)
    
    # 3. Hapus angka untuk membuat soal
    cells_to_remove = 81 - difficulty # difficulty adalah jumlah sel yang terisi
    
    for _ in range(cells_to_remove):
        row, col = np.random.randint(0, 9, 2)
        while board[row, col] == 0: # Pastikan sel yang dipilih belum kosong
             row, col = np.random.randint(0, 9, 2)
        board[row, col] = 0
        
    # Mengembalikan soal dan mask (untuk tahu sel mana yang kosong)
    mask = (board != 0)
    
    return board, solution, mask

def is_solved(board, solution):
    """Memeriksa apakah papan saat ini sama dengan solusi."""
    return np.array_equal(board, solution)

# --- 2. Inisialisasi Streamlit State ---

if 'board' not in st.session_state:
    st.session_state.difficulty = 30 # Default kesulitan: 30 sel terisi
    st.session_state.board, st.session_state.solution, st.session_state.mask = generate_sudoku(st.session_state.difficulty)
    st.session_state.initial_board = np.copy(st.session_state.board)
    st.session_state.message = ""

# --- 3. Fungsi Streamlit UI dan Logika Interaksi ---

def new_game():
    """Membuat permainan baru dan mereset state."""
    st.session_state.board, st.session_state.solution, st.session_state.mask = generate_sudoku(st.session_state.difficulty)
    st.session_state.initial_board = np.copy(st.session_state.board)
    st.session_state.message = "Game baru dimulai!"

def reset_board():
    """Meresset papan ke keadaan awal."""
    st.session_state.board = np.copy(st.session_state.initial_board)
    st.session_state.message = "Papan direset ke kondisi awal."

def check_solution():
    """Memeriksa apakah input user sudah benar (dengan membandingkan ke solusi)."""
    current_board = st.session_state.board
    
    # Cek apakah semua sel sudah terisi
    if 0 in current_board:
        st.session_state.message = "❌ Belum semua sel terisi!"
        return
    
    # Bandingkan input user dengan solusi
    if is_solved(current_board, st.session_state.solution):
        st.balloons()
        st.session_state.message = "🎉 SELAMAT! Anda berhasil memecahkan Sudoku ini!"
    else:
        st.session_state.message = "🤔 Ada kesalahan. Coba periksa kembali angkamu!"

def update_cell(r, c):
    """Logika yang dipanggil saat user memasukkan angka di salah satu kotak."""
    
    # Ambil nilai dari input Streamlit
    try:
        new_val = int(st.session_state[f'cell_{r}_{c}'])
        if new_val < 0 or new_val > 9:
             st.session_state.message = "Input harus angka antara 1 sampai 9."
             return
    except ValueError:
        new_val = 0 # Jika input kosong atau non-angka, anggap 0 (kosong)
    
    # Update papan
    st.session_state.board[r, c] = new_val
    st.session_state.message = ""
    
    # Jika papan penuh, langsung cek solusi
    if 0 not in st.session_state.board:
        check_solution()


# --- 4. Tampilan Streamlit UI ---

st.set_page_config(page_title="Virtual Lab Sudoku", layout="wide")

st.title("🧩 Virtual Lab: Sudoku Interaktif")
st.markdown("Latih **logika** dan **konsentrasi** Anda dengan memecahkan teka-teki Sudoku. Aturan: setiap angka 1-9 harus muncul tepat sekali di setiap baris, kolom, dan kotak 3x3.")

# --- SIDEBAR (Pengaturan) ---
st.sidebar.header("🛠️ Pengaturan Permainan")

st.sidebar.markdown("**Kesulitan:** Jumlah sel yang terisi (maks 81)")
st.session_state.difficulty = st.sidebar.slider("Pilih Kesulitan", 20, 40, st.session_state.difficulty, step=1, on_change=new_game)
st.sidebar.button("Mulai Game Baru", on_click=new_game)
st.sidebar.button("Reset Papan", on_click=reset_board)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Status Game:** {st.session_state.message}")


# --- TAMPILAN UTAMA (Papan Sudoku) ---

st.header("Papan Permainan")
st.subheader(st.session_state.message)

# Menggunakan kolom untuk tata letak yang lebih rapi
board_display = st.columns(1)[0].empty()

with board_display.container():
    # Style CSS sederhana untuk membedakan kotak 3x3 dan angka awal
    st.markdown("""
        <style>
        .sudoku-grid {
            border-collapse: collapse;
        }
        .sudoku-grid td {
            border: 1px solid #ccc;
            padding: 0;
            width: 50px;
            height: 50px;
            text-align: center;
        }
        .sudoku-grid input {
            width: 90%;
            height: 90%;
            border: none;
            text-align: center;
            font-size: 1.2em;
            background-color: transparent;
            margin: auto;
        }
        /* Style untuk garis tebal antar kotak 3x3 */
        .sudoku-grid tr:nth-child(3n) td { border-bottom: 3px solid #666; }
        .sudoku-grid td:nth-child(3n) { border-right: 3px solid #666; }
        .sudoku-grid tr:last-child td { border-bottom: 1px solid #ccc; }
        .sudoku-grid td:last-child { border-right: 1px solid #ccc; }
        
        /* Style untuk angka yang sudah ada (tidak bisa diubah) */
        .fixed-cell input {
            font-weight: bold;
            color: #1f77b4; /* Warna biru */
            pointer-events: none; /* Nonaktifkan input */
        }
        .error-message {
            color: red;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Membuat tabel HTML untuk papan Sudoku
    html_table = "<table class='sudoku-grid'>"
    
    for r in range(9):
        html_table += "<tr>"
        for c in range(9):
            is_fixed = st.session_state.mask[r, c]
            current_val = st.session_state.board[r, c]
            
            # Tentukan class CSS
            cell_class = "fixed-cell" if is_fixed else "editable-cell"
            
            # Gunakan st.column untuk menempatkan widget Streamlit di dalam sel tabel
            # Note: Ini adalah pendekatan yang lebih rumit, di Streamlit kita harus menggunakan
            # widget secara langsung, bukan embedding HTML input secara langsung.
            
            # *PENDAMPING UI STREAMLIT (Membuat Grid)*
            # Karena Streamlit tidak mendukung input langsung dalam HTML string, 
            # kita harus menggunakan kolom dan widget number_input.
            pass # Lanjutkan dengan tata letak kolom di luar HTML string

    # Tampilan Papan (Menggunakan Kolom Streamlit)
    
    cols = st.columns(9)
    for r in range(9):
        cols = st.columns(9)
        for c in range(9):
            with cols[c]:
                # Tentukan nilai awal
                val = st.session_state.board[r, c] if st.session_state.board[r, c] != 0 else ""
                is_fixed = st.session_state.mask[r, c]
                
                # Input Field
                st.number_input(
                    label=f"c{r}{c}",
                    value=val,
                    min_value=0, 
                    max_value=9, 
                    step=1,
                    key=f'cell_{r}_{c}',
                    label_visibility='collapsed',
                    disabled=is_fixed,
                    on_change=update_cell,
                    args=(r, c),
                )

# Tombol Cek dan Petunjuk
st.markdown("---")
col_check, col_hint = st.columns([1, 2])

with col_check:
    st.button("Selesai & Cek Jawaban", on_click=check_solution, use_container_width=True)

with col_hint:
    st.markdown("""
    **Petunjuk Edukasi:**
    Teka-teki ini menguji kemampuan **deduksi logis**. Setiap kali Anda mengisi satu sel, Anda harus menggunakan aturan Sudoku (baris/kolom/kotak 3x3) untuk **mengeliminasi** kemungkinan angka pada sel lain.
    """)
