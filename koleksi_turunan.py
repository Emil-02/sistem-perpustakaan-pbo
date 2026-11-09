"""BAGIAN 2 - Inheritance pada koleksi (single, multilevel, multiple/mixin).

Hierarki:
    Koleksi (abstract)
    ├── Majalah                    single      : Koleksi -> Majalah
    └── Buku
        ├── Referensi              multilevel  : Koleksi -> Buku -> Referensi
        └── EBook(DigitalMixin, Buku)  multiple: punya dua induk
"""

from koleksi import Buku, Koleksi, teks_wajib


class Majalah(Koleksi):
    def __init__(self, kode, judul, tahun, edisi, stok=1):
        super().__init__(kode, judul, tahun, stok)
        self.edisi = edisi

    @property
    def edisi(self):
        return self._edisi

    @edisi.setter
    def edisi(self, nilai):
        self._edisi = teks_wajib(str(nilai), "Edisi")

    def jenis(self):
        return "Majalah"

    def ringkasan(self):
        return f"{super().ringkasan()} | Edisi: {self.edisi}"


class Referensi(Buku):
    """Buku referensi (kamus, ensiklopedia) hanya boleh dibaca di tempat."""

    def jenis(self):
        return "Referensi"

    def bisa_dipinjam(self):
        return False  # override: walaupun stok ada, tetap tidak bisa dipinjam

    def ringkasan(self):
        return f"{super().ringkasan()} | Baca di tempat"


class DigitalMixin:
    """Mixin: bukan koleksi sendiri, hanya menambah kemampuan 'digital'.

    super() di sini mengikuti MRO class pemakainya,
    misalnya EBook -> DigitalMixin -> Buku -> Koleksi.
    """

    FORMAT_DIDUKUNG = ("PDF", "EPUB", "MOBI")

    @property
    def format_file(self):
        return self._format_file

    @format_file.setter
    def format_file(self, nilai):
        nilai = teks_wajib(nilai, "Format file").upper()
        if nilai not in self.FORMAT_DIDUKUNG:
            raise ValueError(f"Format harus salah satu dari {', '.join(self.FORMAT_DIDUKUNG)}")
        self._format_file = nilai

    @property
    def ukuran_mb(self):
        return self._ukuran_mb

    @ukuran_mb.setter
    def ukuran_mb(self, nilai):
        if isinstance(nilai, bool):
            raise ValueError("Ukuran file harus berupa angka")
        try:
            nilai = float(nilai)
        except (TypeError, ValueError):
            raise ValueError("Ukuran file harus berupa angka") from None
        if nilai <= 0:
            raise ValueError("Ukuran file harus lebih dari 0 MB")
        self._ukuran_mb = nilai

    def kena_denda(self):
        return False  # akses digital tidak menimbulkan denda keterlambatan

    def ringkasan(self):
        return f"{super().ringkasan()} | Digital: {self.format_file}, {self.ukuran_mb:g} MB"


class EBook(DigitalMixin, Buku):
    """EBook adalah Buku sekaligus punya kemampuan Digital (multiple inheritance).

    MRO: EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object
    Stok e-book = jumlah lisensi yang bisa dipinjam bersamaan.
    """

    def __init__(self, kode, judul, tahun, penulis, penerbit,
                 format_file="PDF", ukuran_mb=1.0, stok=1):
        super().__init__(kode, judul, tahun, penulis, penerbit, stok)
        self.format_file = format_file
        self.ukuran_mb = ukuran_mb

    def jenis(self):
        return "E-Book"
