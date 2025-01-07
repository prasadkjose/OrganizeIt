""" CLI arg parser module for the project """

import argparse
from organize_it.cli.interactive_cli import InteractiveCLI
from organize_it.settings import load_yaml


class InputArgParser:
    """Command Line Input Arg Parser class to process CLI args used in the tool."""

    def __init__(
        # the callback methods can be none if we are not interested in interactive CLI and also for testing this class.
        self,
        generate_source_tree=None,
        categorize_and_generate_dest_tree=None,
        generate_with_ai=None,
    ):

        (
            self._source_dir,
            self._dest_dir,
            self._move,
            self._interactive,
            self._ai,
            self._config,
        ) = self.parse_args()

        if bool(self._interactive):
            # Get the args from the interactive CLI
            args = self.interactive_cli(
                generate_source_tree,
                categorize_and_generate_dest_tree,
                generate_with_ai,
            )
            self._source_dir, self._dest_dir, self._move, self._config = [
                args.get(f) for f in ["src", "dest", "move", "config"]
            ]

    # TODO: Refactor to programatically create getters and setters

    @property
    def src(self):
        return self._source_dir

    @property
    def dest(self):
        return self._dest_dir

    @property
    def move(self):
        return self._move

    @property
    def interactive(self):
        return bool(self._interactive)

    @property
    def ai(self):
        return bool(self._ai)

    @property
    def config(self):
        if self._interactive:
            return self._config  # The config is already loaded by interactive_cli

        return load_yaml(self._config)

    def parse_args(self) -> dict:
        """
        Parses command-line arguments and options using the configured argument parser.

        This method processes the arguments passed to the CLI, validates them, and returns
        the parsed arguments for further use.

        Returns:
            Namespace: A namespace object containing the parsed arguments as attributes.

        Raises:
            SystemExit: If invalid arguments are provided or required arguments are missing,
                        the method may terminate the program with an error message.

        Example:
            args = parse_args()
            # 'args' will contain the parsed command-line arguments
        """

        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(
                "-s", "--src", help="--src: Path to the directory to organize."
            )
            parser.add_argument(
                "-d",
                "--dest",
                help="--src: Path to the destination directory to move the organized files.",
            )
            parser.add_argument(
                "-m",
                "--move",
                action="store_true",
                help="--move: Move the files to the destination directory. This operation cannot be reverted.",
            )
            parser.add_argument(
                "-c",
                "--config",
                help="--src: Path to the YAML/JSON config file with all the necessary rules and settings.",
            )

            parser.add_argument(
                "-i",
                "--interactive",
                help="--interactive: Use this flag to make the CLI tool interactive.",
                action="store_true",
            )
            parser.add_argument(
                "-ai",
                "--ai",
                help="--ai: Use this flag to use AI to organize your files.",
                action="store_true",
            )

            cli_args = parser.parse_args()
            return [
                vars(cli_args).get(f)
                for f in ["src", "dest", "move", "interactive", "ai", "config"]
            ]

        except SystemExit as exception:
            raise exception

    def interactive_cli(
        self, generate_source_tree, categorize_and_generate_dest_tree, generate_with_ai
    ) -> dict:
        interactive_cli = InteractiveCLI(
            generate_source_tree, categorize_and_generate_dest_tree, generate_with_ai
        )
        arg_dict = interactive_cli.start_interactive_prompts()
        return arg_dict
