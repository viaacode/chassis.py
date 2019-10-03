import json
import sys

from viaa.observability import logging
from viaa.configuration import ConfigParser

config = ConfigParser()

def test_log_info(caplog, capsys):    
    logger = logging.get_logger(__name__, config)
    
    logger.info("test_log_info")
    
    out, err = capsys.readouterr()
    
    record_object = json.loads(out)
    
    assert record_object["message"] == "test_log_info"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "info"
    assert record_object["timestamp"] != ""
    
    
def test_log_warning(caplog, capsys):    
    logger = logging.get_logger(__name__, config)
    
    logger.warning("test_log_warning")
    
    out, err = capsys.readouterr()
    
    record_object = json.loads(out)
    
    assert record_object["message"] == "test_log_warning"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "warning"
    assert record_object["timestamp"] != ""
    

def test_log_critical(caplog, capsys):    
    logger = logging.get_logger(__name__, config)
    
    logger.critical("test_log_critical")
    
    out, err = capsys.readouterr()
    
    record_object = json.loads(out)
    
    assert record_object["message"] == "test_log_critical"
    assert record_object["logger"] == "test_logging"
    assert record_object["level"] == "critical"
    assert record_object["timestamp"] != ""
    
    
def test_logger_name(caplog, capsys):    
    logger = logging.get_logger("test_naam", config)
    
    logger.info("test")
    
    out, err = capsys.readouterr()
    
    record_object = json.loads(out)
    
    assert record_object["message"] == "test"
    assert record_object["logger"] == "test_naam"
    assert record_object["level"] == "info"
    assert record_object["timestamp"] != ""
    