# OrganizeIt

**OrganizeIt** is a Python-based utility to help users automate the organization of their file system. This tool scans a given directory, organizes files into subdirectories based on their file types, and provides a clean, structured way to manage file systems. Whether you're dealing with a messy Downloads folder or a cluttered workspace, **OrganizeIt** helps sort files quickly and easily.

## Features

- Automatically organizes files into categorized subdirectories (e.g., Images, Documents, Music, etc.).
- Supports custom categorization rules based on file extensions and file name patterns.
- Option to organize files into a hierarchical tree structure for easy navigation.
- Simple, easy-to-use command-line interface.
- Supports recursive file handling for organizing files in nested directories.
- Supports regex-based exclusion of files and directories, ensuring that system or other location-sensitive files remain unaffected.
- AI integration with OpenAI and Gpt4All(in future updates) to organize your files so you don't have to worry about configs or file formats. 


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [AI Integration](#ai-integration)
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
#### 1. Run the entire suite without AI integration. 
```bash
pytest
```
#### 2. Run the entire suite with AI integration.
```bash
pytest --ai
```
#### 3. Run the entire suite and keep the generated test files and configs. 
```bash
pytest --keep
```
## Usage

### Command Line Interface

The main functionality of **OrganizeIt** can be accessed via the command line. Here’s how you can use the tool:

### 1. Organize Files

To organize files in a directory, run:

```bash
oIt --src /path/to/your/directory --dest /path/to/your/destination
```

- `--src`: The directory whose files you want to organize.
- `--dest`: The detination directory wwhere the organized files will be moved/copied to.
- By default, your files will be copied. To move your files into an organized structure, use the `--move` flag. Please note that this operation is permanent and cannot be undone.
- Run the tool in AI mode with `--ai` flag. 


This command will scan the specified source directory, organize the files by their types into appropriate subdirectories (such as `Images`, `Documents`, `Videos`, etc.), and move the files accordingly.

### 2. Organize Files with a Custom Directory Structure

You can customize the file organization by defining your own rules for categories. Modify the `configs/config.json` file to suit your needs.


### 3. Interactive Mode

Interactive mode allows you to guide the CLI tool through a step-by-step process, making it easier to configure settings, choose actions, and preview results before executing operations
If you want to see how **OrganizeIt** would organize the files without actually moving them, use the `-i` flag to run the tool in interactive mode and view the source and resultant trees:

```bash
oIt -i
```

This way, you can display a preview of the result but will not modify any files. You can at any time quit the tool and keep you file structure unaltered. 

If you tech savvy, you can find the generated dictionaries and tree structures in the `.tmp` directory in the project.

## AI Integration

This project incorporates AI capabilities using the OpenAI Python SDK to perform various tasks such as generating configurations.

**OpenAI Python SDK**
The OpenAI Python SDK is utilized to interact with OpenAI's language models like gpt-4. The SDK provides a seamless way to send requests and retrieve results from the OpenAI API.

**Adding Your OpenAI API Key**
To use the AI features, you must provide an OpenAI API key. There are two recommended ways to do this:

- ##### Environment Variable

    Add the API key to your system's environment variables.
    Example for a UNIX-based system:
    ``` bash
    export OPENAI_API_KEY="your_openai_api_key"
    ```

    On Windows (using Command Prompt):
    cmd 
    ```
    set OPENAI_API_KEY=your_openai_api_key
    ```
    The SDK will automatically pick up the OPENAI_API_KEY environment variable if it is set.

- ##### Constants File

    Alternatively, you can store the API key in a constants.py file in your project.
    Example constants.py:
    ``` bash
    OPENAI_API_KEY = "your_openai_api_key"
    ```


## Project Structure

Here's an overview of the **OrganizeIt** project structure:

```
organizeIt/
├── __main__.py             # Main entry point for the tool 
├── settings.py             # Common utility methods and constants used in the tool.
├── constants.py            # Add your API keys here. (for example, OPEN_API_KEY)
├── ai/                     # LLM wrapper implementations
    ├── ai_prompts.yaml     # Prompts used in the GPT. Both system and user role based prompts are defined here. 
    ├── gpt_wrapper.py      # Wrapper implementations for LLM model for OpenAI GPT and GPT4All(TODO).
├── bin/                    # Utility class implementations
    ├── file_manager.py     # Handles file manipulation (move, rename, etc.)
    ├── tree_structure.py   # Generates and manages tree structure representation   
    └── categorizer.py      # Handles categorization logic based on file extensions and name patterns.
├── cli/
    ├── input_arg_parser    # CLI arguments parser module.
    ├── interactive_cli     # Module for Interactice mode use inputs
    └── input_script.yaml   # YAML file that defines a list of use prompt flows for your CLI tool in interactive mode
├── configs/                # Utility functions for file operations
    ├── config_schema.json  # A JSON-Schema file to validate the custom config.yaml
    └── config.yaml         # A factory YAML file where you can define your own custom file categories and their corresponding extensions.
├── schema_validation/      # Schema validation 
    └── validator.py        # Validate the config file with rules set in config_schema.json
├── .tmp/                   # The .tmp directory stores temporary files that are short-lived and can be safely deleted when no longer needed.
└── tests/                  # Testing Module. It follows the same structure as the project itself. 
    ├── _fixtures_          # All necessary fixtures used in pytest
        └── .generated      # Generated files for testing. 
    └── conftest.py         # Configuration file used in pytest to define fixtures, hooks, and other settings that are shared across multiple test modules.
    
```

## Contributing

I welcome contributions to **OrganizeIt**! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. ```python3 setup.py develop``` to start developing.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests if applicable. Also make sure none of the exisiting tests fail. 
4. Submit a pull request with a clear description of your changes.

### Issues

If you find any bugs or have suggestions for improvements, feel free to [open an issue](https://github.com/prasadkjose/OrganizeIt/issues). I am happy to review and address any problems.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using **OrganizeIt**! I hope it helps you keep your files organized and your workspace clutter-free.
