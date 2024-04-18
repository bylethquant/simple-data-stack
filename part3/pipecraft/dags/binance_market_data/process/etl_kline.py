import logging
import pandas as pd

from airflow.decorators import task
from datetime import datetime, timedelta
from typing import Optional, List

from libs.airtasks.timescale import ingest_data, retrieve_conn_id
from libs.venues import binance as binance_client
from libs.venues.base import ContractType, Instrument
from binance_market_data.config import TIMESCALE_KLINE_SPOT_TABLE_NAME, TIMESCALE_KLINE_FUTURE_TABLE_NAME


# module logger
logger = logging.getLogger(__name__)


@task
def fetch_data(auth: dict,
               instrument: Instrument,
               testnet: bool = False,
               data_interval_start: Optional[datetime] = None) -> List[list]:
    """Sends get request to fetch candlestick data for the previous hour."""
    fetch_data_map = {ContractType.spot: binance_client.fetch_spot_kline,
                      ContractType.future: binance_client.fetch_future_kline}
    # reminder: data_interval_start will be set from airflow based on scheduler and schedule time!
    start_time = datetime(data_interval_start.year,
                          data_interval_start.month,
                          data_interval_start.day,
                          data_interval_start.hour)
    end_time = start_time + timedelta(hours=1) - timedelta(minutes=1)
    # fetch candlestick data
    response = fetch_data_map[instrument.contract_type](auth=binance_client.BinanceAuth.from_dict(auth),
                                                        symbol=instrument.symbol,
                                                        start_time=start_time,
                                                        end_time=end_time,
                                                        testnet=testnet)
    return response


@task
def transform_data(response: list, symbol: str) -> pd.DataFrame:
    """Transforms the data and prepares to insert."""
    try:
        # process klines
        field_types = binance_client.Kline.get_field_types()
        df = pd.DataFrame(data=response, columns=list(field_types.keys()))
        # remove ignore columns
        df = df.drop(df.columns[df.columns.str.contains('ignore')], axis=1)
        # set type of each column that is kept
        for i_col in df.columns:
            df = df.astype({i_col: field_types[i_col]})
        # set time
        df.open_time = pd.to_datetime(df.open_time, unit="ms", utc=True)
        df.close_time = pd.to_datetime(df.close_time, unit="ms", utc=True)
        # add symbol column
        df["symbol"] = symbol
    except Exception as exc:
        logger.exception(f"Transformation of data: failed. {exc}")
        raise
    else:
        logger.info("Transformation of data: successful.")
    return df


@task
def insert_data(contract_type: ContractType, df: pd.DataFrame) -> None:
    """Inserts data to timescale."""
    timescale_schema_map = {ContractType.spot: TIMESCALE_KLINE_SPOT_TABLE_NAME,
                            ContractType.future: TIMESCALE_KLINE_FUTURE_TABLE_NAME}
    table_name = timescale_schema_map[contract_type]
    try:
        conn_id = retrieve_conn_id()
        ingest_data(conn_id, table_name, df)
    except Exception as exc:
        logger.exception(f"Insert data to timescale: failed. {exc}")
        raise
    else:
        logger.info(f"Insert data to timescale table {table_name}: successful.")
