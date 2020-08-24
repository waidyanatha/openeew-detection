import paho.mqtt.client as mqtt
import json
import argparse
from devices import save_device


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
    client.subscribe('/devices')

def on_message(client, userdata, message):
    try:
        decoded_message = str(message.payload.decode('utf-8', 'ignore'))
        device = json.loads(decoded_message)
        print(f'Received device: {device}')
        save_device(device)
        print('✅ Device saved')
    except BaseException as exception:
        print(exception)


client = authenticate(mqtt.Client())
client.enable_logger()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883)

print('👂🚀 Listening for devices')
client.loop_forever()
