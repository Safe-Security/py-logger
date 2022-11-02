# built-ins
import json
import logging
import typing
import unittest
import unittest.mock as mock

# third party
import pytest

# packages
import safe_security_logger as logger

__author__ = "deepak.s@safe.security"
__copyright__ = "deepak-sreekumar"
__license__ = "MIT"


class TestGetLoggerConfigurations:
    """
    This test class will test the getLogger function inside
    src.safe_security_logger.logger.py

    getLogger creates the logger.

    In this test class,
        - We need to make sure that all the configurations are properly set.
        - This test class lets us be sure that the problems related to
          improper configurations are tested.

    We test:
        - handler settings
        - log level settings
        - formatter settings

    Author: Namah Shrestha
    """

    @pytest.mark.parametrize(
        "loglevel, expected_loglevel",
        [
            (logging.NOTSET, 0),
            (logging.DEBUG, 10),
            (None, 20),
            (logging.WARN, 30),
            (logging.ERROR, 40),
            (logging.CRITICAL, 50),
        ],
    )
    def test_log_level(
        self, loglevel: typing.Union[int, None], expected_loglevel: int
    ) -> None:
        """
        Theory:
        -------
        Python has six log levels.
        Each one is assigned a specific integer,
        indicating the severity of the log.

        NOTSET=0
        DEBUG=10
        INFO=20
        WARN=30
        ERROR=40
        CRITICAL=50

        Tests:
        ------
        1. getLogger says that the default level of log should be INFO
           if no level is provided.
        2. All other logging levels should be set by the level parameter.

        Author: Namah Shrestha
        """
        logname: str = "test-safe-logger"
        if loglevel is not None:
            logr: logging.Logger = logger.getLogger(logname, level=loglevel)
        else:
            logr: logging.Logger = logger.getLogger(logname)
        assert logr.level == expected_loglevel

    @pytest.mark.parametrize(
        "handlers_input, handler_names",
        [
            ([], {"StreamHandler"}),
            ([logging.FileHandler("dummy_file.log")], {"StreamHandler", "FileHandler"}),
        ],
    )
    def test_handlers(self, handlers_input: list, handler_names: set) -> None:
        """
        Theory:
        -------
        There are three core handlers in the logging module.
        1. StreamHandler:
            - Sends logging output to streams.
            - Such as, sys.stdout, sys.stderr, or any file-like object.
            - Precisely, any object which supports write() and flush() methods.
        2. FileHandler:
            - Sends logging output to a disk file.
            - Inherits the output functionality from StreamHandler.
        3. NullHandler:
            - It does not do any formatting or output.
            - It is essentially a `no-op` handler for use by library developers.
        All 3 classes are located in the core logging package.

        There are other handlers located at logging.handlers package
        built for their own purposes.
        Read more: https://docs.python.org/3/library/logging.handlers.html

        Tests:
        ------
        1. console_handler is a StreamHandler sending output to sys.stdout.
            It should be added by default.
        2. We should be able to add other handlers using the handlers list.

        Author: Namah Shrestha
        """
        get_handler_names: callable = lambda x: {
            str(item).split(" ")[0][1:] for item in x.handlers
        }
        logr: logging.Logger = logger.getLogger(
            "test-safe-logger", handlers=handlers_input
        )
        assert get_handler_names(logr) == handler_names


class TestGetLoggerResults(unittest.TestCase):
    """
    This test class uses unittest.
    Just to mock the stdout.write.
    And to assert that stdout.write
    was called with the expected output.
    """

    def setUp(self) -> None:
        self.streamlogr: logging.Logger = logger.getLogger("test-stream-logger")

    def compare_while_ignoring(
        self, first: dict, second: dict, ignore_keys: list = []
    ) -> bool:
        """
        Function compares each key of first and second dictionaries.
        It will ignore keys that are specified in the ignore_keys list.
        """
        for key, value in first.items():
            if key in ignore_keys:
                continue
            if key not in second:
                return False
            if value != second[key]:
                return False
        return True

    @mock.patch("sys.stdout.write")
    def test_results_for_streaming_handler(self, fake_write) -> None:
        """
        Here we test the actual result of the log
        with the expected output.
        """
        input: str = "asd"
        expected_output: dict = {
            "timestamp": "2022-10-29 12:10:33,699",
            "level": "INFO",
            "message": "asd",
            "type": "application",
            "metadata": {
                "loggerName": "test-stream-logger",
                "module": "test_logger",
                "functionName": "test_results_for_streaming_handler",
                "lineno": 173,
            },
        }
        self.streamlogr.info(input)
        actual_output: dict = json.loads(fake_write.call_args_list[0][0][0])
        result: bool = self.compare_while_ignoring(
            expected_output, actual_output, ignore_keys=["timestamp"]
        )
        self.assertEqual(result, True)
