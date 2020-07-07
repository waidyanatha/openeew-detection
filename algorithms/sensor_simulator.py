import paho.mqtt.client as mqtt
import time
import json

def convert_str2json(openeewJSON_out):
	'''
	
	'''
	#print(openeewJSON_out)
	#print("openeewJSON_out is a ",type(openeewJSON_out))
	data_out=json.dumps(openeewJSON_out)# encode oject to JSON
	#print("\nConverting to JSON\n")
	#print ("data -type ",type(data_out))
	#print ("data out =",data_out)

	return data_out


def publish(host, port, topic, data_out):
	'''
	'''
	client=mqtt.Client()
	client.connect(host, port)
	client.loop_start()
	#time.sleep(1)
	print("sending data this is publish")
	client.publish(topic,data_out)
	time.sleep(1)
	#client.loop_stop()
	#client.disconnect()

def read(file_name):
    '''
    Read a file containing json per line with msgs from sensors
    line per second
    '''
    with open(file_name, "r") as fo:
        for line in fo:
            #Convert string to json
            data_out = convert_str2json(line)
            # topic
            topic = "/traces"
            host = "localhost" 	
            port = 1883	 
            publish(host, port, topic, data_out)


# Location of the jsonl file containing json per line with msgs from sensors
file_name = "input/grillo_alert_traces-1-2020-06-04-14-43-48-e651eb58-59ac-43cb-b52d-97998e40d801-3ef3d787af85" # 4.2M Puerto Rico 2020-06-04 14:43:48 hr
read(file_name)
