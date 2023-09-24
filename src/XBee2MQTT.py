import sys, getopt
import time
import signal
from tracemalloc import reset_peak
from HomeAssistantAutoDiscovery import perform_auto_discovery
from SIGINTHandler import SIGINT_handler
import LocalZigbeeDevice
import MQTTHelper
from XBeeDeviceManager import XBeeDeviceManager
import logging

import json
import io
from ConfigurationManager import ConfigurationManager

device_config = {}


def main():
    try:

        
        logging.setLevel(logging.DEBUG)
        
        exit_code = 0
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'c:', ["config="])
        except getopt.GetoptError:
            logging.debug('Xbee2MQTT.py -c <config-path>')
            exit_code = 2
            raise

        for opt, arg in opts:
            if opt in ("-c", "--config"):
                config_path = arg
        
        logging.debug(f'Config path = {config_path}')

        if config_path == "":
            logging.debug("Config path is required")
            exit_code = 2
            raise

        try:
            cm = ConfigurationManager(config_path)
            cm.load_config
        except Exception as ex:
            logging.error(ex)
            exit_code = 2
            raise
        
        logging.debug(f'Setting log level to {cm.log_level}')
        logging.setLevel(cm.log_level)
        
        logging.debug("Registering SIGINT handler")
        handler = SIGINT_handler()
        signal.signal(signal.SIGINT, handler.signal_handler)

        logging.debug("Initializing Zigbee device")
        LocalZigbeeDevice.Initialize(cm)
        
        logging.debug("Connecting to MQTT broker")
        MQTTHelper.connect(cm.mqtt_broker, int(cm.mqtt_port))

        #XBeeDeviceManager(config_path)
        
        #while True:
        #    if handler.SIGINT:
        #        MQTTHelper.client.loop_stop()
        #        break
        #    time.sleep(0.1)

    except Exception as ex:
        logging.error(ex)
        exit_code = 2

    sys.exit(exit_code)
    
if __name__ == "__main__":
  main()
