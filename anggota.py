"""BAGIAN 3 - Enkapsulasi pada Anggota (public, protected, private) + Abstraction.

Isi file ini:
- rupiah()  : format angka ke Rupiah (dipakai juga oleh file lain)
- Anggota   : abstract class, induk semua jenis anggota
"""

import re
from abc import ABC, abstractmethod

from koleksi import teks_wajib


def rupiah(jumlah):
    """Contoh: 32000 -> 'Rp32.000'."""
    return "Rp" + f"{jumlah:,}".replace(",", ".")


class Anggota(ABC):
    """Aturan pinjam disimpan sebagai class attribute, nilainya diubah oleh subclass."""

    MAKS_PINJAM = 2
    LAMA_PINJAM = 7  # hari
    DENDA_PER_HARI = 1000  # rupiah
    _POLA_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, id_anggota, nama, telepon="", total_denda=0, email=""):
        self._id = teks_wajib(id_anggota, "ID anggota").upper()  # protected + read-only
        self.nama = nama
        self.telepon = telepon  # public
        self.email = email
        self.__total_denda = 0  # private: hanya diubah lewat method
        if total_denda:
            self.tambah_denda(total_denda)

    @property
    def id(self):
        return self._id

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        self._nama = teks_wajib(nilai, "Nama")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, nilai):
        """Email boleh kosong, tetapi jika diisi formatnya harus benar."""
        nilai = (nilai or "").strip()
        if nilai and not self._POLA_EMAIL.match(nilai):
            raise ValueError(f"Format email tidak valid: {nilai}")
        self._email = nilai

    @property
    def total_denda(self):
        """Read-only: denda hanya berubah lewat tambah_denda() dan bayar_denda()."""
        return self.__total_denda

    def tambah_denda(self, jumlah):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah < 0:
            raise ValueError("Jumlah denda harus bilangan bulat >= 0")
        self.__total_denda += jumlah

    def bayar_denda(self, jumlah):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah bayar harus bilangan bulat > 0")
        if jumlah > self.__total_denda:
            raise ValueError(f"Jumlah bayar melebihi denda ({rupiah(self.__total_denda)})")
        self.__total_denda -= jumlah
        return self.__total_denda

    @abstractmethod
    def jenis(self):
        """Wajib diimplementasikan oleh setiap subclass."""

    def info_tambahan(self):
        """Info khusus tiap subclass; subclass menambahkan lewat super()."""
        return [f"Email: {self.email}"] if self.email else []

    def ringkasan(self):
        teks = f"{self.id} | {self.jenis():<13} | {self.nama}"
        for info in self.info_tambahan():
            teks += f" | {info}"
        return (f"{teks} | Maks {self.MAKS_PINJAM} buku/{self.LAMA_PINJAM} hari"
                f" | Denda: {rupiah(self.total_denda)}")
