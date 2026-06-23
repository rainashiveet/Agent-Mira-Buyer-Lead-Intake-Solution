import pandas as pd
import json
import os
from typing import List, Dict

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def load_mls_listings(self) -> pd.DataFrame:
        csv_path = os.path.join(self.data_dir, "miami_mls_listings.csv")
        xlsx_path = os.path.join(self.data_dir, "miami_mls_listings.xlsx")
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        elif os.path.exists(xlsx_path):
            df = pd.read_excel(xlsx_path)
        else:
            raise FileNotFoundError("MLS listings file not found in data/ directory")

        return self._clean_mls_data(df)

    def load_inquiries(self) -> List[Dict]:
        path = os.path.join(self.data_dir, "sample_buyer_inquiries.json")
        if not os.path.exists(path):
            raise FileNotFoundError("sample_buyer_inquiries.json not found in data/")
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _clean_mls_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Keep actionable statuses
        valid_statuses = ['Active', 'Pending', 'Active Under Contract']
        df = df[df['listing_status'].isin(valid_statuses)].copy()
        
        # Clean numerics
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
        df['sqft'] = pd.to_numeric(df['sqft'], errors='coerce')
        
        # Handle outliers (e.g., the 250M INR listing)
        df = df[(df['price'] > 50000) & (df['price'] < 50000000)]
        
        # Parse string features to list
        df['features_list'] = df['features'].apply(
            lambda x: [f.strip().lower() for f in str(x).split(';')] if pd.notna(x) else []
        )
        df['neighborhood_lower'] = df['neighborhood'].str.lower().str.strip()
        
        return df.reset_index(drop=True)