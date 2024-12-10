import os
from organizeIt.settings import TEST_FIXTURES_DIR

def create_structure(base_dir, structure):
    """
    Recursively creates directories and files based on the given structure.

    Args:
        base_dir (str): The base directory where the structure will be created.
        structure (dict): The structure to create, where:
                          - keys are directory names or file names
                          - values are either a dictionary of subdirectories/files or empty strings for files.
    """
    for name, content in structure.items():
        # Create the full path for the directory/file
        full_path = os.path.join(base_dir, name)
        
        if isinstance(content, dict):  # This is a subdirectory
            # Create the directory
            os.makedirs(full_path, exist_ok=True)
            # Recurse to create subdirectories and files inside this directory
            create_structure(full_path, content)
        else:  # This is a file
            # Create the file with empty content (or content as given)
            with open(full_path, 'w') as f:
                f.write(content)

def generate_samples_with_config():
    # The base directory where the structure should be created
    base_directory = TEST_FIXTURES_DIR # Replace with your desired base directory

    # The structure to create
    directory_structure = {
        'generatedFiles': {
            'a': {
                'a.py': '',
            },
            'b': {
                'b.py': '',
            },
            'c': {
                'c': {
                    'd.yaml': '',
                    'e.yaml': '',
                    'c': {
                        'c.py': '',
                    },
                }
            },
            'd': {
                'ab.json5': '',
                'ab.yaml': '',
            },
        }
    }

    # Create the directory structure
    create_structure(base_directory, directory_structure)
    print(f"Directory structure created at {base_directory}")