#!/bin/bash

airflow db migrate

airflow users create \
   --username "${_AIRFLOW_WWW_USER_USERNAME}" \
   --firstname "${_AIRFLOW_WWW_USER_FIRSTNAME}" \
   --lastname "${_AIRFLOW_WWW_USER_LASTNAME}" \
   --role "${_AIRFLOW_WWW_USER_ROLE}" \
   --email "${_AIRFLOW_WWW_USER_EMAIL}" \
   --password "${_AIRFLOW_WWW_USER_PASSWORD}" || true

echo "Airflow database initialization completed."
