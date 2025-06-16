import os
import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta

# Ensure 'scripts/' is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def train_lstm(look_back=7, forecast_days=30):
    df = pd.read_csv('data/processed/train.csv', parse_dates=['date'])

    output_dir = 'data/forecast'
    os.makedirs(output_dir, exist_ok=True)

    results = []

    for region in df['region'].unique():
        region_df = df[df['region'] == region].sort_values('date')
        series = region_df['total_claims'].values.reshape(-1, 1)

        scaler = MinMaxScaler()
        scaled_series = scaler.fit_transform(series)

        X, y = [], []
        for i in range(look_back, len(scaled_series)):
            X.append(scaled_series[i - look_back:i])
            y.append(scaled_series[i])
        X, y = np.array(X), np.array(y)

        if len(X) == 0:
            print(f"⚠️ Not enough data for region {region}")
            continue

        model = Sequential([
            LSTM(50, activation='relu', input_shape=(look_back, 1)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=20, verbose=0)

        # Forecasting
        last_sequence = scaled_series[-look_back:]
        preds = []
        current_input = last_sequence

        for _ in range(forecast_days):
            pred = model.predict(current_input.reshape(1, look_back, 1), verbose=0)
            preds.append(pred[0][0])
            current_input = np.append(current_input[1:], [[pred[0][0]]], axis=0)

        forecast = scaler.inverse_transform(np.array(preds).reshape(-1, 1)).flatten()
        last_date = region_df['date'].max()
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

        for date, yhat in zip(forecast_dates, forecast):
            results.append({
                'date': date,
                'region': region,
                'forecast_total_claims': yhat
            })

    forecast_df = pd.DataFrame(results)
    forecast_df.to_csv(os.path.join(output_dir, 'lstm_forecasts.csv'), index=False)
    print(f"LSTM forecasts saved to: {output_dir}/lstm_forecasts.csv")

# Safe CLI entry
if __name__ == "__main__":
    train_lstm()
