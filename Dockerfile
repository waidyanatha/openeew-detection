FROM ubuntu:20.04
LABEL maintainer="Egidio Caprino <egidio.caprino@gmail.com>"

# Mosquitto

ENV username ""
ENV password ""

ENV DEBIAN_FRONTEND "noninteractive"

RUN apt-get --yes update
RUN apt-get --yes install mosquitto python3 python3-paho-mqtt python3-numpy netcat

RUN mkdir /opt/openeew
COPY scripts/detection.py scripts/trigger.py /opt/openeew/

RUN rm /etc/mosquitto/mosquitto.conf
RUN touch /etc/mosquitto/mosquitto.conf

COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector

# TimescaleDB

RUN apt-get --yes update
RUN apt-get --yes install wget software-properties-common sudo
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet --output-document - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get --yes update
RUN add-apt-repository --yes ppa:timescale/timescaledb-ppa
RUN apt-get --yes update
RUN apt-get --yes install timescaledb-postgresql-12

CMD ["/usr/sbin/detector"]
