FROM ubuntu:20.04
LABEL maintainer="Egidio Caprino <egidio.caprino@gmail.com>"

ENV DEBIAN_FRONTEND="noninteractive" \
  username="" \
  password=""

RUN apt-get --yes update \
  && apt-get --yes install --no-install-recommends mosquitto python3 python3-paho-mqtt python3-numpy netcat wget software-properties-common sudo gpg-agent \
  && echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list \
  && wget --quiet --output-document - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && add-apt-repository --yes ppa:timescale/timescaledb-ppa \
  && apt-get --yes update \
  && apt-get --yes install --no-install-recommends timescaledb-postgresql-12 \
  && mkdir /opt/openeew \
  && rm /etc/mosquitto/mosquitto.conf \
  && touch /etc/mosquitto/mosquitto.conf \
  && apt-get --yes remove wget software-properties-common gpg-agent \
  && apt-get --yes autoremove \
  && apt-get --yes clean \
  && rm --recursive --force /var/lib/apt/lists/*

COPY scripts/detection.py scripts/trigger.py /opt/openeew/
COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector

CMD ["/usr/sbin/detector"]
