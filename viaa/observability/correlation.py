#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  viaa/observability/correlation.py
#

# Builtin
# from __future__ import annotations  # See: PEP 563
# Postponed Evaluation of Annotations is only available from Py 3.7
import sys
import threading
import uuid
from functools import wraps
from typing import Optional
# 3d
import pika
from werkzeug.wrappers import Request, Response, ResponseStream
# Local
#~ from viaa.observability import logging

# Constants
CORRELATION_ID_KEY = "X-Correlation-ID" # TODO: this is the header key: should this be moved to flask.py?


class SingletonMeta(type):
    """The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """
    
    #~ _instance: Optional[SingletonMeta] = None
    _instance: Optional = None
    
    #~ def __call__(self) -> SingletonMeta:
    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class SingletonMeta(type):
    """The Singleton metaclass that provides a naive (non-thread-safe)
    singleton implementation.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CorrelationID(metaclass=SingletonMeta):
    """The CorrelationID singleton class"""
    # TODO: try and remove this
    correlation_id = None
    #
    def __init__(self, subject = None):
        self.correlation_id = self._get_or_generate_correlation_id()
    #
    def _get_or_generate_correlation_id(self) -> str:
        """Check if we already have a correlation ID set and generate one if not."""
        if not self.correlation_id:
            return self._generate_correlation_id()
    #
    def _generate_correlation_id(self) -> str:
        """Generates a unique correlation ID. Although trivial enough, this is
        the one and only place where a correlation ID may be generated as to be
        consistent with respect to the format. The format used is
        `uuid.uuid4().hex`, ie., 32 hexadecimal digits NOT seperated in 5
        groups by hyphens. This, also, because they're more easy to copy-paste.
        """
        return uuid.uuid4().hex
    #
    def get_correlation_id_from_flask(self, flask_request):
        """Yes, we could more easily do:
            request.headers.get(CORRELATION_ID_KEY, uuid.uuid4().hex)
        However, than we would lose knowledge about where the correlation-ID
        was originally generated.
        """
        try:
            # The headers dict should be case-insensitive (see: https://stackoverflow.com/a/57562733)
            # We might need to explicitly convert it to lowercase in the future in the unlikely event werkzeug should change its behavior.
            # We get the key not by the dict's `get`-method because we prefer try-except over testing for None.
            correlation_id = flask_request.headers[CORRELATION_ID_KEY]
            # TODO: set_correlation_origin('flask')
            self.correlation_id = correlation_id
            print(f"Request already contained a correlation ID: {correlation_id}")
        except KeyError as e:
            self.correlation_id = self._generate_correlation_id()
            print(f"Flask request did not already contain a correlation ID: generated -> {self.correlation_id}")
        return self.correlation_id
    #
    def get_correlation_id_from_amqp(self):
        pass


class AMQPCorrelationID(CorrelationID):
    pass

