import pandas as pd
import numpy as np
from datetime import datetime

def transformasi_data(product_data: list) -> pd.DataFrame:
    """Membersihkan dan mengubah data mentah produk ke format DataFrame yang bersih."""

    if not product_data:
        return pd.DataFrame(columns=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'])

    df = pd.DataFrame(product_data)

    # Melakukan filter data dengan Title "unknown"
    if 'Title' in df.columns:
        df = df[~df['Title'].str.lower().str.contains('unknown', na=False)]

    # Membersihkan dan mengubah kolom Price menjadi float dalam satuan IDR
    df['Price'] = df['Price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)
    df.dropna(subset=['Price'], inplace=True)
    df['Price'] = df['Price'].astype(float) * 16000

    # Membersihkan dan mengubah kolom Rating menjadi float
    df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.\d+|\d+)').replace('', np.nan)
    df.dropna(subset=['Rating'], inplace=True)
    df['Rating'] = df['Rating'].astype(float)

    # Membersihkan dan mengubah kolom Colors menjadi int64
    df['Colors'] = df['Colors'].replace(r'\D', '', regex=True).replace('', np.nan)
    df.dropna(subset=['Colors'], inplace=True)
    df['Colors'] = df['Colors'].astype('int64')

    # Menghilangkan label dari kolom Size dan Gender
    df['Size'] = df['Size'].replace(r'Size:\s*', '', regex=True)
    df['Gender'] = df['Gender'].replace(r'Gender:\s*', '', regex=True)

    # Hapus duplikat dan nilai kosong
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Mengonversi kolom Timestamp ke datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    return df  
