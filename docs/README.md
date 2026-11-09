# Materi Penjelasan Kode — Sistem Perpustakaan

Folder ini berisi penjelasan **baris per baris** untuk setiap file program.
Setiap presenter cukup mempelajari file materinya sendiri.

| Orang | File kode | Materi | Konsep utama |
|---|---|---|---|
| 1 | `koleksi.py` | [01_koleksi.md](01_koleksi.md) | Class & object, property, enkapsulasi, abstract class |
| 2 | `koleksi_turunan.py` | [02_koleksi_turunan.md](02_koleksi_turunan.md) | Single, multilevel, multiple inheritance (mixin), override |
| 3 | `anggota.py` | [03_anggota.md](03_anggota.md) | Public/protected/private, abstract method |
| 4 | `anggota_turunan.py` | [04_anggota_turunan.md](04_anggota_turunan.md) | Hierarchical & diamond inheritance, MRO |
| 5 | `peminjaman.py` | [05_peminjaman.md](05_peminjaman.md) | Exception kustom, relasi has-a, polymorphism |
| 6 | `perpustakaan.py` | [06_perpustakaan.md](06_perpustakaan.md) | Composition, aturan bisnis, laporan |
| 7 | `main.py` | [07_main.md](07_main.md) | Menu console, penanganan error |
| – | `test_perpustakaan.py` | [08_test_perpustakaan.md](08_test_perpustakaan.md) | Unit test tiap bagian |

## Cara Membaca Materi

1. Baca **Gambaran Umum** untuk mengetahui peran file.
2. Ikuti blok kode bernomor baris; tiap baris dijelaskan di bawah bloknya.
3. Pelajari bagian **Pertanyaan yang Mungkin Ditanyakan Dosen** sebelum presentasi.

## Urutan Presentasi yang Disarankan

`koleksi` → `koleksi_turunan` → `anggota` → `anggota_turunan` → `peminjaman` → `perpustakaan` → `main`

Urutan ini mengikuti arah import: file berikutnya memakai class dari file sebelumnya.
