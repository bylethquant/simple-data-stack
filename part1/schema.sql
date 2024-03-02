DROP TABLE IF EXISTS price CASCADE;
CREATE TABLE price (
   time    TIMESTAMPTZ,
   close   DOUBLE PRECISION
);
SELECT create_hypertable('price', 'time');