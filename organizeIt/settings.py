# settings.py - Configuration for organizeIt project
import yaml
import json
import os
from pathlib import Path
import os
import logging

# setup configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# The project root path
ROOT_DIR = Path(__file__).resolve().parent

# The path to the configs directory
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")

def load_json_schema():
    with open(os.path.join(CONFIG_DIR, 'config-schema.json5'), 'r') as tmp_file:
        return json.load(tmp_file)

def load_yaml_config():
    with open(os.path.join(CONFIG_DIR, 'config.yaml'), 'r') as tmp_yaml_stream:
        try:
            return yaml.full_load(tmp_yaml_stream)
        except yaml.YAMLError as exception:
            raise exception
        
# The json-schema
SCHEMA = load_json_schema()

# The YAML config file
CONFIG = load_yaml_config()
