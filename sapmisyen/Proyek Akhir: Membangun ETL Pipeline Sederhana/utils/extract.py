import requests
from bs4 import BeautifulSoup
import pandas as pd

def ekstrak_halaman(url: str) -> list:
    """Mengambil data produk dari URL halaman koleksi produk."""

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise Exception(f"Gagal mengakses URL {url}: {error}")

    

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        daftar_produk = []

        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            print(f"Tidak ada produk ditemukan di halaman {url}")
        
        # Menambahkan kolom Timestamp
        timestamp = pd.Timestamp.now()

        for card in cards:
            # Mengambil elemen produk
            title = card.find('h3', class_='product-title')
            price = card.find('div', class_='price-container')
            rating = card.find('p', string=lambda t: t and 'Rating' in t)
            colors = card.find('p', string=lambda t: t and 'Colors' in t)
            size = card.find('p', string=lambda t: t and 'Size' in t)
            gender = card.find('p', string=lambda t: t and 'Gender' in t)

            # Memasukkan data ke dictionary
            produk = {
                'Title': title.text.strip() if title else 'Unknown Title',
                'Price': price.text.strip() if price else 'Price Not Available',
                'Rating': rating.text.strip() if rating else 'No Rating',
                'Colors': colors.text.strip() if colors else 'No Color Info',
                'Size': size.text.strip() if size else 'No Size Info',
                'Gender': gender.text.strip() if gender else 'No Gender Info',
                'Timestamp': timestamp,
            }

            daftar_produk.append(produk)

        print(f"{len(daftar_produk)} produk berhasil diambil dari {url}")
        return daftar_produk

    except Exception as parse_error:
        raise Exception(f"Kesalahan saat parsing HTML: {parse_error}")
