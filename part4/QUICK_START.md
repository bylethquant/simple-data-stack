# Quick Start

Follow these steps to set up the application using Docker Compose:

1. Change directory to `./part4/compose/pipecraft/scripts/` and execute the Python script `gen_fernet_key.py`.
2. Change directory to `./part4/compose/` and create a `.env` file (see `.env.template`):
    * Set the environment variable `AIRFLOW_FERNET_KEY` with the fernet key created in step 1.
    * Set the environment variable `BINANCE_API_KEY` with
      your [Binance API keys](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072).
    * Set the environment variables `TIMESCALE_PORT`, `TIMESCALE_DATABASE_NAME`, `TIMESCALE_READONLY_USERNAME`, and
      `TIMESCALE_READONLY_PASSWORD`.
3. Open your terminal.
4. Initialize Apache Airflow by executing ``docker compose up airflow-init``.
5. Start the data infrastructure in detached mode by executing ``docker compose up -d``.
6. Access Airflow web interface through a browser at ``localhost:8080``. Complete the one-time
   initialization of Timescale:
    - Create a connection to Timescale: Admin → Connections
        * Connection Id: timescale_conn_admin
        * Connection Type: Postgres
        * Host: host.docker.internal
        * Database: timescale
        * Login: admin
        * Password: password
        * Port: 5433
    - Execute the Airflow DAG `0_timescale_create_roles` to create read-only user roles.
    - Execute the Airflow DAG `0_timescale_create_tables` to create hypertables.
7. Start the Binance data pipelines.
8. Access Grafana web interface through a browser at ``localhost:3000``.

A detailed guide can be found here: [SDS #4: Crypto Market Data Dashboard with Grafana](https://hiddenorder.io/p/sds-4-crypto-market-data-dashboard).