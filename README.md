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

The biggest challenge was configured the docker-compose for code run correctly. I face a lot of errors of import, because the way I decided to separate the project code.

# Used technologies:

- Git
- Docker-compose
- Python
- PostgreSQL
- Spark
- Airflow

# Verificar logs
```docker logs [container_name]```

Validar se o banco foi criado
```docker exec -it postgres_breweries psql -U kerli -l```

Validar tabelas do banco
```docker exec -it postgres_breweries psql -U kerli -d breweries```

\dt lista de tabelas
\dn lista schemas
\q ou exit para sair o psql

# Get an interactive shell inside the container
docker exec -it [container_name_or_id] /bin/bash
