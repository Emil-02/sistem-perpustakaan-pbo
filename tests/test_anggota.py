import unittest

from perpustakaan.models import Anggota, Dosen, Mahasiswa, Umum, anggota_dari_dict


class TestAnggota(unittest.TestCase):
    def setUp(self):
        self.mhs = Mahasiswa("mhs001", "Nadia", "Informatika")
        self.dosen = Dosen("DSN001", "Aditya", "Rekayasa Perangkat Lunak")
        self.umum = Umum("UMM001", "Budi")

    def test_id_read_only(self):
        self.assertEqual(self.mhs.id, "MHS001")
        with self.assertRaises(AttributeError):
            self.mhs.id = "X"

    def test_nama_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            Mahasiswa("M2", "  ", "IF")
        with self.assertRaises(ValueError):
            self.mhs.nama = ""

    def test_validasi_email(self):
        self.assertEqual(self.mhs.email, "")  # boleh kosong
        self.mhs.email = " nadia@kampus.ac.id "
        self.assertEqual(self.mhs.email, "nadia@kampus.ac.id")
        for salah in ("nadia", "nadia@kampus", "na dia@kampus.ac.id", "@kampus.ac.id"):
            with self.assertRaises(ValueError):
                self.mhs.email = salah
        self.assertEqual(self.mhs.email, "nadia@kampus.ac.id")
        with self.assertRaises(ValueError):
            Dosen("D9", "Aditya", "AI", email="salah-format")

    def test_aturan_berbeda_per_jenis(self):
        self.assertEqual((Mahasiswa.MAKS_PINJAM, Mahasiswa.LAMA_PINJAM, Mahasiswa.DENDA_PER_HARI), (3, 7, 1000))
        self.assertEqual((Dosen.MAKS_PINJAM, Dosen.LAMA_PINJAM, Dosen.DENDA_PER_HARI), (5, 14, 500))
        self.assertEqual((Umum.MAKS_PINJAM, Umum.LAMA_PINJAM, Umum.DENDA_PER_HARI), (2, 7, 2000))

    def test_polymorphism(self):
        semua = [self.mhs, self.dosen, self.umum]
        self.assertEqual([a.jenis() for a in semua], ["Mahasiswa", "Dosen", "Umum"])
        self.assertTrue(all(isinstance(a, Anggota) for a in semua))
        self.assertIn("Prodi: Informatika", self.mhs.ringkasan())
        self.assertIn("Bidang:", self.dosen.ringkasan())

    def test_denda_private(self):
        self.assertFalse(hasattr(self.mhs, "__total_denda"))
        with self.assertRaises(AttributeError):
            self.mhs.total_denda = 100
        self.mhs.tambah_denda(3000)
        self.assertEqual(self.mhs.total_denda, 3000)
        self.assertEqual(self.mhs._Anggota__total_denda, 3000)  # name mangling

    def test_bayar_denda(self):
        self.mhs.tambah_denda(5000)
        self.assertEqual(self.mhs.bayar_denda(2000), 3000)
        with self.assertRaises(ValueError):
            self.mhs.bayar_denda(10000)
        with self.assertRaises(ValueError):
            self.mhs.bayar_denda(0)
        with self.assertRaises(ValueError):
            self.mhs.tambah_denda(-1)

    def test_to_dict_dari_dict(self):
        self.mhs.tambah_denda(1500)
        for a in (self.mhs, self.dosen, self.umum):
            salinan = anggota_dari_dict(a.to_dict())
            self.assertIs(type(salinan), type(a))
            self.assertEqual(salinan.to_dict(), a.to_dict())


if __name__ == "__main__":
    unittest.main()
