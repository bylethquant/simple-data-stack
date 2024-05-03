import logging
import pandas as pd

from psycopg2.extras import execute_values
from psycopg2.extensions import connection
from airflow.providers.postgres.hooks.postgres import PostgresHook

# create module logger
logger = logging.getLogger(__name__)


def _bulk_insert(conn: connection, table_name: str, df_data: pd.DataFrame) -> None:
    """Bulk insert to timescale."""
    try:
        # create a list of tuples from dataframe
        data_tuples = [tuple(x) for x in df_data.to_numpy()]
        # comma-separated dataframe columns
        cols = ','.join(list(df_data.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)
        with conn.cursor() as crs:
            execute_values(crs, query, data_tuples)
            conn.commit()
    except Exception as exc:
        logger.exception(f"Bulk insert: failed. {exc}.")
        raise
    else:
        logger.info("Bulk insert: successful.")


def ingest_data(conn_id: str, table_name: str, df_data: pd.DataFrame) -> None:
    with PostgresHook(postgres_conn_id=conn_id).get_conn() as conn:
        _bulk_insert(conn, table_name, df_data)
