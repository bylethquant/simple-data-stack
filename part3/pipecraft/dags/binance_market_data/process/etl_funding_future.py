import logging
import pandas as pd

from airflow.decorators import task
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from libs.airtasks.timescale import ingest_data, retrieve_conn_id
from libs.venues import binance as binance_client
from binance_market_data.config import TIMESCALE_FUNDING_FUTURE_TABLE_NAME


# module logger
logger = logging.getLogger(__name__)


@task
def fetch_data(auth: dict,
               symbol: str,
               testnet: bool = False,
               data_interval_start: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """Fetches funding rate data."""
    # reminder: data_interval_start will be set from airflow based on scheduler and schedule time!
    start_time = datetime(data_interval_start.year,
                          data_interval_start.month,
                          data_interval_start.day,
                          data_interval_start.hour)
    end_time = start_time + timedelta(days=1)
    # fetch funding rate data
    response = binance_client.fetch_funding_rate(auth=binance_client.BinanceAuth.from_dict(auth),
                                                 symbol=symbol,
                                                 start_time=start_time,
                                                 end_time=end_time,
                                                 testnet=testnet)
    return response


@task
def transform_data(response: List[Dict[str, Any]]) -> pd.DataFrame:
    """Transforms funding rate response from API. """
    try:
        # process funding rate
        field_types = binance_client.FundingRate.get_field_types()
        df = pd.DataFrame(data=response)
        # re-name columns
        df = df.rename(columns=binance_client.FundingRate.get_rename_dict())
        # remove ignore columns
        df = df.drop(df.columns[df.columns.str.contains('ignore')], axis=1)
        # set type of each column that is kept
        for i_col in df.columns:
            df = df.astype({i_col: field_types[i_col]})
        # timestamp
        df.time = pd.to_datetime(df.time, unit="ms", utc=True)
    except Exception as exc:
        logger.exception(f"Transformation of data: failed. {exc}")
        raise
    else:
        logger.info("Transformation of data: successful.")
    return df


@task
def insert_data(df: pd.DataFrame) -> None:
    """Inserts funding rate data to timescale."""
    try:
        conn_id = retrieve_conn_id()
        ingest_data(conn_id, TIMESCALE_FUNDING_FUTURE_TABLE_NAME, df)
    except Exception as exc:
        logger.exception(f"Insert data to timescale: failed. {exc}")
        raise
    else:
        logger.info(f"Insert data to timescale table {TIMESCALE_FUNDING_FUTURE_TABLE_NAME}: successful.")
