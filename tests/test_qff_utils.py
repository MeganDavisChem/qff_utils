#!/usr/bin/env python

"""Tests for `qff_utils` package."""


import unittest
import shutil
from click.testing import CliRunner

from qff_utils import qff_utils
from qff_utils import cli
from qff_utils.spec2latex import panda_qff
from qff_utils.xqpgen import xqpgen
from qff_utils.qff_helper import qff_helper
from qff_utils.spec2latex import cli as spec2latex_cli
from qff_utils.xqpgen import cli as xqpgen_cli
from qff_utils.qff_helper import cli as qff_helper_cli


class TestQff_utils(unittest.TestCase):
    """Tests for `qff_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_000_something(self):
        """Test something."""
        pass

    def test_panda_qff(self):
        assert 1 == 2, "You moron!"

    def test_xqpgen(self):
        runner = CliRunner()
        result = runner.invoke(xqpgen_cli.main)
        shutil.rmtree("freqs")

    def test_qff_helper(self):
        runner = CliRunner()
        result = runner.invoke(
            qff_helper_cli.main,
            [
                "--eland",
                "example_files/hcf/files/freqs",
                "example_files/hcf/pts/intder.in",
                "example_files/hcf/pts/energy.dat",
                "hcf",
                "justtesting",
            ],
        )

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)

        # basic cli tests
        assert result.exit_code == 0
        assert "qff_utils.cli.main" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output


if __name__ == "__main__":
    unittest.main()
