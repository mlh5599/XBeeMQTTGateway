from unittest.mock import MagicMock, patch
from LocalZigbeeDevice import Initialize, ConfigureCoordinator

@patch('LocalZigbeeDevice.XBeeDevice')
def test_initialize(mock_device):
    mock_device_instance = MagicMock()
    mock_device.return_value = mock_device_instance
    mock_device_instance.get_64bit_addr.return_value = "00:11:22:33:44:55:66:77"

    mock_config_manager = MagicMock()
    mock_config_manager.device_port = "/dev/ttyUSB0"
    mock_config_manager.device_baud_rate = 9600

    Initialize(mock_config_manager)

    mock_device.assert_called_once_with(mock_config_manager.device_port, mock_config_manager.device_baud_rate)
    mock_device_instance.open.assert_called_once()
    mock_device_instance.get_64bit_addr.assert_called_once()
    

@patch('LocalZigbeeDevice.XBeeDevice')
def test_configure_coordinator(mock_device):
    mock_device_instance = MagicMock()
    mock_device.return_value = mock_device_instance
    mock_device.get_encryption_options.return_value = "4321"
    mock_device.get_node_join_time.return_value = 5
    mock_device.get_pan_id.return_value = "9999"
    mock_device.get_node_id.return_value = "NoID"
    mock_device.get_encryption_enabled.return_value = False
    mock_device.get_network_join_time.return_value = 5

    mock_config_manager = MagicMock()
    mock_config_manager.coordinator_pan_id = "1234"
    mock_config_manager.coordinator_scan_channels = "11-26"
    mock_config_manager.coordinator_node_join_time = 10
    mock_config_manager.coordinator_node_identifier = "test"
    mock_config_manager.network_encryption_options = True
    mock_config_manager.network_encryption_key = "testkey"
    mock_config_manager.network_node_join_time = 10

    ConfigureCoordinator(mock_config_manager, mock_device_instance)

    mock_device_instance.set_node_id.assert_called_once_with(mock_config_manager.coordinator_node_identifier)
    mock_device_instance.set_pan_id.assert_called_once_with(mock_config_manager.coordinator_pan_id)
    mock_device_instance.set_encryption_enabled.assert_called_once_with(mock_config_manager.coordinator_encryption_enable)
    mock_device_instance.set_encryption_options.assert_called_once_with(mock_config_manager.network_encryption_options)
    mock_device_instance.set_node_join_time.assert_called_once_with(mock_config_manager.network_node_join_time)
    mock_device_instance.set_network_encryption_key.assert_called_once_with(mock_config_manager.network_encryption_key)