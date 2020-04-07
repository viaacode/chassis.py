#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  configuration.py
#
#  Copyleft 2020 meemoo vzw
#


import os
import yaml


class ConfigParser:
    """The ConfigParser has a config dictionary containing
    all the configuration for the Chassis, but it can also be
    used for program-specific configuration.
    The configuration can come from multiple sources and if
    duplicate settings are found the one from the source with
    the highest priority will be used.
    1. Commandline arguments
    2. Environment variables
    3. Config file
    4. Defaults
    """

    config: dict = {}

    def __init__(self, config_file="config.yml"):
        self.cfg = self._parse_config(config_file)
        self.config = self._get_viaa_config()

    def _parse_config(self, config_file) -> dict:
        """Parse and return the full config tree."""
        config_filepath = os.path.join(os.getcwd(), config_file)
        try:
            with open(config_filepath, "r") as ymlfile:
                cfg: dict = yaml.load(ymlfile, Loader=yaml.FullLoader)
        except IOError as e:
            # Fallback to default
            cfg = {"viaa": {"logging": {"level": "DEBUG"}}}
        return cfg
        cfg = {}

    def _get_viaa_config(self) -> dict:
        """Return only the viaa-section of the config tree."""
        try:
            return self.cfg["viaa"]
        except KeyError as e:
            return {}

    def get_config(self) -> dict:
        """Returns only the viaa-section of the config tree."""
        return self.config
