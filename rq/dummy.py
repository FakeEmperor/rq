# -*- coding: utf-8 -*-
"""
Some dummy tasks that are well-suited for generating load for testing purposes.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
import time


from typing import Any
def do_nothing() -> None:
    pass


def sleep(secs: Any) -> None:
    time.sleep(secs)


def endless_loop() -> None:
    while True:
        time.sleep(1)


def div_by_zero() -> None:
    1 / 0


def fib(n: Any):
    if n <= 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)


def random_failure():
    if random.choice([True, False]):
        class RandomError(Exception):
            pass
        raise RandomError('Ouch!')
    return 'OK'
