FROM apache/airflow:2.8.3
USER root
RUN apt-get update 
RUN apt-get install -y gosu git && rm -rf /var/lib/apt/lists/*
USER airflow
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt