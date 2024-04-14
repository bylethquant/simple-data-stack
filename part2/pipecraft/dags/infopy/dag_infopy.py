import logging

from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.bash import BashOperator

from libs.airtasks.initial import start_task, end_task

# create module logger
logger = logging.getLogger(__name__)

with DAG(dag_id=f"0_infopy",
         description="Show all installed python packages.",
         start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
         catchup=False,
         schedule_interval=None) as dag:
    # - create start task
    start_dummy = start_task()
    # - execute pip freeze
    pip_task = BashOperator(task_id="pip_task", bash_command='pip freeze')
    # - create end task
    end_dummy = end_task()

    start_dummy >> pip_task >> end_dummy
