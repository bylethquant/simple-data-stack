import logging

from typing import Dict, Any
from airflow.models import Variable
from airflow.decorators import task

from libs.venues import binance as binance_client
from libs.venues.base import ContractType

# module logger
logger = logging.getLogger(__name__)


@task
def retrieve_binance_secrets() -> Dict[str, Any]:
    """Retrieves Binance API keys."""
    try:
        binance_keys = binance_client.BinanceAuth(Variable.get("BINANCE_API_KEY"))
    except Exception as exc:
        logger.exception(f"Retrieving Binance keys failed. Msg: {exc}.")
        raise
    else:
        logger.info(f"Retrieving Binance keys was successful.")
    return binance_keys.as_dict()


@task
def test_api_connectivity(auth: dict, testnet: bool, contract_type: ContractType) -> None:
    """Tests connectivity to the Rest API."""
    connectivity_map = {ContractType.spot: binance_client.ping_spot_api,
                        ContractType.future: binance_client.ping_future_api}
    connectivity_map[contract_type](binance_client.BinanceAuth.from_dict(auth), testnet)
