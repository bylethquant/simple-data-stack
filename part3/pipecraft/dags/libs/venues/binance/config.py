from libs.venues.base.base import RequestResultLimit


# spot base
# https://binance-docs.github.io/apidocs/spot/en/#general-info
SPOT_MAINNET_URL: str = "https://api.binance.com"
SPOT_TESTNET_URL: str = "https://testnet.binance.vision"
SPOT_REQUEST_RATE_LIMIT: int = 6000
SPOT_REQUEST_INTERVAL_IN_MIN: int = 1

# spot ping
# https://binance-docs.github.io/apidocs/spot/en/#test-connectivity
SPOT_ENDPOINT_PING: str = "/api/v3/ping"
SPOT_ENDPOINT_PING_REQUEST_WEIGHT: int = 1

# spot exchange info
# https://binance-docs.github.io/apidocs/spot/en/#exchange-information
SPOT_ENDPOINT_EXCHANGE_INFO: str = "/api/v3/exchangeInfo"
SPOT_ENDPOINT_EXCHANGE_INFO_REQUEST_WEIGHT: int = 20

# spot kline
# https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
SPOT_ENDPOINT_KLINE: str = "/api/v3/klines"
SPOT_ENDPOINT_KLINE_REQUEST_WEIGHT: int = 2
SPOT_ENDPOINT_KLINE_RESULT_LIMIT: RequestResultLimit = RequestResultLimit(500, 1000)

# futures base
# https://binance-docs.github.io/apidocs/futures/en/#general-info
FUT_MAINNET_URL: str = "https://fapi.binance.com"
FUT_TESTNET_URL: str = "https://testnet.binancefuture.com"
FUT_REQUEST_RATE_LIMIT: int = 2400
FUT_REQUEST_INTERVAL_IN_MIN: int = 1

# future ping
# https://binance-docs.github.io/apidocs/futures/en/#test-connectivity
FUT_ENDPOINT_PING: str = "/fapi/v1/ping"
FUT_ENDPOINT_PING_REQUEST_WEIGHT: int = 1

# future exchangeInfo
# https://binance-docs.github.io/apidocs/futures/en/#exchange-information
FUT_ENDPOINT_EXCHANGEINFO: str = "/fapi/v1/exchangeInfo"
FUT_ENDPOINT_EXCHANGEINFO_REQUEST_WEIGHT: int = 1

# future funding rate
# https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history
FUT_ENDPOINT_FUNDING: str = "/fapi/v1/fundingRate"
FUT_FUNDING_REQUEST_RATE_LIMIT: int = 500
FUT_FUNDING_REQUEST_INTERVAL_IN_MIN: int = 5
FUT_FUNDING_RESULT_LIMIT: RequestResultLimit = RequestResultLimit(100, 1000)
FUT_FUNDING_REQUEST_WEIGHT: int = 1  # assumption

# future kline
# https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data
FUT_ENDPOINT_KLINE: str = "/fapi/v1/klines"
FUT_ENDPOINT_KLINE_RESULT_LIMIT: RequestResultLimit = RequestResultLimit(500, 1500)


def fut_endpoint_kline_request_weight(request_result_limit: int) -> int:
    """Returns the weight conditional on the request result limit."""
    if (request_result_limit >= 1) & (request_result_limit < 100):
        weight = 1
    elif (request_result_limit >= 100) & (request_result_limit < 500):
        weight = 2
    elif (request_result_limit >= 500) & (request_result_limit < 1000):
        weight = 5
    else:
        weight = 10
    return weight
