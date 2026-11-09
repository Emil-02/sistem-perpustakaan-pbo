# Penjelasan Baris per Baris: anggota.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 3 |
| File | `anggota.py` |
| Jumlah baris | 91 |
| Konsep PBO | Enkapsulasi (public, protected, private), name mangling, property & setter, property read-only, class attribute, abstract class & abstract method, validasi data (regex email), method kooperatif dengan `super()` |

## Gambaran Umum

File `anggota.py` berisi dua hal: fungsi bantu `rupiah()` untuk mengubah angka menjadi teks Rupiah, dan class abstrak `Anggota` yang menjadi induk semua jenis anggota perpustakaan. Fokus utama file ini adalah **enkapsulasi** (bagaimana data anggota dilindungi lewat atribut public, protected, private, serta property) dan **abstraction** (class `Anggota` tidak bisa dibuat objeknya langsung karena punya method abstrak `jenis()`). File ini memakai `teks_wajib()` dari `koleksi.py` (Bagian 1). Selanjutnya `anggota_turunan.py` (Bagian 4) membuat subclass `Mahasiswa`, `Dosen`, `Umum`, dan `AsistenDosen` yang mengisi `jenis()` dan mengubah aturan pinjam. `rupiah()` juga dipakai oleh `peminjaman.py`, `perpustakaan.py`, `main.py`, dan diuji di `test_perpustakaan.py`. Sementara itu, `peminjaman.py` membaca `DENDA_PER_HARI` milik anggota untuk menghitung denda keterlambatan.

## Baris 1–7: Docstring Modul

```python
 1 | """BAGIAN 3 - Enkapsulasi pada Anggota (public, protected, private) + Abstraction.
 2 |
 3 | Isi file ini:
 4 | - rupiah()  : format angka ke Rupiah (dipakai juga oleh file lain)
 5 | - Anggota   : abstract class, induk semua jenis anggota
 6 | """
 7 |
```

- **Baris 1–6** — *Docstring modul*, yaitu string tiga tanda kutip di awal file. Tidak dieksekusi sebagai logika, tetapi menjadi dokumentasi file (bisa dibaca lewat `help(anggota)` atau `anggota.__doc__`). Baris 1 menyebut topik bagian ini: enkapsulasi (public, protected, private) dan abstraction. Baris 2 kosong sebagai jeda. Baris 3–5 mendaftar isi file: fungsi `rupiah()` (dipakai juga oleh file lain) dan class abstrak `Anggota`. Baris 6 menutup docstring.
- **Baris 7** — Baris kosong sebagai pemisah antara docstring dan bagian import (gaya penulisan PEP 8).

## Baris 8–13: Import

```python
 8 | import re
 9 | from abc import ABC, abstractmethod
10 |
11 | from koleksi import teks_wajib
12 |
13 |
```

- **Baris 8** — `import re` mengimpor modul *regular expression* bawaan Python. Dipakai untuk mengecek format email (lihat baris 25).
- **Baris 9** — Mengimpor `ABC` (*Abstract Base Class*) dan dekorator `abstractmethod` dari modul `abc`. Keduanya dibutuhkan agar `Anggota` menjadi **class abstrak**: class yang tidak boleh dibuat objeknya langsung, hanya boleh diturunkan.
- **Baris 10** — Baris kosong; memisahkan import pustaka standar dan import dari file proyek sendiri.
- **Baris 11** — Mengimpor fungsi `teks_wajib` dari `koleksi.py`. Fungsi ini memastikan nilai berupa string yang tidak kosong, lalu mengembalikannya tanpa spasi di awal/akhir (`.strip()`); jika tidak valid ia melempar `ValueError("... tidak boleh kosong")`. Memakai ulang fungsi ini lebih baik daripada menulis validasi yang sama dua kali (prinsip DRY: *Don't Repeat Yourself*).
- **Baris 12–13** — Dua baris kosong sebelum definisi fungsi tingkat atas (aturan PEP 8).

## Baris 14–18: Fungsi `rupiah()`

```python
14 | def rupiah(jumlah):
15 |     """Contoh: 32000 -> 'Rp32.000'."""
16 |     return "Rp" + f"{jumlah:,}".replace(",", ".")
17 |
18 |
```

- **Baris 14** — Mendefinisikan fungsi biasa (bukan method) bernama `rupiah` dengan satu parameter `jumlah`. Diletakkan di luar class karena tidak bergantung pada objek mana pun, sehingga bisa dipakai di banyak file.
- **Baris 15** — Docstring fungsi sekaligus contoh: `32000` menjadi `'Rp32.000'`.
- **Baris 16** — Inti fungsi, bekerja dalam dua langkah:
  1. `f"{jumlah:,}"` — format spesifier `,` membuat Python menyisipkan pemisah ribuan gaya Inggris. Contoh: `32000` → `"32,000"`, `1500000` → `"1,500,000"`.
  2. `.replace(",", ".")` — mengganti semua koma menjadi titik agar sesuai gaya Indonesia: `"32,000"` → `"32.000"`.

  Lalu `"Rp" + ...` menempelkan awalan. Hasil: `rupiah(32000)` → `"Rp32.000"`, `rupiah(1500000)` → `"Rp1.500.000"`, `rupiah(0)` → `"Rp0"`.
- **Baris 17–18** — Dua baris kosong sebelum definisi class.

## Baris 19–26: Deklarasi Class dan Class Attribute

```python
19 | class Anggota(ABC):
20 |     """Aturan pinjam disimpan sebagai class attribute, nilainya diubah oleh subclass."""
21 |
22 |     MAKS_PINJAM = 2
23 |     LAMA_PINJAM = 7  # hari
24 |     DENDA_PER_HARI = 1000  # rupiah
25 |     _POLA_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
26 |
```

- **Baris 19** — `class Anggota(ABC):` mendefinisikan class `Anggota` yang mewarisi `ABC`. Pewarisan dari `ABC` membuat Python memeriksa method abstrak: selama masih ada method `@abstractmethod` yang belum diisi, `Anggota(...)` akan gagal dengan `TypeError: Can't instantiate abstract class ...`.
- **Baris 20** — Docstring class: aturan pinjam disimpan sebagai **class attribute** dan nilainya diubah (di-*override*) oleh subclass.
- **Baris 21** — Baris kosong pemisah.
- **Baris 22** — `MAKS_PINJAM = 2` adalah *class attribute* (milik class, dibagi semua objek), bukan atribut objek. Artinya batas default maksimal 2 buku. Penulisan huruf kapital adalah konvensi untuk nilai konstanta.
- **Baris 23** — `LAMA_PINJAM = 7`: lama pinjam default 7 hari.
- **Baris 24** — `DENDA_PER_HARI = 1000`: denda default Rp1.000 per hari terlambat. Nilai ini dibaca `peminjaman.py` (`hari_terlambat * self._anggota.DENDA_PER_HARI`). Subclass menimpanya, misalnya `Umum` memakai 2000 dan `Dosen` memakai 500. Karena dibaca lewat `self.DENDA_PER_HARI`, Python mencari dulu di class objeknya (subclass), baru ke induk. Inilah **polimorfisme lewat class attribute**.
- **Baris 25** — `_POLA_EMAIL` adalah class attribute **protected** (awalan `_`) yang berisi pola regex yang sudah dikompilasi dengan `re.compile` (dikompilasi sekali saat class dibuat, lalu dipakai ulang oleh semua objek). Huruf `r` di depan string berarti *raw string*, jadi `\s` dan `\.` tidak diproses sebagai escape Python. Arti pola `^[^@\s]+@[^@\s]+\.[^@\s]+$` per bagian:
  - `^` — awal teks.
  - `[^@\s]+` — satu atau lebih karakter yang **bukan** `@` dan **bukan** spasi/whitespace (`\s`). Ini bagian nama pengguna, misalnya `budi`.
  - `@` — tepat satu tanda `@`.
  - `[^@\s]+` — nama domain, misalnya `mail`.
  - `\.` — titik literal (tanpa `\`, titik berarti "karakter apa saja").
  - `[^@\s]+` — akhiran domain, misalnya `com` atau `ac.id`.
  - `$` — akhir teks, jadi tidak boleh ada sisa karakter lain.

  Contoh valid: `budi@mail.com`, `ani@student.ac.id`. Contoh tidak valid: `budi@mail` (tidak ada titik setelah `@`), `budi mail@x.com` (ada spasi), `a@@b.com` (dua `@`). Pola ini sengaja sederhana, cukup untuk validasi dasar.
- **Baris 26** — Baris kosong pemisah.

## Baris 27–35: Constructor `__init__`

```python
27 |     def __init__(self, id_anggota, nama, telepon="", total_denda=0, email=""):
28 |         self._id = teks_wajib(id_anggota, "ID anggota").upper()  # protected + read-only
29 |         self.nama = nama
30 |         self.telepon = telepon  # public
31 |         self.email = email
32 |         self.__total_denda = 0  # private: hanya diubah lewat method
33 |         if total_denda:
34 |             self.tambah_denda(total_denda)
35 |
```

- **Baris 27** — Constructor yang dipanggil saat objek subclass dibuat. `id_anggota` dan `nama` wajib diisi. `telepon`, `total_denda`, dan `email` punya nilai default sehingga opsional.
- **Baris 28** — Memvalidasi `id_anggota` lewat `teks_wajib` (tidak boleh kosong, spasi tepi dibuang), lalu `.upper()` menjadikannya huruf besar (`"umm001"` → `"UMM001"`) agar pencarian ID konsisten. Hasilnya disimpan di `self._id`. Awalan `_` berarti **protected**, yaitu konvensi "jangan diakses dari luar class/subclass". ID dibuat **read-only** karena property `id` (baris 36–38) tidak punya setter.
- **Baris 29** — `self.nama = nama` **tidak** langsung menyimpan ke atribut, tetapi memanggil **setter** `nama` (baris 44–46), sehingga validasi juga berjalan di constructor. Nilainya akhirnya tersimpan di `self._nama`.
- **Baris 30** — `self.telepon` adalah atribut **public** (tanpa awalan). Bebas dibaca dan diubah dari luar karena tidak ada aturan khusus.
- **Baris 31** — `self.email = email` juga memanggil **setter** `email` (baris 52–58) yang memeriksa format dengan regex.
- **Baris 32** — `self.__total_denda = 0` adalah atribut **private** (dua garis bawah). Python melakukan **name mangling**: nama ini diubah otomatis menjadi `_Anggota__total_denda` (terlihat di `obj.__dict__`). Akibatnya `obj.__total_denda` dari luar menghasilkan `AttributeError`. Nilai awal selalu 0. Denda hanya boleh berubah lewat method.
- **Baris 33** — Jika argumen `total_denda` bernilai *truthy* (bukan 0), maka...
- **Baris 34** — ...denda awal ditambahkan lewat `tambah_denda()`, **bukan** ditulis langsung. Dengan begitu nilai awal juga ikut divalidasi (harus int ≥ 0, bukan bool). Contoh: `Umum("U2", "Sari", total_denda=4000)` → `total_denda` = 4000.
- **Baris 35** — Baris kosong pemisah.

## Baris 36–39: Property `id` (Read-Only)

```python
36 |     @property
37 |     def id(self):
38 |         return self._id
39 |
```

- **Baris 36** — Dekorator `@property` mengubah method di bawahnya menjadi *getter*, sehingga dipanggil seperti atribut biasa: `a.id`, bukan `a.id()`.
- **Baris 37** — Nama property adalah `id`.
- **Baris 38** — Mengembalikan `self._id`. Karena tidak ada `@id.setter`, perintah `a.id = "X"` menghasilkan `AttributeError`, jadi **ID tidak bisa diganti** setelah objek dibuat. Ini masuk akal karena ID dipakai sebagai kunci data di `Perpustakaan`.
- **Baris 39** — Baris kosong pemisah.

## Baris 40–47: Property `nama` dengan Setter

```python
40 |     @property
41 |     def nama(self):
42 |         return self._nama
43 |
44 |     @nama.setter
45 |     def nama(self, nilai):
46 |         self._nama = teks_wajib(nilai, "Nama")
47 |
```

- **Baris 40** — `@property` untuk getter `nama`.
- **Baris 41** — Mendefinisikan getter `nama`.
- **Baris 42** — Mengembalikan nilai asli yang disimpan di atribut protected `self._nama`. Nama atribut penyimpan harus **berbeda** dari nama property (`_nama` vs `nama`). Jika sama, setter akan memanggil dirinya sendiri terus-menerus (rekursi tanpa akhir).
- **Baris 43** — Baris kosong.
- **Baris 44** — `@nama.setter` mendaftarkan method di bawahnya sebagai *setter* property `nama`. Setter ini dijalankan setiap kali ada `obj.nama = ...`.
- **Baris 45** — Setter menerima `nilai` baru.
- **Baris 46** — Memvalidasi lewat `teks_wajib`. Nama kosong atau hanya spasi ditolak dengan `ValueError("Nama tidak boleh kosong")`. Jika valid, nama disimpan tanpa spasi tepi. Contoh: `a.nama = "  Budi  "` → tersimpan `"Budi"`; `a.nama = ""` → error.
- **Baris 47** — Baris kosong.

## Baris 48–59: Property `email` dengan Validasi Regex

```python
48 |     @property
49 |     def email(self):
50 |         return self._email
51 |
52 |     @email.setter
53 |     def email(self, nilai):
54 |         """Email boleh kosong, tetapi jika diisi formatnya harus benar."""
55 |         nilai = (nilai or "").strip()
56 |         if nilai and not self._POLA_EMAIL.match(nilai):
57 |             raise ValueError(f"Format email tidak valid: {nilai}")
58 |         self._email = nilai
59 |
```

- **Baris 48** — `@property` untuk getter `email`.
- **Baris 49** — Mendefinisikan getter `email`.
- **Baris 50** — Mengembalikan `self._email`.
- **Baris 51** — Baris kosong.
- **Baris 52** — `@email.setter` mendaftarkan setter untuk `email`.
- **Baris 53** — Setter menerima `nilai`.
- **Baris 54** — Docstring: email **boleh kosong** (opsional), tetapi jika diisi formatnya harus benar.
- **Baris 55** — `(nilai or "")` mengubah `None` atau string kosong menjadi `""` agar `.strip()` tidak error, lalu `.strip()` membuang spasi tepi. Contoh: `None` → `""`, `" budi@mail.com "` → `"budi@mail.com"`.
- **Baris 56** — Kondisi error hanya berlaku jika email **diisi** (`nilai` truthy) **dan** tidak cocok dengan pola regex. `self._POLA_EMAIL.match(nilai)` mengembalikan objek *match* jika cocok dan `None` jika tidak. Class attribute diakses lewat `self`, dan itu sah.
- **Baris 57** — Melempar `ValueError` berisi email yang salah, misalnya `Format email tidak valid: budi@mail`.
- **Baris 58** — Jika lolos, email disimpan di `self._email` (bisa `""` jika memang dikosongkan).
- **Baris 59** — Baris kosong.

## Baris 60–64: Property `total_denda` (Read-Only)

```python
60 |     @property
61 |     def total_denda(self):
62 |         """Read-only: denda hanya berubah lewat tambah_denda() dan bayar_denda()."""
63 |         return self.__total_denda
64 |
```

- **Baris 60** — `@property` untuk getter `total_denda`.
- **Baris 61** — Mendefinisikan property `total_denda`.
- **Baris 62** — Docstring yang menegaskan bahwa property ini read-only: denda hanya berubah lewat `tambah_denda()` dan `bayar_denda()`.
- **Baris 63** — Mengembalikan atribut private `self.__total_denda`. Di dalam class, nama ini otomatis dibaca sebagai `self._Anggota__total_denda`. Karena **tidak ada setter**, `a.total_denda = 0` menghasilkan `AttributeError`. Inilah cara melindungi data penting: boleh dibaca, tetapi hanya bisa diubah melalui method yang punya aturan.
- **Baris 64** — Baris kosong.

## Baris 65–69: Method `tambah_denda()`

```python
65 |     def tambah_denda(self, jumlah):
66 |         if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah < 0:
67 |             raise ValueError("Jumlah denda harus bilangan bulat >= 0")
68 |         self.__total_denda += jumlah
69 |
```

- **Baris 65** — Method public untuk menambah denda. Dipanggil oleh `Perpustakaan` saat buku dikembalikan terlambat, dan oleh constructor (baris 34).
- **Baris 66** — Validasi tiga syarat yang digabung dengan `or`. Jika salah satu benar, data ditolak:
  - `isinstance(jumlah, bool)` — tolak `True`/`False`. Di Python, `bool` adalah **turunan `int`** (`True == 1`), jadi tanpa cek ini `tambah_denda(True)` akan lolos sebagai 1. Cek ini harus ditaruh **lebih dulu**.
  - `not isinstance(jumlah, int)` — tolak selain bilangan bulat, misalnya `1500.5` atau `"1000"`.
  - `jumlah < 0` — tolak nilai negatif, karena menambah denda negatif sama saja dengan mengurangi denda secara diam-diam. Nilai 0 masih diizinkan.
- **Baris 67** — Melempar `ValueError` dengan pesan yang jelas.
- **Baris 68** — Menambah saldo denda private. Contoh: denda 0, lalu `tambah_denda(6000)` → 6000.
- **Baris 69** — Baris kosong.

## Baris 70–77: Method `bayar_denda()`

```python
70 |     def bayar_denda(self, jumlah):
71 |         if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
72 |             raise ValueError("Jumlah bayar harus bilangan bulat > 0")
73 |         if jumlah > self.__total_denda:
74 |             raise ValueError(f"Jumlah bayar melebihi denda ({rupiah(self.__total_denda)})")
75 |         self.__total_denda -= jumlah
76 |         return self.__total_denda
77 |
```

- **Baris 70** — Method public untuk membayar (mengurangi) denda.
- **Baris 71** — Validasinya sama dengan baris 66, tetapi memakai `jumlah <= 0`: membayar 0 rupiah tidak masuk akal, jadi pembayaran harus > 0.
- **Baris 72** — Pesan error jika jumlah bayar tidak valid.
- **Baris 73** — Mengecek apakah pembayaran **melebihi** denda yang ada. Tanpa cek ini, denda bisa menjadi negatif.
- **Baris 74** — Melempar error yang menampilkan denda saat ini dalam format Rupiah. Contoh: denda 4000, bayar 5000 → `Jumlah bayar melebihi denda (Rp4.000)`. Ini contoh `rupiah()` dipakai di dalam file sendiri.
- **Baris 75** — Mengurangi saldo denda private.
- **Baris 76** — Mengembalikan **sisa denda** agar pemanggil (misalnya `main.py`) bisa langsung menampilkan `Sisa denda: Rp...`. Contoh: denda 6000, `bayar_denda(4000)` → mengembalikan `2000`.
- **Baris 77** — Baris kosong.

## Baris 78–81: Abstract Method `jenis()`

```python
78 |     @abstractmethod
79 |     def jenis(self):
80 |         """Wajib diimplementasikan oleh setiap subclass."""
81 |
```

- **Baris 78** — Dekorator `@abstractmethod` menandai method ini wajib di-*override* oleh subclass. Bersama `ABC` (baris 19), dekorator ini membuat `Anggota` menjadi class abstrak.
- **Baris 79** — Deklarasi method `jenis()`, yang nanti mengembalikan nama jenis anggota (`"Mahasiswa"`, `"Dosen"`, `"Umum"`, ...).
- **Baris 80** — Method ini hanya berisi docstring tanpa `pass`. Itu sah karena docstring sudah dihitung sebagai isi method. Jika subclass lupa mengimplementasikan `jenis()`, subclass itu juga tidak bisa dibuat objeknya (`TypeError`).
- **Baris 81** — Baris kosong.

## Baris 82–85: Method Kooperatif `info_tambahan()`

```python
82 |     def info_tambahan(self):
83 |         """Info khusus tiap subclass; subclass menambahkan lewat super()."""
84 |         return [f"Email: {self.email}"] if self.email else []
85 |
```

- **Baris 82** — Method yang mengembalikan **list** berisi info tambahan untuk ditampilkan di `ringkasan()`.
- **Baris 83** — Docstring: tiap subclass menambahkan infonya sendiri lalu memanggil `super().info_tambahan()`. Pola ini disebut **method kooperatif**: setiap class menyumbang bagiannya, lalu meneruskan panggilan ke class berikutnya dalam MRO. Contoh di `anggota_turunan.py`: `Mahasiswa` mengembalikan `[f"Prodi: {self.prodi}"] + super().info_tambahan()`.
- **Baris 84** — *Conditional expression*: jika email terisi, kembalikan `["Email: budi@mail.com"]`; jika kosong, kembalikan list kosong `[]`. Mengembalikan list (bukan string) memudahkan penggabungan dengan `+`. Pada `AsistenDosen` (MRO: `AsistenDosen → Mahasiswa → Dosen → Anggota`), hasilnya menjadi `[Prodi, Bidang, Email]`, dan versi milik `Anggota` hanya dijalankan **sekali**.
- **Baris 85** — Baris kosong.

## Baris 86–91: Method `ringkasan()`

```python
86 |     def ringkasan(self):
87 |         teks = f"{self.id} | {self.jenis():<13} | {self.nama}"
88 |         for info in self.info_tambahan():
89 |             teks += f" | {info}"
90 |         return (f"{teks} | Maks {self.MAKS_PINJAM} buku/{self.LAMA_PINJAM} hari"
91 |                 f" | Denda: {rupiah(self.total_denda)}")
```

- **Baris 86** — Method yang menghasilkan satu baris teks ringkas tentang anggota (dipakai saat menampilkan daftar anggota).
- **Baris 87** — Menyusun awal teks. Polimorfisme terjadi di sini: `self.jenis()` memanggil versi milik subclass. `:<13` berarti rata kiri dengan lebar 13 karakter (diisi spasi) agar kolom pada tabel sejajar. Contoh: `"Umum"` → `"Umum         "`.
- **Baris 88** — Melakukan perulangan pada setiap item hasil `info_tambahan()`. Versi yang dipanggil mengikuti class objeknya (polimorfisme).
- **Baris 89** — Menambahkan setiap info dengan pemisah `" | "`.
- **Baris 90** — Awal `return`. Dua f-string yang berdampingan di dalam tanda kurung otomatis **digabung** Python (*implicit string concatenation*). Bagian ini menampilkan aturan pinjam dari class attribute lewat `self`, sehingga nilainya mengikuti subclass (misalnya Umum: `Maks 2 buku/7 hari`).
- **Baris 91** — Lanjutan string: menampilkan denda lewat property `total_denda` (bukan langsung `__total_denda`) dan memformatnya dengan `rupiah()`. Contoh hasil lengkap:
  `UMM001 | Umum          | Budi Santoso | Maks 2 buku/7 hari | Denda: Rp0`

## Alur Saat Objek Dibuat

`Anggota` adalah class abstrak, jadi `Anggota("A1", "X")` akan gagal dengan `TypeError`. Sebagai contoh, kita pakai subclass `Umum` (dari `anggota_turunan.py`, berisi `MAKS_PINJAM = 2`, `LAMA_PINJAM = 7`, `DENDA_PER_HARI = 2000`, dan `jenis()` yang mengembalikan `"Umum"`):

```python
a = Umum("umm001", " Budi Santoso ", "085600000000")
```

1. Python memeriksa apakah `Umum` masih punya method abstrak. Karena `jenis()` sudah diimplementasikan, objek boleh dibuat.
2. `Umum` tidak punya `__init__` sendiri, jadi `Anggota.__init__` (baris 27) yang dijalankan dengan `id_anggota="umm001"`, `nama=" Budi Santoso "`, `telepon="085600000000"`, `total_denda=0`, `email=""`.
3. **Baris 28**: `teks_wajib("umm001", ...)` → `"umm001"` → `.upper()` → `self._id = "UMM001"`.
4. **Baris 29**: memanggil setter `nama` → `teks_wajib` membuang spasi → `self._nama = "Budi Santoso"`.
5. **Baris 30**: `self.telepon = "085600000000"` (public, tanpa validasi).
6. **Baris 31**: memanggil setter `email` → `""` tetap `""` → kosong boleh → `self._email = ""`.
7. **Baris 32**: `self.__total_denda = 0`, yang tersimpan sebagai `_Anggota__total_denda`.
8. **Baris 33**: `total_denda` = 0 (falsy), jadi `tambah_denda` tidak dipanggil. **Total denda awal = 0**.
9. Isi `a.__dict__` sekarang:
   `{'_id': 'UMM001', '_nama': 'Budi Santoso', 'telepon': '085600000000', '_email': '', '_Anggota__total_denda': 0}`
10. Penggunaan:
    - `a.id` → `"UMM001"`; `a.total_denda` → `0`; `a.DENDA_PER_HARI` → `2000` (milik `Umum`, menimpa 1000).
    - `a.tambah_denda(6000)` → denda 6000; `a.bayar_denda(4000)` → mengembalikan `2000`.
    - `a.ringkasan()` → `UMM001 | Umum          | Budi Santoso | Maks 2 buku/7 hari | Denda: Rp2.000`.

Variasi dengan denda awal dan email: `Umum("U2", "Sari", email="sari@mail.com", total_denda=4000)`. Denda awal masuk lewat `tambah_denda(4000)` (baris 34), sehingga `ringkasan()` menghasilkan `U2 | Umum          | Sari | Email: sari@mail.com | Maks 2 buku/7 hari | Denda: Rp4.000`.

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Apa beda `_id` dan `__total_denda`?**
   `_` (satu garis bawah) hanya **konvensi** protected: atributnya tetap bisa diakses (`a._id`), tetapi ada tanda "jangan disentuh dari luar". `__` (dua garis bawah) memicu **name mangling**: namanya diubah menjadi `_Anggota__total_denda`, sehingga `a.__total_denda` gagal dan tidak bentrok dengan atribut bernama sama di subclass. Python tidak punya private yang benar-benar mutlak, karena `a._Anggota__total_denda` tetap bisa diakses. Namun cara ini sudah cukup sebagai pengaman.
2. **Kenapa `total_denda` tidak punya setter?**
   Agar denda tidak bisa diubah sembarangan (`a.total_denda = 0` untuk "menghapus" denda). Perubahan harus lewat `tambah_denda()` atau `bayar_denda()`, yang memvalidasi nilai dan mencegah denda negatif.
3. **Kenapa `bool` ditolak padahal `True` itu int?**
   Justru karena `bool` adalah turunan `int` (`isinstance(True, int)` bernilai `True`). Tanpa cek khusus, `tambah_denda(True)` akan dianggap 1 rupiah. Itu hampir pasti bug, jadi ditolak secara eksplisit.
4. **Kenapa `Anggota` dibuat abstrak?**
   "Anggota" saja terlalu umum. Setiap anggota nyata pasti Mahasiswa, Dosen, Umum, atau Asisten Dosen. `@abstractmethod jenis()` memaksa setiap subclass mendefinisikan jenisnya dan mencegah pembuatan objek `Anggota` secara langsung.
5. **Kenapa aturan pinjam memakai class attribute, bukan atribut objek?**
   Aturannya sama untuk semua anggota dengan jenis yang sama, jadi cukup disimpan sekali di class. Subclass cukup menimpa nilainya, dan kode lain cukup membaca `self.MAKS_PINJAM` tanpa perlu `if` untuk tiap jenis anggota (polimorfisme).
6. **Kenapa di `__init__` ditulis `self.nama = nama`, bukan `self._nama = nama`?**
   Supaya validasi di setter ikut berjalan saat objek dibuat. Dengan begitu objek tidak pernah berada dalam keadaan tidak valid.
7. **Apa gunanya `super()` di `info_tambahan()`?**
   Agar setiap class dalam rantai pewarisan menambahkan infonya sendiri tanpa menulis ulang info milik induk. Pada diamond inheritance `AsistenDosen`, `super()` mengikuti MRO sehingga info Prodi, Bidang, dan Email masing-masing muncul tepat sekali.
8. **Kenapa ID tidak boleh diubah?**
   ID adalah identitas unik yang dipakai sebagai kunci data di `Perpustakaan` dan direferensikan oleh data peminjaman. Jika ID bisa diganti, data bisa menjadi tidak sinkron. Karena itu property `id` dibuat tanpa setter.

## Ringkasan

- `rupiah()` mengubah angka menjadi format Rupiah: `f"{jumlah:,}"` lalu koma diganti titik. Contoh: `32000` → `"Rp32.000"`. Fungsi ini dipakai di banyak file.
- `Anggota(ABC)` + `@abstractmethod jenis()` membentuk **class abstrak** yang tidak bisa dibuat objeknya langsung.
- **Class attribute** `MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI` menjadi aturan default yang ditimpa subclass.
- `_POLA_EMAIL` menyimpan regex `^[^@\s]+@[^@\s]+\.[^@\s]+$` untuk validasi email sederhana (email boleh kosong).
- Tingkat akses: `telepon` (public), `_id`/`_nama`/`_email` (protected), dan `__total_denda` (private, di-*mangle* menjadi `_Anggota__total_denda`).
- **Property**: `id` dan `total_denda` bersifat read-only, sedangkan `nama` dan `email` punya setter yang memvalidasi data, termasuk saat constructor berjalan.
- `tambah_denda()` (≥ 0) dan `bayar_denda()` (> 0, tidak melebihi denda, mengembalikan sisa) menjadi satu-satunya jalan untuk mengubah denda. `bool` ditolak di keduanya.
- `info_tambahan()` adalah method kooperatif berbasis `super()`, sedangkan `ringkasan()` memanfaatkan polimorfisme (`jenis()`, `info_tambahan()`, class attribute) untuk menampilkan satu baris info anggota.
