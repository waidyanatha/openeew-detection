import json
from time import sleep

import paho.mqtt.client as mqtt

from mqtt import authenticate

earthquakes = [
    {
        'event_id': 'foo',
        'time_of_event': 1598295724,
        'intensity': 5,
        'latitude': 19.35,
        'longitude': -99.14,
        'sensor_ids': ['bar'],
    },
]


def on_connect(client, userdata, flags, resultCode):
    print(f'✅ Connected with result code {resultCode}')
    for earthquake in earthquakes:
        print(f'Sending earthquake {earthquake}')
        client.publish('/earthquakes', json.dumps(earthquake))
        sleep(4)
    client.disconnect()


client = authenticate(mqtt.Client())
client.enable_logger()
client.on_connect = on_connect
client.connect('localhost', 1883)
client.loop_forever()
