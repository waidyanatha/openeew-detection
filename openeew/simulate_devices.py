import paho.mqtt.client as mqtt
import json
import argparse
from time import sleep

devices = [
    {
        'device_id': '2351n2x55',
        'latitude': 19.35,
        'longitude': -99.14,
        'firmware_version': 1.2,
        'device_type': 'esp32',
        'time_entered': 1597685615,
    },
]


def authenticate(client):
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")
    args = parser.parse_args()
    if args.username and args.password:
        client.username_pw_set(username=args.username, password=args.password)
    return client


def on_connect(client, userdata, flags, resultCode):
    print(f'✅ Connected with result code {resultCode}')
    for device in devices:
        print(f'Sending device {device}')
        client.publish('/devices', json.dumps(device))
        sleep(4)
    client.disconnect()


client = authenticate(mqtt.Client())
client.enable_logger()
client.on_connect = on_connect
client.connect('localhost', 1883)
client.loop_forever()
