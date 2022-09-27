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
        self.additional_fields = kwargs.pop("additional_fields", None)
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        for key, value in self.additional_fields.items():
            if (not log_record.get(key)) and value:
                log_record[key] = value


def getLogger(
    name, service=None, level=logging.INFO, handlers=[], additional_fields={}
):

    logger = logging.getLogger(name)

    if service:
        additional_fields.update({"service": service})

    formatter = CustomJsonFormatter(
        "%(asctime)s %(levelname)s %(message)s %(name)s %(module)s %(funcName)s",
        rename_fields={
            "levelname": "level",
            "asctime": "timestamp",
            "funcName": "functionName",
            "name": "loggerName",
        },
        service=service,
        additional_fields=additional_fields,
    )
    # Use UTC time
    formatter.converter = time.gmtime

    # console handler would be added by default
    console_handler = logging.StreamHandler(sys.stdout)
    handlers.append(console_handler)

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # default level would be INFO if level is not provided
    logger.setLevel(level)
    return logger
