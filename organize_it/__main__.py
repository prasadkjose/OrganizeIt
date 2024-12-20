# pylint: disable=C0103
""" Main """

import logging
import os

from organize_it.settings import (
    TMP_DIR,
    CONFIG,
    WORKING_DIR,
    GENERATED_DESTINATION_TREE,
    GENERATED_SOURCE_TREE,
    GENERATED_SOURCE_JSON,
)

from organize_it.bin.command_line_parser import CommandLineParser
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
    cli_parser = CommandLineParser()

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

    # Current Structure
    file_manager = FileManager(source_directory, CONFIG)

    # Read the source directory and create oIt tree input dictionary and save it to a file
    source_tree_dict = file_manager.file_walk(source_directory, GENERATED_SOURCE_JSON)

    # write the source tree structure result to a file
    tree_structure = TreeStructure()
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(GENERATED_SOURCE_TREE, "w", encoding="utf-8") as generated_tree_file:
        tree_structure.generate_tree_structure(
            source_tree_dict, "", generated_tree_file
        )

    # Categorize the files and dirs based on the given config
    categorizer = Categorizer(CONFIG)
    categorized_tree_dict = categorizer.categorize_dict(source_tree_dict, True)

    with open(GENERATED_DESTINATION_TREE, "w", encoding="utf-8") as generated_tree_file:
        tree_structure.generate_tree_structure(
            categorized_tree_dict, "", generated_tree_file
        )

    file_manager.categorize_and_sort_file(
        CONFIG,
        categorized_tree_dict["dir"],
        destination_directory,
        source_directory,
        move_files,  # To delete the source files.
    )
    # TODO: copy files based on the new sorted to destination.
    # Explore SYMLINKS(unix), Junction(Windows)

    # TODO: optionally remove the files from source.


if __name__ == "__main__":
    main()
