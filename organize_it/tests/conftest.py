""" Add necessary global fixtrues here """

import os
import pytest
from organize_it.tests._fixtures.generate_samples_utils import (
    generate_samples_with_config,
)
from organize_it.settings import FILES, DIR, TEST_FIXTURES_DIR

GENERATED_ROOT_DIR_NAME = "generated_files"
UNCATEGORIZED_DIR_NAME = "uncategorized_test_directory"
CATEGORIZED_DIR_NAME = "categorized_test_directory"


# Example input format
directory_structure = {
    DIR: {
        UNCATEGORIZED_DIR_NAME: {
            DIR: {
                "subdir1": {
                    DIR: {"subsubdir1": {FILES: ["subsubfile1.txt"], DIR: {}}},
                    FILES: ["subfileA.txt", "subfileB.txt"],
                },
                "subdir2": {FILES: ["subdir2file.txt"], DIR: {}},
            },
            FILES: ["file1.pdf", "file2.txt", "file3.jpg"],
        }
    },
    FILES: [],
}


@pytest.fixture(scope="session")
def test_setup():
    generate_samples_with_config(
        os.path.join(TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME),
        directory_structure,
    )
