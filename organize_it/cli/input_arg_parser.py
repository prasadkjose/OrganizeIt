""" CLI arg parser module for the project """

import argparse
from organize_it.cli.interactive_cli import InteractiveCLI


class InputArgParser:
    """Command Line Input Arg Parser class to process CLI args used in the tool."""

    def __init__(
        # the callback methods can be none if we are not interested in interactive CLI and also for testing this class.
        self,
        generate_source_tree=None,
        categorize_and_generate_dest_tree=None,
    ):

        self._source_dir, self._dest_dir, self._move, self._interactive = (
            self.parse_args()
        )

        if bool(self.interactive):
            # Get the args from the interactive CLI
            args = self.interactive_cli(
                generate_source_tree, categorize_and_generate_dest_tree
            )
            self._source_dir, self._dest_dir, self._move = [
                args.get(f) for f in ["src", "dest", "move"]
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
        return self._interactive

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
                "-i",
                "--interactive",
                help="--interactive: Use this flag to make the CLI tool interactive.",
                action="store_true",
            )
            cli_args = parser.parse_args()
            return [
                vars(cli_args).get(f) for f in ["src", "dest", "move", "interactive"]
            ]

        except SystemExit as exception:
            raise exception

    def interactive_cli(
        self, generate_source_tree, categorize_and_generate_dest_tree
    ) -> dict:
        interactive_cli = InteractiveCLI()
        arg_dict = interactive_cli.start_interactive_prompts(
            generate_source_tree, categorize_and_generate_dest_tree
        )
        return arg_dict
