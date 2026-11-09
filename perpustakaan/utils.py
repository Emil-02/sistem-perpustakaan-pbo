"""Fungsi bantu umum."""


def rupiah(jumlah):
    """Format angka ke gaya Rupiah Indonesia, contoh: 32000 -> 'Rp32.000'."""
    return "Rp" + f"{jumlah:,}".replace(",", ".")
