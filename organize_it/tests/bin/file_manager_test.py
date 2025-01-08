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
    GENERATED_SOURCE_JSON,
    UNCATEGORIZED_DIR_PATH,
)
from organize_it.tests.test_utils import dicts_are_equal

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

        sample_dest_dir = "some/dummy/path"

        manager = FileManager(
            source_path=UNCATEGORIZED_DIR_PATH, destination_path=sample_dest_dir
        )
        tree_dict = manager.file_walk(current_dir=None, file_path=GENERATED_SOURCE_JSON)

        assert dicts_are_equal(UNCATEGORIZED_DIR_DICTIONARY, tree_dict) is True

    def test_categorize_and_sort_file(self):
        """Test FileManager.categorize_and_sort_file method to sort files with sample generated directories and files."""
        destination_directory = os.path.join(
            TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
        )
        source_directory = os.path.join(
            TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
        )
        manager = FileManager(source_directory, destination_directory)

        manager.categorize_and_sort_file(
            config=CONFIG[1], sorted_tree_dict=CATEGORIZED_DIR_DICTIONARY
        )

        # perform file walk and test with fixture.
        manager = FileManager(destination_directory, "")
        tree_dict = manager.file_walk()

        fixture = {
            "document": {
                DIR: {},
                FILES: ["document/dir.doc", "document/dir.pdf"],
            },
            "photo": {DIR: {}, FILES: ["photo/dir.jpg"]},
            "photo_by_name": {FILES: ["photo_by_name/dir-image.jpg"], DIR: {}},
            "project_by_name": {
                FILES: ["project_by_name/dir-project.doc"],
                DIR: {},
            },
            "subDir1": {
                DIR: {
                    "photo_by_name": {
                        FILES: ["subDir1/photo_by_name/subDir1-image.jpg"],
                        DIR: {},
                    },
                    "project_by_name": {
                        FILES: ["subDir1/project_by_name/subDir1-project.doc"],
                        DIR: {},
                    },
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
                            "photo_by_name": {
                                FILES: [
                                    "subDir1/subSubDir1/photo_by_name/subSubDir1-image.jpg"
                                ],
                                DIR: {},
                            },
                            "project_by_name": {
                                FILES: [
                                    "subDir1/subSubDir1/project_by_name/subSubDir1-project.doc"
                                ],
                                DIR: {},
                            },
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
                    "photo_by_name": {
                        FILES: ["subDir2/photo_by_name/subDir2-image.jpg"],
                        DIR: {},
                    },
                    "project_by_name": {
                        FILES: ["subDir2/project_by_name/subDir2-project.doc"],
                        DIR: {},
                    },
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
                            "photo_by_name": {
                                FILES: [
                                    "subDir2/subSubDir2/photo_by_name/subSubDir2-image.jpg"
                                ],
                                DIR: {},
                            },
                            "project_by_name": {
                                FILES: [
                                    "subDir2/subSubDir2/project_by_name/subSubDir2-project.doc"
                                ],
                                DIR: {},
                            },
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

        assert dicts_are_equal(fixture, tree_dict[DIR]) is True
