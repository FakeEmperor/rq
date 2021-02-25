from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from redis import Redis
    from rq.worker import Worker


WORKERS_SUSPENDED: str = 'rq:suspended'


def is_suspended(connection: "Redis", worker: Optional["Worker"] = None) -> bool:
    with connection.pipeline() as pipeline:
        if worker is not None:
            worker.heartbeat(pipeline=pipeline)
        pipeline.exists(WORKERS_SUSPENDED)
        # pipeline returns a list of responses
        # https://github.com/andymccurdy/redis-py#pipelines
        return pipeline.execute()[-1]


def suspend(connection: "Redis", ttl: Optional[float] = None) -> None:
    """ttl = time to live in seconds.  Default is no expiration
       Note:  If you pass in 0 it will invalidate right away
    """
    connection.set(WORKERS_SUSPENDED, 1)
    if ttl is not None:
        connection.expire(WORKERS_SUSPENDED, ttl)


def resume(connection: "Redis"):
    return connection.delete(WORKERS_SUSPENDED)
