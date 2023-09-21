import pytest
from unittest.mock import patch, Mock
from XBeeDeviceManager import XBeeDeviceManager
from RemoteSensorDevice import ADCBinarySensorChannel, RemoteIOSensorDevice, XBeeSensorDevice
from digi.xbee.io import IOSample,IOLine
from digi.xbee.devices import RemoteXBeeDevice

class TestXBeeDeviceManager:

    @classmethod
    def setup_class(cls):
        # Create a mock dictionary to represent __registered_devices
        dev1 = Mock()
        dev1.remote_address = "12345678"

        dev2 = Mock()
        dev2.remote_address = "87654321"
        cls.mock_registered_devices = {
            "12345678": dev1,
            "87654321": dev2,
        }

        cls.mock_io_sample = Mock(spec=IOSample)
        cls.mockIOLine1 = Mock(spec=IOLine)
        cls.mockIOLine2 = Mock(spec=IOLine)
        cls.mock_io_sample.analog_values = {cls.mockIOLine1:1, cls.mockIOLine2:2}
        cls.mock_remote_xbee = Mock(spec=RemoteXBeeDevice)
        cls.mock_remote_xbee.get_64bit_addr.return_value = "19734682"
        cls.mock_remote_xbee.get_node_id.return_value = "TestDevice"

    @classmethod
    def teardown_class(cls):
        pass

    @patch('builtins.print')  # Mock the print function
    @patch('HomeAssistantAutoDiscovery.perform_auto_discovery')
    def test_register_device(self, mock_perform_auto_discovery, mock_print):
        xbee_manager = XBeeDeviceManager()

        # Call the RegisterDevice method
        result = xbee_manager.RegisterDevice(self.mock_io_sample, self.mock_remote_xbee)

        # Verify that RemoteIOSensorDevice was created with the expected arguments
        expected_channels = {
            1: ADCBinarySensorChannel(self.mockIOLine1, self.mock_remote_xbee.return_value, f"myhome/{self.mock_remote_xbee.get_64bit_addr()}/{str(self.mockIOLine1).replace('.','-')}/state", 501, 1, "sensor", 500, False),
            2: ADCBinarySensorChannel(2, 2, "myhome/12345678/2/state", "myhome/12345678/2/raw_adc_value", 1, "sensor", 500, False),
            3: ADCBinarySensorChannel(3, 3, "myhome/12345678/3/state", "myhome/12345678/3/raw_adc_value", 1, "sensor", 500, False),
        }
        # expected_device = RemoteIOSensorDevice("TestDevice", "19734682", expected_channels)

        assert result.name == "TestDevice"
        assert result.remote_address == "19734682"


        # # Verify that XBeeDeviceManager.registered_devices was updated with the new device
        # assert xbee_manager.registered_devices == {"19734682": expected_device}

        # # Verify that perform_auto_discovery was called with the new device
        # mock_perform_auto_discovery.assert_called_once_with(expected_device)

        # # Verify that print was called with the expected message
        # mock_print.assert_called_once_with(f"Registering remote device.  Address={expected_device.remote_address}, Name={expected_device.name}")


    @patch('builtins.print')  # Mock the print function
    def test_get_registered_device_found(self, mock_print):

        deviceManager = XBeeDeviceManager()
        # Set the mock dictionary as registered_devices
        deviceManager.registered_devices = self.mock_registered_devices

        # Call the GetRegisteredDevice method with an existing address
        result = deviceManager.GetRegisteredDevice("12345678")

        assert result == self.mock_registered_devices["12345678"]

        # Verify that the print function was called with the expected message
        # mock_print.assert_called_once_with("Existing device lookup complete, found:", self.mock_registered_devices["12345678"])

    @patch('builtins.print')  # Mock the print function
    def test_get_registered_device_not_found(self, mock_print):
        
        deviceManager = XBeeDeviceManager()
        # Set the mock dictionary as __registered_devices
        deviceManager.registered_devices = self.mock_registered_devices

        # Call the GetRegisteredDevice method with a non-existing address
        result = deviceManager.GetRegisteredDevice("99999999")

        assert result is None  # No device found

        # Verify that the print function was called with the expected message
        mock_print.assert_called_once_with("Existing device lookup complete, found: None")

if __name__ == '__main__':
    pytest.main()
