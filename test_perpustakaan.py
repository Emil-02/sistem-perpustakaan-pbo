"""Unit test seluruh sistem. Jalankan: python -m unittest -v"""

import unittest
from datetime import date, timedelta

from anggota import Anggota, rupiah
from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
from koleksi import Buku, Koleksi
from koleksi_turunan import DigitalMixin, EBook, Majalah, Referensi
from peminjaman import (DataDuplikat, DataTidakDitemukan, Peminjaman,
                        PeminjamanDitolak, PerpustakaanError)
from perpustakaan import Perpustakaan, buat_data_contoh

HARI_INI = date(2024, 1, 1)


def buku(kode="B001", stok=2):
    return Buku(kode, "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang", stok=stok)


# ---------------- Bagian 1: koleksi.py ----------------
class TestKoleksi(unittest.TestCase):
    def test_abstract_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            Koleksi("K1", "Judul", 2000)

    def test_buku_valid(self):
        b = buku("b001")
        self.assertEqual(b.kode, "B001")
        self.assertEqual(b.jenis(), "Buku")
        self.assertIn("Penulis: Andrea Hirata", b.ringkasan())

    def test_kode_read_only(self):
        with self.assertRaises(AttributeError):
            buku().kode = "X"

    def test_validasi_setter(self):
        b = buku()
        for atribut, nilai in [("judul", " "), ("tahun", 1000), ("tahun", True),
                               ("tahun", date.today().year + 1), ("stok", -1), ("stok", "abc")]:
            with self.subTest(atribut=atribut, nilai=nilai), self.assertRaises(ValueError):
                setattr(b, atribut, nilai)

    def test_setter_mengubah_teks_angka(self):
        b = buku()
        b.stok = "5"
        self.assertEqual(b.stok, 5)

    def test_stok(self):
        b = buku(stok=1)
        b.kurangi_stok()
        self.assertFalse(b.bisa_dipinjam())
        with self.assertRaises(ValueError):
            b.kurangi_stok()
        b.tambah_stok()
        self.assertEqual(b.stok, 1)


# ---------------- Bagian 2: koleksi_turunan.py ----------------
class TestKoleksiTurunan(unittest.TestCase):
    def test_majalah_single_inheritance(self):
        m = Majalah("M001", "Tempo", 2024, "Januari")
        self.assertIsInstance(m, Koleksi)
        self.assertNotIsInstance(m, Buku)
        self.assertIn("Edisi: Januari", m.ringkasan())

    def test_referensi_multilevel(self):
        r = Referensi("R001", "KBBI", 2016, "Badan Bahasa", "Balai Pustaka", stok=3)
        self.assertEqual(Referensi.__mro__[1:3], (Buku, Koleksi))
        self.assertFalse(r.bisa_dipinjam())

    def test_ebook_multiple_inheritance(self):
        e = EBook("E001", "Python", 2023, "Tim", "Digital", "epub", "2.5")
        self.assertEqual(EBook.__mro__[1:4], (DigitalMixin, Buku, Koleksi))
        self.assertEqual((e.format_file, e.ukuran_mb), ("EPUB", 2.5))
        self.assertFalse(e.kena_denda())
        self.assertIn("Digital: EPUB", e.ringkasan())
        self.assertIn("Penulis: Tim", e.ringkasan())

    def test_ebook_validasi(self):
        with self.assertRaises(ValueError):
            EBook("E1", "X", 2023, "Tim", "Digital", "DOCX")
        with self.assertRaises(ValueError):
            EBook("E1", "X", 2023, "Tim", "Digital", "PDF", 0)


# ---------------- Bagian 3: anggota.py ----------------
class TestAnggota(unittest.TestCase):
    def test_abstract(self):
        with self.assertRaises(TypeError):
            Anggota("A1", "Nama")

    def test_rupiah(self):
        self.assertEqual(rupiah(32000), "Rp32.000")

    def test_denda_private(self):
        a = Umum("U1", "Budi")
        self.assertFalse(hasattr(a, "__total_denda"))
        with self.assertRaises(AttributeError):
            a.total_denda = 100
        a.tambah_denda(5000)
        self.assertEqual(a.bayar_denda(2000), 3000)
        for salah in (0, 9999, True, 1.5):
            with self.subTest(salah=salah), self.assertRaises(ValueError):
                a.bayar_denda(salah)

    def test_email(self):
        a = Umum("U1", "Budi", email="budi@mail.com")
        self.assertIn("Email: budi@mail.com", a.ringkasan())
        with self.assertRaises(ValueError):
            a.email = "bukan-email"
        a.email = ""
        self.assertEqual(a.email, "")


# ---------------- Bagian 4: anggota_turunan.py ----------------
class TestAnggotaTurunan(unittest.TestCase):
    def test_aturan_tiap_jenis(self):
        data = [(Mahasiswa("M1", "A", "TI"), 3, 7, 1000),
                (Dosen("D1", "B", "AI"), 5, 14, 500),
                (Umum("U1", "C"), 2, 7, 2000)]
        for a, maks, lama, denda in data:
            with self.subTest(jenis=a.jenis()):
                self.assertEqual((a.MAKS_PINJAM, a.LAMA_PINJAM, a.DENDA_PER_HARI),
                                 (maks, lama, denda))

    def test_diamond_mro(self):
        self.assertEqual(AsistenDosen.__mro__,
                         (AsistenDosen, Mahasiswa, Dosen, Anggota, Anggota.__mro__[1], object))

    def test_asisten_dosen(self):
        a = AsistenDosen("asd1", "Rizky", "TI", "PBO", email="r@kampus.ac.id")
        self.assertEqual((a.MAKS_PINJAM, a.LAMA_PINJAM, a.DENDA_PER_HARI), (3, 14, 1000))
        self.assertEqual((a.prodi, a.bidang, a.id), ("TI", "PBO", "ASD1"))
        teks = a.ringkasan()
        self.assertTrue(teks.index("Prodi") < teks.index("Bidang") < teks.index("Email"))


# ---------------- Bagian 5: peminjaman.py ----------------
class TestPeminjaman(unittest.TestCase):
    def test_hirarki_exception(self):
        for kelas in (DataTidakDitemukan, DataDuplikat, PeminjamanDitolak):
            self.assertTrue(issubclass(kelas, PerpustakaanError))

    def test_jatuh_tempo_dan_denda(self):
        p = Peminjaman("P0001", Mahasiswa("M1", "A", "TI"), buku(), HARI_INI)
        self.assertEqual(p.jatuh_tempo, HARI_INI + timedelta(days=7))
        self.assertEqual(p.hitung_denda(HARI_INI + timedelta(days=10)), 3000)
        self.assertEqual(p.kembalikan(HARI_INI + timedelta(days=10)), 3000)
        self.assertEqual(p.status, "Dikembalikan")
        with self.assertRaises(ValueError):
            p.kembalikan()

    def test_ebook_tanpa_denda(self):
        e = EBook("E1", "X", 2023, "Tim", "Digital")
        p = Peminjaman("P0001", Umum("U1", "C"), e, HARI_INI)
        self.assertEqual(p.hitung_denda(HARI_INI + timedelta(days=30)), 0)

    def test_tanggal_kembali_tidak_valid(self):
        p = Peminjaman("P0001", Umum("U1", "C"), buku(), HARI_INI)
        with self.assertRaises(ValueError):
            p.kembalikan(HARI_INI - timedelta(days=1))


# ---------------- Bagian 6: perpustakaan.py ----------------
class TestPerpustakaan(unittest.TestCase):
    def setUp(self):
        self.p = Perpustakaan()
        self.p.tambah_koleksi(buku(stok=5))
        self.p.tambah_koleksi(Referensi("R001", "KBBI", 2016, "Badan", "Balai"))
        self.p.tambah_anggota(Umum("U1", "Budi"))

    def test_tambah_cari_duplikat(self):
        self.assertEqual(self.p.cari_koleksi("b001").kode, "B001")
        with self.assertRaises(DataDuplikat):
            self.p.tambah_koleksi(buku())
        with self.assertRaises(DataTidakDitemukan):
            self.p.cari_anggota("X")
        with self.assertRaises(TypeError):
            self.p.tambah_anggota("bukan anggota")
        self.assertEqual(len(self.p.cari_koleksi_kata("andrea")), 1)

    def test_pinjam_dan_kembali(self):
        t = self.p.pinjam("U1", "B001", HARI_INI)
        self.assertEqual((t.id, self.p.cari_koleksi("B001").stok), ("P0001", 4))
        self.p.kembalikan("P0001", HARI_INI + timedelta(days=9))
        self.assertEqual(self.p.cari_anggota("U1").total_denda, 4000)
        self.assertEqual(self.p.cari_koleksi("B001").stok, 5)
        with self.assertRaises(PeminjamanDitolak):
            self.p.kembalikan("P0001")

    def test_aturan_pinjam(self):
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("U1", "R001")  # referensi
        self.p.pinjam("U1", "B001", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("U1", "B001", HARI_INI)  # judul sama
        self.p.tambah_koleksi(buku("B002"))
        self.p.tambah_koleksi(buku("B003"))
        self.p.pinjam("U1", "B002", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("U1", "B003", HARI_INI)  # batas Umum = 2

    def test_tolak_jika_berdenda_atau_terlambat(self):
        self.p.pinjam("U1", "B001", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.tambah_koleksi(buku("B002"))
            self.p.pinjam("U1", "B002", HARI_INI + timedelta(days=30))
        self.p.kembalikan("P0001", HARI_INI + timedelta(days=8))
        with self.assertRaises(PeminjamanDitolak):
            self.p.pinjam("U1", "B002")
        self.p.bayar_denda("U1", 2000)
        self.assertEqual(self.p.pinjam("U1", "B002").id, "P0002")

    def test_hapus_ditolak_saat_dipinjam(self):
        self.p.pinjam("U1", "B001", HARI_INI)
        with self.assertRaises(PeminjamanDitolak):
            self.p.hapus_koleksi("B001")
        with self.assertRaises(PeminjamanDitolak):
            self.p.hapus_anggota("U1")

    def test_data_contoh_dan_laporan(self):
        perpus = buat_data_contoh()
        self.assertGreaterEqual(len(perpus.daftar_koleksi()), 5)
        self.assertGreaterEqual(len(perpus.daftar_anggota()), 5)
        self.assertIn("LAPORAN", perpus.laporan())


# ---------------- Bagian 7: main.py ----------------
class TestMain(unittest.TestCase):
    def test_teks_mro(self):
        from main import teks_mro
        self.assertEqual(teks_mro(EBook),
                         "EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object")

    def test_menu_bisa_dibuat(self):
        from main import MenuPerpustakaan
        menu = MenuPerpustakaan(buat_data_contoh())
        self.assertEqual(menu.perpus.nama, "Perpustakaan Kampus")


if __name__ == "__main__":
    unittest.main()
