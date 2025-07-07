# Breweries

## Introduction

This repository aims to show a data search project in an API, processing through Airflow the medallion architecture.

* API: `https://api.openbrewerydb.org/v1/breweries`

## Requirements to run this project
- git
- python
- docker-compose

## How to start this project

Clone this repository $ `git clone git@github.com:KerliS9/breweries.git`

Set your `.env` file like this:
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
Run $ `docker-compose up -d --build`. Wait the building to finish.

Check $ `docker logs airflow_init_breweries`. Line 'Database migrating done!' must be present at logs.

Run $ `chmod -R 777 ./volumes/warehouse` for Airflow to have access to read and write inside the volumes of this project.

Then open the browser with `http://localhost:8080`
```
user: admin
password: admin
```
To check test - run $ `docker-compose run --rm test-runner`

## Project structure
```
breweries/
├── dags/
│   ├── __init__.py
│   └── dag_breweries.py
├── src/
│   ├── __init__.py
│   ├── Dockerfile
│   ├── fetch_api.py
│   ├── process_data.py
│   └── utils.py
│   └── elt_utils/
|      ├── __init__.py
|      ├── schemas.py
│      └── write.py
├── tests/
│   ├── __init__.py
│   ├── test_fetch_api.py
│   └── test_process_data.py
├── volumes/
|   └── warehouse/
|     ├── bronze
|     ├── gold
│     └── silver
├── docker-compose.yml
├── Dockerfile.airflow
├── Dockerfile.test
├── requirements.txt
├── README.md
└── .env
```
## Decisions made

I started using Flask to see the request from API. Then changed to Airflow scheduler, through docker compose, to make an integrated project.

The biggest challenge was to configure the docker-compose for the code run correctly.

## Used technologies:

- Git
- Docker-compose
- Python
- Pyspark
- PostgreSQL
- Spark
- Airflow

## Monitoring and Alerting
Case I needed to set an alert to my pipeline, I would add some configs to default args at the dag:
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

For quality checks it's possible to create and run a quality check with soda. For example: setting the columns that shouldn't be null or which columns should be present at the table.

# Additional

### Check Logs
`docker logs [container_name] bash`

### Get an interactive shell inside the container
`docker exec -it [container_name] bash`

### Remove all volumes created inside this project
```docker compose down -v --remove-orphans```
