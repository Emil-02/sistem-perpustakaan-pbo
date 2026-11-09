r"""BAGIAN 4 - Inheritance pada anggota (hierarchical + diamond & MRO).

              Anggota (abstract)
             /       |        \
       Mahasiswa   Dosen     Umum        hierarchical
             \       /
          AsistenDosen                   diamond (multiple inheritance)

MRO AsistenDosen: AsistenDosen -> Mahasiswa -> Dosen -> Anggota -> ABC -> object
"""

from anggota import Anggota
from koleksi import teks_wajib


class Mahasiswa(Anggota):
    MAKS_PINJAM = 3
    LAMA_PINJAM = 7
    DENDA_PER_HARI = 1000

    # **kwargs + super() dengan argumen keyword membuat __init__ "kooperatif":
    # pada diamond, argumen milik Dosen (bidang) diteruskan sesuai MRO.
    def __init__(self, id_anggota, nama, prodi, telepon="", total_denda=0, **kwargs):
        super().__init__(id_anggota=id_anggota, nama=nama, telepon=telepon,
                         total_denda=total_denda, **kwargs)
        self.prodi = prodi

    @property
    def prodi(self):
        return self._prodi

    @prodi.setter
    def prodi(self, nilai):
        self._prodi = teks_wajib(nilai, "Prodi")

    def jenis(self):
        return "Mahasiswa"

    def info_tambahan(self):
        return [f"Prodi: {self.prodi}"] + super().info_tambahan()


class Dosen(Anggota):
    MAKS_PINJAM = 5
    LAMA_PINJAM = 14
    DENDA_PER_HARI = 500

    def __init__(self, id_anggota, nama, bidang, telepon="", total_denda=0, **kwargs):
        super().__init__(id_anggota=id_anggota, nama=nama, telepon=telepon,
                         total_denda=total_denda, **kwargs)
        self.bidang = bidang

    @property
    def bidang(self):
        return self._bidang

    @bidang.setter
    def bidang(self, nilai):
        self._bidang = teks_wajib(nilai, "Bidang")

    def jenis(self):
        return "Dosen"

    def info_tambahan(self):
        return [f"Bidang: {self.bidang}"] + super().info_tambahan()


class Umum(Anggota):
    MAKS_PINJAM = 2
    LAMA_PINJAM = 7
    DENDA_PER_HARI = 2000

    def jenis(self):
        return "Umum"


class AsistenDosen(Mahasiswa, Dosen):
    """Mahasiswa yang juga membantu dosen mengajar (diamond inheritance).

    - MAKS_PINJAM dan DENDA_PER_HARI tidak ditulis ulang, jadi diambil dari
      Mahasiswa karena Mahasiswa berada lebih dulu di MRO.
    - LAMA_PINJAM di-override menjadi 14 hari (hak seperti dosen).
    - Anggota.__init__ hanya dijalankan SEKALI walaupun diwarisi lewat dua jalur.
    """

    LAMA_PINJAM = 14

    def __init__(self, id_anggota, nama, prodi, bidang, telepon="", total_denda=0, email=""):
        super().__init__(id_anggota=id_anggota, nama=nama, prodi=prodi, bidang=bidang,
                         telepon=telepon, total_denda=total_denda, email=email)

    def jenis(self):
        return "Asisten Dosen"
