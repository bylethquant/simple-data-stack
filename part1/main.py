import psycopg2
import random

from psycopg2.extras import execute_values
from dataclasses import dataclass, asdict, astuple, fields
from datetime import datetime, timedelta
from typing import List


@dataclass
class TimescaleConfig:
    database: str
    host: str
    user: str
    password: str
    port: int


class Event:
    pass


@dataclass
class PriceUpdated(Event):
    time: datetime
    close: float


def insert(events: List[PriceUpdated], timescale_config: TimescaleConfig, table_name: str) -> None:
    """Inserts a price update event to timescale database."""
    data_tpl = [astuple(event) for event in events]
    col_name = ','.join([field.name for field in fields(PriceUpdated)])
    query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, col_name)
    with psycopg2.connect(**asdict(timescale_config)) as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, query, data_tpl)
        conn.commit()


def create_hypertable(timescale_config: TimescaleConfig, sql_file_path: str = "schema.sql") -> None:
    """Creates timescale schema."""
    with psycopg2.connect(**asdict(timescale_config)) as conn:
        with conn.cursor() as cursor:
            with open(sql_file_path, 'r') as sql_file:
                cursor.execute(sql_file.read())
        conn.commit()


def read(timescale_config: TimescaleConfig, table_name: str) -> List[tuple]:
    """Reads price update events from timescale database."""
    with psycopg2.connect(**asdict(timescale_config)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()

    return data


def get_mock_data(num: int) -> List[PriceUpdated]:
    """Gets some mock data."""
    mock_events = [PriceUpdated(time=datetime.utcnow() - timedelta(minutes=i),
                                close=random.randint(0, 1)) for i in range(num)]

    return mock_events


def main():
    mock_events = get_mock_data(5)
    ts_config = TimescaleConfig("timescale", "localhost", "user", "password", 5432)
    create_hypertable(ts_config)
    insert(events=mock_events, timescale_config=ts_config, table_name="price")
    print(read(ts_config, table_name="price"))


if __name__ == "__main__":
    main()
