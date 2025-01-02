""" Testing module for interactive_cli"""

import os
import pytest

from organize_it.cli.interactive_cli import InteractiveCLI
from organize_it.settings import TEST_FIXTURES_DIR


class TestInteractiveCli:
    """Testing class for InteractiveCLI"""

    def test_start_interactive_prompts(self, monkeypatch, capfd):
        # https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
        # 1. Create a test input script yaml file
        # 2. Test for exeption in the format.
        # 3. Test for a mock input and set an arg.
        interactive_cli = InteractiveCLI(
            os.path.join(TEST_FIXTURES_DIR, "input_scripts")
        )

        inputs_list = iter(["y", "y"])
        non_prompts_list = iter(
            ["Non-response Prompt 1\n", "\nNon-response Prompt 2\n"]
        )
        interactive_prompts_list = iter(
            ["Interactive Prompt 1", "Interactive Prompt 2"]
        )

        def tester(interactive_prompt):
            out, _ = capfd.readouterr()
            assert out == next(non_prompts_list)
            assert interactive_prompt == next(interactive_prompts_list)
            return next(inputs_list)

        monkeypatch.setattr("builtins.input", tester)  # pass in the tester method
        interactive_cli.start_interactive_prompts(lambda: "1", lambda: "2")

    # TODO:
    # 1. set_arg
    # 2. view_tree_source
    # 3. view_tree_destination

    def test_input_error(self, monkeypatch, capfd):
        interactive_cli = InteractiveCLI(
            os.path.join(TEST_FIXTURES_DIR, "input_scripts")
        )

        # incorrect inputs
        inputs_list = iter(
            [
                "w",
                "w",
                "w",
                "w",
                "w",
                "w",
            ]
        )
        non_prompts_list = iter(
            [
                "Non-response Prompt 1\n",
                "That was an incorrect input. Please try again.\n",
                "That was an incorrect input. Please try again.\n",
                "That was an incorrect input. Please try again.\n",
                "That was an incorrect input. Please try again.\n",
            ]
        )
        interactive_prompts_list = iter(
            ["Interactive Prompt 1", "Interactive Prompt 2"]
        )

        def tester(interactive_prompt):
            out, _ = capfd.readouterr()
            assert out == next(non_prompts_list)
            # assert interactive_prompt == next(interactive_prompts_list)
            return next(inputs_list)

        monkeypatch.setattr("builtins.input", tester)  # pass in the tester method
        with pytest.raises(SystemExit):
            interactive_cli.start_interactive_prompts(lambda: "1", lambda: "2")
