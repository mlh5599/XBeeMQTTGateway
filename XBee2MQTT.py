import sys, getopt
import time
import signal
from tracemalloc import reset_peak
from HomeAssistantAutoDiscovery import perform_auto_discovery
from SIGINTHandler import SIGINT_handler
import LocalZigbeeDevice
import MQTTHelper
from XBeeDeviceManager import XBeeDeviceManager
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.io import IOSample
import json
import io
import pigpio

app_config = {
    "DevicePort" : "COM6",
    "DeviceBaudRate" : "9600",
    "MQTTBroker" : "MQTT.HagueHome.lan",
    "MQTTPort" : "1883",
    "XBeeResetPin" : -1,
    "StatusLightPin" : -1
}

device_config = {}
def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice, send_time):
    print("Callback received")
    print("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)


def main():
# try::
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:d:r:m:p:x:l:', ["config=","device-port=","device-baud-rate=","mqtt-broker=","mqtt-broker-port=","xbee-reset-pin=","status-led-pin="])
    except getopt.GetoptError:
        print('Xbee2MQTT.py -c <config-path> -d <port> -r <device baud rate> -m <mqtt-broker> -p <mqtt-broker-port> -x <xbee-reset-pin> -l <status-led-pin>' )
        sys.exit(2)

    config_path = ""

    for opt, arg in opts:
        if opt in ("-d", "--port"):
            app_config["DevicePort"] = arg
        elif opt in ("-r", "--devict_baud_rate"):
            app_config["DeviceBaudRate"] = arg
        elif opt in ("-m", "--mqtt-broker"):
            app_config["MQTTBroker"] = arg
        elif opt in ("-p", "--mqtt-broker-port"):
            app_config["MQTTPort"] = arg
        elif opt in ("-c", "--config"):
            config_path = arg
        elif opt in ("-x", "--xbee-reset-pin"):
            app_config["XBeeResetPin"] = int(arg)
        elif opt in ("-l", "--status-led-pin"):
            app_config["StatusLightPin"] = int(arg)

    if config_path == "":
        print("Config path is required")
        sys.exit(2)

    handler = SIGINT_handler()
    signal.signal(signal.SIGINT, handler.signal_handler)

    LocalZigbeeDevice.Initialize(app_config["DevicePort"], app_config["DeviceBaudRate"], io_sample_received_callback, app_config["XBeeResetPin"])
    
    MQTTHelper.connect(app_config["MQTTBroker"], int(app_config["MQTTPort"]))

    status_pin = app_config["StatusLightPin"]
    if status_pin >= 0:
        pi.set_mode(status_pin, pigpio.OUTPUT)
        pi.write(status_pin, pigpio.HIGH)

    XBeeDeviceManager(config_path)
    
    while True:
        if handler.SIGINT:
            MQTTHelper.client.loop_stop()
            break
        time.sleep(0.1)

# except Exception as ex:
#     print(ex)`

if __name__ == "__main__":
  main()