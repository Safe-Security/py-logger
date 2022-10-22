# built-ins
import logging
import sys
import typing

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
    def test_handlers(self, handlers_input: list, handler_names: set[str]) -> None:
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


@pytest.mark.usefixtures("get_safe_security_logger", "capture_stdout_output")
class TestGetLoggerResults:
    """
    This test class will test the getLogger function inside
    src.safe_security_logger.logger.py

    getLogger creates the logger.

    In this test class,
        - We make sure the logger behaves the way we want it to.
        - By testing the actual results.
        - We will rely heavily on monkeypatching to capture output results.

    Author: Namah Shrestha
    """

    def test_setup_is_working(self) -> None:
        """
        This test function is written to assure that the fixtures are working fine.
        - The logger is created which means get_safe_security_logger
          fixture is working.
        - `fake_write` in `sys.stdout.write` means that, sys.stdout.write
          has been successfully mocked.
        - `fake_write` in `builtins.open` means that,
            io.open has been succesfully mocked.

        Author: Namah Shrestha
        """
        assert self.logger.name == "test-safe-logger"
        assert "fake_write" in str(sys.stdout.write)
        # uncomment if you have monkeypatched io.open
        # assert 'fake_write' in str(io.open)

    @pytest.mark.parametrize(
        "inputstr, extra, expected_output",
        [
            (
                "Hello World",
                {"text": "world"},
                {
                    "timestamp": "2022-10-24 06:18:11,710",
                    "level": "INFO",
                    "message": "Hello",
                    "type": "application",
                    "metadata": {
                        "loggerName": "awesome-logger",
                        "module": "<stdin>",
                        "functionName": "<module>",
                        "lineno": 1,
                    },
                },
            )
        ],
    )
    def test_results_for_streaming_handler(
        self, inputstr: typing.Any, extra: dict, expected_output: dict
    ) -> None:
        """
                This test will test the output of the streaming handler log.
                With various input configurations.

                Current Issue:
                    - Unable to capture logs from sys.stdout.
                    - StreamHandler should be writing to sys.stdout.
                    - But monkeypatching sys.stdout is not working.
                    - If this happens many times, we might go with a simple
                      unittest method.
        s
                Author: Namah Shrestha
        """
