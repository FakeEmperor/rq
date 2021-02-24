# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from typing import Any

class NoSuchJobError(Exception):
    pass


class InvalidJobDependency(Exception):
    pass


class InvalidJobOperationError(Exception):
    pass


class InvalidJobOperation(Exception):
    pass


class DequeueTimeout(Exception):
    pass


class ShutDownImminentException(Exception):
    extra_info: Any
    def __init__(self, msg: Any, extra_info: Any) -> None:
        self.extra_info = extra_info
        super(ShutDownImminentException, self).__init__(msg)


class TimeoutFormatError(Exception):
    pass
