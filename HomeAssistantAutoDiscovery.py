from RemoteSensorDevice import RemoteIOSensorDevice
from digi.xbee.io import IOLine
import json
import MQTTHelper
import time

def perform_auto_discovery(remote_xbee_device : RemoteIOSensorDevice):

    # master_bathroom_topic = f"homeassistant/binary_sensor/xbee-0x{remote_xbee_device.remote_address}/masterbathroomshower/config"

    for channel in remote_xbee_device.adc_channels:
        device_channel = remote_xbee_device.adc_channels.get(channel)
        xbee_address = remote_xbee_device.remote_address
        sensor = {
            "device": {
                "identifiers": [
                    f"zigbee2mqtt_0x{remote_xbee_device.remote_address}"
                ],
                "manufacturer": "Me",
                "model": "XBee Sensor",
                "name": remote_xbee_device.name
            },
            "device_class": "running",
            "name": str(device_channel.io_line).replace('.','-'),
            "payload_off": device_channel.payload_off,
            "payload_on" : device_channel.payload_on,
            "state_topic": device_channel.state_topic,
            "unique_id": f"0x{remote_xbee_device.remote_address}-{str(device_channel.io_line).replace('.','-')}"
        }

        json_string = json.dumps(sensor)
        discovery_topic = f"homeassistant/binary_sensor/xbee-0x{xbee_address}/{str(device_channel.io_line).replace('.','-')}/config"
        print(f"Publishing auto discovery for 0x{xbee_address} - {str(device_channel.io_line).replace('.','-')} to topic : {discovery_topic}")
        print(json_string)
        MQTTHelper.client.publish(discovery_topic, json_string)
        
        time.sleep(1)

        device_channel = remote_xbee_device.adc_channels.get(channel)
        xbee_address = remote_xbee_device.remote_address
        sensor = {
            "device": {
                "identifiers": [
                    f"zigbee2mqtt_0x{remote_xbee_device.remote_address}"
                ],
                "manufacturer": "Me",
                "model": "XBee Sensor",
                "name": remote_xbee_device.name
            },
            "device_class": "running",
            "name": f"{str(device_channel.io_line).replace('.','-')}-raw_adc",
            "payload_off": device_channel.payload_off,
            "payload_on" : device_channel.payload_on,
            "json_attributes_topic": device_channel.raw_adc_value_topic,
            "state_topic": device_channel.raw_adc_value_topic,
            "unique_id": f"0x{remote_xbee_device.remote_address}-{str(device_channel.io_line).replace('.','-')}-raw_adc"
        }
        json_string = json.dumps(sensor)
        discovery_topic = f"homeassistant/binary_sensor/xbee-0x{xbee_address}/{str(device_channel.io_line).replace('.','-')}-raw/config"
        print(f"Publishing auto discovery for 0x{xbee_address} - {str(device_channel.io_line).replace('.','-')} to topic : {discovery_topic}")
        print(json_string)

        MQTTHelper.client.publish(discovery_topic, json_string, 1, True)

        time.sleep(1)
    