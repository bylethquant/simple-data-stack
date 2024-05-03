from airflow.operators.empty import EmptyOperator
from typing import Optional


def start_task(task_id: Optional[str] = None, **kwargs) -> EmptyOperator:
    tid = "start" if task_id is None else task_id
    return EmptyOperator(task_id=tid, **kwargs)


def end_task(task_id: Optional[str] = None, **kwargs) -> EmptyOperator:
    tid = "end" if task_id is None else task_id
    return EmptyOperator(task_id=tid, **kwargs)


