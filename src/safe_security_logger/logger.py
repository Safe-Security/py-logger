import logging
import sys
import time

from pythonjsonlogger import jsonlogger

__author__ = "deepak.s@safe.security"
__copyright__ = "Safe Security"
__license__ = "MIT"


def getLogger(name):
    logger = logging.getLogger(name)

    # Logs will be written to console
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(name)s %(module)s %(funcName)s ",
        rename_fields={
            "levelname": "level",
            "asctime": "timestamp",
            "funcName": "functionName",
            "name": "loggerName",
        },
    )
    # Use UTC time
    formatter.converter = time.gmtime
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # default level would be INFO
    logger.setLevel(logging.INFO)
    return logger
