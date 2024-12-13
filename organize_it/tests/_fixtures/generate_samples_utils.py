""" This module generates all the necessary sample fixtures for spec tests. """

import os

from organize_it.bin.file_manager import FILES, DIR


def generate_samples_with_config(base_path: str, structure: dict):
    """
    Created sample files and directories as per the directory structure provided.
    """
    # Create files at the current level
    if FILES in structure:
        for file_name in structure[FILES]:
            file_path = os.path.join(base_path, file_name)
            # Create an empty file
            with open(file_path, "w") as f:
                pass  # Just create an empty file

    # Recursively create subdirectories and files
    if DIR in structure:
        for dir_name, subdir_structure in structure[DIR].items():
            # Create the subdirectory
            subdir_path = os.path.join(base_path, dir_name)
            os.makedirs(subdir_path, exist_ok=True)

            # Recursively call the function to create files and subdirectories in the subdir
            generate_samples_with_config(subdir_path, subdir_structure)
