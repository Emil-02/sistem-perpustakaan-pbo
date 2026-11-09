"""BAGIAN 6 - Class Perpustakaan (composition / has-a) + aturan bisnis + data contoh.

Perpustakaan MEMILIKI koleksi, anggota, dan peminjaman, tetapi BUKAN turunannya.
"""

from datetime import date

from anggota import Anggota, rupiah
from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
from koleksi import Buku, Koleksi
from koleksi_turunan import EBook, Majalah, Referensi
from peminjaman import DataDuplikat, DataTidakDitemukan, Peminjaman, PeminjamanDitolak


class Perpustakaan:
    def __init__(self, nama="Perpustakaan Kampus"):
        self.nama = nama
        # Dibuat di __init__ (bukan class attribute) agar tiap objek punya data sendiri
        self._koleksi = {}  # kode -> Koleksi
        self._anggota = {}  # id -> Anggota
        self._peminjaman = []  # list Peminjaman

    # ===================== KOLEKSI =====================
    def tambah_koleksi(self, koleksi):
        if not isinstance(koleksi, Koleksi):
            raise TypeError("Objek harus turunan Koleksi")
        if koleksi.kode in self._koleksi:
            raise DataDuplikat(f"Kode koleksi {koleksi.kode} sudah terdaftar")
        self._koleksi[koleksi.kode] = koleksi

    def cari_koleksi(self, kode):
        kode = str(kode).strip().upper()
        if kode not in self._koleksi:
            raise DataTidakDitemukan(f"Koleksi dengan kode {kode} tidak ditemukan")
        return self._koleksi[kode]

    def cari_koleksi_kata(self, kata):
        """Cari berdasarkan kode, judul, atau penulis (tidak peka huruf besar/kecil)."""
        kata = kata.strip().lower()
        return [k for k in self._koleksi.values()
                if kata in f"{k.kode} {k.judul} {getattr(k, 'penulis', '')}".lower()]

    def hapus_koleksi(self, kode):
        koleksi = self.cari_koleksi(kode)
        if any(p.aktif and p.koleksi is koleksi for p in self._peminjaman):
            raise PeminjamanDitolak(f"'{koleksi.judul}' masih dipinjam, tidak dapat dihapus")
        return self._koleksi.pop(koleksi.kode)

    def daftar_koleksi(self):
        return list(self._koleksi.values())

    # ===================== ANGGOTA =====================
    def tambah_anggota(self, anggota):
        if not isinstance(anggota, Anggota):
            raise TypeError("Objek harus turunan Anggota")
        if anggota.id in self._anggota:
            raise DataDuplikat(f"ID anggota {anggota.id} sudah terdaftar")
        self._anggota[anggota.id] = anggota

    def cari_anggota(self, id_anggota):
        id_anggota = str(id_anggota).strip().upper()
        if id_anggota not in self._anggota:
            raise DataTidakDitemukan(f"Anggota dengan ID {id_anggota} tidak ditemukan")
        return self._anggota[id_anggota]

    def cari_anggota_kata(self, kata):
        kata = kata.strip().lower()
        return [a for a in self._anggota.values() if kata in f"{a.id} {a.nama}".lower()]

    def hapus_anggota(self, id_anggota):
        anggota = self.cari_anggota(id_anggota)
        if self.pinjaman_aktif(anggota):
            raise PeminjamanDitolak(f"{anggota.nama} masih memiliki pinjaman aktif")
        if anggota.total_denda > 0:
            raise PeminjamanDitolak(f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}")
        return self._anggota.pop(anggota.id)

    def daftar_anggota(self):
        return list(self._anggota.values())

    # ===================== TRANSAKSI =====================
    def pinjaman_aktif(self, anggota=None):
        return [p for p in self._peminjaman
                if p.aktif and (anggota is None or p.anggota is anggota)]

    def pinjam(self, id_anggota, kode_koleksi, tanggal=None):
        tanggal = tanggal or date.today()
        anggota = self.cari_anggota(id_anggota)
        koleksi = self.cari_koleksi(kode_koleksi)
        aktif = self.pinjaman_aktif(anggota)

        if not koleksi.bisa_dipinjam():
            if koleksi.stok > 0:
                raise PeminjamanDitolak(f"{koleksi.jenis()} '{koleksi.judul}' hanya baca di tempat")
            raise PeminjamanDitolak(f"Stok '{koleksi.judul}' sedang habis")
        if anggota.total_denda > 0:
            raise PeminjamanDitolak(f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}")
        if any(p.terlambat(tanggal) for p in aktif):
            raise PeminjamanDitolak(f"{anggota.nama} memiliki pinjaman yang terlambat")
        if len(aktif) >= anggota.MAKS_PINJAM:
            raise PeminjamanDitolak(
                f"{anggota.jenis()} hanya boleh meminjam maksimal {anggota.MAKS_PINJAM} koleksi")
        if any(p.koleksi is koleksi for p in aktif):
            raise PeminjamanDitolak(f"{anggota.nama} sedang meminjam '{koleksi.judul}'")

        koleksi.kurangi_stok()
        transaksi = Peminjaman(f"P{len(self._peminjaman) + 1:04d}", anggota, koleksi, tanggal)
        self._peminjaman.append(transaksi)
        return transaksi

    def cari_peminjaman(self, id_pinjam):
        id_pinjam = str(id_pinjam).strip().upper()
        for p in self._peminjaman:
            if p.id == id_pinjam:
                return p
        raise DataTidakDitemukan(f"Peminjaman {id_pinjam} tidak ditemukan")

    def kembalikan(self, id_pinjam, tanggal=None):
        transaksi = self.cari_peminjaman(id_pinjam)
        if not transaksi.aktif:
            raise PeminjamanDitolak(f"Peminjaman {transaksi.id} sudah dikembalikan")
        denda = transaksi.kembalikan(tanggal)
        transaksi.koleksi.tambah_stok()
        if denda:
            transaksi.anggota.tambah_denda(denda)
        return transaksi

    def bayar_denda(self, id_anggota, jumlah):
        anggota = self.cari_anggota(id_anggota)
        if anggota.total_denda == 0:
            raise PeminjamanDitolak(f"{anggota.nama} tidak memiliki denda")
        return anggota.bayar_denda(jumlah)

    # ===================== LAPORAN =====================
    def daftar_peminjaman(self):
        return list(self._peminjaman)

    def pinjaman_terlambat(self, tanggal=None):
        return [p for p in self.pinjaman_aktif() if p.terlambat(tanggal)]

    def total_denda_tertunggak(self):
        return sum(a.total_denda for a in self._anggota.values())

    def laporan(self, tanggal=None):
        """ringkasan() dipanggil pada semua objek tanpa cek tipe (polymorphism)."""
        baris = [f"=== LAPORAN {self.nama.upper()} ===", "", "-- Koleksi --"]
        baris += [k.ringkasan() for k in self._koleksi.values()] or ["(kosong)"]
        baris += ["", "-- Anggota --"]
        baris += [a.ringkasan() for a in self._anggota.values()] or ["(kosong)"]
        baris += ["", "-- Peminjaman Aktif --"]
        baris += [p.ringkasan(tanggal) for p in self.pinjaman_aktif()] or ["(tidak ada)"]
        baris += [
            "",
            f"Jumlah koleksi         : {len(self._koleksi)} judul",
            f"Jumlah anggota         : {len(self._anggota)}",
            f"Peminjaman aktif       : {len(self.pinjaman_aktif())}",
            f"Peminjaman terlambat   : {len(self.pinjaman_terlambat(tanggal))}",
            f"Total denda tertunggak : {rupiah(self.total_denda_tertunggak())}",
        ]
        return "\n".join(baris)


def buat_data_contoh():
    """Data awal yang dibuat setiap kali program dijalankan (tersimpan di memori)."""
    perpus = Perpustakaan("Perpustakaan Kampus")
    for koleksi in (
        Buku("B001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang Pustaka", stok=3),
        Buku("B002", "Bumi Manusia", 1980, "Pramoedya Ananta Toer", "Hasta Mitra", stok=2),
        Buku("B003", "Pemrograman Python untuk Pemula", 2021, "Budi Raharjo", "Informatika", stok=4),
        Majalah("M001", "Majalah Tempo", 2024, "Edisi Januari", stok=2),
        EBook("E001", "Belajar Python Dasar", 2023, "Tim Penulis", "Penerbit Digital", "PDF", 4.5, stok=5),
        Referensi("R001", "Kamus Besar Bahasa Indonesia", 2016, "Badan Bahasa", "Balai Pustaka"),
    ):
        perpus.tambah_koleksi(koleksi)
    for anggota in (
        Mahasiswa("MHS001", "Nadia", "Informatika", "081234567890", email="nadia@kampus.ac.id"),
        Mahasiswa("MHS002", "Fajar", "Sistem Informasi"),
        Dosen("DSN001", "Ir. Ida, S.Kom., M.T.", "Pemrograman", email="ida@kampus.ac.id"),
        AsistenDosen("ASD001", "Rizky Pratama", "Informatika", "Praktikum PBO"),
        Umum("UMM001", "Budi Santoso", "085600000000"),
    ):
        perpus.tambah_anggota(anggota)
    return perpus
