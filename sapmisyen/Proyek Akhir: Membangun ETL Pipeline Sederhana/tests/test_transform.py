import unittest
import pandas as pd
from utils.transform import transformasi_data

class TestTransform(unittest.TestCase):

    def test_transformasi_data_normal(self):
        data_input = [
            {'Title': 'Baju Keren',
             'Price': '90.00',
             'Rating': 'Rating: 4.0',
             'Colors': 'Colors: 3',
             'Size': 'Size: L',
             'Gender': 'Gender: Men',
             'Timestamp': 'Timestamp: 14:24:38.988367'},
            {'Title': 'Unknown Title',
             'Price': '40.00',
             'Rating': 'Rating: 3.9',
             'Colors': 'Colors: 2',
             'Size': 'Size: M',
             'Gender': 'Gender: Women',
             'Timestamp': 'Timestamp: 14:24:38.988367'}
        ]
        df = transformasi_data(data_input)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertNotIn('Unknown Title', df['Title'].values)
        self.assertIn('Timestamp', df.columns)
        self.assertEqual(len(df), 1)

    def test_transformasi_data_kosong(self):
        df = transformasi_data([])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 0)
        self.assertListEqual(
            list(df.columns),
            ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        )

if __name__ == '__main__':
    unittest.main()
