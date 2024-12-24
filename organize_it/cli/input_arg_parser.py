""" CLI arg parser module for the project """

import argparse
from operator import itemgetter
from organize_it.cli.interactive_cli import InteractiveCLI


class InputArgParser:
    """Command Line Input Arg Parser class to process CLI args used in the tool."""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "-s", "--src", help="--src: Path to the directory to organize."
        )
        self.parser.add_argument(
            "-d",
            "--dest",
            help="--src: Path to the destination directory to move the organized files.",
        )
        self.parser.add_argument(
            "-m",
            "--move",
            help="--move: Move the files to the destination directory. This operation cannot be reverted.",
        )

        self.parser.add_argument(
            "-i",
            "--interactive",
            help="--interactive: Use this flag to make the CLI tool interactive.",
            action="store_true",
        )

        cli_args = self.parser.parse_args()

        self._interactive = cli_args.interactive

        if bool(self._interactive):
            # Get the args from the interactive CLI
            self._source_dir, self._dest_dir, self._move = self.interactive_cli()
            self.interactive_cli()
        else:
            self._source_dir = cli_args.src
            self._dest_dir = cli_args.dest
            self._move = cli_args.move

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

    def interactive_cli(self) -> dict:
        interactive_cli = InteractiveCLI()
        arg_dict = interactive_cli.start_interactive_prompts()
        return itemgetter("src", "dest", "move")(arg_dict)
