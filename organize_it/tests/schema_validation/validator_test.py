""" Load all the fixtures """

import pytest
import logging
from organize_it.schema_validation.validator import (
    JSONSchemaValidator,
    PydanticSchemaValidator,
)
from organize_it.settings import TEST_FIXTURES_CONFIGS as CONFIG, SCHEMA
from organize_it.configs.config_schema import ConfigSchema  # Pydantic models

LOGGER = logging.getLogger(__name__)


@pytest.mark.usefixtures("test_setup")
class TestValidator:
    """Testing class for schema validator module"""

    def test_JSONSchemaValidator_schema(self, caplog):
        """Test JSONSchemaValidator cases for schema validation"""
        v = JSONSchemaValidator(config_data=CONFIG[1], schema=SCHEMA)
        assert v.validate_config() is True

        v = JSONSchemaValidator(config_data=CONFIG[2], schema=SCHEMA)
        with pytest.raises(SystemExit):
            v.validate_config()

        assert (
            # pylint: disable=line-too-long
            "- Exiting due to an error: (' - Blueprint validation error:"
            in caplog.text
        )

    def test_PydanticSchemaValidator_schema(self, caplog):
        """Test PydanticSchemaValidator cases for schema validation"""
        v = PydanticSchemaValidator(config_data=CONFIG[1], schema=ConfigSchema)
        assert v.validate_config() is True

        v = PydanticSchemaValidator(config_data=CONFIG[2], schema=ConfigSchema)
        with pytest.raises(SystemExit):
            v.validate_config()

        assert " - Exiting due to an error: list_type" in caplog.text
