# config_loader.py

import json
import os

from dotenv import load_dotenv

# Load .env into environment variables
load_dotenv() 

# Load and store .env values
SMTP_CONFIG = {
    "host": os.getenv("SMTP_HOST", "localhost"),
    "port": os.getenv("SMTP_PORT", "25"),
    "user": os.getenv("SMTP_USER"),
    "password": os.getenv("SMTP_PASS")
}

if not SMTP_CONFIG["user"] or not SMTP_CONFIG["password"]:
    raise ValueError("SMTP credentials are missing!")

def load_config(config_filename="config.json"):

    # Ensure physical paths points to core/
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir,"config",config_filename)

    """Load configuration settings from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    try:
        # load the JSON config
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
    
def get_nested(config: dict, key_path: str, default=None):
    """
    Safely retrieves a nested value from a dict using dot notation.
    """
    keys = key_path.split(".")
    for key in keys:
        if isinstance(config, dict) and key in config:
            config = config[key]
        else:
            return default
    return config

def render_message(template: str, **kwargs) -> str:
    """
    Renders a template string with double-brace placeholders.
    """
    safe_template = template.replace("{{", "{").replace("}}", "}")
    return safe_template.format(**kwargs)

def get_rendered(config: dict, key_path: str, **kwargs) -> str:
    """
    Retrieves a template from config and renders it with kwargs.
    """
    template = get_nested(config, key_path)
    if template is None:
        return f"[Missing template at '{key_path}']"
    return render_message(template, **kwargs)