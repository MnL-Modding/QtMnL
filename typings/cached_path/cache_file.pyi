"""
This type stub file was generated by pyright.
"""

from .common import PathOrStr

logger = ...

class CacheFile:
    """
    This is a context manager that makes robust caching easier.

    On `__enter__`, an IO handle to a temporarily file is returned, which can
    be treated as if it's the actual cache file.

    On `__exit__`, the temporarily file is renamed to the cache file. If anything
    goes wrong while writing to the temporary file, it will be removed.
    """

    def __init__(
        self, cache_filename: PathOrStr, mode: str = ..., suffix: str = ...
    ) -> None: ...
    def __enter__(self):  # -> _TemporaryFileWrapper[Any]:
        ...

    def __exit__(self, exc_type, exc_value, traceback):  # -> bool:
        ...
