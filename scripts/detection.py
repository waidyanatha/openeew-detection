import paho.mqtt.client as mqtt
import time
import json
import numpy
import argparse

from trigger import sta_lta
from trigger import trigger_time
from trigger import accel_value


# initializing empty variables
inbox = []

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

def set_time(times, sr, N):
    """
    times = time stamps by fifo in each payload 
    sr = sample rate 
    N = number of data samples
    """
    
    # number of fifos
    nfifo = len(times)
    
    # create an empty variable to allocate the 
    diff = []
    
    if nfifo > 1:
        # Loop over the times of each fifo 
        for i, item in enumerate(times[0:-1]):
            diff.append(times[i+1] - item)
        
        # Estimate the delta t per data tupple
        delta_t = numpy.mean(diff) / (N/nfifo)
    else: 
        delta_t = 1 / sr
        times.append(times[0] + N*delta_t)
    
    # Defines the time for each tupple
    t = numpy.arange(times[0] - ((N/nfifo))*delta_t, times[-1]+delta_t, delta_t).tolist()
    
    return t


def parser_json(payload):
    '''
    Parser payload from mqtt
    Format json 
    Returns:
        device_id
        cloud_t
        traces 
        sr 
    where:
    traces =  {"t" : numpy.array(t), "x" : numpy.array(x), "y" : numpy.array(y), "z" : numpy.array(z)}
    
    '''
    payload = json.loads(payload)
    device_id = payload["device_id"]
    cloud_t = payload["cloud_t"]
    
    # jsonl from esp32 sensors
    if len(payload) == 3: 
        _x = []
        _y = []
        _z = []
        _t = []
        
        for i, item in enumerate(payload["traces"]):
            _x.append(item["x"])
            _y.append(item["y"])
            _z.append(item["z"])
            _t.append(item["t"])
            sr = item["sr"]
        
        x = [item for sublist in _x for item in sublist]
        y = [item for sublist in _y for item in sublist]
        z = [item for sublist in _z for item in sublist]
        
        # Set times per each data tupple (x, y and z)
        t = set_time(_t, sr, len(x))
        
        traces = {"t" : t, "x" : x, "y" : y, "z" : z}
    
    # jsonl from rp sensors
    elif len(payload) == 8:

        sr = payload["sr"]
        x = payload["x"]
        y = payload["y"]
        z = payload["z"]
        _t = [payload["device_t"]]
        t = set_time(_t, sr, len(x))
    
        traces = {"t" : t, "x" : x, "y" : y, "z" : z}
    
    return device_id, cloud_t, traces, sr


def on_connect(client, userdata, flags, rc):
    client.subscribe("/traces")


def on_publish(host, port, topic, data_out):
    '''
    '''
    client.publish(topic,data_out)


def on_message(client, userdata, msg):
    
    m_decode = str(msg.payload.decode("utf-8","ignore"))
    m_in = json.loads(m_decode)
    
    # appending msg 
    # Missing check if the msgs are from different sensors
    inbox.append(m_in)
    
    # When the msgs are more or equal than the long window
    if len(inbox) >= long_window:
        # Empty variables for the last 10 seconds
        _x = []
        _y = []
        _z = []
        _t = []
        # Looping over the inbox elements
        for i, item in enumerate(inbox):
            device_id, cloud_t, traces, sr = parser_json(item)
            #print(i, device_id)

            _x.extend(traces["x"])
            _y.extend(traces["y"])
            _z.extend(traces["z"])
            _t.extend(traces["t"])
        
        print("Device id:", device_id)

        # -------------- MOVING WINDOW -----------------------------
        # Select the last seconds and rename
        n = len(traces["x"])
        x = _x[-n*long_window:]
        y = _y[-n*long_window:]
        z = _z[-n*long_window:]
        t = _t[-n*long_window:]
        #print("Longitude:", len(x), len(y), len(z), len(t))
        
        # -------------- TRIGGER SECTION -----------------------------
        # STA / LTA algorithm
        x_sta_lta = sta_lta(numpy.array(x), short_window*n, long_window*n)
        y_sta_lta = sta_lta(numpy.array(y), short_window*n, long_window*n)
        z_sta_lta = sta_lta(numpy.array(z), short_window*n, long_window*n)

        
        # Estimating trigger times given a trigger level
        ttimes_x = trigger_time(x_sta_lta, numpy.array(t), trigger_level)
        ttimes_y = trigger_time(y_sta_lta, numpy.array(t), trigger_level)
        ttimes_z = trigger_time(z_sta_lta, numpy.array(t), trigger_level)

        # -------------- CHARACTERIZATION SECTION -----------------------------
        nttimes = len(ttimes_x) + len(ttimes_y) + len(ttimes_z) 
        if nttimes > 0:
            print("------------> Trigger of %s components. Sensor %s. Time %s" % (nttimes, device_id, cloud_t))
            accel = accel_value(numpy.array(x), numpy.array(y), numpy.array(z))
            pga = numpy.round(numpy.max(accel),3)
            print("Acceleration: ", pga)

            # --------------PUBLISH SECTION -----------------------------
            data_out = {"device_id" : numpy.str(device_id),"time" : numpy.str(cloud_t), "pga" : numpy.str(pga)}
            # topic
            topic = "/pga-trigger"
            host = "localhost"  
            port = 1883  
            client.on_publish = on_publish(host, port, topic, numpy.str(data_out))


# --------------MQTT SECTION ----------------------------- 
client = authenticate(mqtt.Client())
client.on_message = on_message
client.on_connect = on_connect
client.connect("localhost", 1883)

client.loop_start()

print('init')

# Continue loop 
while True: 
    if len(inbox) <= long_window:
        continue
    else: 
        inbox = inbox[-long_window:]


client.disconnect()
client.loop_stop()