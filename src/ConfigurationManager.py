import json

class ConfigurationManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.app_config = {}


    def load_config(self):
        try:
            print(f"Loading config from '{self.config_path}'")
            with open(self.config_path, 'r') as config_file:
                self.app_config = json.load(config_file)
            print(f"Config loaded: {self.app_config}")


        except FileNotFoundError:
            print(f"Config file '{self.config_path}' not found.")
            raise
        except Exception as ex:
            print(f"Error loading config from '{self.config_path}': {ex}")
            raise
    
    # def get_config(self):
    #     return self.app_config
    
    @property
    def device_port(self):
        return self.app_config["device_port"]
    
    @property
    def device_baud_rate(self):
        return self.app_config["device_baud_rate"]
    
    @property
    def coordinator_pan_id(self):
        return self.app_config["coordinator_pan_id"]
    
    @property
    def coordinator_scan_channels(self):
        return self.app_config["coordinator_scan_channels"]
    
    @property
    def coordinator_node_join_time(self):
        return self.app_config["coordinator_node_join_time"]
    
    @property
    def coordinator_node_identifier(self):
        return self.app_config["coordinator_node_identifier"]
    
    @property
    def coordinator_encryption_enable(self):
        return self.app_config["coordinator_encryption_enable"]
    
    @property
    def coordinator_encryption_options(self):
        return self.app_config["coordinator_encryption_options"]
    
    @property
    def coordinator_encryption_key(self):
        return self.app_config["coordinator_encryption_key"]
    
    @property
    def coordinator_network_encryption_key(self):
        return self.app_config["coordinator_network_encryption_key"]
    
    @property
    def mqtt_broker(self):
        return self.app_config["mqtt_broker"]
    
    @property
    def mqtt_port(self):
        return self.app_config["mqtt_port"] 
    
    @property
    def xbee_reset_pin(self):
        return self.app_config["xbee_reset_pin"]
    
    @property
    def status_light_pin(self):
        return self.app_config["status_light_pin"]
    
    @property
    def log_level(self):
        return self.app_config["log_level"]
    