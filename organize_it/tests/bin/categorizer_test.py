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
from organize_it.tests.test_utils import dicts_are_equal


@pytest.mark.usefixtures("test_setup")
class TestCategorizer:
    """Main testing class for Categorizer Class"""

    def test_categorize_dict(self):
        """Test Categorizer.categorize_dict method to create oIt input dictionary from a given config file"""

        categorizer = Categorizer(CONFIG[1])
        oit_tree_dict = categorizer.categorize_dict(UNCATEGORIZED_DIR_DICTIONARY, False)
        assert oit_tree_dict[DIR] == {
            "photo": {FILES: ["./dir.jpg"], DIR: {}},
            "document": {FILES: ["./dir.doc", "./dir.pdf"], DIR: {}},
            "photo_by_name": {FILES: ["./dir-image.jpg"], DIR: {}},
            "project_by_name": {FILES: ["./dir-project.doc"], DIR: {}},
        }

        oit_tree_dict_recursive = categorizer.categorize_dict(
            UNCATEGORIZED_DIR_DICTIONARY, True
        )
        assert (
            dicts_are_equal(CATEGORIZED_DIR_DICTIONARY, oit_tree_dict_recursive[DIR])
            is True
        )

    def test_filter_excluded_names(self):
        """Test Categorizer.filter_excluded_names with a list of sample names and exclusion list"""
        # Sample regex expressions to rest for
        test_config = {
            "rules": [{"skip": {DIR: r"\bkeystore|.app$", FILES: r".xxl$|.pga$"}}]
        }

        sample_dir_names = [
            "Visual Studo Code.app",
            "something-keystore-123",
            "no-regex-match",
        ]
        sample_file_names = ["important.xxl", "something.pga", "no-regex-match.txt"]
        categorizer = Categorizer(test_config)

        # Test directories exclusion
        filtered_list = categorizer.filter_excluded_names(sample_dir_names, True)
        assert filtered_list == ["no-regex-match"]

        filtered_list = categorizer.filter_excluded_names(sample_file_names, False)
        assert filtered_list == ["no-regex-match.txt"]

    def test_check_name_pattern(self):
        """Test Categorizer.check_name_pattern with a list of sample names and name_pattern config"""

        test_config = {
            "rules": [
                {
                    "names": {
                        "dir1": {"name_pattern": "^dir1"},  # start with dir1
                        "proj": {
                            "name_pattern": "proj*"
                        },  # end with proj before extension
                    }
                }
            ]
        }
        sample_file_names = [
            ("no_match_at_all.cx", None),
            ("dir1_somefile.as", "dir1"),
            ("dir1_somefile.proj", "proj"),  # the last defined rule will be matched
        ]
        categorizer = Categorizer(test_config)

        for name, d in sample_file_names:
            matched_dir = categorizer.check_name_pattern(name)
            assert matched_dir == d
