""" Interactive CLI module for the project """

import os
from types import SimpleNamespace
from organize_it.settings import (
    load_yaml,
    ROOT_DIR,
    exit_gracefully,
    GENERATED_SOURCE_TREE,
    GENERATED_DESTINATION_TREE,
)

INPUT_SCRIPT_PATH = os.path.join(ROOT_DIR, "cli")

INPUT = "input"
PRINT = "print"
ARG = "arg"
RESPONSE = "response"
PROCEED_DOWN = "proceed_down"

KEY_TO_ARG_DICT = {"m": "move"}

# The number of user attempts per input before exiting.
NUMBER_OF_ATTEMPTS = 5

# TODO: backwards iteration https://stackoverflow.com/questions/55380989/is-there-any-way-to-go-back-a-step-in-a-python-for-loop


class InteractiveCLI:
    """Interactive CLI module to handle input from user"""

    def __init__(
        self,
        generate_source_tree,
        categorize_and_generate_dest_tree,
        script_path: str = INPUT_SCRIPT_PATH,
    ):
        self.script_list = load_yaml(script_path)
        self.generate_source_tree = generate_source_tree
        self.categorize_and_generate_dest_tree = categorize_and_generate_dest_tree

    def start_interactive_prompts(self, script_list: list = None) -> dict:
        curr_script_list = self.script_list if not script_list else script_list
        self.arg_dict = {}
        for prompt_item in curr_script_list:
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
                            self.arg_dict[input_dict[ARG]] = user_response
                            break
                        elif RESPONSE in input_dict:
                            # If it's an response based prompt, then call the appropriate response method from the 'response' key of the input prompt
                            if user_response in input_dict[RESPONSE]:
                                response_method = input_dict[RESPONSE][user_response]
                                # NS user response method arguments.
                                response_fn_args_dict = SimpleNamespace(
                                    user_response=user_response,
                                    input_dict=input_dict,
                                )
                                # Get the correct response method
                                getattr(self, response_method)(response_fn_args_dict)
                                break
                            else:
                                print("That was an incorrect input. Please try again.")
                    else:
                        # Wrong prompt structure
                        exit_gracefully()
            else:
                # Wrong prompt structure
                exit_gracefully()
        return self.arg_dict

    def help_me(self, _):
        with open(
            os.path.join(INPUT_SCRIPT_PATH, "help.txt"), "r", encoding="utf-8"
        ) as f:
            print(f.read())
        self.__continue_and_clear()

    def set_arg(self, args):
        """
        Sets a specific argument in the internal argument dictionary (`arg_dict`) based
        on the user's response. The method checks if the user's response matches a key
        in a predefined dictionary (`KEY_TO_ARG_DICT`) and, if so, updates the argument
        dictionary accordingly.
        """
        arg = args.user_response in KEY_TO_ARG_DICT or None
        if arg is not None:
            self.arg_dict[arg] = True
        print("CLI args will be set based on the response")

    def view_tree_source(self, _):
        """This method calls :func:`organizeIt.__main__.process_source_and_generate_tree`"""
        (
            self.file_manager,
            self.tree_structure,
            self.source_tree_dict,
        ) = self.generate_source_tree(self.arg_dict["src"], self.arg_dict["dest"])

        with open(os.path.join(GENERATED_SOURCE_TREE), "r", encoding="utf-8") as f:
            print(f.read())

        self.__continue_and_clear()

    def view_tree_destination(self, _):
        """This method calls :func:`organizeIt.__main__.categorize_and_generate_dest_tree`"""
        self.categorize_and_generate_dest_tree(
            load_yaml(self.arg_dict["config"]),
            self.source_tree_dict,
            self.tree_structure,
        )
        with open(os.path.join(GENERATED_DESTINATION_TREE), "r", encoding="utf-8") as f:
            print(f.read())

        self.__continue_and_clear()

    def proceed(self, _):
        print("")

    def proceed_down(self, args):
        self.start_interactive_prompts(args.input_dict[PROCEED_DOWN])

    def __continue(self, _):
        input("Press enter to continue")

    def __continue_and_clear(self):
        input("Press enter to continue")
        os.system("clear")
