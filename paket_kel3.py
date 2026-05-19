# PEMBAGIAN FUNGSI
# Febri Dimiyati: code 2 & 3
# Moh. Nukas Herdiyansah: code 1 & 8
# Putra Rais Hakim: code

# Catatan: data paket disimpan sebagai TUPLE (nama, berat, kode)
# Karena tuple immutable, setiap "perubahan" menghasilkan tuple baru.

# ─────────────────────────────────────────────
# Helper tampilan
# ─────────────────────────────────────────────
def garis(char="=", panjang=45):
    print(char * panjang)

def header(judul):
    print()
    garis()
    print(f"  {judul}")
    garis()

def cetak_tabel(data):
    if not data:
        print("  (tidak ada data)")
        return
    print(f"  {'No':<4} {'Nama Paket':<20} {'Berat (kg)':<12} {'Kode'}")
    print(f"  {'-'*4} {'-'*20} {'-'*12} {'-'*6}")
    for i, p in enumerate(data, 1):
        print(f"  {i:<4} {p[0]:<20} {p[1]:<12.2f} {p[2]}")

# ─────────────────────────────────────────────
# 1. Tambah paket
# ─────────────────────────────────────────────
def tambah_paket(data):
    header("TAMBAH PAKET BARU")
    try:
        nama  = input("  Nama paket        : ")
        berat = float(input("  Berat paket (kg)  : "))
        kode  = input("  Kode wilayah      : ").upper()
        paket = (nama, berat, kode)   # <-- tuple
        data.append(paket)
        print(f"\n  [OK] Paket '{nama}' berhasil ditambahkan.")
    except ValueError:
        print("\n  [ERROR] Berat harus berupa angka!")
    return data

# ─────────────────────────────────────────────
# 2. Hitung jumlah paket
# ─────────────────────────────────────────────
def hitung_jumlah_paket(data):
    header("JUMLAH PAKET")
    print(f"  Total paket terdaftar : {len(data)} paket")

# ─────────────────────────────────────────────
# 3. Cari paket berdasarkan kode
# ─────────────────────────────────────────────
def cari_paket_kode(data):
    header("CARI PAKET BERDASARKAN KODE")
    kode  = input("  Kode wilayah : ").upper()
    hasil = [p for p in data if p[2] == kode]  # p[2] = kode wilayah
    print()
    if hasil:
        cetak_tabel(hasil)
        print(f"\n  Ditemukan {len(hasil)} paket dengan kode '{kode}'.")
    else:
        print(f"  Tidak ada paket dengan kode '{kode}'.")

# ─────────────────────────────────────────────
# 4. Statistik paket
# ─────────────────────────────────────────────
def statistik_paket(data):
    header("STATISTIK PAKET PER WILAYAH")
    if not data:
        print("  Belum ada data paket.")
        return

    statistik = {}
    for p in data:
        kode = p[2]  # p[2] = kode wilayah
        if kode not in statistik:
            statistik[kode] = {"jumlah": 0, "total_berat": 0.0}
        statistik[kode]["jumlah"] += 1
        statistik[kode]["total_berat"] += p[1]  # p[1] = berat

    print(f"\n  {'Kode':<8} {'Jumlah':>8} {'Total Berat (kg)':>18} {'Rata-rata (kg)':>16}")
    print(f"  {'-'*8} {'-'*8} {'-'*18} {'-'*16}")
    for kode, info in sorted(statistik.items()):
        rata = info["total_berat"] / info["jumlah"]
        print(f"  {kode:<8} {info['jumlah']:>8} {info['total_berat']:>18.2f} {rata:>16.2f}")
    print()

# ─────────────────────────────────────────────
# 5. Simpan data ke file
# ─────────────────────────────────────────────
def simpan_file(data, filename="paket.txt"):
    header("SIMPAN DATA KE FILE")
    try:
        with open(filename, "w") as f:
            for p in data:
                f.write(f"{p[0]},{p[1]},{p[2]}\n")  # p = (nama, berat, kode)
        print(f"  [OK] Data berhasil disimpan ke '{filename}'.")
    except Exception as e:
        print(f"  [ERROR] Gagal menyimpan file: {e}")

# ─────────────────────────────────────────────
# 6. Muat data dari file
# ─────────────────────────────────────────────
def muat_file(filename="paket.txt"):
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    nama, berat, kode = parts
                    try:
                        paket = (nama, float(berat), kode)  # <-- tuple
                        data.append(paket)
                    except ValueError:
                        print("  [PERINGATAN] Berat tidak valid, baris dilewati.")
        print(f"  [OK] Data dimuat dari '{filename}' ({len(data)} paket).")
    except FileNotFoundError:
        print(f"  [INFO] File '{filename}' tidak ditemukan, mulai dengan data kosong.")
    return data

# ─────────────────────────────────────────────
# 7. Filter data paket
# ─────────────────────────────────────────────
def filter_paket(data):
    header("FILTER PAKET BERDASARKAN BERAT")
    try:
        min_berat = float(input("  Berat minimum (kg) : "))
        hasil = [p for p in data if p[1] >= min_berat]  # p[1] = berat
        print()
        if hasil:
            cetak_tabel(hasil)
            print(f"\n  Ditemukan {len(hasil)} paket dengan berat >= {min_berat} kg.")
        else:
            print(f"  Tidak ada paket dengan berat >= {min_berat} kg.")
    except ValueError:
        print("  [ERROR] Berat harus berupa angka!")

# ─────────────────────────────────────────────
# 8. Rekursif: cari paket berdasarkan nama
# ─────────────────────────────────────────────
def cari_paket_rekursif(data, nama, index=0):
    if index >= len(data):          # base case 1: tidak ditemukan
        return None
    if data[index][0].lower() == nama.lower():  # base case 2: ditemukan
        return data[index]
    return cari_paket_rekursif(data, nama, index + 1)


# ─────────────────────────────────────────────
# Program Utama
# ─────────────────────────────────────────────
def tampil_menu():
    print()
    garis()
    print("       SISTEM MANAJEMEN PAKET")
    garis()
    print("  1. Tambah Paket")
    print("  2. Hitung Jumlah Paket")
    print("  3. Cari Paket Berdasarkan Kode")
    print("  4. Tampilkan Statistik Paket")
    print("  5. Filter Paket Berdasarkan Berat")
    print("  6. Simpan Data ke File")
    print("  7. Cari Paket (Rekursif)")
    print("  0. Keluar")
    garis()

def main():
    print()
    garis("=", 45)
    print("       SISTEM MANAJEMEN PAKET")
    print("       Kelola data paket dengan mudah")
    garis("=", 45)
    print()

    data = muat_file()

    while True:
        tampil_menu()
        pilihan = input("  Pilih menu [0-7] : ")

        if pilihan == "1":
            data = tambah_paket(data)
        elif pilihan == "2":
            hitung_jumlah_paket(data)
        elif pilihan == "3":
            cari_paket_kode(data)
        elif pilihan == "4":
            statistik_paket(data)
        elif pilihan == "5":
            filter_paket(data)
        elif pilihan == "6":
            simpan_file(data)
        elif pilihan == "7":
            header("CARI PAKET (REKURSIF)")
            nama  = input("  Nama paket : ")
            hasil = cari_paket_rekursif(data, nama)
            print()
            if hasil:
                cetak_tabel([hasil])
                print("  [OK] Paket ditemukan!")
            else:
                print(f"  Paket '{nama}' tidak ditemukan.")
        elif pilihan == "0":
            print()
            garis()
            print("  Terima kasih! Program selesai.")
            garis()
            break
        else:
            print("\n  [ERROR] Pilihan tidak valid! Masukkan angka 0-7.")

if __name__ == "__main__":
    main()