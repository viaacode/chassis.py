import json
import sys
import re
#~ from unittest.mock import Mock, patch

import pytest
from flask import Flask, request

from viaa.observability.correlation import (
    CorrelationID,
    CORRELATION_ID_KEY
)
from viaa.configuration import ConfigParser

config = ConfigParser()

UUID_REGEX = r"^[0-9a-fA-F]{32}$"
test_uuid = '8c8f1d230b1140448ee5fe152d019154'

#@patch('viaa.observability.Request')
def test_correlation_id():
    uuid_pattern = re.compile(UUID_REGEX)
    #mock_request.headers.set(CORRELATION_ID_KEY, 'abc123')
    assert uuid_pattern.match(test_uuid).span() == (0, 32)

def test_generate_correlation_id():
    # GIVEN: the known format of our correlation ID's
    uuid_pattern = re.compile(UUID_REGEX)
    # WHEN: we have the have the CorrelationID class generate an ID
    correlation_id = CorrelationID()._generate_correlation_id()
    # THEN: this ID should match the format/pattern
    assert uuid_pattern.match(correlation_id).span() == (0, 32)

def test_get_correlation_id_from_flask():
    # See: https://gist.github.com/pgjones/0bd192d3fae7f6dfadead178dbac0e1e
    app = Flask(__name__)
    app.testing = True
    wsgi_header_name = f"HTTP_{CORRELATION_ID_KEY.upper().replace('-', '_')}"
    with app.test_request_context(environ_base={wsgi_header_name: test_uuid}):
        # WHEN: we have the CorrelationID class retreive the ID from the request
        correlation_id = CorrelationID().get_correlation_id_from_flask(request)
        # THEN: the correlation ID we get back should match the one we initially provided
        assert correlation_id == test_uuid
