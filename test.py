import safe_security_logger as logging

logger = logging.getLogger("awesome-logger")


def test():
    logger.info("Hello world")


test()
