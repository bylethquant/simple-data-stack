import logging

from datetime import datetime, timezone
from airflow import DAG

from libs.airtasks.initial import start_task, end_task
from timescale_init.process import create_tables

# create module logger
logger = logging.getLogger(__name__)

with DAG(dag_id=f"0_timescale_create_tables",
         description="Timescale initialization pipeline for creating hypertables.",
         start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
         catchup=False,
         schedule_interval=None) as dag:
    # - create start task
    start_dummy = start_task()
    # - create hypertables
    tables = create_tables("dags/timescale_init/process/create_hypertables.sql")
    # - create end task
    end_dummy = end_task()

    start_dummy >> tables >> end_dummy
