FROM apache/airflow:2.8.1-python3.11

# install additional requirements (if needed)
# COPY requirements.txt /
# RUN pip install --no-cache-dir -r /requirements.txt

# set environment variables for Airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=false
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=true
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=INFO

# copy DAGs and other configurations into the image
COPY ./dags /opt/airflow/dags
COPY ./config /opt/airflow/config
COPY ./plugins /opt/airflow/plugins
COPY ./scripts /opt/airflow/scripts

# connect docker image to your repo (not required)
# LABEL org.opencontainers.image.source https://github.com/bylethquant/substack-data-infra

# expose port 8080 for the Airflow UI
EXPOSE 8080
