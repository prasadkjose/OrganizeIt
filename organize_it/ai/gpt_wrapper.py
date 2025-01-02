""" GPT4All module to initalize and run local GPT models"""

import logging
import os
from gpt4all import GPT4All
from organize_it.settings import (
    TMP_DIR,
    SCHEMA,
    GENERATED_SOURCE_TREE,
    get_constant,
    load_yaml,
    AI_DIR,
)
import sys
from openai import OpenAI

LOGGER = logging.getLogger(__name__)

SYSTEM = "system"
USER = "user"


class GPTWrapper:
    def __init__(self, is_online: bool = True):
        self.is_online = bool(is_online)
        self.api_key = get_constant("OPEN_API_KEY")

        prompts = load_yaml(AI_DIR)
        self.system_prompt = prompts.get(SYSTEM) if SYSTEM in prompts else None

        if USER in prompts:
            user_prompt = prompts.get(USER)
            self.user_prompts_iter = iter(user_prompt)

        self.init_open_ai()

    def init_gpt4all(self):
        self.model = GPT4All(
            model_name="orca-mini-3b-gguf2-q4_0.gguf", model_path=TMP_DIR, verbose=True
        )

    def init_open_ai(self):
        self.client = OpenAI(api_key=self.api_key)

    def generate_config(self, user_propmts=None):
        # TODO: this method is exposed to the rest of the app. Method to wrap user request with developer prompts
        # TODO: Implement type:json
        if not user_propmts:
            LOGGER.info("Asking OpenAI GPT for some input")

        messages = [
            {
                "role": "system",
                "content": SCHEMA + self.system_prompt,
            },
        ]
        if user_propmts:
            messages.append(user_propmts)
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
        return completion

    def regenerate_config(self):
        # TODO: set up an iterator
        self.generate_config({"role": "user", "content": self.user_prompts_iter.next()})
