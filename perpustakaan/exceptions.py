"""Exception kustom sistem perpustakaan (contoh inheritance pada exception)."""

class PerpustakaanError(Exception):
    """Induk semua error pada sistem perpustakaan."""


class DataTidakDitemukan(PerpustakaanError):
    """Kode koleksi / ID anggota / ID peminjaman tidak ada."""


class DataDuplikat(PerpustakaanError):
    """Kode atau ID yang sama sudah terdaftar."""


class PeminjamanDitolak(PerpustakaanError):
    """Aturan peminjaman/pengembalian/penghapusan dilanggar."""
