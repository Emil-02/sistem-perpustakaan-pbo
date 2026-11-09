# Sistem Perpustakaan v2 – Tugas Kelompok PBO

Mata kuliah **Pemrograman Berorientasi Objek**, dosen **Ir. Ida, S.Kom., M.T.**

Aplikasi console (menu interaktif) untuk mengelola koleksi, anggota, peminjaman,
pengembalian, dan denda perpustakaan. Program ini dibuat untuk menerapkan materi
**Class & Object, Enkapsulasi, Abstraction, Inheritance (single, multilevel,
hierarchical, multiple, diamond + MRO), Polymorphism, dan Composition**.
Seluruh kode hanya memakai *standard library* Python 3, jadi tidak ada yang perlu diinstal.

## Cara Menjalankan

```bash
cd sistem_perpustakaan_v2      # masuk ke folder proyek
python main.py                 # jalankan aplikasi
python -m unittest -v          # jalankan semua unit test
```

Data disimpan otomatis ke `data/perpustakaan.json`. Jika file tersebut dihapus,
program akan membuat ulang data contoh saat dijalankan.

## Struktur Folder

```
sistem_perpustakaan_v2/
├── main.py                  # titik masuk program
├── perpustakaan/
│   ├── exceptions.py        # PerpustakaanError → DataTidakDitemukan, DataDuplikat, PeminjamanDitolak
│   ├── models/
│   │   ├── koleksi.py       # Koleksi (abstract) → Buku → Referensi, Majalah, EBook(DigitalMixin, Buku)
│   │   ├── anggota.py       # Anggota (abstract) → Mahasiswa, Dosen, Umum, AsistenDosen(Mahasiswa, Dosen)
│   │   └── peminjaman.py    # transaksi pinjam + hitung denda
│   ├── sistem.py            # Perpustakaan (composition / has-a)
│   ├── penyimpanan.py       # Penyimpanan (abstract) → PenyimpananJSON + data contoh
│   ├── menu.py              # tampilan menu console
│   └── utils.py             # format Rupiah, teks MRO
├── data/perpustakaan.json
└── tests/                   # unit test (unittest)
```

## Diagram Kelas

```
                    «abstract» Koleksi
       _kode (read-only), _judul, _tahun, _stok
       jenis() «abstract», bisa_dipinjam(), kena_denda(), ringkasan()
             ▲                                 ▲
           Buku                             Majalah
   penulis, penerbit, isbn                   edisi
       ▲           ▲
   Referensi      EBook ──────────▶ DigitalMixin
 bisa_dipinjam()   (multiple)       format_file, ukuran_mb
   → False                          kena_denda() → False

                    «abstract» Anggota
   _id (read-only), _nama, telepon, __total_denda (private)
   MAKS_PINJAM, LAMA_PINJAM, DENDA_PER_HARI, jenis() «abstract»
        ▲                    ▲                    ▲
    Mahasiswa              Dosen                 Umum
    prodi                  bidang
    3 buku/7 hari          5 buku/14 hari        2 buku/7 hari
    Rp1.000/hari           Rp500/hari            Rp2.000/hari
        ▲                    ▲
        └──── AsistenDosen ──┘     ← DIAMOND (Anggota di puncak)
              3 buku/14 hari, Rp1.000/hari

  Peminjaman ── anggota: Anggota, koleksi: Koleksi
  Perpustakaan ◆── {kode: Koleksi}  ◆── {id: Anggota}  ◆── [Peminjaman]
  «abstract» Penyimpanan ◀── PenyimpananJSON
```

### MRO (Method Resolution Order)
Bisa dilihat langsung di program: **Laporan → 6. Struktur kelas & MRO**.

```
Referensi    : Referensi -> Buku -> Koleksi -> ABC -> object
EBook        : EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object
AsistenDosen : AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object
```

- **EBook:** `DigitalMixin.ringkasan()` memanggil `super().ringkasan()`. Menurut MRO, pemanggilan itu
  diteruskan ke `Buku.ringkasan()` (bukan ke `object`), sehingga hasilnya berisi info buku **dan** info digital.
- **AsistenDosen (diamond):** semua `__init__` memakai `super()` dengan argumen keyword (*cooperative*),
  sehingga urutannya `Mahasiswa → Dosen → Anggota` dan `Anggota.__init__` hanya dijalankan **sekali**.
  `MAKS_PINJAM` dan `DENDA_PER_HARI` tidak ditulis ulang, jadi nilainya diambil dari **Mahasiswa** karena
  Mahasiswa berada lebih dulu di MRO. `LAMA_PINJAM` di-override menjadi 14 hari.

## Penerapan Konsep PBO

| Konsep (materi) | Penerapan di program |
|---|---|
| **Class & Object** (Pert. 1–2) | Setiap buku/anggota/transaksi adalah objek terpisah yang dibuat dari class. `__init__` mengisi atribut, method seperti `ringkasan()` dan `kembalikan()` menjadi perilaku objek. |
| **Instance vs class attribute** | `MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI`, `TAHUN_MINIMAL` adalah *class attribute* yang berlaku untuk semua objek dari class tersebut. `nama`, `judul`, `stok` adalah *instance attribute*. |
| **Enkapsulasi: public / protected / private** (Materi 3–4) | `telepon`, `penerbit` → public. `_judul`, `_stok`, `_kode` → protected (diakses lewat property). `__total_denda` → private (name mangling `_Anggota__total_denda`), hanya bisa diubah lewat `tambah_denda()` / `bayar_denda()`. |
| **Getter & setter `@property`** | Judul/nama/penulis tidak boleh kosong, tahun harus 1450 sampai tahun sekarang, stok tidak boleh negatif. Validasi juga berjalan di `__init__`. `kode`, `id`, dan `total_denda` bersifat **read-only** (tanpa setter). |
| **Abstraction** (Pert. 1) | `Koleksi`, `Anggota`, dan `Penyimpanan` adalah *abstract class* (`ABC`). Method `@abstractmethod` seperti `jenis()`, `simpan()`, dan `muat()` wajib diimplementasikan oleh subclass, dan objek abstract class tidak bisa dibuat langsung (`TypeError`). Menu hanya bergantung pada kontrak `Penyimpanan`, bukan pada detail JSON. |
| **Exception** | Model melempar `ValueError` atau exception kustom, lalu `menu.py` menangkap dan menampilkan pesannya tanpa menghentikan program. |
| **Single & hierarchical inheritance** (Pert. 5–6) | `Majalah(Koleksi)`; `Mahasiswa`, `Dosen`, dan `Umum` semuanya turunan `Anggota`. Exception kustom juga diturunkan dari `PerpustakaanError`. |
| **Multilevel inheritance** | `Koleksi → Buku → Referensi` |
| **Multiple inheritance (mixin)** | `EBook(DigitalMixin, Buku)`: EBook adalah Buku dan sekaligus punya kemampuan digital (format, ukuran file, tanpa denda). |
| **Diamond inheritance + MRO** | `AsistenDosen(Mahasiswa, Dosen)` dengan `Anggota` di puncak. `__init__` kooperatif lewat `super()`, dan class attribute dicari mengikuti MRO. |
| **Method overriding** | `jenis()`, `ringkasan()` (memakai `super().ringkasan()`), `bisa_dipinjam()` di `Referensi`, dan `to_dict()`. |
| **Polymorphism** | Laporan memanggil `ringkasan()` pada semua objek tanpa memeriksa tipenya. Lama pinjam, batas pinjam, dan tarif denda otomatis berbeda sesuai jenis anggota. `kena_denda()` membuat E-Book bebas denda. |
| **Composition / has-a** (Pert. 7) | `Perpustakaan` **memiliki** koleksi, anggota, dan peminjaman, tetapi **bukan** turunan dari class-class tersebut. `Peminjaman` memiliki referensi ke `Anggota` dan `Koleksi`. |
| **Unit test** | 56 test di folder `tests/` mencakup validasi, abstraction, multilevel, multiple, diamond/MRO, aturan pinjam, denda, dan simpan/muat JSON. |

### is-a vs has-a
- **is-a (inheritance):** Mahasiswa *adalah* Anggota, Buku *adalah* Koleksi, Referensi *adalah* Buku,
  EBook *adalah* Buku, dan AsistenDosen *adalah* Mahasiswa **dan** Dosen.
- **has-a (composition):** Perpustakaan *memiliki* daftar Koleksi dan Anggota, sedangkan Peminjaman *memiliki* satu Anggota dan satu Koleksi.
  Perpustakaan tidak dibuat sebagai turunan Koleksi/Anggota karena Perpustakaan **bukan** jenis dari keduanya.

## Fitur & Aturan Bisnis

1. **Kelola Koleksi:** tambah (Buku/Majalah/Referensi/E-Book), lihat, cari (kode/judul/penulis), ubah, dan hapus. Koleksi yang sedang dipinjam tidak bisa dihapus.
2. **Kelola Anggota:** tambah (Mahasiswa/Dosen/Umum/Asisten Dosen), lihat, cari, ubah, dan hapus. Anggota yang masih meminjam atau masih punya denda tidak bisa dihapus.
3. **Pinjam:** peminjaman ditolak jika
   - stok habis atau koleksinya Referensi (baca di tempat),
   - anggota masih punya denda atau pinjaman yang terlambat,
   - jumlah pinjaman sudah mencapai batas jenis anggota,
   - judul yang sama sedang dipinjam oleh anggota tersebut.
4. **Kembalikan:** stok bertambah, denda = hari terlambat × tarif jenis anggota, lalu denda dicatat ke anggota.
   E-Book tidak dikenai denda karena aksesnya digital.
5. **Bayar denda:** boleh dicicil, tetapi jumlahnya tidak boleh melebihi total denda.
6. **Laporan:** ringkasan perpustakaan, peminjaman aktif, peminjaman terlambat, riwayat, anggota yang punya denda, dan **struktur kelas & MRO**.

> Tip demo: saat meminjam, isi tanggal mundur (misalnya `2026-10-01`), lalu kembalikan
> dengan tanggal hari ini untuk menunjukkan perhitungan denda keterlambatan.

## Pemetaan ke Rubrik Penilaian

| Aspek | Bobot | Bukti |
|---|---|---|
| Class & Object | 20 | `models/`, objek data contoh di `penyimpanan.py` |
| Enkapsulasi & Abstraction | 25 | property + validasi, `_protected`, `__total_denda` private, read-only, abstract class |
| Inheritance | 25 | single, hierarchical, multilevel, multiple (mixin), diamond + MRO, `super()`, overriding, polymorphism |
| Pengujian | 20 | `tests/` (56 test, `python -m unittest -v`) |
| Dokumentasi | 10 | README ini (diagram kelas, is-a / has-a) |
