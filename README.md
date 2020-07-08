# Earthquake detection for OpenEEW 
This is a simple docker-compose configuration to startup a new OpenEEW detection system. It ingests data from OpenEEW sensors via an MQTT broker, and triggers for individual sensors using a detection method. These events are then sent to a multi-station logic script that checks time and distance proximity for sensors before declaring an earthquake.
  
## Quick start
Install [Docker](https://www.docker.com/get-started) and run a detector container with the following command.

```shell script
docker run \
  --interactive \
  --tty \
  --detach \
  --env username=admin \
  --env password=admin \
  --publish 1883:1883 \
  --name openeew-detector \
  openeew/detector
```

You can change the port published to host and the credentials. In the following example the detector listens on port
`8080` and the username and password used for authentication are `foo` and `bar`. 

```shell script
docker run \
  --interactive \
  --tty \
  --detach \
  --env username=foo \
  --env password=bar \
  --publish 8080:1883 \
  --name openeew-detector \
  openeew/detector
```

You can also omit the `username` and `password` parameters but that would be a **less secure** option and would allow
anyone to publish data to your detector. This setup is primary meant for development.

### Build your own Docker image

*For developers only*. Apply the changes to the `Dockerfile` and run the following command. 

```shell script
docker build --tag openeew/detector:dev .
```

Then run a development container:

```shell script
docker run \
  --interactive \
  --tty \
  --detach \
  --publish 1883:1883 \
  --name openeew-detector-dev \
  openeew/detector:dev
```

### Simulate sensor data

Start a container as indicated above and then run the following on the *host* machine:

```shell script
cd scripts
python3 sensor_simulator.py --username admin --password admin --port 1883
```

## Components

![MQTT](images/mqtt_workflow.png?raw=true "Diagram")
<p align="center"> 
  
## Incoming sensor data
### Sensor data
[The data](https://openeew.com/docs/historic-data#how-are-records-generated) comprises records of acceleration in three channels representing sensor movement in the space. The channels are orthogonal (90 degrees from each other), two components are horizontal, x and y, and one vertical, z. The units are gals, centimeter per second squared.

### MQTT Broker
OpenEEW sensor data is ingested via a [Mosquitto MQTT broker](https://mosquitto.org/) with the topic `/traces`.

## Detection script
A python script subscribes to `/traces` and runs 2 processes against each incoming message; an STA/LTA, and a PGA trigger.

### Single sensor process - STA/LTA
First we run a Short-Term Average/Long-Term Average (STA/LTA) algorithm .This method is widely used to identify any disturbances in the signal (such as earthquakes) and determine the time when an event starts.

![STA/LTA x component](images/sta_lta_x.png?raw=true "Record M7.2 Pinotepa Nacional, Oaxaca, Mexico (16-02-2018)")
<p align="center">
  
The algorithm takes each channel independently (x, y and z) and applies the moving average using two windows and returns the ratio as a function. Based on the part of the signal where there is no earthquake, a trigger level can be defined.

### Single sensor process - Shaking level
The maximum acceleration, or Peak Ground Acceleration (PGA) `(x**2 + y**2 + z**2)**0.5)` is used to determine the level of shaking that needs to be updated after a triggering using the three components at the same time. 

The output from this process is sent as a  value (PGA) using the topic `/pga-trigger`.

To be added.

### Multi sensor process - Earthquake confirmation
To be added.

## Output
To be added

### Authors
- [Grillo](https://grillo.io)
- [Egidio Caprino](https://github.com/EgidioCaprino)
___

Enjoy!  Give us [feedback](https://github.com/openeew/openeew-detection/issues) if you have suggestions on how to improve this information.

## License

This information is licensed under the Apache Software License, Version 2.  Separate third party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1 (DCO)](https://developercertificate.org/) and the [Apache Software License, Version 2](http://www.apache.org/licenses/LICENSE-2.0.txt).
