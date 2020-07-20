import paho.mqtt.client as mqtt
import time
import json
import argparse
import sys

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
argument = sys.argv
file_name = argument[1]
read(file_name)