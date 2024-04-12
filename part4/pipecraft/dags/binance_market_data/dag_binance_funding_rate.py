import logging

from airflow import DAG

import binance_market_data.process.etl_funding_future as etl_funding_tasks
import binance_market_data.config as dag_config
from libs.airtasks.initial import start_task, end_task
from binance_market_data.process.common import retrieve_binance_secrets, test_api_connectivity
from libs.venues.base import Instrument


# create module logger
logger = logging.getLogger(__name__)


def generate_binance_funding_rate_dag(dag_id: str,
                                      instrument: Instrument,
                                      schedule_interval: str,
                                      catchup: bool = False,
                                      testnet: bool = False) -> DAG:
    """Generates a DAG for binance funding rate data pipeline."""
    with DAG(dag_id=dag_id,
             description="Data ingestion pipeline for Binance funding rates.",
             start_date=instrument.first_date,
             catchup=catchup,
             schedule_interval=schedule_interval,
             default_args=dag_config.DAG_FUNDING_DEFAULT_ARGS) as dag:
        # task flow
        start_dummy = start_task()
        binance_keys = retrieve_binance_secrets()
        ping_api = test_api_connectivity(binance_keys, testnet, instrument.contract_type)
        extract = etl_funding_tasks.fetch_data(binance_keys, instrument.symbol, testnet=testnet)
        transform = etl_funding_tasks.transform_data(extract)
        ingest = etl_funding_tasks.insert_data(transform)
        end_dummy = end_task()

        start_dummy >> binance_keys >> ping_api >> extract >> transform >> ingest >> end_dummy

    return dag


# create DAGs for funding rates
for instr in dag_config.FUTURE:
    dag_instance_id = f"{instr.venue.value}_{instr.symbol}_funding_{instr.contract_type.value}"
    globals()[dag_instance_id] = generate_binance_funding_rate_dag(dag_id=dag_instance_id,
                                                                   instrument=instr,
                                                                   schedule_interval=dag_config.DAG_SCHEDULE_INTERVAL_FUNDING_PERP)
