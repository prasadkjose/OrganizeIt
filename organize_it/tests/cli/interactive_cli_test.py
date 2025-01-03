""" Testing module for interactive_cli"""

import os
import pytest

from organize_it.cli.interactive_cli import InteractiveCLI
from organize_it.settings import TEST_FIXTURES_DIR
from organize_it.tests.test_utils import dicts_are_equal


class TestInteractiveCli:
    """Testing class for InteractiveCLI"""

    interactive_cli = InteractiveCLI(
        lambda: "1",
        lambda: "2",
        lambda: "3",
        script_path=os.path.join(TEST_FIXTURES_DIR, "input_scripts"),
    )

    def test_start_interactive_prompts(self, monkeypatch, capfd):
        # 1. Create a test input script yaml file
        # 2. Test for a mock input and set an arg.

        inputs_list = iter(["y", "y", "sample/src/path", 123, "sample/dest/path"])
        non_prompts_list = iter(
            ["Non-response Prompt 1\n", "\nNon-response Prompt 2\n", "\n", "", ""]
        )
        interactive_prompts_list = iter(
            [
                "Interactive Prompt 1",
                "Interactive Prompt 2",
                "This input will set the 'arg1' arg",
                "This input will set the 'arg2' arg",
                "This input will set the 'arg3' arg",
            ]
        )

        def tester(interactive_prompt):
            out, _ = capfd.readouterr()
            assert out == next(non_prompts_list)
            assert interactive_prompt == next(interactive_prompts_list)
            return next(inputs_list)

        monkeypatch.setattr("builtins.input", tester)  # pass in the tester method
        args = TestInteractiveCli.interactive_cli.start_interactive_prompts()

        assert (
            dicts_are_equal(
                args,
                {
                    "arg1": "sample/src/path",
                    "arg2": 123,
                    "arg3": "sample/dest/path",
                },
            )
            is True
        )

    def test_input_error(self, monkeypatch, capfd):

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
            [
                "Interactive Prompt 1",
                "Interactive Prompt 1",
                "Interactive Prompt 1",
                "Interactive Prompt 1",
                "Interactive Prompt 1",
            ]
        )

        def tester(interactive_prompt):
            out, _ = capfd.readouterr()
            assert out == next(non_prompts_list)
            assert interactive_prompt == next(interactive_prompts_list)
            return next(inputs_list)

        monkeypatch.setattr("builtins.input", tester)  # pass in the tester method
        with pytest.raises(SystemExit):
            TestInteractiveCli.interactive_cli.start_interactive_prompts()
