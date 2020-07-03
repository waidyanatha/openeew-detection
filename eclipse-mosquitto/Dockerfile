FROM eclipse-mosquitto:1.6.10

ENV port 1883

COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY detector /usr/sbin/detector
RUN chmod +x /usr/sbin/detector

CMD ["/usr/sbin/detector"]
