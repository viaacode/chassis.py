#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  configuration.py
#
#  Copyleft 2020 meemoo vzw
#


import os
import re

import yaml


yaml_loader = yaml.FullLoader

ENV_TAG = "!ENV"
pattern = re.compile(r".*?\${(\w+)}.*?")


def env_variable_constructor(loader, node):
    """Extracts the environment variable from the node's value.
    
    :param yaml.Loader loader: the yaml loader
    :param node: the current node in the yaml
    :return: the parsed string that contains the value of the environment
    variable
    """
    value = loader.construct_scalar(node)
    match = pattern.findall(value)
    if match:
        full_value = value
        for env_var in match:
            # TODO: refactor into class + raise error on missing env var
            full_value = full_value.replace(
                f"${{{env_var}}}", os.environ.get(env_var, env_var)
            )
        return full_value
    return value


yaml_loader.add_constructor(ENV_TAG, env_variable_constructor)


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

    def __init__(self, config_file="config.yml"):
        self.cfg = self._parse_config(config_file)
        self.config = self._get_viaa_config()

    def _parse_config(self, config_file) -> dict:
        """Parse and return the full config tree."""
        config_filepath = os.path.join(os.getcwd(), config_file)
        try:
            with open(config_filepath, "r") as ymlfile:
                cfg: dict = yaml.load(ymlfile, Loader=yaml_loader)
        except IOError as e:
            # Fallback to default
            cfg = {"viaa": {"logging": {"level": "DEBUG"}}}
        return cfg

    def _get_viaa_config(self) -> dict:
        """Return only the viaa-section of the config tree."""
        try:
            return self.cfg["viaa"]
        except KeyError as e:
            return {}

    def get_config(self) -> dict:
        """Returns only the viaa-section of the config tree."""
        return self.config
