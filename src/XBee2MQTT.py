import sys, getopt
import time
import signal
from tracemalloc import reset_peak
from HomeAssistantAutoDiscovery import perform_auto_discovery
from SIGINTHandler import SIGINT_handler
import LocalZigbeeDevice
import MQTTHelper
from XBeeDeviceManager import XBeeDeviceManager


import json
import io
import pigpio
from ConfigurationManager import ConfigurationManager

device_config = {}


def main():
    try:

        exit_code = 0
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'c:', ["config="])
        except getopt.GetoptError:
            print('Xbee2MQTT.py -c <config-path>')
            exit_code = 2
            raise

        for opt, arg in opts:
            if opt in ("-c", "--config"):
                config_path = arg

        if config_path == "":
            print("Config path is required")
            exit_code = 2
            raise

        try:
            cm = ConfigurationManager(config_path)
            app_config = cm.load_config()
        except Exception as ex:
            print(ex)
            exit_code = 2
            raise

        handler = SIGINT_handler()
        signal.signal(signal.SIGINT, handler.signal_handler)
        
        pi = pigpio.pi()

        LocalZigbeeDevice.Initialize(app_config["DevicePort"], app_config["DeviceBaudRate"], app_config["XBeeResetPin"], pi)
        
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

    except Exception as ex:
        print(ex)
        exit_code = 2

    sys.exit(exit_code)
    
if __name__ == "__main__":
  main()
