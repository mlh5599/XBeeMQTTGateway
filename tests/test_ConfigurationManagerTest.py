import pytest
from ConfigurationManager import load_config
import json

def test_load_config_success(tmp_path):
    # Create a temporary config file for testing
    config_data = {"key": "value"}
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file)

    # Load the config and assert the result
    result = load_config(config_path)
    assert result == config_data

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config('non_existent_config.json')

def test_load_config_invalid_json(tmp_path):
    # Create a temporary config file with invalid JSON
    invalid_json = '{"key": "value"'
    config_path = tmp_path / "invalid_config.json"
    with open(config_path, 'w') as config_file:
        config_file.write(invalid_json)

    with pytest.raises(json.decoder.JSONDecodeError):
        load_config(config_path)