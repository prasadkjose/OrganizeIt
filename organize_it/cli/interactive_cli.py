""" Interactive CLI module for the project """

import os
from organize_it.settings import load_yaml, ROOT_DIR, exit_gracefully

INPUT_SCRIPT_PATH = os.path.join(ROOT_DIR, "cli")


class InteractiveCLI:
    """Interactive CLI module to handle input from user"""

    def __init__(self):
        self.script_list = load_yaml(INPUT_SCRIPT_PATH)

    def start_interactive_prompts(self):
        for prompt_item in self.script_list:
            if isinstance(prompt_item, str):
                #  if list item is string, then print it.
                print(prompt_item)
            elif isinstance(prompt_item, dict):
                # if list item has key input, get 'print' to stdout and 'arg' as the argument to set in input_arg_parser.
                input_dict = prompt_item["input"]
                if "print" in input_dict:
                    input(input_dict["print"])

            else:
                exit_gracefully()
