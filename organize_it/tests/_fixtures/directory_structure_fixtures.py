""" Fixtures """

import os
from organize_it.settings import FILES, DIR
from organize_it.settings import (
    TEST_FIXTURES_DIR,
)

GENERATED_ROOT_DIR_NAME = "generated_files"
UNCATEGORIZED_DIR_NAME = "uncategorized_test_directory"
CATEGORIZED_DIR_NAME = "categorized_test_directory"
CATEGORIZED_TREE_FILE_NAME = "categorized__generated.tree"


GENERATED_SOURCE_JSON = os.path.join(
    TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, "tree_walk_test.json"
)
UNCATEGORIZED_DIR_PATH = os.path.join(
    TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, UNCATEGORIZED_DIR_NAME
)
CATEGORIZED_DIR_PATH = os.path.join(
    TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_DIR_NAME
)
CATEGORIZED_TREE_PATH = os.path.join(
    TEST_FIXTURES_DIR, GENERATED_ROOT_DIR_NAME, CATEGORIZED_TREE_FILE_NAME
)

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
                                "subSubDir1-image.jpg",
                                "subSubDir1-project.doc",
                            ],
                        }
                    },
                    FILES: [
                        "subDir1.jpg",
                        "subDir1.pdf",
                        "subDir1.doc",
                        "subDir1-image.jpg",
                        "subDir1-project.doc",
                    ],
                },
                "subDir2": {
                    DIR: {
                        "subSubDir2": {
                            DIR: {},
                            FILES: [
                                "subSubDir2.jpg",
                                "subSubDir2.pdf",
                                "subSubDir2.doc",
                                "subSubDir2-image.jpg",
                                "subSubDir2-project.doc",
                            ],
                        }
                    },
                    FILES: [
                        "subDir2.jpg",
                        "subDir2.pdf",
                        "subDir2.doc",
                        "subDir2-image.jpg",
                        "subDir2-project.doc",
                    ],
                },
            },
            FILES: [
                "dir.jpg",
                "dir.pdf",
                "dir.doc",
                "dir-image.jpg",
                "dir-project.doc",
            ],
        }
    },
    FILES: [],
}

# Categorized and sorted file structure with relative source path of the files.
CATEGORIZED_DIR_DICTIONARY = {
    "photo_by_name": {FILES: ["./dir-image.jpg"], DIR: {}},
    "project_by_name": {FILES: ["./dir-project.doc"], DIR: {}},
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
            "photo_by_name": {FILES: ["subDir1/subDir1-image.jpg"], DIR: {}},
            "project_by_name": {FILES: ["subDir1/subDir1-project.doc"], DIR: {}},
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
                    "photo_by_name": {
                        FILES: ["subDir1/subSubDir1/subSubDir1-image.jpg"],
                        DIR: {},
                    },
                    "project_by_name": {
                        FILES: ["subDir1/subSubDir1/subSubDir1-project.doc"],
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
            "photo_by_name": {
                FILES: ["subDir2/subDir2-image.jpg"],
                DIR: {},
            },
            "project_by_name": {
                FILES: ["subDir2/subDir2-project.doc"],
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
                    "photo_by_name": {
                        FILES: ["subDir2/subSubDir2/subSubDir2-image.jpg"],
                        DIR: {},
                    },
                    "project_by_name": {
                        FILES: ["subDir2/subSubDir2/subSubDir2-project.doc"],
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
                        "subDir2/subSubDir2/subSubDir2.jpg",
                        "subDir2/subSubDir2/subSubDir2.pdf",
                        "subDir2/subSubDir2/subSubDir2-image.jpg",
                        "subDir2/subSubDir2/subSubDir2-project.doc",
                        "subDir2/subSubDir2/subSubDir2.doc",
                    ],
                }
            },
            FILES: [
                "subDir2/subDir2-image.jpg",
                "subDir2/subDir2-project.doc",
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
                        "subDir1/subSubDir1/subSubDir1-image.jpg",
                        "subDir1/subSubDir1/subSubDir1-project.doc",
                        "subDir1/subSubDir1/subSubDir1.doc",
                        "subDir1/subSubDir1/subSubDir1.jpg",
                        "subDir1/subSubDir1/subSubDir1.pdf",
                    ],
                }
            },
            FILES: [
                "subDir1/subDir1-image.jpg",
                "subDir1/subDir1-project.doc",
                "subDir1/subDir1.doc",
                "subDir1/subDir1.jpg",
                "subDir1/subDir1.pdf",
            ],
        },
    },
    FILES: [
        "./dir-image.jpg",
        "./dir-project.doc",
        "./dir.doc",
        "./dir.jpg",
        "./dir.pdf",
    ],
}
