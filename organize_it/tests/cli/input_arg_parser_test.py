""" Testing module InputArgParser Class """

import pytest
import argparse
from unittest import mock
from organize_it.cli.input_arg_parser import InputArgParser


@pytest.mark.usefixtures("test_setup")
class TestInputArgParser:
    """Main testing class for InputArgParser Class"""

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        side_effect=[
            argparse.Namespace(
                src="some/source", dest="some/dest", move=True, interactive=False
            ),
            argparse.Namespace(src="some/source1", dest="some/dest1"),
            argparse.Namespace(),
        ],
    )
    def test_parse_args(self, mock_args):
        """Test parse_args methods with simulated CLI args and if they correctly get assigned as class members"""

        # Non interactive mode
        # 1. mock ArgumentParser and assign args
        # 2. Check the instance if src, dest and moove values are assigned tot he class instance.
        parser = InputArgParser()

        assert (parser.src, parser.dest, parser.move, parser.interactive) == (
            "some/source",
            "some/dest",
            True,
            False,
        )

        parser = InputArgParser()
        assert (parser.src, parser.dest, parser.move, parser.interactive) == (
            "some/source1",
            "some/dest1",
            None,
            False,
        )

        parser = InputArgParser()
        assert (parser.src, parser.dest, parser.move, parser.interactive) == (
            None,
            None,
            None,
            False,
        )
