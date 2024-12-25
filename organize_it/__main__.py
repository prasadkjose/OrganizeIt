# pylint: disable=C0103
""" Main """

import logging
import os
from organize_it.tests._fixtures.directory_structure_fixtures import (
    GENERATED_ROOT_DIR_NAME,
    UNCATEGORIZED_DIR_NAME,
    CATEGORIZED_DIR_NAME,
)

from organize_it.settings import (
    DIR,
    CONFIG,
    WORKING_DIR,
    GENERATED_DESTINATION_TREE,
    GENERATED_SOURCE_TREE,
    GENERATED_SOURCE_JSON,
    TEST_FIXTURES_DIR,
)

from organize_it.cli.input_arg_parser import InputArgParser
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

    # Validate the YAML config first with the corresponding json-schema
    schema_validator = YAMLConfigValidator(CONFIG)
    schema_validator.validate_config()

    # Take Source and destination as CLI args.
    # Order of preference
    #   1. CLI --src
    #   2. Source from config
    #   3. Current directory
    cli_parser = InputArgParser()

    if cli_parser.move:
        move_files = cli_parser.move
    else:
        move_files = False

    if cli_parser.src:
        source_directory = cli_parser.src
    elif "source" in CONFIG:
        source_directory = CONFIG.source
    else:
        source_directory = WORKING_DIR

    if cli_parser.dest:
        destination_directory = cli_parser.dest
    elif "destination" in CONFIG:
        destination_directory = CONFIG.destination
    else:
        destination_directory = WORKING_DIR

    destination_directory = os.path.join(
        TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
    )
    source_directory = os.path.join(
        TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
    )

    # TODO: If cli is in interactive mode, then source tree will be will be generated already. So skip this part.
    # Current Structure
    file_manager = FileManager(source_directory, destination_directory)

    # Read the source directory and create oIt tree input dictionary and save it to a file
    source_tree_dict = file_manager.file_walk(None, GENERATED_SOURCE_JSON)

    # write the source tree structure result to a file
    tree_structure = TreeStructure()
    FileManager.create_and_write_file(
        GENERATED_SOURCE_TREE,
        lambda file_stream: tree_structure.generate_tree_structure(
            source_tree_dict, "", file_stream
        ),
    )
    # Categorize the files and dirs based on the given config
    categorizer = Categorizer(CONFIG)
    categorized_tree_dict = categorizer.categorize_dict(source_tree_dict, True)

    FileManager.create_and_write_file(
        GENERATED_DESTINATION_TREE,
        lambda file_stream: tree_structure.generate_tree_structure(
            categorized_tree_dict, "", file_stream
        ),
    )

    file_manager.categorize_and_sort_file(
        CONFIG,
        categorized_tree_dict[DIR],
        move_files,  # To delete the source files.
    )
    # Explore SYMLINKS(unix), Junction(Windows)


if __name__ == "__main__":
    main()
