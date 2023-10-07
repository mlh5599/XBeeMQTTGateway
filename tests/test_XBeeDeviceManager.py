import pytest
from unittest.mock import patch, Mock
from XBeeDeviceManager import XBeeDeviceManager
from digi.xbee.io import IOSample, IOLine
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
        cls.mock_io_sample.analog_values = {cls.mockIOLine1: 1,
                                            cls.mockIOLine2: 2}
        cls.mock_remote_xbee = Mock(spec=RemoteXBeeDevice)
        cls.mock_remote_xbee.get_64bit_addr.return_value = "19734682"
        cls.mock_remote_xbee.get_node_id.return_value = "TestDevice"

    @classmethod
    def teardown_class(cls):
        pass

    @patch('builtins.print')  # Mock the print function
    @patch('HomeAssistantAutoDiscovery.perform_auto_discovery')
    def test_register_device(self, mock_perform_auto_discovery, mock_print):

        # Call the RegisterDevice method
        result = XBeeDeviceManager.RegisterDevice(self.mock_io_sample,
                                                  self.mock_remote_xbee)

        assert result.name == "TestDevice"
        assert result.remote_address == "19734682"

    @patch('builtins.print')  # Mock the print function
    def test_get_registered_device_found(self, mock_print):

        # Set the mock dictionary as registered_devices
        XBeeDeviceManager.registered_devices = self.mock_registered_devices

        # Call the GetRegisteredDevice method with an existing address
        result = XBeeDeviceManager.GetRegisteredDevice("12345678")

        assert result == self.mock_registered_devices["12345678"]

    @patch('builtins.print')  # Mock the print function
    def test_get_registered_device_not_found(self, mock_print):

        # Set the mock dictionary as __registered_devices
        XBeeDeviceManager.registered_devices = self.mock_registered_devices

        # Call the GetRegisteredDevice method with a non-existing address
        result = XBeeDeviceManager.GetRegisteredDevice("99999999")

        assert result is None  # No device found


if __name__ == '__main__':
    pytest.main()
