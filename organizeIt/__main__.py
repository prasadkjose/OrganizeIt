import logging

from organizeIt.schemaValidation import Validator # Validator.py
from organizeIt.settings import CONFIG, ROOT_DIR
import organizeIt.bin.FileManager as FileManager

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
    logger.info(' - Starting to organize...')

    # Validate the YAML config file
    schema_validator = Validator.YAMLConfigValidator(CONFIG)
    schema_validator.validate_config()

    # TODO: Take Source and destination as CLI args.

    # Create and return a dict of files and directories
    file_manager = FileManager.FileManager()
    tree_dict = file_manager.file_walk(ROOT_DIR._str)
    # print(tree_dict)

    file_manager.print_tree_structure(tree_dict, "")


if __name__ == '__main__':
    main() 