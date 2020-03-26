import json
import sys

import pytest

from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()

# TODO: can we fix this fixture through `parametrize`?
# see: https://docs.pytest.org/en/latest/parametrize.html
@pytest.fixture
def setup_logging():
    def _f(name, loglevel):
        # loglevel should be one of Python's standard loglevels.
        config.config["logging"]["level"] = loglevel
        logger = logging.get_logger(name, config)
        return logger
    return _f


def test_log_debug(capsys, setup_logging):
    logger = setup_logging(__name__, "DEBUG")

    logger.debug("test_log_debug")

    captured = capsys.readouterr()

    record_object = json.loads(captured.out)

    assert record_object["message"] == "test_log_debug"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "debug"
    assert record_object["timestamp"] != ""


def test_log_info(capsys, setup_logging):
    logger = setup_logging(__name__, "INFO")

    logger.info("test_log_info")

    captured = capsys.readouterr()

    record_object = json.loads(captured.out)

    assert record_object["message"] == "test_log_info"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "info"
    assert record_object["timestamp"] != ""


def test_log_warning(capsys, setup_logging):
    logger = setup_logging(__name__, "WARNING")

    logger.warning("test_log_warning")

    captured = capsys.readouterr()

    record_object = json.loads(captured.out)

    assert record_object["message"] == "test_log_warning"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "warning"
    assert record_object["timestamp"] != ""


def test_log_critical(capsys, setup_logging):
    logger = setup_logging(__name__, "CRITICAL")

    logger.critical("test_log_critical")

    captured = capsys.readouterr()

    record_object = json.loads(captured.out)

    assert record_object["message"] == "test_log_critical"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "critical"
    assert record_object["timestamp"] != ""


def test_logger_name(capsys, setup_logging):
    logger = setup_logging("ionic_defibulizer", "INFO")

    logger.info("test")

    captured = capsys.readouterr()

    record_object = json.loads(captured.out)

    assert record_object["message"] == "test"
    assert record_object["logger"] == "ionic_defibulizer"
    assert record_object["level"] == "info"
    assert record_object["timestamp"] != ""

