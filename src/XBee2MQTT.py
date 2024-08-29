import sys
import getopt
from SIGINTHandler import RegisterSIGINTHandler
import XBee.LocalZigbeeDevice as LocalZigbeeDevice
import MQTTHelper
from XBee.XBeeDeviceManager import XBeeDeviceManager
import logging
from LogHelper import SetLogLevel
from configmanager import ConfigurationManager

device_config = {}
__exit_code = 0


def main():

    try:

        SetLogLevel("DEBUG")

        config_path = GetOpts()

        cm = InitializeConfigManager(config_path)

        sigint_handler = RegisterSIGINTHandler()

        MainProgramLoop(cm, sigint_handler)

    except Exception as ex:
        logging.error(ex)
        __exit_code = 2

    sys.exit(__exit_code)


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

            # MQTTHelper.set_callback(on_message)

            XBeeDeviceManager()


def InitializeConfigManager(config_path):
    try:
        logging.debug("Init config manager")
        cm = ConfigurationManager(config_path)
        logging.debug("Loading config")
        cm.load_config()
    except Exception as ex:
        logging.error(ex)
        raise
    return cm


def GetOpts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ["config="])
    except getopt.GetoptError:
        logging.debug('Xbee2MQTT.py -c <config-path>')
        raise

    for opt, arg in opts:
        if opt in ("-c", "--config"):
            config_path = arg

    logging.debug(f'Config path = {config_path}')

    if config_path == "":
        logging.debug("Config path is required")
        raise
    return config_path


if __name__ == "__main__":
    main()
