import os
import logging

LOGGER = logging.getLogger(__name__)

from organizeIt.bin.FileManager import FileManager, DIR, FILES
from organizeIt.settings import TEST_FIXTURES_DIR
from organizeIt.tests._fixtures.generate_samples_utils import generate_samples_with_config

ROOT_DIR_NAME = 'generatedFiles'

# Example input format
directory_structure = {
    DIR: {
        ROOT_DIR_NAME: {
            DIR: {
                'subdir1': {
                    DIR: {
                        'subsubdir1': {
                            FILES: ['subsubfile1.txt'],
                            DIR: {}
                        }
                    },
                    FILES: ['subfileA.txt', 'subfileB.txt'],                    
                },
                'subdir2': {
                    FILES: ['subdir2file.txt'],
                    DIR: {}
                }
            },
            FILES: ['file1.txt', 'file2.txt'],
        }
    }
}

class TestFileManager:
    def test_directory_structure_dict(self, caplog):
        generate_samples_with_config(directory_structure)
        manager = FileManager()
        tree_dict = manager.file_walk(os.path.join(TEST_FIXTURES_DIR, "generatedFiles"))
        assert directory_structure[DIR][ROOT_DIR_NAME] == tree_dict

        # TODO: compare generated tree structure and tmp file to fixture. 
        # manager.generate_tree_structure(tree_dict, "")
