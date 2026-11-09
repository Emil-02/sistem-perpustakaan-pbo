"""Model anggota perpustakaan: Anggota (parent) -> Mahasiswa, Dosen, Umum."""

from .koleksi import _teks_wajib
from ..utils import rupiah


class Anggota:
    """Parent class anggota. Aturan pinjam diatur lewat class attribute."""

    MAKS_PINJAM = 2
    LAMA_PINJAM = 7  # hari
    DENDA_PER_HARI = 1000  # rupiah

    def __init__(self, id_anggota, nama, telepon="", total_denda=0):
        self._id = _teks_wajib(id_anggota, "ID anggota").upper()
        self._nama = ""
        self.nama = nama
        self.telepon = telepon  # public
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
        self._nama = _teks_wajib(nilai, "Nama")

    @property
    def total_denda(self):
        """Read-only: denda hanya berubah lewat tambah_denda()/bayar_denda()."""
        return self.__total_denda

    def tambah_denda(self, jumlah):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah < 0:
            raise ValueError("Jumlah denda harus bilangan bulat >= 0")
        self.__total_denda += jumlah

    def bayar_denda(self, jumlah):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah bayar harus bilangan bulat > 0")
        if jumlah > self.__total_denda:
            raise ValueError(
                f"Jumlah bayar melebihi denda ({rupiah(self.__total_denda)})"
            )
        self.__total_denda -= jumlah
        return self.__total_denda

    def jenis(self):
        return "Anggota"

    def info_tambahan(self):
        return ""

    def ringkasan(self):
        teks = f"{self.id} | {self.jenis():<9} | {self.nama}"
        tambahan = self.info_tambahan()
        if tambahan:
            teks += f" | {tambahan}"
        return (
            f"{teks} | Maks {self.MAKS_PINJAM} buku/{self.LAMA_PINJAM} hari"
            f" | Denda: {rupiah(self.total_denda)}"
        )

    def to_dict(self):
        return {
            "tipe": type(self).__name__,
            "id_anggota": self.id,
            "nama": self.nama,
            "telepon": self.telepon,
            "total_denda": self.total_denda,
        }

    def __repr__(self):
        return f"{type(self).__name__}({self.id!r}, {self.nama!r})"


class Mahasiswa(Anggota):
    MAKS_PINJAM = 3
    LAMA_PINJAM = 7
    DENDA_PER_HARI = 1000

    def __init__(self, id_anggota, nama, prodi, telepon="", total_denda=0):
        super().__init__(id_anggota, nama, telepon, total_denda)
        self._prodi = ""
        self.prodi = prodi

    @property
    def prodi(self):
        return self._prodi

    @prodi.setter
    def prodi(self, nilai):
        self._prodi = _teks_wajib(nilai, "Prodi")

    def jenis(self):
        return "Mahasiswa"

    def info_tambahan(self):
        return f"Prodi: {self.prodi}"

    def to_dict(self):
        data = super().to_dict()
        data["prodi"] = self.prodi
        return data


class Dosen(Anggota):
    MAKS_PINJAM = 5
    LAMA_PINJAM = 14
    DENDA_PER_HARI = 500

    def __init__(self, id_anggota, nama, bidang, telepon="", total_denda=0):
        super().__init__(id_anggota, nama, telepon, total_denda)
        self._bidang = ""
        self.bidang = bidang

    @property
    def bidang(self):
        return self._bidang

    @bidang.setter
    def bidang(self, nilai):
        self._bidang = _teks_wajib(nilai, "Bidang")

    def jenis(self):
        return "Dosen"

    def info_tambahan(self):
        return f"Bidang: {self.bidang}"

    def to_dict(self):
        data = super().to_dict()
        data["bidang"] = self.bidang
        return data


class Umum(Anggota):
    MAKS_PINJAM = 2
    LAMA_PINJAM = 7
    DENDA_PER_HARI = 2000

    def jenis(self):
        return "Umum"


_TIPE_ANGGOTA = {"Mahasiswa": Mahasiswa, "Dosen": Dosen, "Umum": Umum}


def anggota_dari_dict(data):
    data = dict(data)
    tipe = data.pop("tipe", None)
    kelas = _TIPE_ANGGOTA.get(tipe)
    if kelas is None:
        raise ValueError(f"Tipe anggota tidak dikenal: {tipe}")
    return kelas(**data)
