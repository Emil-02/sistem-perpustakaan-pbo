# Penjelasan Baris per Baris: koleksi_turunan.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 2 |
| File | `koleksi_turunan.py` |
| Jumlah baris | 104 |
| Konsep PBO | Single inheritance, multilevel inheritance, multiple inheritance, mixin, MRO, `super()` mengikuti MRO, method overriding, polymorphism, property (getter/setter), class attribute, abstract method |

## Gambaran Umum

File `koleksi_turunan.py` adalah **Bagian 2** dari Sistem Perpustakaan dan berfokus pada **inheritance (pewarisan)**. File ini mengimpor `Koleksi` (abstract class), `Buku`, dan fungsi validasi `teks_wajib` dari `koleksi.py` (Bagian 1), lalu membuat empat class baru: `Majalah` (single inheritance dari `Koleksi`), `Referensi` (multilevel: `Koleksi → Buku → Referensi`), `DigitalMixin` (mixin penambah kemampuan digital), dan `EBook` (multiple inheritance dari `DigitalMixin` dan `Buku`). Class-class ini kemudian dipakai oleh `perpustakaan.py` (Bagian 6) untuk menyimpan data contoh koleksi, oleh `peminjaman.py` (Bagian 5) yang memanggil `bisa_dipinjam()` dan `kena_denda()` secara polimorfis, oleh `main.py` untuk menu tambah koleksi, serta diuji di `test_perpustakaan.py`.

Diagram hierarki singkat:

```text
            Koleksi (ABC)
           /            \
       Majalah          Buku          DigitalMixin
                       /    \          /
               Referensi    EBook ----
```

## Baris 1–12: Docstring Modul dan Import

```python
  1 | """BAGIAN 2 - Inheritance pada koleksi (single, multilevel, multiple/mixin).
  2 |
  3 | Hierarki:
  4 |     Koleksi (abstract)
  5 |     ├── Majalah                    single      : Koleksi -> Majalah
  6 |     └── Buku
  7 |         ├── Referensi              multilevel  : Koleksi -> Buku -> Referensi
  8 |         └── EBook(DigitalMixin, Buku)  multiple: punya dua induk
  9 | """
 10 |
 11 | from koleksi import Buku, Koleksi, teks_wajib
 12 |
```

- **Baris 1–9** — *Docstring modul* (teks dalam tanda kutip tiga `"""`). Bukan kode yang dijalankan, melainkan dokumentasi file. Baris 1 menyebut ini **Bagian 2** yang membahas tiga jenis *inheritance*: single, multilevel, dan multiple (mixin).
  - **Baris 3–8** menggambar pohon hierarki class:
    - `Majalah` → **single inheritance** (satu induk: `Koleksi`).
    - `Referensi` → **multilevel inheritance** (turunan dari `Buku`, yang juga turunan `Koleksi`; jadi "cucu" dari `Koleksi`).
    - `EBook(DigitalMixin, Buku)` → **multiple inheritance** (punya dua induk langsung).
  - **Baris 2** kosong di dalam docstring hanya untuk merapikan teks.
- **Baris 10** — Baris kosong pemisah (gaya PEP 8). Baris kosong lain di file ini (12, 13, 18, 22, 26, 29, 32, 33, 36, 39, 42, 45, 46, 53, 55, 59, 66, 70, 82, 85, 88, 89, 96, 102) juga hanya pemisah agar kode mudah dibaca; dua baris kosong dipakai sebelum definisi class sesuai PEP 8.
- **Baris 11** — `from koleksi import Buku, Koleksi, teks_wajib` mengambil tiga nama dari file `koleksi.py` (Bagian 1):
  - `Koleksi` → *abstract class* induk semua koleksi (dipakai sebagai induk `Majalah`).
  - `Buku` → turunan `Koleksi` (dipakai sebagai induk `Referensi` dan `EBook`).
  - `teks_wajib` → fungsi bantu validasi: menolak teks kosong dan mengembalikan teks yang sudah di-`strip()`.
  Inilah bukti bahwa file ini **bergantung** pada `koleksi.py`; tanpa import, class induk tidak dikenal.
- **Baris 12** — Baris kosong pemisah.

## Baris 13–33: Class Majalah (Single Inheritance)

```python
 13 |
 14 | class Majalah(Koleksi):
 15 |     def __init__(self, kode, judul, tahun, edisi, stok=1):
 16 |         super().__init__(kode, judul, tahun, stok)
 17 |         self.edisi = edisi
 18 |
 19 |     @property
 20 |     def edisi(self):
 21 |         return self._edisi
 22 |
 23 |     @edisi.setter
 24 |     def edisi(self, nilai):
 25 |         self._edisi = teks_wajib(str(nilai), "Edisi")
 26 |
 27 |     def jenis(self):
 28 |         return "Majalah"
 29 |
 30 |     def ringkasan(self):
 31 |         return f"{super().ringkasan()} | Edisi: {self.edisi}"
 32 |
 33 |
```

- **Baris 13** — Baris kosong (bagian dari dua baris kosong sebelum class).
- **Baris 14** — `class Majalah(Koleksi):` mendefinisikan class `Majalah` yang **mewarisi** `Koleksi`. Ini **single inheritance**: hanya satu induk. Semua atribut & method `Koleksi` (`kode`, `judul`, `tahun`, `stok`, `bisa_dipinjam()`, `kurangi_stok()`, dll.) otomatis dimiliki `Majalah`.
- **Baris 15** — Constructor `__init__`. Parameternya sama dengan `Koleksi` ditambah `edisi`. `stok=1` adalah *default argument*: jika tidak diisi, stok = 1.
- **Baris 16** — `super().__init__(kode, judul, tahun, stok)` memanggil constructor induk (`Koleksi.__init__`) supaya kode, judul, tahun, dan stok diisi **sekaligus divalidasi** oleh kode di induk. Kita tidak menulis ulang validasi → *reuse* kode, inti dari inheritance.
- **Baris 17** — `self.edisi = edisi` terlihat seperti mengisi atribut biasa, tetapi karena ada `@edisi.setter` (baris 23), baris ini sebenarnya **memanggil setter** sehingga validasi juga berjalan saat objek dibuat.
- **Baris 18** — Baris kosong.
- **Baris 19** — `@property` adalah *decorator* yang mengubah method di bawahnya menjadi **getter**; diakses seperti atribut (`m.edisi`, tanpa tanda kurung).
- **Baris 20** — `def edisi(self):` nama getter. Nama property = `edisi`.
- **Baris 21** — `return self._edisi` mengembalikan nilai yang disimpan di atribut *protected* `_edisi` (awalan `_` = konvensi "jangan diakses langsung dari luar"). Ini **enkapsulasi**.
- **Baris 22** — Baris kosong.
- **Baris 23** — `@edisi.setter` menandai method berikutnya sebagai **setter** untuk property `edisi`; dipanggil setiap ada `obj.edisi = ...`.
- **Baris 24** — `def edisi(self, nilai):` nama sama dengan getter (aturan wajib property di Python); `nilai` = data yang akan disimpan.
- **Baris 25** — `self._edisi = teks_wajib(str(nilai), "Edisi")`. `str(nilai)` dulu agar edisi berupa angka (mis. `12`) diterima dan menjadi `"12"`. Lalu `teks_wajib` menolak edisi kosong (`""` atau `"   "` → `ValueError: Edisi tidak boleh kosong`).
- **Baris 26** — Baris kosong.
- **Baris 27** — `def jenis(self):` meng-*implementasikan* method abstrak `jenis()` dari `Koleksi`. Wajib, karena `Koleksi` memakai `@abstractmethod`; tanpa method ini `Majalah(...)` akan gagal dibuat (`TypeError`).
- **Baris 28** — Mengembalikan teks `"Majalah"`; dipakai oleh `ringkasan()` di `Koleksi` untuk menampilkan jenis.
- **Baris 29** — Baris kosong.
- **Baris 30** — `def ringkasan(self):` **override** (menimpa) method `ringkasan()` milik `Koleksi`.
- **Baris 31** — `super().ringkasan()` mengambil hasil ringkasan versi `Koleksi`, lalu ditambah `| Edisi: ...`. Ini pola **extend** (memperluas, bukan mengganti total). Contoh: `Majalah("M1", "Tempo", 2024, 12).ringkasan()` →
  `M1 | Majalah   | Tempo (2024) | Stok: 1 | Edisi: 12`.
  Perhatikan `self.jenis()` di dalam `Koleksi.ringkasan()` memanggil versi `Majalah` → contoh **polymorphism**.
- **Baris 32–33** — Dua baris kosong pemisah antar-class.

## Baris 34–46: Class Referensi (Multilevel Inheritance)

```python
 34 | class Referensi(Buku):
 35 |     """Buku referensi (kamus, ensiklopedia) hanya boleh dibaca di tempat."""
 36 |
 37 |     def jenis(self):
 38 |         return "Referensi"
 39 |
 40 |     def bisa_dipinjam(self):
 41 |         return False  # override: walaupun stok ada, tetap tidak bisa dipinjam
 42 |
 43 |     def ringkasan(self):
 44 |         return f"{super().ringkasan()} | Baca di tempat"
 45 |
 46 |
```

- **Baris 34** — `class Referensi(Buku):` mewarisi `Buku`, sedangkan `Buku` mewarisi `Koleksi`. Rantai `Koleksi → Buku → Referensi` disebut **multilevel inheritance**. Karena tidak ada `__init__` sendiri, `Referensi` memakai constructor `Buku` (kode, judul, tahun, penulis, penerbit, stok).
- **Baris 35** — Docstring class: menjelaskan bahwa buku referensi (kamus, ensiklopedia) hanya boleh dibaca di tempat. Inilah alasan bisnis adanya class ini.
- **Baris 36** — Baris kosong.
- **Baris 37** — `def jenis(self):` **override** `Buku.jenis()` (yang mengembalikan `"Buku"`).
- **Baris 38** — Mengembalikan `"Referensi"`. Kebetulan panjangnya 9 karakter, pas dengan format `{self.jenis():<9}` di `Koleksi.ringkasan()` sehingga kolom tetap rapi.
- **Baris 39** — Baris kosong.
- **Baris 40** — `def bisa_dipinjam(self):` **override** `Koleksi.bisa_dipinjam()` (aslinya `return self._stok > 0`).
- **Baris 41** — `return False` → apa pun stoknya, referensi **tidak bisa dipinjam**. Komentar menegaskan hal ini. Bagian lain program (mis. `Perpustakaan`/`Peminjaman`) cukup memanggil `koleksi.bisa_dipinjam()` tanpa perlu `if isinstance(..., Referensi)` → manfaat **polymorphism**.
- **Baris 42** — Baris kosong.
- **Baris 43** — `def ringkasan(self):` **override** lagi.
- **Baris 44** — `super().ringkasan()` di sini memanggil `Buku.ringkasan()`, yang di dalamnya memanggil `Koleksi.ringkasan()`. Jadi hasilnya bertingkat 3 lapis: Koleksi → Buku → Referensi. Contoh:
  `R1 | Referensi | KBBI (2016) | Stok: 2 | Penulis: Badan Bahasa | Penerbit: Balai Pustaka | Baca di tempat`.
- **Baris 45–46** — Dua baris kosong pemisah.

## Baris 47–55: Class DigitalMixin: Docstring dan Class Attribute

```python
 47 | class DigitalMixin:
 48 |     """Mixin: bukan koleksi sendiri, hanya menambah kemampuan 'digital'.
 49 |
 50 |     super() di sini mengikuti MRO class pemakainya,
 51 |     misalnya EBook -> DigitalMixin -> Buku -> Koleksi.
 52 |     """
 53 |
 54 |     FORMAT_DIDUKUNG = ("PDF", "EPUB", "MOBI")
 55 |
```

- **Baris 47** — `class DigitalMixin:` class **tanpa induk eksplisit** (otomatis turunan `object`). Disebut **mixin**: class kecil yang tidak dimaksudkan berdiri sendiri, hanya "dicampurkan" ke class lain untuk menambah kemampuan (di sini: kemampuan digital).
- **Baris 48–52** — Docstring class:
  - Baris 48: menegaskan mixin bukan koleksi sendiri (tidak mewarisi `Koleksi`, tidak punya `kode`/`judul`).
  - Baris 50–51: poin penting — `super()` di dalam mixin **tidak** berarti "induk DigitalMixin" (yaitu `object`), melainkan **class berikutnya dalam MRO objek yang sedang dipakai**. Untuk objek `EBook`, class setelah `DigitalMixin` adalah `Buku`.
  - Baris 49 kosong di dalam docstring; baris 52 penutup `"""`.
- **Baris 53** — Baris kosong.
- **Baris 54** — `FORMAT_DIDUKUNG = ("PDF", "EPUB", "MOBI")` adalah **class attribute** (milik class, sama untuk semua objek). Dipakai *tuple* agar tidak bisa diubah (immutable). Dibaca lewat `self.FORMAT_DIDUKUNG`.
- **Baris 55** — Baris kosong.

## Baris 56–66: Property format_file

```python
 56 |     @property
 57 |     def format_file(self):
 58 |         return self._format_file
 59 |
 60 |     @format_file.setter
 61 |     def format_file(self, nilai):
 62 |         nilai = teks_wajib(nilai, "Format file").upper()
 63 |         if nilai not in self.FORMAT_DIDUKUNG:
 64 |             raise ValueError(f"Format harus salah satu dari {', '.join(self.FORMAT_DIDUKUNG)}")
 65 |         self._format_file = nilai
 66 |
```

- **Baris 56** — `@property` → method berikutnya menjadi getter.
- **Baris 57** — `def format_file(self):` nama property `format_file`.
- **Baris 58** — Mengembalikan atribut protected `_format_file`. Catatan: mixin memakai `self` milik objek `EBook`, jadi atribut ini tersimpan di objek EBook.
- **Baris 59** — Baris kosong.
- **Baris 60** — `@format_file.setter` → method berikutnya adalah setter.
- **Baris 61** — `def format_file(self, nilai):` menerima nilai baru.
- **Baris 62** — `teks_wajib(nilai, "Format file")` memastikan tidak kosong, lalu `.upper()` mengubah ke huruf besar. Jadi `"epub"` atau `" Epub "` menjadi `"EPUB"` (input lebih fleksibel).
- **Baris 63** — `if nilai not in self.FORMAT_DIDUKUNG:` cek apakah format termasuk daftar yang diizinkan.
- **Baris 64** — Jika tidak, lempar `ValueError` dengan pesan `Format harus salah satu dari PDF, EPUB, MOBI` (`', '.join(...)` menggabungkan isi tuple dengan koma).
- **Baris 65** — Jika lolos, simpan ke `self._format_file`.
- **Baris 66** — Baris kosong.

## Baris 67–82: Property ukuran_mb

```python
 67 |     @property
 68 |     def ukuran_mb(self):
 69 |         return self._ukuran_mb
 70 |
 71 |     @ukuran_mb.setter
 72 |     def ukuran_mb(self, nilai):
 73 |         if isinstance(nilai, bool):
 74 |             raise ValueError("Ukuran file harus berupa angka")
 75 |         try:
 76 |             nilai = float(nilai)
 77 |         except (TypeError, ValueError):
 78 |             raise ValueError("Ukuran file harus berupa angka") from None
 79 |         if nilai <= 0:
 80 |             raise ValueError("Ukuran file harus lebih dari 0 MB")
 81 |         self._ukuran_mb = nilai
 82 |
```

- **Baris 67** — `@property` → getter.
- **Baris 68** — `def ukuran_mb(self):` nama property `ukuran_mb` (ukuran file dalam megabyte).
- **Baris 69** — Mengembalikan `_ukuran_mb`.
- **Baris 70** — Baris kosong.
- **Baris 71** — `@ukuran_mb.setter` → setter.
- **Baris 72** — `def ukuran_mb(self, nilai):`.
- **Baris 73** — `isinstance(nilai, bool)` dicek **lebih dulu** karena di Python `bool` adalah turunan `int`; `float(True)` = `1.0` dan akan lolos. Kita tidak mau `True` dianggap ukuran.
- **Baris 74** — Jika bool → `ValueError("Ukuran file harus berupa angka")`.
- **Baris 75** — `try:` mulai blok penanganan error.
- **Baris 76** — `nilai = float(nilai)` mengubah ke bilangan desimal. `"4.5"` → `4.5`, `3` → `3.0`.
- **Baris 77** — `except (TypeError, ValueError):` menangkap kegagalan konversi: `TypeError` untuk `None`/list, `ValueError` untuk teks seperti `"abc"`.
- **Baris 78** — Melempar ulang sebagai `ValueError` dengan pesan yang ramah. `from None` menyembunyikan *traceback* error asli agar pesan ke pengguna bersih.
- **Baris 79** — `if nilai <= 0:` ukuran file harus positif.
- **Baris 80** — Jika 0 atau negatif → `ValueError("Ukuran file harus lebih dari 0 MB")`.
- **Baris 81** — Lolos semua validasi → simpan ke `self._ukuran_mb`.
- **Baris 82** — Baris kosong.

## Baris 83–89: Method kena_denda dan ringkasan pada DigitalMixin

```python
 83 |     def kena_denda(self):
 84 |         return False  # akses digital tidak menimbulkan denda keterlambatan
 85 |
 86 |     def ringkasan(self):
 87 |         return f"{super().ringkasan()} | Digital: {self.format_file}, {self.ukuran_mb:g} MB"
 88 |
 89 |
```

- **Baris 83** — `def kena_denda(self):` **override** `Koleksi.kena_denda()` (aslinya `return True`). Karena di MRO `EBook`, `DigitalMixin` berada **sebelum** `Koleksi`, versi mixin inilah yang dipakai.
- **Baris 84** — `return False` → keterlambatan mengembalikan e-book tidak didenda (komentar: akses digital tidak menimbulkan denda). Modul `Peminjaman` cukup bertanya `koleksi.kena_denda()` → **polymorphism**.
- **Baris 85** — Baris kosong.
- **Baris 86** — `def ringkasan(self):` versi ringkasan milik mixin.
- **Baris 87** — `super().ringkasan()` **mengikuti MRO**: untuk objek `EBook` artinya memanggil `Buku.ringkasan()` (bukan `object`, yang bahkan tidak punya `ringkasan`). Hasilnya ditambah `| Digital: EPUB, 4.5 MB`. Format `:g` menampilkan angka ringkas: `4.5` → `4.5`, `1.0` → `1` (tanpa `.0`). Ini pola **cooperative multiple inheritance**: tiap class menambah bagiannya lalu menyerahkan ke class berikutnya lewat `super()`.
- **Baris 88–89** — Dua baris kosong pemisah.

## Baris 90–104: Class EBook (Multiple Inheritance)

```python
 90 | class EBook(DigitalMixin, Buku):
 91 |     """EBook adalah Buku sekaligus punya kemampuan Digital (multiple inheritance).
 92 |
 93 |     MRO: EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object
 94 |     Stok e-book = jumlah lisensi yang bisa dipinjam bersamaan.
 95 |     """
 96 |
 97 |     def __init__(self, kode, judul, tahun, penulis, penerbit,
 98 |                  format_file="PDF", ukuran_mb=1.0, stok=1):
 99 |         super().__init__(kode, judul, tahun, penulis, penerbit, stok)
100 |         self.format_file = format_file
101 |         self.ukuran_mb = ukuran_mb
102 |
103 |     def jenis(self):
104 |         return "E-Book"
```

- **Baris 90** — `class EBook(DigitalMixin, Buku):` **multiple inheritance**: dua induk langsung. **Urutan penting**: mixin ditulis di **kiri** agar method-nya (`kena_denda`, `ringkasan`) didahulukan dibanding milik `Buku`/`Koleksi`. Jika ditukar `(Buku, DigitalMixin)`, `Buku.ringkasan()` akan ditemukan duluan dan info digital tidak muncul, serta `kena_denda()` kembali `True`.
- **Baris 91–95** — Docstring class:
  - Baris 91: EBook *adalah* Buku (relasi "is-a") sekaligus punya kemampuan digital.
  - Baris 93: **MRO** (*Method Resolution Order*) = urutan pencarian method: `EBook → DigitalMixin → Buku → Koleksi → ABC → object`. Bisa dicek dengan `EBook.__mro__` atau `EBook.mro()`.
  - Baris 94: arti `stok` untuk e-book = jumlah **lisensi** yang bisa dipinjam bersamaan (jadi `kurangi_stok()`/`tambah_stok()` tetap relevan).
  - Baris 92 kosong; baris 95 penutup docstring.
- **Baris 96** — Baris kosong.
- **Baris 97–98** — Constructor `__init__` (satu pernyataan yang dipecah dua baris karena panjang; baris 98 adalah lanjutan daftar parameter). Parameter: data buku (`kode, judul, tahun, penulis, penerbit`) + data digital dengan default `format_file="PDF"`, `ukuran_mb=1.0`, serta `stok=1`.
- **Baris 99** — `super().__init__(kode, judul, tahun, penulis, penerbit, stok)`. Python mencari `__init__` mengikuti MRO: `DigitalMixin` **tidak punya** `__init__`, jadi yang dipakai adalah `Buku.__init__`. `Buku.__init__` lalu memanggil `Koleksi.__init__` lewat `super()`. Argumen digital **tidak** dikirim ke atas karena `Buku` tidak mengenalnya.
- **Baris 100** — `self.format_file = format_file` → memanggil setter milik `DigitalMixin` (baris 60–65): validasi + ubah ke huruf besar.
- **Baris 101** — `self.ukuran_mb = ukuran_mb` → memanggil setter `ukuran_mb` (baris 71–81).
- **Baris 102** — Baris kosong.
- **Baris 103** — `def jenis(self):` **override** `Buku.jenis()`.
- **Baris 104** — Mengembalikan `"E-Book"`. Perhatikan: `EBook` **tidak** mendefinisikan `ringkasan()` sendiri; ia memakai `DigitalMixin.ringkasan()` yang ditemukan lebih dulu di MRO.

## Alur Saat Objek Dibuat

Contoh: `e = EBook("E001", "Belajar Python", 2023, "Tim", "Digital", "epub", 4.5)`

MRO `EBook`: `EBook → DigitalMixin → Buku → Koleksi → ABC → object`

1. Python membuat objek kosong lalu memanggil `EBook.__init__` (baris 97). Pemetaan argumen: `kode="E001"`, `judul="Belajar Python"`, `tahun=2023`, `penulis="Tim"`, `penerbit="Digital"`, `format_file="epub"`, `ukuran_mb=4.5`, `stok=1` (default).
2. **Baris 99** `super().__init__(...)`: cari `__init__` di class sesudah `EBook` dalam MRO → `DigitalMixin` tidak punya → ketemu **`Buku.__init__`**.
3. Di `Buku.__init__`, `super().__init__(kode, judul, tahun, stok)` → class sesudah `Buku` dalam MRO adalah **`Koleksi`** → `Koleksi.__init__` berjalan:
   - `_kode = "E001"` (divalidasi `teks_wajib`, di-`upper()`),
   - `judul` lewat setter → `"Belajar Python"`,
   - `tahun` lewat setter → `2023` (dicek antara 1450 dan tahun sekarang),
   - `stok` lewat setter → `1`.
4. Kembali ke `Buku.__init__`: `penulis = "Tim"` (setter, divalidasi), `penerbit = "Digital"`.
5. Kembali ke `EBook.__init__` **baris 100**: `self.format_file = "epub"` → setter `DigitalMixin` → `"EPUB"` (ada di `FORMAT_DIDUKUNG`, lolos).
6. **Baris 101**: `self.ukuran_mb = 4.5` → setter → bukan bool, `float(4.5) = 4.5`, > 0, lolos.
7. Objek siap. Jika ada satu validasi gagal (mis. format `"DOCX"`), `ValueError` dilempar dan objek **tidak** jadi dibuat.

**Bagaimana `e.ringkasan()` tersusun** (pencarian method mengikuti MRO):

1. `EBook` tidak punya `ringkasan` → ketemu **`DigitalMixin.ringkasan()`** (baris 86).
2. Di sana `super().ringkasan()` → class sesudah `DigitalMixin` → **`Buku.ringkasan()`**.
3. `Buku.ringkasan()` memanggil `super().ringkasan()` → **`Koleksi.ringkasan()`**, yang menghasilkan
   `E001 | E-Book    | Belajar Python (2023) | Stok: 1`
   (`self.jenis()` di sini memanggil `EBook.jenis()` → `"E-Book"`, polymorphism).
4. `Buku` menambahkan ` | Penulis: Tim | Penerbit: Digital`.
5. `DigitalMixin` menambahkan ` | Digital: EPUB, 4.5 MB`.

Hasil akhir:

```text
E001 | E-Book    | Belajar Python (2023) | Stok: 1 | Penulis: Tim | Penerbit: Digital | Digital: EPUB, 4.5 MB
```

Selain itu: `e.kena_denda()` → `False` (versi `DigitalMixin`), `e.bisa_dipinjam()` → `True` (versi `Koleksi`, karena stok 1).

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Apa beda single, multilevel, dan multiple inheritance di file ini?**
   Single: `Majalah(Koleksi)` – satu induk. Multilevel: `Referensi(Buku)` dengan `Buku(Koleksi)` – berjenjang. Multiple: `EBook(DigitalMixin, Buku)` – dua induk langsung.
2. **Apa itu mixin dan kenapa `DigitalMixin` tidak mewarisi `Koleksi`?**
   Mixin adalah class kecil penambah kemampuan yang tidak berdiri sendiri. Dibuat terpisah agar kemampuan "digital" bisa dicampurkan ke class lain (mis. kelak `MajalahDigital(DigitalMixin, Majalah)`) tanpa menduplikasi kode.
3. **Apa itu MRO dan bagaimana melihatnya?**
   Method Resolution Order = urutan Python mencari atribut/method. Untuk EBook: `EBook → DigitalMixin → Buku → Koleksi → ABC → object`. Dilihat dengan `EBook.__mro__` atau `EBook.mro()` (dihitung dengan algoritma C3 linearization).
4. **`DigitalMixin` tidak punya induk, kenapa boleh memanggil `super().ringkasan()`?**
   Karena `super()` tidak menunjuk "induk class penulisnya", tapi class **berikutnya di MRO objek** (`type(self)`). Untuk objek `EBook`, berikutnya adalah `Buku`, yang punya `ringkasan()`. Akibatnya `DigitalMixin` tidak boleh dipakai sendirian (`DigitalMixin().ringkasan()` akan error).
5. **Apa yang terjadi kalau urutan induk ditukar menjadi `EBook(Buku, DigitalMixin)`?**
   MRO menjadi `EBook → Buku → Koleksi → DigitalMixin → ...`. `Buku.ringkasan()` dan `Koleksi.kena_denda()` ditemukan lebih dulu, sehingga info digital hilang dari ringkasan dan e-book jadi kena denda.
6. **Kenapa `Referensi` cukup override `bisa_dipinjam()` alih-alih pengecekan di tempat lain?**
   Agar aturan "baca di tempat" melekat pada objeknya sendiri (polymorphism). `Peminjaman`/`Perpustakaan` cukup memanggil `bisa_dipinjam()` tanpa `if`/`isinstance`, sehingga mudah ditambah jenis koleksi baru (prinsip open/closed).
7. **Kenapa di `__init__` memakai `self.edisi = ...` dan bukan `self._edisi = ...`?**
   Supaya setter dipanggil dan validasi berjalan sejak objek dibuat; tidak ada objek dengan data tidak valid.
8. **Kenapa `Majalah` wajib punya `jenis()`?**
   Karena `jenis()` adalah `@abstractmethod` di `Koleksi`. Subclass yang belum mengimplementasikannya tetap dianggap abstrak dan tidak bisa diinstansiasi (`TypeError`).

## Ringkasan

- File ini mendemonstrasikan **tiga jenis inheritance**: single (`Majalah`), multilevel (`Referensi`), multiple (`EBook`).
- `super().__init__` dipakai agar validasi di `Koleksi`/`Buku` digunakan ulang, bukan ditulis ulang.
- **Override**: `jenis()`, `ringkasan()`, `bisa_dipinjam()` (Referensi → `False`), `kena_denda()` (DigitalMixin → `False`).
- **Property** (`edisi`, `format_file`, `ukuran_mb`) menjaga data tetap valid (enkapsulasi).
- `DigitalMixin` adalah **mixin**; `super()` di dalamnya **mengikuti MRO** objek pemakai.
- **MRO EBook**: `EBook → DigitalMixin → Buku → Koleksi → ABC → object`; urutan induk di definisi class menentukan method mana yang menang.
- `ringkasan()` EBook tersusun berlapis: Koleksi → + Buku → + DigitalMixin (cooperative inheritance).
- Bagian lain program memanggil method yang sama pada objek berbeda jenis → **polymorphism**.
