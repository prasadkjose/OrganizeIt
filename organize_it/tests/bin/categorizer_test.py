""" Testing module categorizer """

import pytest
from organize_it.bin.categorizer import Categorizer
from organize_it.settings import (
    FILES,
    DIR,
    TEST_FIXTURES_CONFIGS as CONFIG,
)

unsorted_fixuture = {
    DIR: {
        "subDir1": {
            DIR: {
                "subSubDir1": {
                    DIR: {},
                    FILES: ["subSubDir1.jpg", "subSubDir1.pdf", "subSubDir1.doc"],
                }
            },
            FILES: ["subDir1.jpg", "subDir1.pdf", "subDir1.doc"],
        },
        "subDir2": {
            DIR: {
                "subSubDir2": {
                    DIR: {},
                    FILES: ["subSubDir2.jpg", "subSubDir2.pdf", "subSubDir2.doc"],
                }
            },
            FILES: ["subDir2.jpg", "subDir2.pdf", "subDir2.doc"],
        },
    },
    FILES: ["dir.jpg", "dir.pdf", "dir.doc"],
}


@pytest.mark.usefixtures("test_setup")
class TestCategorizer:
    """Main testing class for Categorizer Class"""

    def test_categorize_dict(self):
        """Test TreeStructure.categorize_dict method to create oIt input dictionary from a given config file"""

        tree_structure = Categorizer()
        oit_tree_dict = tree_structure.categorize_dict(
            CONFIG[1], unsorted_fixuture, False
        )
        assert oit_tree_dict[DIR] == {
            "photo": {FILES: ["dir.jpg"], DIR: {}},
            "document": {FILES: ["dir.pdf", "dir.doc"], DIR: {}},
        }

        oit_tree_dict_recursive = tree_structure.categorize_dict(
            CONFIG[1], unsorted_fixuture, True
        )
        assert oit_tree_dict_recursive[DIR] == {
            "photo": {FILES: ["dir.jpg"], DIR: {}},
            "document": {FILES: ["dir.pdf", "dir.doc"], DIR: {}},
            "subDir1": {
                FILES: [],
                DIR: {
                    "photo": {FILES: ["subDir1.jpg"], DIR: {}},
                    "document": {FILES: ["subDir1.pdf", "subDir1.doc"], DIR: {}},
                    "subSubDir1": {
                        FILES: [],
                        DIR: {
                            "photo": {FILES: ["subSubDir1.jpg"], DIR: {}},
                            "document": {
                                FILES: ["subSubDir1.pdf", "subSubDir1.doc"],
                                DIR: {},
                            },
                        },
                    },
                },
            },
            "subDir2": {
                FILES: [],
                DIR: {
                    "photo": {FILES: ["subDir2.jpg"], DIR: {}},
                    "document": {FILES: ["subDir2.pdf", "subDir2.doc"], DIR: {}},
                    "subSubDir2": {
                        FILES: [],
                        DIR: {
                            "photo": {FILES: ["subSubDir2.jpg"], DIR: {}},
                            "document": {
                                FILES: ["subSubDir2.pdf", "subSubDir2.doc"],
                                DIR: {},
                            },
                        },
                    },
                },
            },
        }
