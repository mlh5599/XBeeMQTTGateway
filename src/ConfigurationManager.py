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
    
    def get_device_port(self):
        return self.get_config()["device_port"]
    
    def get_device_baud_rate(self):
        return self.get_config()["device_baud_rate"]
    
    def get_mqtt_broker(self):
        return self.get_config()["mqtt_broker"]
    
    def get_mqtt_port(self):
        return self.get_config()["mqtt_port"]
        
    def get_xbee_reset_pin(self):
        return self.get_config()["xbee_reset_pin"]
    
    def get_status_light_pin(self):
        return self.get_config()["status_light_pin"]
    
    device_port = property(get_device_port)
    device_baudRate = property(get_device_baud_rate)
    mqtt_broker = property(get_mqtt_broker)
    mqtt_port = property(get_mqtt_port)
    xbee_reset_pin = property(get_xbee_reset_pin)
    status_light_pin = property(get_status_light_pin)

    