docker exec -it claims_pg psql -U postgres -d claims_forecasting

docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow users create \
 --username admin \
 --firstname Admin \
 --lastname User \
 --role Admin \
 --email admin@example.com \
 --password admin

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow db init

docker-compose -f docker-compose.airflow.yml run --rm airflow-webserver airflow db migrate
