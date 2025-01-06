""" settings.py - Configuration constants and utility methods for organizeIt project """

import sys
import os
from pathlib import Path
import logging
import json
import yaml
import organize_it.constants as constants

# setup configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

RULES = "rules"
NAMES = "names"
FORMAT = "format"
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

# The path to the AI directory
AI_DIR = os.path.join(ROOT_DIR, "ai")

# .tmp file path for any temporary files
TMP_DIR = os.path.join(ROOT_DIR, ".tmp")
os.makedirs(TMP_DIR, exist_ok=True)

AI_GENERATED_CONFIG = f"{TMP_DIR}/.ai_generated_config.json"

AI_GENERATED_DESTINATION_TREE = f"{TMP_DIR}/.ai-generated_destination.tree"
GENERATED_DESTINATION_TREE = f"{TMP_DIR}/.generated_destination.tree"
GENERATED_DESTINATION_JSON = f"{TMP_DIR}/.generated_destination.json"
GENERATED_SOURCE_TREE = f"{TMP_DIR}/.generated.tree"
GENERATED_SOURCE_JSON = f"{TMP_DIR}/.generated.json"


def load_json_schema():
    """Load json-schema file to memory"""
    with open(
        os.path.join(CONFIG_DIR, "config_schema.json"), "r", encoding="utf-8"
    ) as tmp_file:
        return json.load(tmp_file)


def load_yaml(yaml_dir: str, yaml_path: str = None) -> list[any]:
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

    def read_file(name):
        with open(name, "r", encoding="utf-8") as tmp_yaml_stream:
            try:
                config_list.append(yaml.full_load(tmp_yaml_stream))
            except yaml.YAMLError as exception:
                raise exception

    if yaml_path:
        read_file(yaml_path)
    else:
        yaml_files_list = os.listdir(yaml_dir)  # list all files in the directory
        for name in yaml_files_list:
            if name.endswith(".yaml"):  # filter by .yaml
                read_file(os.path.join(yaml_dir, name))

    return config_list[0] if len(config_list) == 1 else config_list


# The json-schema
SCHEMA = load_json_schema()

# The YAML config file
CONFIG = load_yaml(CONFIG_DIR)

# Load test fixures
TEST_FIXTURES_CONFIGS = load_yaml(TEST_FIXTURES_DIR)


# Util method to exit the tool gracefully
def exit_gracefully(error):
    """
    Exits the tool gracefully, logging the error and performing cleanup if needed.

    Args:
        error (Exception or str): The error that caused the exit, or a descriptive message.

    Returns:
        None
    """
    try:
        # Log the error details
        if isinstance(error, Exception):
            logger.error(" - Exiting due to an exception: %s", str(error))
        else:
            logger.error(" - Exiting due to an error: %s", error)

        # Perform any cleanup operations if necessary
        logger.info(" - Performing cleanup operations...")

        # Exit the program with a non-zero status code to indicate failure
        sys.exit(1)
    except Exception as cleanup_error:
        logger.critical(" - An error occurred during cleanup: %s", str(cleanup_error))
        sys.exit(1)


def get_constant(name):
    """
    Retrieve the value of a constant from the constants module.

    :param name: The name of the constant to retrieve.
    :return: The value of the constant.
    :raises AttributeError: If the constant is not defined in constants.py.
    """
    try:
        return getattr(constants, name)
    except AttributeError as e:
        raise AttributeError(f"Constant '{name}' not found in constants.py") from e
