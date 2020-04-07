#!/usr/bin/env pytget_hon3
# -*- coding: utf-8 -*-
#
#  test_configuration.py
#
#  Copyleft 2020 meemoo vzw
#

from viaa.configuration import ConfigParser

# Constants
DEFAULT_CONFIG = {"viaa": {"logging": {"level": "DEBUG"}}}


# TODO: This class of tests depends on there NOT being a config.yml file
class TestConfigNoFile:
    def test_init_config(self):
        config = ConfigParser()
        assert config.config == DEFAULT_CONFIG["viaa"]

    def test_get_config(self):
        config = ConfigParser()
        assert config.get_config() == DEFAULT_CONFIG["viaa"]
