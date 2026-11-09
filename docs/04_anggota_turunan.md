# Penjelasan Baris per Baris: anggota_turunan.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 4 |
| Jumlah baris | 93 baris |
| Konsep PBO | Hierarchical inheritance, override class attribute, override method, abstract method, multiple inheritance (diamond problem), MRO (C3 linearization), `super()` kooperatif dengan `**kwargs`, property (getter/setter) |

## Gambaran Umum

File `anggota_turunan.py` berisi empat subclass dari class abstrak `Anggota` (yang didefinisikan di `anggota.py`, Bagian 3): `Mahasiswa`, `Dosen`, `Umum`, dan `AsistenDosen`. Tiga class pertama mewarisi `Anggota` secara langsung sehingga membentuk **hierarchical inheritance** (satu induk, banyak anak). Setiap subclass mengubah aturan pinjam (`MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI`) dengan meng-*override* class attribute, dan wajib mengimplementasikan method abstrak `jenis()`. Class `AsistenDosen` mewarisi `Mahasiswa` **dan** `Dosen` sekaligus sehingga membentuk **diamond inheritance**; file ini menunjukkan bagaimana Python menyelesaikannya dengan **MRO** dan `super()` yang kooperatif. File ini memakai `teks_wajib()` dari `koleksi.py` (Bagian 1) untuk validasi teks, dan class-class di sini nantinya dipakai oleh `peminjaman.py` (cek batas pinjam & hitung denda), `perpustakaan.py` (data contoh anggota), dan `main.py` (menu tambah anggota).

## Baris 1–10: Docstring Modul (Diagram Hierarki)

```python
 1 | r"""BAGIAN 4 - Inheritance pada anggota (hierarchical + diamond & MRO).
 2 |
 3 |               Anggota (abstract)
 4 |              /       |        \
 5 |        Mahasiswa   Dosen     Umum        hierarchical
 6 |              \       /
 7 |           AsistenDosen                   diamond (multiple inheritance)
 8 |
 9 | MRO AsistenDosen: AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object
10 | """
```

- **Baris 1** — Awal docstring modul. Prefiks `r` membuat string ini **raw string**: karakter backslash `\` (dipakai di diagram baris 4 dan 6) tidak dianggap escape sequence. Tanpa `r`, `\` diikuti spasi/baris baru bisa memicu `SyntaxWarning` "invalid escape sequence" atau mengubah isi teks. Kalimat pertama menjelaskan bahwa file ini adalah Bagian 4 dan topiknya inheritance (hierarchical + diamond & MRO).
- **Baris 2** — Baris kosong di dalam docstring sebagai pemisah judul dan diagram.
- **Baris 3–7** — Diagram ASCII hierarki class: `Anggota` (abstrak) di puncak; `Mahasiswa`, `Dosen`, `Umum` di bawahnya (pola *hierarchical*); `Mahasiswa` dan `Dosen` bertemu lagi di `AsistenDosen` sehingga garisnya membentuk belah ketupat (*diamond*).
- **Baris 8** — Baris kosong di dalam docstring.
- **Baris 9** — Mencatat urutan MRO (Method Resolution Order) `AsistenDosen`, yaitu urutan Python mencari atribut/method. Ini sudah diverifikasi dengan `AsistenDosen.__mro__`.
- **Baris 10** — Penutup docstring (`"""`).

## Baris 11–15: Import

```python
11 |
12 | from anggota import Anggota
13 | from koleksi import teks_wajib
14 |
15 |
```

- **Baris 11** — Baris kosong (pemisah).
- **Baris 12** — Mengimpor class abstrak `Anggota` dari `anggota.py`. Semua class di file ini adalah turunan `Anggota`, jadi induknya harus diimpor dulu.
- **Baris 13** — Mengimpor fungsi `teks_wajib()` dari `koleksi.py`. Fungsi ini memvalidasi bahwa teks tidak kosong (dan merapikan spasi); dipakai di setter `prodi` dan `bidang`. Ini contoh *reuse* kode antar-file.
- **Baris 14–15** — Dua baris kosong sesuai konvensi PEP 8 sebelum definisi class.

## Baris 16–41: Class Mahasiswa

```python
16 | class Mahasiswa(Anggota):
17 |     MAKS_PINJAM = 3
18 |     LAMA_PINJAM = 7
19 |     DENDA_PER_HARI = 1000
20 |
21 |     # **kwargs + super() dengan argumen keyword membuat __init__ "kooperatif":
22 |     # pada diamond, argumen milik Dosen (bidang) diteruskan sesuai MRO.
23 |     def __init__(self, id_anggota, nama, prodi, telepon="", total_denda=0, **kwargs):
24 |         super().__init__(id_anggota=id_anggota, nama=nama, telepon=telepon,
25 |                          total_denda=total_denda, **kwargs)
26 |         self.prodi = prodi
27 |
28 |     @property
29 |     def prodi(self):
30 |         return self._prodi
31 |
32 |     @prodi.setter
33 |     def prodi(self, nilai):
34 |         self._prodi = teks_wajib(nilai, "Prodi")
35 |
36 |     def jenis(self):
37 |         return "Mahasiswa"
38 |
39 |     def info_tambahan(self):
40 |         return [f"Prodi: {self.prodi}"] + super().info_tambahan()
41 |
```

- **Baris 16** — Mendefinisikan class `Mahasiswa` yang mewarisi `Anggota` (*single inheritance*). Otomatis mendapat semua atribut/method `Anggota`: `id`, `nama`, `email`, `total_denda`, `tambah_denda()`, `bayar_denda()`, `ringkasan()`, dll.
- **Baris 17** — Override class attribute `MAKS_PINJAM` menjadi 3 (di `Anggota` default-nya 2). Mahasiswa boleh meminjam maksimal 3 buku sekaligus.
- **Baris 18** — `LAMA_PINJAM = 7` hari. Nilainya sama dengan default `Anggota`, tetapi ditulis ulang agar aturan Mahasiswa terlihat jelas dan tidak bergantung pada default induk.
- **Baris 19** — `DENDA_PER_HARI = 1000` rupiah per hari keterlambatan (juga sama dengan default, ditulis eksplisit).
- **Baris 20** — Baris kosong pemisah.
- **Baris 21–22** — Komentar: menjelaskan bahwa `**kwargs` + `super()` dengan argumen keyword membuat `__init__` **kooperatif**. Pada diamond, argumen yang bukan milik `Mahasiswa` (misalnya `bidang` milik `Dosen`) tidak dibuang, melainkan diteruskan ke class berikutnya di MRO.
- **Baris 23** — Constructor `Mahasiswa`. Parameter wajib: `id_anggota`, `nama`, `prodi`; opsional: `telepon=""`, `total_denda=0`. `**kwargs` menampung argumen keyword lain yang tidak dikenal `Mahasiswa` (mis. `bidang`, `email`) dalam bentuk dictionary.
- **Baris 24–25** — Memanggil `__init__` milik class **berikutnya di MRO** (bukan selalu `Anggota`!). Untuk objek `Mahasiswa` biasa, berikutnya adalah `Anggota`; untuk objek `AsistenDosen`, berikutnya adalah `Dosen`. Semua argumen dikirim sebagai **keyword** (`id_anggota=...`) agar tidak salah posisi ketika class tujuan punya urutan parameter berbeda. `**kwargs` membongkar sisa argumen agar ikut diteruskan. `prodi` sengaja tidak diteruskan karena hanya milik `Mahasiswa`.
- **Baris 26** — Menyimpan prodi lewat **setter** property (bukan langsung ke `_prodi`), sehingga validasi di baris 34 ikut berjalan. Dilakukan setelah `super().__init__` agar atribut dasar induk sudah siap.
- **Baris 27** — Baris kosong.
- **Baris 28** — Decorator `@property`: method di bawahnya bisa diakses seperti atribut (`mhs.prodi` tanpa tanda kurung).
- **Baris 29** — Getter `prodi`.
- **Baris 30** — Mengembalikan nilai dari atribut *protected* `_prodi` (enkapsulasi: data disimpan tersembunyi, diakses lewat property).
- **Baris 31** — Baris kosong.
- **Baris 32** — Decorator `@prodi.setter`: mendaftarkan method berikut sebagai setter, dipanggil saat `self.prodi = ...`.
- **Baris 33** — Setter menerima `nilai` baru.
- **Baris 34** — Memvalidasi dengan `teks_wajib(nilai, "Prodi")` (error jika kosong; "Prodi" dipakai sebagai label pesan error), lalu menyimpan hasilnya ke `_prodi`.
- **Baris 35** — Baris kosong.
- **Baris 36** — Mengimplementasikan method abstrak `jenis()` dari `Anggota`. Karena semua method abstrak sudah diimplementasi, `Mahasiswa` menjadi class **konkret** dan bisa dibuat objeknya.
- **Baris 37** — Mengembalikan teks `"Mahasiswa"`, dipakai di `ringkasan()` (polymorphism: setiap subclass menjawab berbeda).
- **Baris 38** — Baris kosong.
- **Baris 39** — Override method `info_tambahan()` dari `Anggota`.
- **Baris 40** — Membuat list berisi `"Prodi: ..."` lalu **menggabungkan** dengan hasil `super().info_tambahan()` (method berikutnya di MRO). Jadi info induk (mis. Email) tidak hilang, hanya ditambah — ini pola *extend*, bukan *replace*. Pada `AsistenDosen`, `super()` di sini akan memanggil `Dosen.info_tambahan()`.
- **Baris 41** — Baris kosong (bersama baris 42 menjadi dua baris kosong pemisah class).

## Baris 42–66: Class Dosen

```python
42 |
43 | class Dosen(Anggota):
44 |     MAKS_PINJAM = 5
45 |     LAMA_PINJAM = 14
46 |     DENDA_PER_HARI = 500
47 |
48 |     def __init__(self, id_anggota, nama, bidang, telepon="", total_denda=0, **kwargs):
49 |         super().__init__(id_anggota=id_anggota, nama=nama, telepon=telepon,
50 |                          total_denda=total_denda, **kwargs)
51 |         self.bidang = bidang
52 |
53 |     @property
54 |     def bidang(self):
55 |         return self._bidang
56 |
57 |     @bidang.setter
58 |     def bidang(self, nilai):
59 |         self._bidang = teks_wajib(nilai, "Bidang")
60 |
61 |     def jenis(self):
62 |         return "Dosen"
63 |
64 |     def info_tambahan(self):
65 |         return [f"Bidang: {self.bidang}"] + super().info_tambahan()
66 |
```

- **Baris 42** — Baris kosong pemisah class.
- **Baris 43** — Class `Dosen` juga mewarisi `Anggota` langsung. Bersama `Mahasiswa` dan `Umum`, ini membentuk **hierarchical inheritance**.
- **Baris 44** — `MAKS_PINJAM = 5`: dosen boleh pinjam paling banyak (5 buku).
- **Baris 45** — `LAMA_PINJAM = 14`: masa pinjam dosen 2 minggu.
- **Baris 46** — `DENDA_PER_HARI = 500`: denda dosen paling ringan.
- **Baris 47** — Baris kosong.
- **Baris 48** — Constructor `Dosen`, polanya sama dengan `Mahasiswa`, tetapi parameter khususnya `bidang` (bidang keahlian/mata kuliah). `**kwargs` menampung argumen lain (mis. `email`).
- **Baris 49–50** — `super().__init__` kooperatif: meneruskan argumen dasar sebagai keyword + `**kwargs` ke class berikutnya di MRO. Untuk `Dosen` maupun `AsistenDosen`, class berikutnya setelah `Dosen` adalah `Anggota`. `bidang` tidak diteruskan karena sudah "dikonsumsi" di sini.
- **Baris 51** — Menyimpan `bidang` lewat setter agar tervalidasi.
- **Baris 52** — Baris kosong.
- **Baris 53** — `@property` untuk getter `bidang`.
- **Baris 54** — Definisi getter `bidang`.
- **Baris 55** — Mengembalikan atribut protected `_bidang`.
- **Baris 56** — Baris kosong.
- **Baris 57** — `@bidang.setter` mendaftarkan setter.
- **Baris 58** — Setter menerima `nilai`.
- **Baris 59** — Validasi dengan `teks_wajib(nilai, "Bidang")` lalu simpan ke `_bidang`.
- **Baris 60** — Baris kosong.
- **Baris 61** — Implementasi method abstrak `jenis()`.
- **Baris 62** — Mengembalikan `"Dosen"`.
- **Baris 63** — Baris kosong.
- **Baris 64** — Override `info_tambahan()`.
- **Baris 65** — Menambahkan `"Bidang: ..."` di depan hasil `super().info_tambahan()`. Untuk objek `Dosen` maupun `AsistenDosen`, `super()` di sini menuju `Anggota.info_tambahan()` (yang mengembalikan Email jika ada).
- **Baris 66** — Baris kosong.

## Baris 67–76: Class Umum

```python
67 |
68 | class Umum(Anggota):
69 |     MAKS_PINJAM = 2
70 |     LAMA_PINJAM = 7
71 |     DENDA_PER_HARI = 2000
72 |
73 |     def jenis(self):
74 |         return "Umum"
75 |
76 |
```

- **Baris 67** — Baris kosong pemisah class.
- **Baris 68** — Class `Umum` (anggota masyarakat umum) mewarisi `Anggota`, anak ketiga dalam hierarchical inheritance.
- **Baris 69** — `MAKS_PINJAM = 2` (sama dengan default, ditulis eksplisit agar aturan jelas).
- **Baris 70** — `LAMA_PINJAM = 7` hari (sama dengan default).
- **Baris 71** — `DENDA_PER_HARI = 2000`: denda paling berat, inilah yang benar-benar berbeda dari induk.
- **Baris 72** — Baris kosong.
- **Baris 73** — Implementasi `jenis()`. `Umum` **tidak** mendefinisikan `__init__` sendiri, jadi memakai `Anggota.__init__` apa adanya (tidak ada atribut tambahan). `info_tambahan()` juga tidak di-override, sehingga memakai versi `Anggota`.
- **Baris 74** — Mengembalikan `"Umum"`.
- **Baris 75–76** — Dua baris kosong pemisah class.

## Baris 77–93: Class AsistenDosen (Diamond Inheritance)

```python
77 | class AsistenDosen(Mahasiswa, Dosen):
78 |     """Mahasiswa yang juga membantu dosen mengajar (diamond inheritance).
79 |
80 |     - MAKS_PINJAM dan DENDA_PER_HARI tidak ditulis ulang, jadi diambil dari
81 |       Mahasiswa karena Mahasiswa berada lebih dulu di MRO.
82 |     - LAMA_PINJAM di-override menjadi 14 hari (hak seperti dosen).
83 |     - Anggota.__init__ hanya dijalankan SEKALI walaupun diwarisi lewat dua jalur.
84 |     """
85 |
86 |     LAMA_PINJAM = 14
87 |
88 |     def __init__(self, id_anggota, nama, prodi, bidang, telepon="", total_denda=0, email=""):
89 |         super().__init__(id_anggota=id_anggota, nama=nama, prodi=prodi, bidang=bidang,
90 |                          telepon=telepon, total_denda=total_denda, email=email)
91 |
92 |     def jenis(self):
93 |         return "Asisten Dosen"
```

- **Baris 77** — `AsistenDosen` mewarisi **dua** class: `Mahasiswa` dan `Dosen` (*multiple inheritance*). Karena keduanya sama-sama turunan `Anggota`, terbentuk pola **diamond**. Masalah klasiknya (*diamond problem*): method/atribut milik siapa yang dipakai, dan apakah `Anggota.__init__` jalan dua kali? Python menjawabnya dengan **MRO** yang dihitung algoritma **C3 linearization**: `AsistenDosen → Mahasiswa → Dosen → Anggota → ABC → object`. Urutan penulisan induk penting: `Mahasiswa` ditulis duluan sehingga dicari lebih dulu daripada `Dosen`, dan `Anggota` (induk bersama) baru dicari setelah kedua anaknya.
- **Baris 78–84** — Docstring class (multi-baris): menjelaskan makna `AsistenDosen` dan tiga aturannya — (1) `MAKS_PINJAM` dan `DENDA_PER_HARI` tidak ditulis ulang sehingga diambil dari `Mahasiswa` (yang lebih dulu di MRO), yaitu 3 buku dan Rp1.000/hari; (2) `LAMA_PINJAM` di-override menjadi 14 hari seperti dosen; (3) `Anggota.__init__` hanya dijalankan **sekali** walaupun `Anggota` diwarisi lewat dua jalur. Baris 79 adalah baris kosong di dalam docstring.
- **Baris 85** — Baris kosong.
- **Baris 86** — Override class attribute `LAMA_PINJAM = 14`. Tanpa baris ini, nilai yang dipakai adalah 7 (dari `Mahasiswa`, karena `Mahasiswa` lebih dulu di MRO daripada `Dosen`). Ini menunjukkan bahwa class anak bisa "memilih" aturan mana yang ingin diubah.
- **Baris 87** — Baris kosong.
- **Baris 88** — Constructor `AsistenDosen` menerima **gabungan** parameter: `prodi` (milik Mahasiswa) dan `bidang` (milik Dosen), plus `telepon`, `total_denda`, `email`. Di sini tidak ada `**kwargs` karena `AsistenDosen` adalah ujung bawah hierarki — semua parameter didefinisikan eksplisit agar jelas bagi pemakai.
- **Baris 89–90** — Satu kali `super().__init__(...)` dengan semua argumen sebagai keyword. Berdasarkan MRO, panggilan ini masuk ke `Mahasiswa.__init__`, yang mengambil `prodi` lalu meneruskan sisanya (`bidang`, `email`) lewat `**kwargs` ke `Dosen.__init__`, yang mengambil `bidang` lalu meneruskan `email` ke `Anggota.__init__`. Hasilnya: setiap `__init__` dijalankan tepat sekali, termasuk `Anggota.__init__`. Tidak perlu menambahkan baris lain karena `prodi` dan `bidang` sudah diset oleh `Mahasiswa` dan `Dosen`.
- **Baris 91** — Baris kosong.
- **Baris 92** — Override `jenis()`. Tanpa override, `AsistenDosen` akan mewarisi `Mahasiswa.jenis()` (MRO) dan menampilkan "Mahasiswa".
- **Baris 93** — Mengembalikan `"Asisten Dosen"`. Ini baris terakhir file. `info_tambahan()` tidak di-override di sini; versi `Mahasiswa` yang dipakai, lalu berantai lewat `super()` ke `Dosen` dan `Anggota`.

## Alur Saat Objek Dibuat

Contoh: `AsistenDosen("ASD001", "Rizky", "Informatika", "Praktikum PBO")`

MRO (hasil `AsistenDosen.__mro__`):

```
AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object
```

Langkah `__init__`:

1. **`AsistenDosen.__init__`** menerima `id_anggota="ASD001"`, `nama="Rizky"`, `prodi="Informatika"`, `bidang="Praktikum PBO"`, `telepon=""`, `total_denda=0`, `email=""`. Lalu memanggil `super().__init__(...)` → class berikutnya di MRO adalah `Mahasiswa`.
2. **`Mahasiswa.__init__`** mengambil `id_anggota`, `nama`, `prodi`, `telepon`, `total_denda`.
   Sisa yang masuk ke `kwargs` = `{"bidang": "Praktikum PBO", "email": ""}`.
   Memanggil `super().__init__(id_anggota=..., nama=..., telepon=..., total_denda=..., bidang=..., email=...)`. Karena objeknya `AsistenDosen`, class berikutnya setelah `Mahasiswa` di MRO adalah **`Dosen`** (bukan `Anggota`!).
3. **`Dosen.__init__`** mengambil `id_anggota`, `nama`, `bidang`, `telepon`, `total_denda`.
   Sisa `kwargs` = `{"email": ""}`.
   Memanggil `super().__init__(...)` → class berikutnya adalah **`Anggota`**.
4. **`Anggota.__init__`** (dijalankan **sekali**) menerima `id_anggota`, `nama`, `telepon`, `total_denda`, `email`. Menyetel `_id = "ASD001"`, `nama = "Rizky"`, `telepon = ""`, `email = ""`, `__total_denda = 0`. Tidak memanggil `super().__init__` lagi.
5. Kembali ke **`Dosen.__init__`** → menjalankan `self.bidang = "Praktikum PBO"` (validasi `teks_wajib`).
6. Kembali ke **`Mahasiswa.__init__`** → menjalankan `self.prodi = "Informatika"`.
7. Kembali ke **`AsistenDosen.__init__`** → selesai.

Jadi urutan **pemanggilan** adalah AsistenDosen → Mahasiswa → Dosen → Anggota, sedangkan urutan **pengisian atribut** kebalikannya: atribut Anggota dulu, lalu `bidang`, lalu `prodi`.

Hasil `ringkasan()` (diverifikasi dengan menjalankan kode):

```
ASD001 | Asisten Dosen | Rizky | Prodi: Informatika | Bidang: Praktikum PBO | Maks 3 buku/14 hari | Denda: Rp0
```

Urutan `info_tambahan()`:

1. `Mahasiswa.info_tambahan()` → `["Prodi: Informatika"] + super().info_tambahan()`
2. `Dosen.info_tambahan()` → `["Bidang: Praktikum PBO"] + super().info_tambahan()`
3. `Anggota.info_tambahan()` → `["Email: ..."]` jika email diisi, atau `[]` jika kosong.

Hasil akhirnya: `[Prodi, Bidang, Email]`. Pada contoh di atas email kosong, jadi Email tidak tampil. Jika dibuat dengan `email="sari@kampus.ac.id"`, ringkasannya menjadi `... | Prodi: SI | Bidang: Basis Data | Email: sari@kampus.ac.id | Maks 3 buku/14 hari | Denda: Rp0`.

Tabel aturan pinjam tiap class:

| Class | MAKS_PINJAM | LAMA_PINJAM | DENDA_PER_HARI | Asal nilai |
|---|---|---|---|---|
| Anggota (abstrak) | 2 | 7 | 1000 | Default di `anggota.py` |
| Mahasiswa | 3 | 7 | 1000 | Ditulis di `Mahasiswa` (baris 17–19) |
| Dosen | 5 | 14 | 500 | Ditulis di `Dosen` (baris 44–46) |
| Umum | 2 | 7 | 2000 | Ditulis di `Umum` (baris 69–71) |
| AsistenDosen | 3 | 14 | 1000 | `MAKS_PINJAM` & `DENDA_PER_HARI` dari `Mahasiswa` (pertama di MRO); `LAMA_PINJAM` override sendiri (baris 86) |

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Apa itu diamond problem dan bagaimana Python mengatasinya?**
   Diamond problem terjadi ketika sebuah class mewarisi dua class yang punya induk sama, sehingga muncul ambiguitas method mana yang dipakai dan apakah induk bersama diinisialisasi dua kali. Python mengatasinya dengan MRO (algoritma C3) yang menyusun semua class dalam satu urutan linier; induk bersama (`Anggota`) diletakkan setelah semua anaknya, sehingga hanya dikunjungi sekali.

2. **Kenapa `MAKS_PINJAM` AsistenDosen bernilai 3, bukan 5?**
   Karena `AsistenDosen` tidak mendefinisikannya, Python mencari mengikuti MRO; `Mahasiswa` ditemukan lebih dulu daripada `Dosen`, sehingga nilainya 3. Jika urutan induk dibalik menjadi `(Dosen, Mahasiswa)`, nilainya menjadi 5.

3. **Mengapa harus pakai `**kwargs`? Apa yang terjadi tanpa itu?**
   Saat `Mahasiswa.__init__` dipanggil dari `AsistenDosen`, ia menerima `bidang` dan `email` yang bukan parameternya. Tanpa `**kwargs` akan muncul `TypeError: unexpected keyword argument 'bidang'`, dan `Dosen.__init__` tidak akan mendapat nilai `bidang`. `**kwargs` menampung lalu meneruskannya ke class berikutnya di MRO.

4. **Kenapa tidak memanggil `Mahasiswa.__init__(self, ...)` dan `Dosen.__init__(self, ...)` secara langsung?**
   Pemanggilan langsung membuat `Anggota.__init__` berjalan dua kali (atribut di-reset, denda bisa tertambah dua kali jika `total_denda` diisi). `super()` kooperatif menjamin setiap `__init__` dipanggil tepat sekali sesuai MRO.

5. **`super()` di `Mahasiswa` merujuk ke class apa?**
   Tergantung tipe objeknya. Untuk objek `Mahasiswa` → `Anggota`. Untuk objek `AsistenDosen` → `Dosen`. `super()` artinya "class berikutnya di MRO objek ini", bukan "induk langsung".

6. **Kenapa argumen ke `super().__init__` ditulis sebagai keyword (`nama=nama`)?**
   Karena urutan parameter tiap class berbeda (`Mahasiswa` punya `prodi` di posisi ketiga, `Dosen` punya `bidang`). Dengan keyword, nilai selalu sampai ke parameter yang tepat tanpa bergantung posisi.

7. **Kenapa `Umum` tidak punya `__init__`?**
   Karena tidak punya atribut tambahan; `Anggota.__init__` diwarisi apa adanya. Cukup override class attribute dan implementasi `jenis()`.

8. **Apa yang terjadi jika subclass tidak mengimplementasikan `jenis()`?**
   Class itu tetap abstrak, sehingga membuat objeknya memunculkan `TypeError: Can't instantiate abstract class ...`.

## Ringkasan

- `Mahasiswa`, `Dosen`, `Umum` mewarisi `Anggota` → **hierarchical inheritance**.
- Aturan pinjam diubah dengan **override class attribute** (`MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI`); kode lain (mis. `peminjaman.py`) cukup membaca `anggota.MAKS_PINJAM` tanpa peduli jenisnya (polymorphism).
- Setiap subclass wajib mengimplementasikan method abstrak `jenis()`.
- `prodi` dan `bidang` memakai **property + setter** dengan validasi `teks_wajib()`.
- `info_tambahan()` di-override dengan pola `[info sendiri] + super().info_tambahan()` sehingga info berantai: Prodi → Bidang → Email.
- `AsistenDosen(Mahasiswa, Dosen)` adalah **diamond inheritance**; MRO-nya `AsistenDosen → Mahasiswa → Dosen → Anggota → ABC → object` (C3 linearization).
- `super()` **kooperatif** dengan argumen keyword dan `**kwargs` meneruskan argumen sesuai MRO sehingga `Anggota.__init__` dipanggil **tepat sekali**.
- `AsistenDosen` mendapat `MAKS_PINJAM` 3 dan denda Rp1.000 dari `Mahasiswa`, tetapi `LAMA_PINJAM` di-override menjadi 14 hari.
