""" GPT4All module to initalize and run local GPT models"""

import os
import pytest

from organize_it.ai.gpt_wrapper import GPTWrapper
from organize_it.settings import GENERATED_SOURCE_TREE, AI_GENERATED_CONFIG


@pytest.mark.usefixtures("test_setup")
class TestGPTWrapper:
    def test_gpt_wrapper(self, pytestconfig):
        test_ai = pytestconfig.getoption("ai")
        if test_ai:
            wrapper = GPTWrapper()
            with open(os.path.join(GENERATED_SOURCE_TREE), "r", encoding="utf-8") as f:
                tree = f.read()
            result = wrapper.generate_config(
                unsorted_tree=tree, file_path=AI_GENERATED_CONFIG
            )

            assert result
