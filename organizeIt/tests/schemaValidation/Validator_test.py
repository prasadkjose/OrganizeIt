# Load all the fixtures
import pytest
import logging

LOGGER = logging.getLogger(__name__)

from organizeIt.schemaValidation import Validator
from organizeIt.settings import TEST_FIXTURES_CONFIGS as CONFIG

class TestValidator:

    def test_validate_schema(self, caplog):
        validator = Validator.YAMLConfigValidator(CONFIG[1])
        assert validator.validate_config() == True

        validator = Validator.YAMLConfigValidator(CONFIG[0])
        assert "Blueprint validation error: {'png': None, 'jpg': None} is not of type 'array' / Reason: {'type': 'array'} / Where: ['format', 'photo', 'format']" in caplog.text


def test_validator(caplog):
    v = TestValidator()
    v.test_validate_schema(caplog)