import os
import sys
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Make 'scripts/' importable if running via Airflow
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def evaluate_models():
    test_df = pd.read_csv("data/processed/test.csv", parse_dates=["date"])

    # Read forecast outputs
    arima = pd.read_csv("data/forecast/arima_forecasts.csv", parse_dates=["date"])
    xgb = pd.read_csv("data/forecast/xgb_forecasts.csv", parse_dates=["date"])
    lstm = pd.read_csv("data/forecast/lstm_forecasts.csv", parse_dates=["date"])

    # Rename forecast columns for consistency
    if "forecast_total_claims" in xgb.columns:
        xgb.rename(columns={"forecast_total_claims": "xgb_forecast"}, inplace=True)
    if "forecast_total_claims" in lstm.columns:
        lstm.rename(columns={"forecast_total_claims": "lstm_forecast"}, inplace=True)

    # Merge all forecasts with test data
    merged = test_df[["date", "region", "total_claims"]].merge(
        arima[["date", "region", "forecast_total_claims"]], on=["date", "region"], how="inner"
    ).merge(
        xgb[["date", "region", "xgb_forecast"]], on=["date", "region"], how="inner"
    ).merge(
        lstm[["date", "region", "lstm_forecast"]], on=["date", "region"], how="inner"
    )

    # Compute error metrics
    def compute_metrics(true, pred):
        mae = mean_absolute_error(true, pred)
        mse = mean_squared_error(true, pred)
        rmse = mse ** 0.5  # Manual RMSE
        mape = (abs((true - pred) / true.replace(0, float("nan")))).mean() * 100
        return mae, rmse, mape

    results = []
    for region in merged["region"].unique():
        subset = merged[merged["region"] == region]
        arima_mae, arima_rmse, arima_mape = compute_metrics(subset["total_claims"], subset["forecast_total_claims"])
        xgb_mae, xgb_rmse, xgb_mape = compute_metrics(subset["total_claims"], subset["xgb_forecast"])
        lstm_mae, lstm_rmse, lstm_mape = compute_metrics(subset["total_claims"], subset["lstm_forecast"])

        results.extend([
            {"region": region, "model": "ARIMA", "MAE": arima_mae, "RMSE": arima_rmse, "MAPE (%)": arima_mape},
            {"region": region, "model": "XGBoost", "MAE": xgb_mae, "RMSE": xgb_rmse, "MAPE (%)": xgb_mape},
            {"region": region, "model": "LSTM", "MAE": lstm_mae, "RMSE": lstm_rmse, "MAPE (%)": lstm_mape},
        ])

    # Save results
    os.makedirs("data/evaluated", exist_ok=True)
    results_df = pd.DataFrame(results)
    results_df[["MAE", "RMSE", "MAPE (%)"]] = results_df[["MAE", "RMSE", "MAPE (%)"]].round(4) 
    results_df.to_csv("data/evaluated/model_comparison.csv", index=False)
    print("Evaluation saved to: data/evaluated/model_comparison.csv")

# Safe CLI entrypoint
if __name__ == "__main__":
    evaluate_models()
