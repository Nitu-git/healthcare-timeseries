#!/bin/bash

echo "🔍 Checking if Airflow DB is already initialized..."

# Check if DB volume exists by trying to access a file that should only exist if DB is initialized
docker volume inspect airflow_postgres_data > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "🔧 No volume found or DB wiped. Bootstrapping metadata and user..."

  docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow db init

  docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow users create \
      --username admin \
      --firstname Admin \
      --lastname User \
      --role Admin \
      --email admin@example.com \
      --password admin
else
  echo "✅ DB volume already exists. Skipping init and user creation."
fi

echo "📦 Installing Python dependencies from requirements.txt..."
docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver pip install -r requirements.txt

echo "🚀 Starting Airflow + Postgres..."
docker-compose -f docker-compose.airflow.yml up -d --build
