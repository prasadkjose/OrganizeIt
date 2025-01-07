""" Common reusable subroutines """

import logging
import json
import os

from organize_it.settings import (
    CONFIG,
    GENERATED_SOURCE_TREE,
    GENERATED_SOURCE_JSON,
    get_or_update_current_state,
)

from organize_it.bin.file_manager import FileManager
from organize_it.bin.tree_structure import TreeStructure
from organize_it.bin.categorizer import Categorizer
from organize_it.ai.gpt_wrapper import GPTWrapper

logger = logging.getLogger(__name__)


def generate_with_ai(
    generated_source_tree_path: str = GENERATED_SOURCE_TREE,
):
    wrapper = GPTWrapper()
    with open(os.path.join(generated_source_tree_path), "r", encoding="utf-8") as f:
        tree = f.read()
    # Load the config from the user input
    logger.info(" - Generating config with AI... Please be patient")
    return wrapper.generate_config(unsorted_tree=tree)


def process_source_and_generate_tree(
    source_directory: str, destination_directory: str, generated_source_tree_path: str
):
    """
    Processes a source directory path, generates a hierarchical tree structure of files,
    and generates a trees structure. If the tree structure has already been
    generated previously, it skips the generation process.

    Parameters:
        source_directory (str): The absolute or relative path to the source directory
                                 containing files to be processed.
        destination_directory (str): The absolute or relative path to the source directory
                                 containing files to be processed.
        generated_source_tree_path (str): The path where the generated file tree structure
                                      will be saved.

    Returns:
        tuple: A tuple containing:
            - file_manager (FileManager): An instance of the FileManager class for handling
              file operations in the source and destination directories.
            - tree_structure (TreeStructure): An instance of the TreeStructure class that
              represents the generated file tree.
            - source_tree_dict (dict): A dictionary representation of the file structure in
              the source directory, generated by walking through the source directory recursively.

    Notes:
        - The method may skip tree generation if the tree structure has been previously
          generated, depending on the existence of a specific file or hash check (as indicated
          by the TODO section).

    Example:
        source_dir = "/path/to/source"
        destination_dir = "/path/to/destination"
        file_manager, tree_structure, source_tree_dict = process_source_and_generate_tree(source_dir, destination_dir)
    """

    file_manager = FileManager(source_directory, destination_directory)
    tree_structure = TreeStructure()

    # If cli is in interactive mode, then source tree will be will be generated already.
    # So skip this part IF the generated json file exists for a specific run.
    # Could be a hash of the source path or some other parameter like a simple counter interator.
    # Current Structure
    if not get_or_update_current_state():
        get_or_update_current_state(True)

        # Read the source directory and create oIt tree input dictionary and save it to a file
        source_tree_dict = file_manager.file_walk(file_path=GENERATED_SOURCE_JSON)

        # write the source tree structure result to a file
        FileManager.create_and_write_file(
            file_path=generated_source_tree_path,
            callback=lambda file_stream: tree_structure.generate_tree_structure(
                source_tree_dict, "", file_stream
            ),
        )
        return file_manager, tree_structure, source_tree_dict

    with open(os.path.join(GENERATED_SOURCE_JSON), "r", encoding="utf-8") as f:
        source_tree_dict = json.loads(f.read())
    return file_manager, tree_structure, source_tree_dict


def categorize_and_generate_dest_tree(
    source_tree_dict: dict,
    tree_structure: TreeStructure,
    dest_tree_path: str,
    config: dict,
):
    """
    Categorizes files and directories paths from the source tree dictionary based on a
    given configuration, and then generates and writes the categorized tree structure
    to the destination directory.

    Parameters:
        config (dict): The config dict.
        source_tree_dict (dict): A dictionary representing the hierarchical structure
                                  of files in the source directory, typically generated
                                  from a previous file walk.
        tree_structure (TreeStructure): An instance of the TreeStructure class used
                                         to generate and write the categorized tree structure
                                         to the destination directory.

    Returns:
        dict: A dictionary representing the categorized file tree, where files and
              directories are organized according to the given configuration.

    Example:
        categorized_tree_dict = categorize_and_generate_dest_tree(config, source_tree_dict, tree_structure, dest_tree_path)
    """

    if config is None:
        config = CONFIG

    # Categorize the files and dirs based on the given config
    categorizer = Categorizer(config)
    categorized_tree_dict = categorizer.categorize_dict(source_tree_dict, True)

    FileManager.create_and_write_file(
        file_path=dest_tree_path,
        callback=lambda file_stream: tree_structure.generate_tree_structure(
            categorized_tree_dict, "", file_stream
        ),
    )

    return categorized_tree_dict
