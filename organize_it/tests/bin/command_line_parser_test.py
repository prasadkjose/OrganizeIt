""" Testing module CommandLineParser Class """

import pytest
from organize_it.bin.command_line_parser import CommandLineParser


@pytest.mark.usefixtures("test_setup")
class TestCommandLineParser:
    """Main testing class for CommandLineParser module"""

    def test_command_line_parser(
        self,
    ):
        """Test command_line_parser methods with simulated CLI args"""
        # TODO: Complete test suite for CLI args.
