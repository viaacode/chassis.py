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


class EnvVar(yaml.YAMLObject):
    """This constructor is automatically registerd in the Yaml loader via the
    YAMLObjectMetaclass.
    TODO: also add a representer? -> cls.to_yaml
    """

    # yaml_tag is what is used in the metaclass
    yaml_tag = "!ENV"
    yaml_loader = yaml_loader
    pattern = re.compile(r".*?\${(\w+)}.*?")

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(tag={self.yaml_tag})"

    # This is the YAML deserializer function: in our case, the result is a
    # string object.
    # TODO: do we also need a representer -> to_yaml()?
    @classmethod
    def from_yaml(cls, loader, node):
        value = loader.construct_scalar(node)
        match = cls.pattern.findall(value)
        # TODO: if no match, means we got an '!ENV' tag but a wrong expansion
        # syntax -> raise Error!
        if match:
            return cls._interpolate_env_vars(match, value)
        return value

    def _interpolate_env_vars(match, value):
        for env_var in match:
            try:
                env_var_value = os.environ[env_var]
            except KeyError as e:
                msg = (
                    f'Config requires environment variable "{env_var}" which is not set'
                )
                raise KeyError(msg) from None
            else:
                value = value.replace(f"${{{env_var}}}", env_var_value)
        return value


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
        self.chassis_cfg = self._get_chassis_config()
        self.app_cfg = self._get_app_config()

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

    def _get_chassis_config(self) -> dict:
        """Return only the config internal to Chassis.py, ie., the viaa-section
        of the config tree."""
        try:
            return self.cfg["viaa"]
        except KeyError as e:
            return {}
    
    def _get_app_config(self) -> dict:
        """Return only the application specific configuration."""
        try:
            return self.cfg["app"]
        except KeyError as e:
            return {}

    def get_config(self) -> dict:
        """Return only the config internal to Chassis.py, ie., the viaa-section
        of the config tree."""
        return self.chassis_cfg
