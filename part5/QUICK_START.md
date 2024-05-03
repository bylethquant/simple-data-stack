# Quick Start

Follow these steps to set up the application using Docker Compose:

1. Change directory to `./part5/compose/pipecraft/scripts/` and execute the Python script `gen_fernet_key.py`. Copy key.
2. Change directory to `./part5/compose/` and create an `.env` file (see template `.env.template`):
    * Set the environment variable `AIRFLOW_FERNET_KEY` with the fernet key created in step 1.
    * Set the environment variable `BINANCE_API_KEY` with
      your [Binance API keys](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072).
    * Set the environment variables `TIMESCALE_PORT`, `TIMESCALE_DATABASE_NAME`, `TIMESCALE_READONLY_USERNAME`, and
      `TIMESCALE_READONLY_PASSWORD`.
3. Open your terminal.
4. Create common network for Traefik and data-infra services
   ```
   docker network create traefik-net
   ```
5. Start Traefik service

   ```
   docker compose -f compose.traefik.core.yaml -f compose.traefik.dev.yaml --env-file ./.env up -d
   ```
6. Initialize Apache Airflow

   ```
   docker compose -f compose.infra.core.yaml -f compose.infra.dev.yaml --env-file ./.env up airflow-init
   ```

7. Start the data infrastructure 

   ```   
   docker compose -f compose.infra.core.yaml -f compose.infra.dev.yaml --env-file ./.env up -d
   ```

8. Access Airflow web interface through a browser at ``airflow.localhost``. Complete the one-time
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
9. Start the Binance data pipelines.
10. Access Grafana web interface through a browser at ``grafana.localhost``.

A detailed guide can be found
here:
* [SDS #5-1: How to Set Up the Data Stack in the Cloud](https://hiddenorder.io/p/sds-5-1-how-to-set-up-the-data-stack)
* [SDS #5-2: How to Set Up the Data Stack in the Cloud](https://hiddenorder.io/p/sds-5-2-how-to-set-up-the-data-stack)
