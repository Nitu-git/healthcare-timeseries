import os
import sys
import pandas as pd
from xgboost import XGBRegressor
from datetime import timedelta

# Make 'scripts/' importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def train_xgboost(forecast_days=30):
    df = pd.read_csv('data/processed/train.csv', parse_dates=['date'])

    features = [
        'lag_1', 'lag_7', 'rolling_avg_7', 'rolling_std_7',
        'day_of_week', 'is_weekend', 'is_holiday'
    ]
    target = 'total_claims'

    os.makedirs('data/forecast', exist_ok=True)
    all_forecasts = []

    for region in df['region'].unique():
        region_df = df[df['region'] == region].copy()
        region_df = region_df.sort_values('date')

        # Drop rows with any missing values (shouldn't happen after lag clean-up)
        region_df.dropna(subset=features + [target], inplace=True)

        X_train = region_df[features]
        y_train = region_df[target]

        model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        model.fit(X_train, y_train)

        # Start forecasting
        last_row = region_df.iloc[-1:].copy()
        for day in range(forecast_days):
            x_pred = last_row[features]
            y_pred = model.predict(x_pred)[0]

            forecast_date = pd.to_datetime(last_row['date'].values[0]) + timedelta(days=1)

            all_forecasts.append({
                'date': forecast_date,
                'region': region,
                'forecast_total_claims': y_pred
            })

            # Simulate next day input
            new_row = last_row.copy()
            new_row['date'] = forecast_date
            new_row['lag_1'] = y_pred
            new_row['lag_7'] = last_row['lag_6'].values[0] if 'lag_6' in last_row else y_pred  # crude shift
            new_row['rolling_avg_7'] = (last_row['rolling_avg_7'] * 6 + y_pred) / 7
            new_row['rolling_std_7'] = last_row['rolling_std_7']  # keep same std for simplicity
            new_row['day_of_week'] = forecast_date.dayofweek
            new_row['is_weekend'] = 1 if forecast_date.dayofweek in [5, 6] else 0
            new_row['is_holiday'] = 0  # assume no holiday in future for now

            last_row = new_row

    forecast_df = pd.DataFrame(all_forecasts)
    forecast_df.to_csv('data/forecast/xgb_forecasts.csv', index=False)
    print("XGBoost forecasts saved to: data/forecast/xgb_forecasts.csv")

if __name__ == "__main__":
    train_xgboost()
