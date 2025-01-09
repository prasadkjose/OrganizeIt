""" Add necessary global fixtrues here """

import os
import pytest
import shutil

from organize_it.tests.test_utils import (
    generate_samples_with_config,
)
from organize_it.settings import TEST_FIXTURES_DIR
from organize_it.tests._fixtures.directory_structure_fixtures import (
    GENERATED_ROOT_DIR_NAME,
    directory_structure,
)


def pytest_addoption(parser):
    parser.addoption("--keep", action="store_true", default=False)
    parser.addoption("--ai", action="store_true", default=False)


@pytest.fixture(scope="session")
def test_setup(pytestconfig):
    cleanup(pytestconfig)

    generate_samples_with_config(
        os.path.join(TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME),
        directory_structure,
    )

    yield
    cleanup(pytestconfig)


def cleanup(pytestconfig):
    should_cleanup = not pytestconfig.getoption("keep")
    generated_path = os.path.join(TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME)
    #  Clean up the generated files.
    if should_cleanup:
        shutil.rmtree(generated_path)

    os.makedirs(generated_path, exist_ok=True)
