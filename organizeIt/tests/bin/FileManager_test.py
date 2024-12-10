import os
import logging

LOGGER = logging.getLogger(__name__)

from organizeIt.bin import FileManager
from organizeIt.settings import TEST_FIXTURES_DIR
from organizeIt.tests._fixtures.generate_samples_utils import generate_samples_with_config

class TestFileManager:
    def test_directory_structure_dict(self, caplog):
        generate_samples_with_config()
        manager = FileManager.FileManager()
        tree_dict = manager.file_walk(os.path.join(TEST_FIXTURES_DIR, "generatedFiles"))
        # TODO: assert the result
        manager.print_tree_structure(tree_dict, "")
