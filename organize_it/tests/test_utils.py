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
            with open(file_path, "w", encoding="utf-8") as _:
                pass  # Just create an empty file

    # Recursively create subdirectories and files
    if DIR in structure:
        for dir_name, subdir_structure in structure[DIR].items():
            # Create the subdirectory
            subdir_path = os.path.join(base_path, dir_name)
            os.makedirs(subdir_path, exist_ok=True)

            # Recursively call the function to create files and subdirectories in the subdir
            generate_samples_with_config(subdir_path, subdir_structure)


def dicts_are_equal(dict1: dict, dict2: dict) -> bool:
    """
    Compares two dictionaries to check if they have the same structure and identical elements.
    The order of keys is not considered in the comparison.

    Args:
        dict1 (dict): The first dictionary to compare.
        dict2 (dict): The second dictionary to compare.

    Returns:
        bool: True if both dictionaries have the same structure and elements, False otherwise.
    """
    if dict1 == dict2:
        return True

    # Check if both dicts have the same keys
    if dict1.keys() != dict2.keys():
        return False

    # Recursively compare values for each key
    for key in dict1:
        value1 = dict1[key]
        value2 = dict2[key]

        # If both values are dictionaries, perform a recursive comparison
        if isinstance(value1, dict) and isinstance(value2, dict):
            if not dicts_are_equal(value1, value2):
                return False
        # If list, then just compare values
        elif isinstance(value1, list) and isinstance(value2, list):
            return sorted(value1) == sorted(value2)
        elif value1 != value2:
            return False

    return True
