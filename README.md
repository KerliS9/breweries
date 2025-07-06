# breweries

## Introduction

This repository aims to show a data search project in an API, processing through Airflow the medallion architecture.

* API: `https://api.openbrewerydb.org/v1/breweries`

## Requirements to run this project
- git
- python
- docker-compose

## How to start this project

Clone this repoh $ `git clone git@github.com:KerliS9/breweries.git`

Set your file `.env` file, like this:
```
POSTGRES_USER=your_name
POSTGRES_PASSWORD=postgres_breweries
POSTGRES_DB=breweries
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
AIRFLOW__CORE__FERNET_KEY= run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=90
AIRFLOW__WEBSERVER__SECRET_KEY= run python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Run $ `docker-compose up -d --build`. Wait the building to finished.

Check $ `docker logs airflow_init_breweries`. Line 'Database migrating done!' must be present at logs.

Run $ `chmod -R 777 ./volumes/warehouse` for Airflow to have access to read and write inside the volumes of this project.

Then open the browser with `http://localhost:8080`
```
user: admin
password: admin
```

## Project structure
```
breweries/
├── dags/
│   └── dag_breweries.py
├── src/
│   ├── Dockerfile
│   ├── fetch_api.py
│   ├── process_data.py
│   └── utils.py
│   └── elt_utils/
|      ├── schemas.py
│      └── write.py
├── unit_tests/
│   ├── fetch_api_tests.py
│   └── process_data_test.py
├── volumes/
|   └── warehouse/
|     ├── bronze
|     ├── gold
│     └── silver
├── docker-compose.yml
├── Dockerfile.airflow
├── requirements.txt
├── README.md
└── .env
```
## Decisions made

I start using Flask to see request from API. Then change to Airflow scheduler, through docker compose, to make an integrated project.

The biggest challenge was configured the docker-compose for code run correctly.

## Used technologies:

- Git
- Docker-compose
- Python
- Pyspark
- PostgreSQL
- Spark
- Airflow

## Monitoring and Alerting
In case, I want to set an alerting to my pipeline. I would add some configs to default args
```
'email': ['kerlischroeder9@gmail.com'],
'email_on_failure': True,
'email_on_retry': False,
```
And configure a valid SMTP server, adding this configs to docker-compose or `airflow.cfg` file. Password should be saved at `.env` file.
```
AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT: 587
AIRFLOW__SMTP__SMTP_USER: emaildotime@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD: sua_app_password
AIRFLOW__SMTP__SMTP_MAIL_FROM: emaildotime@gmail.com
AIRFLOW__SMTP__SMTP_STARTTLS: 'True'
AIRFLOW__SMTP__SMTP_SSL: 'False'
```

For quality checks could implement a quality check with soda, setting like the columns that shouldn't be null or which columns should be present at the table.

# Adicional

### Check Logs
`docker logs [container_name] bash`

### Get an interactive shell inside the container
`docker exec -it [container_name] bash`

### Remove all volumes created inside this project
```docker compose down -v --remove-orphans```
