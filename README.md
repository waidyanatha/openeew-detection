# Earthquake detection for OpenEEW 
This is a simple docker-compose configuration to startup a new OpenEEW detection system. It ingests data from OpenEEW sensors via an MQTT broker, and triggers for individual sensors using a detection method. These events are then sent to a multi-station logic script that checks time and distance proximity for sensors before declaring an earthquake.

![MQQT](images/mqqt_workflow.png?raw=true "Diagram")
<p align="center"> 

## Incoming sensor data
### Content
[The data](https://openeew.com/docs/historic-data#how-are-records-generated) comprises records of acceleration in three channels representing sensor movement in the space. The channels are orthogonal (90 degrees from each other), two components are horizontal, x and y, and one vertical, z. The units are gals, centimeter per second squared.

### MQTT Broker
OpenEEW sensor data is ingested via a [Mosquitto MQTT broker](https://mosquitto.org/) with the topic `/traces`.

## Detection script
A python script subscribes to `/traces` and runs 2 processes against each incoming message; an STA/LTA, and a PGA trigger.

### 1. Single sensor process - STA/LTA
First we run a Short-Term Average/Long-Term Average (STA/LTA) algorithm .This method is widely used to identify any disturbances in the signal (such as earthquakes) and determine the time when an event starts.

![STA/LTA x component](images/sta_lta_x.png?raw=true "Record M7.2 Pinotepa Nacional, Oaxaca, Mexico (16-02-2018)")
<p align="center">
  
The algorithm takes each channel independently (x, y and z) and applies the moving average using two windows and returns the ratio as a function. Based on the part of the signal where there is no earthquake, a trigger level can be defined.

### 2. Single sensor process - Shaking level
The maximum acceleration, or Peak Ground Acceleration (PGA) `(x**2 + y**2 + z**2)**0.5)` is used to determine the level of shaking that needs to be updated after a triggering using the three components at the same time. 

The output from this process is sent as a  value (PGA) using the topic `/pga-trigger`.

### 3. Earthquake confirmation - Multi sensor process 
To be added.


### Authors
- [Grillo](https://grillo.io)
___

Enjoy!  Give us [feedback](https://github.com/openeew/openeew-detection/issues) if you have suggestions on how to improve this information.

## License

This information is licensed under the Apache Software License, Version 2.  Separate third party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1 (DCO)](https://developercertificate.org/) and the [Apache Software License, Version 2](http://www.apache.org/licenses/LICENSE-2.0.txt).
