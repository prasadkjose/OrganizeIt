""" GPT4All module to initalize and run local GPT models"""

import logging
from pydantic import BaseModel
import json
from openai import OpenAI
import os
from gpt4all import GPT4All

from organize_it.settings import (
    TMP_DIR,
    SCHEMA,
    get_constant,
    load_yaml,
    AI_DIR,
)
from organize_it.schema_validation.validator import YAMLConfigValidator
from organize_it.bin.file_manager import FileManager

LOGGER = logging.getLogger(__name__)

SYSTEM = "system"
USER = "user"


class GPTWrapper:
    """
    GPT wrapper class to initialize and work with AI endpoints and models.
    """

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

    def generate(self, unsorted_tree, user_propmts=None, file_path: str = None):
        if not user_propmts:
            LOGGER.info("Asking OpenAI GPT for some input")

        # A pydantic subclass of the type of return object.
        class YamlResponseFormat(BaseModel):
            config: str

        messages = [
            {
                "role": "system",
                "content": "Given the following JSON schema:"
                + str(SCHEMA)
                + self.system_prompt
                + str(unsorted_tree),
            },
        ]
        if user_propmts:
            messages.append(user_propmts)

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=YamlResponseFormat,
        )

        if file_path:
            LOGGER.info(" - Saving file structure to %s", os.path.basename(file_path))

        return completion.choices[0].message

    def generate_config(self, unsorted_tree, user_propmts=None, file_path=None):

        result = self.generate(
            unsorted_tree,
            user_propmts,
            file_path,
        )

        json_object = json.loads(result.parsed.config)
        v = YAMLConfigValidator(json_object)
        valid = v.validate_config()

        if not valid:
            result = self.generate_config(
                unsorted_tree,
                {"role": "user", "content": self.user_prompts_iter.next()},
                file_path,
            )

        FileManager.create_and_write_file(
            file_path,
            lambda file_stream: json.dump(
                json_object, file_stream, ensure_ascii=False, indent=4
            ),
        )

        return result
