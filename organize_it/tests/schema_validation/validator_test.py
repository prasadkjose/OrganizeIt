""" Load all the fixtures """

import logging
from organize_it.schema_validation.validator import YAMLConfigValidator
from organize_it.settings import TEST_FIXTURES_CONFIGS as CONFIG

LOGGER = logging.getLogger(__name__)


class TestValidator:
    """Testing class for schema validator module"""

    def test_validate_schema(self, caplog):
        """Test cases for schema validation"""
        v = YAMLConfigValidator(CONFIG[1])
        assert v.validate_config() is True

        v = YAMLConfigValidator(CONFIG[0])
        assert (
            "Blueprint validation error: {'png': None, 'jpg': None} is not of type 'array' / Reason: {'type': 'array'} / Where: ['format', 'photo', 'format']"
            in caplog.text
        )
