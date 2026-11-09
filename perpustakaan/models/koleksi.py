"""Model koleksi perpustakaan.

Hierarki:
    Koleksi (abstract)
    ├── Buku
    │   ├── Referensi                (multilevel: Koleksi -> Buku -> Referensi)
    │   └── EBook(DigitalMixin, Buku) (multiple inheritance dengan mixin)
    └── Majalah
"""

from abc import ABC, abstractmethod
from datetime import date


def _teks_wajib(nilai, nama_field):
    if not isinstance(nilai, str) or not nilai.strip():
        raise ValueError(f"{nama_field} tidak boleh kosong")
    return nilai.strip()


class Koleksi(ABC):
    """Abstract class: tidak bisa dibuat objeknya langsung, harus lewat subclass."""

    TAHUN_MINIMAL = 1450  # class attribute: berlaku untuk semua koleksi

    def __init__(self, kode, judul, tahun, stok=1):
        self._kode = _teks_wajib(kode, "Kode").upper()
        self._judul = ""
        self._tahun = 0
        self._stok = 0
        # Lewat setter agar validasi juga berlaku saat objek dibuat
        self.judul = judul
        self.tahun = tahun
        self.stok = stok

    # ---------- property ----------
    @property
    def kode(self):
        """Kode bersifat read-only (identitas tidak boleh diubah)."""
        return self._kode

    @property
    def judul(self):
        return self._judul

    @judul.setter
    def judul(self, nilai):
        self._judul = _teks_wajib(nilai, "Judul")

    @property
    def tahun(self):
        return self._tahun

    @tahun.setter
    def tahun(self, nilai):
        if isinstance(nilai, bool):
            raise ValueError("Tahun harus berupa angka")
        try:
            nilai = int(nilai)
        except (TypeError, ValueError):
            raise ValueError("Tahun harus berupa angka") from None
        if not self.TAHUN_MINIMAL <= nilai <= date.today().year:
            raise ValueError(
                f"Tahun harus antara {self.TAHUN_MINIMAL} dan {date.today().year}"
            )
        self._tahun = nilai

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai):
        if isinstance(nilai, bool):
            raise ValueError("Stok harus berupa angka bulat")
        try:
            nilai = int(nilai)
        except (TypeError, ValueError):
            raise ValueError("Stok harus berupa angka bulat") from None
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif")
        self._stok = nilai

    # ---------- perilaku ----------
    @abstractmethod
    def jenis(self):
        """Wajib diimplementasikan oleh setiap subclass."""

    def bisa_dipinjam(self):
        return self._stok > 0

    def kena_denda(self):
        """Apakah keterlambatan koleksi ini dikenai denda."""
        return True

    def kurangi_stok(self):
        if self._stok <= 0:
            raise ValueError(f"Stok '{self.judul}' habis")
        self._stok -= 1

    def tambah_stok(self):
        self._stok += 1

    def ringkasan(self):
        return (
            f"{self.kode} | {self.jenis():<9} | {self.judul} ({self.tahun})"
            f" | Stok: {self.stok}"
        )

    def to_dict(self):
        return {
            "tipe": type(self).__name__,
            "kode": self.kode,
            "judul": self.judul,
            "tahun": self.tahun,
            "stok": self.stok,
        }

    def __repr__(self):
        return f"{type(self).__name__}({self.kode!r}, {self.judul!r})"


class Buku(Koleksi):
    def __init__(self, kode, judul, tahun, penulis, penerbit, isbn="", stok=1):
        super().__init__(kode, judul, tahun, stok)
        self._penulis = ""
        self.penulis = penulis
        self.penerbit = penerbit
        self.isbn = isbn

    @property
    def penulis(self):
        return self._penulis

    @penulis.setter
    def penulis(self, nilai):
        self._penulis = _teks_wajib(nilai, "Penulis")

    def jenis(self):
        return "Buku"

    def ringkasan(self):
        return f"{super().ringkasan()} | Penulis: {self.penulis} | Penerbit: {self.penerbit}"

    def to_dict(self):
        data = super().to_dict()
        data.update(penulis=self.penulis, penerbit=self.penerbit, isbn=self.isbn)
        return data


class Majalah(Koleksi):
    def __init__(self, kode, judul, tahun, edisi, stok=1):
        super().__init__(kode, judul, tahun, stok)
        self._edisi = ""
        self.edisi = edisi

    @property
    def edisi(self):
        return self._edisi

    @edisi.setter
    def edisi(self, nilai):
        self._edisi = _teks_wajib(str(nilai), "Edisi")

    def jenis(self):
        return "Majalah"

    def ringkasan(self):
        return f"{super().ringkasan()} | Edisi: {self.edisi}"

    def to_dict(self):
        data = super().to_dict()
        data["edisi"] = self.edisi
        return data


class Referensi(Buku):
    """Buku referensi (kamus, ensiklopedia) hanya boleh dibaca di tempat."""

    def jenis(self):
        return "Referensi"

    def bisa_dipinjam(self):
        return False

    def ringkasan(self):
        return f"{super().ringkasan()} | Baca di tempat"


class DigitalMixin:
    """Mixin kemampuan 'digital'. Bukan koleksi sendiri, hanya menambah kemampuan.

    Method di sini memanggil super(), sehingga urutan eksekusinya ditentukan
    oleh MRO class yang memakainya (misalnya EBook -> DigitalMixin -> Buku -> Koleksi).
    """

    FORMAT_DIDUKUNG = ("PDF", "EPUB", "MOBI")

    @property
    def format_file(self):
        return self._format_file

    @format_file.setter
    def format_file(self, nilai):
        nilai = _teks_wajib(nilai, "Format file").upper()
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
        # Akses digital tidak menimbulkan denda keterlambatan
        return False

    def ringkasan(self):
        return f"{super().ringkasan()} | Digital: {self.format_file}, {self.ukuran_mb:g} MB"

    def to_dict(self):
        data = super().to_dict()
        data.update(format_file=self.format_file, ukuran_mb=self.ukuran_mb)
        return data


class EBook(DigitalMixin, Buku):
    """Multiple inheritance: EBook adalah Buku sekaligus punya kemampuan Digital.

    MRO: EBook -> DigitalMixin -> Buku -> Koleksi -> ABC -> object
    Stok pada e-book berarti jumlah lisensi yang bisa dipinjam bersamaan.
    """

    def __init__(self, kode, judul, tahun, penulis, penerbit, format_file="PDF",
                 ukuran_mb=1.0, isbn="", stok=1):
        super().__init__(kode, judul, tahun, penulis, penerbit, isbn, stok)
        self.format_file = format_file
        self.ukuran_mb = ukuran_mb

    def jenis(self):
        return "E-Book"


_TIPE_KOLEKSI = {
    "Buku": Buku, "Majalah": Majalah, "Referensi": Referensi, "EBook": EBook,
}


def koleksi_dari_dict(data):
    """Membuat ulang objek koleksi dari dict hasil to_dict()."""
    data = dict(data)
    tipe = data.pop("tipe", None)
    kelas = _TIPE_KOLEKSI.get(tipe)
    if kelas is None:
        raise ValueError(f"Tipe koleksi tidak dikenal: {tipe}")
    return kelas(**data)
