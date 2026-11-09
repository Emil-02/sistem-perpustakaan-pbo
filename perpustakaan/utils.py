"""Fungsi bantu umum."""


def rupiah(jumlah):
    """Format angka ke gaya Rupiah Indonesia, contoh: 32000 -> 'Rp32.000'."""
    return "Rp" + f"{jumlah:,}".replace(",", ".")


def urutan_mro(kelas):
    """Teks MRO sebuah class, contoh: 'EBook -> DigitalMixin -> Buku -> ... -> object'."""
    return " -> ".join(k.__name__ for k in kelas.__mro__)
