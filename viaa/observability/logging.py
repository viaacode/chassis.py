#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  viaa/logging.py
#  

import logging
import sys

import structlog

loggers: dict = {}

def get_logger(name="", config=None):
    """Return a logger
    
    Returns:
        BoundLoggerLazyProxy -- logger
    """
    __init()
    
    if name in loggers:
        logger = loggers.get(name)
    else:
        logger = structlog.get_logger(name)
        loggers[name] = logger
    
    if config is not None:
        logger = __configure(logger, config["logging"])

    return logger

def __configure(logger, config: dict) -> None:
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
            # Creates the necessary args, kwargs for log()
            structlog.stdlib.render_to_log_kwargs,
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
