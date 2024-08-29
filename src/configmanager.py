import json
import logging


class ConfigurationManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.app_config = {}

    def load_config(self):
        try:
            logging.debug(f"Loading config from '{self.config_path}'")
            with open(self.config_path, 'r') as config_file:
                self.app_config = json.load(config_file)
            logging.debug(f"Config loaded: {self.app_config}")

        except FileNotFoundError:
            logging.error(f"Config file '{self.config_path}' not found.")
            raise
        except Exception as ex:
            logging.error(f"Error loading config from \
                           '{self.config_path}': {ex}")
            raise

    @property
    def coordinator_port(self):
        return self.app_config.get("coordinator", {})["port"]

    @property
    def coordinator_baud_rate(self):
        return self.app_config.get("coordinator", {}).get("baud_rate", 9600)

    @property
    def mqtt_broker(self):
        return self.app_config["mqtt_broker"]

    @property
    def mqtt_port(self):
        return self.app_config["mqtt_port"]

    @property
    def coordinator_reset_pin(self):
        return self.app_config.get("coordinator", {})["reset_pin"]

    @property
    def status_light_pin(self):
        return self.app_config["status_light_pin"]

    @property
    def log_level(self):
        return self.app_config["log_level"]

    def get_coordinator_device_configs(self):
        return [setting for setting in
                self.app_config.get("coordinator", {})
                .get("setting", {}).values()]
