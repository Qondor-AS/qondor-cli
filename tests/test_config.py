"""Tests for CLI configuration resolution."""

from __future__ import annotations

import os
from unittest.mock import patch

from qondor_cli._config import Config, resolve_config


class TestConfigFromEnv:
    def test_subscription_key_from_env(self):
        with patch.dict(os.environ, {"QONDOR_SUBSCRIPTION_KEY": "env-key"}):
            cfg = resolve_config(subscription_key=None, env=None)
        assert cfg.subscription_key == "env-key"

    def test_env_from_env_var(self):
        with patch.dict(os.environ, {"QONDOR_SUBSCRIPTION_KEY": "k", "QONDOR_ENV": "test"}):
            cfg = resolve_config(subscription_key=None, env=None)
        assert cfg.env == "test"

    def test_env_defaults_to_prod(self):
        with patch.dict(os.environ, {"QONDOR_SUBSCRIPTION_KEY": "k"}, clear=True):
            cfg = resolve_config(subscription_key=None, env=None)
        assert cfg.env == "prod"


class TestConfigFlagOverridesEnv:
    def test_flag_overrides_env_key(self):
        with patch.dict(os.environ, {"QONDOR_SUBSCRIPTION_KEY": "env-key"}):
            cfg = resolve_config(subscription_key="flag-key", env=None)
        assert cfg.subscription_key == "flag-key"

    def test_flag_overrides_env_env(self):
        with patch.dict(os.environ, {"QONDOR_SUBSCRIPTION_KEY": "k", "QONDOR_ENV": "test"}):
            cfg = resolve_config(subscription_key=None, env="dev")
        assert cfg.env == "dev"


class TestConfigBaseUrl:
    def test_prod_base_url(self):
        cfg = Config(subscription_key="k", env="prod")
        assert cfg.base_url == "https://qondor.azure-api.net/Prod"

    def test_test_base_url(self):
        cfg = Config(subscription_key="k", env="test")
        assert cfg.base_url == "https://qondor.azure-api.net/Test"

    def test_dev_base_url(self):
        cfg = Config(subscription_key="k", env="dev")
        assert cfg.base_url == "https://qondor.azure-api.net/Dev"


class TestConfigMissingKey:
    def test_missing_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            import pytest

            with pytest.raises(SystemExit):
                resolve_config(subscription_key=None, env=None)
