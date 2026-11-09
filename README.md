# Sistem Perpustakaan – Tugas Kelompok PBO

Mata kuliah **Pemrograman Berorientasi Objek**, dosen **Ir. Ida, S.Kom., M.T.**

Aplikasi console (menu interaktif) untuk mengelola koleksi, anggota, peminjaman,
pengembalian, dan denda perpustakaan. Program ini dibuat untuk menerapkan materi
**Class & Object, Enkapsulasi, Inheritance, Polymorphism, dan Composition**.
Seluruh kode hanya memakai *standard library* Python 3, jadi tidak ada yang perlu diinstal.

## Cara Menjalankan

```bash
cd sistem_perpustakaan
python main.py                 # jalankan aplikasi
python -m unittest -v          # jalankan semua unit test
```

Data disimpan otomatis ke `data/perpustakaan.json`. Jika file tersebut dihapus,
program akan membuat ulang data contoh saat dijalankan.

## Struktur Folder

```
sistem_perpustakaan/
├── main.py                  # titik masuk program
├── perpustakaan/
│   ├── exceptions.py        # PerpustakaanError → DataTidakDitemukan, DataDuplikat, PeminjamanDitolak
│   ├── models/
│   │   ├── koleksi.py       # Koleksi → Buku → Referensi, Koleksi → Majalah
│   │   ├── anggota.py       # Anggota → Mahasiswa, Dosen, Umum
│   │   └── peminjaman.py    # transaksi pinjam + hitung denda
│   ├── sistem.py            # Perpustakaan (composition / has-a)
│   ├── penyimpanan.py       # simpan/muat JSON + data contoh
│   ├── menu.py              # tampilan menu console
│   └── utils.py             # format Rupiah
├── data/perpustakaan.json
└── tests/                   # unit test (unittest)
```

## Diagram Kelas

```
                 Koleksi                                   Anggota
  _kode (read-only), _judul, _tahun, _stok     _id (read-only), _nama, telepon, __total_denda
  jenis(), bisa_dipinjam(), ringkasan()        MAKS_PINJAM, LAMA_PINJAM, DENDA_PER_HARI
         ▲                    ▲                jenis(), ringkasan(), tambah_denda(), bayar_denda()
       Buku                Majalah                 ▲              ▲              ▲
  penulis, penerbit,        edisi              Mahasiswa        Dosen          Umum
  isbn                                          prodi           bidang
         ▲                                     3 buku/7 hari   5 buku/14 hari  2 buku/7 hari
     Referensi                                 Rp1.000/hari    Rp500/hari      Rp2.000/hari
  bisa_dipinjam() → False

  Peminjaman ── anggota: Anggota, koleksi: Koleksi
     tanggal_pinjam, jatuh_tempo, tanggal_kembali, denda
     terlambat(), hitung_denda(), kembalikan()

  Perpustakaan ◆── {kode: Koleksi}  ◆── {id: Anggota}  ◆── [Peminjaman]
  PenyimpananJSON ── simpan(perpus) / muat() → Perpustakaan
```

## Penerapan Konsep PBO

| Konsep (materi) | Penerapan di program |
|---|---|
| **Class & Object** (Pert. 1–2) | Setiap buku/anggota/transaksi adalah objek terpisah yang dibuat dari class. `__init__` mengisi atribut, method seperti `ringkasan()` dan `kembalikan()` menjadi perilaku objek. |
| **Instance vs class attribute** | `MAKS_PINJAM`, `LAMA_PINJAM`, `DENDA_PER_HARI`, `TAHUN_MINIMAL` adalah *class attribute* yang berlaku untuk semua objek dari class tersebut. `nama`, `judul`, `stok` adalah *instance attribute*. |
| **Enkapsulasi: public / protected / private** (Materi 3–4) | `telepon`, `penerbit` → public. `_judul`, `_stok`, `_kode` → protected (diakses lewat property). `__total_denda` → private (name mangling `_Anggota__total_denda`), hanya bisa diubah lewat `tambah_denda()` / `bayar_denda()`. |
| **Getter & setter `@property`** | Judul/nama/penulis tidak boleh kosong, tahun harus 1450 sampai tahun sekarang, stok tidak boleh negatif. Validasi juga berjalan di `__init__`. `kode`, `id`, dan `total_denda` bersifat **read-only** (tanpa setter). |
| **Exception** | Model melempar `ValueError` atau exception kustom, lalu `menu.py` menangkap dan menampilkan pesannya tanpa menghentikan program. |
| **Inheritance & `super()`** (Pert. 5–6) | `Buku(Koleksi)`, `Majalah(Koleksi)`, `Referensi(Buku)` (*multilevel*), `Mahasiswa/Dosen/Umum(Anggota)` (*hierarchical*). Exception kustom juga diturunkan dari `PerpustakaanError`. |
| **Method overriding** | `jenis()`, `ringkasan()` (memakai `super().ringkasan()`), `bisa_dipinjam()` di `Referensi`, dan `to_dict()`. |
| **Polymorphism** | Laporan memanggil `ringkasan()` pada semua objek tanpa memeriksa tipenya. Lama pinjam, batas pinjam, dan tarif denda otomatis berbeda sesuai jenis anggota. |
| **Composition / has-a** (Pert. 7) | `Perpustakaan` **memiliki** koleksi, anggota, dan peminjaman, tetapi **bukan** turunan dari class-class tersebut. `Peminjaman` memiliki referensi ke `Anggota` dan `Koleksi`. |
| **Unit test** | 40 test di folder `tests/` mencakup validasi, inheritance, aturan pinjam, denda, dan simpan/muat JSON. |

### is-a vs has-a
- **is-a (inheritance):** Mahasiswa *adalah* Anggota, Buku *adalah* Koleksi, Referensi *adalah* Buku.
- **has-a (composition):** Perpustakaan *memiliki* daftar Koleksi dan Anggota, sedangkan Peminjaman *memiliki* satu Anggota dan satu Koleksi.
  Perpustakaan tidak dibuat sebagai turunan Koleksi/Anggota karena Perpustakaan **bukan** jenis dari keduanya.

## Fitur & Aturan Bisnis

1. **Kelola Koleksi:** tambah (Buku/Majalah/Referensi), lihat, cari (kode/judul/penulis), ubah, dan hapus. Koleksi yang sedang dipinjam tidak bisa dihapus.
2. **Kelola Anggota:** tambah (Mahasiswa/Dosen/Umum), lihat, cari, ubah, dan hapus. Anggota yang masih meminjam atau masih punya denda tidak bisa dihapus.
3. **Pinjam:** peminjaman ditolak jika
   - stok habis atau koleksinya Referensi (baca di tempat),
   - anggota masih punya denda atau pinjaman yang terlambat,
   - jumlah pinjaman sudah mencapai batas jenis anggota,
   - judul yang sama sedang dipinjam oleh anggota tersebut.
4. **Kembalikan:** stok bertambah, denda = hari terlambat × tarif jenis anggota, lalu denda dicatat ke anggota.
5. **Bayar denda:** boleh dicicil, tetapi jumlahnya tidak boleh melebihi total denda.
6. **Laporan:** ringkasan perpustakaan, peminjaman aktif, peminjaman terlambat, riwayat, dan anggota yang punya denda.

> Tip demo: saat meminjam, isi tanggal mundur (misalnya `2026-10-01`), lalu kembalikan
> dengan tanggal hari ini untuk menunjukkan perhitungan denda keterlambatan.

## Pemetaan ke Rubrik Penilaian

| Aspek | Bobot | Bukti |
|---|---|---|
| Class & Object | 20 | `models/`, objek data contoh di `penyimpanan.py` |
| Enkapsulasi | 25 | property + validasi, `_protected`, `__total_denda` private, atribut read-only |
| Inheritance | 25 | hierarki Koleksi & Anggota, `super()`, overriding, polymorphism |
| Pengujian | 20 | `tests/` (40 test, `python -m unittest -v`) |
| Dokumentasi | 10 | README ini (diagram kelas, is-a / has-a) |
