import unittest
from datetime import date

from perpustakaan.models import Buku, Koleksi, Majalah, Referensi, koleksi_dari_dict


class TestKoleksi(unittest.TestCase):
    def setUp(self):
        self.buku = Buku("b001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang", stok=2)

    def test_objek_independen(self):
        lain = Buku("B002", "Bumi Manusia", 1980, "Pramoedya", "Hasta Mitra")
        self.assertIsNot(self.buku, lain)
        self.assertNotEqual(self.buku.judul, lain.judul)

    def test_kode_dinormalisasi_dan_read_only(self):
        self.assertEqual(self.buku.kode, "B001")
        with self.assertRaises(AttributeError):
            self.buku.kode = "B999"

    def test_judul_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            Buku("B003", "   ", 2000, "X", "Y")
        with self.assertRaises(ValueError):
            self.buku.judul = ""
        self.assertEqual(self.buku.judul, "Laskar Pelangi")

    def test_stok_negatif_ditolak(self):
        with self.assertRaises(ValueError):
            self.buku.stok = -1
        with self.assertRaises(ValueError):
            self.buku.stok = True
        self.buku.stok = "5"
        self.assertEqual(self.buku.stok, 5)

    def test_tahun_tidak_valid(self):
        with self.assertRaises(ValueError):
            self.buku.tahun = date.today().year + 1
        with self.assertRaises(ValueError):
            self.buku.tahun = "abc"

    def test_kurangi_dan_tambah_stok(self):
        self.buku.kurangi_stok()
        self.buku.kurangi_stok()
        self.assertEqual(self.buku.stok, 0)
        self.assertFalse(self.buku.bisa_dipinjam())
        with self.assertRaises(ValueError):
            self.buku.kurangi_stok()
        self.buku.tambah_stok()
        self.assertTrue(self.buku.bisa_dipinjam())

    def test_inheritance_dan_polymorphism(self):
        majalah = Majalah("M001", "Tempo", 2024, "Januari")
        referensi = Referensi("R001", "KBBI", 2016, "Badan Bahasa", "Balai Pustaka")
        koleksi = [self.buku, majalah, referensi]
        self.assertEqual([k.jenis() for k in koleksi], ["Buku", "Majalah", "Referensi"])
        self.assertTrue(all(isinstance(k, Koleksi) for k in koleksi))
        self.assertTrue(issubclass(Referensi, Buku))
        self.assertIn("Edisi: Januari", majalah.ringkasan())
        self.assertIn("Penulis: Andrea Hirata", self.buku.ringkasan())

    def test_referensi_tidak_bisa_dipinjam(self):
        referensi = Referensi("R001", "KBBI", 2016, "Badan Bahasa", "Balai Pustaka", stok=3)
        self.assertFalse(referensi.bisa_dipinjam())

    def test_to_dict_dari_dict(self):
        for k in (self.buku, Majalah("M001", "Tempo", 2024, "Jan"),
                  Referensi("R001", "KBBI", 2016, "Badan Bahasa", "BP")):
            salinan = koleksi_dari_dict(k.to_dict())
            self.assertIs(type(salinan), type(k))
            self.assertEqual(salinan.to_dict(), k.to_dict())


if __name__ == "__main__":
    unittest.main()
