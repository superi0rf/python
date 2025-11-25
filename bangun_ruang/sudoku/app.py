import streamlit as st
import numpy as np
import random

# --- 1. Fungsi Logika Sudoku ---

def is_valid(board, row, col, num):
    """Mengecek apakah angka 'num' valid diletakkan di board[row][col]"""
    
    # Cek baris
    if num in board[row]:
        return False
    
    # Cek kolom
    if num in board[:, col]:
        return False
        
    # Cek sub-grid 3x3
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i, start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    """Menggunakan backtracking untuk memecahkan Sudoku"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True

def generate_full_board():
    """Menghasilkan board Sudoku yang sudah terpecahkan sepenuhnya"""
    board = np.zeros((9, 9), dtype=int)
    # Memecahkan board kosong untuk menghasilkan board penuh
    solve_sudoku(board) 
    return board

def create_puzzle(full_board, difficulty):
    """Menghasilkan puzzle dengan menghapus sejumlah angka berdasarkan difficulty"""
    puzzle = full_board.copy()
    
    if difficulty == 'Mudah':
        clues_to_remove = random.randint(35, 45) # Sisakan sekitar 36-46 petunjuk
    elif difficulty == 'Sedang':
        clues_to_remove = random.randint(46, 55) # Sisakan sekitar 26-35 petunjuk
    else: # Sulit
        clues_to_remove = random.randint(56, 60) # Sisakan sekitar 21-25 petunjuk

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    
    for r, c in cells:
        if clues_to_remove <= 0:
            break
        
        # Sembunyikan angka, jika puzzle masih bisa dipecahkan secara unik
        puzzle[r, c] = 0
        clues_to_remove -= 1
        
    return puzzle


# --- 2. Fungsi Rendering Grid (UI) ---

def display_sudoku_grid(board, initial_board):
    """Menampilkan grid Sudoku menggunakan elemen input Streamlit"""
    st.markdown("""
        <style>
            .stTextInput > div > div > input {
                text-align: center;
                font-size: 18px;
                padding: 5px;
                border: 1px solid black;
                border-radius: 0;
            }
            .fixed-cell input {
                color: darkblue !important;
                font-weight: bold;
                background-color: #f0f0f0;
            }
            .error-cell input {
                color: red !important;
                font-weight: bold;
                background-color: #ffe0e0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(9)
    for r in range(9):
        for c in range(9):
            cell_value = board[r, c]
            initial_value = initial_board[r, c]
            
            # Tentukan apakah sel ini adalah petunjuk awal
            is_initial = initial_value != 0
            
            # Tentukan class CSS
            css_class = ""
            if is_initial:
                css_class = "fixed-cell"

            # Gunakan st.text_input untuk setiap sel
            key = f"cell_{r}_{c}"
            
            # Menghindari error jika nilai awal 0
            default_value = str(cell_value) if cell_value != 0 else ""
            
            with cols[c]:
                # Nonaktifkan input untuk petunjuk awal
                disabled = is_initial
                
                # Tampilkan input
                input_value = st.text_input(
                    label='.',
                    value=default_value,
                    key=key,
                    max_chars=1,
                    label_visibility="collapsed",
                    placeholder="",
                    disabled=disabled
                )
                
                # Simpan nilai kembali ke board (hanya untuk sel yang tidak tetap)
                if not is_initial:
                    try:
                        num = int(input_value)
                        if 1 <= num <= 9:
                            board[r, c] = num
                        else:
                            board[r, c] = 0
                    except ValueError:
                        board[r, c] = 0

    return board

# --- 3. Pengaturan Streamlit State (Penyimpanan Status Game) ---

def initialize_game(difficulty='Mudah'):
    """Menginisialisasi atau mereset game"""
    full_board = generate_full_board()
    puzzle = create_puzzle(full_board, difficulty)
    
    st.session_state.puzzle = puzzle.copy()       # Grid yang sedang dimainkan
    st.session_state.initial_puzzle = puzzle.copy() # Grid awal (petunjuk tetap)
    st.session_state.solution = full_board.copy() # Solusi resmi
    st.session_state.game_started = True

# --- 4. UI Streamlit Utama ---

st.set_page_config(page_title="Virtual Lab Logika Sudoku", layout="wide")

st.title("🔢 Virtual Lab Logika: Permainan Sudoku")
st.markdown("Latih kemampuan logika dan pemecahan masalah Anda dengan Sudoku interaktif.")

# --- SIDEBAR (Pengaturan dan Kontrol) ---
st.sidebar.header("⚙️ Kontrol Permainan")

# Pilihan Kesulitan
difficulty = st.sidebar.selectbox(
    "Pilih Tingkat Kesulitan:",
    ['Mudah', 'Sedang', 'Sulit']
)

# Tombol Mulai/Reset Game
if st.sidebar.button("Mulai Game Baru", help="Membuat puzzle Sudoku baru"):
    initialize_game(difficulty)

# Pastikan state ada saat pertama kali dijalankan
if 'game_started' not in st.session_state:
    initialize_game(difficulty='Mudah')

# --- TAMPILAN UTAMA ---

current_board = st.session_state.puzzle
initial_board = st.session_state.initial_puzzle
solution = st.session_state.solution

st.subheader("Papan Permainan")
st.markdown(f"Tingkat Kesulitan: **{difficulty}**")

# Tampilkan Grid dan Perbarui Current_board
updated_board = display_sudoku_grid(current_board, initial_board)
st.session_state.puzzle = updated_board # Simpan state yang diperbarui

st.markdown("---")

col_check, col_solve = st.columns(2)

with col_check:
    if st.button("Cek Solusi", help="Periksa apakah angka yang Anda masukkan sudah benar"):
        
        # Cek apakah semua sel sudah terisi
        if np.any(updated_board == 0):
            st.warning("Papan belum terisi penuh! Lanjutkan pengisian.")
        
        # Cek apakah papan saat ini sama dengan solusi
        elif np.array_equal(updated_board, solution):
            st.balloons()
            st.success("🎉 Selamat! Solusi Anda BENAR!")
            st.session_state.game_started = False # Hentikan game
        else:
            st.error("❌ Solusi Anda masih salah. Periksa kembali logikanya!")
            # Di sini bisa ditambahkan logika untuk menandai sel yang salah

with col_solve:
    if st.button("Tampilkan Solusi (Curang!)", help="Menampilkan solusi penuh untuk belajar"):
        st.session_state.puzzle = solution.copy()
        st.info("Solusi ditampilkan. Klik 'Mulai Game Baru' untuk mencoba lagi.")


st.markdown("---")
st.subheader("💡 Konsep Logika Sudoku")
st.markdown("""
Sudoku melibatkan tiga aturan utama:
* **Setiap baris** harus berisi angka 1-9 tepat sekali.
* **Setiap kolom** harus berisi angka 1-9 tepat sekali.
* **Setiap sub-grid 3x3** harus berisi angka 1-9 tepat sekali.

Ini adalah contoh bagus dari aplikasi **logika kombinatorial** dan **algoritma *backtracking*** (yang digunakan oleh fungsi pemecah di balik layar).
""")
