# Penjelasan Baris per Baris: test_perpustakaan.py

| Info | Nilai |
|---|---|
| File | `test_perpustakaan.py` |
| Jumlah baris | 243 |
| Jumlah test | 29 (dalam 7 class) |
| Cara menjalankan | `python -m unittest -v` |

| Bagian | Class test | File yang diuji | Jumlah test | Baris | Presenter |
|---|---|---|---|---|---|
| 1 | `TestKoleksi` | `koleksi.py` | 6 | 21–58 | Orang 1 |
| 2 | `TestKoleksiTurunan` | `koleksi_turunan.py` | 4 | 59–86 | Orang 2 |
| 3 | `TestAnggota` | `anggota.py` | 4 | 87–115 | Orang 3 |
| 4 | `TestAnggotaTurunan` | `anggota_turunan.py` | 3 | 116–138 | Orang 4 |
| 5 | `TestPeminjaman` | `peminjaman.py` | 4 | 139–164 | Orang 5 |
| 6 | `TestPerpustakaan` | `perpustakaan.py` | 6 | 165–228 | Orang 6 |
| 7 | `TestMain` | `main.py` | 2 | 229–241 | Orang 7 |

## Gambaran Umum

- **Unit test** adalah kode kecil yang menguji satu bagian program (satu "unit", mis. satu method) secara otomatis. Test memanggil kode lalu **membandingkan hasil nyata dengan hasil yang diharapkan**. Keuntungannya: setiap kali kode diubah, kita cukup menjalankan test untuk tahu apakah ada fitur yang rusak, tanpa mencoba menu satu per satu.
- **`unittest`** adalah modul pengujian bawaan Python. Cara pakainya juga menerapkan PBO: kita membuat class yang **mewarisi** `unittest.TestCase`, lalu menulis method yang namanya diawali `test`. Di dalamnya dipakai method *assert* warisan `TestCase`, misalnya:
  - `assertEqual(a, b)` → lulus jika `a == b`
  - `assertTrue(x)` / `assertFalse(x)` → lulus jika `x` bernilai `True` / `False`
  - `assertIn(a, b)` → lulus jika `a in b`
  - `assertIsInstance(obj, Kelas)` / `assertNotIsInstance(...)` → mengecek `isinstance`
  - `assertGreaterEqual(a, b)` → lulus jika `a >= b`
  - `with self.assertRaises(Error):` → lulus hanya jika kode di dalam blok melempar `Error`
  - `with self.subTest(...):` → membagi perulangan menjadi sub-test yang dilaporkan terpisah
  - `setUp()` → dijalankan otomatis sebelum setiap test
- **Cara menjalankan** (dari folder repo):
  - `python -m unittest -v` → mencari semua file `test*.py` lalu menjalankannya; `-v` (*verbose*) menampilkan nama setiap test.
  - `python test_perpustakaan.py` → juga bisa, karena ada `unittest.main()` di akhir file.
  - `python -m unittest test_perpustakaan.TestKoleksi -v` → hanya menjalankan satu bagian (berguna saat presentasi per orang).
- **Arti hasil:** setiap test yang lulus ditandai `ok`. Di akhir muncul `Ran 29 tests` dan **`OK`**, artinya semua test lulus. Jika ada yang gagal, muncul `FAIL` (hasil assert tidak sesuai) atau `ERROR` (terjadi exception yang tidak diharapkan), beserta baris penyebabnya.
- Test memakai tanggal tetap `HARI_INI = date(2024, 1, 1)` agar perhitungan jatuh tempo dan denda selalu sama.

## Baris 1–20: Import, Konstanta, dan Fungsi Bantu (dipakai semua bagian)

Bagian awal ini dipakai bersama oleh ketujuh class test.

```python
  1 | """Unit test seluruh sistem. Jalankan: python -m unittest -v"""
  2 |
  3 | import unittest
  4 | from datetime import date, timedelta
  5 |
  6 | from anggota import Anggota, rupiah
  7 | from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
  8 | from koleksi import Buku, Koleksi
  9 | from koleksi_turunan import DigitalMixin, EBook, Majalah, Referensi
 10 | from peminjaman import (DataDuplikat, DataTidakDitemukan, Peminjaman,
 11 |                         PeminjamanDitolak, PerpustakaanError)
 12 | from perpustakaan import Perpustakaan, buat_data_contoh
 13 |
 14 | HARI_INI = date(2024, 1, 1)
 15 |
 16 |
 17 | def buku(kode="B001", stok=2):
 18 |     return Buku(kode, "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang", stok=stok)
 19 |
 20 |
```

- **Baris 1** — Docstring modul (teks di dalam tiga tanda kutip). Menjelaskan isi file: unit test untuk seluruh sistem, sekaligus cara menjalankannya: `python -m unittest -v`.
- **Baris 3** — Mengimpor modul `unittest`, *framework* pengujian bawaan Python (tidak perlu `pip install`). Dari modul ini kita memakai class `TestCase` dan fungsi `unittest.main()`.
- **Baris 4** — Mengimpor `date` (tipe tanggal) dan `timedelta` (selisih waktu, mis. `timedelta(days=7)` = 7 hari) dari modul `datetime`. Dipakai untuk menguji jatuh tempo dan denda.
- **Baris 6** — Mengimpor class abstract `Anggota` dan fungsi `rupiah()` dari `anggota.py` (Bagian 3).
- **Baris 7** — Mengimpor empat subclass anggota dari `anggota_turunan.py` (Bagian 4): `AsistenDosen`, `Dosen`, `Mahasiswa`, `Umum`.
- **Baris 8** — Mengimpor class `Buku` dan class abstract `Koleksi` dari `koleksi.py` (Bagian 1).
- **Baris 9** — Mengimpor `DigitalMixin`, `EBook`, `Majalah`, `Referensi` dari `koleksi_turunan.py` (Bagian 2).
- **Baris 10** — Awal import dari `peminjaman.py` (Bagian 5). Tanda kurung `(` dipakai agar daftar nama yang panjang boleh dipecah ke beberapa baris. Yang diimpor di baris ini: exception `DataDuplikat`, `DataTidakDitemukan`, dan class `Peminjaman`.
- **Baris 11** — Lanjutan baris 10: exception `PeminjamanDitolak` dan induknya `PerpustakaanError`. Kurung tutup `)` mengakhiri pernyataan import.
- **Baris 12** — Mengimpor class `Perpustakaan` dan fungsi `buat_data_contoh()` dari `perpustakaan.py` (Bagian 6).
- **Baris 14** — Konstanta `HARI_INI` = 1 Januari 2024. Test memakai tanggal **tetap**, bukan `date.today()`, supaya hasil hitungan jatuh tempo/denda selalu sama kapan pun test dijalankan (test menjadi *deterministik*). Nama huruf besar = konvensi konstanta.
- **Baris 17** — Fungsi bantu (*helper*) `buku()` dengan parameter default `kode="B001"` dan `stok=2`. Tujuannya agar setiap test tidak perlu menulis ulang 6 argumen `Buku` yang panjang.
- **Baris 18** — Mengembalikan objek `Buku` baru (kode, judul "Laskar Pelangi", tahun 2005, penulis "Andrea Hirata", penerbit "Bentang", stok). Karena dibuat baru setiap dipanggil, test yang satu tidak memengaruhi test lain.
- **Baris 2, 5, 13, 15–16, 19–20** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 21–58: Bagian 1 — TestKoleksi (Orang 1)

Menguji `koleksi.py`: abstract class `Koleksi`, class `Buku`, property (getter/setter), validasi, dan stok. Berisi 6 test.

```python
 21 | # ---------------- Bagian 1: koleksi.py ----------------
 22 | class TestKoleksi(unittest.TestCase):
 23 |     def test_abstract_tidak_bisa_dibuat(self):
 24 |         with self.assertRaises(TypeError):
 25 |             Koleksi("K1", "Judul", 2000)
 26 |
 27 |     def test_buku_valid(self):
 28 |         b = buku("b001")
 29 |         self.assertEqual(b.kode, "B001")
 30 |         self.assertEqual(b.jenis(), "Buku")
 31 |         self.assertIn("Penulis: Andrea Hirata", b.ringkasan())
 32 |
 33 |     def test_kode_read_only(self):
 34 |         with self.assertRaises(AttributeError):
 35 |             buku().kode = "X"
 36 |
 37 |     def test_validasi_setter(self):
 38 |         b = buku()
 39 |         for atribut, nilai in [("judul", " "), ("tahun", 1000), ("tahun", True),
 40 |                                ("tahun", date.today().year + 1), ("stok", -1), ("stok", "abc")]:
 41 |             with self.subTest(atribut=atribut, nilai=nilai), self.assertRaises(ValueError):
 42 |                 setattr(b, atribut, nilai)
 43 |
 44 |     def test_setter_mengubah_teks_angka(self):
 45 |         b = buku()
 46 |         b.stok = "5"
 47 |         self.assertEqual(b.stok, 5)
 48 |
 49 |     def test_stok(self):
 50 |         b = buku(stok=1)
 51 |         b.kurangi_stok()
 52 |         self.assertFalse(b.bisa_dipinjam())
 53 |         with self.assertRaises(ValueError):
 54 |             b.kurangi_stok()
 55 |         b.tambah_stok()
 56 |         self.assertEqual(b.stok, 1)
 57 |
 58 |
```

- **Baris 21** — Komentar penanda: mulai Bagian 1, menguji `koleksi.py`.
- **Baris 22** — Class test `TestKoleksi` **mewarisi** `unittest.TestCase` (contoh *inheritance*). Dari induknya kita mendapat method `assertEqual`, `assertRaises`, dll. `unittest` otomatis menjalankan setiap method yang namanya diawali `test`.
- **Baris 23** — Test 1: memastikan class abstract `Koleksi` tidak bisa dibuat objeknya.
- **Baris 24** — `with self.assertRaises(TypeError):` dipakai sebagai *context manager*: test **lulus** hanya jika kode di dalam blok `with` melempar `TypeError`. Jika tidak ada error, test gagal.
- **Baris 25** — Mencoba membuat `Koleksi(...)` langsung. Karena `Koleksi` turunan `ABC` dan punya `@abstractmethod jenis()` yang belum diisi, Python melempar `TypeError: Can't instantiate abstract class...` → test lulus.
- **Baris 27** — Test 2: membuat buku yang valid dan memeriksa datanya.
- **Baris 28** — Membuat buku dengan kode huruf kecil `"b001"`.
- **Baris 29** — `assertEqual(a, b)` lulus jika `a == b`. Kode harus menjadi `"B001"` karena di `Koleksi.__init__` kode diproses `.upper()`.
- **Baris 30** — Method `jenis()` milik `Buku` (implementasi method abstract) harus mengembalikan `"Buku"`.
- **Baris 31** — `assertIn(x, y)` lulus jika `x in y`. `ringkasan()` milik `Buku` meng-*override* ringkasan `Koleksi` dan menambahkan `"Penulis: Andrea Hirata"`.
- **Baris 33** — Test 3: atribut `kode` harus *read-only*.
- **Baris 34** — Mengharapkan `AttributeError`.
- **Baris 35** — Mencoba mengisi `kode`. Property `kode` hanya punya getter (tidak ada `@kode.setter`), sehingga Python melempar `AttributeError` → test lulus.
- **Baris 37** — Test 4: setter harus menolak semua nilai yang tidak valid.
- **Baris 38** — Membuat satu buku valid yang akan dicoba diisi nilai salah.
- **Baris 39** — Perulangan `for` atas daftar pasangan `(atribut, nilai)` yang **salah**: judul `" "` (hanya spasi → kosong setelah `strip()`), tahun `1000` (< `TAHUN_MINIMAL` 1450), tahun `True` (bool ditolak oleh `angka_bulat` walaupun `bool` turunan `int`).
- **Baris 40** — Lanjutan daftar: tahun depan `date.today().year + 1` (melebihi tahun ini), stok `-1` (negatif), stok `"abc"` (tidak bisa diubah ke `int`). Semuanya harus menghasilkan `ValueError`.
- **Baris 41** — Dua *context manager* dalam satu `with`: `self.subTest(...)` membuat setiap pasangan dilaporkan sebagai sub-test tersendiri (jika satu gagal, yang lain tetap dicek dan laporan menyebut atribut/nilai yang gagal); `self.assertRaises(ValueError)` mengharuskan baris berikutnya melempar `ValueError`.
- **Baris 42** — `setattr(b, atribut, nilai)` sama dengan `b.judul = nilai` / `b.tahun = nilai` / `b.stok = nilai`, tetapi nama atributnya berupa string. Pengisian ini memicu **setter property** yang berisi validasi.
- **Baris 44** — Test 5: setter boleh menerima angka dalam bentuk teks.
- **Baris 45** — Membuat buku baru.
- **Baris 46** — Mengisi stok dengan string `"5"`.
- **Baris 47** — Setter `stok` memanggil `angka_bulat()` yang melakukan `int("5")`, sehingga stok tersimpan sebagai angka `5` (bukan string).
- **Baris 49** — Test 6: logika pengurangan dan penambahan stok.
- **Baris 50** — Buku dengan stok 1.
- **Baris 51** — `kurangi_stok()` → stok menjadi 0.
- **Baris 52** — `assertFalse` lulus jika nilainya `False`. `bisa_dipinjam()` mengembalikan `self._stok > 0` → `0 > 0` = `False`.
- **Baris 53** — Mengharapkan `ValueError` untuk pengurangan berikutnya.
- **Baris 54** — Stok sudah 0, `kurangi_stok()` melempar `ValueError("Stok '...' habis")` sehingga stok tidak pernah negatif.
- **Baris 55** — `tambah_stok()` → stok kembali dari 0 menjadi 1.
- **Baris 56** — Memastikan stok sekarang `1`.
- **Baris 26, 32, 36, 43, 48, 57–58** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 59–86: Bagian 2 — TestKoleksiTurunan (Orang 2)

Menguji `koleksi_turunan.py`: single inheritance (`Majalah`), multilevel (`Referensi`), dan multiple inheritance/mixin (`EBook`). Berisi 4 test.

```python
 59 | # ---------------- Bagian 2: koleksi_turunan.py ----------------
 60 | class TestKoleksiTurunan(unittest.TestCase):
 61 |     def test_majalah_single_inheritance(self):
 62 |         m = Majalah("M001", "Tempo", 2024, "Januari")
 63 |         self.assertIsInstance(m, Koleksi)
 64 |         self.assertNotIsInstance(m, Buku)
 65 |         self.assertIn("Edisi: Januari", m.ringkasan())
 66 |
 67 |     def test_referensi_multilevel(self):
 68 |         r = Referensi("R001", "KBBI", 2016, "Badan Bahasa", "Balai Pustaka", stok=3)
 69 |         self.assertEqual(Referensi.__mro__[1:3], (Buku, Koleksi))
 70 |         self.assertFalse(r.bisa_dipinjam())
 71 |
 72 |     def test_ebook_multiple_inheritance(self):
 73 |         e = EBook("E001", "Python", 2023, "Tim", "Digital", "epub", "2.5")
 74 |         self.assertEqual(EBook.__mro__[1:4], (DigitalMixin, Buku, Koleksi))
 75 |         self.assertEqual((e.format_file, e.ukuran_mb), ("EPUB", 2.5))
 76 |         self.assertFalse(e.kena_denda())
 77 |         self.assertIn("Digital: EPUB", e.ringkasan())
 78 |         self.assertIn("Penulis: Tim", e.ringkasan())
 79 |
 80 |     def test_ebook_validasi(self):
 81 |         with self.assertRaises(ValueError):
 82 |             EBook("E1", "X", 2023, "Tim", "Digital", "DOCX")
 83 |         with self.assertRaises(ValueError):
 84 |             EBook("E1", "X", 2023, "Tim", "Digital", "PDF", 0)
 85 |
 86 |
```

- **Baris 59** — Komentar penanda: mulai Bagian 2, menguji `koleksi_turunan.py`.
- **Baris 60** — Class test `TestKoleksiTurunan`, juga turunan `unittest.TestCase`.
- **Baris 61** — Test 1: *single inheritance* `Koleksi → Majalah`.
- **Baris 62** — Membuat `Majalah` kode M001, judul "Tempo", tahun 2024, edisi "Januari".
- **Baris 63** — `assertIsInstance(obj, Kelas)` lulus jika `isinstance(obj, Kelas)` bernilai `True`. Majalah adalah (*is-a*) Koleksi.
- **Baris 64** — `assertNotIsInstance`: Majalah **bukan** Buku, karena `Majalah` langsung turun dari `Koleksi`, bukan dari `Buku`.
- **Baris 65** — Ringkasan `Majalah` (override + `super().ringkasan()`) harus memuat `"Edisi: Januari"`.
- **Baris 67** — Test 2: *multilevel inheritance* `Koleksi → Buku → Referensi`.
- **Baris 68** — Membuat `Referensi` (kamus KBBI) dengan stok 3.
- **Baris 69** — `Referensi.__mro__` = `(Referensi, Buku, Koleksi, ABC, object)`. *Slicing* `[1:3]` mengambil indeks 1 dan 2 → `(Buku, Koleksi)`, membuktikan urutan pewarisan bertingkat.
- **Baris 70** — Walaupun stok 3, `bisa_dipinjam()` di-*override* oleh `Referensi` untuk selalu mengembalikan `False` (baca di tempat).
- **Baris 72** — Test 3: *multiple inheritance* `EBook(DigitalMixin, Buku)`.
- **Baris 73** — Membuat `EBook` dengan format `"epub"` (huruf kecil) dan ukuran `"2.5"` (string).
- **Baris 74** — `EBook.__mro__` = `(EBook, DigitalMixin, Buku, Koleksi, ABC, object)`; `[1:4]` → `(DigitalMixin, Buku, Koleksi)`. Mixin diperiksa lebih dulu daripada `Buku` karena ditulis paling kiri.
- **Baris 75** — Membandingkan dua nilai sekaligus dalam bentuk tuple: setter `format_file` mengubah `"epub"` menjadi `"EPUB"` (`.upper()`), setter `ukuran_mb` mengubah `"2.5"` menjadi float `2.5`.
- **Baris 76** — `kena_denda()` milik `DigitalMixin` mengembalikan `False`; karena Mixin lebih dulu di MRO, versi ini yang dipakai (bukan `True` milik `Koleksi`).
- **Baris 77** — Ringkasan memuat bagian dari Mixin: `"Digital: EPUB"`.
- **Baris 78** — Ringkasan juga memuat bagian dari `Buku`: `"Penulis: Tim"`. Baris 77–78 membuktikan `super().ringkasan()` di Mixin meneruskan ke `Buku` sesuai MRO, sehingga kedua induk ikut menyumbang teks.
- **Baris 80** — Test 4: validasi khusus e-book.
- **Baris 81** — Mengharapkan `ValueError`.
- **Baris 82** — Format `"DOCX"` tidak ada di `FORMAT_DIDUKUNG = ("PDF", "EPUB", "MOBI")` → `ValueError`.
- **Baris 83** — Mengharapkan `ValueError` lagi.
- **Baris 84** — Format `"PDF"` valid, tetapi ukuran `0` ditolak karena setter mensyaratkan `nilai > 0`.
- **Baris 66, 71, 79, 85–86** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 87–115: Bagian 3 — TestAnggota (Orang 3)

Menguji `anggota.py`: abstract class `Anggota`, fungsi `rupiah()`, atribut private `__total_denda`, dan validasi email. Berisi 4 test.

```python
 87 | # ---------------- Bagian 3: anggota.py ----------------
 88 | class TestAnggota(unittest.TestCase):
 89 |     def test_abstract(self):
 90 |         with self.assertRaises(TypeError):
 91 |             Anggota("A1", "Nama")
 92 |
 93 |     def test_rupiah(self):
 94 |         self.assertEqual(rupiah(32000), "Rp32.000")
 95 |
 96 |     def test_denda_private(self):
 97 |         a = Umum("U1", "Budi")
 98 |         self.assertFalse(hasattr(a, "__total_denda"))
 99 |         with self.assertRaises(AttributeError):
100 |             a.total_denda = 100
101 |         a.tambah_denda(5000)
102 |         self.assertEqual(a.bayar_denda(2000), 3000)
103 |         for salah in (0, 9999, True, 1.5):
104 |             with self.subTest(salah=salah), self.assertRaises(ValueError):
105 |                 a.bayar_denda(salah)
106 |
107 |     def test_email(self):
108 |         a = Umum("U1", "Budi", email="budi@mail.com")
109 |         self.assertIn("Email: budi@mail.com", a.ringkasan())
110 |         with self.assertRaises(ValueError):
111 |             a.email = "bukan-email"
112 |         a.email = ""
113 |         self.assertEqual(a.email, "")
114 |
115 |
```

- **Baris 87** — Komentar penanda: mulai Bagian 3, menguji `anggota.py`.
- **Baris 88** — Class test `TestAnggota`.
- **Baris 89** — Test 1: `Anggota` adalah abstract class.
- **Baris 90** — Mengharapkan `TypeError`.
- **Baris 91** — `Anggota` turunan `ABC` dengan `@abstractmethod jenis()`, jadi tidak bisa dibuat objeknya langsung.
- **Baris 93** — Test 2: fungsi format Rupiah.
- **Baris 94** — `f"{32000:,}"` menghasilkan `"32,000"`, lalu koma diganti titik → `"32.000"`, diberi awalan → `"Rp32.000"`.
- **Baris 96** — Test 3: enkapsulasi atribut **private** `__total_denda`.
- **Baris 97** — Membuat anggota `Umum` (denda awal 0).
- **Baris 98** — `hasattr(obj, nama)` mengecek apakah atribut ada. Hasilnya `False` karena *name mangling*: Python menyimpan `self.__total_denda` dengan nama `_Anggota__total_denda`, sehingga nama `__total_denda` tidak bisa diakses langsung dari luar class.
- **Baris 99** — Mengharapkan `AttributeError`.
- **Baris 100** — Property `total_denda` hanya punya getter (read-only), jadi pengisian langsung ditolak. Denda hanya boleh diubah lewat method.
- **Baris 101** — Menambah denda 5000 lewat method resmi → total 5000.
- **Baris 102** — `bayar_denda(2000)` mengembalikan sisa denda: 5000 − 2000 = `3000`.
- **Baris 103** — Perulangan atas nilai pembayaran yang **salah** (sisa denda sekarang 3000): `0` (harus > 0), `9999` (melebihi sisa 3000), `True` (bool ditolak), `1.5` (bukan bilangan bulat).
- **Baris 104** — Setiap nilai dijalankan sebagai `subTest` dan harus melempar `ValueError`.
- **Baris 105** — Pemanggilan `bayar_denda(salah)` yang diharapkan gagal.
- **Baris 107** — Test 4: validasi email.
- **Baris 108** — Membuat anggota dengan email valid (argumen keyword `email=`).
- **Baris 109** — `info_tambahan()` menambahkan `"Email: ..."` ke ringkasan bila email diisi.
- **Baris 110** — Mengharapkan `ValueError`.
- **Baris 111** — `"bukan-email"` tidak cocok dengan pola regex `_POLA_EMAIL` (tidak ada `@` dan domain) → ditolak.
- **Baris 112** — Email kosong `""` diperbolehkan (email bersifat opsional).
- **Baris 113** — Memastikan email benar-benar tersimpan sebagai string kosong.
- **Baris 92, 95, 106, 114–115** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 116–138: Bagian 4 — TestAnggotaTurunan (Orang 4)

Menguji `anggota_turunan.py`: aturan tiap jenis anggota (hierarchical), diamond inheritance, dan MRO `AsistenDosen`. Berisi 3 test.

```python
116 | # ---------------- Bagian 4: anggota_turunan.py ----------------
117 | class TestAnggotaTurunan(unittest.TestCase):
118 |     def test_aturan_tiap_jenis(self):
119 |         data = [(Mahasiswa("M1", "A", "TI"), 3, 7, 1000),
120 |                 (Dosen("D1", "B", "AI"), 5, 14, 500),
121 |                 (Umum("U1", "C"), 2, 7, 2000)]
122 |         for a, maks, lama, denda in data:
123 |             with self.subTest(jenis=a.jenis()):
124 |                 self.assertEqual((a.MAKS_PINJAM, a.LAMA_PINJAM, a.DENDA_PER_HARI),
125 |                                  (maks, lama, denda))
126 |
127 |     def test_diamond_mro(self):
128 |         self.assertEqual(AsistenDosen.__mro__,
129 |                          (AsistenDosen, Mahasiswa, Dosen, Anggota, Anggota.__mro__[1], object))
130 |
131 |     def test_asisten_dosen(self):
132 |         a = AsistenDosen("asd1", "Rizky", "TI", "PBO", email="r@kampus.ac.id")
133 |         self.assertEqual((a.MAKS_PINJAM, a.LAMA_PINJAM, a.DENDA_PER_HARI), (3, 14, 1000))
134 |         self.assertEqual((a.prodi, a.bidang, a.id), ("TI", "PBO", "ASD1"))
135 |         teks = a.ringkasan()
136 |         self.assertTrue(teks.index("Prodi") < teks.index("Bidang") < teks.index("Email"))
137 |
138 |
```

- **Baris 116** — Komentar penanda: mulai Bagian 4, menguji `anggota_turunan.py`.
- **Baris 117** — Class test `TestAnggotaTurunan`.
- **Baris 118** — Test 1: aturan pinjam (class attribute) tiap jenis anggota, contoh *hierarchical inheritance* (satu induk, banyak anak).
- **Baris 119** — List `data` berisi tuple `(objek, maks_pinjam, lama_pinjam, denda_per_hari)` yang diharapkan. Mahasiswa: 3 buku, 7 hari, Rp1.000/hari.
- **Baris 120** — Dosen: 5 buku, 14 hari, Rp500/hari.
- **Baris 121** — Umum: 2 buku, 7 hari, Rp2.000/hari.
- **Baris 122** — *Unpacking* tiap tuple ke variabel `a, maks, lama, denda`.
- **Baris 123** — `subTest(jenis=a.jenis())`: bila gagal, laporan menyebut jenis anggota yang bermasalah.
- **Baris 124** — Membandingkan tuple class attribute milik objek (`MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI`) ...
- **Baris 125** — ... dengan tuple nilai yang diharapkan. Membuktikan setiap subclass meng-*override* class attribute induknya.
- **Baris 127** — Test 2: *diamond inheritance* dan MRO `AsistenDosen`.
- **Baris 128** — Membandingkan seluruh `AsistenDosen.__mro__` ...
- **Baris 129** — ... dengan urutan `AsistenDosen → Mahasiswa → Dosen → Anggota → ABC → object`. `Anggota.__mro__` = `(Anggota, ABC, object)`, jadi `Anggota.__mro__[1]` adalah class `ABC`; cara ini dipakai agar tidak perlu `from abc import ABC` di file test. `Anggota` hanya muncul **sekali** di MRO walaupun diwarisi lewat dua jalur.
- **Baris 131** — Test 3: perilaku objek `AsistenDosen`.
- **Baris 132** — Membuat asisten dosen: id `"asd1"`, nama, prodi `"TI"`, bidang `"PBO"`, dan email.
- **Baris 133** — `MAKS_PINJAM` 3 dan `DENDA_PER_HARI` 1000 diambil dari `Mahasiswa` (lebih dulu di MRO), `LAMA_PINJAM` 14 karena di-override di `AsistenDosen`.
- **Baris 134** — `prodi` diisi oleh `Mahasiswa.__init__`, `bidang` oleh `Dosen.__init__` (berkat `super()` + `**kwargs` yang kooperatif), dan id diubah menjadi huruf besar `"ASD1"` oleh `Anggota.__init__`.
- **Baris 135** — Menyimpan teks ringkasan ke variabel `teks`.
- **Baris 136** — `teks.index(x)` memberi posisi teks `x`. Perbandingan berantai `a < b < c` memastikan urutan **Prodi → Bidang → Email**, sesuai urutan MRO: `info_tambahan()` Mahasiswa menambah Prodi lalu memanggil `super()` (Dosen) yang menambah Bidang, lalu `super()` (Anggota) yang menambah Email.
- **Baris 126, 130, 137–138** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 139–164: Bagian 5 — TestPeminjaman (Orang 5)

Menguji `peminjaman.py`: hierarki exception kustom, jatuh tempo, denda, dan polymorphism `kena_denda()`. Berisi 4 test.

```python
139 | # ---------------- Bagian 5: peminjaman.py ----------------
140 | class TestPeminjaman(unittest.TestCase):
141 |     def test_hirarki_exception(self):
142 |         for kelas in (DataTidakDitemukan, DataDuplikat, PeminjamanDitolak):
143 |             self.assertTrue(issubclass(kelas, PerpustakaanError))
144 |
145 |     def test_jatuh_tempo_dan_denda(self):
146 |         p = Peminjaman("P0001", Mahasiswa("M1", "A", "TI"), buku(), HARI_INI)
147 |         self.assertEqual(p.jatuh_tempo, HARI_INI + timedelta(days=7))
148 |         self.assertEqual(p.hitung_denda(HARI_INI + timedelta(days=10)), 3000)
149 |         self.assertEqual(p.kembalikan(HARI_INI + timedelta(days=10)), 3000)
150 |         self.assertEqual(p.status, "Dikembalikan")
151 |         with self.assertRaises(ValueError):
152 |             p.kembalikan()
153 |
154 |     def test_ebook_tanpa_denda(self):
155 |         e = EBook("E1", "X", 2023, "Tim", "Digital")
156 |         p = Peminjaman("P0001", Umum("U1", "C"), e, HARI_INI)
157 |         self.assertEqual(p.hitung_denda(HARI_INI + timedelta(days=30)), 0)
158 |
159 |     def test_tanggal_kembali_tidak_valid(self):
160 |         p = Peminjaman("P0001", Umum("U1", "C"), buku(), HARI_INI)
161 |         with self.assertRaises(ValueError):
162 |             p.kembalikan(HARI_INI - timedelta(days=1))
163 |
164 |
```

- **Baris 139** — Komentar penanda: mulai Bagian 5, menguji `peminjaman.py`.
- **Baris 140** — Class test `TestPeminjaman`.
- **Baris 141** — Test 1: hierarki exception kustom.
- **Baris 142** — Perulangan atas tiga exception kustom.
- **Baris 143** — `issubclass(kelas, PerpustakaanError)` harus `True`; artinya cukup `except PerpustakaanError` untuk menangkap ketiganya (inheritance pada exception).
- **Baris 145** — Test 2: perhitungan jatuh tempo dan denda.
- **Baris 146** — Membuat transaksi `P0001`: Mahasiswa meminjam buku pada `HARI_INI` (1 Jan 2024). `Peminjaman` *memiliki* (has-a) anggota dan koleksi.
- **Baris 147** — Jatuh tempo = tanggal pinjam + `LAMA_PINJAM` Mahasiswa (7 hari) = 8 Januari 2024.
- **Baris 148** — Dicek pada hari ke-10 (11 Jan): terlambat 11 − 8 = 3 hari × `DENDA_PER_HARI` Mahasiswa Rp1.000 = `3000`.
- **Baris 149** — `kembalikan()` pada tanggal yang sama menutup transaksi dan mengembalikan denda yang sama, `3000`.
- **Baris 150** — Setelah dikembalikan, property `status` bernilai `"Dikembalikan"` (sebelumnya `"Dipinjam"`).
- **Baris 151** — Mengharapkan `ValueError`.
- **Baris 152** — Transaksi yang sudah tidak aktif tidak boleh dikembalikan dua kali → `ValueError("Peminjaman P0001 sudah dikembalikan")`.
- **Baris 154** — Test 3: e-book tidak dikenai denda (*polymorphism*).
- **Baris 155** — Membuat `EBook` dengan format default PDF dan ukuran default 1.0 MB.
- **Baris 156** — Anggota `Umum` meminjam e-book pada `HARI_INI`.
- **Baris 157** — Pada hari ke-30 sebenarnya terlambat 23 hari, tetapi `hitung_denda()` memanggil `koleksi.kena_denda()` yang untuk e-book bernilai `False`, sehingga denda `0`. Tidak ada `if` pengecekan tipe, cukup method yang di-override.
- **Baris 159** — Test 4: tanggal kembali tidak valid.
- **Baris 160** — Membuat transaksi pinjam pada `HARI_INI`.
- **Baris 161** — Mengharapkan `ValueError`.
- **Baris 162** — Tanggal kembali satu hari **sebelum** tanggal pinjam (31 Des 2023) ditolak.
- **Baris 144, 153, 158, 163–164** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 165–228: Bagian 6 — TestPerpustakaan (Orang 6)

Menguji `perpustakaan.py`: menambah/mencari/menghapus data dan aturan bisnis peminjaman. Memakai `setUp()`. Berisi 6 test.

```python
165 | # ---------------- Bagian 6: perpustakaan.py ----------------
166 | class TestPerpustakaan(unittest.TestCase):
167 |     def setUp(self):
168 |         self.p = Perpustakaan()
169 |         self.p.tambah_koleksi(buku(stok=5))
170 |         self.p.tambah_koleksi(Referensi("R001", "KBBI", 2016, "Badan", "Balai"))
171 |         self.p.tambah_anggota(Umum("U1", "Budi"))
172 |
173 |     def test_tambah_cari_duplikat(self):
174 |         self.assertEqual(self.p.cari_koleksi("b001").kode, "B001")
175 |         with self.assertRaises(DataDuplikat):
176 |             self.p.tambah_koleksi(buku())
177 |         with self.assertRaises(DataTidakDitemukan):
178 |             self.p.cari_anggota("X")
179 |         with self.assertRaises(TypeError):
180 |             self.p.tambah_anggota("bukan anggota")
181 |         self.assertEqual(len(self.p.cari_koleksi_kata("andrea")), 1)
182 |
183 |     def test_pinjam_dan_kembali(self):
184 |         t = self.p.pinjam("U1", "B001", HARI_INI)
185 |         self.assertEqual((t.id, self.p.cari_koleksi("B001").stok), ("P0001", 4))
186 |         self.p.kembalikan("P0001", HARI_INI + timedelta(days=9))
187 |         self.assertEqual(self.p.cari_anggota("U1").total_denda, 4000)
188 |         self.assertEqual(self.p.cari_koleksi("B001").stok, 5)
189 |         with self.assertRaises(PeminjamanDitolak):
190 |             self.p.kembalikan("P0001")
191 |
192 |     def test_aturan_pinjam(self):
193 |         with self.assertRaises(PeminjamanDitolak):
194 |             self.p.pinjam("U1", "R001")  # referensi
195 |         self.p.pinjam("U1", "B001", HARI_INI)
196 |         with self.assertRaises(PeminjamanDitolak):
197 |             self.p.pinjam("U1", "B001", HARI_INI)  # judul sama
198 |         self.p.tambah_koleksi(buku("B002"))
199 |         self.p.tambah_koleksi(buku("B003"))
200 |         self.p.pinjam("U1", "B002", HARI_INI)
201 |         with self.assertRaises(PeminjamanDitolak):
202 |             self.p.pinjam("U1", "B003", HARI_INI)  # batas Umum = 2
203 |
204 |     def test_tolak_jika_berdenda_atau_terlambat(self):
205 |         self.p.pinjam("U1", "B001", HARI_INI)
206 |         with self.assertRaises(PeminjamanDitolak):
207 |             self.p.tambah_koleksi(buku("B002"))
208 |             self.p.pinjam("U1", "B002", HARI_INI + timedelta(days=30))
209 |         self.p.kembalikan("P0001", HARI_INI + timedelta(days=8))
210 |         with self.assertRaises(PeminjamanDitolak):
211 |             self.p.pinjam("U1", "B002")
212 |         self.p.bayar_denda("U1", 2000)
213 |         self.assertEqual(self.p.pinjam("U1", "B002").id, "P0002")
214 |
215 |     def test_hapus_ditolak_saat_dipinjam(self):
216 |         self.p.pinjam("U1", "B001", HARI_INI)
217 |         with self.assertRaises(PeminjamanDitolak):
218 |             self.p.hapus_koleksi("B001")
219 |         with self.assertRaises(PeminjamanDitolak):
220 |             self.p.hapus_anggota("U1")
221 |
222 |     def test_data_contoh_dan_laporan(self):
223 |         perpus = buat_data_contoh()
224 |         self.assertGreaterEqual(len(perpus.daftar_koleksi()), 5)
225 |         self.assertGreaterEqual(len(perpus.daftar_anggota()), 5)
226 |         self.assertIn("LAPORAN", perpus.laporan())
227 |
228 |
```

- **Baris 165** — Komentar penanda: mulai Bagian 6, menguji `perpustakaan.py`.
- **Baris 166** — Class test `TestPerpustakaan`.
- **Baris 167** — `setUp()` adalah method khusus `unittest` yang otomatis dijalankan **sebelum setiap** method test. Jadi setiap test mendapat perpustakaan baru yang bersih (tidak saling memengaruhi).
- **Baris 168** — Membuat objek `Perpustakaan` dan menyimpannya di `self.p` agar bisa dipakai di method test.
- **Baris 169** — Menambah buku B001 dengan stok 5.
- **Baris 170** — Menambah buku referensi R001 (stok default 1).
- **Baris 171** — Menambah anggota `Umum` U1 "Budi" (maks 2 pinjaman, 7 hari, denda Rp2.000/hari).
- **Baris 173** — Test 1: tambah, cari, dan cek duplikat.
- **Baris 174** — Pencarian tidak peka huruf besar/kecil: `cari_koleksi()` mengubah `"b001"` menjadi `"B001"` sebelum mencari.
- **Baris 175** — Mengharapkan exception kustom `DataDuplikat`.
- **Baris 176** — `buku()` default berkode B001 yang sudah terdaftar di `setUp` → ditolak.
- **Baris 177** — Mengharapkan `DataTidakDitemukan`.
- **Baris 178** — Anggota dengan ID `"X"` tidak ada.
- **Baris 179** — Mengharapkan `TypeError`.
- **Baris 180** — Yang ditambahkan berupa string, bukan objek turunan `Anggota` → `isinstance` gagal → `TypeError`.
- **Baris 181** — Pencarian kata `"andrea"` di kode/judul/penulis hanya cocok dengan B001 (penulis Andrea Hirata), R001 tidak cocok → panjang list `1`.
- **Baris 183** — Test 2: alur pinjam lalu kembali.
- **Baris 184** — U1 meminjam B001 pada `HARI_INI`; hasilnya objek transaksi `t`.
- **Baris 185** — ID transaksi pertama `"P0001"` (format `P{nomor:04d}`), dan stok B001 berkurang dari 5 menjadi 4.
- **Baris 186** — Dikembalikan pada hari ke-9 (10 Jan). Jatuh tempo Umum = 1 Jan + 7 = 8 Jan, terlambat 2 hari.
- **Baris 187** — Denda = 2 hari × Rp2.000 = `4000`, otomatis ditambahkan ke `total_denda` anggota.
- **Baris 188** — Stok kembali menjadi 5.
- **Baris 189** — Mengharapkan `PeminjamanDitolak`.
- **Baris 190** — Mengembalikan transaksi yang sudah selesai ditolak oleh `Perpustakaan` dengan exception kustom (bukan `ValueError` milik `Peminjaman`).
- **Baris 192** — Test 3: aturan bisnis peminjaman.
- **Baris 193** — Mengharapkan `PeminjamanDitolak`.
- **Baris 194** — Buku referensi tidak bisa dipinjam (`bisa_dipinjam()` = `False` padahal stok ada) → ditolak "hanya baca di tempat". Komentar `# referensi` menjelaskan alasannya.
- **Baris 195** — U1 meminjam B001 (berhasil, pinjaman aktif = 1).
- **Baris 196** — Mengharapkan `PeminjamanDitolak`.
- **Baris 197** — Meminjam judul yang sama dua kali ditolak (`# judul sama`).
- **Baris 198** — Menambah buku B002 (stok 2).
- **Baris 199** — Menambah buku B003 (stok 2).
- **Baris 200** — U1 meminjam B002 → pinjaman aktif = 2.
- **Baris 201** — Mengharapkan `PeminjamanDitolak`.
- **Baris 202** — Pinjaman aktif sudah 2 = `MAKS_PINJAM` anggota Umum, jadi pinjaman ketiga ditolak (`# batas Umum = 2`).
- **Baris 204** — Test 4: ditolak jika punya pinjaman terlambat atau denda belum lunas.
- **Baris 205** — U1 meminjam B001 pada 1 Jan (jatuh tempo 8 Jan).
- **Baris 206** — Mengharapkan `PeminjamanDitolak` dari salah satu baris di dalam blok.
- **Baris 207** — Menambah B002 (baris ini sendiri berhasil, tidak melempar error).
- **Baris 208** — Mencoba meminjam B002 pada hari ke-30 (31 Jan): B001 masih aktif dan sudah lewat jatuh tempo → ditolak "memiliki pinjaman yang terlambat".
- **Baris 209** — B001 dikembalikan pada hari ke-8 (9 Jan): terlambat 1 hari × Rp2.000 = denda Rp2.000.
- **Baris 210** — Mengharapkan `PeminjamanDitolak`.
- **Baris 211** — Masih ada denda Rp2.000 yang belum dibayar → pinjaman ditolak.
- **Baris 212** — Membayar denda Rp2.000 lewat `Perpustakaan.bayar_denda()` → denda menjadi 0.
- **Baris 213** — Sekarang pinjaman berhasil; ID-nya `"P0002"` karena pinjaman yang ditolak tidak pernah dicatat (hanya P0001 yang tercatat sebelumnya).
- **Baris 215** — Test 5: data tidak boleh dihapus saat masih dipakai transaksi aktif.
- **Baris 216** — U1 meminjam B001.
- **Baris 217** — Mengharapkan `PeminjamanDitolak`.
- **Baris 218** — B001 masih dipinjam → tidak boleh dihapus.
- **Baris 219** — Mengharapkan `PeminjamanDitolak`.
- **Baris 220** — U1 masih punya pinjaman aktif → tidak boleh dihapus.
- **Baris 222** — Test 6: data contoh dan laporan.
- **Baris 223** — Membuat perpustakaan berisi data contoh (6 koleksi, 5 anggota).
- **Baris 224** — `assertGreaterEqual(a, b)` lulus jika `a >= b`; jumlah koleksi minimal 5.
- **Baris 225** — Jumlah anggota minimal 5.
- **Baris 226** — Teks laporan harus memuat kata `"LAPORAN"` (judul `=== LAPORAN PERPUSTAKAAN KAMPUS ===`).
- **Baris 172, 182, 191, 203, 214, 221, 227–228** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 229–241: Bagian 7 — TestMain (Orang 7)

Menguji `main.py`: fungsi `teks_mro()` dan pembuatan objek menu. Berisi 2 test.

```python
229 | # ---------------- Bagian 7: main.py ----------------
230 | class TestMain(unittest.TestCase):
231 |     def test_teks_mro(self):
232 |         from main import teks_mro
233 |         self.assertEqual(teks_mro(EBook),
234 |                          "EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object")
235 |
236 |     def test_menu_bisa_dibuat(self):
237 |         from main import MenuPerpustakaan
238 |         menu = MenuPerpustakaan(buat_data_contoh())
239 |         self.assertEqual(menu.perpus.nama, "Perpustakaan Kampus")
240 |
241 |
```

- **Baris 229** — Komentar penanda: mulai Bagian 7, menguji `main.py`.
- **Baris 230** — Class test `TestMain`.
- **Baris 231** — Test 1: fungsi `teks_mro()`.
- **Baris 232** — Import **di dalam method**: `main.py` baru dimuat saat test ini berjalan. Jika `main.py` bermasalah, hanya test Bagian 7 yang gagal, test bagian lain tetap jalan. Import aman karena menu interaktif di `main.py` hanya berjalan di dalam `if __name__ == "__main__":`.
- **Baris 233** — Memanggil `teks_mro(EBook)` dan membandingkan hasilnya ...
- **Baris 234** — ... dengan string MRO EBook yang digabung `" -> "`: `EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object`.
- **Baris 236** — Test 2: objek menu bisa dibuat tanpa error.
- **Baris 237** — Import class `MenuPerpustakaan` di dalam method (alasan sama seperti baris 232).
- **Baris 238** — Membuat menu yang *memiliki* (has-a) objek perpustakaan berisi data contoh. Menu tidak dijalankan (tidak memanggil `input()`), jadi test tidak menunggu ketikan pengguna.
- **Baris 239** — Atribut `menu.perpus` adalah perpustakaan yang diberikan; namanya `"Perpustakaan Kampus"`.
- **Baris 235, 240–241** — Baris kosong, hanya pemisah agar kode mudah dibaca (PEP 8: dua baris kosong sebelum class/fungsi tingkat atas, satu baris kosong antar method).

## Baris 242–243: Menjalankan File Secara Langsung

Dua baris penutup file.

```python
242 | if __name__ == "__main__":
243 |     unittest.main()
```

- **Baris 242** — Blok ini hanya berjalan jika file dijalankan langsung (`python test_perpustakaan.py`), bukan saat diimpor atau dijalankan lewat `python -m unittest`.
- **Baris 243** — `unittest.main()` mencari semua class turunan `TestCase` di file ini, menjalankan semua method `test...`, lalu menampilkan hasilnya.

## Contoh Output

Hasil nyata menjalankan `python -m unittest -v` di folder repo. Urutan class mengikuti abjad nama class (bukan urutan di file), dan method juga diurutkan menurut abjad.

```text
test_abstract (test_perpustakaan.TestAnggota.test_abstract) ... ok
test_denda_private (test_perpustakaan.TestAnggota.test_denda_private) ... ok
test_email (test_perpustakaan.TestAnggota.test_email) ... ok
test_rupiah (test_perpustakaan.TestAnggota.test_rupiah) ... ok
test_asisten_dosen (test_perpustakaan.TestAnggotaTurunan.test_asisten_dosen) ... ok
test_aturan_tiap_jenis (test_perpustakaan.TestAnggotaTurunan.test_aturan_tiap_jenis) ... ok
test_diamond_mro (test_perpustakaan.TestAnggotaTurunan.test_diamond_mro) ... ok
test_abstract_tidak_bisa_dibuat (test_perpustakaan.TestKoleksi.test_abstract_tidak_bisa_dibuat) ... ok
test_buku_valid (test_perpustakaan.TestKoleksi.test_buku_valid) ... ok
test_kode_read_only (test_perpustakaan.TestKoleksi.test_kode_read_only) ... ok
test_setter_mengubah_teks_angka (test_perpustakaan.TestKoleksi.test_setter_mengubah_teks_angka) ... ok
test_stok (test_perpustakaan.TestKoleksi.test_stok) ... ok
test_validasi_setter (test_perpustakaan.TestKoleksi.test_validasi_setter) ... ok
test_ebook_multiple_inheritance (test_perpustakaan.TestKoleksiTurunan.test_ebook_multiple_inheritance) ... ok
test_ebook_validasi (test_perpustakaan.TestKoleksiTurunan.test_ebook_validasi) ... ok
test_majalah_single_inheritance (test_perpustakaan.TestKoleksiTurunan.test_majalah_single_inheritance) ... ok
test_referensi_multilevel (test_perpustakaan.TestKoleksiTurunan.test_referensi_multilevel) ... ok
test_menu_bisa_dibuat (test_perpustakaan.TestMain.test_menu_bisa_dibuat) ... ok
test_teks_mro (test_perpustakaan.TestMain.test_teks_mro) ... ok
test_ebook_tanpa_denda (test_perpustakaan.TestPeminjaman.test_ebook_tanpa_denda) ... ok
test_hirarki_exception (test_perpustakaan.TestPeminjaman.test_hirarki_exception) ... ok
test_jatuh_tempo_dan_denda (test_perpustakaan.TestPeminjaman.test_jatuh_tempo_dan_denda) ... ok
test_tanggal_kembali_tidak_valid (test_perpustakaan.TestPeminjaman.test_tanggal_kembali_tidak_valid) ... ok
test_aturan_pinjam (test_perpustakaan.TestPerpustakaan.test_aturan_pinjam) ... ok
test_data_contoh_dan_laporan (test_perpustakaan.TestPerpustakaan.test_data_contoh_dan_laporan) ... ok
test_hapus_ditolak_saat_dipinjam (test_perpustakaan.TestPerpustakaan.test_hapus_ditolak_saat_dipinjam) ... ok
test_pinjam_dan_kembali (test_perpustakaan.TestPerpustakaan.test_pinjam_dan_kembali) ... ok
test_tambah_cari_duplikat (test_perpustakaan.TestPerpustakaan.test_tambah_cari_duplikat) ... ok
test_tolak_jika_berdenda_atau_terlambat (test_perpustakaan.TestPerpustakaan.test_tolak_jika_berdenda_atau_terlambat) ... ok

----------------------------------------------------------------------
Ran 29 tests in 0.007s

OK
```

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Mengapa class test harus mewarisi `unittest.TestCase`?**
   Agar mendapat method `assertEqual`, `assertRaises`, `subTest`, `setUp`, dll., dan agar `unittest` mengenali class itu sebagai kumpulan test. Ini contoh penerapan inheritance.
2. **Apa bedanya `setUp()` dengan membuat objek di luar class?**
   `setUp()` dipanggil ulang sebelum **setiap** test, jadi setiap test di `TestPerpustakaan` mendapat perpustakaan baru yang bersih. Jika objek dibuat sekali di luar, perubahan stok/denda di satu test akan memengaruhi test lain.
3. **Bagaimana test membuktikan atribut `__total_denda` benar-benar private?**
   `hasattr(a, "__total_denda")` bernilai `False` karena name mangling mengubah namanya menjadi `_Anggota__total_denda`, dan `a.total_denda = 100` menghasilkan `AttributeError` karena property tidak punya setter.
4. **Mengapa memakai `HARI_INI = date(2024, 1, 1)`, bukan `date.today()`?**
   Agar hasil hitungan tetap. Contoh: Mahasiswa pinjam 1 Jan, jatuh tempo 8 Jan, dikembalikan 11 Jan → 3 hari × Rp1.000 = Rp3.000, kapan pun test dijalankan.
5. **Apa gunanya `subTest`?**
   Dalam perulangan, jika satu nilai gagal, nilai lain tetap diuji dan laporan menyebut nilai mana yang gagal (mis. `atribut='tahun', nilai=1000`).
6. **Mengapa `from main import ...` ditulis di dalam method?**
   Supaya `main.py` hanya dimuat oleh test Bagian 7. Jika `main.py` error, test bagian 1–6 tetap berjalan. Import tidak menjalankan menu karena menu dilindungi `if __name__ == "__main__":`.

## Ringkasan

- File berisi **29 test** dalam **7 class** (`TestKoleksi` … `TestMain`), satu class per file program sehingga setiap presenter (Orang 1–7) punya bagian test sendiri.
- Semua class test mewarisi `unittest.TestCase`; method berawalan `test` dijalankan otomatis.
- Yang diuji: abstract class tidak bisa dibuat (`TypeError`), validasi setter (`ValueError`), atribut read-only/private (`AttributeError`, name mangling), single/multilevel/multiple/diamond inheritance dan MRO, polymorphism (`kena_denda`, `ringkasan`), exception kustom, serta aturan bisnis perpustakaan.
- Alat `unittest` yang dipakai: `assertEqual`, `assertTrue/False`, `assertIn`, `assertIsInstance`, `assertGreaterEqual`, `assertRaises` (context manager), `subTest`, dan `setUp`.
- Tanggal tetap `HARI_INI` membuat perhitungan denda dapat diprediksi: Mahasiswa terlambat 3 hari = Rp3.000; Umum terlambat 2 hari = Rp4.000; Umum terlambat 1 hari = Rp2.000; e-book = Rp0.
- Hasil `python -m unittest -v`: `Ran 29 tests ... OK` → semua test lulus.
