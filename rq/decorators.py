# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from functools import wraps

from rq.compat import string_types

from .defaults import DEFAULT_RESULT_TTL
from .queue import Queue
from .utils import backend_class


from redis import Redis
from .defaults import DEFAULT_RESULT_TTL as DEFAULT_RESULT_TTL
from .job import Job
from .queue import Queue as Queue
from .utils import backend_class as backend_class
from typing import Any, Optional, Type, Iterable, Union, Callable
class job(object):  # noqa
    queue: str
    connection: Redis
    timeout: Optional[int]
    result_ttl: Optional[int]
    ttl: Optional[int]
    meta: Optional[dict]
    depends_on: Optional[Iterable[Union[str, Job]]]
    at_front: Optional[bool]
    description: Optional[str]
    failure_ttl: Optional[int]
    queue_class: Type[Queue] = Queue

    def __init__(self, queue: str, connection: Optional[Redis] = None, timeout: Optional[int] = None,
                 result_ttl: int = DEFAULT_RESULT_TTL, ttl: Optional[int] = None,
                 queue_class: Optional[Type[Queue]] = None, depends_on: Optional[Iterable[Union[str, Job]]] = None, at_front: Optional[bool] = None, meta: Optional[dict] = None,
                 description: Optional[str] = None, failure_ttl: Optional[int] = None, retry: Optional[int] = None) -> None:
        """A decorator that adds a ``delay`` method to the decorated function,
        which in turn creates a RQ job when called. Accepts a required
        ``queue`` argument that can be either a ``Queue`` instance or a string
        denoting the queue name.  For example:

            @job(queue='default')
            def simple_add(x, y):
                return x + y

            simple_add.delay(1, 2) # Puts simple_add function into queue
        """
        self.queue = queue
        self.queue_class = backend_class(self, 'queue_class', override=queue_class)
        self.connection = connection
        self.timeout = timeout
        self.result_ttl = result_ttl
        self.ttl = ttl
        self.meta = meta
        self.depends_on = depends_on
        self.at_front = at_front
        self.description = description
        self.failure_ttl = failure_ttl
        self.retry = retry

    def __call__(self, f: Callable) -> Job:
        @wraps(f)
        def delay(*args, **kwargs):
            if isinstance(self.queue, string_types):
                queue = self.queue_class(name=self.queue,
                                         connection=self.connection)
            else:
                queue = self.queue

            depends_on = kwargs.pop('depends_on', None)
            job_id = kwargs.pop('job_id', None)
            at_front = kwargs.pop('at_front', False)

            if not depends_on:
                depends_on = self.depends_on

            if not at_front:
                at_front = self.at_front

            return queue.enqueue_call(f, args=args, kwargs=kwargs,
                                      timeout=self.timeout, result_ttl=self.result_ttl,
                                      ttl=self.ttl, depends_on=depends_on, job_id=job_id, at_front=at_front,
                                      meta=self.meta, description=self.description, failure_ttl=self.failure_ttl,
                                      retry=self.retry)
        f.delay = delay
        return f
