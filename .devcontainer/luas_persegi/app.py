# fungsi untuk mencari luas persegi
def luas_persegi(sisi):
  luas = sisi*sisi
  return luas

# Masukan nilai sisi persegi
s = int(input('Masukkan panjang sisi persegi yang akan dihitung '))
print("Luas persegi yang Anda inginkan adalah ",luas_persegi(s) )