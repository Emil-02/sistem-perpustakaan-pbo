# Penjelasan Baris per Baris: peminjaman.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 5 |
| File | `peminjaman.py` (111 baris) |
| Konsep PBO | Inheritance pada exception, relasi has-a (asosiasi), enkapsulasi & property read-only, property terhitung, polymorphism (class attribute & method overriding) |

## Gambaran Umum

File `peminjaman.py` berisi dua hal. Pertama, **empat exception kustom** (`PerpustakaanError` sebagai induk, lalu `DataTidakDitemukan`, `DataDuplikat`, dan `PeminjamanDitolak`) yang di-`raise` oleh `perpustakaan.py` saat terjadi kesalahan, dan cukup ditangkap `main.py` dengan satu `except PerpustakaanError`. Kedua, kelas **`Peminjaman`** yang mewakili satu transaksi pinjam: ia *memiliki* (has-a) satu objek anggota (dari `anggota.py`/`anggota_turunan.py`) dan satu objek koleksi (dari `koleksi.py`/`koleksi_turunan.py`). Lama pinjam dan tarif denda dibaca dari objek anggota, sedangkan kena/tidaknya denda ditanyakan ke objek koleksi, sehingga aturan berbeda per jenis tanpa satu pun `if` pengecekan tipe. Objek `Peminjaman` dibuat dan disimpan oleh kelas `Perpustakaan` (`perpustakaan.py`), lalu `ringkasan()`-nya ditampilkan di menu `main.py`.

## Baris 1–12: Docstring Modul dan Import

```python
  1 | """BAGIAN 5 - Exception kustom + transaksi Peminjaman (relasi has-a, polymorphism).
  2 |
  3 | Peminjaman MEMILIKI satu Anggota dan satu Koleksi.
  4 | Lama pinjam & tarif denda diambil dari jenis anggota, kena/tidaknya denda
  5 | diambil dari jenis koleksi -> tanpa if per tipe (polymorphism).
  6 | """
  7 |
  8 | from datetime import date, timedelta
  9 |
 10 | from anggota import rupiah
 11 |
 12 |
```

- **Baris 1–6** — Docstring modul (diawali dan diakhiri `"""`). Baris 1 memberi judul: file ini adalah **Bagian 5** yang berisi exception kustom dan kelas transaksi `Peminjaman`. Baris 3 menegaskan relasi **has-a**: satu `Peminjaman` *memiliki* satu `Anggota` dan satu `Koleksi`. Baris 4–5 meringkas ide **polymorphism**: lama pinjam dan tarif denda diambil dari jenis anggota, sedangkan kena/tidaknya denda ditentukan jenis koleksi, sehingga tidak perlu `if isinstance(...)` per tipe. Baris 6 menutup docstring. Docstring ini bisa dibaca lewat `help(peminjaman)` atau `peminjaman.__doc__`.
- **Baris 8** — Mengimpor `date` (tipe tanggal tanpa jam) dan `timedelta` (selisih/durasi waktu) dari modul standar `datetime`. `date` dipakai untuk tanggal pinjam/kembali, `timedelta` untuk menghitung jatuh tempo.
- **Baris 10** — Mengimpor fungsi `rupiah()` dari `anggota.py` (Bagian 3). Fungsi ini mengubah angka menjadi teks uang, misal `3000` → `'Rp3.000'`. Dipakai ulang agar format uang konsisten di seluruh program (prinsip *reuse*, tidak menulis ulang).
- **Baris kosong 7, 9, 11, 12** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 13–29: Exception Kustom (Inheritance pada Exception)

```python
 13 | # ---------- exception kustom (inheritance pada exception) ----------
 14 | class PerpustakaanError(Exception):
 15 |     """Induk semua error pada sistem perpustakaan."""
 16 |
 17 |
 18 | class DataTidakDitemukan(PerpustakaanError):
 19 |     """Kode koleksi / ID anggota / ID peminjaman tidak ada."""
 20 |
 21 |
 22 | class DataDuplikat(PerpustakaanError):
 23 |     """Kode atau ID yang sama sudah terdaftar."""
 24 |
 25 |
 26 | class PeminjamanDitolak(PerpustakaanError):
 27 |     """Aturan peminjaman/pengembalian/penghapusan dilanggar."""
 28 |
 29 |
```

- **Baris 13** — Komentar penanda bagian: di bawah ini adalah exception kustom yang memakai **inheritance**.
- **Baris 14** — Mendefinisikan kelas `PerpustakaanError` yang **mewarisi** kelas bawaan `Exception`. Karena turunan `Exception`, objeknya bisa di-`raise` dan ditangkap dengan `except`. Kelas ini menjadi **induk** semua error khusus perpustakaan.
- **Baris 15** — Docstring kelas. Kelas ini tidak punya isi lain; docstring sudah cukup sebagai badan kelas (tidak perlu `pass`). Semua perilaku (pesan error, traceback) diwarisi dari `Exception`.
- **Baris 18** — `DataTidakDitemukan` mewarisi `PerpustakaanError` (jadi juga turunan `Exception`). Dipakai di `perpustakaan.py` saat kode koleksi, ID anggota, atau ID peminjaman yang dicari tidak ada.
- **Baris 19** — Docstring yang menjelaskan kapan error ini dipakai.
- **Baris 22** — `DataDuplikat` juga turunan `PerpustakaanError`. Di-`raise` oleh `perpustakaan.py` jika kode koleksi atau ID anggota yang ditambahkan sudah terdaftar.
- **Baris 23** — Docstring penjelas error duplikat.
- **Baris 26** — `PeminjamanDitolak` turunan `PerpustakaanError`. Di-`raise` jika aturan bisnis dilanggar, mis. stok habis, koleksi Referensi hanya baca di tempat, anggota masih punya denda, atau koleksi masih dipinjam saat mau dihapus.
- **Baris 27** — Docstring penjelas. **Manfaat hierarki ini:** `main.py` cukup menulis `except PerpustakaanError` untuk menangkap ketiga anak kelasnya sekaligus (polymorphism pada exception), tetapi kode lain tetap bisa menangkap jenis yang spesifik.
- **Baris kosong 16, 17, 20, 21, 24, 25, 28, 29** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 30–40: Kelas Peminjaman dan Konstruktor (Relasi Has-a)

```python
 30 | # ---------- transaksi ----------
 31 | class Peminjaman:
 32 |     def __init__(self, id_pinjam, anggota, koleksi, tanggal_pinjam=None):
 33 |         self._id = id_pinjam
 34 |         self._anggota = anggota
 35 |         self._koleksi = koleksi
 36 |         self._tanggal_pinjam = tanggal_pinjam or date.today()
 37 |         self._jatuh_tempo = self._tanggal_pinjam + timedelta(days=anggota.LAMA_PINJAM)
 38 |         self._tanggal_kembali = None
 39 |         self._denda = 0
 40 |
```

- **Baris 30** — Komentar penanda bagian kedua: kelas transaksi peminjaman.
- **Baris 31** — Mendefinisikan kelas `Peminjaman`. Kelas ini **tidak mewarisi** `Anggota` maupun `Koleksi` (bukan *is-a*), melainkan **menyimpan** objek keduanya sebagai atribut (relasi *has-a* / asosiasi).
- **Baris 32** — Konstruktor. Parameter: `id_pinjam` (mis. `'P0001'`), `anggota` (objek turunan `Anggota`), `koleksi` (objek turunan `Koleksi`), dan `tanggal_pinjam` yang **opsional** (default `None`). Default `None` dipakai, bukan `date.today()`, karena nilai default di Python dihitung sekali saat fungsi dibuat; `None` membuat tanggal dihitung ulang setiap pemanggilan.
- **Baris 33** — Menyimpan ID transaksi ke atribut `_id`. Awalan `_` menandakan atribut *protected* (enkapsulasi: jangan diubah dari luar).
- **Baris 34** — Menyimpan **objek** anggota (bukan sekadar ID-nya). Inilah relasi has-a: lewat atribut ini `Peminjaman` bisa memanggil atribut/metode anggota, misalnya `LAMA_PINJAM`, `DENDA_PER_HARI`, `nama`.
- **Baris 35** — Menyimpan objek koleksi yang dipinjam (relasi has-a kedua), sehingga bisa memanggil `kena_denda()`, `judul`, `kode`.
- **Baris 36** — `tanggal_pinjam or date.today()` — operator `or` mengembalikan operand pertama yang bernilai *truthy*. Jika `tanggal_pinjam` diisi (objek `date`), itulah yang dipakai; jika `None`, dipakai tanggal hari ini. Ini pola singkat untuk **nilai default**. Mengisi tanggal manual berguna untuk pengujian dan data contoh.
- **Baris 37** — Menghitung jatuh tempo: tanggal pinjam + `timedelta(days=anggota.LAMA_PINJAM)`. `LAMA_PINJAM` adalah *class attribute* yang nilainya berbeda per subclass (Mahasiswa/Umum 7 hari, Dosen/AsistenDosen 14 hari). Kode ini tidak peduli tipe anggotanya — cukup membaca atributnya → **polymorphism**. Hasil `date + timedelta` adalah objek `date` baru.
- **Baris 38** — Tanggal kembali diisi `None` karena saat transaksi dibuat buku belum dikembalikan. `None` juga menjadi penanda transaksi masih aktif.
- **Baris 39** — Denda awal 0. Nilai ini baru diisi ketika `kembalikan()` dipanggil.
- **Baris kosong 40** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 41–68: Property Read-only (Getter Tanpa Setter)

```python
 41 |     # Semua data transaksi read-only dari luar (hanya getter)
 42 |     @property
 43 |     def id(self):
 44 |         return self._id
 45 |
 46 |     @property
 47 |     def anggota(self):
 48 |         return self._anggota
 49 |
 50 |     @property
 51 |     def koleksi(self):
 52 |         return self._koleksi
 53 |
 54 |     @property
 55 |     def tanggal_pinjam(self):
 56 |         return self._tanggal_pinjam
 57 |
 58 |     @property
 59 |     def jatuh_tempo(self):
 60 |         return self._jatuh_tempo
 61 |
 62 |     @property
 63 |     def tanggal_kembali(self):
 64 |         return self._tanggal_kembali
 65 |
 66 |     @property
 67 |     def denda(self):
 68 |         return self._denda
```

- **Baris 41** — Komentar: semua data transaksi dibuat **read-only** dari luar. Kita hanya membuat *getter* (`@property`) tanpa *setter*, sehingga data transaksi tidak bisa diubah sembarangan (menjaga integritas data).
- **Baris 42** — Dekorator `@property` mengubah metode di bawahnya menjadi atribut yang dibaca tanpa tanda kurung: `p.id`, bukan `p.id()`.
- **Baris 43** — Getter `id`. Karena tidak ada `@id.setter`, perintah `p.id = 'X'` akan memunculkan `AttributeError`.
- **Baris 44** — Mengembalikan nilai atribut tersembunyi `_id`.
- **Baris 46** — Dekorator `@property` untuk getter berikutnya.
- **Baris 47** — Getter `anggota` — mengakses objek anggota pemilik transaksi.
- **Baris 48** — Mengembalikan objek `_anggota` (bukan salinan). Contoh pemakaian: `p.anggota.nama`. `perpustakaan.py` memakainya untuk mencari pinjaman aktif milik anggota tertentu.
- **Baris 50** — Dekorator `@property`.
- **Baris 51** — Getter `koleksi`.
- **Baris 52** — Mengembalikan objek `_koleksi`. Dipakai `perpustakaan.py`, mis. `p.koleksi is koleksi` untuk mengecek apakah koleksi masih dipinjam sebelum dihapus.
- **Baris 54** — Dekorator `@property`.
- **Baris 55** — Getter `tanggal_pinjam`.
- **Baris 56** — Mengembalikan `_tanggal_pinjam` (objek `date`).
- **Baris 58** — Dekorator `@property`.
- **Baris 59** — Getter `jatuh_tempo`.
- **Baris 60** — Mengembalikan `_jatuh_tempo` yang sudah dihitung di konstruktor (baris 37).
- **Baris 62** — Dekorator `@property`.
- **Baris 63** — Getter `tanggal_kembali`.
- **Baris 64** — Mengembalikan `_tanggal_kembali`; bernilai `None` jika belum dikembalikan.
- **Baris 66** — Dekorator `@property`.
- **Baris 67** — Getter `denda`.
- **Baris 68** — Mengembalikan `_denda` — denda final yang tercatat saat pengembalian (0 jika belum dikembalikan).
- **Baris kosong 45, 49, 53, 57, 61, 65** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 69–77: Property Terhitung `aktif` dan `status`

```python
 69 |
 70 |     @property
 71 |     def aktif(self):
 72 |         return self._tanggal_kembali is None
 73 |
 74 |     @property
 75 |     def status(self):
 76 |         return "Dipinjam" if self.aktif else "Dikembalikan"
 77 |
```

- **Baris 70** — Dekorator `@property` untuk **property terhitung** (*computed property*): nilainya tidak disimpan, tetapi dihitung saat dibaca.
- **Baris 71** — Property `aktif` — apakah transaksi masih berjalan.
- **Baris 72** — Mengembalikan `True` jika `_tanggal_kembali` masih `None`. Memakai `is None` (membandingkan identitas) adalah cara yang dianjurkan untuk mengecek `None`. Karena dihitung, nilainya otomatis berubah menjadi `False` setelah `kembalikan()` tanpa perlu atribut tambahan yang bisa tidak sinkron.
- **Baris 74** — Dekorator `@property` untuk property terhitung kedua.
- **Baris 75** — Property `status` — versi teks dari `aktif`.
- **Baris 76** — Ekspresi kondisional (*ternary*): `'Dipinjam'` jika `self.aktif` bernilai `True`, selain itu `'Dikembalikan'`. Property memanggil property lain (`self.aktif`) tanpa tanda kurung.
- **Baris kosong 69, 73, 77** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 78–89: Menghitung Keterlambatan dan Denda (Polymorphism)

```python
 78 |     def hari_terlambat(self, tanggal=None):
 79 |         acuan = self._tanggal_kembali or tanggal or date.today()
 80 |         return max(0, (acuan - self._jatuh_tempo).days)
 81 |
 82 |     def terlambat(self, tanggal=None):
 83 |         return self.hari_terlambat(tanggal) > 0
 84 |
 85 |     def hitung_denda(self, tanggal=None):
 86 |         if not self._koleksi.kena_denda():
 87 |             return 0
 88 |         return self.hari_terlambat(tanggal) * self._anggota.DENDA_PER_HARI
 89 |
```

- **Baris 78** — Metode `hari_terlambat`, menghitung jumlah hari keterlambatan. Parameter `tanggal` opsional agar bisa mengecek keterlambatan pada tanggal tertentu (mis. untuk simulasi/pengujian).
- **Baris 79** — Menentukan tanggal acuan dengan rantai `or`: (1) jika sudah dikembalikan, pakai `_tanggal_kembali`; (2) jika belum, pakai argumen `tanggal`; (3) jika keduanya `None`, pakai hari ini. Operand pertama yang tidak `None` yang dipilih.
- **Baris 80** — `acuan - self._jatuh_tempo` menghasilkan objek `timedelta`; `.days` mengambil jumlah harinya (bisa negatif jika belum lewat tempo). `max(0, ...)` memastikan hasil tidak pernah negatif: dikembalikan lebih cepat berarti terlambat 0 hari.
- **Baris 82** — Metode `terlambat` — versi boolean (ya/tidak) dari keterlambatan.
- **Baris 83** — Mengembalikan `True` jika hari terlambat lebih dari 0. Metode ini **memakai ulang** `hari_terlambat()` dan meneruskan argumen `tanggal`, jadi logika hanya ditulis di satu tempat.
- **Baris 85** — Metode `hitung_denda` — menghitung besar denda pada tanggal acuan.
- **Baris 86** — Memanggil `kena_denda()` milik koleksi. Ini **polymorphism lewat method overriding**: `Koleksi`/`Buku` mengembalikan `True`, sedangkan `DigitalMixin` (dipakai `EBook`) meng-*override* menjadi `False`. `Peminjaman` tidak perlu tahu jenis koleksinya.
- **Baris 87** — Jika koleksi tidak kena denda (koleksi digital), langsung kembalikan 0 (*early return*), baris berikutnya tidak dijalankan.
- **Baris 88** — Denda = hari terlambat × `DENDA_PER_HARI` milik anggota. `DENDA_PER_HARI` juga *class attribute* yang berbeda per subclass (Mahasiswa Rp1.000, Dosen Rp500, Umum Rp2.000) → polymorphism tanpa `if` per tipe anggota.
- **Baris kosong 81, 84, 89** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 90–100: Metode `kembalikan()` — Menutup Transaksi

```python
 90 |     def kembalikan(self, tanggal=None):
 91 |         """Menutup transaksi dan mengembalikan besar denda."""
 92 |         if not self.aktif:
 93 |             raise ValueError(f"Peminjaman {self.id} sudah dikembalikan")
 94 |         tanggal = tanggal or date.today()
 95 |         if tanggal < self._tanggal_pinjam:
 96 |             raise ValueError("Tanggal kembali tidak boleh sebelum tanggal pinjam")
 97 |         self._tanggal_kembali = tanggal
 98 |         self._denda = self.hitung_denda()
 99 |         return self._denda
100 |
```

- **Baris 90** — Metode `kembalikan` — menutup transaksi. Parameter `tanggal` opsional (default hari ini).
- **Baris 91** — Docstring metode: menjelaskan bahwa metode menutup transaksi dan mengembalikan besar denda.
- **Baris 92** — Validasi: jika transaksi sudah tidak aktif (sudah dikembalikan sebelumnya) ...
- **Baris 93** — ... munculkan `ValueError` dengan pesan memakai f-string. Mencegah pengembalian ganda yang bisa membuat denda/stok tercatat dua kali.
- **Baris 94** — Jika `tanggal` tidak diisi (`None`), pakai `date.today()` — pola `or` sebagai nilai default yang sama seperti baris 36.
- **Baris 95** — Validasi kedua: tanggal kembali tidak masuk akal jika lebih awal dari tanggal pinjam. Objek `date` bisa dibandingkan dengan `<`.
- **Baris 96** — Jika tidak valid, munculkan `ValueError` agar data transaksi tetap konsisten.
- **Baris 97** — Mencatat tanggal kembali. Sejak baris ini `aktif` otomatis menjadi `False` dan `status` menjadi `'Dikembalikan'` (karena keduanya property terhitung).
- **Baris 98** — Menghitung dan menyimpan denda final. `hitung_denda()` dipanggil tanpa argumen karena `hari_terlambat()` kini memakai `_tanggal_kembali` yang baru diisi sebagai acuan (baris 79).
- **Baris 99** — Mengembalikan besar denda ke pemanggil. `perpustakaan.py` memakai nilai ini untuk menambah total denda anggota dan menambah kembali stok koleksi.
- **Baris kosong 100** — Pemisah agar kode mudah dibaca (PEP 8: dua baris kosong antar-kelas/fungsi tingkat atas, satu baris antar-metode).

## Baris 101–111: Metode `ringkasan()` — Teks untuk Ditampilkan

```python
101 |     def ringkasan(self, tanggal=None):
102 |         teks = (f"{self.id} | {self.anggota.nama} ({self.anggota.id}) | "
103 |                 f"{self.koleksi.judul} ({self.koleksi.kode}) | "
104 |                 f"Pinjam: {self.tanggal_pinjam} | Tempo: {self.jatuh_tempo} | {self.status}")
105 |         if not self.aktif:
106 |             return teks + f" ({self.tanggal_kembali}) | Denda: {rupiah(self.denda)}"
107 |         if self.terlambat(tanggal):
108 |             keterangan = (f"denda {rupiah(self.hitung_denda(tanggal))}"
109 |                           if self.koleksi.kena_denda() else "tanpa denda, koleksi digital")
110 |             teks += f" | TERLAMBAT {self.hari_terlambat(tanggal)} hari ({keterangan})"
111 |         return teks
```

- **Baris 101** — Metode `ringkasan` — membuat satu baris teks ringkasan transaksi untuk ditampilkan di menu (`main.py`). Parameter `tanggal` opsional untuk mengecek keterlambatan pada tanggal tertentu.
- **Baris 102–104** — Menyusun teks dasar dari tiga f-string yang ditulis berdampingan di dalam tanda kurung. Python otomatis **menggabungkan string literal yang berdampingan**, dan tanda kurung membuat ekspresi boleh dipecah ke beberapa baris. Isinya: ID, nama & ID anggota, judul & kode koleksi, tanggal pinjam, jatuh tempo, dan status. Semua diambil lewat property (`self.id`, `self.anggota.nama`, `self.koleksi.judul`, ...) — data objek lain diakses melalui relasi has-a.
- **Baris 105** — Jika transaksi sudah selesai (tidak aktif) ...
- **Baris 106** — ... tambahkan tanggal kembali dan denda (diformat `rupiah()`), lalu langsung `return`. Transaksi yang sudah selesai tidak perlu dicek keterlambatannya lagi.
- **Baris 107** — Untuk transaksi yang masih aktif: cek apakah sudah melewati jatuh tempo pada tanggal acuan.
- **Baris 108–109** — Menyusun keterangan memakai ekspresi kondisional yang dipecah 2 baris (dalam tanda kurung). Jika koleksi kena denda, tampilkan perkiraan denda berjalan (`hitung_denda(tanggal)` diformat `rupiah`); jika tidak (EBook), tampilkan `'tanpa denda, koleksi digital'`. Lagi-lagi keputusan diserahkan ke `kena_denda()` milik objek koleksi.
- **Baris 110** — Menambahkan peringatan `TERLAMBAT n hari (keterangan)` ke teks dengan operator `+=`.
- **Baris 111** — Mengembalikan teks ringkasan. Untuk pinjaman aktif yang belum terlambat, teks dasar dikembalikan apa adanya. Ini juga baris terakhir file (baris 111).

## Contoh Perhitungan

Aturan anggota (class attribute di `anggota_turunan.py`): **Mahasiswa** 7 hari, Rp1.000/hari; **Dosen** 14 hari, Rp500/hari; **Umum** 7 hari, Rp2.000/hari. Koleksi: `Buku.kena_denda()` → `True`, `EBook.kena_denda()` → `False`.

```python
from datetime import date
m = Mahasiswa("M001", "Budi Santoso", "Informatika")
d = Dosen("D001", "Dr. Sari", "Basis Data")
buku = Buku("B001", "Pemrograman Python", 2020, "Andi", "Informatika Press")
ebook = EBook("E001", "Belajar OOP", 2022, "Rina", "Digital Press")

p1 = Peminjaman("P0001", m, buku, date(2024, 1, 1))
p1.jatuh_tempo                    # datetime.date(2024, 1, 8)
p1.kembalikan(date(2024, 1, 11))  # 3000
```

| Kasus | Jatuh tempo | Kembali | Hari terlambat | Perhitungan | Denda |
|---|---|---|---|---|---|
| Mahasiswa + Buku | 2024-01-08 (1 Jan + 7) | 2024-01-11 | 3 | 3 × Rp1.000 | **Rp3.000** |
| Dosen + Buku | 2024-01-15 (1 Jan + 14) | 2024-01-11 | 0 (`max(0, -4)`) | 0 × Rp500 | **Rp0** |
| Dosen + Buku | 2024-01-15 | 2024-01-20 | 5 | 5 × Rp500 | **Rp2.500** |
| Mahasiswa + EBook | 2024-01-08 | 2024-01-11 | 3 | `kena_denda()` = False → langsung 0 | **Rp0** |

Langkah untuk Mahasiswa + Buku: `jatuh_tempo = 2024-01-01 + timedelta(days=7) = 2024-01-08` → `(2024-01-11 - 2024-01-08).days = 3` → `max(0, 3) = 3` → `buku.kena_denda()` True → `3 × 1000 = 3000`.

Contoh output `ringkasan()` (hasil menjalankan kode sungguhan):

```text
# p1 sebelum dikembalikan, dicek pada 2024-01-11:
P0001 | Budi Santoso (M001) | Pemrograman Python (B001) | Pinjam: 2024-01-01 | Tempo: 2024-01-08 | Dipinjam | TERLAMBAT 3 hari (denda Rp3.000)
# p1 setelah kembalikan(date(2024, 1, 11)):
P0001 | Budi Santoso (M001) | Pemrograman Python (B001) | Pinjam: 2024-01-01 | Tempo: 2024-01-08 | Dikembalikan (2024-01-11) | Denda: Rp3.000
# Dosen, dikembalikan 2024-01-11 (belum lewat tempo):
P0002 | Dr. Sari (D001) | Pemrograman Python (B001) | Pinjam: 2024-01-01 | Tempo: 2024-01-15 | Dikembalikan (2024-01-11) | Denda: Rp0
# Mahasiswa + EBook, dicek pada 2024-01-11 sebelum dikembalikan:
P0003 | Budi Santoso (M001) | Belajar OOP (E001) | Pinjam: 2024-01-01 | Tempo: 2024-01-08 | Dipinjam | TERLAMBAT 3 hari (tanpa denda, koleksi digital)
```

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Mengapa membuat `PerpustakaanError` sebagai induk exception?**  
   Agar semua error khusus perpustakaan bisa ditangkap sekaligus dengan `except PerpustakaanError` (seperti di `main.py`), karena `except` juga menangkap semua subclass. Jika perlu, error tertentu tetap bisa ditangkap secara spesifik.
2. **Apa beda relasi `Peminjaman` dengan `Anggota`/`Koleksi` dibanding inheritance?**  
   Ini relasi **has-a** (asosiasi): `Peminjaman` menyimpan objek anggota dan koleksi sebagai atribut. Peminjaman *bukan* sejenis anggota atau koleksi, jadi tidak tepat memakai inheritance (*is-a*).
3. **Di mana letak polymorphism di file ini?**  
   Pada `anggota.LAMA_PINJAM` dan `anggota.DENDA_PER_HARI` (nilai berbeda per subclass anggota) serta `koleksi.kena_denda()` (di-override `EBook` lewat `DigitalMixin`). Kode yang sama menghasilkan perilaku berbeda tergantung objeknya, tanpa `if isinstance`.
4. **Mengapa hanya ada getter tanpa setter?**  
   Supaya data transaksi read-only dari luar. Perubahan hanya boleh lewat metode resmi `kembalikan()` yang memvalidasi data, sehingga tanggal dan denda tidak bisa dimanipulasi sembarangan (enkapsulasi).
5. **Mengapa `aktif` dan `status` tidak disimpan sebagai atribut biasa?**  
   Keduanya dihitung dari `_tanggal_kembali`, jadi selalu sinkron. Jika disimpan terpisah, ada risiko lupa memperbarui sehingga data bertentangan.
6. **Apa fungsi `max(0, ...)` di `hari_terlambat`?**  
   Selisih tanggal bisa negatif jika dikembalikan sebelum jatuh tempo. `max(0, ...)` memastikan keterlambatan minimal 0, sehingga denda tidak pernah negatif.
7. **Mengapa default parameter `tanggal_pinjam=None`, bukan `date.today()`?**  
   Nilai default dievaluasi sekali saat fungsi didefinisikan. Dengan `None` lalu `tanggal_pinjam or date.today()`, tanggal hari ini dihitung setiap kali objek dibuat.
8. **Mengapa `kembalikan()` memakai `ValueError`, bukan `PeminjamanDitolak`?**  
   Itu validasi data dasar di level objek (input tidak valid). `main.py` menangkap `ValueError` juga, jadi pesan tetap tampil rapi; aturan bisnis tingkat perpustakaan memakai `PeminjamanDitolak` di `perpustakaan.py`.

## Ringkasan

- Empat exception kustom membentuk hierarki: `PerpustakaanError` (induk) → `DataTidakDitemukan`, `DataDuplikat`, `PeminjamanDitolak`.
- `Peminjaman` memiliki (has-a) satu anggota dan satu koleksi, bukan mewarisinya.
- Jatuh tempo = tanggal pinjam + `timedelta(days=anggota.LAMA_PINJAM)`.
- Semua data transaksi read-only lewat `@property`; satu-satunya cara mengubah adalah `kembalikan()`.
- `aktif` dan `status` adalah property terhitung dari `_tanggal_kembali`.
- Denda = `max(0, hari terlambat)` × `anggota.DENDA_PER_HARI`, atau 0 jika `koleksi.kena_denda()` bernilai `False`.
- Pola `x or default` dipakai untuk nilai default tanggal; `ringkasan()` menyajikan transaksi sebagai satu baris teks untuk `main.py`.
