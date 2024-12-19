""" File Manager module which handles all product related file handling"""

import os
import shutil
import json
import logging

from organize_it.settings import FILES, DIR

LOGGER = logging.getLogger(__name__)


class FileManager:
    """
    A class to handle complex file operations such as traversal, generating directory tree. etc

    Methods:
        file_walk(self, root_dir: str) -> dict
        def generate_tree_structure(self, tree_dict, indent, generated_tree_file)
    """

    def __init__(self, source_path):
        """Constructor"""
        self.source_path = source_path

    def file_walk(self, root_dir: str, file_path=None) -> dict:
        """
        Recursively lists all files and directories starting from the given root directory,
        and returns the result in a nested oIt dictionary format.

        Args:
            root_dir (str): The root directory from which to start the search.
            file_path (str): File path to save the resultant dict, preferably as json.

        Returns:
            dict: A dictionary containing files and subdirectories in the format:
                {
                    'files': [list_of_files],
                    'dir': {
                        'subdir_name': {
                            'files': [list_of_files_in_subdir],
                            'dir': {
                                ...
                            }
                        }
                    }
                }
        Raises:
            FileNotFoundError: If the root_dir does not exist.
            NotADirectoryError: If the provided root_dir is not a directory.
        """
        if not os.path.isdir(root_dir):
            raise NotADirectoryError(
                f"The provided path {root_dir} is not a valid directory."
            )

        file_dict = {FILES: [], DIR: {}}

        # Traverse the root directory using os.walk to get directories and files
        for dirpath, _, filenames in os.walk(root_dir):
            # Skip directories above the current directory level
            rel_dir = os.path.relpath(
                dirpath, self.source_path
            )  # relative to source_dir
            if dirpath == root_dir:
                # Add files directly in the root directory
                file_dict[FILES] = sorted([os.path.join(rel_dir, f) for f in filenames])

            else:
                # For subdirectories, add their content recursively
                # TODO: if there are not sub dir, we don't need to return empty object. Fix tests later
                if len(dirpath.split("/")) - 1 == len(root_dir.split("/")):
                    subdir_name = os.path.basename(dirpath)
                    if subdir_name not in file_dict[DIR]:
                        file_dict[DIR][subdir_name] = {
                            FILES: sorted(
                                [os.path.join(rel_dir, f) for f in filenames]
                            ),
                            DIR: self.file_walk(dirpath)[
                                DIR
                            ],  # Recursive call for subdirectories
                        }
        if file_path:
            LOGGER.info(
                " - Saving unsorted file structure to %s", os.path.basename(file_path)
            )
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(file_dict, f, ensure_ascii=False)

        return file_dict

    def categorize_and_sort_file(
        self, config, sorted_tree_dict, destination_directory, source_directory
    ):
        """Perform file operations based on the sorted_tree_dict"""
        LOGGER.info(
            " - Performing File operation based on the organised tree structure."
        )
        # Iterate through the sorted dict top-down and do the cp command.
        formats_in_config = list(config["format"].keys())

        def perform(current_dir_contents):
            current_level_directories = current_dir_contents.keys()
            for dir_name in current_level_directories:
                for file_to_be_copied in current_dir_contents[dir_name][FILES]:
                    # Get the relative path from the source file path
                    rel_path = os.path.dirname(file_to_be_copied)
                    dest_subdir_path = os.path.join(
                        destination_directory, rel_path, dir_name
                    )
                    os.makedirs(dest_subdir_path, exist_ok=True)

                    cleaned_file_name = file_to_be_copied
                    if file_to_be_copied.startswith("./"):
                        cleaned_file_name = file_to_be_copied.replace(("."), "", 1)
                    source_file_path = f"{source_directory}/{cleaned_file_name}"
                    shutil.copy(source_file_path, dest_subdir_path)

                # Go into the directories that are not in the config and categorize them
                if dir_name not in formats_in_config:
                    perform(current_dir_contents[dir_name][DIR])

        perform(sorted_tree_dict)
        LOGGER.info(" - Successfully categorized and organized your files.")
