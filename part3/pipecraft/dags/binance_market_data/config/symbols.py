from libs.venues.base import Instrument, Venue, ContractType
from datetime import datetime, timezone

SPOT = [
    Instrument("ADAUSDT", Venue.binance, ContractType.spot, datetime(2018, 4, 18, 0, tzinfo=timezone.utc)),
    Instrument("ATOMUSDT", Venue.binance, ContractType.spot, datetime(2019, 4, 30, 0, tzinfo=timezone.utc)),
    Instrument("AVAXUSDT", Venue.binance, ContractType.spot, datetime(2020, 9, 23, 0, tzinfo=timezone.utc)),
    Instrument("BTCUSDT", Venue.binance, ContractType.spot, datetime(2017, 8, 18, 0, tzinfo=timezone.utc)),
    Instrument("DOGEUSDT", Venue.binance, ContractType.spot, datetime(2019, 7, 6, 0, tzinfo=timezone.utc)),
    Instrument("ETHUSDT", Venue.binance, ContractType.spot, datetime(2017, 8, 18, 0, tzinfo=timezone.utc)),
    Instrument("FTMUSDT", Venue.binance, ContractType.spot, datetime(2019, 6, 12, 0, tzinfo=timezone.utc)),
    Instrument("SOLUSDT", Venue.binance, ContractType.spot, datetime(2020, 8, 12, 0, tzinfo=timezone.utc)),
    Instrument("MATICUSDT", Venue.binance, ContractType.spot, datetime(2019, 4, 27, 0, tzinfo=timezone.utc)),
    Instrument("LINKUSDT", Venue.binance, ContractType.spot, datetime(2019, 1, 17, 0, tzinfo=timezone.utc)),
    Instrument("LTCUSDT", Venue.binance, ContractType.spot, datetime(2017, 12, 14, 0, tzinfo=timezone.utc)),
    Instrument("TRXUSDT", Venue.binance, ContractType.spot, datetime(2018, 6, 12, 0, tzinfo=timezone.utc)),
    Instrument("VETUSDT", Venue.binance, ContractType.spot, datetime(2018, 7, 26, 0, tzinfo=timezone.utc)),
    Instrument("XLMUSDT", Venue.binance, ContractType.spot, datetime(2018, 6, 1, 0, tzinfo=timezone.utc)),
    Instrument("XRPUSDT", Venue.binance, ContractType.spot, datetime(2019, 3, 16, 0, tzinfo=timezone.utc))
]

FUTURE = [
    Instrument("ADAUSDT", Venue.binance, ContractType.future, datetime(2020, 2, 1, 0, tzinfo=timezone.utc)),
    Instrument("ATOMUSDT", Venue.binance, ContractType.future, datetime(2020, 2, 8, 0, tzinfo=timezone.utc)),
    Instrument("AVAXUSDT", Venue.binance, ContractType.future, datetime(2020, 9, 24, 0, tzinfo=timezone.utc)),
    Instrument("BTCUSDT", Venue.binance, ContractType.future, datetime(2019, 9, 9, 0, tzinfo=timezone.utc)),
    Instrument("DOGEUSDT", Venue.binance, ContractType.future, datetime(2020, 7, 11, 0, tzinfo=timezone.utc)),
    Instrument("ETHUSDT", Venue.binance, ContractType.future, datetime(2019, 11, 28, 0, tzinfo=timezone.utc)),
    Instrument("FTMUSDT", Venue.binance, ContractType.future, datetime(2019, 6, 12, 0, tzinfo=timezone.utc)),
    Instrument("SOLUSDT", Venue.binance, ContractType.future, datetime(2020, 9, 15, 0, tzinfo=timezone.utc)),
    Instrument("MATICUSDT", Venue.binance, ContractType.future, datetime(2020, 10, 23, 0, tzinfo=timezone.utc)),
    Instrument("LINKUSDT", Venue.binance, ContractType.future, datetime(2020, 1, 18, 0, tzinfo=timezone.utc)),
    Instrument("LTCUSDT", Venue.binance, ContractType.future, datetime(2020, 1, 10, 0, tzinfo=timezone.utc)),
    Instrument("TRXUSDT", Venue.binance, ContractType.future, datetime(2020, 1, 16, 0, tzinfo=timezone.utc)),
    Instrument("VETUSDT", Venue.binance, ContractType.future, datetime(2020, 2, 15, 0, tzinfo=timezone.utc)),
    Instrument("XLMUSDT", Venue.binance, ContractType.future, datetime(2020, 1, 21, 0, tzinfo=timezone.utc)),
    Instrument("XRPUSDT", Venue.binance, ContractType.future, datetime(2020, 1, 7, 0, tzinfo=timezone.utc))
]
