""" Add necessary global fixtrues here """

import pytest
from organize_it.tests._fixtures.generate_samples_utils import (
    generate_samples_with_config,
)
from organize_it.settings import FILES, DIR, TEST_FIXTURES_DIR

ROOT_DIR_NAME = "generated_files"

# Example input format
directory_structure = {
    DIR: {
        ROOT_DIR_NAME: {
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
    generate_samples_with_config(TEST_FIXTURES_DIR, directory_structure)
