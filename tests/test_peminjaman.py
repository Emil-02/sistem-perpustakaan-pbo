import unittest
from datetime import date, timedelta

from perpustakaan.models import Buku, Dosen, Mahasiswa, Peminjaman, Umum

HARI_INI = date(2026, 11, 9)


class TestPeminjaman(unittest.TestCase):
    def setUp(self):
        self.buku = Buku("B001", "Clean Code", 2008, "Robert C. Martin", "PH")

    def buat(self, anggota):
        return Peminjaman("P0001", anggota, self.buku, HARI_INI)

    def test_jatuh_tempo_sesuai_jenis_anggota(self):
        self.assertEqual(self.buat(Mahasiswa("M1", "Nadia", "IF")).jatuh_tempo, HARI_INI + timedelta(days=7))
        self.assertEqual(self.buat(Dosen("D1", "Aditya", "AI")).jatuh_tempo, HARI_INI + timedelta(days=14))

    def test_tepat_waktu_tanpa_denda(self):
        p = self.buat(Mahasiswa("M1", "Nadia", "IF"))
        self.assertEqual(p.kembalikan(HARI_INI + timedelta(days=7)), 0)
        self.assertFalse(p.aktif)
        self.assertEqual(p.status, Peminjaman.STATUS_KEMBALI)

    def test_denda_keterlambatan_polimorfik(self):
        terlambat = 3
        for anggota, tarif in ((Mahasiswa("M1", "Nadia", "IF"), 1000),
                               (Dosen("D1", "Aditya", "AI"), 500),
                               (Umum("U1", "Budi"), 2000)):
            p = self.buat(anggota)
            tanggal = p.jatuh_tempo + timedelta(days=terlambat)
            self.assertTrue(p.terlambat(tanggal))
            self.assertEqual(p.kembalikan(tanggal), terlambat * tarif)
            self.assertEqual(p.denda, terlambat * tarif)

    def test_tidak_bisa_dikembalikan_dua_kali(self):
        p = self.buat(Mahasiswa("M1", "Nadia", "IF"))
        p.kembalikan(HARI_INI)
        with self.assertRaises(ValueError):
            p.kembalikan(HARI_INI)

    def test_tanggal_kembali_sebelum_pinjam_ditolak(self):
        p = self.buat(Mahasiswa("M1", "Nadia", "IF"))
        with self.assertRaises(ValueError):
            p.kembalikan(HARI_INI - timedelta(days=1))


if __name__ == "__main__":
    unittest.main()
