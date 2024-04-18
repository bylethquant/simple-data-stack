from datetime import timedelta

DAG_SCHEDULE_INTERVAL_KLINE: str = "5 * * * *"
TIMESCALE_KLINE_SPOT_TABLE_NAME: str = "binance_kline_spot"
TIMESCALE_KLINE_FUTURE_TABLE_NAME: str = "binance_kline_future"
DAG_KLINE_DEFAULT_ARGS: dict = {"retry_delay": timedelta(minutes=1),
                                "retries": 2}
