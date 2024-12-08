# Load all the fixtures
import pytest

from organizeIt.schemaValidation import Validator
from organizeIt.settings import CONFIG

def test_validate_schama():
    validator = Validator.YAMLConfigValidator(CONFIG)
    assert validator.validate_config() == True