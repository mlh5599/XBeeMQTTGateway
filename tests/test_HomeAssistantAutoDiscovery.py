import pytest
from unittest.mock import patch, Mock
from HomeAssistantAutoDiscovery import perform_auto_discovery


class TestAutoDiscovery:

    # @patch('MQTTHelper.client.publish')
    # def test_publish_raw_adc(self, mock_publish):
    #     # Create a mock instance of RemoteIOSensorDevice
    #     remote_device = Mock()
    #     remote_device.remote_address = "12345678"
    #     remote_device.name = "TestDevice"
    #     remote_device.adc_channels = {
    #         'channel1': Mock(
    #             io_line=IOLine.DIO0_AD0,
    #             payload_off="OFF",
    #             payload_on="ON",
    #             raw_adc_value_topic="raw_adc_topic"
    #         )
    #     }

    #     # Call the function with the mock device and channel
    #     publish_raw_adc(remote_device, 'channel1')

    #     # Verify that MQTTHelper.client.publish was called with the expected
    #       arguments
    #     expected_discovery_topic = (
    #         "homeassistant/binary_sensor/xbee-0x12345678/IOLine-DIO0_AD0-raw/config"
    #     )
    #     expected_sensor_payload = {
    #         "device": {
    #             "identifiers": ["zigbee2mqtt_0x12345678"],
    #             "manufacturer": "RobotMikeIndustries",
    #             "model": "XBee Sensor",
    #             "name": "TestDevice"
    #         },
    #         "device_class": "running",
    #         "name": "IOLine-DIO0_AD0-raw",
    #         "payload_off": "OFF",
    #         "payload_on": "ON",
    #         "json_attributes_topic": "raw_adc_topic",
    #         "state_topic": "raw_adc_topic",
    #         "unique_id": "0x12345678-IOLine-DIO0_AD0-raw"
    #     }
    #     mock_publish.assert_called_once_with(
    #         expected_discovery_topic,
    #         str(expected_sensor_payload),
    #         1,
    #         True
    #     )

    # @patch('MQTTHelper.client.publish')
    # def test_publish_device_config(self, mock_publish):
    #     # Create a mock instance of RemoteIOSensorDevice
    #     remote_device = Mock()
    #     remote_device.remote_address = "12345678"
    #     remote_device.name = "TestDevice"
    #     remote_device.adc_channels = {
    #         'channel1': Mock(
    #             io_line=IOLine.DIO0_AD0,
    #             payload_off="OFF",
    #             payload_on="ON",
    #             state_topic="state_topic"
    #         )
    #     }

    #     # Call the function with the mock device and channel
    #     publish_device_config(remote_device, 'channel1')

    #     # Verify that MQTTHelper.client.publish was called with the expected\
    # arguments
    #     expected_discovery_topic = (
    #         "homeassistant/binary_sensor/xbee-0x12345678/IOLine-DIO0_AD0/config"
    #     )
    #     expected_sensor_payload = {
    #         "device": {
    #             "identifiers": ["zigbee2mqtt_0x12345678"],
    #             "manufacturer": "RobotMikeIndustries",
    #             "model": "XBee Sensor",
    #             "name": "TestDevice"
    #         },
    #         "device_class": "running",
    #         "name": "IOLine-DIO0_AD0",
    #         "payload_off": "OFF",
    #         "payload_on": "ON",
    #         "state_topic": "state_topic",
    #         "unique_id": "0x12345678-IOLine-DIO0_AD0"
    #     }
    #     mock_publish.assert_called_once_with(
    #         expected_discovery_topic,
    #         str(expected_sensor_payload),
    #     )

    @patch('time.sleep', side_effect=lambda x: None)
    @patch('HomeAssistantAutoDiscovery.publish_device_config')
    @patch('HomeAssistantAutoDiscovery.publish_raw_adc')
    def test_perform_auto_discovery(self, mock_publish_raw_adc,
                                    mock_publish_device_config, mock_sleep):
        # Create a mock instance of RemoteIOSensorDevice
        remote_device = Mock()
        remote_device.remote_address = "12345678"
        remote_device.name = "TestDevice"
        remote_device.adc_channels = {
            'channel1': Mock(),
            'channel2': Mock(),
            # Add more channels as needed
        }

        # Call the function with the mock device
        perform_auto_discovery(remote_device)

        # # Verify that publish_device_config and publish_raw_adc were called
        # with the expected arguments
        # expected_calls = [
        #     # Expected call for publish_device_config for channel1
        #     Mock().configure_mock(
        #         __name__='publish_device_config',
        #         call_args=(remote_device, 'channel1'),
        #     ),
        #     # Expected call for publish_raw_adc for channel1
        #     Mock().configure_mock(
        #         __name__='publish_raw_adc',
        #         call_args=(remote_device, 'channel1'),
        #     ),

        #     # Expected call for publish_raw_adc for channel2
        #     Mock().configure_mock(
        #         __name__='publish_raw_adc',
        #         call_args=(remote_device, 'channel2'),
        #     ),
        # ]
        assert mock_publish_device_config.call_count == 2
        assert mock_publish_raw_adc.call_count == 2

        # assert mock_publish_device_config.mock_calls == expected_calls
        # assert mock_publish_raw_adc.mock_calls == expected_calls


if __name__ == '__main__':
    pytest.main()


if __name__ == '__main__':
    pytest.main()
