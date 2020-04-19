#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   viaa.communication.amqp

# Builtin
from functools import wraps
# 3d
import pika
# Local
from viaa.observability.correlation import CorrelationID


def outgoing_rabbit_wrapper(f):
    """ Sets the correlation_id property of a rabbit message to the current correlation id """

    @wraps(f)
    def wrapper(*args, **kwgs):
        properties = kwgs.get("properties")
        if properties is None:
            properties = pika.BasicProperties(correlation_id=CorrelationID().correlation_id)
        else:
            properties.correlation_id = CorrelationID().correlation_id
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
        CorrelationID().correlation_id = properties.correlation_id

        return f(*args, **kwgs)

    return wrapper

class amqp:
    """ Wrap outgoing messages when using `basic_publish`. """
    pika.channel.Channel.basic_publish = outgoing_rabbit_wrapper(
        pika.channel.Channel.basic_publish
    )
    """ Wrap incoming messages when using `basic_consume`. """
    pika.channel.Channel.basic_consume = incoming_rabbit_wrapper(
        pika.channel.Channel.basic_consume
    )
    ConnectionParameters = pika.ConnectionParameters
    BlockingConnection = pika.BlockingConnection
    BasicProperties = pika.BasicProperties
