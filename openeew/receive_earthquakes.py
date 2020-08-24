import json

import paho.mqtt.client as mqtt

from earthquakes import save_earthquake
from mqtt import authenticate


def on_connect(client, userdata, flags, resultCode):
    print(f'✅ Connected with result code {resultCode}')
    client.subscribe('/earthquakes')


def on_message(client, userdata, message):
    try:
        decoded_message = str(message.payload.decode('utf-8', 'ignore'))
        earthquake = json.loads(decoded_message)
        print(f'Received earthquake: {earthquake}')
        save_earthquake(earthquake)
        print('✅ Earthquake saved')
    except BaseException as exception:
        print(exception)


client = authenticate(mqtt.Client())
client.enable_logger()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883)

print('👂🚀 Listening for earthquakes')
client.loop_forever()
