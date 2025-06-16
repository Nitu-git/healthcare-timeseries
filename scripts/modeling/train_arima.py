import os
import sys
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta

# Make 'scripts/' importable inside Airflow container
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def train_arima(forecast_days=30):
    # Load training data
    input_path = 'data/processed/train.csv'
    df = pd.read_csv(input_path, parse_dates=['date'])

    # Output directory
    output_dir = 'data/forecast'
    os.makedirs(output_dir, exist_ok=True)

    # Prepare storage for all forecasts
    all_forecasts = []

    # Iterate through regions
    for region in df['region'].unique():
        region_df = df[df['region'] == region].sort_values('date')
        ts = region_df['total_claims']

        try:
            # Fit ARIMA (p=1, d=1, q=1 for now — can be optimized later)
            model = ARIMA(ts, order=(1, 1, 1))
            model_fit = model.fit()

            # Forecast
            forecast = model_fit.forecast(steps=forecast_days)
            last_date = region_df['date'].max()
            forecast_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

            # Save forecast
            for date, yhat in zip(forecast_dates, forecast):
                all_forecasts.append({
                    'date': date,
                    'region': region,
                    'forecast_total_claims': yhat
                })
        except Exception as e:
            print(f"⚠️ ARIMA failed for region {region}: {e}")

    # Convert to DataFrame and save
    forecast_df = pd.DataFrame(all_forecasts)
    forecast_df.to_csv(os.path.join(output_dir, 'arima_forecasts.csv'), index=False)
    print(f"✅ ARIMA forecasts saved to: {output_dir}/arima_forecasts.csv")

# Safe CLI / Airflow entry
if __name__ == "__main__":
    train_arima()
