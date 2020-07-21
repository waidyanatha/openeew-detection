import paho.mqtt.client as mqtt

# Subscribed to 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/pga-trigger")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	#print("Mensaje recibido")
	print(msg.topic, msg.payload)


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
