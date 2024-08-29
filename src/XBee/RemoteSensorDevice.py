from digi.xbee.io import IOLine
import MQTTHelper
import logging


class XBeeSensorDevice():

    def __init__(self, remote_address, name):
        self.remote_address = remote_address
        self.name = name
        self.payload_available = "online"
        self.payload_unavailable = "offline"

    def ProcessIncommingIOSample(self, io_sample):
        for channel in io_sample.analog_values:
            new_reading = io_sample.get_analog_value(channel)
            device_channel = self.adc_channels.get(channel)

            logging.debug(f"New reading received on channel \
                          {str(device_channel.io_line)} = {new_reading} \
                            - Publishing to \
                            {device_channel.raw_adc_value_topic}")
            MQTTHelper.client.publish(device_channel.raw_adc_value_topic,
                                      new_reading)

            new_binary_value = False
            if new_reading > device_channel.threshold:
                new_binary_value = device_channel.greater_than_value
            else:
                new_binary_value = not device_channel.greater_than_value

            if new_binary_value != device_channel.last_binary_value:
                logging.debug(
                    f"Sample changed, publishing for channel {channel},\
                          last reading: {device_channel.last_binary_value}, \
                            new reading: {new_binary_value} to \
                                 {self.adc_channels[channel].state_topic}")
                self.adc_channels[channel].last_reading = new_reading
                self.adc_channels[channel].last_binary_value = new_binary_value
                MQTTHelper.client.publish(
                    self.adc_channels[channel].state_topic,
                    new_binary_value, 1, True)


class RemoteIOSensorDevice(XBeeSensorDevice):

    def __init__(self, name, remote_address, adc_channels: dict):
        super().__init__(remote_address, name)
        self.adc_channels = adc_channels


class RemoteIOSensorChannel():

    def __init__(self, io_line: IOLine, name, state_topic,
                 raw_adc_value_topic, qos: int, device_class: str):
        self.io_line = io_line
        self.name = name
        self.state_topic = state_topic
        self.raw_adc_value_topic = raw_adc_value_topic
        self.qos = qos
        self.device_class = device_class
        self.payload_on = True
        self.payload_off = False
        self.last_reading = -1


class ADCBinarySensorChannel(RemoteIOSensorChannel):

    def __init__(self, io_line: IOLine, name,
                 state_topic, raw_adc_value_topic, qos,
                 device_class, threshold, greater_than_value: bool):
        super().__init__(io_line, name, state_topic, raw_adc_value_topic,
                         qos, device_class)
        self.threshold = threshold
        self.greater_than_value = greater_than_value
        self.last_binary_value = None


class ADCDecimalSensorChannel(RemoteIOSensorChannel):
    pass


class DIOBinarySensorChannel(RemoteIOSensorChannel):
    pass
