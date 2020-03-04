import sys
import threading
import uuid
from functools import wraps

import pika
from flask import request
from werkzeug.wrappers import Request, Response, ResponseStream


def meemooId() -> str:
    """
    Returns the current correlation id or generates a new one if there isn't one available.
    """
    try:
        """
        Accessing request throws an exception if there is no request context.
        Every incoming request through flask has a request context. An exception thus means
        we have to get the correlation id from somewhere else.
        """
        meemooId = request.headers.get("X-Viaa-Request-Id", uuid.uuid4().hex)
    except Exception:
        """
        The current_thread name is set to a new uuid on incoming rabbit messages.
        The thread name being 32 characters indicates that the name is an uuid and not 'MainThread'
        """
        if len(threading.current_thread().name) == 32:
            meemooId = threading.current_thread().name
        else:
            meemooId = uuid.uuid4().hex

    return meemooId


def logger_wrapper(f):
    """ The correlation id is added to the kwargs of every log statement. """

    @wraps(f)
    def wrapper(*args, **kwgs):
        return f(*args, correlationId=meemooId(), **kwgs)

    return wrapper


def requests_wrapper(f):
    """ Adds the current correlation id as header to all outgoing http requests. """

    @wraps(f)
    def wrapper(*args, **kwgs):
        custom_headers = {"X-Viaa-Request-Id": meemooId()}
        headers = kwgs.pop("headers", None) or {}
        headers.update(custom_headers)
        return f(*args, headers=headers, **kwgs)

    return wrapper


def outgoing_rabbit_wrapper(f):
    """ Sets the correlation_id property of a rabbit message to the current correlation id """

    @wraps(f)
    def wrapper(*args, **kwgs):
        properties = kwgs.get("properties")
        if properties is None:
            properties = pika.BasicProperties(correlation_id=meemooId())
        else:
            properties.correlation_id = meemooId()
        kwgs["properties"] = properties
        return f(*args, **kwgs)

    return wrapper


def incoming_rabbit_wrapper(f):
    """ We pop the callback function for incoming rabbit messages and we wrap the callback function. """

    @wraps(f)
    def wrapper(*args, **kwgs):
        callback_function = kwgs.pop("on_message_callback", None)
        callback_function = __get_request_id_from_rabbit_message(callback_function)
        return f(*args, on_message_callback=callback_function, **kwgs)

    return wrapper


def __get_request_id_from_rabbit_message(f):
    """ 
    The callback function gets the following positional arguments: channel, method, properties, body.
    The correlation id is stored in properties.correlation_id.
    """

    @wraps(f)
    def wrapper(*args, **kwgs):
        properties = args[2]
        threading.current_thread().name = properties.correlation_id

        return f(*args, **kwgs)

    return wrapper


def init_flask(app):
    """ Adds our CorrelationMiddleware to the flask application. """
    app.wsgi_app = CorrelationMiddleware(app.wsgi_app)


def init_logger(logger):
    """ Wrap all logging methods in the logger. """
    logger.log = logger_wrapper(logger.log)
    logger.info = logger_wrapper(logger.info)
    logger.warn = logger_wrapper(logger.warn)
    logger.warning = logger_wrapper(logger.warning)
    logger.critical = logger_wrapper(logger.critical)
    logger.debug = logger_wrapper(logger.debug)


def init_requests(requests):
    """ Wrap all (normal and from `Session`) outgoing request methods. """
    requests.api.request = requests_wrapper(requests.api.request)
    requests.sessions.Session.request = requests_wrapper(
        requests.sessions.Session.request
    )


def init_outgoing_rabbit(pika):
    """ Wrap outgoing messages when using `basic_publish`. """
    pika.channel.Channel.basic_publish = outgoing_rabbit_wrapper(
        pika.channel.Channel.basic_publish
    )


def init_incoming_rabbit(pika):
    """ Wrap incoming messages when using `basic_consume`. """
    pika.channel.Channel.basic_consume = incoming_rabbit_wrapper(
        pika.channel.Channel.basic_consume
    )


def initialize(flask=None, logger=None, requests=None, pika=None):
    if flask:
        init_flask(flask)
    if logger:
        init_logger(logger)
    if requests:
        init_requests(requests)
    if pika:
        init_incoming_rabbit(pika)
        init_outgoing_rabbit(pika)


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
