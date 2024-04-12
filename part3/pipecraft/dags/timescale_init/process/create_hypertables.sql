CREATE TABLE IF NOT EXISTS binance_kline_spot (
    open_time TIMESTAMPTZ,
    symbol TEXT NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    close_time TIMESTAMPTZ,
    quote_asset_volume DOUBLE PRECISION,
    number_of_trades BIGINT,
    taker_buy_base_asset_volume DOUBLE PRECISION,
    taker_buy_quote_asset_volume DOUBLE PRECISION
);
SELECT create_hypertable('binance_kline_spot', 'open_time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_symbol_time_spot ON binance_kline_spot (symbol, open_time DESC);

CREATE TABLE IF NOT EXISTS binance_kline_future (
    open_time TIMESTAMPTZ,
    symbol TEXT NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    close_time TIMESTAMPTZ,
    quote_asset_volume DOUBLE PRECISION,
    number_of_trades BIGINT,
    taker_buy_base_asset_volume DOUBLE PRECISION,
    taker_buy_quote_asset_volume DOUBLE PRECISION
);
SELECT create_hypertable('binance_kline_future', 'open_time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_symbol_time_future ON binance_kline_future (symbol, open_time DESC);


CREATE TABLE IF NOT EXISTS binance_funding_future (
    time TIMESTAMPTZ,
    symbol TEXT NOT NULL,
    funding_rate DOUBLE PRECISION
);
SELECT create_hypertable('binance_funding_future', 'time', if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_symbol_time_funding_future ON binance_funding_future (symbol, time DESC);
