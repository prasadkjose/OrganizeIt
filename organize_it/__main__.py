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
    TEST_FIXTURES_DIR,
    SCHEMA,
)

from organize_it.cli.input_arg_parser import InputArgParser
from organize_it.schema_validation.validator import JSONSchemaValidator
from organize_it.bin.subroutines import (
    process_source_and_generate_tree,
    categorize_and_generate_dest_tree,
    generate_with_ai,
)

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

    # Take Source and destination as CLI args.
    # Order of preference
    #   1. CLI --src
    #   2. Source from config
    #   3. Current directory
    cli_parser = InputArgParser(
        process_source_and_generate_tree,
        categorize_and_generate_dest_tree,
        generate_with_ai,
    )

    if cli_parser.ai:
        config = generate_with_ai()
    elif cli_parser.config:
        config = cli_parser.config
    else:
        config = CONFIG

    if cli_parser.move:
        move_files = cli_parser.move
    else:
        move_files = False

    # Validate the YAML config first with the corresponding json-schema
    schema_validator = JSONSchemaValidator(config_data=config, schema=SCHEMA)
    schema_validator.validate_config()

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

    ##########################DUMMY###################################################
    destination_directory = os.path.join(
        TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
    )
    source_directory = os.path.join(
        TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
    )
    ##########################DUMMY###################################################

    file_manager, tree_structure, source_tree_dict = process_source_and_generate_tree(
        source_directory=source_directory,
        destination_directory=destination_directory,
        generated_source_tree_path=GENERATED_SOURCE_TREE,
    )
    categorized_tree_dict = categorize_and_generate_dest_tree(
        config=config,
        source_tree_dict=source_tree_dict,
        tree_structure=tree_structure,
        dest_tree_path=GENERATED_DESTINATION_TREE,
    )

    file_manager.categorize_and_sort_file(
        config=config,
        sorted_tree_dict=categorized_tree_dict[DIR],
        move_files=move_files,  # To delete the source files.
    )
    # Explore SYMLINKS(unix), Junction(Windows)


if __name__ == "__main__":
    main()
