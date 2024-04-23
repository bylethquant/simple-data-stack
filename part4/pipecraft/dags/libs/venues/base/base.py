from enum import Enum
from dataclasses import dataclass, fields
from datetime import datetime


class Venue(Enum):
    """Crypto venues."""
    binance = "binance"


class VenueAuthentication:
    """Base class to authenticate at a venue."""
    pass


class VenueNet(Enum):
    """Production vs test environment."""
    mainnet = "mainnet"
    testnet = "testnet"


class ContractType(Enum):
    """The contract type of traded instrument."""
    spot = "spot"
    future = "future"


@dataclass
class Instrument:
    """The traded instrument."""
    symbol: str
    venue: Venue
    contract_type: ContractType
    first_date: datetime


@dataclass
class MarketDataStructure:
    """Base class for market data API responses."""

    @classmethod
    def get_field_types(cls) -> dict:
        return {field.name: field.type for field in fields(cls)}


@dataclass
class RequestResultLimit:
    """Default and maximum limit on result of an API market data request."""
    default: int
    max: int
