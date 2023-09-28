from unittest.mock import MagicMock, patch, PropertyMock
from LocalZigbeeDevice import *


def test_SetNodeID_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_node_id.return_value = "NoID"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_node_identifier = "COORDINATOR"

    # Call the SetNodeID function
    result = SetNodeID(device_mock, configuration_manager_mock)

    # Assert that the node ID was set to the coordinator node identifier
    device_mock.set_node_id.assert_called_once_with("COORDINATOR")

    # Assert that changes were written
    assert result == True

def test_SetNodeID_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_node_id.return_value = "COORDINATOR"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_node_identifier = "COORDINATOR"

    # Call the SetNodeID function
    result = SetNodeID(device_mock, configuration_manager_mock)

    # Assert that the node ID was set to the coordinator node identifier
    device_mock.set_node_id.assert_not_called()

    # Assert that changes were written
    assert result == False

def test_SetPanID_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_pan_id.return_value = b'\x1234'
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    type(configuration_manager_mock).coordinator_pan_id = PropertyMock(return_value="01")

    # Call the SetPanID function
    result = SetPanID(device_mock, configuration_manager_mock)

    # Assert that the PAN ID was set to the coordinator node identifier
    device_mock.set_pan_id.assert_called_once_with(b'\x01')

    # Assert that changes were written
    assert result == True

def test_SetPanID_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_pan_id.return_value = "4321"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_pan_id = "4321"

    # Call the SetPanID function
    result = SetPanID(device_mock, configuration_manager_mock)

    # Assert that the PAN ID was set to the coordinator node identifier
    device_mock.set_pan_id.assert_not_called()

    # Assert that changes were written
    assert result == False

def test_EncryptionEnabled_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_enabled.return_value = False
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_enable = True

    # Call the EncryptionEnabled function
    result = GetEncryptionEnabled(device_mock, configuration_manager_mock)

    # Assert that the encryption enabled was set to the coordinator node identifier
    device_mock.set_encryption_enabled.assert_called_once_with(True)

    # Assert that changes were written
    assert result == True

def test_EncryptionEnabled_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_enabled.return_value = True
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_enable = True

    # Call the EncryptionEnabled function
    result = GetEncryptionEnabled(device_mock, configuration_manager_mock)

    # Assert that the encryption enabled was set to the coordinator node identifier
    device_mock.set_encryption_enabled.assert_not_called()

    # Assert that changes were written
    assert result == False

def test_SetEncryptionOptions_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_options.return_value = "02"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.network_encryption_options = "03"

    # Call the SetEncryptionOptions function
    result = SetEncryptionOptions(device_mock, configuration_manager_mock)

    # Assert that the encryption options were set to the coordinator node identifier
    device_mock.set_encryption_options.assert_called_once_with(b'\x03')

    # Assert that changes were written
    assert result == True

# @patch('LocalZigbeeDevice.XBeeDevice')
# def test_configure_coordinator(mock_device):
#     mock_device_instance = MagicMock()
#     mock_device.return_value = mock_device_instance
#     mock_device.get_encryption_options.return_value = "4321"
#     mock_device.get_node_join_time.return_value = 5
#     mock_device.get_pan_id.return_value = "9999"
#     mock_device.get_node_id.return_value = "NoID"
#     mock_device.get_encryption_enabled.return_value = False
#     mock_device.get_network_join_time.return_value = 5

#     mock_config_manager = MagicMock()
#     mock_config_manager.coordinator_pan_id = "1234"
#     mock_config_manager.coordinator_scan_channels = "11-26"
#     mock_config_manager.coordinator_node_join_time = 10
#     mock_config_manager.coordinator_node_identifier = "test"
#     mock_config_manager.network_encryption_options = True
#     mock_config_manager.network_encryption_key = "testkey"
#     mock_config_manager.network_node_join_time = 10

#     ConfigureCoordinator(mock_config_manager, mock_device_instance)

#     mock_device_instance.set_node_id.assert_called_once_with(mock_config_manager.coordinator_node_identifier)
#     mock_device_instance.set_pan_id.assert_called_once_with(mock_config_manager.coordinator_pan_id)
#     mock_device_instance.set_encryption_enabled.assert_called_once_with(mock_config_manager.coordinator_encryption_enable)
#     mock_device_instance.set_encryption_options.assert_called_once_with(mock_config_manager.network_encryption_options)
#     mock_device_instance.set_node_join_time.assert_called_once_with(mock_config_manager.network_node_join_time)
#     mock_device_instance.set_network_encryption_key.assert_called_once_with(mock_config_manager.network_encryption_key)