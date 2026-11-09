"""BAGIAN 1 - Class & Object, Enkapsulasi, Abstraction.

Isi file ini:
- fungsi bantu validasi teks dan angka (dipakai juga oleh file lain)
- Koleksi : abstract class (induk semua jenis koleksi)
- Buku    : turunan Koleksi
"""

from abc import ABC, abstractmethod
from datetime import date


def teks_wajib(nilai, nama_field):
    """Teks tidak boleh kosong. Mengembalikan teks tanpa spasi di awal/akhir."""
    if not isinstance(nilai, str) or not nilai.strip():
        raise ValueError(f"{nama_field} tidak boleh kosong")
    return nilai.strip()


def angka_bulat(nilai, nama_field):
    """Ubah ke int. True/False ditolak walaupun bool adalah turunan int."""
    if isinstance(nilai, bool):
        raise ValueError(f"{nama_field} harus berupa angka")
    try:
        return int(nilai)
    except (TypeError, ValueError):
        raise ValueError(f"{nama_field} harus berupa angka") from None


class Koleksi(ABC):
    """Abstract class: objeknya tidak bisa dibuat langsung, harus lewat subclass."""

    TAHUN_MINIMAL = 1450  # class attribute: berlaku untuk semua koleksi

    def __init__(self, kode, judul, tahun, stok=1):
        self._kode = teks_wajib(kode, "Kode").upper()  # protected + read-only
        # Diisi lewat setter agar validasi juga berlaku saat objek dibuat
        self.judul = judul
        self.tahun = tahun
        self.stok = stok

    # ---------- getter & setter (property) ----------
    @property
    def kode(self):
        """Read-only (tidak ada setter) karena kode adalah identitas koleksi."""
        return self._kode

    @property
    def judul(self):
        return self._judul

    @judul.setter
    def judul(self, nilai):
        self._judul = teks_wajib(nilai, "Judul")

    @property
    def tahun(self):
        return self._tahun

    @tahun.setter
    def tahun(self, nilai):
        nilai = angka_bulat(nilai, "Tahun")
        tahun_ini = date.today().year
        if not self.TAHUN_MINIMAL <= nilai <= tahun_ini:
            raise ValueError(f"Tahun harus antara {self.TAHUN_MINIMAL} dan {tahun_ini}")
        self._tahun = nilai

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai):
        nilai = angka_bulat(nilai, "Stok")
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif")
        self._stok = nilai

    # ---------- method (perilaku objek) ----------
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
        return f"{self.kode} | {self.jenis():<9} | {self.judul} ({self.tahun}) | Stok: {self.stok}"


class Buku(Koleksi):
    def __init__(self, kode, judul, tahun, penulis, penerbit, stok=1):
        super().__init__(kode, judul, tahun, stok)  # jalankan __init__ milik Koleksi
        self.penulis = penulis
        self.penerbit = penerbit  # public

    @property
    def penulis(self):
        return self._penulis

    @penulis.setter
    def penulis(self, nilai):
        self._penulis = teks_wajib(nilai, "Penulis")

    def jenis(self):
        return "Buku"

    def ringkasan(self):
        # Override: hasil ringkasan Koleksi ditambah info khusus buku
        return f"{super().ringkasan()} | Penulis: {self.penulis} | Penerbit: {self.penerbit}"
