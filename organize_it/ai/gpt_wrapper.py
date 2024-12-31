""" GPT4All module to initalize and run local GPT models"""

import os
from gpt4all import GPT4All
from organize_it.settings import TMP_DIR, SCHEMA, GENERATED_SOURCE_TREE, get_constant
import sys
from openai import OpenAI


class GPTWrapper:
    def __init__(self, is_online: bool = True):
        self.is_online = bool(is_online)
        self.api_key = get_constant("OPEN_API_KEY")

    def init_gpt4all(self):
        self.model = GPT4All(
            model_name="orca-mini-3b-gguf2-q4_0.gguf", model_path=TMP_DIR, verbose=True
        )

    def init_open_ai(self):
        client = OpenAI(api_key=self.api_key)
        # TODO: Implement type:json
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who will help organize files and directories. Provide "},
                {
                    "role": "user",
                    "content": "Write a haiku about recursion in programming.",
                },
            ],
        )

    def generate(self):
        # TODO: this method is exposed to the rest of the app. Method to wrap user request with developer prompts
        pass

    def generate_single_line_response(self, prompt):
        a = self.model.generate(prompt)
        return a
