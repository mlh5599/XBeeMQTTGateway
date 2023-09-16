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
from ConfigurationManager import load_config

device_config = {}
def io_sample_received_callback(io_sample : IOSample, remote_xbee : RemoteXBeeDevice, send_time):
    print("Callback received")
    print("Calling Device = %s" % remote_xbee.get_64bit_addr())

    device = XBeeDeviceManager.GetRegisteredDevice(str(remote_xbee.get_64bit_addr()))
    
    if device == None:

        device = XBeeDeviceManager.RegisterDevice(io_sample, remote_xbee)

    device.ProcessIncommingIOSample(io_sample)

config_path = ""
app_config = {}

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ["config="])
    except getopt.GetoptError:
        print('Xbee2MQTT.py -c <config-path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-c", "--config"):
            config_path = arg

    if config_path == "":
        print("Config path is required")
        sys.exit(2)

    try:
        app_config = load_config(config_path)
    except Exception as ex:
        print(ex)
        sys.exit(2)

    handler = SIGINT_handler()
    signal.signal(signal.SIGINT, handler.signal_handler)
    
    pi = pigpio.pi()

    LocalZigbeeDevice.Initialize(app_config["DevicePort"], app_config["DeviceBaudRate"], io_sample_received_callback, app_config["XBeeResetPin"], pi)
    
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
