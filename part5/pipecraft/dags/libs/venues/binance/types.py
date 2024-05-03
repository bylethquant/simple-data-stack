from dataclasses import dataclass
from typing import Any

from libs.venues.base.base import MarketDataStructure


@dataclass
class Kline(MarketDataStructure):
    open_time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    ignored: Any


@dataclass
class FundingRate(MarketDataStructure):
    symbol: str
    time: int
    funding_rate: float
    ignored: Any

    @staticmethod
    def get_rename_dict() -> dict:
        return {"symbol": "symbol",
                "fundingTime": "time",
                "fundingRate": "funding_rate",
                "markPrice": "ignored"}
