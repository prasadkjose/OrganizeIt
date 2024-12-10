import os
from organizeIt.settings import TEST_FIXTURES_DIR
from organizeIt.bin.FileManager import FILES, DIR

def create_structure(base_path, structure):
    # Create files at the current level
    if FILES in structure:
        for file_name in structure[FILES]:
            file_path = os.path.join(base_path, file_name)
            # Create an empty file
            with open(file_path, 'w') as f:
                pass  # Just create an empty file

    # Recursively create subdirectories and files
    if DIR in structure:
        for dir_name, subdir_structure in structure[DIR].items():
            # Create the subdirectory
            subdir_path = os.path.join(base_path, dir_name)
            os.makedirs(subdir_path, exist_ok=True)
            
            # Recursively call the function to create files and subdirectories in the subdir
            create_structure(subdir_path, subdir_structure)

def generate_samples_with_config(directory_structure):
    # Create the directory structure
    create_structure(TEST_FIXTURES_DIR, directory_structure)
    print(f"Directory structure created at {TEST_FIXTURES_DIR}")