""" Testing module tree_structure """

import pytest
import filecmp
from organize_it.bin.tree_structure import TreeStructure
from organize_it.tests.conftest import directory_structure
from organize_it.settings import (
    DIR,
    TMP_DIR,
    TEST_FIXTURES_DIR,
    TEST_FIXTURES_CONFIGS as CONFIG,
)


@pytest.mark.usefixtures("test_setup")
class TestTreeStructure:
    """Main testing class for TreeStructure Class"""

    def test_generate_tree_structure(self):
        """Test TreeStructure.generate_tree_structure method with sample generated directories and files."""

        tree_structure = TreeStructure()

        # Compare generated tree structure in .tmp file to fixture.
        with open(f"{TMP_DIR}/.generated_tests.tree", "w") as generated_tree_file:
            tree_structure.generate_tree_structure(
                directory_structure, "", generated_tree_file
            )

        assert (
            filecmp.cmp(
                f"{TMP_DIR}/.generated_tests.tree",
                f"{TEST_FIXTURES_DIR}/.generated_tests_fixture.tree",
            )
            is True
        )

    def test_yaml_config_to_dict(self):
        """Test TreeStructure.yaml_config_to_dict method to create oIt input dictionary from a given config file"""

        tree_structure = TreeStructure()
        oit_tree_dict = tree_structure.yaml_config_to_dict(CONFIG[1])
        assert oit_tree_dict[DIR] == {
            "photo": {},
            "video": {},
            "document": {},
            "compressed": {},
        }

        oit_tree_dict = tree_structure.yaml_config_to_dict(CONFIG[0])
        assert oit_tree_dict[DIR] == {
            "photo": {DIR: {"photoA": {}}},
            "video": {},
            "document": {DIR: {"documentA": {}}},
            "compressed": {},
        }
