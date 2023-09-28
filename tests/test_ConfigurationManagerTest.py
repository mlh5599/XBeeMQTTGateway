import os
import pytest
from ConfigurationManager import ConfigurationManager
import json

config_data = {
    "mqtt_broker": "MQTT.HagueHome.lan",
    "mqtt_port": 1883,
    "status_light_pin": 24,
    "log_level": "DEBUG",
    "Coordinator": {
        "port": "COM4",
        "baud_rate": 9600,
        "pan_id": "2000",
        "scan_channels": "FF",
        "node_join_time": "FF",
        "node_identifier": "TestGateway",
        "encryption_enable": "1",
        "encryption_options": "0",
        "encryption_key": "0",
        "network_encryption_key": "0x81041771",
        "reset_pin": 27
    }
}

def test_load_config_success():
    # Create a temporary config file
    config_path = "config.json"
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file)

    cm = ConfigurationManager(config_path)
    cm.load_config()

    # Assert that the configuration manager has the expected values
    assert cm.coordinator_port == "COM4"
    assert cm.coordinator_baud_rate == 9600
    assert cm.coordinator_pan_id == "2000"
    assert cm.coordinator_scan_channels == "FF"
    assert cm.coordinator_node_join_time == "FF"
    assert cm.coordinator_node_identifier == "TestGateway"
    assert cm.coordinator_encryption_enable == "1"
    assert cm.coordinator_encryption_options == "0"
    assert cm.coordinator_reset_pin == 27
    assert cm.status_light_pin == 24
    assert cm.mqtt_broker == "MQTT.HagueHome.lan"
    assert cm.mqtt_port == 1883
    # Delete the temporary config file
    os.remove(config_path)

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        cm = ConfigurationManager("non_existent_config.json")
        cm.load_config()
        
def test_load_config_invalid_json(tmp_path):
    # Create a temporary config file with invalid JSON
    invalid_json = '{"key": "value"'
    config_path = tmp_path / "invalid_config.json"
    with open(config_path, 'w') as config_file:
        config_file.write(invalid_json)

    with pytest.raises(json.decoder.JSONDecodeError):
        cm = ConfigurationManager(config_path)
        cm.load_config()