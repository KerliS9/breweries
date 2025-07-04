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
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=breweries
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
```
Run $ `docker-compose up --build -d`. Wait the building to finished.

Then open the browser with `http://localhost:8080/home`

user: admin
password: admin

Project structure
```
breweries/
├── dags/
│   ├── dag_breweries.py
├── src/
│   ├── Dockerfile
│   ├── fetch_api.py
│   ├── insert_data.py
│   ├── process_data.py
│   └── utils.py
│   └── elt_utils/
│      ├── read.py
|      ├── schemas.py
|      ├── transform.py
│      └── write.py
├── volumes/
|   └── warehouse/
├── docker-compose.yml
├── Dockerfile.airflow
├── requirements.txt
├── README.md
└── .env
```
### Decisions made

I start using Flask to see request from API. Then change to Airflow scheduler, through docker compose, to make an integrated project.

# Used technologies:

- Git
- Docker-compose
- Python
- PostgreSQL
- Spark
- Airflow