""" Interactive CLI module for the project """

import os
from organize_it.settings import (
    load_yaml,
    ROOT_DIR,
    exit_gracefully,
)

INPUT_SCRIPT_PATH = os.path.join(ROOT_DIR, "cli")

INPUT = "input"
PRINT = "print"
ARG = "arg"
RESPONSE = "response"


def help_me():
    print("you will find help here")


def view_tree():
    print("This is where the tree will be viewed")


def set_arg():
    print("CLI args will be set based on the response")


def proceed():
    print("Proceed next")


# TODO: backwards iteration https://stackoverflow.com/questions/55380989/is-there-any-way-to-go-back-a-step-in-a-python-for-loop


class InteractiveCLI:
    """Interactive CLI module to handle input from user"""

    def __init__(self):
        self.script_list = load_yaml(INPUT_SCRIPT_PATH)

    def start_interactive_prompts(self) -> dict:
        arg_dict = {}
        for prompt_item in self.script_list:
            if isinstance(prompt_item, str):
                #  if list item is string, then print it.
                print(prompt_item)
            elif isinstance(prompt_item, dict):
                input_dict = prompt_item[INPUT]
                if PRINT in input_dict:
                    # Prompt the user for input in the 'print'
                    user_response = input(input_dict[PRINT])
                    if ARG in input_dict:
                        # If it's an arg based prompt, then store the response in it
                        arg_dict[input_dict[ARG]] = user_response
                    elif RESPONSE in input_dict:
                        # If it's an response based prompt, then call the appropriate response method from the 'response' key of the input prompt
                        if user_response in input_dict[RESPONSE]:
                            response_method = input_dict[RESPONSE][user_response]
                            globals()[response_method]()  # can be global or local
                        else:
                            print("oops wrong input")
                            exit_gracefully()
                    else:
                        # Wrong prompt structure
                        exit_gracefully()
            else:
                # Wrong prompt structure
                exit_gracefully()
        return arg_dict
