""" Testing module categorizer """

import pytest
from organize_it.bin.categorizer import Categorizer
from organize_it.settings import (
    FILES,
    DIR,
    TEST_FIXTURES_CONFIGS as CONFIG,
)
from organize_it.tests._fixtures.directory_structure_fixtures import (
    UNCATEGORIZED_DIR_DICTIONARY,
    CATEGORIZED_DIR_DICTIONARY,
)


@pytest.mark.usefixtures("test_setup")
class TestCategorizer:
    """Main testing class for Categorizer Class"""

    def test_categorize_dict(self):
        """Test TreeStructure.categorize_dict method to create oIt input dictionary from a given config file"""

        tree_structure = Categorizer(CONFIG[1])
        oit_tree_dict = tree_structure.categorize_dict(
            UNCATEGORIZED_DIR_DICTIONARY, False
        )
        assert oit_tree_dict[DIR] == {
            "photo": {FILES: ["./dir.jpg"], DIR: {}},
            "document": {FILES: ["./dir.doc", "./dir.pdf"], DIR: {}},
        }

        oit_tree_dict_recursive = tree_structure.categorize_dict(
            UNCATEGORIZED_DIR_DICTIONARY, True
        )
        assert oit_tree_dict_recursive[DIR] == CATEGORIZED_DIR_DICTIONARY
