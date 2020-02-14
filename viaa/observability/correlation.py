import sys
import uuid

from flask import request
from werkzeug.wrappers import Request, Response, ResponseStream


def meemooId():
    try:
        meemooId = request.headers.get("X-Viaa-Request-Id", uuid.uuid4().hex)
    except Exception:
        meemooId = uuid.uuid4().hex

    return meemooId


def init_flask(app):
    app.wsgi_app = CorrelationMiddleware(app.wsgi_app)
    print("Flask patched up and ready to go")


class CorrelationMiddleware:
    """
    Middleware to check if a viaa request id is present in the request header.
    Generates a new one if not present.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        incoming_request = Request(environ)

        requestId = incoming_request.headers.get("X-Viaa-Request-Id", uuid.uuid4().hex)

        environ["HTTP_X_VIAA_REQUEST_ID"] = requestId

        return self.app(environ, start_response)
