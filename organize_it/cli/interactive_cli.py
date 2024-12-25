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

# The number of user attempts per input before exiting.
NUMBER_OF_ATTEMPTS = 5

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
                    for _ in range(NUMBER_OF_ATTEMPTS):
                        user_response = input(input_dict[PRINT])
                        if ARG in input_dict:
                            # If it's an arg based prompt, then store the response in it
                            arg_dict[input_dict[ARG]] = user_response
                        elif RESPONSE in input_dict:
                            # If it's an response based prompt, then call the appropriate response method from the 'response' key of the input prompt
                            if user_response in input_dict[RESPONSE]:
                                response_method = input_dict[RESPONSE][user_response]
                                getattr(
                                    self, response_method
                                )()  # can be global or local
                                break
                            else:
                                print("That was an incorrect input. Please try again.")
                    else:
                        # Wrong prompt structure
                        exit_gracefully()
            else:
                # Wrong prompt structure
                exit_gracefully()
        return arg_dict

    def help_me(self):
        with open(os.path.join(INPUT_SCRIPT_PATH, "help.txt"), "r") as f:
            print(f.read())
        self.__continue_and_clear()

    def view_tree(self):
        print("This is where the tree will be viewed")

    def set_arg(self):
        print("CLI args will be set based on the response")

    def proceed(self):
        print("Proceed next")

    def __continue(self):
        input("Press enter to continue")

    def __continue_and_clear(self):
        input("Press enter to continue")
        os.system("clear")
