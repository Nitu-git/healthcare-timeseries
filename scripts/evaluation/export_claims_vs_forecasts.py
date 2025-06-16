import os
import sys
import pandas as pd

# Make 'scripts/' importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

EVALUATED_DIR = "data/evaluated"

def export_claims_vs_forecasts():
    # Load actuals
    test = pd.read_csv("data/processed/test.csv", parse_dates=["date"])[["date", "region", "total_claims"]]

    # Load model forecasts
    arima = pd.read_csv("data/forecast/arima_forecasts.csv", parse_dates=["date"])
    xgb = pd.read_csv("data/forecast/xgb_forecasts.csv", parse_dates=["date"])
    lstm = pd.read_csv("data/forecast/lstm_forecasts.csv", parse_dates=["date"])

    # Rename forecast columns
    test.rename(columns={"total_claims": "actual_claim"}, inplace=True)
    arima.rename(columns={"forecast_total_claims": "arima_forecast"}, inplace=True)
    xgb.rename(columns={"forecast_total_claims": "xgb_forecast"}, inplace=True)
    lstm.rename(columns={"forecast_total_claims": "lstm_forecast"}, inplace=True)

    # Merge all into one table
    merged = test.merge(arima[["date", "region", "arima_forecast"]], on=["date", "region"], how="left")
    merged = merged.merge(xgb[["date", "region", "xgb_forecast"]], on=["date", "region"], how="left")
    merged = merged.merge(lstm[["date", "region", "lstm_forecast"]], on=["date", "region"], how="left")
    merged[["arima_forecast", "xgb_forecast", "lstm_forecast"]] = merged[["arima_forecast", "xgb_forecast", "lstm_forecast"]].round(4)
    # Save
    os.makedirs(EVALUATED_DIR, exist_ok=True)

    # Clean and export final CSV for dashboard
    merged.dropna(axis=1, how='all', inplace=True)
    merged.dropna(axis=0, how='all', inplace=True)

    merged.to_csv(os.path.join(EVALUATED_DIR, "claims_vs_forecast.csv"), index=False)
    print("Exported claims vs forecast to: data/evaluated/claims_vs_forecast.csv")

if __name__ == "__main__":
    export_claims_vs_forecast()
