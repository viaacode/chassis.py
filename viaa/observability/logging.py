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

# logger configuration
logging.basicConfig(format="%(message)s", level=logging.INFO, stream=sys.stdout)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,  # First step, filter by level to
        structlog.stdlib.add_logger_name,  # module name
        structlog.stdlib.add_log_level,  # log level
        structlog.stdlib.PositionalArgumentsFormatter(),  # % formatting
        structlog.processors.StackInfoRenderer(),  # adds stack if stack_info=True
        structlog.processors.format_exc_info,  # Formats exc_info
        structlog.processors.UnicodeDecoder(),  # Decodes all bytes in dict to unicode
        structlog.processors.TimeStamper(
            fmt="iso"
        ),  # Because timestamps! UTC by default
        structlog.stdlib.render_to_log_kwargs,  # Preps for logging call
        structlog.processors.JSONRenderer(),  # to json
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def get_logger():
    """Return a logger
    
    Returns:
        BoundLoggerLazyProxy -- logger
    """
    logger = structlog.get_logger()
    return logger
    