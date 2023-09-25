from LogHelper import SetLogLevel
import logging

def test_SetLogLevel():

    logger = logging.getLogger()

    SetLogLevel("TRACE")
    assert logger.level == logging.DEBUG

    SetLogLevel("DEBUG")
    assert logger.level == logging.DEBUG

    SetLogLevel("INFO")
    assert logger.level == logging.INFO

    SetLogLevel("NOTE")
    assert logger.level == logging.INFO

    SetLogLevel("WARNING")
    assert logger.level == logging.WARNING

    SetLogLevel("ERROR")
    assert logger.level == logging.ERROR

    SetLogLevel("FATAL")
    assert logger.level == logging.CRITICAL

    SetLogLevel("INVALID")
    assert logger.level == logging.DEBUG
