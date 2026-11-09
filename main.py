"""BAGIAN 7 - Menu console (titik masuk program).

Jalankan: python main.py
Data contoh dibuat di memori setiap program dijalankan (tidak disimpan ke file).
"""

from datetime import date

from anggota import Anggota, rupiah
from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
from koleksi import Buku, Koleksi
from koleksi_turunan import EBook, Majalah, Referensi
from peminjaman import PerpustakaanError
from perpustakaan import buat_data_contoh


def tanya(prompt, bawaan=None):
    teks = input(f"{prompt}{f' [{bawaan}]' if bawaan is not None else ''}: ").strip()
    return teks if teks else ("" if bawaan is None else str(bawaan))


def tanya_tanggal(prompt):
    teks = tanya(f"{prompt} (YYYY-MM-DD, kosong = hari ini)")
    return date.fromisoformat(teks) if teks else date.today()


def cetak_daftar(judul, data):
    print(f"\n--- {judul} ---")
    for baris in data or ["(kosong)"]:
        print(baris if isinstance(baris, str) else baris.ringkasan())


def teks_mro(kelas):
    return " -> ".join(k.__name__ for k in kelas.__mro__)


class MenuPerpustakaan:
    def __init__(self, perpus):
        self.perpus = perpus

    # ---------- kerangka menu ----------
    def jalankan_aksi(self, aksi):
        try:
            aksi()
        except (PerpustakaanError, ValueError, TypeError) as e:
            print(f"[GAGAL] {e}")

    def tampilkan_menu(self, judul, opsi, teks_keluar="Kembali"):
        """opsi: list (kunci, teks, fungsi). Berulang sampai pengguna memilih 0."""
        while True:
            print(f"\n===== {judul} =====")
            for kunci, teks, _ in opsi:
                print(f"{kunci}. {teks}")
            print(f"0. {teks_keluar}")
            pilihan = input("Pilih: ").strip()
            if pilihan == "0":
                return
            aksi = {k: f for k, _, f in opsi}.get(pilihan)
            if aksi:
                self.jalankan_aksi(aksi)
            else:
                print("Pilihan tidak tersedia.")

    def ubah_data(self, objek, atribut_list):
        """Ubah atribut lewat setter; kosongkan input agar nilai lama tetap."""
        for atribut in atribut_list:
            lama = getattr(objek, atribut)
            baru = tanya(f"{atribut.replace('_', ' ').capitalize()}", lama)
            if baru != str(lama):
                try:
                    setattr(objek, atribut, baru)  # validasi dijalankan oleh setter
                except ValueError as e:
                    print(f"[GAGAL] {atribut}: {e}")
        print("Data diperbarui:", objek.ringkasan())

    def jalankan(self):
        self.tampilkan_menu(self.perpus.nama.upper(), [
            ("1", "Kelola koleksi", self.menu_koleksi),
            ("2", "Kelola anggota", self.menu_anggota),
            ("3", "Pinjam koleksi", self.pinjam),
            ("4", "Kembalikan koleksi", self.kembalikan),
            ("5", "Bayar denda", self.bayar_denda),
            ("6", "Laporan", self.menu_laporan),
        ], teks_keluar="Keluar")
        print("Terima kasih!")

    # ---------- koleksi ----------
    def menu_koleksi(self):
        self.tampilkan_menu("KOLEKSI", [
            ("1", "Lihat semua", lambda: cetak_daftar("Koleksi", self.perpus.daftar_koleksi())),
            ("2", "Tambah", self.tambah_koleksi),
            ("3", "Cari", lambda: cetak_daftar(
                "Hasil", self.perpus.cari_koleksi_kata(tanya("Kata kunci")))),
            ("4", "Ubah", self.ubah_koleksi),
            ("5", "Hapus", lambda: print("Dihapus:",
                                         self.perpus.hapus_koleksi(tanya("Kode")).judul)),
        ])

    def tambah_koleksi(self):
        jenis = tanya("Jenis (1 Buku, 2 Majalah, 3 E-Book, 4 Referensi)")
        if jenis not in ("1", "2", "3", "4"):
            raise ValueError("Jenis koleksi tidak valid")
        kode, judul, tahun = tanya("Kode"), tanya("Judul"), tanya("Tahun")
        if jenis == "2":
            koleksi = Majalah(kode, judul, tahun, tanya("Edisi"), tanya("Stok", 1))
        else:
            penulis, penerbit = tanya("Penulis"), tanya("Penerbit")
            if jenis == "1":
                koleksi = Buku(kode, judul, tahun, penulis, penerbit, tanya("Stok", 1))
            elif jenis == "3":
                koleksi = EBook(kode, judul, tahun, penulis, penerbit, tanya("Format", "PDF"),
                                tanya("Ukuran MB", 1.0), tanya("Jumlah lisensi", 1))
            else:
                koleksi = Referensi(kode, judul, tahun, penulis, penerbit, tanya("Stok", 1))
        self.perpus.tambah_koleksi(koleksi)
        print("Ditambahkan:", koleksi.ringkasan())

    def ubah_koleksi(self):
        koleksi = self.perpus.cari_koleksi(tanya("Kode"))
        atribut = ["judul", "tahun", "stok"]
        if isinstance(koleksi, Buku):
            atribut += ["penulis", "penerbit"]
        if isinstance(koleksi, Majalah):
            atribut += ["edisi"]
        if isinstance(koleksi, EBook):
            atribut += ["format_file", "ukuran_mb"]
        self.ubah_data(koleksi, atribut)

    # ---------- anggota ----------
    def menu_anggota(self):
        self.tampilkan_menu("ANGGOTA", [
            ("1", "Lihat semua", lambda: cetak_daftar("Anggota", self.perpus.daftar_anggota())),
            ("2", "Tambah", self.tambah_anggota),
            ("3", "Cari", lambda: cetak_daftar(
                "Hasil", self.perpus.cari_anggota_kata(tanya("Kata kunci")))),
            ("4", "Ubah", self.ubah_anggota),
            ("5", "Hapus", lambda: print("Dihapus:",
                                         self.perpus.hapus_anggota(tanya("ID")).nama)),
        ])

    def tambah_anggota(self):
        jenis = tanya("Jenis (1 Mahasiswa, 2 Dosen, 3 Asisten Dosen, 4 Umum)")
        if jenis not in ("1", "2", "3", "4"):
            raise ValueError("Jenis anggota tidak valid")
        id_anggota, nama = tanya("ID"), tanya("Nama")
        if jenis == "1":
            anggota = Mahasiswa(id_anggota, nama, tanya("Prodi"))
        elif jenis == "2":
            anggota = Dosen(id_anggota, nama, tanya("Bidang"))
        elif jenis == "3":
            anggota = AsistenDosen(id_anggota, nama, tanya("Prodi"), tanya("Bidang"))
        else:
            anggota = Umum(id_anggota, nama)
        anggota.telepon = tanya("Telepon (boleh kosong)")
        anggota.email = tanya("Email (boleh kosong)")
        self.perpus.tambah_anggota(anggota)
        print("Ditambahkan:", anggota.ringkasan())

    def ubah_anggota(self):
        anggota = self.perpus.cari_anggota(tanya("ID"))
        atribut = ["nama", "telepon", "email"]
        if isinstance(anggota, Mahasiswa):
            atribut += ["prodi"]
        if isinstance(anggota, Dosen):
            atribut += ["bidang"]  # AsistenDosen mendapat prodi DAN bidang
        self.ubah_data(anggota, atribut)

    # ---------- transaksi ----------
    def pinjam(self):
        transaksi = self.perpus.pinjam(tanya("ID anggota"), tanya("Kode koleksi"),
                                       tanya_tanggal("Tanggal pinjam"))
        print("Berhasil:", transaksi.ringkasan())

    def kembalikan(self):
        cetak_daftar("Pinjaman aktif", self.perpus.pinjaman_aktif())
        transaksi = self.perpus.kembalikan(tanya("ID peminjaman"),
                                           tanya_tanggal("Tanggal kembali"))
        print("Dikembalikan:", transaksi.ringkasan())

    def bayar_denda(self):
        anggota = self.perpus.cari_anggota(tanya("ID anggota"))
        print(f"Denda {anggota.nama}: {rupiah(anggota.total_denda)}")
        jumlah = int(tanya("Jumlah bayar"))  # bayar_denda() mewajibkan int
        sisa = self.perpus.bayar_denda(anggota.id, jumlah)
        print("Sisa denda:", rupiah(sisa))

    # ---------- laporan ----------
    def menu_laporan(self):
        self.tampilkan_menu("LAPORAN", [
            ("1", "Ringkasan perpustakaan", lambda: print(self.perpus.laporan())),
            ("2", "Peminjaman aktif", lambda: cetak_daftar(
                "Aktif", self.perpus.pinjaman_aktif())),
            ("3", "Peminjaman terlambat", lambda: cetak_daftar(
                "Terlambat", self.perpus.pinjaman_terlambat())),
            ("4", "Riwayat peminjaman", lambda: cetak_daftar(
                "Riwayat", self.perpus.daftar_peminjaman())),
            ("5", "Anggota berdenda", lambda: cetak_daftar(
                "Berdenda", [a for a in self.perpus.daftar_anggota() if a.total_denda > 0])),
            ("6", "Struktur class & MRO", self.struktur_kelas),
        ])

    def struktur_kelas(self):
        print("\n--- MRO (urutan pencarian method) ---")
        for kelas in (Koleksi, Buku, Majalah, Referensi, EBook,
                      Anggota, Mahasiswa, Dosen, Umum, AsistenDosen):
            print(f"{kelas.__name__:<12}: {teks_mro(kelas)}")


def main():
    try:
        MenuPerpustakaan(buat_data_contoh()).jalankan()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")


if __name__ == "__main__":
    main()
