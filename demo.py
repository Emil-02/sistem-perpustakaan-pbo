"""Demo non-interaktif: menampilkan semua konsep PBO secara berurutan.

Jalankan: python demo.py
Demo ini tidak mengubah file data (semua objek hanya ada di memori).
"""

from datetime import date, timedelta

from perpustakaan import Penyimpanan, Perpustakaan
from perpustakaan.exceptions import PerpustakaanError
from perpustakaan.models import (
    Anggota, AsistenDosen, Buku, DigitalMixin, Dosen, EBook, Koleksi,
    Mahasiswa, Majalah, Referensi, Umum,
)
from perpustakaan.utils import rupiah, urutan_mro


def judul(teks):
    print(f"\n=== {teks} ===")


def coba(keterangan, aksi):
    """Menjalankan aksi yang seharusnya gagal, lalu menampilkan pesan error-nya."""
    try:
        aksi()
        print(f"{keterangan}: diterima")
    except (ValueError, TypeError, AttributeError, PerpustakaanError) as err:
        print(f"{keterangan}: DITOLAK -> {type(err).__name__}: {err}")


def main():
    hari_ini = date(2026, 11, 9)

    judul("1. CLASS & OBJECT")
    b1 = Buku("B001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang Pustaka", stok=2)
    b2 = Buku("B002", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang Pustaka", stok=2)
    b3 = b1
    print(b1.ringkasan())
    print("b1 is b2 (isi sama, objek beda) :", b1 is b2)
    print("b1 is b3 (referensi objek sama) :", b1 is b3)
    print("Class attribute Koleksi.TAHUN_MINIMAL :", Koleksi.TAHUN_MINIMAL)
    print("Instance attribute b1.judul           :", b1.judul)

    judul("2. ENKAPSULASI (public, protected, private, property)")
    m = Mahasiswa("MHS001", "Nadia", "Informatika", "0812", email="nadia@kampus.ac.id")
    m.tambah_denda(3000)
    print("Public    m.telepon               :", m.telepon)
    print("Protected m._nama                 :", m._nama, "(bisa diakses, tapi tidak disarankan)")
    print("Private   m.total_denda (property):", rupiah(m.total_denda))
    print("Private   m._Anggota__total_denda :", m._Anggota__total_denda, "(name mangling)")
    print("Akses langsung m.__total_denda    :", hasattr(m, "__total_denda"))
    coba("Setter stok = -5", lambda: setattr(b1, "stok", -5))
    coba("Setter judul = '   '", lambda: setattr(b1, "judul", "   "))
    coba("Setter email = 'nadia'", lambda: setattr(m, "email", "nadia"))
    coba("Ubah kode (read-only)", lambda: setattr(b1, "kode", "X01"))
    coba("Ubah total_denda (read-only)", lambda: setattr(m, "total_denda", 0))
    print("Data tetap valid ->", b1.ringkasan())

    judul("3. ABSTRACTION")
    coba("Koleksi(...) langsung", lambda: Koleksi("K1", "Judul", 2020))
    coba("Anggota(...) langsung", lambda: Anggota("A1", "Nama"))
    coba("Penyimpanan() langsung", lambda: Penyimpanan())

    judul("4. INHERITANCE & MRO")
    for kelas in (Majalah, Referensi, EBook, Mahasiswa, Umum, AsistenDosen):
        print(f"{kelas.__name__:<13}: {urutan_mro(kelas)}")
    print("Single       : Majalah(Koleksi)")
    print("Hierarchical : Mahasiswa, Dosen, Umum -> Anggota")
    print("Multilevel   : Koleksi -> Buku -> Referensi")
    print("Multiple     : EBook(DigitalMixin, Buku)")
    print("Diamond      : AsistenDosen(Mahasiswa, Dosen), keduanya turunan Anggota")
    asd = AsistenDosen("ASD001", "Rizky Pratama", "Informatika", "Praktikum PBO")
    print("isinstance(asd, Mahasiswa), (asd, Dosen):", isinstance(asd, Mahasiswa), isinstance(asd, Dosen))
    print("issubclass(EBook, DigitalMixin)         :", issubclass(EBook, DigitalMixin))
    print("AsistenDosen.MAKS_PINJAM (dari Mahasiswa via MRO):", AsistenDosen.MAKS_PINJAM)
    print("AsistenDosen.LAMA_PINJAM (override)              :", AsistenDosen.LAMA_PINJAM)

    judul("5. POLYMORPHISM (satu pemanggilan, perilaku berbeda)")
    koleksi = [
        b1,
        Majalah("M001", "Majalah Tempo", 2024, "Januari"),
        Referensi("R001", "KBBI", 2016, "Badan Bahasa", "Balai Pustaka"),
        EBook("E001", "Belajar Python", 2023, "Tim Penulis", "Penerbit Digital", "EPUB", 2.5),
    ]
    for k in koleksi:
        print(f"{k.jenis():<9} bisa_dipinjam={k.bisa_dipinjam()!s:<5} kena_denda={k.kena_denda()!s:<5} | {k.ringkasan()}")
    anggota = [m, Dosen("DSN001", "Ir. Ida, S.Kom., M.T.", "Pemrograman"), Umum("UMM001", "Budi"), asd]
    for a in anggota:
        print(a.ringkasan())

    judul("6. COMPOSITION (has-a) + ATURAN BISNIS")
    perpus = Perpustakaan("Perpustakaan Demo")
    for k in koleksi:
        perpus.tambah_koleksi(k)
    for a in anggota:
        perpus.tambah_anggota(a)
    coba("Tambah kode duplikat b001", lambda: perpus.tambah_koleksi(
        Buku("b001", "Buku Lain", 2020, "Penulis", "Penerbit")))
    coba("Pinjam Referensi R001", lambda: perpus.pinjam("UMM001", "R001", hari_ini))
    coba("Nadia pinjam (masih ada denda)", lambda: perpus.pinjam("MHS001", "B001", hari_ini))
    m.bayar_denda(3000)
    t1 = perpus.pinjam("MHS001", "B001", hari_ini)
    t2 = perpus.pinjam("ASD001", "E001", hari_ini)
    print(f"{t1.id}: jatuh tempo {t1.jatuh_tempo} (Mahasiswa 7 hari)")
    print(f"{t2.id}: jatuh tempo {t2.jatuh_tempo} (Asisten Dosen 14 hari)")
    perpus.kembalikan(t1.id, t1.jatuh_tempo + timedelta(days=3))
    perpus.kembalikan(t2.id, t2.jatuh_tempo + timedelta(days=3))
    print(f"{t1.id} terlambat 3 hari -> denda {rupiah(t1.denda)} (buku cetak)")
    print(f"{t2.id} terlambat 3 hari -> denda {rupiah(t2.denda)} (e-book, tanpa denda)")

    judul("7. LAPORAN")
    print(perpus.laporan(hari_ini))


if __name__ == "__main__":
    main()
