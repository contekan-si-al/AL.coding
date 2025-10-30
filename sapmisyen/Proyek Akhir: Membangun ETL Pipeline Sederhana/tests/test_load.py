from dotenv import load_dotenv
import os
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock, ANY
import pandas as pd
import datetime
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine, text
from utils.load import simpan_ke_csv, simpan_ke_postgresql, simpan_ke_googlesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
WORKSHEET_NAME = 'Sheet1'
DATABASE_URL = os.getenv('DATABASE_URL')

class TestLoad(unittest.TestCase):

    def test_simpan_ke_csv(self):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            simpan_ke_csv(df, "dummy.csv")
            mock_to_csv.assert_called_once_with("dummy.csv", index=False)

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_berhasil(self, mock_create_engine):
        df = pd.DataFrame({'col1': [1], 'col2': [2]})
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        with patch.object(df, 'to_sql') as mock_to_sql, patch('builtins.print') as mock_print:
            simpan_ke_postgresql(df, 'fashion_produk')
            
            mock_create_engine.assert_called_once_with(
                'postgresql+psycopg2://postgres:password_kamu@localhost:5432/database_kamu' #ganti kata sandi dan nama database kamu di sini
            )
            
            mock_to_sql.assert_called_once_with('fashion_produk', mock_engine, if_exists='replace', index=False)
            mock_print.assert_called_with("Data berhasil disimpan ke PostgreSQL, tabel: 'fashion_produk'")

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_gagal(self, mock_create_engine):
        df = pd.DataFrame({'col1': [1]})
        mock_create_engine.side_effect = Exception("Koneksi gagal")

        with patch('builtins.print') as mock_print:
            simpan_ke_postgresql(df, 'fashion_produk')
            printed_messages = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertTrue(any("Gagal menyimpan data ke PostgreSQL" in msg for msg in printed_messages))
    
    # tes googlesheets
    def setUp(self):
        self.data = pd.DataFrame(
            {
                "Title": ["Product X", "Product Y"],
                "Price": ["$11.99", "$17.99"],
                "Rating": ["4.5", "3.5"],
                "Colors": ["Red, Blue", "Green, Yellow"],
                "Size": ["XL, M, L", "M, S, XL"],
                "Gender": ["Women", "Men"],
                "Timestamp": [datetime.datetime.now(), datetime.datetime.now()],
            }
        )

        self.mock_creds = MagicMock(spec=Credentials)
        self.mock_service = MagicMock()
        self.mock_sheets = MagicMock()
        self.mock_values = MagicMock()
        self.mock_update = MagicMock()
        self.mock_execute = MagicMock()

        self.mock_service.spreadsheets.return_value = self.mock_sheets
        self.mock_sheets.values.return_value = self.mock_values
        self.mock_values.update.return_value = self.mock_update
        self.mock_update.execute.return_value = {"updatedCells": 14}

    @patch("utils.load.Credentials.from_service_account_file")
    @patch("utils.load.build")
    def test_berhasil_unggah(self, mock_build, mock_creds):
        """Test successful upload to Google Sheets."""
        mock_creds.return_value = self.mock_creds
        mock_build.return_value = self.mock_service

        result = simpan_ke_googlesheet(self.data, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, WORKSHEET_NAME)

        self.assertIsNotNone(result)
        self.assertEqual(result["updatedCells"], 14)
        mock_creds.assert_called_once_with(SERVICE_ACCOUNT_FILE, scopes=ANY)
        mock_build.assert_called_once_with("sheets", "v4", credentials=self.mock_creds)


if __name__ == '__main__':
    unittest.main()