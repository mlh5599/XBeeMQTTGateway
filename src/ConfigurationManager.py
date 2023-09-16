import sys
import json

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file '{config_path}' not found.")
        raise
    except Exception as ex:
        print(f"Error loading config from '{config_path}': {ex}")
        raise
