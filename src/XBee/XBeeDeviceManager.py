from digi.xbee.devices import RemoteXBeeDevice
from HomeAssistantAutoDiscovery import perform_auto_discovery
from XBee.RemoteSensorDevice import ADCBinarySensorChannel, \
    RemoteIOSensorDevice
from digi.xbee.io import IOSample
import logging


class XBeeDeviceManager():

    registered_devices = {}

    def RegisterDevice(io_sample: IOSample, remote_xbee: RemoteXBeeDevice):

        channels = {}

        remote_xbee.read_device_info()

        for channel in io_sample.analog_values:
            state_topic = f"myhome/{remote_xbee.get_64bit_addr()}\
                /{str(channel).replace('.','-')}/state"
            raw_adc_value_topic = f"myhome/{remote_xbee.get_64bit_addr()}\
                /{str(channel).replace('.','-')}/raw_adc_value"
            binary_sensor_channel = ADCBinarySensorChannel(
                channel, channel, state_topic, raw_adc_value_topic,
                1, "sensor", 500, False)
            channels[binary_sensor_channel.io_line] = binary_sensor_channel
            binary_sensor_channel.last_reading = io_sample.get_analog_value(
                channel)

        device = RemoteIOSensorDevice(remote_xbee.get_node_id(),
                                      str(remote_xbee.get_64bit_addr()),
                                      channels)

        logging.debug(f"Registering remote device.  \
                      Address={device.remote_address}, \
                      Name={remote_xbee.get_node_id()}")
        XBeeDeviceManager.registered_devices[device.remote_address] = device
        logging.debug(f"Current registered devices: \
                      {XBeeDeviceManager.registered_devices}")
        perform_auto_discovery(device)

        return device

    def GetRegisteredDevice(address):
        device = XBeeDeviceManager.registered_devices.get(address)
        logging.debug(f"Existing device lookup complete, found: {device}")
        return device
