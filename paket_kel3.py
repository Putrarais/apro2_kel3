# PEMBAGIAN FUNGSI
# Febri Dimyati: code 2, 3, 9
# Moh. Nukhas Herdiansyah: code 1, 8, 10
# Putra Rais Hakim: code 4, 5, 6, 7

# Catatan: data paket disimpan sebagai TUPLE (nama, berat, kode, status)
# Status: "PENDING" atau "TERKIRIM"
# Karena tuple immutable, setiap "perubahan" menghasilkan tuple baru.

# ─────────────────────────────────────────────
# Helper tampilan
# ─────────────────────────────────────────────
def garis(char="=", panjang=55):
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
    print(f"  {'No':<4} {'Nama Paket':<20} {'Berat (kg)':<12} {'Kode':<8} {'Status'}")
    print(f"  {'-'*4} {'-'*20} {'-'*12} {'-'*8} {'-'*10}")
    for i, p in enumerate(data, 1):
        status = p[3] if len(p) > 3 else "PENDING"
        status_str = f"[✓] {status}" if status == "TERKIRIM" else f"[ ] {status}"
        print(f"  {i:<4} {p[0]:<20} {p[1]:<12.2f} {p[2]:<8} {status_str}")

# ─────────────────────────────────────────────
# 1. Tambah paket
# ─────────────────────────────────────────────
def tambah_paket(data):
    header("TAMBAH PAKET BARU")
    try:
        nama  = input("  Nama paket        : ")
        berat = float(input("  Berat paket (kg)  : "))
        kode  = input("  Kode wilayah      : ").upper()
        paket = (nama, berat, kode, "PENDING")   # <-- tuple dengan status default PENDING
        data.append(paket)
        print(f"\n  [OK] Paket '{nama}' berhasil ditambahkan dengan status PENDING.")
    except ValueError:
        print("\n  [ERROR] Berat harus berupa angka!")
    return data

# ─────────────────────────────────────────────
# 2. Hitung jumlah paket
# ─────────────────────────────────────────────
def hitung_jumlah_paket(data):
    header("JUMLAH PAKET")
    total     = len(data)
    pending   = sum(1 for p in data if (len(p) <= 3 or p[3] == "PENDING"))
    terkirim  = sum(1 for p in data if len(p) > 3 and p[3] == "TERKIRIM")
    print(f"  Total paket terdaftar : {total} paket")
    print(f"  - Pending             : {pending} paket")
    print(f"  - Terkirim            : {terkirim} paket")

# ─────────────────────────────────────────────
# 3. Cari paket berdasarkan kode
# ─────────────────────────────────────────────
def cari_paket_kode(data):
    header("CARI PAKET BERDASARKAN KODE")
    kode  = input("  Kode wilayah : ").upper()
    hasil = [p for p in data if p[2] == kode]
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
        kode = p[2]
        if kode not in statistik:
            statistik[kode] = {"jumlah": 0, "total_berat": 0.0, "terkirim": 0}
        statistik[kode]["jumlah"] += 1
        statistik[kode]["total_berat"] += p[1]
        if len(p) > 3 and p[3] == "TERKIRIM":
            statistik[kode]["terkirim"] += 1

    print(f"\n  {'Kode':<8} {'Jumlah':>8} {'Terkirim':>10} {'Total Berat (kg)':>18} {'Rata-rata (kg)':>16}")
    print(f"  {'-'*8} {'-'*8} {'-'*10} {'-'*18} {'-'*16}")
    for kode, info in sorted(statistik.items()):
        rata = info["total_berat"] / info["jumlah"]
        print(f"  {kode:<8} {info['jumlah']:>8} {info['terkirim']:>10} {info['total_berat']:>18.2f} {rata:>16.2f}")
    print()

# ─────────────────────────────────────────────
# 5. Simpan data ke file
# ─────────────────────────────────────────────
def simpan_file(data, filename="paket.txt"):
    header("SIMPAN DATA KE FILE")
    try:
        with open(filename, "w") as f:
            for p in data:
                status = p[3] if len(p) > 3 else "PENDING"
                f.write(f"{p[0]},{p[1]},{p[2]},{status}\n")
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
                # Support format lama (3 kolom) maupun baru (4 kolom)
                if len(parts) == 3:
                    nama, berat, kode = parts
                    status = "PENDING"
                elif len(parts) == 4:
                    nama, berat, kode, status = parts
                else:
                    continue
                try:
                    paket = (nama, float(berat), kode, status)
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
        hasil = [p for p in data if p[1] >= min_berat]
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
    if index >= len(data):
        return None
    if data[index][0].lower() == nama.lower():
        return data[index]
    return cari_paket_rekursif(data, nama, index + 1)

# ─────────────────────────────────────────────
# 9. Tandai paket sebagai selesai dikirim
# ─────────────────────────────────────────────
def tandai_terkirim(data):
    header("TANDAI PAKET SELESAI DIKIRIM")
    if not data:
        print("  Belum ada data paket.")
        return data

    cetak_tabel(data)
    print()
    try:
        nomor = int(input("  Masukkan nomor paket yang akan ditandai terkirim : "))
        if nomor < 1 or nomor > len(data):
            print("  [ERROR] Nomor paket tidak valid!")
            return data

        paket_lama = data[nomor - 1]
        if len(paket_lama) > 3 and paket_lama[3] == "TERKIRIM":
            print(f"\n  [INFO] Paket '{paket_lama[0]}' sudah berstatus TERKIRIM.")
            return data

        # Buat tuple baru dengan status TERKIRIM (karena tuple immutable)
        paket_baru = (paket_lama[0], paket_lama[1], paket_lama[2], "TERKIRIM")
        data[nomor - 1] = paket_baru
        print(f"\n  [OK] Paket '{paket_baru[0]}' berhasil ditandai sebagai TERKIRIM.")
    except ValueError:
        print("  [ERROR] Masukkan angka yang valid!")
    return data

# ─────────────────────────────────────────────
# 10. Hapus paket
# ─────────────────────────────────────────────
def hapus_paket(data):
    header("HAPUS PAKET")
    if not data:
        print("  Belum ada data paket.")
        return data

    cetak_tabel(data)
    print()
    print("  Opsi hapus:")
    print("  [1] Hapus berdasarkan nomor urut")
    print("  [2] Hapus berdasarkan nama paket")
    print("  [3] Hapus semua paket berstatus TERKIRIM")
    print("  [0] Batal")

    pilihan = input("\n  Pilih opsi : ")

    if pilihan == "1":
        try:
            nomor = int(input("  Masukkan nomor paket yang akan dihapus : "))
            if nomor < 1 or nomor > len(data):
                print("  [ERROR] Nomor tidak valid!")
                return data
            paket = data[nomor - 1]
            konfirmasi = input(f"  Hapus paket '{paket[0]}'? (y/n) : ").lower()
            if konfirmasi == "y":
                data.pop(nomor - 1)
                print(f"\n  [OK] Paket '{paket[0]}' berhasil dihapus.")
            else:
                print("  [BATAL] Penghapusan dibatalkan.")
        except ValueError:
            print("  [ERROR] Masukkan angka yang valid!")

    elif pilihan == "2":
        nama = input("  Masukkan nama paket yang akan dihapus : ")
        indeks_hapus = [i for i, p in enumerate(data) if p[0].lower() == nama.lower()]
        if not indeks_hapus:
            print(f"  [INFO] Paket dengan nama '{nama}' tidak ditemukan.")
        else:
            # Tampilkan yang ditemukan jika lebih dari satu
            if len(indeks_hapus) > 1:
                print(f"\n  Ditemukan {len(indeks_hapus)} paket dengan nama '{nama}':")
                for idx in indeks_hapus:
                    p = data[idx]
                    status = p[3] if len(p) > 3 else "PENDING"
                    print(f"    [{idx+1}] {p[0]} | {p[1]} kg | {p[2]} | {status}")
                try:
                    nomor = int(input("  Masukkan nomor urut paket yang ingin dihapus (0=semua) : "))
                    if nomor == 0:
                        for idx in sorted(indeks_hapus, reverse=True):
                            data.pop(idx)
                        print(f"\n  [OK] {len(indeks_hapus)} paket dengan nama '{nama}' berhasil dihapus.")
                    elif 1 <= nomor <= len(data):
                        if (nomor - 1) in indeks_hapus:
                            data.pop(nomor - 1)
                            print(f"\n  [OK] Paket dihapus.")
                        else:
                            print("  [ERROR] Nomor tidak sesuai dengan hasil pencarian.")
                    else:
                        print("  [ERROR] Nomor tidak valid.")
                except ValueError:
                    print("  [ERROR] Masukkan angka yang valid!")
            else:
                paket = data[indeks_hapus[0]]
                konfirmasi = input(f"  Hapus paket '{paket[0]}'? (y/n) : ").lower()
                if konfirmasi == "y":
                    data.pop(indeks_hapus[0])
                    print(f"\n  [OK] Paket '{paket[0]}' berhasil dihapus.")
                else:
                    print("  [BATAL] Penghapusan dibatalkan.")

    elif pilihan == "3":
        terkirim = [p for p in data if len(p) > 3 and p[3] == "TERKIRIM"]
        if not terkirim:
            print("  [INFO] Tidak ada paket berstatus TERKIRIM.")
        else:
            print(f"\n  Akan menghapus {len(terkirim)} paket berstatus TERKIRIM:")
            cetak_tabel(terkirim)
            konfirmasi = input(f"\n  Lanjutkan penghapusan? (y/n) : ").lower()
            if konfirmasi == "y":
                data = [p for p in data if not (len(p) > 3 and p[3] == "TERKIRIM")]
                print(f"\n  [OK] {len(terkirim)} paket TERKIRIM berhasil dihapus.")
            else:
                print("  [BATAL] Penghapusan dibatalkan.")

    elif pilihan == "0":
        print("  [BATAL] Kembali ke menu utama.")
    else:
        print("  [ERROR] Pilihan tidak valid!")

    return data

# ─────────────────────────────────────────────
# Program Utama
# ─────────────────────────────────────────────
def tampil_menu():
    print()
    garis()
    print("        SISTEM MANAJEMEN PAKET")
    garis()
    print("  1. Tambah Paket")
    print("  2. Hitung Jumlah Paket")
    print("  3. Cari Paket Berdasarkan Kode")
    print("  4. Tampilkan Statistik Paket")
    print("  5. Filter Paket Berdasarkan Berat")
    print("  6. Simpan Data ke File")
    print("  7. Cari Paket (Rekursif)")
    print("  8. Tandai Paket Selesai Dikirim   ")
    print("  9. Hapus Paket                    ")
    print("  0. Keluar")
    garis()

def main():
    print()
    garis("=", 55)
    print("        SISTEM MANAJEMEN PAKET")
    print("        Kelola data paket dengan mudah")
    garis("=", 55)
    print()

    data = muat_file()

    while True:
        tampil_menu()
        pilihan = input("  Pilih menu [0-9] : ")

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
        elif pilihan == "8":
            data = tandai_terkirim(data)
        elif pilihan == "9":
            data = hapus_paket(data)
        elif pilihan == "0":
            print()
            garis()
            print("  Terima kasih! Program selesai.")
            garis()
            break
        else:
            print("\n  [ERROR] Pilihan tidak valid! Masukkan angka 0-9.")

if __name__ == "__main__":
    main()