def hitung_kecepatan(jarak_km, waktu_jam):
    """Menghitung kecepatan rata-rata (km/jam)."""

    kecepatan = jarak_km / waktu_jam
    return kecepatan

# --- Penggunaan Program ---

# Input
jarak = float(input("Masukkan jarak yang ditempuh (km): "))
waktu = float(input("Masukkan waktu tempuh (jam): "))

# Panggil fungsi
hasil_kecepatan = hitung_kecepatan(jarak, waktu)

# Output
print(f"\nKecepatan rata-rata Anda adalah: {hasil_kecepatan:.2f} km/jam")