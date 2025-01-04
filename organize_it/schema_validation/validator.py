""" validator Class """

import logging
import jsonschema

from organize_it.settings import SCHEMA, exit_gracefully

LOGGER = logging.getLogger(__name__)


class YAMLConfigValidator:
    """
    A class responsible for validating YAML configuration files.

    This class is designed to load and validate YAML configuration files
    against predefined json-schema to ensure the configuration is valid
    before being used in the tool. It checks for required fields, data types,
    and any additional validation rules that may apply to the configuration.

    """

    def __init__(self, config_data):
        """
        Initializes the YAMLConfigValidator instance with the json-schema and YAML config.
        """
        self.__obj_schema = SCHEMA
        self.__yaml_data = config_data

    def validate_config(self) -> bool:
        """
        Validates the YAML config against the schema.

        This function checks whether the keys and values in the YAML data
        conform to the rules defined in the schema. It performs the following:

        Returns:
            bool: True if the YAML data is valid, False otherwise.

        Raises:
            ValidationError: If the YAML data does not conform to the validation rules.
        """
        LOGGER.info(" - Starting Config Validation.")
        # Create the validator instance
        self.__obj_validator = jsonschema.Draft202012Validator(
            self.__obj_schema,
            format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
        )
        return self.__handle_errors()

    def __handle_errors(self):
        obj_errors = self.__obj_validator.iter_errors(self.__yaml_data)
        lst_errors = []
        for error in obj_errors:
            lst_errors.append(error)

        if len(lst_errors) == 0:
            LOGGER.info(" - Config is Successfully Validated.")
            return True
        else:
            for item_error in lst_errors:
                exit_gracefully(
                    (
                        " - Blueprint validation error: %s / Reason: %s / Where: %s ",
                        item_error.message,
                        str(item_error.schema),
                        str(list(item_error.absolute_path)),
                    ),
                )
