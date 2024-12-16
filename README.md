# OrganizeIt

**OrganizeIt** is a Python-based utility to help users automate the organization of their file system. This tool scans a given directory, organizes files into subdirectories based on their file types, and provides a clean, structured way to manage file systems. Whether you're dealing with a messy Downloads folder or a cluttered workspace, **OrganizeIt** helps sort files quickly and easily.

## Features

- Automatically organizes files into categorized subdirectories (e.g., Images, Documents, Music, etc.).
- Supports custom categorization rules based on file extensions.
- Option to organize files into a hierarchical tree structure for easy navigation.
- Simple, easy-to-use command-line interface.
- Supports recursive file handling for organizing files in nested directories.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use **OrganizeIt**, follow these steps:

### 1. Clone the repository:

```bash
git clone https://github.com/prasadkjose/OrganizeIt.git
```

### 2. Navigate to the project directory:

```bash
cd OrganizeIt
```

### 3. (Optional) Create and activate a virtual environment:

It's recommended to use a virtual environment to avoid version conflicts:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 4. Install the required dependencies:

```bash
python3 setup.py install
```
## Testing

Testing is done using pytest. You can find the testing configurations and fixtures in conftest.py. 
#### 1. Run the entire suite. 
```bash
pytest
```
## Usage

### Command Line Interface

The main functionality of **OrganizeIt** can be accessed via the command line. Here’s how you can use the tool:

### 1. Organize Files

To organize files in a directory, run:

```bash
oIt --path /path/to/your/directory
```

- `--path`: The directory whose files you want to organize.

This command will scan the specified directory, organize the files by their types into appropriate subdirectories (such as `Images`, `Documents`, `Videos`, etc.), and move the files accordingly.

### 2. Organize Files with a Custom Directory Structure

You can customize the file organization by defining your own rules for categories. Modify the `config.json` file to suit your needs.

### 3. Dry-Run Mode

If you want to see how **OrganizeIt** would organize the files without actually moving them, use the `--dry-run` flag:

```bash
oIt --dry-run
```

This will display a preview of the changes but will not modify any files.

## Project Structure

Here's an overview of the **OrganizeIt** project structure:

```
OrganizeIt/
├── organizeit.py           # Main file for organizing the files
├── config.json             # Configuration file for file categories
├── requirements.txt        # List of required dependencies
├── README.md               # Project documentation
└── bin/                    # Utility functions for file operations
    ├── file_manager.py     # Handles file manipulation (move, rename, etc.)
    ├── tree_structure.py   # Generates and manages tree structure representation
    └── categorizer.py      # Handles categorization logic based on file extensions
└── configs/                # Utility functions for file operations
    ├── config-schema.json  # A JSON-SCHEMA file to validate the custom config.yaml
    ├── config.yaml         # A factory YAML file where you can define your own custom file categories and their corresponding extensions.
└── schema_validation/      # Schema validation 
    ├── validator.py        # Validate the config file with rules set in config-schema.json
```

## Contributing

I welcome contributions to **OrganizeIt**! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests if applicable. Also make sure none of the exisiting tests fail. 
4. Submit a pull request with a clear description of your changes.

### Issues

If you find any bugs or have suggestions for improvements, feel free to [open an issue](https://github.com/prasadkjose/OrganizeIt/issues). We’re happy to review and address any problems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using **OrganizeIt**! I hope it helps you keep your files organized and your workspace clutter-free.
