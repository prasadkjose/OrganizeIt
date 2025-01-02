""" Testing module tree_structure """

import pytest
import filecmp
from organize_it.bin.tree_structure import TreeStructure
from organize_it.tests._fixtures.directory_structure_fixtures import (
    GENERATED_ROOT_DIR_NAME,
    directory_structure,
)
from organize_it.settings import (
    TEST_FIXTURES_DIR,
)


@pytest.mark.usefixtures("test_setup")
class TestTreeStructure:
    """Main testing class for TreeStructure Class"""

    def test_generate_tree_structure(self):
        """Test TreeStructure.generate_tree_structure method with sample generated directories and files."""

        tree_structure = TreeStructure()

        # Compare generated tree structure in .tmp file to fixture.
        with open(
            f"{TEST_FIXTURES_DIR}/{GENERATED_ROOT_DIR_NAME}/.generated_tests.tree",
            "w",
            encoding="utf-8",
        ) as generated_tree_file:
            tree_structure.generate_tree_structure(
                directory_structure, "", generated_tree_file
            )

        assert (
            filecmp.cmp(
                f"{TEST_FIXTURES_DIR}/{GENERATED_ROOT_DIR_NAME}/.generated_tests.tree",
                f"{TEST_FIXTURES_DIR}/.generated_tests_fixture.tree",
            )
            is True
        )
