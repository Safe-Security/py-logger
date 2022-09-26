import logging
import sys
import time

from pythonjsonlogger import jsonlogger

__author__ = "deepak.s@safe.security"
__copyright__ = "Safe Security"
__license__ = "MIT"

# Adding custom logger to support additional default field such as serviceName
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop("service", None)
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if (not log_record.get("service")) and self.service:
            log_record["service"] = self.service


def getLogger(name, service=None, level=logging.INFO):
    logger = logging.getLogger(name)

    # Logs will be written to console
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = CustomJsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(name)s %(module)s %(funcName)s",
        rename_fields={
            "levelname": "level",
            "asctime": "timestamp",
            "funcName": "functionName",
            "name": "loggerName",
        },
        service=service,
    )

    # Use UTC time
    formatter.converter = time.gmtime
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # default level would be INFO if level is not provided
    logger.setLevel(level)
    return logger
