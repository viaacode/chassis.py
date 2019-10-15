Logging
=======

The logging interface is made to resemble the Python standard logging
as close as possible. The biggest difference is that you can pass
a config object when getting a logger instance.

**ALL** logging will go to `stdout` as a JSON string,
this means that logging by external packages will be formatted aswell.
Formatting all logs as JSON makes it easier to parse the logs
in other applications.

Running following example:

.. code-block:: python

    import logging as basic_logging
    from viaa.observability import logging
    from viaa.configuration import ConfigParser

    example_dictionary = {"test_key": "test_value"}

    config = ConfigParser()
    logger = logging.get_logger(__name__, config)

    basic_logger = basic_logging.getLogger()

    logger.warning("Hello world!", string="extra info", dictionary=example_dictionary)
    basic_logger.warning("basic log")


Will print:

.. code-block:: json

    {"message": "Hello world!", "string": "extra info", "dictionary": {"test_key": "test_value"}, "logger": "__main__", "level": "warning", "timestamp": "2019-10-03T12:52:21.857624Z", "source": ".\\hello.py:<module>:12"}
    {"message": "basic log"}

API
---

.. automodule:: viaa.observability.logging
    :members:
