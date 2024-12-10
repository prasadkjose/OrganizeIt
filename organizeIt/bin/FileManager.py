from pathlib import Path
import os

FILES = 'files'
DIR = 'dir'
class FileManager:
   
    def file_walk(self, root_dir: str) -> dict:
        """
        Recursively lists all files and directories starting from the given root directory,
        and returns the result in a nested dictionary format.

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
            raise NotADirectoryError(f"The provided path {root_dir} is not a valid directory.")
        
        file_dict = {
            FILES: [],
            DIR: {}
        }

        # Traverse the root directory using os.walk to get directories and files
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip directories above the current directory level
            if dirpath == root_dir:
                # Add files directly in the root directory
                file_dict[FILES] = sorted(filenames) # keep them sorted
                
            else:
                # For subdirectories, add their content recursively
                # TODO: if there are not sub dir, we don't need to return empty object. Fix tests later 
                if len(dirpath.split('/')) - 1 == len(root_dir.split('/')):
                    subdir_name = os.path.basename(dirpath)
                    if subdir_name not in file_dict[DIR]:
                        file_dict[DIR][subdir_name] = {
                            FILES: sorted(filenames),
                            DIR: self.file_walk(dirpath)[DIR]  # Recursive call for subdirectories
                        }

        return file_dict
    
    def generate_tree_structure(self, tree_dict, indent, generated_tree_file):
        indent += "│   "
        # if file list files
        for file in tree_dict[FILES]:
            generated_tree_file.write(f"\n{indent}├── {file}")

        for dir in tree_dict[DIR]:
            generated_tree_file.write(f"\n{indent}├── {dir}/")
            self.generate_tree_structure(tree_dict[DIR][dir], indent + "    ", generated_tree_file)


        

