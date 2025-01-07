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
    AI_GENERATED_CONFIG,
    get_constant,
    load_yaml,
    AI_DIR,
    exit_gracefully,
)
from organize_it.schema_validation.validator import JSONSchemaValidator
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

    def generate(self, unsorted_tree, user_propmts=None):
        """
        openai.generate wrapper to create a YAML configuration based on a given unsorted file tree and optional user prompts.

        Args:
            unsorted_tree (dict): A representation of the unsorted file and directory structure.
            user_propmts (dict, optional): Additional user-provided prompts to guide the YAML generation.
                If not provided, the method will interact with OpenAI GPT to gather input.

        Returns:
            str: A YAML configuration string generated based on the schema and file tree.

        Notes:
            - The method uses a Pydantic model (`YamlResponseFormat`) to validate the response format.
            - If no user prompts are supplied, a message is logged, and the system relies on the OpenAI model
            to generate suggestions.
            - The OpenAI chat model (`gpt-4o-mini`) is used for generating the YAML output.

        Raises:
            Any exceptions raised by the OpenAI client or Pydantic validation will propagate.
        """
        if not user_propmts:
            LOGGER.info(" - Asking OpenAI GPT for some input")

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

        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                response_format=YamlResponseFormat,
            )
        except Exception as error:
            exit_gracefully(error)

        return completion.choices[0].message

    def generate_config(
        self,
        unsorted_tree: dict,
        user_propmts: dict = None,
        file_path: str = AI_GENERATED_CONFIG,
    ):
        """
        Validates the AI generated configuration file based on an unsorted file tree, with optional user prompts.

        This method leverages AI to create a configuration file in JSON format, validates it against predefined rules,
        and optionally saves it to a specified file path.

        This method can be extended to be used for any AI models where the results will be validated for the oIt system.

        Args:
            unsorted_tree (dict): A representation of the unsorted file and directory structure.
            user_propmts (dict, optional): Additional user-provided prompts to guide the configuration generation. Defaults to None.
            file_path (str, optional): Path to save the generated configuration file. Defaults to AI_GENERATED_CONFIG.

        Returns:
            dict: The validated configuration as a JSON object.

        Raises:
            StopIteration: Raised when no further user prompts are available, exiting the tool gracefully.

        Workflow:
            1. Calls the `generate` method to produce a configuration using AI.
            2. Attempts to parse the AI-generated configuration as JSON.
            3. If parsing fails or validation fails:
                - Logs the issue and retries with the next user prompt from `self.user_prompts_iter`.
                - Exits gracefully if there are no more user prompts.
            4. Validates the configuration using `JSONSchemaValidator`.
            5. Saves the validated configuration to `file_path` if provided.

        Notes:
            - If validation or parsing fails, the method will retry with the next available user prompt.
            - Logs progress and errors to the application logger.
            - Ensures the configuration is saved in a human-readable JSON format.

        """

        LOGGER.info(" - Generating config with AI... Please be patient")
        result = self.generate(
            unsorted_tree=unsorted_tree,
            user_propmts=user_propmts,
        )

        try:
            try:
                json_object = json.loads(result.parsed.config)
            except ValueError as exeption:
                LOGGER.debug(" - Regenerating the config due to: %s", str(exeption))
                result = self.generate_config(
                    unsorted_tree=unsorted_tree,
                    user_propmts={
                        "role": "user",
                        "content": self.user_prompts_iter.next(),
                    },
                    file_path=file_path,
                )

            # Validate the config.
            v = JSONSchemaValidator(config_data=json_object, schema=SCHEMA)
            valid = v.validate_config()
            if not valid:
                result = self.generate_config(
                    unsorted_tree=unsorted_tree,
                    user_propmts={
                        "role": "user",
                        "content": self.user_prompts_iter.next(),
                    },
                    file_path=file_path,
                )
        except StopIteration as error:
            exit_gracefully(error)

        if file_path:
            LOGGER.info(" - Saving file structure to %s", os.path.basename(file_path))
            FileManager.create_and_write_file(
                file_path=file_path,
                callback=lambda file_stream: json.dump(
                    json_object, file_stream, ensure_ascii=False, indent=4
                ),
            )

        return json_object
