"""Model transaksi peminjaman (menghubungkan Anggota dan Koleksi)."""

from datetime import date, timedelta

from ..utils import rupiah


class Peminjaman:
    STATUS_DIPINJAM = "Dipinjam"
    STATUS_KEMBALI = "Dikembalikan"

    def __init__(self, id_pinjam, anggota, koleksi, tanggal_pinjam=None,
                 jatuh_tempo=None, tanggal_kembali=None, denda=0):
        self._id = id_pinjam
        self._anggota = anggota
        self._koleksi = koleksi
        self._tanggal_pinjam = tanggal_pinjam or date.today()
        # Lama pinjam mengikuti jenis anggota (polymorphism via class attribute)
        self._jatuh_tempo = jatuh_tempo or (
            self._tanggal_pinjam + timedelta(days=anggota.LAMA_PINJAM)
        )
        self._tanggal_kembali = tanggal_kembali
        self._denda = denda

    @property
    def id(self):
        return self._id

    @property
    def anggota(self):
        return self._anggota

    @property
    def koleksi(self):
        return self._koleksi

    @property
    def tanggal_pinjam(self):
        return self._tanggal_pinjam

    @property
    def jatuh_tempo(self):
        return self._jatuh_tempo

    @property
    def tanggal_kembali(self):
        return self._tanggal_kembali

    @property
    def denda(self):
        return self._denda

    @property
    def aktif(self):
        return self._tanggal_kembali is None

    @property
    def status(self):
        return self.STATUS_DIPINJAM if self.aktif else self.STATUS_KEMBALI

    def hari_terlambat(self, tanggal=None):
        acuan = self._tanggal_kembali or tanggal or date.today()
        return max(0, (acuan - self._jatuh_tempo).days)

    def terlambat(self, tanggal=None):
        return self.hari_terlambat(tanggal) > 0

    def hitung_denda(self, tanggal=None):
        return self.hari_terlambat(tanggal) * self._anggota.DENDA_PER_HARI

    def kembalikan(self, tanggal=None):
        """Menutup transaksi dan mengembalikan besar denda."""
        if not self.aktif:
            raise ValueError(f"Peminjaman {self.id} sudah dikembalikan")
        tanggal = tanggal or date.today()
        if tanggal < self._tanggal_pinjam:
            raise ValueError("Tanggal kembali tidak boleh sebelum tanggal pinjam")
        self._tanggal_kembali = tanggal
        self._denda = self.hitung_denda()
        return self._denda

    def ringkasan(self, tanggal=None):
        teks = (
            f"{self.id} | {self.anggota.nama} ({self.anggota.id}) | "
            f"{self.koleksi.judul} ({self.koleksi.kode}) | "
            f"Pinjam: {self.tanggal_pinjam} | Tempo: {self.jatuh_tempo} | "
            f"{self.status}"
        )
        if self.aktif:
            if self.terlambat(tanggal):
                teks += (
                    f" | TERLAMBAT {self.hari_terlambat(tanggal)} hari"
                    f" (denda {rupiah(self.hitung_denda(tanggal))})"
                )
        else:
            teks += f" ({self.tanggal_kembali}) | Denda: {rupiah(self.denda)}"
        return teks

    def to_dict(self):
        return {
            "id_pinjam": self.id,
            "id_anggota": self.anggota.id,
            "kode_koleksi": self.koleksi.kode,
            "tanggal_pinjam": self.tanggal_pinjam.isoformat(),
            "jatuh_tempo": self.jatuh_tempo.isoformat(),
            "tanggal_kembali": (
                self.tanggal_kembali.isoformat() if self.tanggal_kembali else None
            ),
            "denda": self.denda,
        }

    def __repr__(self):
        return f"Peminjaman({self.id!r}, {self.status!r})"
