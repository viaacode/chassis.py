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

    def __init__(self):
        cfg = {}
        # TODO: Take config from commandline arguments
        # TODO: Take config from environment variables
        # Take config from the user's config file
        if os.path.isfile(os.getcwd() + "/config.yml"):
            with open(os.getcwd() + "/config.yml", "r") as ymlfile:
                cfg: dict = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # Fallback to default
        else:
            cfg = {"viaa": {"logging": {"level": "DEBUG"}}}

        if "viaa" in cfg:
            self.config = cfg["viaa"]

    def get_config(self) -> dict:
        return self.config
