FROM bitnami/spark:3.5.0

USER root

RUN apt-get update && apt-get install -y curl

# Cria diretório da app
WORKDIR /app

# Instala dependências Python
COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

# Baixa o driver JDBC do PostgreSQL (necessário pro Spark ler PostgreSQL)
RUN curl -L -o /opt/bitnami/spark/jars/postgresql.jar \
https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

# Copia todo o código do Spark para dentro do container
COPY . /app

# Deixa o container em modo sleep para comandos interativos ou spark-submit
CMD ["sleep", "infinity"]
