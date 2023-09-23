# XBeeMQTTGateway
XBee to MQTT gateway


## Dependencies
### pigpiod
sudo apt-get install pigpio\
sudo systemctl enable pigpiod.service\
sudo systemctl start pigpiod.service

### paho-mqtt
pip install paho-mqtt

### digi-xbee
pip install digi-xbee

## Setup
### Enable Serial Port
sudo raspi-setup
  -> Interface Options -> I6 Serial Port
    -> Disable login shell through serial
    -> Enable serial hardware

sudo usermod -aG dialout <username>
sudo usermod -aG tty <username>
  
## Wiring
### Rasperry Pi Model 1B

Schematic
![Screenshot](/Schematics/SchematicScreenshot)

Breadboard Layout
![Screenshot](/Schematics/BreadboardScreenshot)
