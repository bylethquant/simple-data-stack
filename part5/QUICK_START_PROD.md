# Quick Start PROD

Preliminary steps:

* Create [Hetzner Cloud](https://www.hetzner.com/cloud/) server with Docker Compose application installed
* Register domain and link domain to server

Follow these steps to set up the application using Docker Compose:

1. Change directory to `./part5/compose/pipecraft/scripts/` and execute the Python script `gen_fernet_key.py`. Copy key.
2. Change directory to `./part5/compose/` and create a `.env.prod` file (see template `.env.prod.template`):
    * Set the environment variable `AIRFLOW_FERNET_KEY` with the fernet key created in step 1.
    * Set the environment variable `BINANCE_API_KEY` with
      your [Binance API keys](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072).
    * Set the environment variables `TIMESCALE_PORT`, `TIMESCALE_DATABASE_NAME`, `TIMESCALE_READONLY_USERNAME`, and
      `TIMESCALE_READONLY_PASSWORD`.
    * Set the domain you registered `DOMAIN_NAME`. For example: `DOMAIN_NAME=mydomain.com`
    * We use [Let´s Encrypt](https://letsencrypt.org/) to get an SSL/TLS certificate. The certificate is used to enable
      HTTPS (SSL/TLS) to secure browser-to-server communications. [Let´s Encrypt](https://letsencrypt.org/) issues the
      certificate automatically. We need to provide a valid email using `ACME_EMAIL`, which is used for important
      communications related to the certificate that we generated. For example, this email would be used to alert you of
      impending certificate expirations.
3. Create custom docker images for Apache Airflow and Grafana that we push
   to [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (
   GHCR):
    1. Create a GitHub access token to push docker images to GHCR. Store it in a file `.ghcr.secret`
       at `./part5/compose/`.
    2. Open your terminal, navigate to `./part5/compose/`  and log into GitHub Container Registry with your generated
       access token
   ```
   cat .ghcr.secret | docker login --username <githubusername> --password-stdin ghcr.io
   ```
    3. Navigate to `./part5/pipecraft/` and execute `pipecraft_build_and_push.sh`. We build the custom docker image
       using `pipecraft.Dockerfile` and push it to GHCR.
   ```
   ./pipecraft_build_and_push.sh
   ```
    4. Navigate to `./part5/grafana/` and execute `grafana_build_and_push.sh`. We build the custom docker image
       using `grafana.Dockerfile` and push it to GHCR.
   ```
   ./grafana_build_and_push.sh
   ```
3. Connect with root user to Hetzner Cloud server and do the following initial steps
    1. Create folders and `acme.json` file (the file is prepared to store sensitive data securely, such as SSL/TLS
       certificates from Let's Encrypt)
   ```
   mkdir -p /docker/part5/storage/traefik
   mkdir -p /docker/part5/pipecraft/logs
   mkdir -p /docker/part5/compose
   touch /docker/part5/storage/traefik/acme.json
   chmod 600 /docker/part5/storage/traefik/acme.json
   ```
    2. Navigate `./docker/part5/` and set ownership to airflow user (important: use here AIRFLOW_USER_ID
       from `.env.prod`
       file, default=50000)
   ```
   chown -R 50000:50000 pipecraft
   ```
    3. Set read and write access for pipecraft folder (used to write logs by Airflow)
   ```
   chmod -R u+rwX pipecraft
   ```
4. Copy local docker compose, `env.prod`, and `ghcr.secret` files to the server `/docker/part5/compose`.
5. Login to Github Container Registry using your access token
   ```
   cat .ghcr.secret | docker login --username <githubusername> --password-stdin ghcr.io
   ```
6. Navigate to `/docker/part5/compose` and create a common network
   ```
   docker network create traefik-net
   ```
5. Start Traefik service
   ```
   docker compose -f compose.traefik.core.yaml -f compose.traefik.prod.yaml --env-file ./.env.prod up -d
   ```
6. Initialize Apache Airflow

   ```
   docker compose -f compose.infra.core.yaml -f compose.infra.prod.yaml --env-file ./.env.prod up airflow-init
   ```
7. Start the data infrastructure
   ```   
   docker compose -f compose.infra.core.yaml -f compose.infra.prod.yaml --env-file ./.env.prod up -d
   ```
8. Access Airflow web interface through a browser at ``airflow.mydomain.com``. Complete the one-time
   initialization of Timescale:
    - Create a connection to Timescale: Admin → Connections
        * Connection Id: timescale_conn_admin
        * Connection Type: Postgres
        * Host: mydomain.com
        * Database: timescale
        * Login: admin
        * Password: password
        * Port: 5433
    - Execute the Airflow DAG `0_timescale_create_roles` to create read-only user roles.
    - Execute the Airflow DAG `0_timescale_create_tables` to create hypertables.
9. Start the Binance data pipelines.
10. Access Grafana web interface through a browser at ``grafana.mydomain.com``.

A detailed guide can be found
here: 
* [SDS #5-1: How to Set Up the Data Stack in the Cloud](https://hiddenorder.io/p/sds-5-1-how-to-set-up-the-data-stack)
* [SDS #5-2: How to Set Up the Data Stack in the Cloud](https://hiddenorder.io/p/sds-5-2-how-to-set-up-the-data-stack)
