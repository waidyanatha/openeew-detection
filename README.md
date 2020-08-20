![](https://github.com/openeew/openeew-detection/workflows/CI/badge.svg)
# Earthquake detection for OpenEEW
This is a simple Docker configuration to startup a new OpenEEW detection system on your local machine. It ingests data from OpenEEW sensors via an MQTT broker, and triggers for individual sensors using a detection method. These events are then sent to a multi-station logic script that checks time and distance proximity for sensors before declaring an earthquake. You can also [deploy the Docker container on Kubernetes](KUBERNETES.md) to target a publicly accessible endpoint.

The OpenEEW strategy for accurately detecting earthquakes while avoiding false positives is to use a variety of tactics, including:
* Filtering out non-earthquake vibrations by using [STA/LTA (Short-Term Average/Long-Term Average)](#stalta)
* Detecting peak accelerations ([PGAs](#shaking-level)) above a certain threshold from the sensors
* Aggregating readings from [multiple nearby sensors](#multistation-for-multiple-sensor-comparison)
  
## Quick start
Install [Docker](https://www.docker.com/get-started) and run a detector container with the following command.

```shell-script
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
`8080` and the username and password created for authentication are `foo` and `bar`. 

```shell-script
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

The Docker image contains a PostgreSQL database which is used to store devices and events. You can find its structure
[here](https://github.com/openeew/openeew-detection/blob/master/init_db.sql).

### Build your own Docker image

*For developers only*. Apply the changes to the `Dockerfile` and run the following command. 

```shell-script
docker build --tag openeew/detector:dev .
```

Then run a development container:

```shell-script
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

```shell-script
cd openeew
python3 sensor_simulator.py --username admin --password admin --earthquake 2018_7.2 --port 1883
```

Note: You may need to install the Paho MQTT client. For example, `pip install paho-mqtt`

[The data](https://openeew.com/docs/historic-data#how-are-records-generated) comprises records of acceleration in three channels representing sensor movement in the space. The channels are orthogonal (90 degrees from each other), two components are horizontal, x and y, and one vertical, z. The units are gals, centimeter per second squared. This is true of both the simulated sensor data, and actual sensor data. The script will send data at the rate of one message from each sensor per second.

## Run unit tests

```shell script
PYTHONPATH=./openeew python -m unittest
```

## Components

![MQTT](images/mqtt_workflow2.png?raw=true "Diagram")
<p align="center"> 

### Sensor simulator
`sensor_simulator.py` selects historic data from [/input](https://github.com/openeew/openeew-detection/tree/master/input) and publishes them to MQTT at an accurate rate (1 msg per sensor per second).

### MQTT broker
A [Mosquitto MQTT broker](https://mosquitto.org/) administers the following topics:
- `/traces` (raw accelerations from sensor, time, deviceid)
- `/device` (device metadata; deviceid, lat, lon, firmware version)
- `/pga-trigger` (threshold triggered for sensor; deviceid, pga intensity, time)
- `/earthquake` (earthquake declared by comparing recent pga-triggers from various devices; eventid, time of event, pga intensity)

### Device information to database
`DBwriter.py` updates the `devices` [table](https://github.com/openeew/openeew-detection/blob/master/init_db.sql) in the database with meta data for each sensor, including its location coordinates. This script also writes earthquake events to the database as they happen.

### Detection script for single sensors
The `detection.py` script runs a Short-Term Average/Long-Term Average STA/LTA algorithm followed by a Peak Ground Acceleration (PGA) calculation.

#### STA/LTA 
This method is widely used to identify any disturbances in the signal (such as earthquakes) and determine the time when an event starts.

![STA/LTA x component](images/sta_lta_x.png?raw=true "Record M7.2 Pinotepa Nacional, Oaxaca, Mexico (16-02-2018)")
<p align="center">
  
The algorithm takes each channel independently (x, y and z) and applies the moving average using two windows and returns the ratio as a function. Based on the part of the signal where there is no earthquake, a trigger level can be defined.

#### Shaking level
The maximum acceleration, or Peak Ground Acceleration (PGA) `(x**2 + y**2 + z**2)**0.5)` is used to determine the level of shaking that needs to be updated after a triggering using the three components at the same time. 

The output from this process is sent as a  value (PGA) using the topic `/pga-trigger`.

### Multistation for multiple sensor comparison
The `multistation.py` script subscribes to `/pga-trigger` to determine if an earthquake is occuring. This is done by evaluating distance and time between each `pga-trigger` msg. To get latitude and longitude, the script must read from the `devices` table in the database.

The outcome of this script is a confirmed earthquake event. This is sent by msg to the `/earthquake` topic.


## Alternative detection implementations
### JavaScript
The [openeew-nodered README]( https://github.com/openeew/openeew-nodered) contains an example of how to implement the PGA algorithm in JavaScript. 


### Authors
- [Grillo](https://grillo.io)
- [Egidio Caprino](https://github.com/EgidioCaprino)
___

Enjoy!  Give us [feedback](https://github.com/openeew/openeew-detection/issues) if you have suggestions on how to improve this information. Here are some [guidelines for contributing algorithms](openeew/README.md).

## License

This information is licensed under the Apache Software License, Version 2.  Separate third party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1 (DCO)](https://developercertificate.org/) and the [Apache Software License, Version 2](http://www.apache.org/licenses/LICENSE-2.0.txt).
