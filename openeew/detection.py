import paho.mqtt.client as mqtt
import json
import numpy
import argparse

from trigger import sta_lta
from trigger import trigger_time
from trigger import accel_value
from mqtt import parser_json

# initializing empty variables
inbox = {}

# trigger parameters
long_window = 11
short_window = 1
trigger_level = 3


def authenticate(client):
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")
    args = parser.parse_args()
    if args.username and args.password:
        client.username_pw_set(username=args.username, password=args.password)
    return client


def on_connect(client, userdata, flags, rc):
    client.subscribe("/traces")


def on_publish(host, port, topic, data_out):
    '''
    '''
    client.publish(topic, data_out)


def on_message(client, userdata, msg):
    try:
        m_decode = str(msg.payload.decode('utf-8', 'ignore'))
        m_in = json.loads(m_decode)

        # appending msg
        device_id, _, _, _ = parser_json(m_in)
        if device_id not in inbox:
            inbox[device_id] = []
        inbox[device_id].append(m_in)

        for device_id, device_inbox in inbox.items():
            # When the msgs are more or equal than the long window
            if len(device_inbox) >= long_window:
                # Empty variables for the last 10 seconds
                _x = []
                _y = []
                _z = []
                _t = []
                # Looping over the inbox elements
                for i, item in enumerate(device_inbox):
                    device_id, cloud_t, traces, sr = parser_json(item)
                    _x.extend(traces["x"])
                    _y.extend(traces["y"])
                    _z.extend(traces["z"])
                    _t.extend(traces["t"])

                # -------------- MOVING WINDOW -----------------------------
                # Select the last seconds and rename
                n = len(traces["x"])
                x = _x[-n * long_window:]
                y = _y[-n * long_window:]
                z = _z[-n * long_window:]
                t = _t[-n * long_window:]
                # print("Longitude:", len(x), len(y), len(z), len(t))

                # -------------- TRIGGER SECTION -----------------------------
                # STA / LTA algorithm
                x_sta_lta = sta_lta(numpy.array(x), short_window * n, long_window * n)
                y_sta_lta = sta_lta(numpy.array(y), short_window * n, long_window * n)
                z_sta_lta = sta_lta(numpy.array(z), short_window * n, long_window * n)

                # Estimating trigger times given a trigger level
                ttimes_x = trigger_time(x_sta_lta, numpy.array(t), trigger_level)
                ttimes_y = trigger_time(y_sta_lta, numpy.array(t), trigger_level)
                ttimes_z = trigger_time(z_sta_lta, numpy.array(t), trigger_level)

                # -------------- CHARACTERIZATION SECTION -----------------------------
                nttimes = len(ttimes_x) + len(ttimes_y) + len(ttimes_z)

                if nttimes > 0:
                    print("------------> Trigger of %s components. Sensor %s. Time %s" % (nttimes, device_id, cloud_t))
                    accel = accel_value(numpy.array(x), numpy.array(y), numpy.array(z))
                    pga = numpy.round(numpy.max(accel), 3)
                    print("Acceleration: ", pga)

                    # --------------PUBLISH SECTION -----------------------------
                    data_out = {"device_id": numpy.str(device_id), "time": numpy.str(cloud_t), "pga": numpy.str(pga)}
                    # topic
                    topic = "/pga-trigger"
                    host = "localhost"
                    port = 1883
                    client.on_publish = on_publish(host, port, topic, numpy.str(data_out))
    except BaseException as exception:
        print(exception)


client = authenticate(mqtt.Client())
client.on_message = on_message
client.on_connect = on_connect
client.connect('localhost', 1883)

client.loop_start()

print('🚀 Detector started')

while True:
    for device_id in list(inbox):
        if len(inbox[device_id]) <= long_window:
            continue
        else:
            inbox[device_id] = inbox[device_id][-long_window:]
