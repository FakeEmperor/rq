# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import sys

from rq.utils import ColorizingStreamHandler
from rq.defaults import (DEFAULT_LOGGING_FORMAT,
                         DEFAULT_LOGGING_DATE_FORMAT)


from typing import Optional


def setup_loghandlers(level: Optional[int] = None, date_format: str = DEFAULT_LOGGING_DATE_FORMAT,
                      log_format: str = DEFAULT_LOGGING_FORMAT, name: str = 'rq.worker') -> None:
    logger = logging.getLogger(name)

    if not _has_effective_handler(logger):
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        handler = ColorizingStreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        handler.addFilter(lambda record: record.levelno < logging.ERROR)
        error_handler = ColorizingStreamHandler(stream=sys.stderr)
        error_handler.setFormatter(formatter)
        error_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
        logger.addHandler(handler)
        logger.addHandler(error_handler)

    if level is not None:
        # The level may be a numeric value (e.g. when using the logging module constants)
        # Or a string representation of the logging level
        logger.setLevel(level if isinstance(level, int) else level.upper())


def _has_effective_handler(logger: logging.Logger):
    """
    Checks if a logger has a handler that will catch its messages in its logger hierarchy.
    :param `logging.Logger` logger: The logger to be checked.
    :return: True if a handler is found for the logger, False otherwise.
    :rtype: bool
    """
    while True:
        if logger.handlers:
            return True
        if not logger.parent:
            return False
        logger = logger.parent
