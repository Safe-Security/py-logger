import safe_security_logger as logger

__author__ = "deepak.s@safe.security"
__copyright__ = "deepak-sreekumar"
__license__ = "MIT"


def test_logger():
    safelogger = logger.getLogger("safe-logger")
    assert safelogger.name == "safe-logger"
