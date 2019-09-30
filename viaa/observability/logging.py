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
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

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
            __add_log_source_to_dict,
            # Creates the necessary args, kwargs for log()
            # structlog.stdlib.
            __render_to_log_kwargs,
            # Print as json
            structlog.processors.JSONRenderer(), 
        ],
        # Our "event_dict" is explicitly a dict
        # There's also structlog.threadlocal.wrap_dict(dict) in some examples
        # which keeps global context as well as thread locals
        context_class=dict,
        # Provides the logging.Logger for the underlaying log call
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Provides predefined methods - log.debug(), log.info(), etc.
        wrapper_class=structlog.stdlib.BoundLogger,
        # Caching of our logger
        cache_logger_on_first_use=True,
    )
    
def __add_log_source_to_dict(logger, _, event_dict):
    # If by any chance the record already contains a `modline` key,
    # (very rare) move that into a 'modline_original' key
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

def __render_to_log_kwargs(logger, method_name, event_dict):
    return {
        "message": event_dict.pop("event"), 
        "source": event_dict.pop("source"), 
        "logger": event_dict.pop("logger"), 
        "level": event_dict.pop("level"), 
        "timestamp": event_dict.pop("timestamp"), 
        "extra": event_dict
    }
