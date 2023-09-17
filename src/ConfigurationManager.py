import json

class ConfigurationManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.app_config = {}

    def load_config(self):
        try:
            with open(self.config_path, 'r') as config_file:
                self.app_config = json.load(config_file)
        except FileNotFoundError:
            print(f"Config file '{self.config_path}' not found.")
            raise
        except Exception as ex:
            print(f"Error loading config from '{self.config_path}': {ex}")
            raise
    
    def get_config(self):
        return self.app_config

