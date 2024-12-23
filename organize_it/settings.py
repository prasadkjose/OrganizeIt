""" settings.py - Configuration constants and utility methods for organizeIt project """

import sys
import os
from pathlib import Path
import logging
import json
import yaml

# setup configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

FILES = "files"
DIR = "dir"
SKIP = "skip"
# Current path
WORKING_DIR = os.getcwd()

# The project root path
ROOT_DIR = Path(__file__).resolve().parent

# The path to the configs directory
CONFIG_DIR = os.path.join(ROOT_DIR, "configs")

# The path to the test fixtures configs directory
TEST_FIXTURES_DIR = os.path.join(ROOT_DIR, "tests/_fixtures")

# .tmp file path for any temporary files
TMP_DIR = os.path.join(ROOT_DIR, ".tmp")
os.makedirs(TMP_DIR, exist_ok=True)

GENERATED_DESTINATION_TREE = f"{TMP_DIR}/.generated_destination.tree"
GENERATED_DESTINATION_JSON = f"{TMP_DIR}/.generated_destination.json"
GENERATED_SOURCE_TREE = f"{TMP_DIR}/.generated.tree"
GENERATED_SOURCE_JSON = f"{TMP_DIR}/.generated.json"


def load_json_schema():
    """Load json-schema file to memory"""
    with open(
        os.path.join(CONFIG_DIR, "config-schema.json"), "r", encoding="utf-8"
    ) as tmp_file:
        return json.load(tmp_file)


def load_yaml(yaml_dir: str) -> list[any]:
    """
    Loads YAML configuration files from a specified directory and returns their contents as a list.

    This method reads all YAML files from the directory specified by `yaml_dir`,
    parses each YAML file, and appends the parsed content to a list, which is then returned.

    Args:
        yaml_dir (str): The directory containing the YAML files to load.

    Returns:
        list[any]: A list containing the parsed contents of all the YAML files found
        in the specified directory. The content can be any Python object depending
        on the structure of the YAML files.

    Raises:
        yaml.YAMLError: If any YAML file in the directory is malformed and cannot be parsed.
    """
    config_list = []
    yaml_files_list = os.listdir(yaml_dir)  # list all files in the directory
    for name in yaml_files_list:
        if name.endswith(".yaml"):  # filter by .yaml
            with open(
                os.path.join(yaml_dir, name), "r", encoding="utf-8"
            ) as tmp_yaml_stream:
                try:
                    config_list.append(yaml.full_load(tmp_yaml_stream))
                except yaml.YAMLError as exception:
                    raise exception

    return config_list[0] if len(config_list) == 1 else config_list


# The json-schema
SCHEMA = load_json_schema()

# The YAML config file
CONFIG = load_yaml(CONFIG_DIR)

# Load test fixures
TEST_FIXTURES_CONFIGS = load_yaml(TEST_FIXTURES_DIR)


# Util method to exit the tool gracefully
def exit_gracefully():
    logger.error(
        "Exiting OrganizeIt due to an error. Please check the verbose logs for more information."
    )
    sys.exit(1)
