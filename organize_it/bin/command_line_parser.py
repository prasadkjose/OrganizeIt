""" CLI arg parser module for the project """

import argparse


class CommandLineParser:
    """Command Line Parser class to process CLI args used in the tool."""

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--src", help="--src: Path to the directory to organize."
        )
        self.parser.add_argument(
            "--dest",
            help="--src: Path to the destination directory to move the organized files.",
        )
        cli_args = self.parser.parse_args()
        self._source_dir = cli_args.src
        self._dest_dir = cli_args.dest

    @property
    def src(self):
        return self._source_dir

    @property
    def dest(self):
        return self._dest_dir
