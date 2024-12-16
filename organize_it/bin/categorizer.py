""" Categorizer Module"""

import logging
from organize_it.settings import FILES, DIR

LOGGER = logging.getLogger(__name__)


class Categorizer:
    """Categorizer class that handles categorization logic based on file extensions"""

    def categorize_dict(self, config, source_tree_dict, recursive) -> dict:
        """
        Method that categorizes files based on input using the provided config and returns the categorized dictionary
        Args:
            config_dict (str): The parsed config file.
            source_tree_dict (dict): The unsorted source tree structure dictionary
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

        # create a cache of types mapped to format to quickly access them later.
        types_to_format_dict = {}
        for cat, types in config["format"].items():
            format_types = types["types"]
            for format_type in format_types:
                types_to_format_dict[format_type] = cat

        def categorize(input_dict) -> dict:
            """Takes in the config and categorizes based on the config"""
            sorted_dict = {DIR: {}, FILES: []}
            current_level_files = input_dict[FILES]
            for file_name in current_level_files:
                # Check if last substring with . is in the cache and add the format as dir_name to the dict
                current_file_format = file_name.rsplit(".", 1)[1]
                if current_file_format in types_to_format_dict:
                    current_dir_format_name = types_to_format_dict[current_file_format]
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
                current_level_subdir_names = current_level_subdir.keys()
                for dir_name in current_level_subdir_names:
                    # Check if we have files to categorize at this level
                    if len(current_level_subdir[dir_name][FILES]):
                        sorted_dict[DIR][dir_name] = categorize(
                            current_level_subdir[dir_name]
                        )

            return sorted_dict

        return categorize(source_tree_dict)
