""" Testing Module for subroutines"""

import pytest
import os
from organize_it.bin.subroutines import (
    process_source_and_generate_tree,
    categorize_and_generate_dest_tree,
)
from organize_it.tests._fixtures.directory_structure_fixtures import (
    UNCATEGORIZED_DIR_PATH,
    CATEGORIZED_DIR_PATH,
    GENERATED_SOURCE_JSON,
    UNCATEGORIZED_DIR_DICTIONARY,
    GENERATED_ROOT_DIR_NAME,
    CATEGORIZED_TREE_PATH,
    CATEGORIZED_DIR_DICTIONARY,
)
from organize_it.settings import (
    DIR,
    get_or_update_current_state,
    TEST_FIXTURES_DIR,
    TEST_FIXTURES_CONFIGS as CONFIG,
)

from organize_it.tests.test_utils import dicts_are_equal
from organize_it.bin.file_manager import FileManager
from organize_it.bin.tree_structure import TreeStructure


@pytest.mark.usefixtures("test_setup")
class TestSubroutines:
    """Main testing class for the different subroutines"""

    def test_process_source_and_generate_tree(self):
        """Sanity test to create and process source tree"""
        generated_source_tree_path = (
            f"{TEST_FIXTURES_DIR}/{GENERATED_ROOT_DIR_NAME}/.generated_tests.tree"
        )

        assert get_or_update_current_state() is False

        file_manager, tree_structure, source_dict = process_source_and_generate_tree(
            source_directory=UNCATEGORIZED_DIR_PATH,
            destination_directory=CATEGORIZED_DIR_PATH,
            generated_source_tree_path=generated_source_tree_path,
            generated_source_json=GENERATED_SOURCE_JSON,
        )
        # confirm both files are created.
        assert os.path.exists(generated_source_tree_path) is True
        assert os.path.exists(GENERATED_SOURCE_JSON) is True

        # test tool current state
        assert get_or_update_current_state() is True

        # Test with fresh run
        assert isinstance(file_manager, FileManager)
        assert isinstance(tree_structure, TreeStructure)
        assert dicts_are_equal(UNCATEGORIZED_DIR_DICTIONARY, source_dict) is True

        # Test with stale run. One way to test this is to delete the generated json file from the previous run and call the method again.
        #  When it tried to read the file, instead of creating one(like in a fresh run), we can catch the error.
        # TODO: A better way would be to cache the instances and then compare equality

        # Delete the generated GENERATED_SOURCE_JSON file from above.
        os.remove(GENERATED_SOURCE_JSON)
        assert os.path.exists(GENERATED_SOURCE_JSON) is False

        assert get_or_update_current_state() is True

        with pytest.raises(FileNotFoundError) as exc_info:
            _ = process_source_and_generate_tree(
                source_directory=UNCATEGORIZED_DIR_PATH,
                destination_directory=CATEGORIZED_DIR_PATH,
                generated_source_tree_path=generated_source_tree_path,
                generated_source_json=GENERATED_SOURCE_JSON,
            )
        # In a stale run, we try to read from the previously generated configs.
        assert isinstance(exc_info.value, FileNotFoundError) is True

    def test_categorize_and_generate_dest_tree(self, pytestconfig):
        """Sanity test to sort and categorize oIt dict and check the generated tree"""
        clean = pytestconfig.getoption("clean")

        tree_structure = TreeStructure()
        if clean:
            assert os.path.exists(CATEGORIZED_TREE_PATH) is False
        categorized_tree_dict = categorize_and_generate_dest_tree(
            config=CONFIG[1],
            source_tree_dict=UNCATEGORIZED_DIR_DICTIONARY,
            tree_structure=tree_structure,
            dest_tree_path=CATEGORIZED_TREE_PATH,
        )
        assert os.path.exists(CATEGORIZED_TREE_PATH) is True
        assert (
            dicts_are_equal(CATEGORIZED_DIR_DICTIONARY, categorized_tree_dict[DIR])
            is True
        )
