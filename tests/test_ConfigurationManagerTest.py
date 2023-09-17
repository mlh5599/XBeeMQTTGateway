import os
import pytest
from ConfigurationManager import ConfigurationManager
import json

def test_load_config_success(tmp_path):
    # Create a temporary config file for testing
    config_data = {"key": "value"}
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