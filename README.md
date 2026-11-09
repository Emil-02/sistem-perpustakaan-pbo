# Sistem Perpustakaan — Pemrograman Berbasis Objek (Python)

Aplikasi console perpustakaan sederhana untuk tugas mata kuliah **Pemrograman Berbasis Objek**.
Program memakai konsep *class & object*, *encapsulation*, *inheritance* (single, multilevel,
hierarchical, multiple, diamond), *MRO*, *abstraction*, dan *polymorphism*.

## Cara Menjalankan

```bash
python main.py                 # menjalankan menu
python -m unittest -v          # menjalankan unit test
```

Data contoh dibuat di memori setiap kali program dijalankan, jadi tidak ada file database.

## Struktur Folder

```
sistem-perpustakaan-pbo/
├── koleksi.py            # 1. Koleksi (abstract) + Buku
├── koleksi_turunan.py    # 2. Majalah, Referensi, DigitalMixin, EBook
├── anggota.py            # 3. Anggota (abstract) + rupiah()
├── anggota_turunan.py    # 4. Mahasiswa, Dosen, Umum, AsistenDosen
├── peminjaman.py         # 5. Exception kustom + Peminjaman
├── perpustakaan.py       # 6. Perpustakaan (composition) + data contoh
├── main.py               # 7. Menu console
└── test_perpustakaan.py  # unit test (dibagi per bagian 1–7)
```

## Pembagian Presentasi (7 Orang)

| Orang | File | Konsep yang dijelaskan |
|---|---|---|
| 1 | `koleksi.py` | Class & object, constructor, property getter/setter, protected & read-only, abstract class |
| 2 | `koleksi_turunan.py` | Single (`Majalah`), multilevel (`Referensi`), multiple/mixin (`EBook`), override, `super()` |
| 3 | `anggota.py` | Public/protected/private (`__total_denda`), validasi email, abstract method, class attribute |
| 4 | `anggota_turunan.py` | Hierarchical inheritance, diamond inheritance (`AsistenDosen`), MRO, `**kwargs` kooperatif |
| 5 | `peminjaman.py` | Inheritance pada exception, relasi *has-a*, hitung denda dengan polymorphism |
| 6 | `perpustakaan.py` | Composition, aturan bisnis peminjaman, laporan polymorphic, data contoh |
| 7 | `main.py` | Menu console, penanganan error, ubah data lewat setter, tampilan MRO |

Setiap orang juga dapat menunjukkan bagian test miliknya di `test_perpustakaan.py`.

## Hierarki Class

```
Koleksi (abstract)                     Anggota (abstract)
├── Majalah                            ├── Mahasiswa ─┐
└── Buku                               ├── Dosen ─────┴── AsistenDosen (diamond)
    ├── Referensi                      └── Umum
    └── EBook(DigitalMixin, Buku)

PerpustakaanError → DataTidakDitemukan, DataDuplikat, PeminjamanDitolak
Perpustakaan  —has-a→  Koleksi, Anggota, Peminjaman
```

MRO: `AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object`

## Aturan Peminjaman

| Jenis anggota | Maks. pinjam | Lama pinjam | Denda/hari |
|---|---|---|---|
| Mahasiswa | 3 | 7 hari | Rp1.000 |
| Dosen | 5 | 14 hari | Rp500 |
| Asisten Dosen | 3 | 14 hari | Rp1.000 |
| Umum | 2 | 7 hari | Rp2.000 |

- Referensi hanya boleh dibaca di tempat. E-Book tidak dikenai denda.
- Peminjaman ditolak jika stok habis, anggota masih punya denda atau pinjaman terlambat,
  batas pinjam sudah tercapai, atau judul yang sama sedang dipinjam.
- Koleksi/anggota tidak dapat dihapus selama masih terkait pinjaman aktif (atau denda).
