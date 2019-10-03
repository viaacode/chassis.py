#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  viaa/logging.py
#  

import inspect
import logging
import sys

import structlog
from pythonjsonlogger import jsonlogger
from structlog._frames import _find_first_app_frame_and_name

from viaa.configuration import ConfigParser

loggers: dict = {}

def get_logger(name="", config: ConfigParser=None):
    """Return a logger with the specified name and configuration, creating it if necessary.
    If no name is specified, return the root logger.
    If a config is specified it will override the current config for a logger.
    """

    __init()
    
    if name in loggers:
        logger = loggers.get(name)
    else:
        logger = structlog.get_logger(name)
        loggers[name] = logger
    
    if config is not None:
        logger = __configure(logger, config.config["logging"])

    return logger

def __configure(logger, config: dict) -> None:
    """Configures the logger with all relevant configuration from the passed config.
    
    Arguments:
        logger {BoundLoggerLazyProxy} -- Instance of the logger that needs to be configured.
        config {dict} -- Configuration for the logging.
    """
    if "level" in config:
        logger.setLevel(config["level"])
        
    return logger


def __init():
    structlog.configure(
        processors=[
            # This performs the initial filtering, so we don't
            # evaluate e.g. DEBUG when unnecessary
            structlog.stdlib.filter_by_level,
            # Adds logger=module_name (e.g __main__)
            structlog.stdlib.add_logger_name,
            # Adds level=info, debug, etc.
            structlog.stdlib.add_log_level,
            # Performs the % string interpolation as expected
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Include the stack when stack_info=True
            structlog.processors.StackInfoRenderer(),
            # Include the exception when exc_info=True
            # e.g log.exception() or log.warning(exc_info=True)'s behavior
            structlog.processors.format_exc_info,
            # Decodes the unicode values in any kv pairs
            structlog.processors.UnicodeDecoder(),            
            # Adds timestamp in iso format to each log
            structlog.processors.TimeStamper(
                fmt="iso"
            ),
            # Adds linenumber and file to each log
            __add_log_source_to_dict,
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(jsonlogger.JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
def __add_log_source_to_dict(logger, _, event_dict):
    # If by any chance the record already contains a `source` key,
    # (very rare) move that into a 'source_original' key
    if 'source' in event_dict:
        event_dict['source_original'] = event_dict['source']
    
    f, name = _find_first_app_frame_and_name(additional_ignores=[
        "logging",
        __name__
    ])
    
    if not f:
        return event_dict
    filename = inspect.getfile(f)
    frameinfo = inspect.getframeinfo(f)
    if not frameinfo:
        return event_dict
    if frameinfo:
        event_dict['source'] = '{}:{}:{}'.format(
            filename,
            frameinfo.function,
            frameinfo.lineno,
        )
    return event_dict

