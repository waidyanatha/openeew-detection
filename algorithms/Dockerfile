FROM eclipse-mosquitto:1.6.10
LABEL maintainer="Egidio Caprino <egidio.caprino@gmail.com>"

ENV username ""
ENV password ""

RUN apk update
RUN apk add python3 py3-paho-mqtt py3-numpy

RUN mkdir /opt/openeew
COPY detection.py trigger.py /opt/openeew/

RUN rm /mosquitto/config/mosquitto.conf
COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector

CMD ["/usr/sbin/detector"]
