CREATE ROLE readaccess;
GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;
CREATE USER {TIMESCALE_READONLY_USERNAME} WITH PASSWORD {TIMESCALE_READONLY_PASSWORD};
GRANT readaccess TO {TIMESCALE_READONLY_USERNAME};