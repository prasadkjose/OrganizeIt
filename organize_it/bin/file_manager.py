""" File Manager module which handles all product related file handling"""

import os
from organize_it.settings import FILES, DIR


class FileManager:
    """
    A class to handle complex file operations such as traversal, generating directory tree. etc

    Methods:
        file_walk(self, root_dir: str) -> dict
        def generate_tree_structure(self, tree_dict, indent, generated_tree_file)
    """

    def file_walk(self, root_dir: str) -> dict:
        """
        Recursively lists all files and directories starting from the given root directory,
        and returns the result in a nested oIt dictionary format.

        Args:
            root_dir (str): The root directory from which to start the search.

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
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip directories above the current directory level
            if dirpath == root_dir:
                # Add files directly in the root directory
                file_dict[FILES] = sorted(filenames)  # keep them sorted

            else:
                # For subdirectories, add their content recursively
                # TODO: if there are not sub dir, we don't need to return empty object. Fix tests later
                if len(dirpath.split("/")) - 1 == len(root_dir.split("/")):
                    subdir_name = os.path.basename(dirpath)
                    if subdir_name not in file_dict[DIR]:
                        file_dict[DIR][subdir_name] = {
                            FILES: sorted(filenames),
                            DIR: self.file_walk(dirpath)[
                                DIR
                            ],  # Recursive call for subdirectories
                        }

        return file_dict

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
        for file in tree_dict[FILES]:
            generated_tree_file.write(f"\n{indent}├── {file}")

        for directory in tree_dict[DIR]:
            generated_tree_file.write(f"\n{indent}├── {directory}/")
            self.generate_tree_structure(
                tree_dict[DIR][directory], indent + "    ", generated_tree_file
            )
