""" File Manager module which handles all product related file handling"""

import os
import shutil
import json
import logging

from organize_it.settings import FILES, DIR, SKIP

LOGGER = logging.getLogger(__name__)


class FileManager:
    """
    A class to handle complex file operations such as traversal, generating directory tree. etc

    Methods:
        file_walk(self, current_dir: str) -> dict
        def generate_tree_structure(self, tree_dict, indent, generated_tree_file)
    """

    def __init__(self, source_path, config):
        """Constructor"""
        self.source_path = source_path

        # TODO: Create cache of dirs names and file type to skip. Get it form the config.
        self.skip_dir_names = config[SKIP][DIR]
        self.skip_file_names = config[SKIP][FILES]

    def filter_excluded_names(self, name_list, is_dir):
        """
        Returns list of file/dir names after removing excluded ones.

        Args:
            name_list (list): list of
            is_dir (bool): If the string is question is a file or diretory name
        """

        return ""

    def file_walk(self, current_dir: str, file_path=None) -> dict:
        """
        Recursively lists all files and directories starting from the given root directory,
        and returns the result in a nested oIt dictionary format.

        Args:
            current_dir (str): The root directory from which to start the search.
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
            FileNotFoundError: If the current_dir does not exist.
            NotADirectoryError: If the provided current_dir is not a directory.
        """
        if not os.path.isdir(current_dir):
            raise NotADirectoryError(
                f"The provided path {current_dir} is not a valid directory."
            )

        file_dict = {FILES: [], DIR: {}}

        # Traverse the root directory using os.walk to get directories and files
        for dirpath, _, filenames in os.walk(current_dir):
            # Skip directories above the current directory level
            rel_dir = os.path.relpath(
                dirpath, self.source_path
            )  # relative to source_dir
            if dirpath == current_dir:
                # Add files directly in the root directory
                file_dict[FILES] = sorted([os.path.join(rel_dir, f) for f in filenames])

            else:
                # For subdirectories, add their content recursively
                # TODO: if there are not sub dir, we don't need to return empty object. Fix tests later
                if len(dirpath.split("/")) - 1 == len(current_dir.split("/")):
                    subdir_name = os.path.basename(dirpath)
                    if subdir_name not in file_dict[DIR]:
                        file_dict[DIR][subdir_name] = {
                            FILES: sorted(
                                [os.path.join(rel_dir, f) for f in filenames]
                            ),
                            # Recursive call for subdirectories
                            DIR: self.file_walk(dirpath)[DIR],
                        }
        if file_path:
            LOGGER.info(
                " - Saving unsorted file structure to %s", os.path.basename(file_path)
            )
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(file_dict, f, ensure_ascii=False)

        return file_dict

    def categorize_and_sort_file(
        self,
        config: dict,
        sorted_tree_dict: dict,
        destination_directory: dict,
        source_directory: str,
        move_files: bool = False,
    ):
        """
        Categorizes and sorts files from the source directory into the destination directory according to predefined rules.

        This method will:
        1. Load the categorization rules from the provided configuration (`config`).
        2. Use the sorted tree dictionary (`sorted_tree_dict`) to organize files into categories.
        3. Create the destination directory if it doesn't exist, ensuring a tidy home for the files.
        4. Optionally move files instead of copying them based on the `move_files` flag.
        5. Handle any errors in file operations, such as missing directories or permission issues.

        Args:
            config (dict): A dictionary containing categorization rules and configurations. The structure of this dictionary
                        is expected to define how files should be categorized, renamed, or organized.
                        For example, it could contain file extensions or patterns to group by file type.
            sorted_tree_dict (dict): A dictionary representing the structure of the files to be categorized. It maps files or
                                    directories to their respective categories.
            destination_directory (dict): A dictionary containing the absolute path or structure of the destination directory
                                        where the sorted files will be placed. It can include subdirectories or any other
                                        required directory structure for organizing the files.
            source_directory (str): The absolute or relative path to the source directory that contains the files to be
                                    categorized and sorted.
            move_files (bool): A flag indicating whether the files should be moved (True) or copied (False) to the destination
                            directory. Default is False (copy).
        """
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
                    if move_files:
                        shutil.move(source_file_path, dest_subdir_path)
                    else:
                        shutil.copy(source_file_path, dest_subdir_path)

                # Go into the directories that are not in the config and categorize them
                if dir_name not in formats_in_config:
                    perform(current_dir_contents[dir_name][DIR])

        perform(sorted_tree_dict)
        LOGGER.info(" - Successfully categorized and organized your files.")
