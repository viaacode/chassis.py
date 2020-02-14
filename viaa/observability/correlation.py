import sys
import uuid
from functools import wraps

from flask import request
from werkzeug.wrappers import Request, Response, ResponseStream


def meemooId():
    try:
        meemooId = request.headers.get("X-Viaa-Request-Id", uuid.uuid4().hex)
    except Exception:
        meemooId = uuid.uuid4().hex

    return meemooId


def requests_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwgs):
        custom_headers = {"X-Viaa-Request-Id": meemooId()}
        headers = kwgs.pop("headers", None) or {}
        headers.update(custom_headers)
        return f(*args, headers=headers, **kwgs)

    return wrapper


def init_flask(app):
    app.wsgi_app = CorrelationMiddleware(app.wsgi_app)

    print("Flask patched up and ready to go")


def init_requests(requests):
    requests.api.request = requests_wrapper(requests.api.request)
    requests.api.get = requests_wrapper(requests.api.get)
    requests.api.options = requests_wrapper(requests.api.options)
    requests.api.head = requests_wrapper(requests.api.head)
    requests.api.post = requests_wrapper(requests.api.post)
    requests.api.put = requests_wrapper(requests.api.put)
    requests.api.patch = requests_wrapper(requests.api.patch)
    requests.api.delete = requests_wrapper(requests.api.delete)

    print("Requests patched up and ready to go")


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
