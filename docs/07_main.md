# Penjelasan Baris per Baris: main.py

| Info | Keterangan |
|---|---|
| Presenter | Orang 7 |
| File | `main.py` (Bagian 7 – menu console / titik masuk program) |
| Jumlah baris | 217 baris |
| Konsep yang dibahas | modul & `import`, fungsi bantu, f-string, *exception handling* (`try/except`, exception induk `PerpustakaanError`), fungsi sebagai nilai (*first-class function*) & `lambda`, *dict comprehension*, `getattr`/`setattr` + *property setter*, `isinstance`, *polymorphism* (`ringkasan()`), `__mro__` & *multiple inheritance*, `EOFError`/`KeyboardInterrupt`, `if __name__ == "__main__"` |

## Gambaran Umum

`main.py` adalah **lapisan antarmuka (UI) berbasis teks** sekaligus **titik masuk** program. File ini *tidak* berisi aturan bisnis perpustakaan: semua aturan (stok, batas pinjam, denda, validasi data) sudah ada di file 1–6. Tugas `main.py` hanya: (1) menanyakan input ke pengguna, (2) membuat objek dari class yang tepat (`Buku`, `Majalah`, `EBook`, `Referensi`, `Mahasiswa`, `Dosen`, `AsistenDosen`, `Umum`), (3) memanggil method milik objek `Perpustakaan` (file 6) dan (4) mencetak hasil atau pesan gagal. Semua menu dibangun oleh satu method generik `tampilkan_menu()` yang menerima daftar opsi berisi **fungsi**, sehingga kode menu menjadi pendek dan seragam. Jika aturan dilanggar, file lain melempar exception (`DataTidakDitemukan`, `DataDuplikat`, `PeminjamanDitolak` – semuanya turunan `PerpustakaanError` dari file 5, atau `ValueError` dari setter) dan `main.py` cukup menangkapnya di satu tempat lalu menampilkan `[GAGAL] ...`.

Struktur menu:

```text
PERPUSTAKAAN KAMPUS (menu utama)      -> MenuPerpustakaan.jalankan()
├── 1. Kelola koleksi                 -> menu_koleksi()
│     ├── 1. Lihat semua              -> cetak_daftar(daftar_koleksi())
│     ├── 2. Tambah                   -> tambah_koleksi()
│     ├── 3. Cari                     -> cetak_daftar(cari_koleksi_kata())
│     ├── 4. Ubah                     -> ubah_koleksi() -> ubah_data()
│     ├── 5. Hapus                    -> hapus_koleksi()
│     └── 0. Kembali
├── 2. Kelola anggota                 -> menu_anggota()
│     ├── 1. Lihat semua / 2. Tambah / 3. Cari / 4. Ubah / 5. Hapus
│     └── 0. Kembali
├── 3. Pinjam koleksi                 -> pinjam()
├── 4. Kembalikan koleksi             -> kembalikan()
├── 5. Bayar denda                    -> bayar_denda()
├── 6. Laporan                        -> menu_laporan()
│     ├── 1. Ringkasan perpustakaan   -> perpus.laporan()
│     ├── 2. Peminjaman aktif
│     ├── 3. Peminjaman terlambat
│     ├── 4. Riwayat peminjaman
│     ├── 5. Anggota berdenda
│     ├── 6. Struktur class & MRO     -> struktur_kelas()
│     └── 0. Kembali
└── 0. Keluar                         -> "Terima kasih!"
```

Hubungan dengan file lain:

```text
main.py ──import──> anggota.py          (Anggota, rupiah)
        ──import──> anggota_turunan.py  (Mahasiswa, Dosen, Umum, AsistenDosen)
        ──import──> koleksi.py          (Koleksi, Buku)
        ──import──> koleksi_turunan.py  (Majalah, Referensi, EBook)
        ──import──> peminjaman.py       (PerpustakaanError)
        ──import──> perpustakaan.py     (buat_data_contoh -> objek Perpustakaan)
```

## Baris 1–5: Docstring modul

```python
  1 | """BAGIAN 7 - Menu console (titik masuk program).
  2 |
  3 | Jalankan: python main.py
  4 | Data contoh dibuat di memori setiap program dijalankan (tidak disimpan ke file).
  5 | """
```

- **Baris 1** — Awal *docstring* modul (string bertanda kutip tiga `"""`). Docstring yang diletakkan di baris paling atas file menjadi dokumentasi modul dan bisa dibaca lewat `main.__doc__` atau `help(main)`. Isinya menandai bahwa file ini adalah *Bagian 7* dan merupakan *titik masuk program* (file yang dijalankan pertama kali).
- **Baris 2** — Baris kosong di dalam docstring, pemisah antara judul dan keterangan (konvensi PEP 257).
- **Baris 3** — Petunjuk cara menjalankan: `python main.py`.
- **Baris 4** — Penjelasan penting: data contoh dibuat ulang **di memori (RAM)** setiap kali program dijalankan, jadi semua perubahan hilang saat program ditutup (tidak ada penyimpanan file/database).
- **Baris 5** — Penutup docstring.

## Baris 6–14: Import

```python
  6 |
  7 | from datetime import date
  8 |
  9 | from anggota import Anggota, rupiah
 10 | from anggota_turunan import AsistenDosen, Dosen, Mahasiswa, Umum
 11 | from koleksi import Buku, Koleksi
 12 | from koleksi_turunan import EBook, Majalah, Referensi
 13 | from peminjaman import PerpustakaanError
 14 | from perpustakaan import buat_data_contoh
```

- **Baris 6** — Baris kosong, pemisah docstring dan import.
- **Baris 7** — Mengimpor class `date` dari modul bawaan `datetime`. Dipakai di `tanya_tanggal()` untuk `date.fromisoformat()` (mengubah teks `"2026-11-09"` menjadi objek tanggal) dan `date.today()` (tanggal hari ini).
- **Baris 8** — Baris kosong; memisahkan import *library bawaan* dari import *modul buatan sendiri* (konvensi PEP 8).
- **Baris 9** — Dari `anggota.py` (file 3) diambil class abstrak `Anggota` (dipakai di `struktur_kelas()` untuk menampilkan MRO) dan fungsi `rupiah()` (memformat angka menjadi teks seperti `Rp5.000`, dipakai di `bayar_denda()`).
- **Baris 10** — Dari `anggota_turunan.py` (file 4) diambil keempat subclass anggota. Dibutuhkan untuk **membuat objek** saat menambah anggota, untuk pengecekan `isinstance` saat mengubah anggota, dan untuk menampilkan MRO.
- **Baris 11** — Dari `koleksi.py` (file 1) diambil class abstrak `Koleksi` (untuk MRO) dan `Buku` (untuk membuat objek & `isinstance`).
- **Baris 12** — Dari `koleksi_turunan.py` (file 2) diambil `EBook`, `Majalah`, `Referensi`. `DigitalMixin` tidak perlu diimpor karena tidak pernah dipakai langsung di sini (ia tetap muncul di MRO `EBook`).
- **Baris 13** — Dari `peminjaman.py` (file 5) cukup diimpor **exception induk** `PerpustakaanError`. Karena `DataTidakDitemukan`, `DataDuplikat`, dan `PeminjamanDitolak` adalah turunannya, `except PerpustakaanError` otomatis menangkap ketiganya (prinsip *inheritance* juga berlaku pada exception).
- **Baris 14** — Dari `perpustakaan.py` (file 6) diambil fungsi `buat_data_contoh()` yang mengembalikan objek `Perpustakaan` yang sudah terisi 6 koleksi dan 5 anggota. Class `Perpustakaan` sendiri tidak perlu diimpor karena objeknya dibuat oleh fungsi ini.

## Baris 15–19: Fungsi `tanya()`

```python
 15 |
 16 |
 17 | def tanya(prompt, bawaan=None):
 18 |     teks = input(f"{prompt}{f' [{bawaan}]' if bawaan is not None else ''}: ").strip()
 19 |     return teks if teks else ("" if bawaan is None else str(bawaan))
```

- **Baris 15–16** — Dua baris kosong sebelum definisi fungsi tingkat modul (aturan PEP 8).
- **Baris 17** — Mendefinisikan fungsi `tanya` dengan dua parameter: `prompt` (teks pertanyaan) dan `bawaan` (nilai *default*/nilai lama) yang nilai default-nya `None`. Fungsi ini adalah pembungkus `input()` agar semua pertanyaan di program punya gaya yang sama.
- **Baris 18** — Baris terpadat di file ini. Diuraikan dari dalam ke luar:
  - `f' [{bawaan}]'` → f-string kecil yang menghasilkan misalnya `" [1]"` atau `" [Rizky Pratama]"`.
  - `f' [{bawaan}]' if bawaan is not None else ''` → *conditional expression* (operator ternary): kalau ada nilai bawaan tampilkan dalam kurung siku, kalau tidak tampilkan string kosong. Dipakai `is not None` (bukan `if bawaan`) supaya nilai bawaan `0` atau `""` tetap ditampilkan sebagai `[0]` / `[]`.
  - `f"{prompt}{ ... }: "` → f-string luar yang menyambung teks pertanyaan + bagian kurung siku + `": "`. Ini **f-string bersarang**; kutip dalam memakai `'` agar tidak bentrok dengan kutip luar `"`. Hasil contoh: `Stok [1]: ` atau `Kode: `.
  - `input(...)` → menampilkan teks itu lalu menunggu pengguna mengetik dan menekan Enter; hasilnya selalu bertipe `str`.
  - `.strip()` → membuang spasi/tab di awal dan akhir input agar `" B001 "` dianggap `"B001"`.
  - Hasil akhirnya disimpan di variabel `teks`.
- **Baris 19** — Menentukan nilai yang dikembalikan: jika `teks` tidak kosong (string kosong bernilai *falsy*), kembalikan `teks`. Jika pengguna hanya menekan Enter: kembalikan `""` bila tidak ada bawaan, atau `str(bawaan)` bila ada. `str()` dipakai agar tipe kembalian **selalu string** (mis. bawaan `1` → `"1"`); konversi ke angka diserahkan pada *setter* di class model (mis. setter `stok` dan `tahun` memakai `angka_bulat()`), sehingga validasi tetap terpusat di class.

## Baris 20–24: Fungsi `tanya_tanggal()`

```python
 20 |
 21 |
 22 | def tanya_tanggal(prompt):
 23 |     teks = tanya(f"{prompt} (YYYY-MM-DD, kosong = hari ini)")
 24 |     return date.fromisoformat(teks) if teks else date.today()
```

- **Baris 20–21** — Dua baris kosong pemisah fungsi.
- **Baris 22** — Fungsi untuk meminta input tanggal. Parameter `prompt` misalnya `"Tanggal pinjam"`.
- **Baris 23** — **Memanggil ulang** `tanya()` (penggunaan kembali kode/*reuse*), dengan prompt ditambah petunjuk format `(YYYY-MM-DD, kosong = hari ini)`.
- **Baris 24** — Ternary lagi: kalau ada teks, ubah menjadi objek `date` dengan `date.fromisoformat(teks)`; kalau kosong, pakai `date.today()`. Bila format salah (mis. `09-11-2026`), `fromisoformat` melempar `ValueError` yang nanti ditangkap oleh `jalankan_aksi()` dan dicetak sebagai `[GAGAL] ...`.

## Baris 25–30: Fungsi `cetak_daftar()`

```python
 25 |
 26 |
 27 | def cetak_daftar(judul, data):
 28 |     print(f"\n--- {judul} ---")
 29 |     for baris in data or ["(kosong)"]:
 30 |         print(baris if isinstance(baris, str) else baris.ringkasan())
```

- **Baris 25–26** — Dua baris kosong pemisah.
- **Baris 27** — Fungsi untuk mencetak daftar apa pun (koleksi, anggota, peminjaman) dengan judul.
- **Baris 28** — Mencetak judul, mis. `--- Koleksi ---`. `\n` di depan membuat satu baris kosong sebelum judul agar tampilan rapi.
- **Baris 29** — `data or ["(kosong)"]`: operator `or` mengembalikan operan pertama jika *truthy*, jika tidak mengembalikan operan kedua. List kosong bernilai *falsy*, jadi bila tidak ada data, yang di-loop adalah list berisi satu teks `"(kosong)"`. Trik ini menghindari `if` tambahan.
- **Baris 30** — Jika elemen adalah `str` (yaitu teks `"(kosong)"`), cetak langsung. Selain itu panggil `baris.ringkasan()`. Inilah **polymorphism**: fungsi ini tidak peduli objeknya `Buku`, `Majalah`, `Mahasiswa`, `AsistenDosen`, atau `Peminjaman` — semuanya punya method `ringkasan()` (di-*override* di tiap class) dan Python memanggil versi milik class objek tersebut. Jadi satu fungsi bisa mencetak semua jenis daftar.

## Baris 31–34: Fungsi `teks_mro()`

```python
 31 |
 32 |
 33 | def teks_mro(kelas):
 34 |     return " -> ".join(k.__name__ for k in kelas.__mro__)
```

- **Baris 31–32** — Dua baris kosong pemisah.
- **Baris 33** — Fungsi yang menerima sebuah **class** (bukan objek) sebagai argumen. Di Python class juga objek, sehingga bisa dikirim ke fungsi.
- **Baris 34** — `kelas.__mro__` adalah *tuple* berisi urutan class yang ditelusuri Python saat mencari method/atribut (*Method Resolution Order*), mis. `(AsistenDosen, Mahasiswa, Dosen, Anggota, ABC, object)`. `k.__name__` mengambil nama class sebagai teks. `(... for k in ...)` adalah *generator expression*, dan `" -> ".join(...)` menggabungkan nama-nama itu dengan pemisah `" -> "`. Hasil: `"AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object"`.

## Baris 35–39: Class `MenuPerpustakaan` dan konstruktornya

```python
 35 |
 36 |
 37 | class MenuPerpustakaan:
 38 |     def __init__(self, perpus):
 39 |         self.perpus = perpus
```

- **Baris 35–36** — Dua baris kosong sebelum definisi class.
- **Baris 37** — Mendefinisikan class `MenuPerpustakaan`. Seluruh logika menu dibungkus dalam class agar semua method bisa berbagi satu objek perpustakaan lewat `self.perpus`.
- **Baris 38** — Konstruktor `__init__` yang menerima objek `Perpustakaan`.
- **Baris 39** — Menyimpan objek itu sebagai atribut `self.perpus`. Ini relasi **asosiasi/komposisi**: menu *memiliki* (has-a) perpustakaan dan meneruskan semua pekerjaan ke sana. Menu tidak menyimpan data koleksi/anggota sendiri.

## Baris 40–46: Kerangka menu – `jalankan_aksi()`

```python
 40 |
 41 |     # ---------- kerangka menu ----------
 42 |     def jalankan_aksi(self, aksi):
 43 |         try:
 44 |             aksi()
 45 |         except (PerpustakaanError, ValueError, TypeError) as e:
 46 |             print(f"[GAGAL] {e}")
```

- **Baris 40** — Baris kosong pemisah method.
- **Baris 41** — Komentar penanda kelompok method "kerangka menu" (method umum yang dipakai semua menu).
- **Baris 42** — Method yang menerima `aksi`, yaitu sebuah **fungsi** (*callable*) yang akan dijalankan.
- **Baris 43** — Membuka blok `try`: kode di dalamnya "dicoba"; kalau terjadi exception, alur pindah ke `except`.
- **Baris 44** — `aksi()` → memanggil fungsi yang dikirim. Karena `aksi` adalah variabel berisi fungsi, tanda kurung `()` di sini yang benar-benar mengeksekusinya.
- **Baris 45** — Menangkap tiga jenis error sekaligus (ditulis sebagai tuple): `PerpustakaanError` (beserta semua turunannya: `DataTidakDitemukan`, `DataDuplikat`, `PeminjamanDitolak`), `ValueError` (input tidak valid dari setter, `int()`, atau `date.fromisoformat()`), dan `TypeError` (mis. objek bukan turunan `Koleksi`/`Anggota`). `as e` menyimpan objek exception ke variabel `e`.
- **Baris 46** — Mencetak pesan error, mis. `[GAGAL] Stok 'Bumi Manusia' sedang habis`. Program **tidak berhenti**; pengguna kembali ke menu. Dengan menaruh `try/except` di satu tempat ini, semua method menu (tambah, pinjam, dsb.) tidak perlu menulis `try/except` sendiri.

## Baris 47–62: Kerangka menu – `tampilkan_menu()`

```python
 47 |
 48 |     def tampilkan_menu(self, judul, opsi, teks_keluar="Kembali"):
 49 |         """opsi: list (kunci, teks, fungsi). Berulang sampai pengguna memilih 0."""
 50 |         while True:
 51 |             print(f"\n===== {judul} =====")
 52 |             for kunci, teks, _ in opsi:
 53 |                 print(f"{kunci}. {teks}")
 54 |             print(f"0. {teks_keluar}")
 55 |             pilihan = input("Pilih: ").strip()
 56 |             if pilihan == "0":
 57 |                 return
 58 |             aksi = {k: f for k, _, f in opsi}.get(pilihan)
 59 |             if aksi:
 60 |                 self.jalankan_aksi(aksi)
 61 |             else:
 62 |                 print("Pilihan tidak tersedia.")
```

- **Baris 47** — Baris kosong pemisah.
- **Baris 48** — Method generik untuk **semua** menu. Parameter: `judul` (judul menu), `opsi` (list tuple), dan `teks_keluar` dengan default `"Kembali"` (menu utama memakai `"Keluar"`).
- **Baris 49** — Docstring method: setiap opsi berbentuk tuple `(kunci, teks, fungsi)` dan menu diulang sampai pengguna memilih `0`.
- **Baris 50** — `while True` = perulangan tanpa akhir; keluar hanya lewat `return` di baris 57.
- **Baris 51** — Mencetak judul menu, mis. `===== KOLEKSI =====`.
- **Baris 52** — Loop seluruh opsi dengan *tuple unpacking*: tiap tuple dibongkar ke `kunci`, `teks`, dan `_`. Nama `_` adalah konvensi untuk "nilai yang tidak dipakai" (fungsinya tidak diperlukan saat mencetak).
- **Baris 53** — Mencetak tiap pilihan, mis. `1. Lihat semua`.
- **Baris 54** — Mencetak pilihan keluar, mis. `0. Kembali` / `0. Keluar`.
- **Baris 55** — Membaca pilihan pengguna dan membuang spasi.
- **Baris 56** — Jika pengguna memilih `"0"` ...
- **Baris 57** — ... `return` keluar dari method (dan otomatis dari `while`). Untuk submenu, kembali ke menu pemanggil; untuk menu utama, lanjut ke `print("Terima kasih!")`.
- **Baris 58** — *Dict comprehension* `{k: f for k, _, f in opsi}` membangun kamus dari list opsi, mis. `{"1": fungsi_lihat, "2": self.tambah_koleksi, ...}`. Lalu `.get(pilihan)` mengambil fungsi sesuai pilihan; jika kunci tidak ada, `.get` mengembalikan `None` (tidak error seperti `dict[...]`). Ini pengganti rantai `if/elif` yang panjang.
- **Baris 59** — `if aksi:` → benar jika fungsi ditemukan (bukan `None`).
- **Baris 60** — Menjalankan fungsi itu **melalui** `jalankan_aksi()` agar setiap error tertangkap.
- **Baris 61** — Selain itu (pilihan tidak dikenal) ...
- **Baris 62** — ... cetak pesan, lalu `while` mengulang menampilkan menu.

## Baris 63–74: Kerangka menu – `ubah_data()`

```python
 63 |
 64 |     def ubah_data(self, objek, atribut_list):
 65 |         """Ubah atribut lewat setter; kosongkan input agar nilai lama tetap."""
 66 |         for atribut in atribut_list:
 67 |             lama = getattr(objek, atribut)
 68 |             baru = tanya(f"{atribut.replace('_', ' ').capitalize()}", lama)
 69 |             if baru != str(lama):
 70 |                 try:
 71 |                     setattr(objek, atribut, baru)  # validasi dijalankan oleh setter
 72 |                 except ValueError as e:
 73 |                     print(f"[GAGAL] {atribut}: {e}")
 74 |         print("Data diperbarui:", objek.ringkasan())
```

- **Baris 63** — Baris kosong pemisah.
- **Baris 64** — Method generik untuk mengubah data objek apa pun (koleksi maupun anggota). `atribut_list` berisi **nama** atribut dalam bentuk string, mis. `["judul", "tahun", "stok"]`.
- **Baris 65** — Docstring: perubahan dilakukan lewat *setter*; jika input dikosongkan, nilai lama dipertahankan.
- **Baris 66** — Loop setiap nama atribut.
- **Baris 67** — `getattr(objek, atribut)` membaca atribut berdasarkan **nama dalam string**; `getattr(buku, "judul")` sama dengan `buku.judul`. Karena `judul` adalah `@property`, getter property-lah yang dijalankan.
- **Baris 68** — Menanyakan nilai baru dengan nilai lama sebagai bawaan. `atribut.replace('_', ' ').capitalize()` mengubah nama atribut menjadi label yang enak dibaca: `"format_file"` → `"Format file"`, `"ukuran_mb"` → `"Ukuran mb"`. Contoh tampilan: `Judul [Laskar Pelangi]: `.
- **Baris 69** — Hanya mengubah jika nilai baru berbeda dari nilai lama. `str(lama)` diperlukan karena `baru` selalu string sedangkan `lama` bisa angka (mis. tahun `2005`); tanpa `str()` perbandingan `"2005" != 2005` selalu `True`.
- **Baris 70** — Membuka `try` untuk tiap atribut, sehingga kegagalan satu atribut tidak membatalkan atribut lain.
- **Baris 71** — `setattr(objek, atribut, baru)` sama dengan `objek.<atribut> = baru`. Poin penting: karena atributnya property, assignment ini **memicu setter**, sehingga validasi di class model tetap berjalan (mis. judul tidak boleh kosong, tahun harus angka dan dalam rentang, stok tidak negatif, email harus valid, format e-book harus didukung). Komentar di baris ini menegaskan hal itu. Setter juga yang mengonversi teks `"3"` menjadi angka `3`.
- **Baris 72** — Jika setter menolak, ia melempar `ValueError`; ditangkap di sini.
- **Baris 73** — Mencetak pesan gagal beserta nama atributnya, mis. `[GAGAL] email: Format email tidak valid: rizky-salah`, lalu loop lanjut ke atribut berikutnya.
- **Baris 74** — Setelah semua atribut diproses, cetak ringkasan objek terbaru (polymorphism lewat `ringkasan()`).

## Baris 75–85: Menu utama – `jalankan()`

```python
 75 |
 76 |     def jalankan(self):
 77 |         self.tampilkan_menu(self.perpus.nama.upper(), [
 78 |             ("1", "Kelola koleksi", self.menu_koleksi),
 79 |             ("2", "Kelola anggota", self.menu_anggota),
 80 |             ("3", "Pinjam koleksi", self.pinjam),
 81 |             ("4", "Kembalikan koleksi", self.kembalikan),
 82 |             ("5", "Bayar denda", self.bayar_denda),
 83 |             ("6", "Laporan", self.menu_laporan),
 84 |         ], teks_keluar="Keluar")
 85 |         print("Terima kasih!")
```

- **Baris 75** — Baris kosong pemisah.
- **Baris 76** — Method yang memulai menu utama.
- **Baris 77** — Memanggil `tampilkan_menu()` dengan judul nama perpustakaan dalam huruf besar (`"Perpustakaan Kampus".upper()` → `PERPUSTAKAAN KAMPUS`) dan sebuah list opsi.
- **Baris 78** — Opsi 1: `self.menu_koleksi` ditulis **tanpa tanda kurung**, artinya yang dimasukkan adalah *fungsinya* (bound method), bukan hasil pemanggilannya. Fungsi baru dijalankan nanti di `jalankan_aksi()`. Ini contoh **fungsi sebagai nilai** (*first-class function*).
- **Baris 79** — Opsi 2: menuju submenu anggota.
- **Baris 80** — Opsi 3: langsung menjalankan proses pinjam.
- **Baris 81** — Opsi 4: proses pengembalian.
- **Baris 82** — Opsi 5: pembayaran denda.
- **Baris 83** — Opsi 6: submenu laporan.
- **Baris 84** — Menutup list opsi dan mengirim argumen bernama `teks_keluar="Keluar"` agar pilihan 0 menu utama bertuliskan "Keluar".
- **Baris 85** — Dijalankan setelah `tampilkan_menu()` selesai (pengguna memilih 0): cetak salam penutup.

## Baris 86–97: Submenu koleksi – `menu_koleksi()`

```python
 86 |
 87 |     # ---------- koleksi ----------
 88 |     def menu_koleksi(self):
 89 |         self.tampilkan_menu("KOLEKSI", [
 90 |             ("1", "Lihat semua", lambda: cetak_daftar("Koleksi", self.perpus.daftar_koleksi())),
 91 |             ("2", "Tambah", self.tambah_koleksi),
 92 |             ("3", "Cari", lambda: cetak_daftar(
 93 |                 "Hasil", self.perpus.cari_koleksi_kata(tanya("Kata kunci")))),
 94 |             ("4", "Ubah", self.ubah_koleksi),
 95 |             ("5", "Hapus", lambda: print("Dihapus:",
 96 |                                          self.perpus.hapus_koleksi(tanya("Kode")).judul)),
 97 |         ])
```

- **Baris 86** — Baris kosong pemisah.
- **Baris 87** — Komentar penanda kelompok method koleksi.
- **Baris 88** — Method submenu koleksi.
- **Baris 89** — Memanggil menu generik dengan judul `"KOLEKSI"` (teks keluar memakai default `"Kembali"`).
- **Baris 90** — Opsi "Lihat semua". Dipakai `lambda` karena kita perlu memanggil `cetak_daftar` **dengan argumen** tetapi **belum sekarang**. `lambda: ...` membuat fungsi tanpa nama dan tanpa parameter yang isinya baru dieksekusi saat dipanggil. Jika ditulis tanpa `lambda`, `cetak_daftar(...)` akan langsung berjalan saat list dibuat.
- **Baris 91** — Opsi "Tambah": method biasa tanpa argumen, jadi cukup referensi `self.tambah_koleksi`.
- **Baris 92** — Opsi "Cari": `lambda` yang akan memanggil `cetak_daftar("Hasil", ...)`. Ekspresi dilanjutkan ke baris berikutnya karena masih di dalam tanda kurung (Python mengizinkan pindah baris di dalam `()`).
- **Baris 93** — Lanjutan: `tanya("Kata kunci")` dijalankan dulu, hasilnya dikirim ke `self.perpus.cari_koleksi_kata(...)` yang mengembalikan list koleksi yang cocok, lalu list itu dicetak. Urutan eksekusi dari dalam ke luar.
- **Baris 94** — Opsi "Ubah": method `ubah_koleksi`.
- **Baris 95** — Opsi "Hapus": `lambda` yang mencetak `"Dihapus:"` diikuti ...
- **Baris 96** — ... `self.perpus.hapus_koleksi(tanya("Kode")).judul`: minta kode, hapus koleksi, dan karena `hapus_koleksi()` **mengembalikan objek yang dihapus**, kita bisa langsung mengambil `.judul`-nya (*method chaining*). Jika koleksi masih dipinjam, `PeminjamanDitolak` dilempar dan ditangkap `jalankan_aksi()`.
- **Baris 97** — Menutup list opsi dan pemanggilan `tampilkan_menu`.

## Baris 98–116: Menambah koleksi – `tambah_koleksi()`

```python
 98 |
 99 |     def tambah_koleksi(self):
100 |         jenis = tanya("Jenis (1 Buku, 2 Majalah, 3 E-Book, 4 Referensi)")
101 |         if jenis not in ("1", "2", "3", "4"):
102 |             raise ValueError("Jenis koleksi tidak valid")
103 |         kode, judul, tahun = tanya("Kode"), tanya("Judul"), tanya("Tahun")
104 |         if jenis == "2":
105 |             koleksi = Majalah(kode, judul, tahun, tanya("Edisi"), tanya("Stok", 1))
106 |         else:
107 |             penulis, penerbit = tanya("Penulis"), tanya("Penerbit")
108 |             if jenis == "1":
109 |                 koleksi = Buku(kode, judul, tahun, penulis, penerbit, tanya("Stok", 1))
110 |             elif jenis == "3":
111 |                 koleksi = EBook(kode, judul, tahun, penulis, penerbit, tanya("Format", "PDF"),
112 |                                 tanya("Ukuran MB", 1.0), tanya("Jumlah lisensi", 1))
113 |             else:
114 |                 koleksi = Referensi(kode, judul, tahun, penulis, penerbit, tanya("Stok", 1))
115 |         self.perpus.tambah_koleksi(koleksi)
116 |         print("Ditambahkan:", koleksi.ringkasan())
```

- **Baris 98** — Baris kosong pemisah.
- **Baris 99** — Method untuk menambah koleksi baru.
- **Baris 100** — Menanyakan jenis koleksi (1–4).
- **Baris 101** — Jika input bukan salah satu dari `"1"`–`"4"` ...
- **Baris 102** — ... lempar `ValueError` secara sengaja dengan `raise`. Exception ini ditangkap `jalankan_aksi()` → `[GAGAL] Jenis koleksi tidak valid`. Validasi dilakukan **sebelum** menanyakan data lain agar pengguna tidak membuang waktu.
- **Baris 103** — *Multiple assignment*: tiga `tanya()` dijalankan berurutan (kiri ke kanan) dan hasilnya dimasukkan ke `kode`, `judul`, `tahun`. Ketiga data ini dimiliki semua jenis koleksi (atribut milik class induk `Koleksi`).
- **Baris 104** — Jenis 2 = Majalah ditangani terpisah karena Majalah **tidak** punya penulis/penerbit.
- **Baris 105** — Membuat objek `Majalah` (subclass `Koleksi`) dengan edisi dan stok (bawaan 1). `tahun` dan `stok` masih string; konstruktor memanggil setter yang memvalidasi dan mengonversinya.
- **Baris 106** — Selain Majalah (Buku, E-Book, Referensi) ...
- **Baris 107** — ... ketiganya turunan `Buku`, jadi sama-sama butuh penulis dan penerbit; ditanyakan sekali di sini agar tidak berulang.
- **Baris 108** — Jika jenis 1 ...
- **Baris 109** — ... buat objek `Buku` dengan stok (bawaan 1).
- **Baris 110** — Jika jenis 3 ...
- **Baris 111** — ... buat `EBook` (multiple inheritance: `DigitalMixin` + `Buku`) dengan format file (bawaan `"PDF"`) ...
- **Baris 112** — ... ukuran file dalam MB (bawaan `1.0`) dan jumlah lisensi (bawaan 1). Jumlah lisensi masuk ke parameter `stok` milik `EBook`, karena stok e-book = jumlah lisensi yang boleh dipinjam bersamaan. Format dan ukuran divalidasi setter `DigitalMixin`.
- **Baris 113** — Sisanya (jenis 4) ...
- **Baris 114** — ... buat `Referensi` (turunan `Buku` yang tidak bisa dipinjam/baca di tempat).
- **Baris 115** — Menyerahkan objek ke `Perpustakaan`. Di sana dicek tipe (`TypeError`) dan kode ganda (`DataDuplikat`). Perhatikan: variabel `koleksi` bisa bertipe apa saja, tetapi `tambah_koleksi()` menerimanya karena semua adalah `Koleksi` (*substitusi/polymorphism*).
- **Baris 116** — Mencetak ringkasan; versi `ringkasan()` yang dipanggil tergantung class objek (polymorphism).

## Baris 117–127: Mengubah koleksi – `ubah_koleksi()`

```python
117 |
118 |     def ubah_koleksi(self):
119 |         koleksi = self.perpus.cari_koleksi(tanya("Kode"))
120 |         atribut = ["judul", "tahun", "stok"]
121 |         if isinstance(koleksi, Buku):
122 |             atribut += ["penulis", "penerbit"]
123 |         if isinstance(koleksi, Majalah):
124 |             atribut += ["edisi"]
125 |         if isinstance(koleksi, EBook):
126 |             atribut += ["format_file", "ukuran_mb"]
127 |         self.ubah_data(koleksi, atribut)
```

- **Baris 117** — Baris kosong pemisah.
- **Baris 118** — Method untuk mengubah data koleksi.
- **Baris 119** — Mencari koleksi berdasarkan kode; jika tidak ada, `cari_koleksi()` melempar `DataTidakDitemukan` (ditangkap `jalankan_aksi()`).
- **Baris 120** — Atribut yang dimiliki **semua** koleksi (didefinisikan di class `Koleksi`).
- **Baris 121** — `isinstance(koleksi, Buku)` bernilai `True` untuk `Buku` **dan semua turunannya** (`Referensi`, `EBook`), karena isinstance memperhitungkan pewarisan.
- **Baris 122** — Jika Buku/turunannya, tambahkan `penulis` dan `penerbit` ke list (`+=` pada list = menambah elemen).
- **Baris 123** — Cek apakah Majalah ...
- **Baris 124** — ... tambahkan `edisi`.
- **Baris 125** — Cek apakah EBook. Sengaja memakai `if` terpisah (bukan `elif`) agar satu objek bisa lolos beberapa pengecekan: `EBook` lolos cek `Buku` **dan** cek `EBook` ...
- **Baris 126** — ... sehingga E-Book mendapat atribut `penulis`, `penerbit`, `format_file`, dan `ukuran_mb` sekaligus.
- **Baris 127** — Menyerahkan objek dan daftar atribut ke `ubah_data()` yang generik.

## Baris 128–139: Submenu anggota – `menu_anggota()`

```python
128 |
129 |     # ---------- anggota ----------
130 |     def menu_anggota(self):
131 |         self.tampilkan_menu("ANGGOTA", [
132 |             ("1", "Lihat semua", lambda: cetak_daftar("Anggota", self.perpus.daftar_anggota())),
133 |             ("2", "Tambah", self.tambah_anggota),
134 |             ("3", "Cari", lambda: cetak_daftar(
135 |                 "Hasil", self.perpus.cari_anggota_kata(tanya("Kata kunci")))),
136 |             ("4", "Ubah", self.ubah_anggota),
137 |             ("5", "Hapus", lambda: print("Dihapus:",
138 |                                          self.perpus.hapus_anggota(tanya("ID")).nama)),
139 |         ])
```

- **Baris 128** — Baris kosong pemisah.
- **Baris 129** — Komentar penanda kelompok method anggota.
- **Baris 130** — Method submenu anggota; strukturnya sama persis dengan `menu_koleksi()` (pola yang konsisten).
- **Baris 131** — Memanggil menu generik dengan judul `"ANGGOTA"`.
- **Baris 132** — "Lihat semua": `lambda` yang mencetak semua anggota; tiap anggota dicetak dengan `ringkasan()` miliknya (polymorphism).
- **Baris 133** — "Tambah": referensi method `tambah_anggota`.
- **Baris 134** — "Cari": `lambda` pencarian, dilanjutkan ke baris berikutnya ...
- **Baris 135** — ... minta kata kunci → `cari_anggota_kata()` → hasil dicetak.
- **Baris 136** — "Ubah": referensi method `ubah_anggota`.
- **Baris 137** — "Hapus": `lambda` mencetak `"Dihapus:"` ...
- **Baris 138** — ... diikuti `.nama` dari objek anggota yang dikembalikan `hapus_anggota()`. Ditolak (`PeminjamanDitolak`) bila anggota masih meminjam atau masih punya denda.
- **Baris 139** — Menutup list dan pemanggilan.

## Baris 140–157: Menambah anggota – `tambah_anggota()`

```python
140 |
141 |     def tambah_anggota(self):
142 |         jenis = tanya("Jenis (1 Mahasiswa, 2 Dosen, 3 Asisten Dosen, 4 Umum)")
143 |         if jenis not in ("1", "2", "3", "4"):
144 |             raise ValueError("Jenis anggota tidak valid")
145 |         id_anggota, nama = tanya("ID"), tanya("Nama")
146 |         if jenis == "1":
147 |             anggota = Mahasiswa(id_anggota, nama, tanya("Prodi"))
148 |         elif jenis == "2":
149 |             anggota = Dosen(id_anggota, nama, tanya("Bidang"))
150 |         elif jenis == "3":
151 |             anggota = AsistenDosen(id_anggota, nama, tanya("Prodi"), tanya("Bidang"))
152 |         else:
153 |             anggota = Umum(id_anggota, nama)
154 |         anggota.telepon = tanya("Telepon (boleh kosong)")
155 |         anggota.email = tanya("Email (boleh kosong)")
156 |         self.perpus.tambah_anggota(anggota)
157 |         print("Ditambahkan:", anggota.ringkasan())
```

- **Baris 140** — Baris kosong pemisah.
- **Baris 141** — Method untuk menambah anggota baru.
- **Baris 142** — Menanyakan jenis anggota (1–4).
- **Baris 143** — Validasi pilihan jenis ...
- **Baris 144** — ... jika salah, lempar `ValueError`.
- **Baris 145** — Data yang dimiliki semua anggota: ID dan nama (atribut class induk `Anggota`).
- **Baris 146** — Jenis 1 ...
- **Baris 147** — ... buat `Mahasiswa` dengan tambahan `prodi`.
- **Baris 148** — Jenis 2 ...
- **Baris 149** — ... buat `Dosen` dengan tambahan `bidang`.
- **Baris 150** — Jenis 3 ...
- **Baris 151** — ... buat `AsistenDosen` yang butuh `prodi` **dan** `bidang`, karena ia mewarisi `Mahasiswa` sekaligus `Dosen` (*diamond inheritance*).
- **Baris 152** — Selain itu (jenis 4) ...
- **Baris 153** — ... buat `Umum` yang hanya butuh ID dan nama.
- **Baris 154** — Mengisi telepon setelah objek dibuat (atribut publik biasa, boleh kosong). Diletakkan di luar `if/elif` agar tidak ditulis empat kali.
- **Baris 155** — Mengisi email. `email` adalah property: assignment ini memicu **setter** yang memvalidasi format. Jika salah, `ValueError` dilempar **sebelum** baris 156, sehingga anggota tidak jadi ditambahkan.
- **Baris 156** — Menyerahkan objek ke `Perpustakaan` (cek tipe dan ID ganda → `DataDuplikat`).
- **Baris 157** — Mencetak ringkasan anggota baru.

## Baris 158–166: Mengubah anggota – `ubah_anggota()`

```python
158 |
159 |     def ubah_anggota(self):
160 |         anggota = self.perpus.cari_anggota(tanya("ID"))
161 |         atribut = ["nama", "telepon", "email"]
162 |         if isinstance(anggota, Mahasiswa):
163 |             atribut += ["prodi"]
164 |         if isinstance(anggota, Dosen):
165 |             atribut += ["bidang"]  # AsistenDosen mendapat prodi DAN bidang
166 |         self.ubah_data(anggota, atribut)
```

- **Baris 158** — Baris kosong pemisah.
- **Baris 159** — Method untuk mengubah data anggota.
- **Baris 160** — Mencari anggota berdasarkan ID (bisa melempar `DataTidakDitemukan`).
- **Baris 161** — Atribut milik semua anggota.
- **Baris 162** — Jika objek adalah `Mahasiswa` (termasuk `AsistenDosen`, karena ia turunan Mahasiswa) ...
- **Baris 163** — ... tambahkan `prodi`.
- **Baris 164** — Jika objek adalah `Dosen` (termasuk `AsistenDosen`, karena ia juga turunan Dosen) ...
- **Baris 165** — ... tambahkan `bidang`. Komentar menegaskan: karena dua `if` terpisah, `AsistenDosen` **lolos keduanya** sehingga mendapat `prodi` **dan** `bidang`. Ini bukti nyata multiple inheritance: `isinstance(asisten, Mahasiswa)` dan `isinstance(asisten, Dosen)` sama-sama `True`.
- **Baris 166** — Memanggil `ubah_data()` generik.

## Baris 167–172: Transaksi – `pinjam()`

```python
167 |
168 |     # ---------- transaksi ----------
169 |     def pinjam(self):
170 |         transaksi = self.perpus.pinjam(tanya("ID anggota"), tanya("Kode koleksi"),
171 |                                        tanya_tanggal("Tanggal pinjam"))
172 |         print("Berhasil:", transaksi.ringkasan())
```

- **Baris 167** — Baris kosong pemisah.
- **Baris 168** — Komentar penanda kelompok method transaksi.
- **Baris 169** — Method proses peminjaman.
- **Baris 170** — Memanggil `self.perpus.pinjam(...)` dengan tiga argumen: ID anggota, kode koleksi (diminta berurutan) ...
- **Baris 171** — ... dan tanggal pinjam. Semua aturan (stok habis, Referensi baca di tempat, masih punya denda, ada pinjaman terlambat, melebihi batas `MAKS_PINJAM`, sudah meminjam judul yang sama) dicek di `Perpustakaan.pinjam()` dan dilempar sebagai `PeminjamanDitolak`. `main.py` cukup memanggil — inilah pemisahan tanggung jawab antara UI dan logika bisnis. Hasilnya objek `Peminjaman` baru.
- **Baris 172** — Mencetak ringkasan transaksi (ID, anggota, koleksi, tanggal pinjam, jatuh tempo, status).

## Baris 173–178: Transaksi – `kembalikan()`

```python
173 |
174 |     def kembalikan(self):
175 |         cetak_daftar("Pinjaman aktif", self.perpus.pinjaman_aktif())
176 |         transaksi = self.perpus.kembalikan(tanya("ID peminjaman"),
177 |                                            tanya_tanggal("Tanggal kembali"))
178 |         print("Dikembalikan:", transaksi.ringkasan())
```

- **Baris 173** — Baris kosong pemisah.
- **Baris 174** — Method proses pengembalian.
- **Baris 175** — Menampilkan dulu daftar pinjaman aktif supaya pengguna tahu ID peminjaman yang harus diketik (mis. `P0001`).
- **Baris 176** — Memanggil `self.perpus.kembalikan(...)` dengan ID peminjaman ...
- **Baris 177** — ... dan tanggal kembali. Di dalamnya stok dikembalikan dan denda keterlambatan (jika ada) ditambahkan ke anggota.
- **Baris 178** — Mencetak ringkasan transaksi yang statusnya sudah dikembalikan (beserta denda bila terlambat).

## Baris 179–185: Transaksi – `bayar_denda()`

```python
179 |
180 |     def bayar_denda(self):
181 |         anggota = self.perpus.cari_anggota(tanya("ID anggota"))
182 |         print(f"Denda {anggota.nama}: {rupiah(anggota.total_denda)}")
183 |         jumlah = int(tanya("Jumlah bayar"))  # bayar_denda() mewajibkan int
184 |         sisa = self.perpus.bayar_denda(anggota.id, jumlah)
185 |         print("Sisa denda:", rupiah(sisa))
```

- **Baris 179** — Baris kosong pemisah.
- **Baris 180** — Method pembayaran denda.
- **Baris 181** — Mencari anggota berdasarkan ID.
- **Baris 182** — Menampilkan total denda dalam format rupiah memakai fungsi `rupiah()` dari `anggota.py`. `total_denda` adalah property *read-only* (nilai aslinya disimpan di atribut private `__total_denda`).
- **Baris 183** — Mengubah input menjadi `int`. Komentar menjelaskan alasannya: `bayar_denda()` di class model mewajibkan bilangan bulat. Jika pengguna mengetik `abc`, `int()` melempar `ValueError` → `[GAGAL] ...`.
- **Baris 184** — Memanggil `self.perpus.bayar_denda()` dengan `anggota.id` (ID yang sudah dinormalisasi huruf besar) dan jumlah bayar; method mengembalikan **sisa denda**. Ditolak bila anggota tidak punya denda atau jumlah melebihi denda.
- **Baris 185** — Mencetak sisa denda dalam format rupiah.

## Baris 186–200: Submenu laporan – `menu_laporan()`

```python
186 |
187 |     # ---------- laporan ----------
188 |     def menu_laporan(self):
189 |         self.tampilkan_menu("LAPORAN", [
190 |             ("1", "Ringkasan perpustakaan", lambda: print(self.perpus.laporan())),
191 |             ("2", "Peminjaman aktif", lambda: cetak_daftar(
192 |                 "Aktif", self.perpus.pinjaman_aktif())),
193 |             ("3", "Peminjaman terlambat", lambda: cetak_daftar(
194 |                 "Terlambat", self.perpus.pinjaman_terlambat())),
195 |             ("4", "Riwayat peminjaman", lambda: cetak_daftar(
196 |                 "Riwayat", self.perpus.daftar_peminjaman())),
197 |             ("5", "Anggota berdenda", lambda: cetak_daftar(
198 |                 "Berdenda", [a for a in self.perpus.daftar_anggota() if a.total_denda > 0])),
199 |             ("6", "Struktur class & MRO", self.struktur_kelas),
200 |         ])
```

- **Baris 186** — Baris kosong pemisah.
- **Baris 187** — Komentar penanda kelompok method laporan.
- **Baris 188** — Method submenu laporan.
- **Baris 189** — Memanggil menu generik dengan judul `"LAPORAN"`.
- **Baris 190** — Opsi 1: `lambda` yang mencetak string laporan ringkas hasil `self.perpus.laporan()` (jumlah koleksi, anggota, pinjaman, denda tertunggak).
- **Baris 191** — Opsi 2: `lambda` yang mencetak daftar berjudul `"Aktif"` ...
- **Baris 192** — ... berisi `pinjaman_aktif()` (peminjaman yang belum dikembalikan).
- **Baris 193** — Opsi 3: daftar `"Terlambat"` ...
- **Baris 194** — ... dari `pinjaman_terlambat()` (aktif dan sudah lewat jatuh tempo).
- **Baris 195** — Opsi 4: daftar `"Riwayat"` ...
- **Baris 196** — ... dari `daftar_peminjaman()` (semua transaksi, aktif maupun selesai).
- **Baris 197** — Opsi 5: daftar `"Berdenda"` ...
- **Baris 198** — ... dibuat dengan *list comprehension* `[a for a in ... if a.total_denda > 0]`: ambil semua anggota, saring yang dendanya lebih dari 0. Penyaringan dilakukan di `main.py` karena `Perpustakaan` tidak punya method khusus untuk ini.
- **Baris 199** — Opsi 6: referensi method `struktur_kelas` untuk menampilkan MRO.
- **Baris 200** — Menutup list opsi dan pemanggilan.

## Baris 201–206: Struktur class – `struktur_kelas()`

```python
201 |
202 |     def struktur_kelas(self):
203 |         print("\n--- MRO (urutan pencarian method) ---")
204 |         for kelas in (Koleksi, Buku, Majalah, Referensi, EBook,
205 |                       Anggota, Mahasiswa, Dosen, Umum, AsistenDosen):
206 |             print(f"{kelas.__name__:<12}: {teks_mro(kelas)}")
```

- **Baris 201** — Baris kosong pemisah.
- **Baris 202** — Method untuk menampilkan hierarki class (fitur edukatif untuk presentasi PBO).
- **Baris 203** — Mencetak judul bagian.
- **Baris 204** — Loop sebuah tuple berisi **class-class** (bukan objek). Baris dilanjutkan karena masih dalam tanda kurung ...
- **Baris 205** — ... lanjutan tuple: class keluarga anggota. Total 10 class dari file 1–4.
- **Baris 206** — Mencetak nama class dan MRO-nya. Format `{kelas.__name__:<12}` artinya rata kiri dengan lebar 12 karakter, sehingga tanda `:` tersusun lurus. MRO yang menarik: `EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object` (mixin dicari lebih dulu daripada Buku) dan `AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object` (diamond: `Anggota` hanya muncul **sekali** dan setelah kedua induk, berkat algoritma C3 linearization).

## Baris 207–213: Fungsi `main()`

```python
207 |
208 |
209 | def main():
210 |     try:
211 |         MenuPerpustakaan(buat_data_contoh()).jalankan()
212 |     except (KeyboardInterrupt, EOFError):
213 |         print("\nProgram dihentikan.")
```

- **Baris 207–208** — Dua baris kosong pemisah antara class dan fungsi tingkat modul.
- **Baris 209** — Fungsi `main()` sebagai pintu masuk program.
- **Baris 210** — Membuka `try` yang membungkus seluruh jalannya program.
- **Baris 211** — Satu baris melakukan tiga hal (dari dalam ke luar): `buat_data_contoh()` membuat objek `Perpustakaan` berisi data awal → objek itu dikirim ke konstruktor `MenuPerpustakaan(...)` → method `.jalankan()` langsung dipanggil pada objek menu baru (tanpa disimpan ke variabel).
- **Baris 212** — Menangkap dua exception khusus: `KeyboardInterrupt` (pengguna menekan **Ctrl+C**) dan `EOFError` (input habis, mis. menekan **Ctrl+Z/Ctrl+D**, atau saat input dikirim lewat *pipe* dan barisnya habis). Tanpa ini, program akan berhenti dengan *traceback* panjang yang membingungkan.
- **Baris 213** — Mencetak pesan rapi lalu program selesai dengan normal.

## Baris 214–217: `if __name__ == "__main__"`

```python
214 |
215 |
216 | if __name__ == "__main__":
217 |     main()
```

- **Baris 214–215** — Dua baris kosong pemisah.
- **Baris 216** — Setiap modul Python punya variabel `__name__`. Jika file dijalankan langsung (`python main.py`), nilainya `"__main__"`; jika file di-*import* oleh file lain (mis. `import main` di test), nilainya `"main"`. Kondisi ini memastikan menu **hanya** berjalan saat file dijalankan langsung, bukan saat diimpor.
- **Baris 217** — Memanggil `main()` untuk memulai program.

## Contoh Sesi Program

Contoh nyata (diambil dari menjalankan program; teks setelah `Pilih:`/pertanyaan adalah input pengguna). **Tambah buku lalu pinjam**:

```text
===== PERPUSTAKAAN KAMPUS =====
1. Kelola koleksi
2. Kelola anggota
3. Pinjam koleksi
4. Kembalikan koleksi
5. Bayar denda
6. Laporan
0. Keluar
Pilih: 1

===== KOLEKSI =====
1. Lihat semua
2. Tambah
3. Cari
4. Ubah
5. Hapus
0. Kembali
Pilih: 2
Jenis (1 Buku, 2 Majalah, 3 E-Book, 4 Referensi): 1
Kode: B010
Judul: Clean Code
Tahun: 2008
Penulis: Robert C. Martin
Penerbit: Prentice Hall
Stok [1]: 2
Ditambahkan: B010 | Buku      | Clean Code (2008) | Stok: 2 | Penulis: Robert C. Martin | Penerbit: Prentice Hall

===== KOLEKSI =====
...
Pilih: 0

===== PERPUSTAKAAN KAMPUS =====
...
Pilih: 3
ID anggota: MHS002
Kode koleksi: B010
Tanggal pinjam (YYYY-MM-DD, kosong = hari ini): 2026-11-09
Berhasil: P0001 | Fajar (MHS002) | Clean Code (B010) | Pinjam: 2026-11-09 | Tempo: 2026-11-16 | Dipinjam
```

**Peminjaman ditolak** (exception `PeminjamanDitolak` ditangkap `jalankan_aksi()`):

```text
Pilih: 3
ID anggota: MHS002
Kode koleksi: R001
Tanggal pinjam (YYYY-MM-DD, kosong = hari ini):
[GAGAL] Referensi 'Kamus Besar Bahasa Indonesia' hanya baca di tempat
```

**Ubah data Asisten Dosen** (mendapat `prodi` dan `bidang`; email salah ditolak setter, atribut lain tetap diproses):

```text
Pilih: 4
ID: ASD001
Nama [Rizky Pratama]:
Telepon []:
Email []: rizky-salah
[GAGAL] email: Format email tidak valid: rizky-salah
Prodi [Informatika]:
Bidang [Praktikum PBO]: Asisten Praktikum PBO
Data diperbarui: ASD001 | Asisten Dosen | Rizky Pratama | Prodi: Informatika | Bidang: Asisten Praktikum PBO | Maks 3 buku/14 hari | Denda: Rp0
```

**Laporan → 6. Struktur class & MRO**:

```text
Pilih: 6

--- MRO (urutan pencarian method) ---
Koleksi     : Koleksi -> ABC -> object
Buku        : Buku -> Koleksi -> ABC -> object
Majalah     : Majalah -> Koleksi -> ABC -> object
Referensi   : Referensi -> Buku -> Koleksi -> ABC -> object
EBook       : EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object
Anggota     : Anggota -> ABC -> object
Mahasiswa   : Mahasiswa -> Anggota -> ABC -> object
Dosen       : Dosen -> Anggota -> ABC -> object
Umum        : Umum -> Anggota -> ABC -> object
AsistenDosen: AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object
```

Pilihan tidak dikenal dan input yang habis/Ctrl+C:

```text
Pilih: 9
Pilihan tidak tersedia.
...
Pilih:
Program dihentikan.
```

## Pertanyaan yang Mungkin Ditanyakan Dosen

1. **Mengapa `try/except` hanya ada di `jalankan_aksi()`, bukan di setiap method?**
   Karena semua aksi menu dijalankan lewat `jalankan_aksi()`. Error dari mana pun (setter, `Perpustakaan`, `int()`) "naik" ke pemanggil sampai tertangkap di sana. Jadi penanganan error terpusat dan kode method lain tetap bersih.
2. **Kenapa cukup `except PerpustakaanError`, padahal yang dilempar `PeminjamanDitolak` dll.?**
   Karena `except` menangkap class yang disebut **beserta semua subclass-nya**. `DataTidakDitemukan`, `DataDuplikat`, dan `PeminjamanDitolak` adalah turunan `PerpustakaanError`.
3. **Apa bedanya `self.tambah_koleksi` dan `lambda: cetak_daftar(...)` di list opsi?**
   Keduanya sama-sama *fungsi yang belum dipanggil*. `self.tambah_koleksi` tidak butuh argumen, jadi cukup referensinya. `cetak_daftar` butuh argumen, sehingga dibungkus `lambda` agar pemanggilannya ditunda sampai opsi dipilih.
4. **Mengapa `ubah_data()` memakai `setattr`, bukan langsung mengubah `_judul`?**
   `setattr(objek, "judul", nilai)` setara `objek.judul = nilai`, yang memicu **property setter**, sehingga validasi & konversi tipe di class model tetap berjalan. Mengubah `_judul` langsung akan melewati validasi dan melanggar enkapsulasi.
5. **Bagaimana `AsistenDosen` bisa mendapat atribut `prodi` dan `bidang` saat diubah?**
   `AsistenDosen(Mahasiswa, Dosen)` adalah turunan keduanya, jadi `isinstance` terhadap `Mahasiswa` dan `Dosen` sama-sama `True`, dan karena dipakai dua `if` terpisah (bukan `elif`), kedua atribut ditambahkan.
6. **Di mana letak polymorphism pada file ini?**
   `cetak_daftar()` dan `ubah_data()` memanggil `ringkasan()` tanpa tahu class objeknya; tiap class (Buku, Majalah, EBook, Mahasiswa, Peminjaman, …) punya versinya sendiri. Juga `perpus.tambah_koleksi()` menerima objek jenis koleksi apa pun.
7. **Apa fungsi `if __name__ == "__main__":`?**
   Agar `main()` hanya berjalan saat file dieksekusi langsung, bukan saat file di-*import* (misalnya oleh file test), sehingga import tidak memicu menu interaktif.
8. **Kenapa `tanya()` selalu mengembalikan string, padahal tahun/stok angka?**
   Konversi dan validasi tipe adalah tanggung jawab class model (setter `tahun`, `stok`, `ukuran_mb` mengubah string ke angka dan menolak nilai tidak valid). UI cukup mengumpulkan teks; aturan tetap di satu tempat.

## Ringkasan

- `main.py` adalah **UI console** dan **titik masuk**; seluruh aturan bisnis ada di file 1–6.
- Fungsi bantu: `tanya()` (input + nilai bawaan), `tanya_tanggal()` (teks → `date`), `cetak_daftar()` (cetak list via `ringkasan()` – polymorphism), `teks_mro()` (menampilkan `__mro__`).
- `MenuPerpustakaan` menyimpan objek `Perpustakaan` di `self.perpus` dan meneruskan semua pekerjaan ke sana.
- `tampilkan_menu()` adalah menu generik: opsi berisi **fungsi sebagai nilai**/`lambda`, dipilih lewat **dict comprehension** + `.get()`.
- `jalankan_aksi()` memusatkan penanganan error: `PerpustakaanError` (dan turunannya), `ValueError`, `TypeError` → `[GAGAL] ...`, program tetap berjalan.
- `ubah_data()` memakai `getattr`/`setattr` sehingga **property setter** (validasi) tetap dijalankan.
- `isinstance` memilih atribut yang bisa diubah; `EBook` lolos cek `Buku` & `EBook`, `AsistenDosen` lolos cek `Mahasiswa` & `Dosen`.
- `struktur_kelas()` menampilkan MRO, memperlihatkan multiple inheritance (`EBook`) dan diamond (`AsistenDosen`).
- `main()` menangani `KeyboardInterrupt`/`EOFError`; `if __name__ == "__main__"` mencegah program berjalan saat diimpor.
