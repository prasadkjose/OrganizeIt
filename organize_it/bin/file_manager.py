""" File Manager module which handles all product related file handling"""

import os
import shutil
import json
import logging

from organize_it.settings import FILES, DIR

LOGGER = logging.getLogger(__name__)


def sanitize_file_path(path: str) -> str:
    """
    Sanitizes a file or directory path by:
    - Removing trailing slashes or backslashes
    - Normalizing path separators to the OS default

    Args:
        path (str): The file or directory path to sanitize.

    Returns:
        str: The sanitized path.
    """
    # Remove trailing slashes or backslashes
    sanitized_path = path.rstrip(os.sep)

    # Normalize path (to use OS-specific separator)
    sanitized_path = os.path.normpath(sanitized_path)

    return sanitized_path


class FileManager:
    """
    A class to handle complex file operations such as traversal, generating directory tree. etc

    Methods:
        file_walk(self, current_dir: str) -> dict
        def generate_tree_structure(self, tree_dict, indent, generated_tree_file)
    """

    def __init__(self, source_path: str, destination_path: str = None):
        """Constructor"""
        self.source_path = sanitize_file_path(source_path)
        self.destination_path = sanitize_file_path(destination_path)

    def file_walk(self, current_dir: str = None, file_path: str = None) -> dict:
        """
        Recursively lists all files and directories starting from the given root directory,
        and returns the result in a nested oIt dictionary format.

        Args:
            current_dir (str): The current directory from which to perform the search.
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
        # Take root source directory from the class member.
        if current_dir is None:
            current_dir = self.source_path

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
            LOGGER.info(" - Saving file structure to %s", os.path.basename(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(file_dict, f, ensure_ascii=False)

        return file_dict

    def categorize_and_sort_file(
        self,
        config: dict,
        sorted_tree_dict: dict,
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
                        self.destination_path, rel_path, dir_name
                    )
                    os.makedirs(dest_subdir_path, exist_ok=True)

                    cleaned_file_name = file_to_be_copied
                    if file_to_be_copied.startswith("./"):
                        cleaned_file_name = file_to_be_copied.replace(("."), "", 1)
                    source_file_path = f"{self.source_path}/{cleaned_file_name}"
                    if move_files:
                        shutil.move(source_file_path, dest_subdir_path)
                    else:
                        shutil.copy(source_file_path, dest_subdir_path)

                # Go into the directories that are not in the config and categorize them
                if dir_name not in formats_in_config:
                    perform(current_dir_contents[dir_name][DIR])

        perform(sorted_tree_dict)
        LOGGER.info(" - Successfully categorized and organized your files.")

    @staticmethod
    def create_and_write_file(file_path: str, callback):
        """
        Creates a file at the specified file_path, ensuring that the parent directory exists.
        Then, it writes content to the file by calling the provided callback function.

        Args:
            file_path (str): The path (including file name) where the file should be created.
            callback (function): A function that takes a file object as its argument and writes to the file.

        Raises:
            OSError: If there is an error creating the directory or opening the file.
            Exception: If the callback function raises an exception during execution.

        Example:
            def write_content(file):
                file.write("Hello, World!")

            create_and_write_file("/path/to/file.txt", write_content)
        """
        # Split the file path into parent directory and file name
        parent_path, file_name = os.path.split(file_path)

        # Ensure the parent directory exists
        os.makedirs(parent_path, exist_ok=True)

        # Open the file and invoke the callback function to write content
        try:
            with open(file_path, "w", encoding="utf-8") as generated_tree_file:
                callback(generated_tree_file)
        except Exception as e:
            # Optionally handle exceptions, e.g., logging
            raise Exception(f"Failed to write to file {file_path}: {e}")
