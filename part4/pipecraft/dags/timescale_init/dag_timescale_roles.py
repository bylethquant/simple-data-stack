import logging

from datetime import datetime, timezone
from airflow import DAG

from libs.airtasks.initial import start_task, end_task
from timescale_init.process import create_roles

# create module logger
logger = logging.getLogger(__name__)

with DAG(dag_id=f"0_timescale_create_roles",
         description="Timescale initialization pipeline for creating user roles.",
         start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
         catchup=False,
         schedule_interval=None) as dag:
    # - create start task
    start_dummy = start_task()
    # - create read only user role
    roles = create_roles("dags/timescale_init/process/create_roles.sql")
    # - create end task
    end_dummy = end_task()

    start_dummy >> roles >> end_dummy
