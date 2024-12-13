""" File Manager module which handles all product related file handling"""

import logging
from organize_it.settings import FILES, DIR

LOGGER = logging.getLogger(__name__)


class TreeStructure:
    """
    A class to handle tree operations and representations such as traversal, generating directory tree. etc

    Methods:
        def generate_tree_structure(self, tree_dict, indent, generated_tree_file)
        yaml_config_to_dict(self, config_dict)
    """

    def generate_tree_structure(self, tree_dict, indent, generated_tree_file):
        """
        Recursively generates a textual tree structure representation of files and directories
        and writes it to a specified file.

        This method traverses a nested dictionary representing the structure of directories
        and files. For each directory, it prints the directory name followed by a list of
        files and subdirectories in a tree-like format, which is then written to the
        `generated_tree_file`.

        Args:
            tree_dict (dict): A nested dictionary representing the directory structure.
                            It should have two main keys: 'FILES' and 'DIR'. 'FILES' maps
                            to a list of file names, and 'DIR' maps to another dictionary
                            of subdirectories with their corresponding structure.
            indent (str): A string representing the current indentation level. This is used
                        to format the tree structure with appropriate spacing.
            generated_tree_file (file-like object): A writable file object where the tree structure
                                                    will be written. This could be a file opened
                                                    in write or append mode.

        Example:
            tree_dict = {
                'FILES': ['file1.txt', 'file2.txt'],
                'DIR': {
                    'subdir1': {
                        'FILES': ['file3.txt'],
                        'DIR': {}
                    },
                    'subdir2': {
                        'FILES': [],
                        'DIR': {}
                    }
                }
            }
        """
        indent += "│   "
        # if file list files
        if FILES in tree_dict:
            for file in tree_dict[FILES]:
                generated_tree_file.write(f"\n{indent}├── {file}")

        if DIR in tree_dict:
            for directory in tree_dict[DIR]:
                generated_tree_file.write(f"\n{indent}├── {directory}/")
                self.generate_tree_structure(
                    tree_dict[DIR][directory], indent + "    ", generated_tree_file
                )

    def yaml_config_to_dict(self, config_dict: dict) -> dict:
        """
        Takes in the config dictionary and converts it to oIt tree input dictionary.

        Args:
            config_dict (str): The parsed config file.

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
        """
        LOGGER.info(
            "Generating clean and organised tree structure based on the provided config."
        )

        def recursive(config_dict):
            # Loop through the formats in the config and create subdirs in the tree.
            if "format" in config_dict:
                formated_directories = list(config_dict["format"].keys())
                generated_dict = {}
                for directory_name in formated_directories:
                    generated_dict[directory_name] = recursive(
                        config_dict["format"][directory_name]
                    )

                return {DIR: generated_dict}
            else:
                return {}

        return recursive(config_dict)

    def create_tree_from_config(self, config: dict) -> dict:
        """
        Creates a directory tree structure from the given YAML config.
        Makes sure the config is validated before creating a tree.

        Args:
            dict: config dictonary to build tree from
            bool: save_to_file If true, saves the generated tree to a file

        Returns:
            dict: directory tree structure

        Raises:
            ValidationError: If the YAML data does not conform to the validation rules.
        """
