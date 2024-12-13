# pylint: disable=C0103
""" Main """

import logging
import os

from organize_it.settings import TEST_FIXTURES_DIR, TMP_DIR, CONFIG
from organize_it.bin.file_manager import FileManager
from organize_it.bin.tree_structure import TreeStructure
from organize_it.schema_validation.validator import YAMLConfigValidator

logger = logging.getLogger(__name__)


def main():
    """
    The main entry point of the program.

    The function does not take any arguments and does not return a value. Any relevant
    output (such as results, status messages, or errors) is typically printed to the console
    or written to log files.

    This function is typically wrapped in a `if __name__ == "__main__":` block to allow
    for better modularity and to enable unit testing of other parts of the program.
    """
    logger.info(" - Starting to organize...")

    # validate the YAML config first with the corresponding json-schema
    schema_validator = YAMLConfigValidator(CONFIG)
    schema_validator.validate_config()

    ## Current Structure
    # Create and return a dict of files and directories
    file_manager = FileManager()
    # TODO: Take Source and destination as CLI args.
    tree_dict = file_manager.file_walk(TEST_FIXTURES_DIR + "/generated_files")

    # write to a temp buffer
    tree_structure = TreeStructure()
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(f"{TMP_DIR}/.generated.tree", "w") as generated_tree_file:
        tree_structure.generate_tree_structure(tree_dict, "", generated_tree_file)

    ## new Structure
    # get the source and destination directories, if any
    # create tree dict from config
    config_tree_dic = tree_structure.yaml_config_to_dict(CONFIG)

    with open(f"{TMP_DIR}/.generated_destination.tree", "w") as generated_tree_file:
        tree_structure.generate_tree_structure(config_tree_dic, "", generated_tree_file)

    # TODO: Read the source directory and create oIt tree input dictionary
    # TODO: recursive_sort:
    # If is_recursive, Read each level of the recursively directory
    # and generate oIt dict based on the config
    # else, create the tree of the top level.

    # TODO: copy files based on the new sorted to destination.
    # Explore SYMLINKS(unix), Junction(Windows)

    # TODO: remove the files from source.


if __name__ == "__main__":
    main()
