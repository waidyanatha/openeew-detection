import paho.mqtt.client as mqtt
import numpy
import csv
import json

def parser_json(payload):
    '''
    Parser payload from mqtt
    Format json 
    Returns:
        device_id
        time
        pga 
    '''
    m_in = json.loads(payload) 

    device_id = m_in["device_id"]
    time = m_in["time"]
    pga = m_in["pga"]

    return device_id, time, pga

def read_sensor_coordinates(filename):
    '''
    filename contains the location of the file with a csv with 
    device id and coordinates (latitude and longitude) of grillo sensors 
    '''

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        
        device_id = []
        lat = []
        lon = []
        
        for row in readCSV:
            dat1, dat2, dat3 = row
            device_id.append(numpy.str(dat1))
            lat.append(numpy.float(dat2))
            lon.append(numpy.float(dat3))
                
    return numpy.array(device_id), numpy.array(lat), numpy.array(lon)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/pga-trigger")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic, msg.payload)
    m_decode = msg.payload.decode("utf-8","ignore")
    m_decode = m_decode.replace("'", '"')
    # Json parser to extract info
    device_id, time, pga = parser_json(m_decode)


# MQTT SECTIONS
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_start()

# Continue loop 
while True: 
    continue

#client.disconnect()
#client.loop_stop()
