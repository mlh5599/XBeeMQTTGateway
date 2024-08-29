from unittest.mock import MagicMock, PropertyMock
from XBee.LocalZigbeeDevice import SetNodeID, SetPanID, SetScanChannels, \
    SetEncryptionOptions, GetEncryptionEnabled, SetZigbeeStackProfile, \
    SetNodeJoinTime

testConfigs = {
    "mqtt_broker": "MQTT.HagueHome.lan",
    "mqtt_port": "1883",
    "status_light_pin": 24,
    "log_level": "DEBUG",
    "Coordinator": {
        "port": "COM4",
        "baud_rate": 9600,
        "pan_id": "2000",
        "scan_channels": "7FFF",
        "scan_duration": "03",
        "node_join_time": "FF",
        "node_identifier": "XBeeGateway2",
        "encryption_enable": "1",
        "encryption_options": "0",
        "encryption_key": "0",
        "network_encryption_key": "0x81041771",
        "reset_pin": 27
    }
}


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
    assert result is True


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
    assert result is False


def test_SetPanID_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_pan_id.return_value = b'\x1234'
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    type(configuration_manager_mock).coordinator_pan_id = \
        PropertyMock(return_value="01")

    # Call the SetPanID function
    result = SetPanID(device_mock, configuration_manager_mock)

    # Assert that the PAN ID was set to the coordinator node identifier
    device_mock.set_pan_id.assert_called_once_with(b'\x01')

    # Assert that changes were written
    assert result is True


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
    assert result is False


def test_SetScanChannels_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_scanning_channels.return_value = b'\x1234'
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_scan_channels = "01"

    # Call the SetScanChannels function
    result = SetScanChannels(device_mock, configuration_manager_mock)

    # Assert that the scan channels were set to the coordinator node identifier
    device_mock.set_scanning_channels.assert_called_once_with(b'\x01')

    # Assert that changes were written
    assert result is True


def test_SetScanChannels_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_scanning_channels.return_value = "4321"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_scan_channels = "4321"

    # Call the SetScanChannels function
    result = SetScanChannels(device_mock, configuration_manager_mock)

    # Assert that the scan channels were set to the coordinator node identifier
    device_mock.set_scanning_channels.assert_not_called()

    # Assert that changes were written
    assert result is False


def test_SetEncryptionOptions_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_options.return_value = b'\x1234'
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_options = "01"

    # Call the SetEncryptionOptions function
    result = SetEncryptionOptions(device_mock, configuration_manager_mock)

    # Assert that the encryption options were set to the coordinator node
    # identifier
    device_mock.set_encryption_options.assert_called_once_with(b'\x01')

    # Assert that changes were written
    assert result is True


def test_SetEncryptionOptions_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_options.return_value = b'\x11'
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_options = b'\x11'

    # Call the SetEncryptionOptions function
    result = SetEncryptionOptions(device_mock, configuration_manager_mock)

    # Assert that the encryption options were set to the coordinator node
    # identifier
    device_mock.set_encryption_options.assert_not_called()

    # Assert that changes were written
    assert result is False


def test_EncryptionEnabled_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_enabled.return_value = False
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_enable = True

    # Call the EncryptionEnabled function
    result = GetEncryptionEnabled(device_mock, configuration_manager_mock)

    # Assert that the encryption enabled was set to the coordinator node
    # identifier
    device_mock.set_encryption_enabled.assert_called_once_with(True)

    # Assert that changes were written
    assert result is True


def test_EncryptionEnabled_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_encryption_enabled.return_value = True
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_encryption_enable = True

    # Call the EncryptionEnabled function
    result = GetEncryptionEnabled(device_mock, configuration_manager_mock)

    # Assert that the encryption enabled was set to the coordinator node
    # identifier
    device_mock.set_encryption_enabled.assert_not_called()

    # Assert that changes were written
    assert result is False


def test_SetZigbeeStackProfile_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_zigbee_stack_profile.return_value = "NoProfile"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_zigbee_stack_profile = "0x02"

    # Call the SetZigbeeStackProfile function
    result = SetZigbeeStackProfile(device_mock, configuration_manager_mock)

    # Assert that the Zigbee stack profile was set to the coordinator
    # Zigbee stack profile
    device_mock.set_zigbee_stack_profile.assert_called_once_with("0x02")

    # Assert that changes were written
    assert result is True


def test_SetZigbeeStackProfile_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_zigbee_stack_profile.return_value = "0x02"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_zigbee_stack_profile = "0x02"

    # Call the SetZigbeeStackProfile function
    result = SetZigbeeStackProfile(device_mock, configuration_manager_mock)

    # Assert that the Zigbee stack profile was set to the coordinator
    # Zigbee stack profile
    device_mock.set_zigbee_stack_profile.assert_not_called()

    # Assert that changes were written
    assert result is False
    

def test_SetNodeJoinTime_With_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_node_join_time.return_value = "00"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_node_join_time = "FF"

    # Call the SetNodeJoinTime function
    result = SetNodeJoinTime(device_mock, configuration_manager_mock)

    # Assert that the node join time was set to the coordinator node join time
    device_mock.set_node_join_time.assert_called_once_with("FF")

    # Assert that changes were written
    assert result is True


def test_SetNodeJoinTime_No_Change():
    # Create a mock XBeeDevice object
    device_mock = MagicMock()
    device_mock.get_node_join_time.return_value = "FF"
    # Create a mock ConfigurationManager object
    configuration_manager_mock = MagicMock()
    configuration_manager_mock.coordinator_node_join_time = "FF"

    # Call the SetNodeJoinTime function
    result = SetNodeJoinTime(device_mock, configuration_manager_mock)

    # Assert that the node join time was set to the coordinator node join time
    device_mock.set_node_join_time.assert_not_called()

    # Assert that changes were written
    assert result is False