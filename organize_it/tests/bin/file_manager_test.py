""" Testing module file_manager """

import os
import logging
import pytest

from organize_it.bin.file_manager import FileManager
from organize_it.tests._fixtures.directory_structure_fixtures import (
    GENERATED_ROOT_DIR_NAME,
    UNCATEGORIZED_DIR_NAME,
    CATEGORIZED_DIR_NAME,
    CATEGORIZED_DIR_DICTIONARY,
    UNCATEGORIZED_DIR_DICTIONARY,
)

from organize_it.settings import (
    TEST_FIXTURES_DIR,
    DIR,
    FILES,
    TEST_FIXTURES_CONFIGS as CONFIG,
)


LOGGER = logging.getLogger(__name__)


@pytest.mark.usefixtures("test_setup")
class TestFileManager:
    """Main testing class for FileManger module"""

    def test_file_walk(self):
        """Test FileManager.file_walk method with sample generated directories and files."""
        source_directory = os.path.join(
            TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
        )

        manager = FileManager(source_directory)
        tree_dict = manager.file_walk(
            source_directory,
            os.path.join(
                TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, "tree_walk_test.json"
            ),
        )
        assert UNCATEGORIZED_DIR_DICTIONARY == tree_dict

    def test_categorize_and_sort_file(self):
        """Test FileManager.categorize_and_sort_file method to sort files with sample generated directories and files."""
        destination_directory = os.path.join(
            TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
        )
        source_directory = os.path.join(
            TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
        )
        manager = FileManager(source_directory)

        manager.categorize_and_sort_file(
            CONFIG[1],
            CATEGORIZED_DIR_DICTIONARY,
            destination_directory,
            source_directory,
        )

        # perform file walk and test with fixture.
        manager = FileManager(destination_directory)
        tree_dict = manager.file_walk(
            os.path.join(
                TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
            )
        )

        fixture = {
            "document": {
                DIR: {},
                FILES: ["document/dir.doc", "document/dir.pdf"],
            },
            "photo": {DIR: {}, FILES: ["photo/dir.jpg"]},
            "subDir1": {
                DIR: {
                    "document": {
                        DIR: {},
                        FILES: [
                            "subDir1/document/subDir1.doc",
                            "subDir1/document/subDir1.pdf",
                        ],
                    },
                    "photo": {DIR: {}, FILES: ["subDir1/photo/subDir1.jpg"]},
                    "subSubDir1": {
                        DIR: {
                            "photo": {
                                DIR: {},
                                FILES: ["subDir1/subSubDir1/photo/subSubDir1.jpg"],
                            },
                            "document": {
                                DIR: {},
                                FILES: [
                                    "subDir1/subSubDir1/document/subSubDir1.doc",
                                    "subDir1/subSubDir1/document/subSubDir1.pdf",
                                ],
                            },
                        },
                        FILES: [],
                    },
                },
                FILES: [],
            },
            "subDir2": {
                DIR: {
                    "document": {
                        DIR: {},
                        FILES: [
                            "subDir2/document/subDir2.doc",
                            "subDir2/document/subDir2.pdf",
                        ],
                    },
                    "photo": {DIR: {}, FILES: ["subDir2/photo/subDir2.jpg"]},
                    "subSubDir2": {
                        DIR: {
                            "document": {
                                DIR: {},
                                FILES: [
                                    "subDir2/subSubDir2/document/subSubDir2.doc",
                                    "subDir2/subSubDir2/document/subSubDir2.pdf",
                                ],
                            },
                            "photo": {
                                DIR: {},
                                FILES: ["subDir2/subSubDir2/photo/subSubDir2.jpg"],
                            },
                        },
                        FILES: [],
                    },
                },
                FILES: [],
            },
        }
        assert fixture == tree_dict[DIR]
