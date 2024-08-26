# Quick Start
Follow these steps to set up the application using Docker Compose:
1. Change directory to `./part3/compose/pipecraft/scripts/` and execute the Python script `gen_fernet_key.py`. Copy key.
2. Change directory to `./part3/compose/` and create a `.env` file (see `.env.template`):
   * Set the environment variable `AIRFLOW_FERNET_KEY` to the fernet key created in step 1.
   * Set the environment variable `BINANCE_API_KEY` with your [Binance API keys](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072). 
3. Open your terminal.
4. Change to the directory ``./part3/compose`` with the ``docker-compose.yaml`` file.
5. Initialize Apache Airflow by executing ``docker compose up airflow-init``.
6. Start the data infrastructure in detached mode by executing ``docker compose up -d``.
7. Access Airflow web interface through a browser at ``localhost:8080``. Complete the one-time 
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
8. Start the Binance data pipelines.

A detailed guide can be found here: SDS #3: Robust Crypto Data Pipelines with Apache Airflow.