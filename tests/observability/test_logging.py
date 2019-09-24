import json
import sys

from viaa.observability import logging


def test_log_info(caplog, capsys):    
    logger = logging.get_logger(__name__)
    
    logger.info("test_log_info")
    
    assert len(caplog.records) == 1
    record = next(iter(caplog.records))
    record_object = json.loads(record.msg)
    
    assert record_object["msg"] == "test_log_info"
    assert record_object["extra"]["logger"] == "test_logging"
    assert record_object["extra"]["level"] == "info"
    assert record_object["extra"]["timestamp"] != ""
    
    
def test_log_warning(caplog, capsys):    
    logger = logging.get_logger(__name__)
    
    logger.warning("test_log_warning")
    
    assert len(caplog.records) == 1
    record = next(iter(caplog.records))
    record_object = json.loads(record.msg)
    
    assert record_object["msg"] == "test_log_warning"
    assert record_object["extra"]["logger"] == "test_logging"
    assert record_object["extra"]["level"] == "warning"
    assert record_object["extra"]["timestamp"] != ""
    

def test_log_critical(caplog, capsys):    
    logger = logging.get_logger(__name__)
    
    logger.critical("test_log_critical")
    
    assert len(caplog.records) == 1
    record = next(iter(caplog.records))
    record_object = json.loads(record.msg)
    
    assert record_object["msg"] == "test_log_critical"
    assert record_object["extra"]["logger"] == "test_logging"
    assert record_object["extra"]["level"] == "critical"
    assert record_object["extra"]["timestamp"] != ""
    
    
def test_logger_name(caplog, capsys):    
    logger = logging.get_logger("test_naam")
    
    logger.info("test")
    
    assert len(caplog.records) == 1
    record = next(iter(caplog.records))
    record_object = json.loads(record.msg)
    
    assert record_object["msg"] == "test"
    assert record_object["extra"]["logger"] == "test_naam"
    assert record_object["extra"]["level"] == "info"
    assert record_object["extra"]["timestamp"] != ""
    