FROM bitnami/spark:3.4.1

USER root

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

RUN curl -L -o /opt/bitnami/spark/jars/postgresql.jar \
https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

RUN curl -L -o /opt/bitnami/spark/jars/delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar \
  && curl -L -o /opt/bitnami/spark/jars/delta-storage-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar

COPY . /app

CMD ["sleep", "infinity"]
