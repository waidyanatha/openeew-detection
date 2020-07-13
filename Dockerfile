FROM ubuntu:20.04
LABEL maintainer="Egidio Caprino <egidio.caprino@gmail.com>"

ENV username ""
ENV password ""

RUN apt-get --yes update
RUN apt-get --yes install mosquitto python3 python3-paho-mqtt python3-numpy netcat

RUN mkdir /opt/openeew
COPY scripts/detection.py scripts/trigger.py /opt/openeew/

RUN rm /etc/mosquitto/mosquitto.conf
RUN touch /etc/mosquitto/mosquitto.conf

COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector

CMD ["/usr/sbin/detector"]
