import os
import sys
import pandas as pd

# Make 'scripts' importable when running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.extract.extract_claims import extract_tables

def generate_claims_features():
    # Step 1: Extract data from DB
    df, calendar = extract_tables()
    print("EXTRACTED TABLES:    ")
    print(extract_tables())
    # Step 2: Ensure datetime format
    df['date'] = pd.to_datetime(df['date'])
    calendar['date'] = pd.to_datetime(calendar['date'])

    # Step 3: Handle missing dates using all (region, date) combinations
    full_dates = pd.date_range(start=df['date'].min(), end=df['date'].max())
    all_regions = df['region'].unique()
    full_index = pd.MultiIndex.from_product([all_regions, full_dates], names=['region', 'date'])
    full_df = pd.DataFrame(index=full_index).reset_index()

    # Step 4: Merge with actual data
    df = pd.merge(full_df, df, on=['region', 'date'], how='left')

    # Step 5: Fill missing claim values
    df['total_claims'] = df['total_claims'].fillna(0)
    df['avg_processing_time'] = df['avg_processing_time'].fillna(method='ffill')
    df['avg_claim_amount'] = df['avg_claim_amount'].fillna(0)

    # Step 6: Merge calendar events (add is_holiday if missing)
    if 'holiday_flag' not in calendar.columns:
        print("⚠️ 'holiday_flag' column missing from calendar_events — adding default False.")
        calendar['holiday_flag'] = False

    df = df.merge(calendar, on='date', how='left')
    df['is_holiday'] = df['holiday_flag'].fillna(False).astype(int)
    df.drop(columns=['holiday_flag'], inplace=True)

    # Step 7: Time-based features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

    # Step 8: Lag and rolling features
    df = df.sort_values(['region', 'date'])

    for lag in [1, 7]:
        df[f'lag_{lag}'] = df.groupby('region')['total_claims'].shift(lag)

    df['rolling_avg_7'] = df.groupby('region')['total_claims'].transform(lambda x: x.rolling(7).mean())
    df['rolling_std_7'] = df.groupby('region')['total_claims'].transform(lambda x: x.rolling(7).std())

    # Step 9: Drop rows with NaNs (from lag/rolling)
    df.dropna(inplace=True)

    # Step 10: Export
    output_path = 'data/cleaned/claims_features.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Feature file saved to: {output_path}")

# CLI and Airflow compatible entry point
if __name__ == "__main__":
    generate_claims_features()
