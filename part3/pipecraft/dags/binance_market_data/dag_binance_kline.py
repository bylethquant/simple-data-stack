import logging

from airflow import DAG

import binance_market_data.process.etl_kline as etl_kline_tasks
import binance_market_data.config as dag_config
from libs.airtasks.initial import start_task, end_task
from binance_market_data.process.common import retrieve_binance_secrets, test_api_connectivity
from libs.venues.base import Instrument

# create module logger
logger = logging.getLogger(__name__)


def generate_binance_candlestick_dag(dag_id: str,
                                     instrument: Instrument,
                                     schedule_interval: str,
                                     catchup: bool = False,
                                     testnet: bool = False) -> DAG:
    """Generates a DAG for binance candlestick data pipeline."""
    with DAG(dag_id=dag_id,
             description="Data ingestion pipeline for Binance candlestick data.",
             start_date=instrument.first_date,
             catchup=catchup,
             schedule_interval=schedule_interval,
             default_args=dag_config.DAG_KLINE_DEFAULT_ARGS) as dag:
        # task flow
        # - create start task
        start_dummy = start_task()
        # - retrieve binance api keys
        binance_keys = retrieve_binance_secrets()
        # - test connectivity of binance api
        ping_api = test_api_connectivity(binance_keys, testnet, instrument.contract_type)
        # - fetch binance candlestick data
        extract = etl_kline_tasks.fetch_data(binance_keys, instrument, testnet=testnet)
        # - transform data
        transform = etl_kline_tasks.transform_data(extract, instrument.symbol)
        # - insert data to timescale database
        ingest = etl_kline_tasks.insert_data(instrument.contract_type, transform)
        # - create end task
        end_dummy = end_task()

        start_dummy >> binance_keys >> ping_api >> extract >> transform >> ingest >> end_dummy

    return dag


# create DAGs for kline
for instr in dag_config.SPOT + dag_config.FUTURE:
    dag_instance_id = f"{instr.venue.value}_{instr.symbol}_kline_{instr.contract_type.value}"
    globals()[dag_instance_id] = generate_binance_candlestick_dag(dag_id=dag_instance_id,
                                                                  instrument=instr,
                                                                  schedule_interval=dag_config.DAG_SCHEDULE_INTERVAL_KLINE)
