import sys, getopt
from SIGINTHandler import RegisterSIGINTHandler
import LocalZigbeeDevice
import MQTTHelper
from XBeeDeviceManager import XBeeDeviceManager
import logging
from LogHelper import SetLogLevel
from ConfigurationManager import ConfigurationManager

device_config = {}


def main():
    exit_code = 0
    
    try:

        SetLogLevel("DEBUG")

        config_path = GetOpts()

        cm = InitializeConfigManager(config_path)
        
        sigint_handler = RegisterSIGINTHandler()

        MainProgramLoop(cm, sigint_handler)

    except Exception as ex:
           logging.error(ex)
           exit_code = 2

    sys.exit(exit_code)

def MainProgramLoop(cm, sigint_handler):

    firstLoop = True
    while not sigint_handler.SIGINT:

        if firstLoop:
            firstLoop = False

            SetLogLevel(cm.log_level)

            logging.debug("Initializing Zigbee device")
            LocalZigbeeDevice.Initialize(cm)
                
            logging.debug("Connecting to MQTT broker")
            MQTTHelper.connect(cm.mqtt_broker, int(cm.mqtt_port))

            XBeeDeviceManager()

def InitializeConfigManager(config_path):
    try:
        logging.debug("Init config manager")
        cm = ConfigurationManager(config_path)
        logging.debug("Loading config")
        cm.load_config()
    except Exception as ex:
        logging.error(ex)
        exit_code = 2
        raise
    return cm

def GetOpts():
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
    return config_path
   
if __name__ == "__main__":
  main()
