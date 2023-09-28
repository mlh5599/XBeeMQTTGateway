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
            logging.error(f"Error loading config from '{self.config_path}': {ex}")
            raise
    
    # def get_config(self):
    #     return self.app_config
    
    @property
    def coordinator_port(self):
        return self.app_config["Coordinator"]["port"]
    
    @property
    def coordinator_baud_rate(self):
        return self.app_config["Coordinator"]["baud_rate"]
    
    @property
    def coordinator_pan_id(self):
        return self.app_config["Coordinator"]["pan_id"]
    
    @property
    def coordinator_scan_channels(self):
        return self.app_config["Coordinator"]["scan_channels"]
    
    @property
    def coordinator_node_join_time(self):
        return self.app_config["Coordinator"]["node_join_time"]
    
    @property
    def coordinator_node_identifier(self):
        return self.app_config["Coordinator"]["node_identifier"]
    
    @property
    def coordinator_encryption_enable(self):
        return self.app_config["Coordinator"]["encryption_enable"]
    
    @property
    def coordinator_encryption_options(self):
        return self.app_config["Coordinator"]["encryption_options"]
    
    @property
    def coordinator_encryption_key(self):
        return self.app_config["Coordinator"]["encryption_key"]
    
    @property
    def coordinator_network_encryption_key(self):
        return self.app_config["Coordinator"]["network_encryption_key"]
    
    @property
    def mqtt_broker(self):
        return self.app_config["mqtt_broker"]
    
    @property
    def mqtt_port(self):
        return self.app_config["mqtt_port"] 
    
    @property
    def coordinator_reset_pin(self):
        return self.app_config["Coordinator"]["reset_pin"]
    
    @property
    def status_light_pin(self):
        return self.app_config["status_light_pin"]
    
    @property
    def log_level(self):
        return self.app_config["log_level"]
    