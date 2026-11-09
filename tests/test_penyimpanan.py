import json
import os
import tempfile
import unittest
from datetime import date, timedelta

from perpustakaan import PenyimpananJSON, buat_data_contoh

HARI_INI = date(2026, 11, 9)


class TestPenyimpanan(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "data", "perpus.json")
        self.penyimpanan = PenyimpananJSON(self.path)

    def tearDown(self):
        self.folder.cleanup()

    def test_buat_data_contoh_jika_file_belum_ada(self):
        self.assertFalse(self.penyimpanan.ada())
        perpus = self.penyimpanan.muat_atau_buat()
        self.assertTrue(self.penyimpanan.ada())
        self.assertGreater(len(perpus.daftar_koleksi()), 0)
        self.assertGreater(len(perpus.daftar_anggota()), 0)

    def test_simpan_lalu_muat_sama(self):
        perpus = buat_data_contoh()
        t1 = perpus.pinjam("MHS001", "B001", HARI_INI)
        perpus.pinjam("DSN001", "B002", HARI_INI)
        perpus.kembalikan(t1.id, t1.jatuh_tempo + timedelta(days=2))
        self.penyimpanan.simpan(perpus)

        hasil = self.penyimpanan.muat()
        self.assertEqual([k.to_dict() for k in hasil.daftar_koleksi()],
                         [k.to_dict() for k in perpus.daftar_koleksi()])
        self.assertEqual([a.to_dict() for a in hasil.daftar_anggota()],
                         [a.to_dict() for a in perpus.daftar_anggota()])
        self.assertEqual([p.to_dict() for p in hasil.daftar_peminjaman()],
                         [p.to_dict() for p in perpus.daftar_peminjaman()])
        self.assertEqual(hasil.cari_anggota("MHS001").total_denda, 2000)
        # Objek peminjaman menunjuk objek anggota/koleksi yang sama di sistem
        aktif = hasil.pinjaman_aktif()[0]
        self.assertIs(aktif.anggota, hasil.cari_anggota("DSN001"))
        # Nomor transaksi berikutnya melanjutkan, bukan mengulang
        self.assertEqual(hasil.pinjam("UMM001", "B003", HARI_INI).id, "P0003")

    def test_file_json_valid(self):
        self.penyimpanan.simpan(buat_data_contoh())
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(set(data), {"nama", "koleksi", "anggota", "peminjaman"})


if __name__ == "__main__":
    unittest.main()
