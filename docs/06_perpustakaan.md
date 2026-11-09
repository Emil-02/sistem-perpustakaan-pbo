# Penjelasan Baris per Baris: perpustakaan.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 6 |
| File | `perpustakaan.py` |
| Jumlah baris | 183 baris |
| Konsep PBO yang dibahas | Composition (has-a) vs inheritance (is-a), dictionary/list sebagai penyimpanan objek, `isinstance` terhadap abstract class, raise exception kustom, list comprehension & generator expression, `getattr` dengan default, `is` vs `==`, `any()`, f-string `:04d`, polymorphism di `laporan()`, urutan validasi (aturan bisnis) di `pinjam()` |

## Gambaran Umum

`perpustakaan.py` adalah "otak" sistem. File ini berisi class `Perpustakaan` yang **memiliki** (has-a / composition) tiga kumpulan data: koleksi (dari `koleksi.py` dan `koleksi_turunan.py`), anggota (dari `anggota.py` dan `anggota_turunan.py`), dan transaksi peminjaman (dari `peminjaman.py`). `Perpustakaan` **tidak** mewarisi class mana pun; ia hanya menyimpan objek-objek itu di dalam dictionary/list lalu mengatur aturan bisnisnya: menambah, mencari, menghapus, meminjam, mengembalikan, membayar denda, dan membuat laporan. Di bagian bawah ada fungsi `buat_data_contoh()` yang mengisi perpustakaan dengan 6 koleksi dan 5 anggota. Fungsi inilah yang diimpor oleh `main.py` (`from perpustakaan import buat_data_contoh`) sehingga menu console langsung punya data; `test_perpustakaan.py` juga menguji class ini. Jadi file ini adalah penghubung antara semua model (file 1–5) dan antarmuka pengguna (file 7).


## Baris 1–5: Docstring Modul

Docstring modul menjelaskan isi file. Python menyimpannya di `perpustakaan.__doc__`, sehingga bisa dibaca dengan `help(perpustakaan)`.

```python
  1 | """BAGIAN 6 - Class Perpustakaan (composition / has-a) + aturan bisnis + data contoh.
  2 |
  3 | Perpustakaan MEMILIKI koleksi, anggota, dan peminjaman, tetapi BUKAN turunannya.
  4 | """
  5 |
```

- **Baris 1** — Pembuka docstring modul (tanda `"""`). Kalimatnya menyebut tiga isi file: class `Perpustakaan`, aturan bisnis, dan data contoh. Kata kunci **composition / has-a** langsung disebut karena itulah konsep utama yang dipresentasikan Orang 6.
- **Baris 2** — Baris kosong **di dalam** docstring, hanya untuk merapikan paragraf (bukan pemisah kode).
- **Baris 3** — Menegaskan perbedaan relasi: Perpustakaan **MEMILIKI** koleksi, anggota, dan peminjaman (has-a), tetapi **BUKAN turunannya** (bukan is-a). Contoh: "Perpustakaan *punya* Buku" benar, "Perpustakaan *adalah* Buku" salah — jadi yang tepat composition, bukan inheritance.
- **Baris 4** — Penutup docstring.
- **Baris 5** — Baris kosong pemisah docstring dan blok import.

## Baris 6–14: Import

File ini mengimpor **semua** model dari file 1–5. Ini wajar karena `Perpustakaan` adalah pengelola seluruh objek.

```python
  6 | from datetime import date
  7 |
  8 | from anggota import Anggota, rupiah
  9 | from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
 10 | from koleksi import Buku, Koleksi
 11 | from koleksi_turunan import EBook, Majalah, Referensi
 12 | from peminjaman import DataDuplikat, DataTidakDitemukan, Peminjaman, PeminjamanDitolak
 13 |
 14 |
```

- **Baris 6** — Mengimpor class `date` dari modul bawaan `datetime`. Dipakai di `pinjam()` untuk tanggal default (`date.today()`), misalnya `date(2026, 11, 9)`.
- **Baris 7** — Baris kosong: memisahkan import pustaka bawaan Python dengan import file buatan sendiri (gaya PEP 8).
- **Baris 8** — Dari `anggota.py` (file 3): `Anggota` (abstract class, dipakai untuk `isinstance` di `tambah_anggota`) dan fungsi `rupiah()` untuk format uang, contoh `rupiah(3000)` → `'Rp3.000'`.
- **Baris 9** — Dari `anggota_turunan.py` (file 4): empat subclass anggota. Di file ini hanya dipakai untuk membuat objek di `buat_data_contoh()`.
- **Baris 10** — Dari `koleksi.py` (file 1): `Buku` (untuk data contoh) dan `Koleksi` (abstract class, untuk validasi `isinstance` di `tambah_koleksi`).
- **Baris 11** — Dari `koleksi_turunan.py` (file 2): `EBook`, `Majalah`, `Referensi`, dipakai di data contoh.
- **Baris 12** — Dari `peminjaman.py` (file 5): tiga **exception kustom** (`DataDuplikat`, `DataTidakDitemukan`, `PeminjamanDitolak`) yang akan di-`raise`, dan class `Peminjaman` untuk membuat objek transaksi.
- **Baris 13** — Baris kosong.
- **Baris 14** — Baris kosong kedua — PEP 8 menganjurkan **dua** baris kosong sebelum definisi class/fungsi tingkat atas.

## Baris 15–22: Class dan Constructor

Di sinilah composition terlihat: atribut objek `Perpustakaan` berisi objek-objek class lain.

```python
 15 | class Perpustakaan:
 16 |     def __init__(self, nama="Perpustakaan Kampus"):
 17 |         self.nama = nama
 18 |         # Dibuat di __init__ (bukan class attribute) agar tiap objek punya data sendiri
 19 |         self._koleksi = {}  # kode -> Koleksi
 20 |         self._anggota = {}  # id -> Anggota
 21 |         self._peminjaman = []  # list Peminjaman
 22 |
```

- **Baris 15** — Mendefinisikan class `Perpustakaan`. Perhatikan tidak ada tanda kurung berisi induk, artinya **tidak ada inheritance** (secara implisit hanya turunan `object`). Hubungannya dengan class lain murni has-a.
- **Baris 16** — Constructor `__init__`, dipanggil otomatis saat `Perpustakaan(...)` dibuat. Parameter `nama` punya nilai default `"Perpustakaan Kampus"`, jadi `Perpustakaan()` tanpa argumen tetap valid.
- **Baris 17** — Menyimpan nama ke atribut publik `self.nama`. Contoh: `Perpustakaan("Perpus FT").nama` → `'Perpus FT'`. Dipakai di judul laporan.
- **Baris 18** — Komentar penting: tiga wadah data **dibuat di dalam `__init__`**, bukan sebagai class attribute. Kalau ditulis sebagai class attribute (`_koleksi = {}` di bawah `class`), semua objek Perpustakaan akan **berbagi dictionary yang sama** (karena dict itu mutable), sehingga data perpus A ikut muncul di perpus B.
- **Baris 19** — `self._koleksi` adalah **dictionary** dengan kunci kode koleksi dan nilai objek koleksi, contoh `{"B001": <Buku Laskar Pelangi>, "M001": <Majalah Tempo>}`. Dict dipilih karena pencarian berdasarkan kode cepat (`O(1)`) dan kunci otomatis unik. Awalan `_` = **protected**: sebaiknya diakses lewat method, bukan langsung dari luar.
- **Baris 20** — `self._anggota` juga dictionary: kunci ID anggota, nilai objek anggota, contoh `{"MHS001": <Mahasiswa Nadia>}`.
- **Baris 21** — `self._peminjaman` berupa **list**, karena transaksi disimpan berurutan sebagai riwayat dan tidak pernah dihapus. Urutan ini juga dipakai untuk membuat ID transaksi (`P0001`, `P0002`, ...).
- **Baris 22** — Baris kosong pemisah antar-method.

## Baris 23–30: KOLEKSI — `tambah_koleksi()`

```python
 23 |     # ===================== KOLEKSI =====================
 24 |     def tambah_koleksi(self, koleksi):
 25 |         if not isinstance(koleksi, Koleksi):
 26 |             raise TypeError("Objek harus turunan Koleksi")
 27 |         if koleksi.kode in self._koleksi:
 28 |             raise DataDuplikat(f"Kode koleksi {koleksi.kode} sudah terdaftar")
 29 |         self._koleksi[koleksi.kode] = koleksi
 30 |
```

- **Baris 23** — Komentar penanda bagian: method-method untuk mengelola koleksi.
- **Baris 24** — Method untuk menambahkan satu objek koleksi ke perpustakaan, contoh `perpus.tambah_koleksi(Buku("B004", ...))`.
- **Baris 25** — Validasi tipe dengan `isinstance(koleksi, Koleksi)`. Karena `Koleksi` adalah **abstract class** induk semua koleksi, pengecekan ini menerima `Buku`, `Majalah`, `Referensi`, maupun `EBook` sekaligus (isinstance ikut memeriksa turunan). Yang ditolak misalnya string `"B004"` atau objek `Mahasiswa`.
- **Baris 26** — Jika bukan koleksi, lempar `TypeError` (exception bawaan Python yang memang untuk tipe data salah).
- **Baris 27** — Cek duplikasi: operator `in` pada dictionary memeriksa **kunci**. Jika `"B001"` sudah ada, koleksi baru dengan kode sama ditolak.
- **Baris 28** — Melempar exception kustom `DataDuplikat`, contoh pesan: `Kode koleksi B001 sudah terdaftar`. Pakai exception kustom agar `main.py` bisa menangkap semua error perpustakaan dengan satu induk (`PerpustakaanError`).
- **Baris 29** — Jika lolos semua validasi, objek disimpan ke dictionary dengan kunci kodenya: `self._koleksi["B004"] = koleksi`. Inilah momen composition: objek koleksi kini "dimiliki" perpustakaan.
- **Baris 30** — Baris kosong.

## Baris 31–36: `cari_koleksi()`

```python
 31 |     def cari_koleksi(self, kode):
 32 |         kode = str(kode).strip().upper()
 33 |         if kode not in self._koleksi:
 34 |             raise DataTidakDitemukan(f"Koleksi dengan kode {kode} tidak ditemukan")
 35 |         return self._koleksi[kode]
 36 |
```

- **Baris 31** — Mencari satu koleksi berdasarkan kode persis.
- **Baris 32** — Menormalkan input: `str()` agar aman bila yang dikirim bukan string, `strip()` membuang spasi, `upper()` menyamakan huruf. Contoh `" b001 "` → `"B001"`. Ini cocok karena di `Koleksi.__init__` kode juga disimpan dalam huruf besar.
- **Baris 33** — Jika kode tidak ada sebagai kunci dictionary...
- **Baris 34** — ...lempar `DataTidakDitemukan`, contoh: `Koleksi dengan kode X999 tidak ditemukan`. Lebih jelas daripada membiarkan Python melempar `KeyError`.
- **Baris 35** — Mengembalikan objek koleksinya, contoh `perpus.cari_koleksi("b001").judul` → `'Laskar Pelangi'`. Method ini dipakai ulang oleh `hapus_koleksi()` dan `pinjam()` (prinsip *don't repeat yourself*).
- **Baris 36** — Baris kosong.

## Baris 37–42: `cari_koleksi_kata()`

```python
 37 |     def cari_koleksi_kata(self, kata):
 38 |         """Cari berdasarkan kode, judul, atau penulis (tidak peka huruf besar/kecil)."""
 39 |         kata = kata.strip().lower()
 40 |         return [k for k in self._koleksi.values()
 41 |                 if kata in f"{k.kode} {k.judul} {getattr(k, 'penulis', '')}".lower()]
 42 |
```

- **Baris 37** — Pencarian bebas berdasarkan kata kunci (bisa banyak hasil), berbeda dengan `cari_koleksi()` yang harus persis satu kode.
- **Baris 38** — Docstring: pencarian mencakup kode, judul, atau penulis dan **tidak peka huruf besar/kecil** (case-insensitive).
- **Baris 39** — Kata kunci dirapikan dan dikecilkan, contoh `" PYTHON "` → `"python"`.
- **Baris 40** — Awal **list comprehension**: mengambil setiap objek `k` dari `self._koleksi.values()` (nilai dictionary = objek koleksi)...
- **Baris 41** — ...dan hanya memasukkan yang cocok. Untuk tiap koleksi dibuat satu teks gabungan, misal `"B003 Pemrograman Python untuk Pemula Budi Raharjo"`, lalu dikecilkan dan dicek apakah `kata` ada di dalamnya. `getattr(k, 'penulis', '')` dipakai karena **tidak semua koleksi punya atribut `penulis`** (Majalah tidak punya); jika atribut tidak ada, hasilnya `''` sehingga tidak terjadi `AttributeError`. Contoh: `cari_koleksi_kata("python")` → `[B003, E001]`.
- **Baris 42** — Baris kosong.

## Baris 43–51: `hapus_koleksi()` dan `daftar_koleksi()`

```python
 43 |     def hapus_koleksi(self, kode):
 44 |         koleksi = self.cari_koleksi(kode)
 45 |         if any(p.aktif and p.koleksi is koleksi for p in self._peminjaman):
 46 |             raise PeminjamanDitolak(f"'{koleksi.judul}' masih dipinjam, tidak dapat dihapus")
 47 |         return self._koleksi.pop(koleksi.kode)
 48 |
 49 |     def daftar_koleksi(self):
 50 |         return list(self._koleksi.values())
 51 |
```

- **Baris 43** — Menghapus koleksi berdasarkan kode.
- **Baris 44** — Memanggil `cari_koleksi()` — otomatis menormalkan kode dan melempar `DataTidakDitemukan` jika tidak ada.
- **Baris 45** — Aturan: koleksi yang **masih dipinjam** tidak boleh dihapus. `any(...)` bernilai `True` jika minimal satu transaksi memenuhi syarat: masih aktif **dan** koleksinya adalah objek yang sama. Dipakai `is` (identitas objek, "objek yang sama di memori"), bukan `==` (kesamaan nilai). `any()` juga berhenti di kecocokan pertama sehingga efisien.
- **Baris 46** — Jika masih dipinjam, lempar `PeminjamanDitolak`, contoh: `'Laskar Pelangi' masih dipinjam, tidak dapat dihapus`.
- **Baris 47** — `dict.pop(kunci)` menghapus entri sekaligus **mengembalikan objek yang dihapus**, sehingga `main.py` bisa menampilkan judulnya ("... berhasil dihapus"). Dipakai `koleksi.kode` (yang sudah huruf besar), bukan input mentah.
- **Baris 48** — Baris kosong.
- **Baris 49** — Method untuk mengambil semua koleksi.
- **Baris 50** — Mengembalikan `list` **baru** berisi objek koleksi. Karena list baru, kode luar yang mengubah list ini (misal `append`) tidak merusak dictionary internal — bentuk sederhana dari **enkapsulasi**.
- **Baris 51** — Baris kosong.

## Baris 52–59: ANGGOTA — `tambah_anggota()`

Pola bagian anggota sama persis dengan bagian koleksi; ini menunjukkan desain yang konsisten.

```python
 52 |     # ===================== ANGGOTA =====================
 53 |     def tambah_anggota(self, anggota):
 54 |         if not isinstance(anggota, Anggota):
 55 |             raise TypeError("Objek harus turunan Anggota")
 56 |         if anggota.id in self._anggota:
 57 |             raise DataDuplikat(f"ID anggota {anggota.id} sudah terdaftar")
 58 |         self._anggota[anggota.id] = anggota
 59 |
```

- **Baris 52** — Komentar penanda bagian anggota.
- **Baris 53** — Menambahkan objek anggota, contoh `perpus.tambah_anggota(Mahasiswa("MHS003", "Sari", "Informatika"))`.
- **Baris 54** — `isinstance(anggota, Anggota)`: menerima semua turunan abstract class `Anggota` — `Mahasiswa`, `Dosen`, `Umum`, dan juga `AsistenDosen` (diamond) karena ia tetap turunan `Anggota`.
- **Baris 55** — Selain itu ditolak dengan `TypeError`.
- **Baris 56** — Cek apakah ID sudah dipakai (kunci dictionary).
- **Baris 57** — Lempar `DataDuplikat`, contoh: `ID anggota MHS001 sudah terdaftar`.
- **Baris 58** — Simpan ke dictionary: `self._anggota["MHS003"] = anggota`.
- **Baris 59** — Baris kosong.

## Baris 60–65: `cari_anggota()`

```python
 60 |     def cari_anggota(self, id_anggota):
 61 |         id_anggota = str(id_anggota).strip().upper()
 62 |         if id_anggota not in self._anggota:
 63 |             raise DataTidakDitemukan(f"Anggota dengan ID {id_anggota} tidak ditemukan")
 64 |         return self._anggota[id_anggota]
 65 |
```

- **Baris 60** — Mencari anggota berdasarkan ID persis.
- **Baris 61** — Normalisasi input, contoh `"mhs001 "` → `"MHS001"` (ID di `Anggota` juga disimpan huruf besar).
- **Baris 62** — Cek keberadaan ID sebagai kunci.
- **Baris 63** — Jika tidak ada: `DataTidakDitemukan`, contoh `Anggota dengan ID MHS999 tidak ditemukan`.
- **Baris 64** — Mengembalikan objek anggota. Dipakai ulang oleh `hapus_anggota()`, `pinjam()`, dan `bayar_denda()`.
- **Baris 65** — Baris kosong.

## Baris 66–69: `cari_anggota_kata()`

```python
 66 |     def cari_anggota_kata(self, kata):
 67 |         kata = kata.strip().lower()
 68 |         return [a for a in self._anggota.values() if kata in f"{a.id} {a.nama}".lower()]
 69 |
```

- **Baris 66** — Pencarian anggota berdasarkan kata kunci (ID atau nama).
- **Baris 67** — Rapikan dan kecilkan kata kunci.
- **Baris 68** — List comprehension satu baris: setiap anggota yang teks gabungan `"ID nama"`-nya (dikecilkan) mengandung kata kunci. Di sini tidak perlu `getattr` karena **semua** anggota pasti punya `id` dan `nama` (didefinisikan di class induk `Anggota`). Contoh: `cari_anggota_kata("mhs")` → `[Nadia, Fajar]`.
- **Baris 69** — Baris kosong.

## Baris 70–80: `hapus_anggota()` dan `daftar_anggota()`

```python
 70 |     def hapus_anggota(self, id_anggota):
 71 |         anggota = self.cari_anggota(id_anggota)
 72 |         if self.pinjaman_aktif(anggota):
 73 |             raise PeminjamanDitolak(f"{anggota.nama} masih memiliki pinjaman aktif")
 74 |         if anggota.total_denda > 0:
 75 |             raise PeminjamanDitolak(f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}")
 76 |         return self._anggota.pop(anggota.id)
 77 |
 78 |     def daftar_anggota(self):
 79 |         return list(self._anggota.values())
 80 |
```

- **Baris 70** — Menghapus anggota berdasarkan ID.
- **Baris 71** — Cari dulu (sekaligus validasi keberadaan).
- **Baris 72** — Aturan 1: anggota yang masih punya pinjaman aktif tidak boleh dihapus. `self.pinjaman_aktif(anggota)` mengembalikan list; list kosong bernilai `False`, list berisi bernilai `True` (*truthiness*).
- **Baris 73** — Pesan contoh: `Nadia masih memiliki pinjaman aktif`.
- **Baris 74** — Aturan 2: anggota yang masih punya denda tidak boleh dihapus. `total_denda` adalah property read-only dari `Anggota` (atribut privat `__total_denda`).
- **Baris 75** — Pesan contoh: `Nadia masih memiliki denda Rp3.000` (memakai `rupiah()`).
- **Baris 76** — Hapus dengan `pop` dan kembalikan objeknya (agar nama bisa ditampilkan oleh `main.py`).
- **Baris 77** — Baris kosong.
- **Baris 78** — Mengambil semua anggota.
- **Baris 79** — Mengembalikan list baru berisi objek anggota (salinan, bukan dictionary aslinya).
- **Baris 80** — Baris kosong.

## Baris 81–85: TRANSAKSI — `pinjaman_aktif()`

```python
 81 |     # ===================== TRANSAKSI =====================
 82 |     def pinjaman_aktif(self, anggota=None):
 83 |         return [p for p in self._peminjaman
 84 |                 if p.aktif and (anggota is None or p.anggota is anggota)]
 85 |
```

- **Baris 81** — Komentar penanda bagian transaksi.
- **Baris 82** — Mengambil daftar pinjaman yang belum dikembalikan. Parameter `anggota=None` membuat method ini **dua fungsi dalam satu**: tanpa argumen → semua pinjaman aktif; dengan argumen → pinjaman aktif milik satu anggota.
- **Baris 83** — List comprehension dari list `self._peminjaman`...
- **Baris 84** — ...dengan syarat: `p.aktif` (property di `Peminjaman`: `True` jika `tanggal_kembali` masih `None`) **dan** (`anggota is None` atau pemilik transaksinya adalah objek anggota yang sama). `is None` adalah cara baku membandingkan dengan `None`; `p.anggota is anggota` membandingkan **identitas objek**. Contoh: `perpus.pinjaman_aktif(nadia)` → `[P0001]`.
- **Baris 85** — Baris kosong.

## Baris 86–91: `pinjam()` — Persiapan

Method terpenting di file ini. Langkah pertama adalah mengambil semua data yang diperlukan sebelum memeriksa aturan.

```python
 86 |     def pinjam(self, id_anggota, kode_koleksi, tanggal=None):
 87 |         tanggal = tanggal or date.today()
 88 |         anggota = self.cari_anggota(id_anggota)
 89 |         koleksi = self.cari_koleksi(kode_koleksi)
 90 |         aktif = self.pinjaman_aktif(anggota)
 91 |
```

- **Baris 86** — Method peminjaman. Menerima ID anggota, kode koleksi, dan tanggal (opsional, berguna untuk testing/simulasi), contoh `perpus.pinjam("MHS001", "B001")`.
- **Baris 87** — `tanggal or date.today()`: jika `tanggal` bernilai `None` (falsy), pakai tanggal hari ini. Default `None` dipakai karena jika ditulis `tanggal=date.today()` di parameter, nilainya hanya dihitung **sekali** saat program dimuat.
- **Baris 88** — Ambil objek anggota. Jika ID salah, `DataTidakDitemukan` langsung terlempar dan proses berhenti.
- **Baris 89** — Ambil objek koleksi. Jika kode salah, `DataTidakDitemukan` terlempar.
- **Baris 90** — Simpan daftar pinjaman aktif anggota ini ke variabel `aktif` agar tidak dihitung berulang-ulang di aturan 3, 4, dan 5.
- **Baris 91** — Baris kosong: pemisah antara persiapan dan pemeriksaan aturan.

## Baris 92–95: `pinjam()` — Aturan 1: Koleksi harus bisa dipinjam

Urutan validasi: (1) koleksi → (2) denda → (3) keterlambatan → (4) batas jumlah → (5) koleksi yang sama. Semua dicek **sebelum** stok dikurangi, jadi jika ditolak tidak ada data yang berubah.

```python
 92 |         if not koleksi.bisa_dipinjam():
 93 |             if koleksi.stok > 0:
 94 |                 raise PeminjamanDitolak(f"{koleksi.jenis()} '{koleksi.judul}' hanya baca di tempat")
 95 |             raise PeminjamanDitolak(f"Stok '{koleksi.judul}' sedang habis")
```

- **Baris 92** — Memanggil `koleksi.bisa_dipinjam()` — contoh **polymorphism**: untuk `Buku`/`Majalah`/`EBook` hasilnya `stok > 0`, sedangkan `Referensi` meng-override selalu `False`. Perpustakaan tidak perlu `if isinstance(koleksi, Referensi)`.
- **Baris 93** — Membedakan **alasan** penolakan: jika tidak bisa dipinjam padahal stok masih ada, berarti koleksinya memang hanya baca di tempat (Referensi).
- **Baris 94** — Pesan contoh: `Referensi 'Kamus Besar Bahasa Indonesia' hanya baca di tempat`. `koleksi.jenis()` adalah method abstract yang diimplementasikan tiap subclass.
- **Baris 95** — Jika stoknya 0: `Stok 'Bumi Manusia' sedang habis`. Tidak perlu `else` karena `raise` di baris 94 sudah menghentikan fungsi.

## Baris 96–97: `pinjam()` — Aturan 2: Tidak boleh punya denda

```python
 96 |         if anggota.total_denda > 0:
 97 |             raise PeminjamanDitolak(f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}")
```

- **Baris 96** — Anggota yang masih punya tunggakan denda (> 0) tidak boleh meminjam lagi.
- **Baris 97** — Pesan contoh: `Nadia masih memiliki denda Rp3.000`.

## Baris 98–99: `pinjam()` — Aturan 3: Tidak boleh ada pinjaman terlambat

```python
 98 |         if any(p.terlambat(tanggal) for p in aktif):
 99 |             raise PeminjamanDitolak(f"{anggota.nama} memiliki pinjaman yang terlambat")
```

- **Baris 98** — `any(...)` dengan **generator expression**: `True` jika ada minimal satu pinjaman aktif yang sudah lewat jatuh tempo **pada tanggal peminjaman baru**. Denda belum tercatat karena buku belum dikembalikan, maka aturan ini terpisah dari aturan 2. Catatan: pinjaman E-Book yang terlambat juga menghalangi, walaupun E-Book tidak kena denda.
- **Baris 99** — Pesan contoh: `Nadia memiliki pinjaman yang terlambat`.

## Baris 100–102: `pinjam()` — Aturan 4: Batas jumlah pinjaman

```python
100 |         if len(aktif) >= anggota.MAKS_PINJAM:
101 |             raise PeminjamanDitolak(
102 |                 f"{anggota.jenis()} hanya boleh meminjam maksimal {anggota.MAKS_PINJAM} koleksi")
```

- **Baris 100** — Membandingkan jumlah pinjaman aktif dengan `anggota.MAKS_PINJAM`. Ini **class attribute** yang nilainya berbeda per subclass (Mahasiswa 3, Dosen 5, Umum 2, AsistenDosen 3 diwarisi dari Mahasiswa via MRO). Satu baris kode berlaku untuk semua jenis anggota — polymorphism lewat atribut.
- **Baris 101** — `raise PeminjamanDitolak(` — argumen dipecah ke baris berikutnya agar baris tidak terlalu panjang (di dalam tanda kurung Python mengizinkan pindah baris).
- **Baris 102** — Isi pesan, contoh untuk Nadia: `Mahasiswa hanya boleh meminjam maksimal 3 koleksi`; untuk Bu Ida: `Dosen hanya boleh meminjam maksimal 5 koleksi`.

## Baris 103–105: `pinjam()` — Aturan 5: Tidak boleh meminjam koleksi yang sama dua kali

```python
103 |         if any(p.koleksi is koleksi for p in aktif):
104 |             raise PeminjamanDitolak(f"{anggota.nama} sedang meminjam '{koleksi.judul}'")
105 |
```

- **Baris 103** — Cek apakah anggota sedang meminjam **objek koleksi yang sama** (`is`). Contoh: Nadia sudah pinjam B001 lalu mencoba pinjam B001 lagi.
- **Baris 104** — Pesan contoh: `Nadia sedang meminjam 'Laskar Pelangi'`.
- **Baris 105** — Baris kosong: semua aturan lolos, lanjut ke pencatatan.

## Baris 106–110: `pinjam()` — Mencatat Transaksi

```python
106 |         koleksi.kurangi_stok()
107 |         transaksi = Peminjaman(f"P{len(self._peminjaman) + 1:04d}", anggota, koleksi, tanggal)
108 |         self._peminjaman.append(transaksi)
109 |         return transaksi
110 |
```

- **Baris 106** — Stok dikurangi 1 lewat method `kurangi_stok()` milik `Koleksi` (stok tidak diubah langsung → enkapsulasi). Contoh B001: 3 → 2.
- **Baris 107** — Membuat objek `Peminjaman` baru. ID dibuat dari jumlah transaksi + 1 dengan f-string `:04d` = bilangan bulat (`d`) lebar 4 digit diisi nol di depan (`04`). Contoh: transaksi pertama `len = 0` → `f"P{1:04d}"` → `"P0001"`; transaksi ke-12 → `"P0012"`. ID selalu unik karena transaksi tidak pernah dihapus. Objek `Peminjaman` sendiri **memiliki** anggota dan koleksi (composition berlapis).
- **Baris 108** — Transaksi ditambahkan ke list riwayat.
- **Baris 109** — Objek transaksi dikembalikan agar pemanggil (`main.py`) bisa menampilkan ID dan jatuh tempo, contoh `t.jatuh_tempo` → 7 hari setelah tanggal pinjam untuk mahasiswa.
- **Baris 110** — Baris kosong.

## Baris 111–117: `cari_peminjaman()`

```python
111 |     def cari_peminjaman(self, id_pinjam):
112 |         id_pinjam = str(id_pinjam).strip().upper()
113 |         for p in self._peminjaman:
114 |             if p.id == id_pinjam:
115 |                 return p
116 |         raise DataTidakDitemukan(f"Peminjaman {id_pinjam} tidak ditemukan")
117 |
```

- **Baris 111** — Mencari transaksi berdasarkan ID, contoh `"p0001"`.
- **Baris 112** — Normalisasi: `"p0001 "` → `"P0001"`.
- **Baris 113** — Karena transaksi disimpan di **list** (bukan dict), pencarian dilakukan dengan perulangan satu per satu (linear search).
- **Baris 114** — Di sini dipakai `==` karena yang dibandingkan adalah **nilai string** ID, bukan identitas objek. (Bandingkan dengan `is` di baris 45/84/103 yang membandingkan objek.)
- **Baris 115** — Begitu ketemu, langsung `return` (loop berhenti).
- **Baris 116** — Jika loop selesai tanpa `return`, berarti tidak ada: `Peminjaman P0099 tidak ditemukan`.
- **Baris 117** — Baris kosong.

## Baris 118–127: `kembalikan()`

```python
118 |     def kembalikan(self, id_pinjam, tanggal=None):
119 |         transaksi = self.cari_peminjaman(id_pinjam)
120 |         if not transaksi.aktif:
121 |             raise PeminjamanDitolak(f"Peminjaman {transaksi.id} sudah dikembalikan")
122 |         denda = transaksi.kembalikan(tanggal)
123 |         transaksi.koleksi.tambah_stok()
124 |         if denda:
125 |             transaksi.anggota.tambah_denda(denda)
126 |         return transaksi
127 |
```

- **Baris 118** — Proses pengembalian berdasarkan ID transaksi dan tanggal kembali (opsional).
- **Baris 119** — Cari transaksinya (bisa melempar `DataTidakDitemukan`).
- **Baris 120** — Cek transaksi masih aktif (belum dikembalikan).
- **Baris 121** — Jika sudah dikembalikan: `Peminjaman P0001 sudah dikembalikan`. Dicek di sini agar error yang muncul adalah `PeminjamanDitolak` (keluarga exception perpustakaan) sebelum masuk ke `Peminjaman.kembalikan()` yang juga punya pengaman `ValueError`.
- **Baris 122** — **Delegasi** ke objek transaksi: `Peminjaman.kembalikan()` mengisi tanggal kembali dan menghitung denda = hari terlambat × `DENDA_PER_HARI` anggota (0 jika koleksi digital). Jika tanggal kembali sebelum tanggal pinjam, `ValueError` dilempar di sana **sebelum** stok diubah.
- **Baris 123** — Stok koleksi dikembalikan +1 lewat `tambah_stok()`, contoh B001: 2 → 3.
- **Baris 124** — `if denda:` — angka 0 bernilai falsy, jadi blok di bawah hanya jalan jika ada denda.
- **Baris 125** — Denda dicatat ke akun anggota lewat `tambah_denda()` (atribut privat tidak bisa diubah langsung). Contoh terlambat 3 hari, mahasiswa: 3 × Rp1.000 = Rp3.000.
- **Baris 126** — Mengembalikan objek transaksi (berisi `denda`, `tanggal_kembali`, `status` "Dikembalikan").
- **Baris 127** — Baris kosong.

## Baris 128–133: `bayar_denda()`

```python
128 |     def bayar_denda(self, id_anggota, jumlah):
129 |         anggota = self.cari_anggota(id_anggota)
130 |         if anggota.total_denda == 0:
131 |             raise PeminjamanDitolak(f"{anggota.nama} tidak memiliki denda")
132 |         return anggota.bayar_denda(jumlah)
133 |
```

- **Baris 128** — Membayar denda anggota sebesar `jumlah`.
- **Baris 129** — Cari anggota.
- **Baris 130** — Jika tidak punya denda sama sekali...
- **Baris 131** — ...tolak dengan pesan ramah: `Fajar tidak memiliki denda`.
- **Baris 132** — Delegasi ke `Anggota.bayar_denda()` yang memvalidasi jumlah (harus int > 0 dan tidak melebihi denda) lalu mengembalikan **sisa denda**. Contoh denda Rp3.000, bayar 2000 → mengembalikan `1000`.
- **Baris 133** — Baris kosong.

## Baris 134–143: LAPORAN — Method Pembantu

```python
134 |     # ===================== LAPORAN =====================
135 |     def daftar_peminjaman(self):
136 |         return list(self._peminjaman)
137 |
138 |     def pinjaman_terlambat(self, tanggal=None):
139 |         return [p for p in self.pinjaman_aktif() if p.terlambat(tanggal)]
140 |
141 |     def total_denda_tertunggak(self):
142 |         return sum(a.total_denda for a in self._anggota.values())
143 |
```

- **Baris 134** — Komentar penanda bagian laporan.
- **Baris 135** — Mengambil seluruh riwayat peminjaman (aktif maupun selesai).
- **Baris 136** — `list(...)` membuat salinan list agar list internal tidak bisa diubah dari luar.
- **Baris 137** — Baris kosong.
- **Baris 138** — Mengambil pinjaman yang terlambat pada tanggal tertentu (default hari ini).
- **Baris 139** — List comprehension yang **memakai ulang** `pinjaman_aktif()` (tanpa argumen = semua anggota) lalu menyaring yang `terlambat(tanggal)`.
- **Baris 140** — Baris kosong.
- **Baris 141** — Menghitung total denda yang belum dibayar seluruh anggota.
- **Baris 142** — `sum()` dengan generator expression: menjumlahkan `total_denda` setiap anggota tanpa membuat list perantara. Contoh Nadia Rp3.000 + Budi Rp4.000 → `7000`.
- **Baris 143** — Baris kosong.

## Baris 144–162: `laporan()`

Laporan disusun sebagai list baris teks lalu digabung menjadi satu string.

```python
144 |     def laporan(self, tanggal=None):
145 |         """ringkasan() dipanggil pada semua objek tanpa cek tipe (polymorphism)."""
146 |         baris = [f"=== LAPORAN {self.nama.upper()} ===", "", "-- Koleksi --"]
147 |         baris += [k.ringkasan() for k in self._koleksi.values()] or ["(kosong)"]
148 |         baris += ["", "-- Anggota --"]
149 |         baris += [a.ringkasan() for a in self._anggota.values()] or ["(kosong)"]
150 |         baris += ["", "-- Peminjaman Aktif --"]
151 |         baris += [p.ringkasan(tanggal) for p in self.pinjaman_aktif()] or ["(tidak ada)"]
152 |         baris += [
153 |             "",
154 |             f"Jumlah koleksi         : {len(self._koleksi)} judul",
155 |             f"Jumlah anggota         : {len(self._anggota)}",
156 |             f"Peminjaman aktif       : {len(self.pinjaman_aktif())}",
157 |             f"Peminjaman terlambat   : {len(self.pinjaman_terlambat(tanggal))}",
158 |             f"Total denda tertunggak : {rupiah(self.total_denda_tertunggak())}",
159 |         ]
160 |         return "\n".join(baris)
161 |
162 |
```

- **Baris 144** — Membuat laporan teks lengkap. `tanggal` opsional dipakai untuk menghitung keterlambatan.
- **Baris 145** — Docstring menyebut konsep kuncinya: **polymorphism** — `ringkasan()` dipanggil pada semua objek tanpa mengecek tipenya.
- **Baris 146** — Inisialisasi list `baris` dengan judul, baris kosong, dan subjudul. `self.nama.upper()` → `"=== LAPORAN PERPUSTAKAAN KAMPUS ==="`.
- **Baris 147** — Polymorphism: `k.ringkasan()` dipanggil untuk setiap koleksi; Buku, Majalah, Referensi, dan EBook masing-masing menjalankan versi override-nya sendiri (misal EBook menambahkan `| Digital: PDF, 4.5 MB`, Referensi menambahkan `| Baca di tempat`). Trik `[...] or ["(kosong)"]`: list kosong bernilai falsy, sehingga yang ditambahkan adalah `["(kosong)"]`. `+=` pada list = menambahkan semua elemennya (seperti `extend`).
- **Baris 148** — Menambahkan baris kosong dan subjudul anggota.
- **Baris 149** — Polymorphism lagi: `a.ringkasan()` milik `Anggota` memanggil `jenis()` dan `info_tambahan()` yang berbeda di tiap subclass (Mahasiswa menampilkan Prodi, Dosen menampilkan Bidang, AsistenDosen menampilkan keduanya lewat MRO).
- **Baris 150** — Subjudul peminjaman aktif.
- **Baris 151** — `p.ringkasan(tanggal)` untuk setiap pinjaman aktif; jika ada yang terlambat, ringkasan menampilkan `TERLAMBAT n hari (denda ...)`. Jika kosong → `"(tidak ada)"`.
- **Baris 152** — Mulai menambahkan blok statistik dengan list bertingkat beberapa baris.
- **Baris 153** — String kosong → baris kosong pemisah di laporan.
- **Baris 154** — Jumlah judul koleksi = jumlah kunci dictionary, contoh `Jumlah koleksi         : 6 judul`. Spasi dalam teks sengaja dibuat agar tanda `:` sejajar.
- **Baris 155** — Jumlah anggota, contoh `5`.
- **Baris 156** — Jumlah pinjaman aktif (memakai ulang `pinjaman_aktif()`).
- **Baris 157** — Jumlah pinjaman terlambat pada `tanggal` (memakai ulang `pinjaman_terlambat()`).
- **Baris 158** — Total denda tertunggak diformat Rupiah, contoh `Rp3.000`.
- **Baris 159** — Penutup list statistik.
- **Baris 160** — `"\n".join(baris)` menggabungkan semua elemen list menjadi satu string dengan pemisah baris baru. Method ini **mengembalikan** string (tidak langsung `print`), sehingga bisa dicetak oleh `main.py` atau diuji di `test_perpustakaan.py`.
- **Baris 161** — Baris kosong.
- **Baris 162** — Baris kosong kedua — dua baris kosong sebelum fungsi tingkat atas (PEP 8).

## Baris 163–174: `buat_data_contoh()` — Koleksi

Fungsi biasa (bukan method) yang membuat objek `Perpustakaan` lengkap dengan data awal.

```python
163 | def buat_data_contoh():
164 |     """Data awal yang dibuat setiap kali program dijalankan (tersimpan di memori)."""
165 |     perpus = Perpustakaan("Perpustakaan Kampus")
166 |     for koleksi in (
167 |         Buku("B001", "Laskar Pelangi", 2005, "Andrea Hirata", "Bentang Pustaka", stok=3),
168 |         Buku("B002", "Bumi Manusia", 1980, "Pramoedya Ananta Toer", "Hasta Mitra", stok=2),
169 |         Buku("B003", "Pemrograman Python untuk Pemula", 2021, "Budi Raharjo", "Informatika", stok=4),
170 |         Majalah("M001", "Majalah Tempo", 2024, "Edisi Januari", stok=2),
171 |         EBook("E001", "Belajar Python Dasar", 2023, "Tim Penulis", "Penerbit Digital", "PDF", 4.5, stok=5),
172 |         Referensi("R001", "Kamus Besar Bahasa Indonesia", 2016, "Badan Bahasa", "Balai Pustaka"),
173 |     ):
174 |         perpus.tambah_koleksi(koleksi)
```

- **Baris 163** — Definisi fungsi tingkat modul (di luar class). Diimpor oleh `main.py`.
- **Baris 164** — Docstring: data dibuat ulang setiap program dijalankan dan hanya disimpan di memori (tidak ada database/file), jadi perubahan hilang saat program ditutup.
- **Baris 165** — Membuat **objek** `Perpustakaan` — instansiasi class. Variabel `perpus` berisi objek dengan dictionary/list masih kosong.
- **Baris 166** — Perulangan `for` atas sebuah **tuple** berisi objek-objek koleksi yang langsung dibuat di dalamnya.
- **Baris 167** — `Buku` B001 "Laskar Pelangi" (2005), penulis Andrea Hirata, penerbit Bentang Pustaka, `stok=3` (argumen keyword).
- **Baris 168** — `Buku` B002 "Bumi Manusia" (1980), stok 2.
- **Baris 169** — `Buku` B003 "Pemrograman Python untuk Pemula" (2021), stok 4.
- **Baris 170** — `Majalah` M001 "Majalah Tempo" (2024), edisi "Edisi Januari", stok 2 — turunan langsung `Koleksi` (single inheritance), tidak punya penulis.
- **Baris 171** — `EBook` E001 "Belajar Python Dasar" (2023), format `"PDF"`, ukuran `4.5` MB, `stok=5` (= jumlah lisensi). EBook = multiple inheritance (`DigitalMixin` + `Buku`) dan tidak kena denda.
- **Baris 172** — `Referensi` R001 "Kamus Besar Bahasa Indonesia" (2016). Stok default 1, tetapi `bisa_dipinjam()` selalu `False` → hanya baca di tempat (multilevel: Koleksi → Buku → Referensi).
- **Baris 173** — Penutup tuple dan header `for`.
- **Baris 174** — Setiap objek didaftarkan lewat `tambah_koleksi()` — sehingga validasi `isinstance` dan cek duplikat ikut berjalan, bukan memasukkan langsung ke `_koleksi`.

## Baris 175–183: `buat_data_contoh()` — Anggota dan Hasil

```python
175 |     for anggota in (
176 |         Mahasiswa("MHS001", "Nadia", "Informatika", "081234567890", email="nadia@kampus.ac.id"),
177 |         Mahasiswa("MHS002", "Fajar", "Sistem Informasi"),
178 |         Dosen("DSN001", "Ir. Ida, S.Kom., M.T.", "Pemrograman", email="ida@kampus.ac.id"),
179 |         AsistenDosen("ASD001", "Rizky Pratama", "Informatika", "Praktikum PBO"),
180 |         Umum("UMM001", "Budi Santoso", "085600000000"),
181 |     ):
182 |         perpus.tambah_anggota(anggota)
183 |     return perpus
```

- **Baris 175** — Perulangan atas tuple berisi objek anggota.
- **Baris 176** — `Mahasiswa` MHS001 Nadia, prodi Informatika, telepon `"081234567890"`, `email=` dikirim sebagai keyword dan diteruskan lewat `**kwargs` ke `Anggota.__init__`.
- **Baris 177** — `Mahasiswa` MHS002 Fajar, prodi Sistem Informasi (tanpa telepon/email, memakai default).
- **Baris 178** — `Dosen` DSN001 "Ir. Ida, S.Kom., M.T.", bidang Pemrograman, beserta email. Hak dosen: maks 5 koleksi, 14 hari, denda Rp500/hari.
- **Baris 179** — `AsistenDosen` ASD001 Rizky Pratama, prodi Informatika, bidang "Praktikum PBO" — contoh diamond inheritance (Mahasiswa + Dosen).
- **Baris 180** — `Umum` UMM001 Budi Santoso, telepon `"085600000000"`. Hak umum: maks 2 koleksi, 7 hari, denda Rp2.000/hari.
- **Baris 181** — Penutup tuple dan header `for`.
- **Baris 182** — Setiap anggota didaftarkan lewat `tambah_anggota()` (tervalidasi).
- **Baris 183** — Mengembalikan objek `Perpustakaan` yang sudah terisi 6 koleksi dan 5 anggota. Di `main.py`: `self.perpus = buat_data_contoh()`.

## Alur Peminjaman & Pengembalian

Contoh memakai data dari `buat_data_contoh()`. Nadia (MHS001) adalah **Mahasiswa**: maks 3 koleksi, lama pinjam 7 hari, denda Rp1.000/hari. Buku B001 "Laskar Pelangi" stok awal 3.

```python
from datetime import date
from perpustakaan import buat_data_contoh

perpus = buat_data_contoh()
t = perpus.pinjam("MHS001", "B001", date(2026, 11, 1))
t.id, t.jatuh_tempo            # ('P0001', datetime.date(2026, 11, 8))
perpus.cari_koleksi("B001").stok   # 2

perpus.kembalikan("P0001", date(2026, 11, 11))
t.denda                        # 3000  (terlambat 3 hari x Rp1.000)
perpus.cari_koleksi("B001").stok   # 3
perpus.cari_anggota("MHS001").total_denda  # 3000

perpus.pinjam("MHS001", "B002")    # PeminjamanDitolak: Nadia masih memiliki denda Rp3.000
perpus.bayar_denda("MHS001", 3000) # 0 (sisa denda)
```

Langkah demi langkah:

1. **`pinjam("MHS001", "B001", 1 Nov 2026)`** — `cari_anggota` → objek Nadia; `cari_koleksi` → objek B001; `pinjaman_aktif(Nadia)` → `[]`.
2. Lima aturan diperiksa berurutan: B001 bisa dipinjam (stok 3) ✔, denda Rp0 ✔, tidak ada pinjaman terlambat ✔, 0 < 3 ✔, belum meminjam B001 ✔.
3. `kurangi_stok()` → stok B001 **3 → 2**. Dibuat `Peminjaman("P0001", Nadia, B001, 1 Nov)` dengan jatuh tempo 1 Nov + 7 hari = **8 Nov 2026**. Transaksi dimasukkan ke `_peminjaman`.
4. **`kembalikan("P0001", 11 Nov 2026)`** — transaksi ditemukan dan masih aktif. `Peminjaman.kembalikan()` mengisi tanggal kembali; hari terlambat = 11 − 8 = **3 hari**; B001 adalah Buku (`kena_denda()` = True) → denda = 3 × Rp1.000 = **Rp3.000**.
5. `tambah_stok()` → stok B001 **2 → 3**. Karena denda ≠ 0, `Nadia.tambah_denda(3000)` → total denda Nadia **Rp3.000**.
6. Pinjaman berikutnya oleh Nadia ditolak oleh aturan 2 sampai ia membayar: `bayar_denda("MHS001", 3000)` → sisa **0**, dan Nadia boleh meminjam lagi.

Catatan: jika yang dipinjam E-Book E001 lalu terlambat, denda = 0 karena `DigitalMixin.kena_denda()` mengembalikan `False` — tetapi selama belum dikembalikan, pinjaman terlambat itu tetap memblokir peminjaman baru (aturan 3).

### Daftar Alasan Penolakan `pinjam()`

| Urutan | Kondisi | Exception | Contoh pesan error |
|---|---|---|---|
| — | ID anggota tidak terdaftar | `DataTidakDitemukan` | `Anggota dengan ID MHS999 tidak ditemukan` |
| — | Kode koleksi tidak terdaftar | `DataTidakDitemukan` | `Koleksi dengan kode X999 tidak ditemukan` |
| 1a | Koleksi hanya baca di tempat (Referensi) | `PeminjamanDitolak` | `Referensi 'Kamus Besar Bahasa Indonesia' hanya baca di tempat` |
| 1b | Stok koleksi 0 | `PeminjamanDitolak` | `Stok 'Bumi Manusia' sedang habis` |
| 2 | Anggota masih punya denda | `PeminjamanDitolak` | `Nadia masih memiliki denda Rp3.000` |
| 3 | Ada pinjaman aktif yang terlambat | `PeminjamanDitolak` | `Nadia memiliki pinjaman yang terlambat` |
| 4 | Jumlah pinjaman aktif ≥ `MAKS_PINJAM` | `PeminjamanDitolak` | `Mahasiswa hanya boleh meminjam maksimal 3 koleksi` |
| 5 | Sedang meminjam koleksi yang sama | `PeminjamanDitolak` | `Nadia sedang meminjam 'Laskar Pelangi'` |

Penolakan pada `kembalikan()`: ID tidak ada → `DataTidakDitemukan` (`Peminjaman P0099 tidak ditemukan`); sudah dikembalikan → `PeminjamanDitolak` (`Peminjaman P0001 sudah dikembalikan`); tanggal kembali sebelum tanggal pinjam → `ValueError` dari `Peminjaman`.

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Kenapa `Perpustakaan` tidak mewarisi `Koleksi` atau `Anggota`?**
   Karena relasinya *has-a*, bukan *is-a*. Perpustakaan *memiliki* banyak buku dan anggota; ia bukan sebuah buku. Maka dipakai composition: objek-objek disimpan sebagai atribut (`_koleksi`, `_anggota`, `_peminjaman`).
2. **Kenapa koleksi dan anggota disimpan di dictionary, sedangkan peminjaman di list?**
   Koleksi/anggota dicari berdasarkan kode/ID unik → dictionary cepat dan otomatis mencegah kunci ganda. Peminjaman adalah riwayat berurutan yang tidak dihapus, dan urutannya dipakai untuk ID `P0001`, `P0002`, ...
3. **Apa gunanya `isinstance(koleksi, Koleksi)` padahal `Koleksi` abstract?**
   Justru karena abstract, `Koleksi` menjadi "kontrak" bersama. `isinstance` bernilai `True` untuk semua subclass (Buku, Majalah, Referensi, EBook), sehingga satu pengecekan cukup untuk semua jenis koleksi, termasuk subclass baru di masa depan.
4. **Apa beda `is` dan `==` di file ini?**
   `is` membandingkan identitas objek (objek yang sama di memori), dipakai untuk `p.koleksi is koleksi` dan `p.anggota is anggota`. `==` membandingkan nilai, dipakai untuk membandingkan string ID di `cari_peminjaman()`.
5. **Di mana polymorphism terlihat?**
   Di `laporan()` (`ringkasan()` dipanggil pada semua objek tanpa cek tipe), di `pinjam()` (`bisa_dipinjam()` berbeda untuk Referensi, `MAKS_PINJAM` berbeda per jenis anggota), dan di `kembalikan()` (denda bergantung `kena_denda()` koleksi dan `DENDA_PER_HARI` anggota).
6. **Kenapa urutan aturan di `pinjam()` penting, dan kenapa stok dikurangi paling akhir?**
   Semua aturan harus lolos dulu; jika stok dikurangi di awal lalu ada aturan yang gagal, stok jadi salah. Urutannya juga menentukan pesan mana yang muncul jika ada beberapa pelanggaran sekaligus.
7. **Kenapa memakai exception kustom, bukan `print` pesan error?**
   Supaya kelas `Perpustakaan` tidak bergantung pada tampilan. Ia cukup `raise`; `main.py` yang menangkap (`except PerpustakaanError`) dan menampilkan pesan, sedangkan `test_perpustakaan.py` bisa menguji dengan `assertRaises`.
8. **Kenapa `getattr(k, 'penulis', '')` dan bukan `k.penulis`?**
   `Majalah` tidak punya atribut `penulis`; `k.penulis` akan melempar `AttributeError`. `getattr` dengan default `''` membuat pencarian tetap jalan untuk semua jenis koleksi.

## Ringkasan

- `Perpustakaan` adalah contoh **composition (has-a)**: memiliki koleksi, anggota, dan peminjaman tanpa mewarisi class-class tersebut.
- Penyimpanan: `_koleksi` dan `_anggota` berupa **dictionary** (kunci kode/ID), `_peminjaman` berupa **list** riwayat; ketiganya dibuat di `__init__` agar tiap objek punya data sendiri.
- Validasi memakai `isinstance` terhadap **abstract class** dan **exception kustom** (`DataDuplikat`, `DataTidakDitemukan`, `PeminjamanDitolak`).
- Pola CRUD konsisten untuk koleksi dan anggota: `tambah_`, `cari_`, `cari_..._kata`, `hapus_`, `daftar_`.
- `pinjam()` memeriksa 5 aturan berurutan (bisa dipinjam → denda → terlambat → batas jumlah → koleksi sama) sebelum mengurangi stok dan membuat ID `P{n:04d}`.
- `kembalikan()` mendelegasikan perhitungan denda ke `Peminjaman`, menambah stok, dan mencatat denda ke anggota; `bayar_denda()` mendelegasikan ke `Anggota`.
- Teknik Python yang dipakai: list comprehension, generator expression dengan `any()`/`sum()`, `getattr` dengan default, `is` vs `==`, trik `list or [default]`, `"\n".join()`.
- `laporan()` menunjukkan **polymorphism**: `ringkasan()` dipanggil pada semua objek tanpa cek tipe.
- `buat_data_contoh()` mengisi 6 koleksi dan 5 anggota lewat method resmi, lalu dipakai oleh `main.py`.
