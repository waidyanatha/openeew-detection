FROM alpine:3.12.0
LABEL maintainer="Egidio Caprino <egidio.caprino@gmail.com>"

ENV PGDATA "/var/lib/postgresql/data"

RUN apk update --no-cache \
  && apk add --no-cache mosquitto python3 py3-paho-mqtt py3-numpy py3-psycopg2 postgresql postgresql-dev cmake build-base git bash logrotate \
  && git clone --branch 1.7.2 https://github.com/timescale/timescaledb.git /tmp/timescaledb \
  && cd /tmp/timescaledb && ./bootstrap -DREGRESS_CHECKS=OFF && cd build && make && make install && cd / \
  && mkdir /opt/openeew/ \
  && touch /opt/openeew/mosquitto.conf \
  && mkdir /var/log/mosquitto \
  && chown mosquitto:mosquitto /var/log/mosquitto \
  && echo "log_dest file /var/log/mosquitto/mosquitto.log" >> /opt/openeew/mosquitto.conf \
  && mkdir /run/postgresql \
  && chown postgres:postgres /run/postgresql \
  && apk del postgresql-dev cmake build-base git bash \
  && rm -rf /tmp/timescaledb \
  && rm -rf /var/cache/apk/*

COPY openeew/*.py ./init_db.sql /opt/openeew/
COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector
COPY logrotate/mosquitto /etc/logrotate.d/

USER postgres
RUN mkdir "${PGDATA}" \
  && chmod 0700 "${PGDATA}" \
  && initdb "${PGDATA}" \
  && echo "shared_preload_libraries = 'timescaledb'" >> "${PGDATA}/postgresql.conf" \
  && echo "log_destination = 'csvlog'" >> "${PGDATA}/postgresql.conf" \
  && echo "logging_collector = on" >> "${PGDATA}/postgresql.conf" \
  && echo "log_directory = '/var/log/postgresql'" >> "${PGDATA}/postgresql.conf" \
  && echo "log_filename = '%Y-%m-%d_%H%M%S.log'" >> "${PGDATA}/postgresql.conf"

USER root
CMD ["/usr/sbin/detector"]
