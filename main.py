"""Titik masuk program Sistem Perpustakaan.

Jalankan dari folder sistem_perpustakaan:
    python main.py
"""

import os

from perpustakaan import PenyimpananJSON
from perpustakaan.menu import MenuPerpustakaan

FILE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "perpustakaan.json")


def main():
    penyimpanan = PenyimpananJSON(FILE_DATA)
    perpus = penyimpanan.muat_atau_buat()
    try:
        MenuPerpustakaan(perpus, penyimpanan).jalankan()
    except (KeyboardInterrupt, EOFError):
        penyimpanan.simpan(perpus)
        print("\nProgram dihentikan. Data tersimpan.")


if __name__ == "__main__":
    main()
