""" Testing module file_manager """

import os
import logging
import pytest

from organize_it.bin.file_manager import FileManager
from organize_it.tests.conftest import ROOT_DIR_NAME, directory_structure
from organize_it.settings import TEST_FIXTURES_DIR, DIR, FILES

LOGGER = logging.getLogger(__name__)

tree_walk_result = {
    DIR: {
        ROOT_DIR_NAME: {
            DIR: {
                "subdir1": {
                    DIR: {
                        "subsubdir1": {FILES: ["subsubdir1/subsubfile1.txt"], DIR: {}}
                    },
                    FILES: ["subdir1/subfileA.txt", "subdir1/subfileB.txt"],
                },
                "subdir2": {FILES: ["subdir2/subdir2file.txt"], DIR: {}},
            },
            FILES: ["./file1.pdf", "./file2.txt", "./file3.jpg"],
        }
    },
    FILES: [],
}


@pytest.mark.usefixtures("test_setup")
class TestFileManager:
    """Main testing class for FileManger module"""

    def test_file_walk(self):
        """Test FileManager.file_walk method with sample generated directories and files."""

        manager = FileManager()
        tree_dict = manager.file_walk(os.path.join(TEST_FIXTURES_DIR, ROOT_DIR_NAME))
        assert tree_walk_result[DIR][ROOT_DIR_NAME] == tree_dict

    def test_categorize_and_sort_file(self):
        """Test FileManager.categorize_and_sort_file method to sort files with sample generated directories and files."""
        categorized_test_directory = "categorized_test_directory"
        destination_directory = os.path.join(
            TEST_FIXTURES_DIR, ROOT_DIR_NAME, categorized_test_directory
        )
        source_directory = os.path.join(TEST_FIXTURES_DIR, ROOT_DIR_NAME)
        manager = FileManager()
        sorted_tree_dict = {
            DIR: {
                "photo": {FILES: ["./file3.jpg"], DIR: {}},
                "document": {FILES: ["./file1.pdf", "./file2.txt"], DIR: {}},
            },
            FILES: [],
        }
        manager.categorize_and_sort_file(
            sorted_tree_dict, destination_directory, source_directory
        )

        # perform file walk and test with fixture.
        tree_dict = manager.file_walk(
            os.path.join(TEST_FIXTURES_DIR, ROOT_DIR_NAME, categorized_test_directory)
        )
        resultant_tree = {
            DIR: {
                "photo": {FILES: ["photo/file3.jpg"], DIR: {}},
                "document": {
                    FILES: ["document/file1.pdf", "document/file2.txt"],
                    DIR: {},
                },
            },
            FILES: [],
        }
        assert resultant_tree == tree_dict
