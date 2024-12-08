import jsonschema
import yaml
import json
import os
import logging
from datetime import datetime

from organizeIt.settings import CONFIG_DIR

logger = logging.getLogger(__name__)

class YAMLConfigValidator:
    def __init__(self):
        with open(os.path.join(CONFIG_DIR, 'config-schema.json5'), 'r') as tmp_file:
            self.__obj_schema = json.load(tmp_file)

        with open(os.path.join(CONFIG_DIR, 'config.yaml'), 'r') as tmp_json_stream:
            try:
                self.__json_data = yaml.full_load(tmp_json_stream)
            except yaml.YAMLError as exception:
                raise exception
            
    def validate_config(self): 
        self.__str_DateTime = datetime.now().strftime('%H:%M:%S')
        logger.info(self.__str_DateTime + ' - Starting config Validation.')
        try:
            self.__obj_validator = jsonschema.Draft202012Validator(self.__obj_schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER)
            self.__print_errors()
        except jsonschema.exceptions.ValidationError as obj_exceptions:
            logger.exception(obj_exceptions)

    def __print_errors(self):
        self.__str_DateTime = datetime.now().strftime('%H:%M:%S')
        obj_errors = self.__obj_validator.iter_errors(self.__json_data)
        lst_errors = []
        for error in obj_errors:
            lst_errors.append(error)

        if len(lst_errors) == 0:
            logger.info(self.__str_DateTime + ' - Successfully Validated.')
        else:
            for item_error in lst_errors:
                logger.error(self.__str_DateTime + ' - Blueprint validation error: ' + item_error.message + ' / Reason: ' + str(item_error.schema) + ' / Where: ' + str(list(item_error.absolute_path)))

