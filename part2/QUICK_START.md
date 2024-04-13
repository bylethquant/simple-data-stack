# Quick Start
Follow these steps to set up the application using Docker Compose:
1. Change directory to `./part2/compose/pipecraft/scripts/` and execute the Python script `gen_fernet_key.py`.
2. Change directory to `./part2/compose/` and create a `.env` file (see `.env.template`):
   * Set the environment variable `AIRFLOW_FERNET_KEY` with the fernet key created in step 1.
3. Open your terminal.
4. Change to the directory ``./part2/compose`` with the ``docker-compose.yaml`` file.
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

A detailed guide can be found here: TBA.