""" Interactive CLI module for the project """

import os
from types import SimpleNamespace
from organize_it.settings import (
    load_yaml,
    ROOT_DIR,
    AI_GENERATED_CONFIG,
    exit_gracefully,
    GENERATED_SOURCE_TREE,
    GENERATED_DESTINATION_TREE,
)
from organize_it.ai.gpt_wrapper import GPTWrapper

INPUT_SCRIPT_PATH = os.path.join(ROOT_DIR, "cli")

INPUT = "input"
PRINT = "print"
ARG = "arg"
RESPONSE = "response"
PROCEED_DOWN = "proceed_down"

KEY_TO_ARG_DICT = {"m": "move"}

# A dict of args and a corresponding method name to be invoked after the arg is set.
ARG_SIDE_EFFECTS = {"config": "on_config_set"}

# The number of user attempts per input before exiting.
NUMBER_OF_ATTEMPTS = 5

# TODO: backwards iteration https://stackoverflow.com/questions/55380989/is-there-any-way-to-go-back-a-step-in-a-python-for-loop


class InteractiveCLI:
    """Interactive CLI module to handle input from user"""

    def __init__(
        self,
        generate_source_tree,
        categorize_and_generate_dest_tree,
        generate_with_ai,
        script_path: str = INPUT_SCRIPT_PATH,
    ):
        self.script_list = load_yaml(script_path)
        self.generate_source_tree = generate_source_tree
        self.categorize_and_generate_dest_tree = categorize_and_generate_dest_tree
        self.generate_with_ai = generate_with_ai

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
                        # NS user response method arguments.
                        response_fn_args_dict = SimpleNamespace(
                            user_response=user_response,
                            input_dict=input_dict,
                        )
                        if ARG in input_dict:
                            # If it's an arg based prompt, then store the response in it
                            self.arg_dict[input_dict[ARG]] = user_response
                            # Execute any side effect callables if registered for this arg.
                            if input_dict[ARG] in ARG_SIDE_EFFECTS:
                                getattr(self, ARG_SIDE_EFFECTS[input_dict[ARG]])(
                                    response_fn_args_dict
                                )
                            break
                        elif RESPONSE in input_dict:
                            # If it's an response based prompt, then call the appropriate response method from the 'response' key of the input prompt
                            if user_response in input_dict[RESPONSE]:
                                response_method = input_dict[RESPONSE][user_response]
                                # Invoke the associated response method registered in the prompt config
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

    # Arg sideffects.
    def on_config_set(self, _):
        # Load the config from the user input
        self.config = load_yaml(self.arg_dict["config"])
        self.arg_dict["config"] = self.config

    def help_me(self, _):
        with open(
            os.path.join(INPUT_SCRIPT_PATH, "help.txt"), "r", encoding="utf-8"
        ) as f:
            print(f.read())
        self.__continue_and_clear()

    def generate_config_with_ai(self, _):
        self.config = self.generate_with_ai()
        self.arg_dict["config"] = self.config

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

    def view_tree_source(self, args):
        """This method calls :func:`organizeIt.__main__.process_source_and_generate_tree`"""
        (
            self.file_manager,
            self.tree_structure,
            self.source_tree_dict,
        ) = self.generate_source_tree(self.arg_dict["src"], self.arg_dict["dest"])
        # Print the source tree only if the use chooses to view it.
        if args.user_response == "y":
            with open(os.path.join(GENERATED_SOURCE_TREE), "r", encoding="utf-8") as f:
                print(f.read())
                self.__continue_and_clear()

    def view_tree_destination(self, _):
        """This method calls :func:`organizeIt.__main__.categorize_and_generate_dest_tree`"""
        # The YAML config is loaded either using AI or a static config.
        self.categorize_and_generate_dest_tree(
            self.config,
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
