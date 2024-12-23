""" Categorizer Module"""

import logging
import re

from organize_it.settings import FILES, DIR, SKIP

LOGGER = logging.getLogger(__name__)


class Categorizer:
    """Categorizer class that handles categorization logic based on file extensions"""

    def __init__(self, config):
        # create a cache of types mapped to format to quickly access them later.
        self.types_to_format_dict = {}
        if "format" in config:
            for cat, types in config["format"].items():
                format_types = types["types"]
                for format_type in format_types:
                    self.types_to_format_dict[format_type] = cat

        # Regex of dirs and file names to skip.
        if SKIP in config:
            skip_dict = config[SKIP]
            self.skip_dir_regex = skip_dict.get(DIR)
            self.skip_file_regex = skip_dict.get(FILES)

    def filter_excluded_names(self, name_list, is_dir) -> list:
        """
        Returns list of file/dir names after removing excluded ones based on the regex matcher provided in the config.

        Args:
            name_list (list): list of fie/dir names to be processed
            is_dir (bool): If the string is question is a file or diretory name
        """
        if hasattr(self, "skip_dir_regex") or hasattr(self, "skip_file_regex"):
            skip_regex = self.skip_dir_regex if is_dir else self.skip_file_regex
            return (
                [name for name in name_list if not re.search(skip_regex, name)]
                if skip_regex
                else name_list
            )
        else:
            return name_list

    def categorize_dict(self, source_tree_dict: dict, recursive: bool) -> dict:
        """
        Method that categorizes files based on input using the provided config and returns the categorized dictionary
        Args:
            source_tree_dict (dict): The unsorted source tree structure dictionary
            recursive (bool): Optional flag to recurce into all sub directories and categorize them based on the config
        Returns:
            dict: A sorted and categorized dictionary containing files and subdirectories in the format:
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
        """
        LOGGER.info(
            " - Generating clean and organised tree structure based on the provided config."
        )

        def categorize(input_dict) -> dict:
            """Takes in the config and categorizes based on the config"""
            sorted_dict = {DIR: {}, FILES: []}
            current_level_files = self.filter_excluded_names(input_dict[FILES], False)
            for file_name in current_level_files:
                # Check if last substring with . is in the cache and add the format as dir_name to the dict
                current_file_format = file_name.rsplit(".", 1)[1]
                if current_file_format in self.types_to_format_dict:
                    current_dir_format_name = self.types_to_format_dict[
                        current_file_format
                    ]
                    if current_dir_format_name in sorted_dict[DIR]:
                        sorted_dict[DIR][current_dir_format_name][FILES].append(
                            file_name
                        )
                    else:
                        sorted_dict[DIR][current_dir_format_name] = {
                            DIR: {},
                            FILES: [file_name],
                        }

            if recursive:
                # Go into each sub dir of source_tree_dict and categorize recursively.
                current_level_subdir = input_dict[DIR]
                current_level_subdir_names = self.filter_excluded_names(
                    current_level_subdir.keys(), True
                )
                for dir_name in current_level_subdir_names:
                    # Check if we have files to categorize at this level
                    if len(current_level_subdir[dir_name][FILES]):
                        sorted_dict[DIR][dir_name] = categorize(
                            current_level_subdir[dir_name]
                        )

            return sorted_dict

        return categorize(source_tree_dict)
