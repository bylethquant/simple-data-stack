import requests
import logging
from datetime import datetime
from requests import Response, HTTPError
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential
from time import sleep

from libs.venues.base.base import ContractType, VenueNet
from libs.venues.binance.common import BinanceAuth, to_ms_int, prepare_binance_request_headers
import libs.venues.binance.config as binance_config

# create module logger
logger = logging.getLogger(__name__)
# log messages from requests above level warning
logging.getLogger('urllib3').setLevel(logging.WARNING)

# module constants
_KLINE_INTERVAL: str = "1m"
_RATE_LIMIT_SLEEPER_IN_SECS: int = 5*60


def _get_base_url(contract_type: ContractType, testnet: bool) -> str:
    api_url_map: dict = {ContractType.spot: {VenueNet.testnet: binance_config.SPOT_TESTNET_URL,
                                             VenueNet.mainnet: binance_config.SPOT_MAINNET_URL},
                         ContractType.future: {VenueNet.testnet: binance_config.FUT_TESTNET_URL,
                                               VenueNet.mainnet: binance_config.FUT_MAINNET_URL}}
    return api_url_map[contract_type][VenueNet.testnet if testnet else VenueNet.mainnet]


def _get_kline_endpoint(contract_type: ContractType) -> str:
    kline_ep_map: dict = {ContractType.spot: binance_config.SPOT_ENDPOINT_KLINE,
                          ContractType.future: binance_config.FUT_ENDPOINT_KLINE}
    return kline_ep_map[contract_type]


def _get_ping_endpoint(contract_type: ContractType) -> str:
    ping_ep_map: dict = {ContractType.spot: binance_config.SPOT_ENDPOINT_PING,
                         ContractType.future: binance_config.FUT_ENDPOINT_PING}
    return ping_ep_map[contract_type]


def _raise_for_status(response: Response) -> None:
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        if response.status_code == 429:
            logger.exception(f"Binance rate limit was reached. "
                             f"I need to sleep immediately for a while to avoid any IP ban!")
            sleep(5*60)
        logger.exception(http_err)
        raise


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def _fetch_api_data(auth: BinanceAuth,
                    base_url: str,
                    endpoint: str,
                    symbol: Optional[str] = None,
                    start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None,
                    kline_interval: Optional[str] = None,
                    request_result_limit: int = None,
                    request_timeout_in_secs: int = 10) -> Any:
    """Market data fetcher for Binance API."""
    request_url: str = f"{base_url}{endpoint}"
    headers: dict = prepare_binance_request_headers(auth)

    # build request url, if necessary
    if symbol is not None:
        request_url += f"?symbol={symbol}"
    if start_time is not None:
        request_url += f"&startTime={to_ms_int(start_time)}"
    if end_time is not None:
        request_url += f"&endTime={to_ms_int(end_time)}"
    if kline_interval is not None:
        request_url += f"&interval={kline_interval}"
    if request_result_limit is not None:
        request_url += f"&limit={request_result_limit}"
    # send get request
    response = requests.get(request_url,
                            headers=headers,
                            timeout=request_timeout_in_secs)
    _raise_for_status(response)
    return response.json()


def fetch_spot_kline(auth: BinanceAuth,
                     symbol: str,
                     start_time: datetime,
                     end_time: datetime,
                     request_result_limit: int = binance_config.SPOT_ENDPOINT_KLINE_RESULT_LIMIT.default,
                     testnet: bool = False) -> List[list]:
    """Fetches spot kline market data from Binance API."""
    return _fetch_api_data(auth=auth,
                           base_url=_get_base_url(ContractType.spot, testnet),
                           endpoint=_get_kline_endpoint(ContractType.spot),
                           symbol=symbol,
                           start_time=start_time,
                           end_time=end_time,
                           request_result_limit=request_result_limit,
                           kline_interval=_KLINE_INTERVAL)


def fetch_future_kline(auth: BinanceAuth,
                       symbol: str,
                       start_time: Optional[datetime] = None,
                       end_time: Optional[datetime] = None,
                       request_result_limit: int = binance_config.FUT_ENDPOINT_KLINE_RESULT_LIMIT.default,
                       testnet: bool = False) -> List[list]:
    """Fetches future kline market data from Binance API."""
    return _fetch_api_data(auth=auth,
                           base_url=_get_base_url(ContractType.future, testnet),
                           endpoint=_get_kline_endpoint(ContractType.future),
                           symbol=symbol,
                           start_time=start_time,
                           end_time=end_time,
                           request_result_limit=request_result_limit,
                           kline_interval=_KLINE_INTERVAL)


def fetch_funding_rate(auth: BinanceAuth,
                       symbol: str,
                       start_time: Optional[datetime] = None,
                       end_time: Optional[datetime] = None,
                       request_result_limit: int = binance_config.FUT_FUNDING_RESULT_LIMIT.default,
                       testnet: bool = False) -> List[Dict[str, Any]]:
    """Fetches funding rate market data from Binance API."""
    return _fetch_api_data(auth=auth,
                           base_url=_get_base_url(ContractType.future, testnet),
                           endpoint=binance_config.FUT_ENDPOINT_FUNDING,
                           symbol=symbol,
                           start_time=start_time,
                           end_time=end_time,
                           request_result_limit=request_result_limit)


def ping_spot_api(auth: BinanceAuth, testnet: bool) -> dict:
    """Tests connectivity to spot Binance API."""
    return _fetch_api_data(auth=auth,
                           base_url=_get_base_url(ContractType.spot, testnet),
                           endpoint=binance_config.SPOT_ENDPOINT_PING)


def ping_future_api(auth: BinanceAuth, testnet: bool) -> dict:
    """Tests connectivity to future Binance API."""
    return _fetch_api_data(auth=auth,
                           base_url=_get_base_url(ContractType.future, testnet),
                           endpoint=binance_config.FUT_ENDPOINT_PING)


def fetch_spot_exchange_info() -> Dict[str, Any]:
    raise NotImplementedError


def fetch_fut_exchange_info() -> Dict[str, Any]:
    raise NotImplementedError
