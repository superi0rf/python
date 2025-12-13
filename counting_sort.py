import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time


class CountingSort:
    def __init__(self, root):
        self.root = root
        self.root.title("Counting Sort")
        self.root.geometry("1150x750")

        self.speed = tk.DoubleVar(value=0.6)
        self.step_mode = tk.BooleanVar(value=False)
        self.step_event = threading.Event()

        self.data = []
        self.count = []
        self.output = []

        self.build_ui()

    # ================= UI =================
    def build_ui(self):
        tk.Label(
            self.root,
            text="Counting Sort)",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        ctrl = ttk.Frame(self.root)
        ctrl.pack()

        ttk.Label(ctrl, text="Masukkan data (pisahkan koma):").grid(row=0, column=0)
        self.entry = ttk.Entry(ctrl, width=40)
        self.entry.grid(row=0, column=1, padx=5)

        ttk.Button(ctrl, text="Start", command=self.start).grid(row=0, column=2, padx=5)
        ttk.Button(ctrl, text="Next Step", command=self.next_step).grid(row=0, column=3, padx=5)
        ttk.Button(ctrl, text="Reset", command=self.reset).grid(row=0, column=4, padx=5)

        ttk.Checkbutton(
            ctrl, text="Mode Step-by-Step", variable=self.step_mode
        ).grid(row=0, column=5, padx=10)

        ttk.Label(ctrl, text="Kecepatan Animasi").grid(row=1, column=0)
        ttk.Scale(
            ctrl, from_=0.1, to=1.5,
            orient="horizontal", variable=self.speed, length=250
        ).grid(row=1, column=1, pady=5)

        # === Grafik ===
        fig_frame = ttk.Frame(self.root)
        fig_frame.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.get_tk_widget().pack()

        # === Log ===
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(log_frame, text="Log Proses Algoritma").pack(anchor="w")
        self.log = scrolledtext.ScrolledText(log_frame, font=("Consolas", 10))
        self.log.pack(fill="both", expand=True)

    # ================= DRAW =================
    def draw_array(self, array, highlight=None, title="Array"):
        self.ax.clear()
        bars = self.ax.bar(range(len(array)), array, color="skyblue")

        if highlight is not None:
            bars[highlight].set_color("orange")

        self.ax.set_title(title)
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.grid(axis="y", linestyle="--", alpha=0.5)

        # X = indeks integer
        self.ax.set_xticks(range(len(array)))
        self.ax.set_xticklabels([str(i) for i in range(len(array))])

        # Y = nilai integer
        max_y = max(array) if array else 1
        self.ax.set_yticks(range(0, max_y + 1))
        self.ax.set_yticklabels([str(i) for i in range(0, max_y + 1)])

        self.canvas.draw()

    # ================= CONTROL =================
    def pause(self):
        if self.step_mode.get():
            self.step_event.clear()
            self.step_event.wait()
        time.sleep(self.speed.get())

    def next_step(self):
        self.step_event.set()

    def reset(self):
        self.entry.delete(0, tk.END)
        self.log.delete("1.0", tk.END)
        self.ax.clear()
        self.canvas.draw()

    def start(self):
        try:
            self.data = list(map(int, self.entry.get().split(",")))
            self.log.delete("1.0", tk.END)
            threading.Thread(target=self.run).start()
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka")

    # ================= ALGORITHM =================
    def run(self):
        self.log.insert(tk.END, "=== COUNTING SORT DIMULAI ===\n\n")
        self.log.insert(tk.END, f"Data awal: {self.data}\n")
        self.log.insert(tk.END, "Grafik menampilkan kondisi awal array.\n\n")

        # tampilkan data awal
        self.draw_array(self.data, title="Data Awal")
        self.pause()

        max_val = max(self.data)
        self.count = [0] * (max_val + 1)
        self.output = [0] * len(self.data)

        # STEP 1
        self.log.insert(tk.END, "STEP 1: Menghitung frekuensi\n")
        for i, num in enumerate(self.data):
            self.count[num] += 1
            self.log.insert(
                tk.END,
                f"Membaca data[{i}] = {num} → count[{num}] = {self.count[num]}\n"
            )
            self.pause()

        # STEP 2
        self.log.insert(tk.END, "\nSTEP 2: Prefix Sum\n")
        for i in range(1, len(self.count)):
            self.count[i] += self.count[i - 1]
            self.log.insert(
                tk.END,
                f"prefix[{i}] menyatakan jumlah elemen ≤ {i} → {self.count[i]}\n"
            )
            self.pause()

        # STEP 3
        self.log.insert(
            tk.END,
            "\nSTEP 3: Mengisi output (iterasi dari belakang untuk stabilitas)\n"
        )

        for i in range(len(self.data) - 1, -1, -1):
            num = self.data[i]
            pos = self.count[num] - 1

            self.output[pos] = num
            self.count[num] -= 1

            self.log.insert(
                tk.END,
                f"data[{i}] = {num} → posisi akhir = [{pos}]\n"
            )

            self.draw_array(self.output, highlight=pos, title="Output Sementara")
            self.pause()

        self.log.insert(
            tk.END,
            "\n=== SELESAI ===\n"
            f"Output akhir (terurut): {self.output}\n"
        )

        self.draw_array(self.output, title="Output Akhir (Sorted)")


# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = CountingSort(root)
    root.mainloop()
