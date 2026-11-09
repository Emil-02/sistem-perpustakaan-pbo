"""Pengujian konsep lanjutan: abstraction, multilevel, multiple, diamond, dan MRO."""

import unittest
from datetime import date, timedelta

from perpustakaan import Penyimpanan, Perpustakaan
from perpustakaan.models import (
    Anggota, AsistenDosen, Buku, DigitalMixin, Dosen, EBook, Koleksi,
    Mahasiswa, Referensi, anggota_dari_dict, koleksi_dari_dict,
)
from perpustakaan.utils import urutan_mro

HARI_INI = date(2026, 11, 9)


class TestAbstraction(unittest.TestCase):
    def test_abstract_class_tidak_bisa_dibuat_objek(self):
        with self.assertRaises(TypeError):
            Koleksi("K1", "Judul", 2020)
        with self.assertRaises(TypeError):
            Anggota("A1", "Nama")
        with self.assertRaises(TypeError):
            Penyimpanan()

    def test_subclass_wajib_implementasi_method_abstrak(self):
        class KoleksiTanpaJenis(Koleksi):
            pass

        with self.assertRaises(TypeError):
            KoleksiTanpaJenis("K1", "Judul", 2020)


class TestMultilevel(unittest.TestCase):
    def test_referensi_bertingkat(self):
        r = Referensi("R1", "KBBI", 2016, "Badan Bahasa", "BP")
        self.assertTrue(issubclass(Referensi, Buku) and issubclass(Buku, Koleksi))
        self.assertIsInstance(r, Koleksi)
        self.assertEqual(r.penulis, "Badan Bahasa")  # atribut dari Buku
        self.assertEqual(r.stok, 1)  # atribut dari Koleksi


class TestMultipleInheritance(unittest.TestCase):
    def setUp(self):
        self.ebook = EBook("E1", "Belajar Python", 2023, "Tim", "Digital", "epub", 2.5, stok=2)

    def test_ebook_turunan_dua_parent(self):
        self.assertIsInstance(self.ebook, Buku)
        self.assertIsInstance(self.ebook, DigitalMixin)
        self.assertEqual(EBook.__bases__, (DigitalMixin, Buku))

    def test_mro_ebook(self):
        self.assertEqual(
            urutan_mro(EBook),
            "EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object",
        )

    def test_mixin_memperluas_ringkasan_lewat_super(self):
        teks = self.ebook.ringkasan()
        self.assertIn("Penulis: Tim", teks)  # dari Buku (lanjutan super() di mixin)
        self.assertIn("Digital: EPUB, 2.5 MB", teks)  # dari DigitalMixin
        self.assertIn("E-Book", teks)

    def test_validasi_mixin(self):
        with self.assertRaises(ValueError):
            self.ebook.format_file = "DOCX"
        with self.assertRaises(ValueError):
            self.ebook.ukuran_mb = 0

    def test_ebook_tanpa_denda(self):
        p = Perpustakaan()
        p.tambah_koleksi(self.ebook)
        p.tambah_anggota(Mahasiswa("M1", "Nadia", "IF"))
        t = p.pinjam("M1", "E1", HARI_INI)
        p.kembalikan(t.id, t.jatuh_tempo + timedelta(days=5))
        self.assertEqual(t.denda, 0)
        self.assertEqual(p.cari_anggota("M1").total_denda, 0)

    def test_simpan_dict(self):
        salinan = koleksi_dari_dict(self.ebook.to_dict())
        self.assertIsInstance(salinan, EBook)
        self.assertEqual(salinan.to_dict(), self.ebook.to_dict())


class TestDiamondDanMRO(unittest.TestCase):
    def setUp(self):
        self.asisten = AsistenDosen("ASD1", "Rizky", "Informatika", "Praktikum PBO", total_denda=500)

    def test_bentuk_diamond(self):
        self.assertEqual(AsistenDosen.__bases__, (Mahasiswa, Dosen))
        self.assertIs(Mahasiswa.__bases__[0], Anggota)
        self.assertIs(Dosen.__bases__[0], Anggota)

    def test_mro_asisten(self):
        self.assertEqual(
            AsistenDosen.__mro__,
            (AsistenDosen, Mahasiswa, Dosen, Anggota, Anggota.__mro__[1], object),
        )

    def test_init_kooperatif_mengisi_semua_atribut(self):
        self.assertEqual(self.asisten.prodi, "Informatika")
        self.assertEqual(self.asisten.bidang, "Praktikum PBO")
        # Anggota.__init__ hanya sekali, jadi denda awal tidak terhitung dua kali
        self.assertEqual(self.asisten.total_denda, 500)

    def test_class_attribute_mengikuti_mro(self):
        self.assertEqual(AsistenDosen.MAKS_PINJAM, Mahasiswa.MAKS_PINJAM)
        self.assertEqual(AsistenDosen.DENDA_PER_HARI, Mahasiswa.DENDA_PER_HARI)
        self.assertEqual(AsistenDosen.LAMA_PINJAM, 14)  # override sendiri

    def test_info_tambahan_dari_kedua_jalur(self):
        teks = self.asisten.ringkasan()
        self.assertIn("Asisten Dosen", teks)
        self.assertIn("Prodi: Informatika | Bidang: Praktikum PBO", teks)

    def test_isinstance_kedua_parent(self):
        self.assertIsInstance(self.asisten, Mahasiswa)
        self.assertIsInstance(self.asisten, Dosen)
        self.assertIsInstance(self.asisten, Anggota)

    def test_jatuh_tempo_dan_simpan_dict(self):
        self.asisten.bayar_denda(500)
        p = Perpustakaan()
        p.tambah_koleksi(Buku("B1", "Clean Code", 2008, "Martin", "PH"))
        p.tambah_anggota(self.asisten)
        t = p.pinjam("ASD1", "B1", HARI_INI)
        self.assertEqual(t.jatuh_tempo, HARI_INI + timedelta(days=14))
        salinan = anggota_dari_dict(self.asisten.to_dict())
        self.assertIsInstance(salinan, AsistenDosen)
        self.assertEqual(salinan.to_dict(), self.asisten.to_dict())


if __name__ == "__main__":
    unittest.main()
