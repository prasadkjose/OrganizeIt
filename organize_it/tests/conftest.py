""" Add necessary global fixtrues here """

import os
import pytest
from organize_it.tests.test_utils import (
    generate_samples_with_config,
)
from organize_it.settings import TEST_FIXTURES_DIR
from organize_it.tests._fixtures.directory_structure_fixtures import (
    GENERATED_ROOT_DIR_NAME,
    directory_structure,
)


@pytest.fixture(scope="session")
def test_setup():
    generate_samples_with_config(
        os.path.join(TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME),
        directory_structure,
    )
