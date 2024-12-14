# pylint: disable=C0103
""" Main """

import logging
import os

from organize_it.settings import (
    TEST_FIXTURES_DIR,
    TMP_DIR,
    CONFIG,
    GENERATED_DESTINATION_TREE_PATH,
    GENERATED_SOURCE_TREE,
)
from organize_it.bin.file_manager import FileManager
from organize_it.bin.tree_structure import TreeStructure
from organize_it.bin.categorizer import Categorizer
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
    file_manager = FileManager()
    # TODO: Take Source and destination as CLI args.

    source_directory = TEST_FIXTURES_DIR + "/generated_files"
    # Read the source directory and create oIt tree input dictionary
    source_tree_dict = file_manager.file_walk(source_directory)

    # write the source tree to a file
    tree_structure = TreeStructure()
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(GENERATED_SOURCE_TREE, "w") as generated_tree_file:
        tree_structure.generate_tree_structure(
            source_tree_dict, "", generated_tree_file
        )

    ## new Structure
    # TODO: recursive_sort:
    # If is_recursive, Read each level of the recursively directory
    # and generate oIt dict based on the config
    # else, create the tree of the top level.

    categorizer = Categorizer()
    categorized_tree_dict = categorizer.categorize_dict(CONFIG, source_tree_dict, False)

    with open(GENERATED_DESTINATION_TREE_PATH, "w") as generated_tree_file:
        tree_structure.generate_tree_structure(
            categorized_tree_dict, "", generated_tree_file
        )

    # TODO: copy files based on the new sorted to destination.
    # Explore SYMLINKS(unix), Junction(Windows)

    # TODO: remove the files from source.


if __name__ == "__main__":
    main()
