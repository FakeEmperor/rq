# -*- coding: utf-8 -*-
#
# Copyright 2020 NVIDIA Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from distutils.version import StrictVersion

from .connections import resolve_connection as resolve_connection
from .exceptions import NoSuchJobError as NoSuchJobError
from .local import LocalStack as LocalStack
from .serializers import DefaultSerializer
from .utils import (
    import_attribute as import_attribute,
    parse_timeout as parse_timeout,
    str_to_date as str_to_date,
    utcformat as utcformat,
    utcnow as utcnow,
)
from enum import Enum
from redis.client import Pipeline, Redis
from rq.compat import (
    as_text as as_text,
    decode_redis_hash as decode_redis_hash,
    string_types as string_types,
    text_type as text_type,
)
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union, Iterable, Iterator, Dict

T = TypeVar("T")
logger: logging.Logger

class JobStatus:
    QUEUED: "str" = ...
    FINISHED: "str" = ...
    FAILED: "str" = ...
    STARTED: "str" = ...
    DEFERRED: "str" = ...
    CANCELLED: "str" = ...
    SCHEDULED: "str" = ...

    _values: Dict[str, str] = ...

    @classmethod
    def terminal(cls, value: str) -> bool: ...

    @classmethod
    def keys(cls) -> Iterator[str]: ...

    @classmethod
    def values(cls) -> Iterator[str]: ...


class RunCondition(Enum):
    FAILURE: str = ...
    SUCCESS: str = ...
    @classmethod
    def can_run(cls: Any, conditions: List[RunCondition], upstream_status: str) -> bool: ...


class JobMetadataKeys:
    DEPENDENCY_STATUS: str = ...
    CANCELLED: str = ...


class JobRunConditionStatus:
    CANNOT_RUN: str = ...
    CAN_RUN: str = ...
    DEPENDENCIES_UNFINISHED: str = ...


UNEVALUATED: Any


def unpickle(pickled_string: Any): ...
def cancel_job(job_id: Any, connection: Optional[Any] = ...) -> None: ...
def get_current_job(connection: Optional[Any] = ..., job_class: Optional[Any] = ...): ...
def requeue_job(job_id: Any, connection: Any): ...


class Job:
    redis_job_namespace_prefix: str = ...
    @classmethod
    def create(
        cls,
        func: Any,
        args: Optional[Any] = ...,
        kwargs: Optional[Any] = ...,
        connection: Optional[Redis] = ...,
        result_ttl: Optional[int] = ...,
        ttl: Optional[int] = ...,
        status: Optional[Union[str, JobStatus]] = ...,
        description: Optional[Any] = ...,
        depends_on: Union[None, str, Job, Iterable[Union[str, Job]]] = ...,
        timeout: Optional[int] = ...,
        id: Optional[str] = ...,
        origin: Optional[Any] = ...,
        meta: Optional[dict] = ...,
        failure_ttl: Optional[int] = ...,
        serializer: Optional[DefaultSerializer] = ...,
    ): ...
    def get_position(self) -> Optional[int]: ...
    def get_status(self, refresh: bool = ...) -> Optional[str]: ...
    def set_status(self, status: Union[str, JobStatus], pipeline: Optional[Pipeline] = ...) -> Any: ...
    @property
    def is_finished(self) -> bool: ...
    @property
    def is_queued(self) -> bool: ...
    @property
    def is_failed(self) -> bool: ...
    @property
    def is_started(self) -> bool: ...
    @property
    def is_deferred(self) -> bool: ...
    @property
    def is_scheduled(self) -> bool: ...
    @property
    def dependency(self) -> Optional[Job]: ...
    @property
    def dependent_ids(self): ...
    @property
    def func(self): ...
    @property
    def data(self): ...
    @data.setter
    def data(self, value: Any) -> None: ...
    def _deserialize_data(self) -> None: ...
    @property
    def func_name(self) -> str: ...
    @func_name.setter
    def func_name(self, value: Any) -> None: ...
    @property
    def instance(self): ...
    @instance.setter
    def instance(self, value: Any) -> None: ...
    @property
    def args(self) -> Tuple[Any, ...]: ...
    @args.setter
    def args(self, value: Any) -> None: ...
    @property
    def kwargs(self): ...
    @kwargs.setter
    def kwargs(self, value: Any) -> None: ...
    @classmethod
    def exists(cls, job_id: str, connection: Optional[Any] = ...): ...
    @classmethod
    def fetch(cls, id: str, connection: Optional[Any] = ...): ...
    @classmethod
    def fetch_many(cls, job_ids: Iterable[str], connection: Any): ...
    _dependency_ids: List[str] = ...
    _func_name: str = ...
    _result: Any = ...
    _status: Optional[str] = ...
    _args: tuple = ...
    _kwargs: dict = ...
    _instance: Any = ...
    _id: str = ...
    connection: Redis = ...
    created_at: Any = ...
    serializer: DefaultSerializer = ...
    description: Optional[str] = ...
    origin: Any = ...
    enqueued_at: Any = ...
    started_at: Any = ...
    ended_at: Any = ...
    exc_info: Any = ...
    timeout: Optional[int] = ...
    result_ttl: Optional[int] = ...
    failure_ttl: Optional[int] = ...
    retries_left: Optional[int] = ...
    retry_intervals: Optional[List[int]] = ...
    ttl: Optional[int] = ...
    meta: dict = ...

    def __init__(
        self, id: Optional[str] = ..., connection: Optional[Redis] = ..., serializer: Optional[DefaultSerializer] = ...
    ) -> None: ...
    def __eq__(self, other: Job) -> Any: ...
    def __hash__(self) -> Any: ...
    def get_id(self) -> str: ...
    def set_id(self, value: str) -> None: ...

    @property
    def id(self) -> str: ...

    @id.setter
    def id(self, value: str) -> None: ...

    @classmethod
    def key_for(cls, job_id: str): ...
    @classmethod
    def dependents_key_for(cls, job_id: str): ...
    @property
    def key(self): ...
    @property
    def dependents_key(self): ...
    @property
    def dependencies_key(self): ...
    def fetch_dependencies(self, watch: bool = ..., pipeline: Optional[Pipeline] = ...): ...
    def get_parent_ids(
        self, recursive: bool = ..., pipeline: Pipeline = ..., raise_on_no_such_job: bool = ...
    ) -> List[str]: ...
    def get_parents(self, recursive: bool = ..., pipeline: Pipeline = ..., raise_on_no_such_job: bool = ...) -> List[Job]: ...
    def get_children(self, recursive: bool = ..., pipeline: Pipeline = ..., raise_on_no_such_job: bool = ...) -> List[Job]: ...
    @property
    def result(self) -> T: ...
    return_value: Any = ...
    def restore(self, raw_data: Any) -> None: ...
    def refresh(self) -> None: ...
    def to_dict(self, include_meta: bool = ...): ...
    def save(self, pipeline: Optional[Pipeline] = ..., include_meta: bool = ...) -> None: ...
    def get_redis_server_version(self) -> StrictVersion: ...
    def save_meta(self) -> None: ...
    def cancel(self, pipeline: Optional[Pipeline] = ...) -> None: ...
    @property
    def run_when(self) -> List[RunCondition]: ...
    @property
    def on_failure(self) -> Optional[Callable[[Job, BaseException], Any]]: ...
    @property
    def on_success(self) -> Optional[Callable[[Job, Any], Any]]: ...
    def process_dependencies(self, job_status: Union[str, JobStatus], pipeline: Pipeline = ...) -> None: ...
    def check_run_condition(self, pipeline: Pipeline = None, refresh: bool = False) -> str: ...
    def requeue(self) -> None: ...
    def delete(
        self, pipeline: Optional[Pipeline] = ..., remove_from_queue: bool = ..., delete_dependents: bool = ...
    ) -> None: ...
    def delete_dependents(self, pipeline: Optional[Pipeline] = ...) -> None: ...
    def _execute(self) -> Any: ...
    def perform(self, invoke_callbacks: bool = ..., process_dependencies: bool = ...) -> T: ...
    def get_ttl(self, default_ttl: Optional[int] = ...): ...
    def get_result_ttl(self, default_ttl: Optional[int] = ...): ...
    def get_call_string(self): ...
    def cleanup(
        self, ttl: Optional[int] = ..., pipeline: Optional[Pipeline] = ..., remove_from_queue: bool = ...
    ) -> None: ...
    def get_retry_interval(self) -> int: ...
    @property
    def failed_job_registry(self): ...
    def register_dependency(self, pipeline: Optional[Pipeline] = ...) -> None: ...
    @classmethod
    def _get_linked_jobs(
        cls,
        job: Job,
        link_key_getter: Callable[[Job], str],
        recursive: bool,
        pipeline: Pipeline,
        raise_on_no_such_job: bool = ...,
    ) -> List[str]: ...

    @property
    def dependency_ids(self) -> List[str]: ...
    def dependencies_are_met(self, exclude_job_id: Optional[str] = ..., pipeline: Optional[Pipeline] = ...) -> bool: ...


_job_stack: LocalStack


class Retry(object):
    max: int = ...
    intervals: List[int] = ...
    def __init__(self, max: int, interval: int = 0): ...
