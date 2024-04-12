import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2 import sql
from psycopg2.sql import Composable
from airflow.models import Variable
from airflow.decorators import task
from typing import Union

from libs.airtasks.timescale import retrieve_conn_id

# create module logger
logger = logging.getLogger(__name__)


def _read_sql(path: str) -> str:
    """Reads an sql script."""
    try:
        with open(path, "r") as sql_script:
            sql_cmd_str = sql_script.read()
    except Exception as exc:
        logger.exception(f"Could not read sql file. {exc}")
        raise
    else:
        logger.info(f"Read sql file successfully.")
    return sql_cmd_str


def _get_roles_sql(path_str: str) -> Composable:
    """Constructs the sql script for creating roles."""
    # read file
    sql_cmd_str = _read_sql(path_str)
    try:
        # replace dummy variables with environmental variables
        sql_cmd = sql.SQL(sql_cmd_str).format(
            TIMESCALE_READONLY_USERNAME=sql.Identifier(Variable.get("TIMESCALE_READONLY_USERNAME")),
            TIMESCALE_READONLY_PASSWORD=sql.Literal(Variable.get("TIMESCALE_READONLY_PASSWORD"))
        )
        logger.info(Variable.get("TIMESCALE_READONLY_PASSWORD"))
        logger.info(type(Variable.get("TIMESCALE_READONLY_PASSWORD")))
    except Exception as exc:
        logger.exception(f"Get create roles sql statement: failed. {exc}")
        raise
    else:
        logger.info("Get create roles sql statement: successful.")
    return sql_cmd


def _execute_sql(conn_id: str, sql_cmd: Union[str, Composable]) -> None:
    try:
        with PostgresHook(postgres_conn_id=conn_id).get_conn() as conn:
            logger.info(f"Executing query. {sql_cmd if isinstance(sql_cmd, str) else sql_cmd.as_string(conn)}")
            with conn.cursor() as crs:
                # execute sql
                crs.execute(sql_cmd)
                # commit
                conn.commit()
    except Exception as exc:
        logger.exception(f"Executing query: failed. {exc}")
        raise
    else:
        logger.info(f"Executing query: successful.")


@task
def create_roles(path_str: str) -> None:
    """Creates roles."""
    _execute_sql(retrieve_conn_id(), _get_roles_sql(path_str))


@task
def create_tables(path_str: str) -> None:
    """Creates hypertables."""
    _execute_sql(retrieve_conn_id(), _read_sql(path_str))

