from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any

from libs.venues.base.base import VenueAuthentication


@dataclass
class BinanceAuth(VenueAuthentication):
    BINANCE_API_KEY: str

    @classmethod
    def from_dict(cls, auth_dict: Dict[str, str]):
        return cls(auth_dict["BINANCE_API_KEY"])

    def as_dict(self) -> Dict[str, str]:
        return asdict(self)


def to_ms_int(dt: datetime) -> int:
    """Converts datetime timestamp to integer in ms."""
    return int(round(dt.timestamp() * 1000))


def to_dt(ms_int: int) -> datetime:
    """Converts timestamp in ms (integer) to datetime."""
    return datetime.utcfromtimestamp(ms_int / 1000).replace(tzinfo=timezone.utc)


def prepare_binance_request_headers(auth: BinanceAuth) -> Dict[str, Any]:
    """Creates headers for Binance REST API."""
    return {"content-type": "application/json", "X-MBX-APIKEY": auth.BINANCE_API_KEY}
