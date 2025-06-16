import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def split_train_test():
    # Load engineered features
    input_path = 'data/cleaned/claims_features.csv'
    df = pd.read_csv(input_path)
    df['date'] = pd.to_datetime(df['date'])

    # Sort by region and date
    df = df.sort_values(['region', 'date'])

    # Determine 80% split point based on date
    unique_dates = df['date'].sort_values().unique()
    split_index = int(len(unique_dates) * 0.8)
    cutoff_date = unique_dates[split_index]

    # Split data
    train_df = df[df['date'] <= cutoff_date]
    test_df = df[df['date'] > cutoff_date]

    # Save outputs
    os.makedirs('data/processed', exist_ok=True)
    train_df.to_csv('data/processed/train.csv', index=False)
    test_df.to_csv('data/processed/test.csv', index=False)

    print(f"Train/Test split done.\nTrain shape: {train_df.shape}\nTest shape: {test_df.shape}")
    print("Saved to: data/processed/train.csv and test.csv")

# Safe entry for CLI / Airflow
if __name__ == "__main__":
    split_train_test()
