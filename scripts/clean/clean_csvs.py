import os
import pandas as pd

# These paths are from the container's perspective
RAW_DIR = "/opt/airflow/data/raw"
CLEAN_DIR = "/opt/airflow/data/cleaned"

# Ensure the cleaned data directory exists
os.makedirs(CLEAN_DIR, exist_ok=True)

# Iterate through all CSV files in the raw data directory
for filename in os.listdir(RAW_DIR):
    if filename.endswith(".csv"):
        filepath = os.path.join(RAW_DIR, filename)
        df = pd.read_csv(filepath)

        # If a 'date' column exists, clean it
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
            df = df[df['date'].notna()]  # Remove invalid/missing dates
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Convert back to string format

        # Save cleaned CSV with missing values replaced by empty string
        cleaned_path = os.path.join(CLEAN_DIR, filename)
        df.to_csv(cleaned_path, index=False, na_rep='')

        print(f"Cleaned: {filename}")
