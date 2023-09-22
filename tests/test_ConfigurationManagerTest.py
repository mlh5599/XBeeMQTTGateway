import os
import pytest
from ConfigurationManager import ConfigurationManager
import json

def test_load_config_success(tmp_path):
    # Create a temporary config file for testing
    config_data = {
    "device_port": "test1",
    "device_baud_rate": "test2",
    "mqtt_broker": "test3",
    "mqtt_port": "test4",
    "xbee_reset_pin": 1,
    "status_light_pin": 2
}

    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file)

    cm = ConfigurationManager(config_path)
    cm.load_config()
    # Load the config and assert the result
    result = cm.get_config()
    print(result)
    print(config_data)
    assert result == config_data

    assert cm.device_port == config_data["device_port"]
    assert cm.device_baudRate == config_data["device_baud_rate"]
    assert cm.mqtt_broker == config_data["mqtt_broker"]
    assert cm.mqtt_port == config_data["mqtt_port"] 
    assert cm.xbee_reset_pin == config_data["xbee_reset_pin"]
    assert cm.status_light_pin == config_data["status_light_pin"]

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