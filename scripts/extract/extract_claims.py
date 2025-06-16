import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Load environment variables from .env (only needed when running locally)
load_dotenv()

# Detect environment: default is LOCAL unless running inside Airflow
IS_LOCAL = os.getenv("AIRFLOW_CTX_DAG_ID") is None


# Choose connection strategy
if IS_LOCAL:
    # Use split connection parts for localhost
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "admin")
    db_host = os.getenv("DB_HOST", "postgres")  # <--- localhost for local dev
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "claims_forecasting")

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
else:
    # Use full Airflow connection URI inside Docker
    db_url = os.getenv("AIRFLOW_CONN_POSTGRES_DEFAULT")
    if db_url is None:
        raise ValueError("Missing AIRFLOW_CONN_POSTGRES_DEFAULT for Docker/Airflow context")

# Create engine
engine = create_engine(db_url)

# Extraction function
def extract_tables():
    daily_claims = pd.read_sql("SELECT * FROM daily_claims_agg ORDER BY date", engine)
    calendar_events = pd.read_sql("SELECT * FROM calendar_events", engine)
    return daily_claims, calendar_events
