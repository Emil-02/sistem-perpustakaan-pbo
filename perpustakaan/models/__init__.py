from .koleksi import Koleksi, Buku, Majalah, Referensi, koleksi_dari_dict
from .anggota import Anggota, Mahasiswa, Dosen, Umum, anggota_dari_dict
from .peminjaman import Peminjaman

__all__ = [
    "Koleksi", "Buku", "Majalah", "Referensi", "koleksi_dari_dict",
    "Anggota", "Mahasiswa", "Dosen", "Umum", "anggota_dari_dict",
    "Peminjaman",
]
