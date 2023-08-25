from configparser import ConfigParser
from digi.xbee.devices import RemoteXBeeDevice
from HomeAssistantAutoDiscovery import perform_auto_discovery
from RemoteSensorDevice import ADCBinarySensorChannel, RemoteIOSensorDevice, XBeeSensorDevice
from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.io import IOLine
from digi.xbee.io import IOSample
import json
from os.path import exists

class XBeeDeviceManager():

    __registered_devices = {}

    def __init__(self, config):
        pass

    def LoadRegisteredDevices(self, config_path):
        self.config_path = config_path
        if exists(config_path):
            with open(config_path, 'r') as openfile:
                self.device_config_json = json.load(openfile)
        else:
            self.device_config_json = ""


    def RegisterDevice(io_sample : IOSample, remote_xbee : RemoteXBeeDevice):
        
        
        channels = {}

        remote_xbee.read_device_info()

        for channel in io_sample.analog_values:
            state_topic = f"myhome/{remote_xbee.get_64bit_addr()}/{str(channel).replace('.','-')}/state"
            raw_adc_value_topic = f"myhome/{remote_xbee.get_64bit_addr()}/{str(channel).replace('.','-')}/raw_adc_value"
            binary_sensor_channel = ADCBinarySensorChannel(channel, channel, state_topic, raw_adc_value_topic, 1, "sensor", 500, False)
            channels[binary_sensor_channel.io_line] = binary_sensor_channel
            binary_sensor_channel.last_reading = io_sample.get_analog_value(channel)
    
        device = RemoteIOSensorDevice(remote_xbee.get_node_id(), str(remote_xbee.get_64bit_addr()), channels)

        print(f"Registering remote device.  Address={device.remote_address}, Name={remote_xbee.get_node_id()}")
        XBeeDeviceManager.__registered_devices[device.remote_address] = device
        print(f"Current registered devices: {XBeeDeviceManager.__registered_devices}")
        perform_auto_discovery(device)

        return device

    def GetRegisteredDevice(address):
        device = XBeeDeviceManager.__registered_devices.get(address)
        print(f"Existing device lookup complete, found: {device}")
        return device