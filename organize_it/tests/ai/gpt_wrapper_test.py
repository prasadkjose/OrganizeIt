""" GPT4All module to initalize and run local GPT models"""

from organize_it.ai.gpt_wrapper import GPTWrapper


class TestGPTWrapper:
    def test_gpt_wrapper(self):
        print("start")
        wrapper = GPTWrapper()
        wrapper.init_open_ai()
        prompt = "Give me a fact about the earth in less than 20 words"
        pass
