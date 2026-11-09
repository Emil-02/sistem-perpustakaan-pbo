# Penjelasan Baris per Baris: koleksi.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 1 |
| Jumlah baris | 122 baris |
| Konsep PBO | Class & Object, Enkapsulasi (atribut protected `_`), Property (getter/setter), Read-only property, Class attribute, Abstract class (`ABC`, `@abstractmethod`), Inheritance, `super()`, Override, Polymorphism |

## Gambaran Umum

File `koleksi.py` adalah fondasi seluruh program. Isinya tiga hal: (1) dua fungsi bantu validasi, `teks_wajib` dan `angka_bulat`, yang memastikan data teks tidak kosong dan data angka benar-benar bilangan bulat; (2) class abstrak `Koleksi`, induk dari semua jenis koleksi perpustakaan, yang menyimpan kode, judul, tahun, dan stok dengan validasi lewat property; dan (3) class `Buku`, turunan pertama `Koleksi`. File ini tidak mengimpor file lain di proyek (hanya modul bawaan `abc` dan `datetime`), justru **diimpor** oleh banyak file: `koleksi_turunan.py` mengimpor `Buku`, `Koleksi`, `teks_wajib` (untuk membuat `Majalah`, `Referensi`, `EBook`); `anggota.py` dan `anggota_turunan.py` mengimpor `teks_wajib`; `perpustakaan.py`, `main.py`, dan `test_perpustakaan.py` mengimpor `Buku` dan `Koleksi`. Method `bisa_dipinjam`, `kurangi_stok`, `tambah_stok` dipanggil oleh `perpustakaan.py` saat meminjam/mengembalikan, dan `kena_denda` dipanggil oleh `peminjaman.py` saat menghitung denda.

## Baris 1–8: Docstring Modul

```python
  1 | """BAGIAN 1 - Class & Object, Enkapsulasi, Abstraction.
  2 | 
  3 | Isi file ini:
  4 | - fungsi bantu validasi teks dan angka (dipakai juga oleh file lain)
  5 | - Koleksi : abstract class (induk semua jenis koleksi)
  6 | - Buku    : turunan Koleksi
  7 | """
  8 | 
```

- **Baris 1** — Membuka *docstring modul* dengan tiga tanda kutip `"""`. Docstring adalah string pertama di file yang menjadi dokumentasi resmi modul (bisa dibaca dengan `help(koleksi)` atau `koleksi.__doc__`). Kalimat pertama menyebut topik presentasi bagian 1: Class & Object, Enkapsulasi, Abstraction.
- **Baris 2** — Baris kosong di dalam docstring: pemisah antara judul dan isi (konvensi PEP 257).
- **Baris 3** — Pengantar daftar isi file.
- **Baris 4** — Poin pertama: ada fungsi bantu validasi yang juga dipakai file lain (misalnya `anggota.py`).
- **Baris 5** — Poin kedua: `Koleksi` adalah *abstract class*, induk semua jenis koleksi.
- **Baris 6** — Poin ketiga: `Buku` adalah turunan (*subclass*) dari `Koleksi`.
- **Baris 7** — Menutup docstring dengan `"""`.
- **Baris 8** — Baris kosong: pemisah antara docstring dan bagian import.

## Baris 9–12: Import

```python
  9 | from abc import ABC, abstractmethod
 10 | from datetime import date
 11 | 
 12 | 
```

- **Baris 9** — Mengimpor `ABC` (Abstract Base Class) dan dekorator `abstractmethod` dari modul bawaan `abc`. Keduanya dibutuhkan untuk membuat class abstrak `Koleksi`: class yang mewarisi `ABC` dan punya `@abstractmethod` tidak bisa dibuat objeknya secara langsung.
- **Baris 10** — Mengimpor class `date` dari modul `datetime`. Dipakai di setter `tahun` untuk mengetahui tahun sekarang (`date.today().year`), sehingga batas atas tahun selalu mengikuti tanggal komputer, bukan angka yang ditulis mati (*hard-coded*).
- **Baris 11–12** — Dua baris kosong: aturan PEP 8, fungsi/class di level atas dipisah dua baris kosong.

## Baris 13–19: Fungsi Bantu `teks_wajib`

```python
 13 | def teks_wajib(nilai, nama_field):
 14 |     """Teks tidak boleh kosong. Mengembalikan teks tanpa spasi di awal/akhir."""
 15 |     if not isinstance(nilai, str) or not nilai.strip():
 16 |         raise ValueError(f"{nama_field} tidak boleh kosong")
 17 |     return nilai.strip()
 18 | 
 19 | 
```

- **Baris 13** — Mendefinisikan fungsi biasa (bukan method, karena di luar class) bernama `teks_wajib` dengan dua parameter: `nilai` (data yang dicek) dan `nama_field` (nama data, dipakai di pesan error). Dibuat sebagai fungsi terpisah agar validasi yang sama bisa dipakai ulang di banyak tempat (prinsip DRY – *Don't Repeat Yourself*): judul, kode, penulis, nama anggota, prodi, dll.
- **Baris 14** — Docstring fungsi: menjelaskan aturan (tidak boleh kosong) dan hasilnya (teks yang sudah dibersihkan spasinya).
- **Baris 15** — Kondisi gagal: `isinstance(nilai, str)` mengecek apakah `nilai` bertipe string; `nilai.strip()` menghapus spasi di awal/akhir, dan string kosong dianggap `False`. Jadi kondisi bernilai benar jika nilai **bukan string** atau **hanya berisi spasi/kosong**. Urutan `or` penting: kalau `nilai` bukan string (misal `None`), Python berhenti di bagian pertama sehingga `.strip()` tidak dipanggil pada `None` (*short-circuit*).
- **Baris 16** — Jika kondisi gagal, lempar `ValueError` dengan pesan memakai f-string. Contoh: `teks_wajib("   ", "Judul")` → `ValueError: Judul tidak boleh kosong`.
- **Baris 17** — Jika lolos, kembalikan teks yang sudah di-`strip()`. Contoh: `teks_wajib("  abc ", "Judul")` → `"abc"`.
- **Baris 18–19** — Dua baris kosong pemisah (PEP 8).

## Baris 20–29: Fungsi Bantu `angka_bulat`

```python
 20 | def angka_bulat(nilai, nama_field):
 21 |     """Ubah ke int. True/False ditolak walaupun bool adalah turunan int."""
 22 |     if isinstance(nilai, bool):
 23 |         raise ValueError(f"{nama_field} harus berupa angka")
 24 |     try:
 25 |         return int(nilai)
 26 |     except (TypeError, ValueError):
 27 |         raise ValueError(f"{nama_field} harus berupa angka") from None
 28 | 
 29 | 
```

- **Baris 20** — Mendefinisikan fungsi `angka_bulat` untuk mengubah input menjadi bilangan bulat (`int`) sekaligus memvalidasinya. Dipakai oleh setter `tahun` dan `stok`.
- **Baris 21** — Docstring: fungsi mengubah ke `int`, dan menolak `True/False`. Alasannya: di Python, `bool` adalah *subclass* dari `int` (`True == 1`, `False == 0`), sehingga tanpa pengecekan khusus `stok=True` akan lolos sebagai angka 1 — ini contoh nyata inheritance di Python sendiri.
- **Baris 22** — Mengecek apakah `nilai` bertipe `bool`.
- **Baris 23** — Jika ya, tolak dengan `ValueError`. Contoh: `angka_bulat(True, "Stok")` → `ValueError: Stok harus berupa angka`.
- **Baris 24** — Membuka blok `try` untuk menangkap error saat konversi.
- **Baris 25** — Mencoba `int(nilai)` dan langsung mengembalikan hasilnya. Contoh: `angka_bulat("2020", "Tahun")` → `2020`; `angka_bulat(5, "Stok")` → `5`. Ini berguna karena input dari menu console (`input()`) selalu berupa string.
- **Baris 26** — Menangkap dua jenis error: `TypeError` (misal `int(None)`) dan `ValueError` (misal `int("abc")`).
- **Baris 27** — Melempar ulang sebagai `ValueError` dengan pesan yang ramah. `from None` menyembunyikan error asli dari traceback sehingga pesan yang terlihat hanya satu dan jelas. Contoh: `angka_bulat("abc", "Tahun")` → `ValueError: Tahun harus berupa angka`. Hasilnya, kode pemanggil cukup menangkap `ValueError` saja.
- **Baris 28–29** — Dua baris kosong pemisah (PEP 8).

## Baris 30–34: Deklarasi Class Abstrak `Koleksi` dan Class Attribute

```python
 30 | class Koleksi(ABC):
 31 |     """Abstract class: objeknya tidak bisa dibuat langsung, harus lewat subclass."""
 32 | 
 33 |     TAHUN_MINIMAL = 1450  # class attribute: berlaku untuk semua koleksi
 34 | 
```

- **Baris 30** — Mendefinisikan class `Koleksi` yang mewarisi `ABC`. Pewarisan dari `ABC` menjadikan `Koleksi` *abstract class*: cetak biru umum yang tidak boleh dibuat objeknya langsung. `Koleksi("K1", "X", 2020)` akan menghasilkan `TypeError` karena masih ada method abstrak (`jenis`). Konsep: **Abstraction**.
- **Baris 31** — Docstring class yang menegaskan sifat abstraknya.
- **Baris 32** — Baris kosong pemisah.
- **Baris 33** — `TAHUN_MINIMAL = 1450` adalah **class attribute**: ditulis di badan class (bukan di `self`), sehingga dimiliki class dan dibagi oleh semua objek serta subclass. Angka 1450 dipilih karena sekitar tahun itulah mesin cetak Gutenberg ditemukan, jadi koleksi tercetak tidak mungkin lebih tua. Ditulis huruf besar sebagai konvensi konstanta.
- **Baris 34** — Baris kosong pemisah.

## Baris 35–41: Constructor `__init__` Koleksi

```python
 35 |     def __init__(self, kode, judul, tahun, stok=1):
 36 |         self._kode = teks_wajib(kode, "Kode").upper()  # protected + read-only
 37 |         # Diisi lewat setter agar validasi juga berlaku saat objek dibuat
 38 |         self.judul = judul
 39 |         self.tahun = tahun
 40 |         self.stok = stok
 41 | 
```

- **Baris 35** — Constructor `__init__`, dipanggil otomatis saat objek dibuat. `self` adalah objek yang sedang dibuat. `stok=1` adalah *default parameter*: jika tidak diisi, stok bernilai 1.
- **Baris 36** — Memvalidasi kode lewat `teks_wajib`, lalu `.upper()` agar seragam huruf besar (`" b001 "` → `"B001"`), kemudian disimpan di `self._kode`. Awalan garis bawah `_` menandakan atribut **protected** (konvensi Python: "jangan diakses langsung dari luar class"). Kode langsung disimpan ke `_kode` (bukan lewat setter) karena `kode` sengaja dibuat **read-only** (lihat baris 43–46).
- **Baris 37** — Komentar yang menjelaskan alasan tiga baris berikutnya memakai `self.judul = ...` dan bukan `self._judul = ...`.
- **Baris 38** — `self.judul = judul` tampak seperti assignment biasa, tetapi karena `judul` adalah property, Python sebenarnya memanggil **setter** `judul` (baris 52–54) sehingga validasi berjalan juga saat objek pertama kali dibuat.
- **Baris 39** — Sama: memanggil setter `tahun` (baris 60–66) yang memvalidasi rentang tahun.
- **Baris 40** — Sama: memanggil setter `stok` (baris 72–77) yang menolak stok negatif.
- **Baris 41** — Baris kosong pemisah.

## Baris 42–47: Property `kode` (Read-only)

```python
 42 |     # ---------- getter & setter (property) ----------
 43 |     @property
 44 |     def kode(self):
 45 |         """Read-only (tidak ada setter) karena kode adalah identitas koleksi."""
 46 |         return self._kode
 47 | 
```

- **Baris 42** — Komentar penanda bagian: di bawah ini kumpulan getter & setter berbentuk property.
- **Baris 43** — Dekorator `@property` mengubah method di bawahnya menjadi **getter**: bisa diakses seperti atribut (`buku.kode`, tanpa tanda kurung).
- **Baris 44** — Method getter `kode`.
- **Baris 45** — Docstring: tidak ada setter, jadi `kode` hanya bisa dibaca. Kode adalah identitas unik koleksi (dipakai sebagai kunci pencarian di `Perpustakaan`), sehingga tidak boleh diubah setelah dibuat. Mencoba `buku.kode = "X"` → `AttributeError`.
- **Baris 46** — Mengembalikan nilai atribut protected `_kode`. Inilah **enkapsulasi**: data disimpan tersembunyi, akses dari luar lewat "pintu" yang dikontrol.
- **Baris 47** — Baris kosong pemisah.

## Baris 48–55: Property `judul` (Getter & Setter)

```python
 48 |     @property
 49 |     def judul(self):
 50 |         return self._judul
 51 | 
 52 |     @judul.setter
 53 |     def judul(self, nilai):
 54 |         self._judul = teks_wajib(nilai, "Judul")
 55 | 
```

- **Baris 48** — `@property`: menjadikan `judul` sebuah getter.
- **Baris 49** — Method getter `judul`.
- **Baris 50** — Mengembalikan atribut protected `_judul`.
- **Baris 51** — Baris kosong pemisah.
- **Baris 52** — `@judul.setter` mendaftarkan method di bawahnya sebagai **setter** untuk property `judul`. Nama method harus sama (`judul`).
- **Baris 53** — Method setter, menerima `nilai` baru. Dipanggil otomatis saat `objek.judul = ...`.
- **Baris 54** — Validasi dengan `teks_wajib` lalu simpan ke `_judul`. Contoh: `buku.judul = "  Laskar Pelangi "` → tersimpan `"Laskar Pelangi"`; `buku.judul = ""` → `ValueError: Judul tidak boleh kosong`, dan judul lama tetap utuh.
- **Baris 55** — Baris kosong pemisah.

## Baris 56–67: Property `tahun` (dengan Validasi Rentang)

```python
 56 |     @property
 57 |     def tahun(self):
 58 |         return self._tahun
 59 | 
 60 |     @tahun.setter
 61 |     def tahun(self, nilai):
 62 |         nilai = angka_bulat(nilai, "Tahun")
 63 |         tahun_ini = date.today().year
 64 |         if not self.TAHUN_MINIMAL <= nilai <= tahun_ini:
 65 |             raise ValueError(f"Tahun harus antara {self.TAHUN_MINIMAL} dan {tahun_ini}")
 66 |         self._tahun = nilai
 67 | 
```

- **Baris 56** — `@property`: getter `tahun`.
- **Baris 57** — Method getter `tahun`.
- **Baris 58** — Mengembalikan `_tahun`.
- **Baris 59** — Baris kosong pemisah.
- **Baris 60** — `@tahun.setter`: mendaftarkan setter `tahun`.
- **Baris 61** — Method setter `tahun`.
- **Baris 62** — Mengubah input menjadi `int` lewat `angka_bulat` (menolak teks non-angka dan `bool`). Contoh: `"2008"` → `2008`.
- **Baris 63** — Mengambil tahun saat ini dari tanggal sistem, misalnya `2026`.
- **Baris 64** — Mengecek rentang dengan *chained comparison* khas Python: `1450 <= nilai <= tahun_ini`. `self.TAHUN_MINIMAL` membaca class attribute melalui objek (Python mencari di objek dulu, lalu di class). Jika di luar rentang, kondisi `not ...` bernilai benar.
- **Baris 65** — Melempar `ValueError` dengan pesan rentang. Contoh: `tahun=3000` → `ValueError: Tahun harus antara 1450 dan 2026`.
- **Baris 66** — Jika valid, simpan ke `_tahun`.
- **Baris 67** — Baris kosong pemisah.

## Baris 68–78: Property `stok` (Tidak Boleh Negatif)

```python
 68 |     @property
 69 |     def stok(self):
 70 |         return self._stok
 71 | 
 72 |     @stok.setter
 73 |     def stok(self, nilai):
 74 |         nilai = angka_bulat(nilai, "Stok")
 75 |         if nilai < 0:
 76 |             raise ValueError("Stok tidak boleh negatif")
 77 |         self._stok = nilai
 78 | 
```

- **Baris 68** — `@property`: getter `stok`.
- **Baris 69** — Method getter `stok`.
- **Baris 70** — Mengembalikan `_stok`.
- **Baris 71** — Baris kosong pemisah.
- **Baris 72** — `@stok.setter`: mendaftarkan setter `stok`.
- **Baris 73** — Method setter `stok`.
- **Baris 74** — Konversi ke `int` lewat `angka_bulat`. Contoh: `"3"` → `3`; `"tiga"` → `ValueError: Stok harus berupa angka`.
- **Baris 75** — Mengecek apakah stok negatif. Stok 0 tetap boleh (artinya sedang habis).
- **Baris 76** — Jika negatif, lempar `ValueError("Stok tidak boleh negatif")`. Contoh: `buku.stok = -1` → error.
- **Baris 77** — Jika valid, simpan ke `_stok`.
- **Baris 78** — Baris kosong pemisah.

## Baris 79–83: Method Abstrak `jenis`

```python
 79 |     # ---------- method (perilaku objek) ----------
 80 |     @abstractmethod
 81 |     def jenis(self):
 82 |         """Wajib diimplementasikan oleh setiap subclass."""
 83 | 
```

- **Baris 79** — Komentar penanda bagian: method yang menggambarkan perilaku objek.
- **Baris 80** — Dekorator `@abstractmethod` menandai `jenis` sebagai method abstrak: hanya "kontrak", tanpa isi. Setiap subclass **wajib** meng-override-nya; jika tidak, subclass itu ikut menjadi abstrak dan tidak bisa dibuat objeknya.
- **Baris 81** — Deklarasi method `jenis`. Tujuannya mengembalikan nama jenis koleksi (`"Buku"`, `"Majalah"`, `"Referensi"`, `"E-Book"`, dll.).
- **Baris 82** — Badan method hanya berisi docstring. Secara sintaks docstring sudah cukup sebagai isi fungsi, sehingga tidak perlu `pass`.
- **Baris 83** — Baris kosong pemisah.

## Baris 84–90: Method `bisa_dipinjam` dan `kena_denda`

```python
 84 |     def bisa_dipinjam(self):
 85 |         return self._stok > 0
 86 | 
 87 |     def kena_denda(self):
 88 |         """Apakah keterlambatan koleksi ini dikenai denda."""
 89 |         return True
 90 | 
```

- **Baris 84** — Method `bisa_dipinjam`: menjawab apakah koleksi boleh dipinjam. Dipanggil oleh `Perpustakaan` sebelum membuat transaksi.
- **Baris 85** — Aturan default: boleh dipinjam jika stok lebih dari 0. Contoh: stok 2 → `True`, stok 0 → `False`. Method ini di-**override** oleh `Referensi` di `koleksi_turunan.py` (koleksi referensi tidak boleh dibawa pulang) — contoh **polymorphism**: pemanggilan sama, perilaku berbeda.
- **Baris 86** — Baris kosong pemisah.
- **Baris 87** — Method `kena_denda`: apakah keterlambatan koleksi ini dikenai denda. Dipakai oleh `Peminjaman` di `peminjaman.py`.
- **Baris 88** — Docstring penjelasan.
- **Baris 89** — Default `True`: koleksi fisik dikenai denda bila terlambat. Di-override oleh `DigitalMixin`/`EBook` agar mengembalikan `False` (koleksi digital tanpa denda).
- **Baris 90** — Baris kosong pemisah.

## Baris 91–98: Method `kurangi_stok` dan `tambah_stok`

```python
 91 |     def kurangi_stok(self):
 92 |         if self._stok <= 0:
 93 |             raise ValueError(f"Stok '{self.judul}' habis")
 94 |         self._stok -= 1
 95 | 
 96 |     def tambah_stok(self):
 97 |         self._stok += 1
 98 | 
```

- **Baris 91** — Method `kurangi_stok`, dipanggil saat koleksi dipinjam.
- **Baris 92** — Pengaman: jika stok sudah 0 (atau kurang), tidak boleh dikurangi lagi.
- **Baris 93** — Lempar `ValueError` berisi judul koleksi. Contoh: `"Stok 'Laskar Pelangi' habis"`.
- **Baris 94** — Kurangi stok 1. Di sini langsung memakai `_stok` (bukan setter) karena kita berada **di dalam** class dan kondisinya sudah dicek di baris 92, jadi hasilnya pasti tidak negatif.
- **Baris 95** — Baris kosong pemisah.
- **Baris 96** — Method `tambah_stok`, dipanggil saat koleksi dikembalikan.
- **Baris 97** — Tambah stok 1. Perubahan stok dari luar dilakukan lewat method ini (bukan mengubah `_stok` langsung) — inilah inti enkapsulasi: objek mengatur datanya sendiri.
- **Baris 98** — Baris kosong pemisah.

## Baris 99–102: Method `ringkasan`

```python
 99 |     def ringkasan(self):
100 |         return f"{self.kode} | {self.jenis():<9} | {self.judul} ({self.tahun}) | Stok: {self.stok}"
101 | 
102 | 
```

- **Baris 99** — Method `ringkasan`: menghasilkan satu baris teks berisi info koleksi, dipakai saat menampilkan daftar koleksi di menu.
- **Baris 100** — f-string yang menggabungkan kode, jenis, judul, tahun, dan stok. `{self.jenis():<9}` memanggil method `jenis()` lalu meratakannya ke kiri dengan lebar 9 karakter agar kolom tabel rapi. Perhatikan: `Koleksi` memanggil `self.jenis()` padahal `jenis` abstrak — yang terpanggil adalah versi milik subclass objek tersebut (**polymorphism**). Contoh hasil: `B001 | Buku      | Laskar Pelangi (2005) | Stok: 3`.
- **Baris 101–102** — Dua baris kosong pemisah antar class (PEP 8).

## Baris 103–108: Class `Buku` dan Constructor-nya

```python
103 | class Buku(Koleksi):
104 |     def __init__(self, kode, judul, tahun, penulis, penerbit, stok=1):
105 |         super().__init__(kode, judul, tahun, stok)  # jalankan __init__ milik Koleksi
106 |         self.penulis = penulis
107 |         self.penerbit = penerbit  # public
108 | 
```

- **Baris 103** — Mendefinisikan class `Buku` yang mewarisi `Koleksi` (**inheritance**). `Buku` otomatis memiliki semua atribut dan method `Koleksi` (kode, judul, tahun, stok, `bisa_dipinjam`, `kurangi_stok`, dst.).
- **Baris 104** — Constructor `Buku` menerima parameter milik `Koleksi` ditambah dua parameter khusus buku: `penulis` dan `penerbit`. `stok=1` tetap default dan diletakkan di akhir karena parameter ber-default harus setelah parameter tanpa default.
- **Baris 105** — `super().__init__(...)` memanggil constructor induk (`Koleksi`) agar kode, judul, tahun, dan stok divalidasi dan disimpan oleh induknya. Jadi `Buku` tidak perlu menulis ulang logika tersebut (*reuse*). `super()` juga penting untuk pewarisan berlapis (lihat `EBook` di `koleksi_turunan.py`).
- **Baris 106** — `self.penulis = penulis` memanggil setter `penulis` (baris 113–115), sehingga penulis divalidasi tidak kosong.
- **Baris 107** — `self.penerbit` disimpan sebagai atribut **public** biasa (tanpa `_` dan tanpa property) karena tidak membutuhkan validasi. Ini menunjukkan perbandingan: tidak semua atribut harus diberi property — gunakan bila memang perlu kontrol.
- **Baris 108** — Baris kosong pemisah.

## Baris 109–116: Property `penulis`

```python
109 |     @property
110 |     def penulis(self):
111 |         return self._penulis
112 | 
113 |     @penulis.setter
114 |     def penulis(self, nilai):
115 |         self._penulis = teks_wajib(nilai, "Penulis")
116 | 
```

- **Baris 109** — `@property`: getter `penulis`, atribut tambahan yang hanya dimiliki `Buku`.
- **Baris 110** — Method getter `penulis`.
- **Baris 111** — Mengembalikan atribut protected `_penulis`.
- **Baris 112** — Baris kosong pemisah.
- **Baris 113** — `@penulis.setter`: mendaftarkan setter `penulis`.
- **Baris 114** — Method setter `penulis`.
- **Baris 115** — Validasi dengan `teks_wajib`. Contoh: `Buku("B9", "Judul", 2020, "", "Gramedia")` → `ValueError: Penulis tidak boleh kosong`.
- **Baris 116** — Baris kosong pemisah.

## Baris 117–122: Implementasi `jenis` dan Override `ringkasan`

```python
117 |     def jenis(self):
118 |         return "Buku"
119 | 
120 |     def ringkasan(self):
121 |         # Override: hasil ringkasan Koleksi ditambah info khusus buku
122 |         return f"{super().ringkasan()} | Penulis: {self.penulis} | Penerbit: {self.penerbit}"
```

- **Baris 117** — Mengimplementasikan method abstrak `jenis` dari `Koleksi`. Karena semua method abstrak sudah diisi, `Buku` menjadi **concrete class** dan objeknya bisa dibuat.
- **Baris 118** — Mengembalikan teks `"Buku"`.
- **Baris 119** — Baris kosong pemisah.
- **Baris 120** — **Override** method `ringkasan` milik `Koleksi`: nama dan parameter sama, isi berbeda.
- **Baris 121** — Komentar: ringkasan induk dipakai lalu ditambah info khusus buku.
- **Baris 122** — `super().ringkasan()` memanggil versi induk (baris 99–100), lalu hasilnya diperluas dengan penulis dan penerbit. Teknik ini disebut *extending* (memperluas, bukan mengganti total), sehingga format dasar tidak ditulis dua kali. Contoh hasil: `B001 | Buku      | Laskar Pelangi (2005) | Stok: 3 | Penulis: Andrea Hirata | Penerbit: Bentang`. Ini baris terakhir file (baris 122).

## Alur Saat Objek Dibuat

Contoh pemanggilan:

```python
b = Buku(" b001 ", "Laskar Pelangi", "2005", "Andrea Hirata", "Bentang", stok=3)
```

1. Python membuat objek `Buku` kosong, lalu memanggil `Buku.__init__` (baris 104) dengan `kode=" b001 "`, `judul="Laskar Pelangi"`, `tahun="2005"`, `penulis="Andrea Hirata"`, `penerbit="Bentang"`, `stok=3`.
2. Baris 105: `super().__init__(...)` menjalankan `Koleksi.__init__` (baris 35).
3. Baris 36: `teks_wajib(" b001 ", "Kode")` → `"b001"`, lalu `.upper()` → `"B001"`, disimpan di `b._kode`.
4. Baris 38: `self.judul = ...` → setter `judul` (baris 54) → `teks_wajib` lolos → `b._judul = "Laskar Pelangi"`.
5. Baris 39: `self.tahun = "2005"` → setter `tahun` (baris 62–66) → `angka_bulat("2005")` = `2005` → dicek `1450 <= 2005 <= 2026` → `b._tahun = 2005`.
6. Baris 40: `self.stok = 3` → setter `stok` (baris 74–77) → `3` tidak negatif → `b._stok = 3`.
7. Kembali ke `Buku.__init__`, baris 106: setter `penulis` → `b._penulis = "Andrea Hirata"`.
8. Baris 107: `b.penerbit = "Bentang"` (atribut public biasa).
9. Objek selesai dibuat. Memanggil `b.ringkasan()` → `Buku.ringkasan` (baris 122) → `super().ringkasan()` (baris 100) yang memanggil `self.jenis()` → `"Buku"` → hasil akhir: `B001 | Buku      | Laskar Pelangi (2005) | Stok: 3 | Penulis: Andrea Hirata | Penerbit: Bentang`.

Jika salah satu validasi gagal (misal `tahun="abc"`), `ValueError` dilempar di langkah tersebut dan objek **tidak** jadi dibuat.

Contoh lain: `Koleksi("K1", "X", 2020)` langsung gagal dengan `TypeError: Can't instantiate abstract class Koleksi ...` karena `Koleksi` abstrak.

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Mengapa `Koleksi` dibuat abstract?**
   Karena "koleksi" adalah konsep umum; yang nyata adalah buku, majalah, referensi, e-book. Dengan `ABC` + `@abstractmethod jenis`, objek `Koleksi` langsung tidak bisa dibuat dan setiap subclass dipaksa menyediakan `jenis()`.

2. **Apa beda `_kode` dan `kode`?**
   `_kode` adalah atribut penyimpan (protected, konvensi "jangan diakses dari luar"). `kode` adalah property getter yang menjadi pintu baca resmi. Karena tidak ada setter, `kode` read-only.

3. **Mengapa di `__init__` memakai `self.judul = judul`, bukan `self._judul = judul`?**
   Agar setter terpanggil sehingga validasi berlaku juga saat objek dibuat, bukan hanya saat diubah belakangan. Aturan validasi cukup ditulis sekali di setter.

4. **Apa fungsi `super().__init__` di `Buku`?**
   Memanggil constructor induk agar atribut umum (kode, judul, tahun, stok) diisi dan divalidasi oleh `Koleksi`, sehingga kode tidak diduplikasi.

5. **Apa itu `TAHUN_MINIMAL` dan apa bedanya dengan atribut objek?**
   Class attribute: satu nilai milik class, dibagi semua objek dan subclass. Atribut objek (`self._judul`) berbeda di tiap objek.

6. **Mengapa `bool` ditolak di `angka_bulat`?**
   Karena `bool` adalah subclass `int` sehingga `int(True)` = 1. Tanpa pengecekan, `stok=True` dianggap valid, padahal itu jelas salah input.

7. **Di mana polymorphism di file ini?**
   `Koleksi.ringkasan()` memanggil `self.jenis()`; hasilnya tergantung class objek (`"Buku"`, `"Majalah"`, ...). Juga `bisa_dipinjam` dan `kena_denda` yang di-override oleh subclass di `koleksi_turunan.py`, sementara `Perpustakaan` cukup memanggil method yang sama tanpa peduli jenisnya.

8. **Mengapa `penerbit` tidak dibuat property?**
   Karena tidak ada aturan validasi untuknya. Property dipakai saat perlu kontrol (validasi/read-only); atribut public biasa cukup untuk data bebas.

## Ringkasan

- `teks_wajib` dan `angka_bulat` adalah fungsi validasi yang dipakai ulang di banyak file (DRY).
- `Koleksi` adalah abstract class (`ABC` + `@abstractmethod jenis`) yang tidak bisa dibuat objeknya langsung.
- Enkapsulasi: data disimpan di atribut protected (`_kode`, `_judul`, `_tahun`, `_stok`) dan diakses lewat property.
- `kode` read-only (tanpa setter); `judul`, `tahun`, `stok` punya setter dengan validasi.
- Constructor memakai setter agar validasi juga berlaku saat objek dibuat.
- `TAHUN_MINIMAL` adalah class attribute bersama.
- Method perilaku: `bisa_dipinjam`, `kena_denda`, `kurangi_stok`, `tambah_stok`, `ringkasan` — sebagian di-override subclass (polymorphism).
- `Buku` mewarisi `Koleksi`, memakai `super().__init__`, menambah atribut `penulis` (property) dan `penerbit` (public), mengimplementasikan `jenis`, dan meng-override `ringkasan` dengan memperluas versi induk via `super().ringkasan()`.
