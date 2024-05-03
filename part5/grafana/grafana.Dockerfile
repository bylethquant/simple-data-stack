FROM grafana/grafana:10.0.2

# set environment variables
ENV GF_DATABASE_SSL_MODE=disable
ENV GF_ENABLE_GZIP=true

# copy provisioning and dashboards configurations
COPY prod/dashboards /var/lib/grafana/dashboards
COPY prod/provisioning /etc/grafana/provisioning

# expose port 3000 for Grafana UI
EXPOSE 3000

# connect docker image to your repo (not required)
# LABEL org.opencontainers.image.source https://github.com/bylethquant/substack-data-infra

# start grafana
CMD ["grafana-server", "--config", "/etc/grafana/grafana.ini"]
