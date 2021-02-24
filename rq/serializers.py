from functools import partial

import pickle
import json

from .compat import string_types as string_types
from .utils import import_attribute as import_attribute
from typing import Optional, Any, Callable, Union, Type


class DefaultSerializer:
    dumps: Callable[[Any], str] = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
    loads: Callable[[str], Any] = pickle.loads


class JSONSerializer():
    @staticmethod
    def dumps(*args, **kwargs):
        return json.dumps(*args, **kwargs).encode('utf-8')

    @staticmethod
    def loads(s, *args, **kwargs):
        return json.loads(s.decode('utf-8'), *args, **kwargs)


def resolve_serializer(serializer: Optional[Union[str, bytes]]) -> Union[Type[DefaultSerializer], Any]:
    """This function checks the user defined serializer for ('dumps', 'loads') methods
    It returns a default pickle serializer if not found else it returns a MySerializer
    The returned serializer objects implement ('dumps', 'loads') methods
    Also accepts a string path to serializer that will be loaded as the serializer
    """
    if not serializer:
        return DefaultSerializer

    if isinstance(serializer, string_types):
        serializer = import_attribute(serializer)

    default_serializer_methods = ('dumps', 'loads')

    for instance_method in default_serializer_methods:
        if not hasattr(serializer, instance_method):
            raise NotImplementedError('Serializer should have (dumps, loads) methods.')

    return serializer
