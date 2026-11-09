"""Penyimpanan data perpustakaan ke file JSON."""

import json
import os
import tempfile
from datetime import date

from .models import Buku, Dosen, Mahasiswa, Majalah, Peminjaman, Referensi, Umum
from .models import anggota_dari_dict, koleksi_dari_dict
from .sistem import Perpustakaan


class PenyimpananJSON:
    def __init__(self, path_file):
        self._path = path_file

    @property
    def path(self):
        return self._path

    def ada(self):
        return os.path.exists(self._path)

    def simpan(self, perpus):
        data = {
            "nama": perpus.nama,
            "koleksi": [k.to_dict() for k in perpus.daftar_koleksi()],
            "anggota": [a.to_dict() for a in perpus.daftar_anggota()],
            "peminjaman": [p.to_dict() for p in perpus.daftar_peminjaman()],
        }
        folder = os.path.dirname(os.path.abspath(self._path))
        os.makedirs(folder, exist_ok=True)
        # Tulis ke file sementara lalu ganti, agar file tidak rusak jika gagal di tengah
        fd, sementara = tempfile.mkstemp(dir=folder, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(sementara, self._path)
        except BaseException:
            if os.path.exists(sementara):
                os.remove(sementara)
            raise

    def muat(self):
        with open(self._path, encoding="utf-8") as f:
            data = json.load(f)

        perpus = Perpustakaan(data.get("nama", "Perpustakaan Kampus"))
        for item in data.get("koleksi", []):
            perpus.tambah_koleksi(koleksi_dari_dict(item))
        for item in data.get("anggota", []):
            perpus.tambah_anggota(anggota_dari_dict(item))
        for item in data.get("peminjaman", []):
            kembali = item.get("tanggal_kembali")
            transaksi = Peminjaman(
                item["id_pinjam"],
                perpus.cari_anggota(item["id_anggota"]),
                perpus.cari_koleksi(item["kode_koleksi"]),
                date.fromisoformat(item["tanggal_pinjam"]),
                date.fromisoformat(item["jatuh_tempo"]),
                date.fromisoformat(kembali) if kembali else None,
                item.get("denda", 0),
            )
            perpus._pulihkan_peminjaman(transaksi)
        return perpus

    def muat_atau_buat(self):
        """Muat data jika file ada; jika belum, buat data contoh lalu simpan."""
        if self.ada():
            return self.muat()
        perpus = buat_data_contoh()
        self.simpan(perpus)
        return perpus


def buat_data_contoh():
    perpus = Perpustakaan("Perpustakaan Kampus")
    perpus.tambah_koleksi(Buku("B001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang Pustaka", "9789793062792", stok=3))
    perpus.tambah_koleksi(Buku("B002", "Bumi Manusia", 1980, "Pramoedya Ananta Toer", "Hasta Mitra", stok=2))
    perpus.tambah_koleksi(Buku("B003", "Pemrograman Python untuk Pemula", 2021, "Budi Raharjo", "Informatika", stok=4))
    perpus.tambah_koleksi(Buku("B004", "Clean Code", 2008, "Robert C. Martin", "Prentice Hall", stok=1))
    perpus.tambah_koleksi(Majalah("M001", "Majalah Tempo", 2024, "Edisi Januari", stok=2))
    perpus.tambah_koleksi(Referensi("R001", "Kamus Besar Bahasa Indonesia", 2016, "Badan Bahasa", "Balai Pustaka", stok=1))

    perpus.tambah_anggota(Mahasiswa("MHS001", "Nadia", "Informatika", "081234567890"))
    perpus.tambah_anggota(Mahasiswa("MHS002", "Fajar", "Sistem Informasi"))
    perpus.tambah_anggota(Dosen("DSN001", "Ir. Ida, S.Kom., M.T.", "Pemrograman"))
    perpus.tambah_anggota(Umum("UMM001", "Budi Santoso", "085600000000"))
    return perpus
