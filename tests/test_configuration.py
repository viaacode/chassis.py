#!/usr/bin/env pytget_hon3
# -*- coding: utf-8 -*-
#
#  test_configuration.py
#
#  Copyleft 2020 meemoo vzw
#

import pytest

from viaa.configuration import ConfigParser


class TestConfigNoFile:
    """Test the configparser when no config.yml file is present in the working
    directory.
    TODO: Calling the ConfigParser with an explicit filepath argument would
    only ever happen from within the application code, and thus, should raise
    an exception instead of falling back to a default configuration (DEV-790).
    """

    default_config = {"viaa": {"logging": {"level": "DEBUG"}}}

    def test_init_config(self):
        config = ConfigParser("non_existant_file.yml")
        assert config.chassis_cfg == self.default_config["viaa"]

    def test_get_config(self):
        config = ConfigParser("non_existant_file.yml")
        assert config.get_config() == self.default_config["viaa"]


class TestConfigFileViaa:
    """Test the configparser with a config-file with a 'viaa'-section."""

    config_test_file = "tests/resources/default_config.yml"

    def test_init_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.chassis_cfg == {"logging": {"level": "WARNING"}}

    def test_get_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.get_config() == {"logging": {"level": "WARNING"}}


class TestConfigFileViaaAndApplication:
    """Test the configparser with a config-file with a 'viaa'-section and an
    application-specific section."""

    config_test_file = "tests/resources/default_config_with_app.yml"

    def test_init_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.cfg["app"]
        assert config.cfg["app"]["service"]["host"] == "api.example.com"


class TestConfigFileNoViaa:
    """Test the configparser with a config-file without a 'viaa'-section.
    In this case, the configparser returns an empty dict."""

    config_test_file = "tests/resources/config_no_viaa.yml"

    def test_init_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.chassis_cfg == {}

    def test_get_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.get_config() == {}


class TestConfigWithEnvVars:
    """Test the configparser with a config-file with a 'viaa'-section and
    with interpolation of several environment variables."""

    config_test_file = "tests/resources/default_config_with_env_vars.yml"

    def test_init_config(self, monkeypatch):
        monkeypatch.setenv("PASSWD", "veryverysecret")
        monkeypatch.setenv("LOG_PATH", "logs/service")

        config = ConfigParser(self.config_test_file)
        # Test -> log_path: !ENV "/var/${LOG_PATH}"
        assert config.cfg["app"]["log_path"] == "/var/logs/service"
        # Test -> passwd: !ENV ${PASSWD}
        assert config.cfg["app"]["passwd"] == "veryverysecret"


class TestConfigWithMissingEnvVars:
    """Test the configparser with a config-file with a 'viaa'-section and
    with interpolation of several environment variables."""

    config_test_file = "tests/resources/default_config_with_env_vars.yml"

    def test_init_config(self, monkeypatch):
        # Make sure we have one missing env var
        monkeypatch.delenv("LOG_PATH", raising=False)
        monkeypatch.setenv("PASSWD", "veryverysecret")

        with pytest.raises(KeyError) as excinfo:
            config = ConfigParser(self.config_test_file)
