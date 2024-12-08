import logging

from organizeIt.schemaValidation import Validator # Validator.py
from organizeIt.settings import CONFIG

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


if __name__ == '__main__':
    main() 