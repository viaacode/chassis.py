#!/usr/bin/env pytget_hon3
# -*- coding: utf-8 -*-
#
#  test_configuration.py
#
#  Copyleft 2020 meemoo vzw
#

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
