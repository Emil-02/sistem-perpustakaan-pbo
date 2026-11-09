"""Class Perpustakaan: pusat logika sistem (relasi has-a / composition)."""

from datetime import date

from .exceptions import DataDuplikat, DataTidakDitemukan, PeminjamanDitolak
from .models import Anggota, Koleksi, Peminjaman
from .utils import rupiah


class Perpustakaan:
    """Perpustakaan MEMILIKI koleksi, anggota, dan peminjaman (bukan turunannya)."""

    def __init__(self, nama="Perpustakaan Kampus"):
        self.nama = nama
        self._koleksi = {}  # kode -> Koleksi
        self._anggota = {}  # id -> Anggota
        self._peminjaman = []  # list Peminjaman
        self._nomor_pinjam = 0

    # ===================== KOLEKSI =====================
    def tambah_koleksi(self, koleksi):
        if not isinstance(koleksi, Koleksi):
            raise TypeError("Objek harus turunan Koleksi")
        if koleksi.kode in self._koleksi:
            raise DataDuplikat(f"Kode koleksi {koleksi.kode} sudah terdaftar")
        self._koleksi[koleksi.kode] = koleksi
        return koleksi

    def cari_koleksi(self, kode):
        kode = str(kode).strip().upper()
        if kode not in self._koleksi:
            raise DataTidakDitemukan(f"Koleksi dengan kode {kode} tidak ditemukan")
        return self._koleksi[kode]

    def cari_koleksi_kata(self, kata):
        """Cari berdasarkan kode, judul, atau penulis (tidak peka huruf besar)."""
        kata = kata.strip().lower()
        hasil = []
        for k in self._koleksi.values():
            teks = f"{k.kode} {k.judul} {getattr(k, 'penulis', '')}".lower()
            if kata in teks:
                hasil.append(k)
        return hasil

    def ubah_koleksi(self, kode, /, **perubahan):
        koleksi = self.cari_koleksi(kode)
        self._ubah_atribut(koleksi, perubahan, terlarang=("kode",))
        return koleksi

    def hapus_koleksi(self, kode):
        koleksi = self.cari_koleksi(kode)
        if any(p.aktif and p.koleksi is koleksi for p in self._peminjaman):
            raise PeminjamanDitolak(f"'{koleksi.judul}' masih dipinjam, tidak dapat dihapus")
        return self._koleksi.pop(koleksi.kode)

    def daftar_koleksi(self):
        return list(self._koleksi.values())

    # ===================== ANGGOTA =====================
    def tambah_anggota(self, anggota):
        if not isinstance(anggota, Anggota):
            raise TypeError("Objek harus turunan Anggota")
        if anggota.id in self._anggota:
            raise DataDuplikat(f"ID anggota {anggota.id} sudah terdaftar")
        self._anggota[anggota.id] = anggota
        return anggota

    def cari_anggota(self, id_anggota):
        id_anggota = str(id_anggota).strip().upper()
        if id_anggota not in self._anggota:
            raise DataTidakDitemukan(f"Anggota dengan ID {id_anggota} tidak ditemukan")
        return self._anggota[id_anggota]

    def cari_anggota_kata(self, kata):
        kata = kata.strip().lower()
        return [
            a for a in self._anggota.values()
            if kata in f"{a.id} {a.nama}".lower()
        ]

    def ubah_anggota(self, id_anggota, /, **perubahan):
        anggota = self.cari_anggota(id_anggota)
        self._ubah_atribut(anggota, perubahan, terlarang=("id", "total_denda"))
        return anggota

    def hapus_anggota(self, id_anggota):
        anggota = self.cari_anggota(id_anggota)
        if self.pinjaman_aktif(anggota):
            raise PeminjamanDitolak(f"{anggota.nama} masih memiliki pinjaman aktif")
        if anggota.total_denda > 0:
            raise PeminjamanDitolak(
                f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}"
            )
        return self._anggota.pop(anggota.id)

    def daftar_anggota(self):
        return list(self._anggota.values())

    # ===================== TRANSAKSI =====================
    def pinjaman_aktif(self, anggota=None):
        return [
            p for p in self._peminjaman
            if p.aktif and (anggota is None or p.anggota is anggota)
        ]

    def _id_pinjam_baru(self):
        self._nomor_pinjam += 1
        return f"P{self._nomor_pinjam:04d}"

    def pinjam(self, id_anggota, kode_koleksi, tanggal=None):
        tanggal = tanggal or date.today()
        anggota = self.cari_anggota(id_anggota)
        koleksi = self.cari_koleksi(kode_koleksi)

        if not koleksi.bisa_dipinjam():
            if koleksi.stok > 0:
                raise PeminjamanDitolak(
                    f"{koleksi.jenis()} '{koleksi.judul}' tidak dapat dipinjam (baca di tempat)"
                )
            raise PeminjamanDitolak(f"Stok '{koleksi.judul}' sedang habis")
        if anggota.total_denda > 0:
            raise PeminjamanDitolak(
                f"{anggota.nama} masih memiliki denda {rupiah(anggota.total_denda)}"
            )
        aktif = self.pinjaman_aktif(anggota)
        if any(p.terlambat(tanggal) for p in aktif):
            raise PeminjamanDitolak(f"{anggota.nama} memiliki pinjaman yang terlambat")
        if len(aktif) >= anggota.MAKS_PINJAM:
            raise PeminjamanDitolak(
                f"{anggota.jenis()} hanya boleh meminjam maksimal {anggota.MAKS_PINJAM} koleksi"
            )
        if any(p.koleksi is koleksi for p in aktif):
            raise PeminjamanDitolak(f"{anggota.nama} sedang meminjam '{koleksi.judul}'")

        koleksi.kurangi_stok()
        transaksi = Peminjaman(self._id_pinjam_baru(), anggota, koleksi, tanggal)
        self._peminjaman.append(transaksi)
        return transaksi

    def cari_peminjaman(self, id_pinjam):
        id_pinjam = str(id_pinjam).strip().upper()
        for p in self._peminjaman:
            if p.id == id_pinjam:
                return p
        raise DataTidakDitemukan(f"Peminjaman {id_pinjam} tidak ditemukan")

    def kembalikan(self, id_pinjam, tanggal=None):
        transaksi = self.cari_peminjaman(id_pinjam)
        if not transaksi.aktif:
            raise PeminjamanDitolak(f"Peminjaman {transaksi.id} sudah dikembalikan")
        denda = transaksi.kembalikan(tanggal)
        transaksi.koleksi.tambah_stok()
        if denda:
            transaksi.anggota.tambah_denda(denda)
        return transaksi

    def bayar_denda(self, id_anggota, jumlah):
        anggota = self.cari_anggota(id_anggota)
        if anggota.total_denda == 0:
            raise PeminjamanDitolak(f"{anggota.nama} tidak memiliki denda")
        return anggota.bayar_denda(jumlah)

    # ===================== LAPORAN =====================
    def daftar_peminjaman(self):
        return list(self._peminjaman)

    def pinjaman_terlambat(self, tanggal=None):
        return [p for p in self.pinjaman_aktif() if p.terlambat(tanggal)]

    def total_denda_tertunggak(self):
        return sum(a.total_denda for a in self._anggota.values())

    def total_denda_tercatat(self):
        return sum(p.denda for p in self._peminjaman)

    def laporan(self, tanggal=None):
        """Laporan ringkas; ringkasan() dipanggil secara polimorfik."""
        baris = [f"=== LAPORAN {self.nama.upper()} ===", "", "-- Koleksi --"]
        baris += [k.ringkasan() for k in self._koleksi.values()] or ["(kosong)"]
        baris += ["", "-- Anggota --"]
        baris += [a.ringkasan() for a in self._anggota.values()] or ["(kosong)"]
        baris += ["", "-- Peminjaman Aktif --"]
        baris += [p.ringkasan(tanggal) for p in self.pinjaman_aktif()] or ["(tidak ada)"]
        baris += [
            "",
            f"Jumlah koleksi          : {len(self._koleksi)} judul "
            f"({sum(k.stok for k in self._koleksi.values())} eksemplar tersedia)",
            f"Jumlah anggota          : {len(self._anggota)}",
            f"Peminjaman aktif        : {len(self.pinjaman_aktif())}",
            f"Peminjaman terlambat    : {len(self.pinjaman_terlambat(tanggal))}",
            f"Total denda tercatat    : {rupiah(self.total_denda_tercatat())}",
            f"Total denda tertunggak  : {rupiah(self.total_denda_tertunggak())}",
        ]
        return "\n".join(baris)

    # ===================== BANTUAN INTERNAL =====================
    @staticmethod
    def _ubah_atribut(objek, perubahan, terlarang):
        """Ubah beberapa atribut sekaligus; jika satu gagal validasi, semua dibatalkan."""
        for atribut in perubahan:
            if (atribut in terlarang or atribut.startswith("_")
                    or not hasattr(objek, atribut) or callable(getattr(objek, atribut))):
                raise ValueError(f"Atribut '{atribut}' tidak dapat diubah")
        lama = {atribut: getattr(objek, atribut) for atribut in perubahan}
        try:
            for atribut, nilai in perubahan.items():
                setattr(objek, atribut, nilai)
        except (ValueError, TypeError):
            for atribut, nilai in lama.items():
                setattr(objek, atribut, nilai)
            raise

    def _pulihkan_peminjaman(self, transaksi):
        """Dipakai oleh PenyimpananJSON saat memuat data (tanpa mengubah stok)."""
        self._peminjaman.append(transaksi)
        nomor = int(transaksi.id.lstrip("P") or 0)
        self._nomor_pinjam = max(self._nomor_pinjam, nomor)
