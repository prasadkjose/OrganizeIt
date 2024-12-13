""" Testing module file_manager """

import os
import logging

from organize_it.bin.file_manager import FileManager, DIR, FILES
from organize_it.tests._fixtures.generate_samples_utils import (
    generate_samples_with_config,
)
from organize_it.settings import TEST_FIXTURES_DIR

LOGGER = logging.getLogger(__name__)


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
            FILES: ["file1.txt", "file2.txt"],
        }
    }
}


class TestFileManager:
    """Main testing class for FileManger module"""

    def test_directory_structure_dict(self):
        """Test FileManager.file_walk method with sample generated directories and files."""

        generate_samples_with_config(TEST_FIXTURES_DIR, directory_structure)
        manager = FileManager()
        tree_dict = manager.file_walk(os.path.join(TEST_FIXTURES_DIR, ROOT_DIR_NAME))
        assert directory_structure[DIR][ROOT_DIR_NAME] == tree_dict

        # TODO: compare generated tree structure and tmp file to fixture.
        # manager.generate_tree_structure(tree_dict, "")
