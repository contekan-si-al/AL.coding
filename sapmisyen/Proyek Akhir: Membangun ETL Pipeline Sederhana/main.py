from utils.extract import ekstrak_halaman
from utils.transform import transformasi_data
from utils.load import simpan_ke_csv, simpan_ke_postgresql, simpan_ke_googlesheet
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    """Fungsi utama untuk menjalankan proses ETL: Extract, Transform, Load."""
    base_url = 'https://fashion-studio.dicoding.dev/'
    semua_produk = []

    # Mulai scraping dari halaman utama
    print(f"Memulai scraping dari halaman utama: {base_url}")
    try:
        produk = ekstrak_halaman(base_url)
        semua_produk.extend(produk)
    except Exception as error:
        print(f"Gagal mengambil data dari halaman utama: {error}")

    # Lanjut scraping dari halaman 2 sampai 50
    for page_number in range(2, 51):
        page_url = f"{base_url}page{page_number}"
        print(f"Scraping halaman ke-{page_number}: {page_url}")
        try:
            produk = ekstrak_halaman(page_url)
            semua_produk.extend(produk)
        except Exception as error:
            print(f"Gagal mengambil data dari halaman {page_number}: {error}")

    # Jika tidak ada data yang berhasil diambil
    if not semua_produk:
        print("Tidak ada data produk yang berhasil diambil. Program dihentikan.")
        return

    # Transformasi dan membersihan data
    data_bersih = transformasi_data(semua_produk)

    # Simpan data ke file CSV
    simpan_ke_csv(data_bersih)

    try:
        # Simpan data ke Google Sheet
      SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
      SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
      if SPREADSHEET_ID is None:
        raise ValueError("SPREADSHEET_ID environment variable not set")
      WORKSHEET_NAME = 'Sheet1'

      simpan_ke_googlesheet(data_bersih, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, WORKSHEET_NAME)
      print("Data berhasil disimpan ke Google Sheets")
    except Exception as e:
      print(f"Error muncul selama proses: {e}")

    # Simpan data ke file PostgreSQL
    simpan_ke_postgresql(data_bersih)
 
    print("Proses scraping dan penyimpanan data selesai.")
    

# Menjalankan fungsi main
if __name__ == "__main__":
    main()
