from digi.xbee.models.address import XBee64BitAddress
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.io import IOSample, IOLine
import logging

class XBeeReceiveBase():
    
    def __init__(self, remote_device : RemoteXBeeDevice):
        self.remote_device = remote_device

class XBeeIOSampleReceive(XBeeReceiveBase):

    def __init__(self, remote_device : RemoteXBeeDevice, io_sample : IOSample):
        XBeeReceiveBase.__init__(self, remote_device)
        self.io_sample = io_sample

    def get_mqtt_topic(self, base_topic):
        remote_address = self.remote_device.get_64bit_addr()
        full_topic = f"{base_topic}/test/{remote_address}"
        logging.debug(full_topic)
        return full_topic

    def get_mqtt_payload(self):
        value_string = "{"
        if self.io_sample.has_analog_values():

            value_string = f"{value_string} analog_values: ["
            for line in self.io_sample.analog_values:
                analog_value = self.io_sample.get_analog_value(line)
                value_string = f"{value_string}{line} : {analog_value}, "
                
            value_string = value_string.rstrip(", ")
            value_string = f"{value_string}],"

        if self.io_sample.has_digital_values():

            value_string = f"{value_string} digital_values: ["
            for line in self.io_sample.digital_values:
                digital_value = self.io_sample.get_digital_value(line)
                value_string = f"{value_string}{line} : {digital_value}, "
                
            value_string = value_string.rstrip(", ")
            value_string = f"{value_string}]"
        
        value_string = f"{value_string} }}"
        logging.debug(value_string)


