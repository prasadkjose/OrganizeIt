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
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The main functionality of **OrganizeIt** can be accessed via the command line. Here’s how you can use the tool:

### 1. Organize Files

To organize files in a directory, run:

```bash
python organizeit.py --path /path/to/your/directory
```

- `--path`: The directory whose files you want to organize.

This command will scan the specified directory, organize the files by their types into appropriate subdirectories (such as `Images`, `Documents`, `Videos`, etc.), and move the files accordingly.

### 2. Organize Files with a Custom Directory Structure

You can customize the file organization by defining your own rules for categories. Modify the `config.json` file to suit your needs.

### 3. Generate a File Tree

You can generate a tree structure representation of your organized directory:

```bash
python organizeit.py --path /path/to/your/directory --generate-tree /path/to/output/file.txt
```

This will generate a textual tree of your file structure and write it to the specified file (`file.txt`).

### 4. Dry-Run Mode

If you want to see how **OrganizeIt** would organize the files without actually moving them, use the `--dry-run` flag:

```bash
python organizeit.py --path /path/to/your/directory --dry-run
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
└── utils/                  # Utility functions for file operations
    ├── file_manager.py     # Handles file manipulation (move, rename, etc.)
    ├── tree_structure.py   # Generates and manages tree structure representation
    └── categorizer.py      # Handles categorization logic based on file extensions
```

### Key Files:
- `organizeit.py`: The main script that handles the file organization process. This file is where you interact with the tool.
- `config.json`: A JSON file where you define your own custom file categories and their corresponding extensions.
- `file_manager.py`: Contains utility functions to perform file operations such as moving, renaming, and creating directories.
- `tree_structure.py`: Used for generating a tree-like representation of your organized file structure.
- `categorizer.py`: Handles the logic to categorize files based on extensions or custom rules.

## Contributing

We welcome contributions to **OrganizeIt**! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests if applicable.
4. Submit a pull request with a clear description of your changes.

### Issues

If you find any bugs or have suggestions for improvements, feel free to [open an issue](https://github.com/prasadkjose/OrganizeIt/issues). We’re happy to review and address any problems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using **OrganizeIt**! We hope it helps you keep your files organized and your workspace clutter-free.
