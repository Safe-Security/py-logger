.. image:: https://img.shields.io/pypi/v/safe-security-logger.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/safe-security-logger/


.. image:: https://img.shields.io/github/workflow/status/deepak-sreekumar/safe-security-logger/publish
    :alt: Built Status
    :target: https://github.com/deepak-sreekumar/safe-security-logger/actions/workflows/publish.yml


|

====================
safe-security-logger
====================


    Structured JSON logger package from Safe Security



============
Installation
============

::

    pip install -i https://test.pypi.org/simple/ safe-security-logger


============
Usage
============

::

    import safe_security_logger as logging

    logger = logging.getLogger("awesome-logger")

    def test():
        logger.info("Hello world")
        logger.info("Hello world", extra={"text": "testing logging"})

    test()
