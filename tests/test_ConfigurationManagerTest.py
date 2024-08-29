import pytest
from configmanager import ConfigurationManager
import json

test_config_data_non_defaults = {
    "mqtt_broker": "MQTT.HagueHome.lan",
    "mqtt_port": 1883,
    "status_light_pin": 24,
    "log_level": "DEBUG",
    "coordinator": {
        "port": "COM4",
        "baud_rate": 115200,
        "pan_id": "2000",
        "scan_channels": "1111",
        "scan_duration": "1112",
        "zigbee_stack_profile": "2",
        "node_join_time": "11",
        "destination_address_high": "FFFFFFFF",
        "destination_address_low": "00000000",
        "node_identifier": "TestGateway",
        "maximum_hops": "3",
        "broadcast_radius": "0",
        "many_to_one_broadcast_time": "20",
        "device_type_identifier": "FFFD",
        "node_discovery_backoff": "2",
        "node_discovery_options": "1",
        "pan_conflict_threshold": "5",
        "power_level": "100",
        "power_mode": "4",
        "encryption_enable": "1",
        "encryption_options": "1",
        "encryption_key": "0",
        "network_encryption_key": "0x81041771",
        "parity": "1",
        "stop_bits": "1",
        "DIO7_configuration": "0",
        "DIO6_configuration": "1",
        "API_enable": "0",
        "API_output_mode": "1",
        "cyclic_sleep_period": "0",
        "number_of_cyclic_sleep_periods": "0",
        "AD0_DIO0_configuration": "0",
        "AD1_DIO1_configuration": "1",
        "AD2_DIO2_configuration": "2",
        "AD3_DIO3_configuration": "3",
        "DIO4_configuration": "4",
        "DIO5_configuration": "5",
        "DIO10_PWM0_configuration": "2",
        "DIO11_configuration": "3",
        "DIO12_configuration": "4",
        "pull_up_resistor_enable": "000000",
        "rssi_pwm_timer": "0",
        "device_options": "0",
        "IO_sampling_rate": "10",
        "digital_IO_change_detection": "1111",
        "supply_voltage_high_threshold": "10",
        "reset_pin": 27,
    }
}

config_data = {
    "mqtt_broker": "MQTT.HagueHome.lan",
    "mqtt_port": 1883,
    "status_light_pin": 24,
    "log_level": "DEBUG",
    "coordinator": {
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
        "reset_pin": 27,

    }
}


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
