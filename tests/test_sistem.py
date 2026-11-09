import unittest
from datetime import date, timedelta

from perpustakaan import Perpustakaan
from perpustakaan.exceptions import DataDuplikat, DataTidakDitemukan, PeminjamanDitolak, PerpustakaanError
from perpustakaan.models import Buku, Dosen, Mahasiswa, Majalah, Referensi, Umum

HARI_INI = date(2026, 11, 9)


class TestPerpustakaan(unittest.TestCase):
    def setUp(self):
        self.p = Perpustakaan("Perpus Uji")
        self.p.tambah_koleksi(Buku("B001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang", stok=2))
        self.p.tambah_koleksi(Buku("B002", "Bumi Manusia", 1980, "Pramoedya", "Hasta Mitra", stok=1))
        self.p.tambah_koleksi(Buku("B003", "Clean Code", 2008, "Robert C. Martin", "PH", stok=5))
        self.p.tambah_koleksi(Majalah("M001", "Tempo", 2024, "Januari", stok=3))
        self.p.tambah_koleksi(Referensi("R001", "KBBI", 2016, "Badan Bahasa", "BP", stok=1))
        self.p.tambah_anggota(Mahasiswa("MHS001", "Nadia", "Informatika"))
        self.p.tambah_anggota(Dosen("DSN001", "Aditya", "AI"))
        self.p.tambah_anggota(Umum("UMM001", "Budi"))

    def test_exception_turunan_perpustakaan_error(self):
        for exc in (DataDuplikat, DataTidakDitemukan, PeminjamanDitolak):
            self.assertTrue(issubclass(exc, PerpustakaanError))

    def test_duplikat_ditolak(self):
        with self.assertRaises(DataDuplikat):
            self.p.tambah_koleksi(Buku("b001", "Lain", 2000, "X", "Y"))
        with self.assertRaises(DataDuplikat):
            self.p.tambah_anggota(Umum("mhs001", "Lain"))

    def test_tipe_salah_ditolak(self):
        with self.assertRaises(TypeError):
            self.p.tambah_koleksi("bukan koleksi")
        with self.assertRaises(TypeError):
            self.p.tambah_anggota(object())

    def test_cari(self):
        self.assertEqual(self.p.cari_koleksi("b001").judul, "Laskar Pelangi")
        self.assertEqual(len(self.p.cari_koleksi_kata("pramoedya")), 1)
        self.assertEqual(len(self.p.cari_anggota_kata("nad")), 1)
        with self.assertRaises(DataTidakDitemukan):
            self.p.cari_koleksi("X999")
        with self.assertRaises(DataTidakDitemukan):
            self.p.cari_anggota("X999")

    def test_ubah(self):
        self.p.ubah_koleksi("B001", judul="Sang Pemimpi", stok="4")
        self.assertEqual(self.p.cari_koleksi("B001").judul, "Sang Pemimpi")
        self.assertEqual(self.p.cari_koleksi("B001").stok, 4)
        with self.assertRaises(ValueError):
            self.p.ubah_koleksi("B001", kode="B999")
        with self.assertRaises(ValueError):
            self.p.ubah_anggota("MHS001", total_denda=0)
        self.p.ubah_anggota("MHS001", prodi="Sistem Informasi")
        self.assertEqual(self.p.cari_anggota("MHS001").prodi, "Sistem Informasi")

    def test_ubah_gagal_dibatalkan_semua(self):
        with self.assertRaises(ValueError):
            self.p.ubah_koleksi("B001", judul="Judul Baru", stok=-1)
        buku = self.p.cari_koleksi("B001")
        self.assertEqual((buku.judul, buku.stok), ("Laskar Pelangi", 2))

    def test_pinjam_mengurangi_stok(self):
        t = self.p.pinjam("MHS001", "B001", HARI_INI)
        self.assertEqual(t.id, "P0001")
        self.assertEqual(self.p.cari_koleksi("B001").stok, 1)
        self.assertEqual(len(self.p.pinjaman_aktif()), 1)

    def test_stok_habis(self):
        self.p.pinjam("MHS001", "B002", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("DSN001", "B002", HARI_INI)

    def test_referensi_ditolak(self):
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("MHS001", "R001", HARI_INI)

    def test_batas_maksimal_per_jenis(self):
        self.p.pinjam("UMM001", "B001", HARI_INI)
        self.p.pinjam("UMM001", "B003", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("UMM001", "M001", HARI_INI)  # Umum maks 2
        self.p.pinjam("MHS001", "B001", HARI_INI)
        self.p.pinjam("MHS001", "B003", HARI_INI)
        self.p.pinjam("MHS001", "M001", HARI_INI)  # Mahasiswa boleh 3

    def test_tidak_boleh_pinjam_judul_sama_bersamaan(self):
        self.p.pinjam("DSN001", "B003", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("DSN001", "B003", HARI_INI)

    def test_kembali_terlambat_menambah_denda(self):
        t = self.p.pinjam("MHS001", "B001", HARI_INI)
        self.p.kembalikan(t.id, t.jatuh_tempo + timedelta(days=4))
        nadia = self.p.cari_anggota("MHS001")
        self.assertEqual(nadia.total_denda, 4000)
        self.assertEqual(self.p.cari_koleksi("B001").stok, 2)
        with self.assertRaises(PeminjamanDitolak):
            self.p.kembalikan(t.id, HARI_INI)

    def test_denda_atau_terlambat_memblokir_pinjam(self):
        t = self.p.pinjam("MHS001", "B001", HARI_INI)
        terlambat = t.jatuh_tempo + timedelta(days=1)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("MHS001", "B003", terlambat)
        self.p.kembalikan(t.id, terlambat)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("MHS001", "B003", terlambat)
        self.p.bayar_denda("MHS001", 1000)
        self.p.pinjam("MHS001", "B003", terlambat)

    def test_bayar_denda_tanpa_denda_ditolak(self):
        with self.assertRaises(PeminjamanDitolak):
            self.p.bayar_denda("DSN001", 1000)

    def test_hapus_dengan_pinjaman_aktif_ditolak(self):
        t = self.p.pinjam("MHS001", "B001", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.hapus_koleksi("B001")
        with self.assertRaises(PeminjamanDitolak):
            self.p.hapus_anggota("MHS001")
        self.p.kembalikan(t.id, HARI_INI)
        self.p.hapus_anggota("MHS001")
        self.p.hapus_koleksi("B001")
        with self.assertRaises(DataTidakDitemukan):
            self.p.cari_koleksi("B001")

    def test_laporan(self):
        t = self.p.pinjam("MHS001", "B001", HARI_INI)
        teks = self.p.laporan(t.jatuh_tempo + timedelta(days=2))
        self.assertIn("Laskar Pelangi", teks)
        self.assertIn("TERLAMBAT 2 hari", teks)
        self.assertEqual(len(self.p.pinjaman_terlambat(t.jatuh_tempo + timedelta(days=2))), 1)


if __name__ == "__main__":
    unittest.main()
