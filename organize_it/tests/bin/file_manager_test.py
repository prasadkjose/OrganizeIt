""" Testing module file_manager """

import os
import logging
import pytest

from organize_it.bin.file_manager import FileManager
from organize_it.tests.conftest import ROOT_DIR_NAME, directory_structure
from organize_it.settings import TEST_FIXTURES_DIR, DIR

LOGGER = logging.getLogger(__name__)


@pytest.mark.usefixtures("test_setup")
class TestFileManager:
    """Main testing class for FileManger module"""

    def test_file_walk(self):
        """Test FileManager.file_walk method with sample generated directories and files."""

        manager = FileManager()
        tree_dict = manager.file_walk(os.path.join(TEST_FIXTURES_DIR, ROOT_DIR_NAME))
        assert directory_structure[DIR][ROOT_DIR_NAME] == tree_dict
