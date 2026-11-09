"""Antarmuka console (menu interaktif). Semua exception ditangkap di lapisan ini."""

from datetime import date

from .exceptions import DataDuplikat, PerpustakaanError
from .models import AsistenDosen, Buku, Dosen, EBook, Mahasiswa, Majalah, Referensi, Umum
from .utils import rupiah, urutan_mro

GARIS = "=" * 60


class MenuPerpustakaan:
    def __init__(self, perpus, penyimpanan=None):
        self.perpus = perpus
        self.penyimpanan = penyimpanan

    # ---------------- helper input/output ----------------
    @staticmethod
    def _input(prompt, wajib=True, bawaan=None):
        while True:
            nilai = input(prompt).strip()
            if nilai:
                return nilai
            if not wajib:
                return bawaan
            print("  ! Input tidak boleh kosong.")

    @staticmethod
    def _input_angka(prompt, bawaan=None):
        while True:
            nilai = input(prompt).strip()
            if not nilai and bawaan is not None:
                return bawaan
            try:
                return int(nilai)
            except ValueError:
                print("  ! Masukkan angka bulat.")

    @staticmethod
    def _input_tanggal(prompt):
        while True:
            nilai = input(f"{prompt} (YYYY-MM-DD, Enter = hari ini): ").strip()
            if not nilai:
                return date.today()
            try:
                return date.fromisoformat(nilai)
            except ValueError:
                print("  ! Format tanggal salah, contoh: 2026-11-09")

    @staticmethod
    def _pilih(judul, opsi):
        print(f"\n{GARIS}\n{judul}\n{GARIS}")
        for kunci, teks in opsi:
            print(f"  {kunci}. {teks}")
        return input("Pilih menu: ").strip()

    @staticmethod
    def _cetak_daftar(items, kosong="(data kosong)"):
        if not items:
            print(kosong)
        for item in items:
            print(" -", item.ringkasan())

    def _simpan(self):
        if self.penyimpanan:
            self.penyimpanan.simpan(self.perpus)

    def _jalankan(self, aksi):
        """Menjalankan aksi; error validasi ditampilkan tanpa menghentikan program."""
        try:
            if aksi():
                self._simpan()
        except (PerpustakaanError, ValueError, TypeError) as err:
            print(f"  ! Gagal: {err}")

    # ---------------- menu utama ----------------
    def jalankan(self):
        print(f"\nSelamat datang di {self.perpus.nama}")
        menu = {
            "1": self.menu_koleksi,
            "2": self.menu_anggota,
            "3": lambda: self._jalankan(self.pinjam),
            "4": lambda: self._jalankan(self.kembalikan),
            "5": lambda: self._jalankan(self.bayar_denda),
            "6": self.menu_laporan,
        }
        while True:
            pilihan = self._pilih("MENU UTAMA", [
                ("1", "Kelola Koleksi"),
                ("2", "Kelola Anggota"),
                ("3", "Pinjam Koleksi"),
                ("4", "Kembalikan Koleksi"),
                ("5", "Bayar Denda"),
                ("6", "Laporan"),
                ("0", "Simpan & Keluar"),
            ])
            if pilihan == "0":
                self._simpan()
                print("Data tersimpan. Terima kasih!")
                return
            aksi = menu.get(pilihan)
            if aksi:
                aksi()
            else:
                print("  ! Pilihan tidak tersedia.")

    # ---------------- koleksi ----------------
    def menu_koleksi(self):
        aksi = {
            "1": self.tambah_koleksi,
            "2": self.lihat_koleksi,
            "3": self.cari_koleksi,
            "4": self.ubah_koleksi,
            "5": self.hapus_koleksi,
        }
        while True:
            pilihan = self._pilih("KELOLA KOLEKSI", [
                ("1", "Tambah koleksi"), ("2", "Lihat semua koleksi"),
                ("3", "Cari koleksi"), ("4", "Ubah koleksi"),
                ("5", "Hapus koleksi"), ("0", "Kembali"),
            ])
            if pilihan == "0":
                return
            if pilihan in aksi:
                self._jalankan(aksi[pilihan])
            else:
                print("  ! Pilihan tidak tersedia.")

    def tambah_koleksi(self):
        jenis = self._input("Jenis (1=Buku, 2=Majalah, 3=Referensi, 4=E-Book): ")
        if jenis not in ("1", "2", "3", "4"):
            raise ValueError("Jenis koleksi tidak valid")
        kode = self._input("Kode       : ")
        if kode.upper() in {k.kode for k in self.perpus.daftar_koleksi()}:
            raise DataDuplikat(f"Kode koleksi {kode.upper()} sudah terdaftar")
        judul = self._input("Judul      : ")
        tahun = self._input_angka("Tahun      : ")
        stok = self._input_angka("Stok [1]   : ", bawaan=1)
        if jenis == "2":
            edisi = self._input("Edisi      : ")
            koleksi = Majalah(kode, judul, tahun, edisi, stok)
        else:
            penulis = self._input("Penulis    : ")
            penerbit = self._input("Penerbit   : ", wajib=False, bawaan="-")
            isbn = self._input("ISBN       : ", wajib=False, bawaan="")
            if jenis == "4":
                format_file = self._input("Format (PDF/EPUB/MOBI) [PDF]: ", wajib=False, bawaan="PDF")
                ukuran = self._input("Ukuran (MB) [1]: ", wajib=False, bawaan="1")
                koleksi = EBook(kode, judul, tahun, penulis, penerbit, format_file, ukuran, isbn, stok)
            else:
                kelas = Buku if jenis == "1" else Referensi
                koleksi = kelas(kode, judul, tahun, penulis, penerbit, isbn, stok)
        self.perpus.tambah_koleksi(koleksi)
        print(f"  ✓ {koleksi.jenis()} '{koleksi.judul}' ditambahkan.")
        return True

    def lihat_koleksi(self):
        self._cetak_daftar(self.perpus.daftar_koleksi())

    def cari_koleksi(self):
        kata = self._input("Kata kunci (kode/judul/penulis): ")
        self._cetak_daftar(self.perpus.cari_koleksi_kata(kata), "Tidak ada koleksi yang cocok.")

    def ubah_koleksi(self):
        koleksi = self.perpus.cari_koleksi(self._input("Kode koleksi: "))
        print("Data saat ini:", koleksi.ringkasan())
        print("(Kosongkan input jika tidak ingin mengubah)")
        perubahan = {}
        for atribut in ("judul", "tahun", "stok", "penulis", "penerbit", "edisi", "format_file", "ukuran_mb"):
            if hasattr(koleksi, atribut):
                nilai = self._input(f"{atribut.capitalize():<10} [{getattr(koleksi, atribut)}]: ", wajib=False)
                if nilai is not None:
                    perubahan[atribut] = nilai
        self.perpus.ubah_koleksi(koleksi.kode, **perubahan)
        print("  ✓ Koleksi diperbarui:", koleksi.ringkasan())
        return True

    def hapus_koleksi(self):
        koleksi = self.perpus.hapus_koleksi(self._input("Kode koleksi: "))
        print(f"  ✓ '{koleksi.judul}' dihapus.")
        return True

    # ---------------- anggota ----------------
    def menu_anggota(self):
        aksi = {
            "1": self.tambah_anggota,
            "2": self.lihat_anggota,
            "3": self.cari_anggota,
            "4": self.ubah_anggota,
            "5": self.hapus_anggota,
        }
        while True:
            pilihan = self._pilih("KELOLA ANGGOTA", [
                ("1", "Tambah anggota"), ("2", "Lihat semua anggota"),
                ("3", "Cari anggota"), ("4", "Ubah anggota"),
                ("5", "Hapus anggota"), ("0", "Kembali"),
            ])
            if pilihan == "0":
                return
            if pilihan in aksi:
                self._jalankan(aksi[pilihan])
            else:
                print("  ! Pilihan tidak tersedia.")

    def tambah_anggota(self):
        jenis = self._input("Jenis (1=Mahasiswa, 2=Dosen, 3=Umum, 4=Asisten Dosen): ")
        if jenis not in ("1", "2", "3", "4"):
            raise ValueError("Jenis anggota tidak valid")
        id_anggota = self._input("ID anggota : ")
        if id_anggota.upper() in {a.id for a in self.perpus.daftar_anggota()}:
            raise DataDuplikat(f"ID anggota {id_anggota.upper()} sudah terdaftar")
        nama = self._input("Nama       : ")
        telepon = self._input("Telepon    : ", wajib=False, bawaan="")
        email = self._input("Email      : ", wajib=False, bawaan="")
        if jenis == "1":
            anggota = Mahasiswa(id_anggota, nama, self._input("Prodi      : "), telepon, email=email)
        elif jenis == "2":
            anggota = Dosen(id_anggota, nama, self._input("Bidang     : "), telepon, email=email)
        elif jenis == "4":
            prodi = self._input("Prodi      : ")
            bidang = self._input("Bidang     : ")
            anggota = AsistenDosen(id_anggota, nama, prodi, bidang, telepon, email=email)
        else:
            anggota = Umum(id_anggota, nama, telepon, email=email)
        self.perpus.tambah_anggota(anggota)
        print(f"  ✓ {anggota.jenis()} '{anggota.nama}' ditambahkan.")
        return True

    def lihat_anggota(self):
        self._cetak_daftar(self.perpus.daftar_anggota())

    def cari_anggota(self):
        kata = self._input("Kata kunci (ID/nama): ")
        self._cetak_daftar(self.perpus.cari_anggota_kata(kata), "Tidak ada anggota yang cocok.")

    def ubah_anggota(self):
        anggota = self.perpus.cari_anggota(self._input("ID anggota: "))
        print("Data saat ini:", anggota.ringkasan())
        print("(Kosongkan input jika tidak ingin mengubah)")
        perubahan = {}
        for atribut in ("nama", "telepon", "email", "prodi", "bidang"):
            if hasattr(anggota, atribut):
                nilai = self._input(f"{atribut.capitalize():<10} [{getattr(anggota, atribut)}]: ", wajib=False)
                if nilai is not None:
                    perubahan[atribut] = nilai
        self.perpus.ubah_anggota(anggota.id, **perubahan)
        print("  ✓ Anggota diperbarui:", anggota.ringkasan())
        return True

    def hapus_anggota(self):
        anggota = self.perpus.hapus_anggota(self._input("ID anggota: "))
        print(f"  ✓ Anggota '{anggota.nama}' dihapus.")
        return True

    # ---------------- transaksi ----------------
    def pinjam(self):
        id_anggota = self._input("ID anggota   : ")
        kode = self._input("Kode koleksi : ")
        tanggal = self._input_tanggal("Tanggal pinjam")
        transaksi = self.perpus.pinjam(id_anggota, kode, tanggal)
        print(f"  ✓ Peminjaman {transaksi.id} berhasil. Jatuh tempo: {transaksi.jatuh_tempo}")
        return True

    def kembalikan(self):
        aktif = self.perpus.pinjaman_aktif()
        if not aktif:
            print("Tidak ada peminjaman aktif.")
            return False
        print("Peminjaman aktif:")
        for p in aktif:
            print(" -", p.ringkasan())
        id_pinjam = self._input("ID peminjaman: ")
        tanggal = self._input_tanggal("Tanggal kembali")
        transaksi = self.perpus.kembalikan(id_pinjam, tanggal)
        print(f"  ✓ '{transaksi.koleksi.judul}' dikembalikan.")
        if transaksi.denda:
            print(
                f"  ! Terlambat {transaksi.hari_terlambat()} hari, denda {rupiah(transaksi.denda)} "
                f"(total denda {transaksi.anggota.nama}: {rupiah(transaksi.anggota.total_denda)})"
            )
        return True

    def bayar_denda(self):
        anggota = self.perpus.cari_anggota(self._input("ID anggota: "))
        print(f"Denda {anggota.nama}: {rupiah(anggota.total_denda)}")
        jumlah = self._input_angka(f"Jumlah bayar [{anggota.total_denda}]: ", bawaan=anggota.total_denda)
        sisa = self.perpus.bayar_denda(anggota.id, jumlah)
        print(f"  ✓ Pembayaran diterima. Sisa denda: {rupiah(sisa)}")
        return True

    # ---------------- laporan ----------------
    def menu_laporan(self):
        while True:
            pilihan = self._pilih("LAPORAN", [
                ("1", "Ringkasan perpustakaan"),
                ("2", "Peminjaman aktif"),
                ("3", "Peminjaman terlambat"),
                ("4", "Riwayat semua peminjaman"),
                ("5", "Anggota yang memiliki denda"),
                ("6", "Struktur kelas & MRO"),
                ("0", "Kembali"),
            ])
            if pilihan == "0":
                return
            if pilihan == "1":
                print(self.perpus.laporan())
            elif pilihan == "2":
                self._cetak_daftar(self.perpus.pinjaman_aktif(), "Tidak ada peminjaman aktif.")
            elif pilihan == "3":
                self._cetak_daftar(self.perpus.pinjaman_terlambat(), "Tidak ada peminjaman terlambat.")
            elif pilihan == "4":
                self._cetak_daftar(self.perpus.daftar_peminjaman(), "Belum ada transaksi.")
            elif pilihan == "5":
                berdenda = [a for a in self.perpus.daftar_anggota() if a.total_denda > 0]
                self._cetak_daftar(berdenda, "Tidak ada anggota yang memiliki denda.")
                print(f"Total denda tertunggak: {rupiah(self.perpus.total_denda_tertunggak())}")
            elif pilihan == "6":
                self.tampilkan_struktur_kelas()
            else:
                print("  ! Pilihan tidak tersedia.")

    @staticmethod
    def tampilkan_struktur_kelas():
        """Menampilkan MRO tiap class, berguna saat presentasi konsep inheritance."""
        print("Urutan pencarian method (MRO) tiap class:")
        for kelas in (Buku, Majalah, Referensi, EBook, Mahasiswa, Dosen, Umum, AsistenDosen):
            print(f" - {kelas.__name__:<13}: {urutan_mro(kelas)}")
        print("\nCatatan:")
        print(" - Koleksi & Anggota adalah abstract class (tidak bisa dibuat objeknya langsung).")
        print(" - Referensi : multilevel  (Koleksi -> Buku -> Referensi).")
        print(" - EBook     : multiple    (DigitalMixin + Buku).")
        print(" - AsistenDosen: diamond   (Mahasiswa + Dosen, keduanya turunan Anggota).")
        print(f"   MAKS_PINJAM={AsistenDosen.MAKS_PINJAM} dan DENDA_PER_HARI={AsistenDosen.DENDA_PER_HARI}"
              " diambil dari Mahasiswa karena Mahasiswa lebih dulu di MRO.")
