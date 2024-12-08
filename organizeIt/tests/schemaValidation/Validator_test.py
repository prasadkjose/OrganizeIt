from organizeIt.schemaValidation import Validator
from organizeIt.settings import CONFIG

def validate_schama():
    schema_validator = Validator.YAMLConfigValidator(CONFIG)
    assert schema_validator.validate_config() == True


