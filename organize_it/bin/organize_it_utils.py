""" Utility functions """

from organize_it.settings import CONFIG
from organize_it.schema_validation.validator import YAMLConfigValidator


def create_tree_from_config(config: dict) -> dict:
    """
    Creates a directory tree structure from the given YAML config.
    Makes sure the config is validated before creating a tree.

    Args:
        dict: config dictonary to build tree from
        bool: save_to_file If true, saves the generated tree to a file

    Returns:
        dict: directory tree structure

    Raises:
        ValidationError: If the YAML data does not conform to the validation rules.
    """

    # TODO: validate the YAML config first with the corresponding json-schema
    # Validate the YAML config file
    schema_validator = YAMLConfigValidator(CONFIG)
    schema_validator.validate_config()
    # TODO: Read the YAML file and convert it to a dictionary

    # TODO: get the source and destination directories, if any
    # source_dir = config["source"]
    # destination_dir = config["destination"]

    # TODO: Read the source directory and create oIt tree input dictionary

    # TODO: recursive_sort:
    # If is_recursive, Read each level of the recursively directory
    # and generate oIt dict based on the config
    # else, create the tree of the top level.

    # TODO: copy files based on the new sorted to destination.
    # Explore SYMLINKS(unix), Junction(Windows)

    # TODO: remove the files from source.
