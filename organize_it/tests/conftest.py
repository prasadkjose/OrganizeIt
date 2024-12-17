""" Add necessary global fixtrues here """

import os
import pytest
from organize_it.tests._fixtures.generate_samples_utils import (
    generate_samples_with_config,
)
from organize_it.settings import FILES, DIR, TEST_FIXTURES_DIR

GENERATED_ROOT_DIR_NAME = "generated_files"
UNCATEGORIZED_DIR_NAME = "uncategorized_test_directory"
CATEGORIZED_DIR_NAME = "categorized_test_directory"


# Example input format
directory_structure = {
    DIR: {
        UNCATEGORIZED_DIR_NAME: {
            DIR: {
                "subDir1": {
                    DIR: {
                        "subSubDir1": {
                            DIR: {},
                            FILES: [
                                "subSubDir1.jpg",
                                "subSubDir1.pdf",
                                "subSubDir1.doc",
                            ],
                        }
                    },
                    FILES: ["subDir1.jpg", "subDir1.pdf", "subDir1.doc"],
                },
                "subDir2": {
                    DIR: {
                        "subSubDir2": {
                            DIR: {},
                            FILES: [
                                "subSubDir2.jpg",
                                "subSubDir2.pdf",
                                "subSubDir2.doc",
                            ],
                        }
                    },
                    FILES: ["subDir2.jpg", "subDir2.pdf", "subDir2.doc"],
                },
            },
            FILES: ["dir.jpg", "dir.pdf", "dir.doc"],
        }
    },
    FILES: [],
}

# Categorized and sorted file structure with relative source path of the files.  
CATEGORIZED_DIR_DICTIONARY = {
    "photo": {FILES: ["./dir.jpg"], DIR: {}},
    "document": {FILES: ["./dir.doc", "./dir.pdf"], DIR: {}},
    "subDir1": {
        FILES: [],
        DIR: {
            "photo": {FILES: ["subDir1/subDir1.jpg"], DIR: {}},
            "document": {
                FILES: ["subDir1/subDir1.doc", "subDir1/subDir1.pdf"],
                DIR: {},
            },
            "subSubDir1": {
                FILES: [],
                DIR: {
                    "photo": {FILES: ["subDir1/subSubDir1/subSubDir1.jpg"], DIR: {}},
                    "document": {
                        FILES: [
                            "subDir1/subSubDir1/subSubDir1.doc",
                            "subDir1/subSubDir1/subSubDir1.pdf",
                        ],
                        DIR: {},
                    },
                },
            },
        },
    },
    "subDir2": {
        FILES: [],
        DIR: {
            "photo": {FILES: ["subDir2/subDir2.jpg"], DIR: {}},
            "document": {
                FILES: ["subDir2/subDir2.doc", "subDir2/subDir2.pdf"],
                DIR: {},
            },
            "subSubDir2": {
                FILES: [],
                DIR: {
                    "photo": {FILES: ["subDir2/subSubDir2/subSubDir2.jpg"], DIR: {}},
                    "document": {
                        FILES: [
                            "subDir2/subSubDir2/subSubDir2.doc",
                            "subDir2/subSubDir2/subSubDir2.pdf",
                        ],
                        DIR: {},
                    },
                },
            },
        },
    },
}

UNCATEGORIZED_DIR_DICTIONARY = {
    DIR: {
        "subDir2": {
            DIR: {
                "subSubDir2": {
                    DIR: {},
                    FILES: [
                        "subDir2/subSubDir2/subSubDir2.doc",
                        "subDir2/subSubDir2/subSubDir2.jpg",
                        "subDir2/subSubDir2/subSubDir2.pdf",
                    ],
                }
            },
            FILES: [
                "subDir2/subDir2.doc",
                "subDir2/subDir2.jpg",
                "subDir2/subDir2.pdf",
            ],
        },
        "subDir1": {
            DIR: {
                "subSubDir1": {
                    DIR: {},
                    FILES: [
                        "subDir1/subSubDir1/subSubDir1.doc",
                        "subDir1/subSubDir1/subSubDir1.jpg",
                        "subDir1/subSubDir1/subSubDir1.pdf",
                    ],
                }
            },
            FILES: [
                "subDir1/subDir1.doc",
                "subDir1/subDir1.jpg",
                "subDir1/subDir1.pdf",
            ],
        },
    },
    FILES: ["./dir.doc", "./dir.jpg", "./dir.pdf"],
}


@pytest.fixture(scope="session")
def test_setup():
    generate_samples_with_config(
        os.path.join(TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME),
        directory_structure,
    )
