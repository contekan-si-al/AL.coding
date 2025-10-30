import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine, text

def simpan_ke_csv(df: pd.DataFrame, filename="produk.csv") -> None:
    """Menyimpan DataFrame ke file CSV lokal."""
    df.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke {filename}")

def simpan_ke_googlesheet(df: pd.DataFrame, SERVICE_ACCOUNT_FILE: str, SPREADSHEET_ID: str, WORKSHEET_NAME: str):
    """Stores a Pandas DataFrame to a Google Sheet"""
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    try:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=WORKSHEET_NAME).execute()

        sheet = service.spreadsheets()
        clean_df = df.copy()

        for col in clean_df.columns:
            clean_df[col] = clean_df[col].astype(str)

        values = clean_df.values.tolist()
        body = {"values": values}

        range_label = f"{WORKSHEET_NAME}!A1"

        result = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_label,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )

        print(f"DataFrame berhasil diunggah ke '{WORKSHEET_NAME}' di spreadsheet.")
        return result

    except FileNotFoundError:
        print(f"Error: Service account file '{SERVICE_ACCOUNT_FILE}' not found.")
        return None
    
    except HttpError as error:
        print(f"An HTTP error occurred: {error}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def simpan_ke_postgresql(df: pd.DataFrame, nama_tabel='fashion_produk') -> None:
    """Menyimpan DataFrame ke database PostgreSQL."""

    try:
        # Konfigurasi koneksi database (ubah sesuai kebutuhanmu)
        username = 'postgres'
        password = 'kata_sandi' #ganti dengan sandi kamu
        host = 'localhost'
        port = '5432'
        database = 'nama_database' #ganti dengan nama database kamu

        # Buat koneksi engine SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        # Simpan DataFrame ke tabel PostgreSQL (replace = ganti tabel jika sudah ada)
        df.to_sql(nama_tabel, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL, tabel: '{nama_tabel}'")

    except Exception as error:
        print(f"Gagal menyimpan data ke PostgreSQL: {error}")
