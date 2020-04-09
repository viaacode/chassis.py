#!/usr/bin/env pytget_hon3
# -*- coding: utf-8 -*-
#
#  test_configuration.py
#
#  Copyleft 2020 meemoo vzw
#

import os

import pytest

from viaa.configuration import ConfigParser


# TODO: This class of tests depends on there NOT being a config.yml file
class TestConfigNoFile:
    """Test the configparser when no config.yml file is present in the working
    directory.
    """

    default_config = {"viaa": {"logging": {"level": "DEBUG"}}}

    def test_init_config(self):
        config = ConfigParser()
        assert config.config == self.default_config["viaa"]

    def test_get_config(self):
        config = ConfigParser()
        assert config.get_config() == self.default_config["viaa"]


class TestConfigFileViaa:
    """Test the configparser with a config-file with a 'viaa'-section."""

    config_test_file = "tests/resources/default_config.yml"

    def test_init_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.config == {"logging": {"level": "WARN"}}

    def test_get_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.get_config() == {"logging": {"level": "WARN"}}


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
        assert config.config == {}

    def test_get_config(self):
        config = ConfigParser(self.config_test_file)
        assert config.get_config() == {}


class TestConfigWithEnvVars:
    """Test the configparser with a config-file with a 'viaa'-section and
    with interpolation of several environment variables."""

    config_test_file = "tests/resources/default_config_with_env_vars.yml"

    os.environ["LOG_PATH"] = "logs/service"
    os.environ["PASSWD"] = "veryverysecret"

    def test_init_config(self):
        config = ConfigParser(self.config_test_file)
        # Test -> log_path: !ENV "/var/${LOG_PATH}"
        assert config.cfg["app"]["log_path"] == "/var/logs/service"
        # Test -> passwd: !ENV ${PASSWD}
        assert config.cfg["app"]["passwd"] == "veryverysecret"


@pytest.mark.skip(reason="ConfigParser raises KeyError, but not here: quid?")
class TestConfigWithMissingEnvVars:
    """Test the configparser with a config-file with a 'viaa'-section and
    with interpolation of several environment variables."""

    config_test_file = "tests/resources/default_config_with_env_vars.yml"

    os.environ["PASSWD"] = "veryverysecret"

    def test_init_config(self):
        with pytest.raises(KeyError) as excinfo:
            config = ConfigParser(self.config_test_file)
