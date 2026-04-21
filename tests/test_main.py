"""Tests for the Typer app entry point and global options."""

from __future__ import annotations

import os
from unittest.mock import patch

from typer.testing import CliRunner

from qondor_cli.main import app

runner = CliRunner()


class TestHelpOutput:
    def test_root_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "qondor" in result.output.lower() or "Usage" in result.output

    def test_offer_help(self):
        result = runner.invoke(app, ["offer", "--help"])
        assert result.exit_code == 0
        assert "get" in result.output.lower()

    def test_project_help(self):
        result = runner.invoke(app, ["project", "--help"])
        assert result.exit_code == 0

    def test_customer_help(self):
        result = runner.invoke(app, ["customer", "--help"])
        assert result.exit_code == 0

    def test_product_help(self):
        result = runner.invoke(app, ["product", "--help"])
        assert result.exit_code == 0

    def test_product_group_help(self):
        result = runner.invoke(app, ["product-group", "--help"])
        assert result.exit_code == 0

    def test_supplier_help(self):
        result = runner.invoke(app, ["supplier", "--help"])
        assert result.exit_code == 0

    def test_contact_person_help(self):
        result = runner.invoke(app, ["contact-person", "--help"])
        assert result.exit_code == 0

    def test_office_help(self):
        result = runner.invoke(app, ["office", "--help"])
        assert result.exit_code == 0

    def test_statistics_help(self):
        result = runner.invoke(app, ["statistics", "--help"])
        assert result.exit_code == 0


class TestMissingSubscriptionKey:
    def test_no_key_exits_with_error(self):
        with patch.dict(os.environ, {}, clear=True):
            result = runner.invoke(app, ["office", "list"])
        assert result.exit_code != 0
