import paho.mqtt.client as mqtt
import time
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--username", help="MQTT username")
parser.add_argument("--password", help="MQTT password")
parser.add_argument("--port", help="MQTT port", nargs="?", type=int, const=1883, default=1883)
args = parser.parse_args()
client = mqtt.Client()
if args.username and args.password:
	client.username_pw_set(username=args.username, password=args.password)
client.connect("localhost", args.port)

def convert_str2json(openeewJSON_out):
	data_out=json.dumps(openeewJSON_out)# encode oject to JSON
	return data_out

def publish(topic, data_out):
	client.loop_start()
	print("sending data this is publish")
	client.publish(topic,data_out)
	time.sleep(1)
	
def read(file_name):
    '''
    Read a file containing json per line with msgs from sensors
    line per second
    '''
    with open(file_name, "r") as fo:
        for line in fo:
            data_out = convert_str2json(line)
            topic = "/traces"
            publish(topic, data_out)

# Location of the jsonl file containing json per line with msgs from sensors
file_name = "input/grillo_alert_traces-1-2020-06-04-14-43-48-e651eb58-59ac-43cb-b52d-97998e40d801-3ef3d787af85" # 4.2M Puerto Rico 2020-06-04 14:43:48 hr
read(file_name)
