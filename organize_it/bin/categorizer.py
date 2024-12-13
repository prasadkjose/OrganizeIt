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
            "Generating clean and organised tree structure based on the provided config."
        )

        # def recursive(config_dict):
        #     # Loop through the formats in the config and create subdirs in the tree.
        #     if "format" in config_dict:
        #         formated_directories = list(config_dict["format"].keys())
        #         generated_dict = {}
        #         for directory_name in formated_directories:
        #             generated_dict[directory_name] = recursive(
        #                 config_dict["format"][directory_name]
        #             )

        #         return {DIR: generated_dict}
        #     else:
        #         return {}

        # return recursive(source_tree_dict)

        def categorize(config__dict, input_dict) -> dict:
            """Takes in the config and categorizes based on the config"""
            types_to_format_dict = {}
            sorted_dict = {DIR: {}, FILES: []}
            # create a cache of types mapped to format to quickly access them later.
            for cat, types in config__dict["format"].items():
                format_types = types["types"]
                for format_type in format_types:
                    types_to_format_dict[format_type] = cat

            files = input_dict[FILES]
            for file_name in files:
                # Check if last substring with . is in the cache and add the format as dir_name to the dict
                current_file_format = file_name.rsplit(".", 1)[1]
                if current_file_format in types_to_format_dict:
                    if current_file_format in sorted_dict[DIR]:
                        sorted_dict[DIR][types_to_format_dict[current_file_format]][
                            FILES
                        ].concat(file_name)
                    else:
                        sorted_dict[DIR][types_to_format_dict[current_file_format]] = {
                            DIR: {},
                            FILES: [file_name],
                        }
            return sorted_dict

        return categorize(config, source_tree_dict)
