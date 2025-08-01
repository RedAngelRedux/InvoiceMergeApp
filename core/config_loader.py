# config_loader.py

import json
import os

def load_config(config_filename="config.json"):
    base_dir = os.path.dirname(__file__) # This points to core/
    config_path = os.path.join(base_dir,"config",config_filename)

    """Load configuration settings from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {config_path}: {e}")

def get_setting(config, key, default=None):
    """Retrieve a setting from the loaded config dictionary."""
    return config.get(key, default)

def get_ui_text():
    with open("config/ui_text.json") as f:
        return json.load(f)
