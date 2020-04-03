#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   viaa.frameworks.flask

from flask import Flask as App
from werkzeug.wrappers import Request, Response, ResponseStream

from viaa.observability.correlation import CorrelationID, CORRELATION_ID_KEY


class CorrelationMiddleware:
    """
    Middleware to check if a viaa request id is present in the request header.
    Generates a new one if not present.
    """

    def __init__(self, app):
        self.app = app.wsgi_app
        # 
        app.wsgi_app = self

    def __call__(self, environ, start_response) -> App:
        incoming_request = Request(environ)
        # TODO: it seems odd that `CorrelationID` needs to be instantiated
        correlation_id = CorrelationID().get_correlation_id_from_flask(incoming_request)
        print(f"Correlation ID returned: {correlation_id}")
        # Set the correlation ID in the environment.
        # The environment variable name is all uppercase, snakecase prefixed with "HTTP"
        env_var = f"HTTP_{CORRELATION_ID_KEY.upper().replace('-', '_')}"
        environ[env_var] = correlation_id

        # Finally, add the header to the response
        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append((CORRELATION_ID_KEY, correlation_id))
            return start_response(status, response_headers, exc_info)
            
        return self.app(environ, new_start_response)


#~ class Flask(App):
    #~ pass


#~ class Flask(App):
    #~ """"""
    #~ def __init__(self, app: App):
        #~ """
        #~ :type app: App
        #~ :param app: Flask application
        #~ """
        #~ self.app = app
    #~ #
    #~ def __call__(self, environ, start_response) -> App:
        #~ incoming_request = Request(environ)
        #~ correlation_id = CorrelationID.get_correlation_id_from_flask(incoming_request)
        #~ # Set the correlation ID in the environment
        #~ environ["HTTP_X_CORRELATION_ID"] = correlation_id
        #~ return self.app(environ, start_response)
