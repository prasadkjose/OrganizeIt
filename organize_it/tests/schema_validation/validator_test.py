""" Load all the fixtures """

import pytest
import logging
from organize_it.schema_validation.validator import YAMLConfigValidator
from organize_it.settings import TEST_FIXTURES_CONFIGS as CONFIG

LOGGER = logging.getLogger(__name__)


@pytest.mark.usefixtures("test_setup")
class TestValidator:
    """Testing class for schema validator module"""

    def test_validate_schema(self, caplog):
        """Test cases for schema validation"""
        v = YAMLConfigValidator(CONFIG[1])
        assert v.validate_config() is True

        v = YAMLConfigValidator(CONFIG[2])
        with pytest.raises(SystemExit):
            v.validate_config()
            assert (
                # pylint: disable=line-too-long
                "Blueprint validation error: {'png': None, 'jpg': None} is not of type 'array' / Reason: {'type': 'array'} / Where: ['format', 'photo', 'types']"
                in caplog.text
            )
