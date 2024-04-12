from datetime import timedelta

DAG_SCHEDULE_INTERVAL_FUNDING_PERP: str = "5 0 * * *"
TIMESCALE_FUNDING_FUTURE_TABLE_NAME: str = "binance_funding_future"
DAG_FUNDING_DEFAULT_ARGS: dict = {"retry_delay": timedelta(minutes=1),
                                  "retries": 2}
