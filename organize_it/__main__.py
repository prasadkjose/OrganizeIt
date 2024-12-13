""" Main """

import logging
import os

from organize_it.settings import TEST_FIXTURES_DIR, TMP_DIR
from organize_it.bin.file_manager import FileManager

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

    # Create and return a dict of files and directories
    file_manager = FileManager()
    # TODO: Take Source and destination as CLI args.
    tree_dict = file_manager.file_walk(TEST_FIXTURES_DIR + "/generated_files")

    # write to a temp buffer
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(f"{TMP_DIR}/.generated.tree", "w") as generated_tree_file:
        file_manager.generate_tree_structure(tree_dict, "", generated_tree_file)


if __name__ == "__main__":
    main()
