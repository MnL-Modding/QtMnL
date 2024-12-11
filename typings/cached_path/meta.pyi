"""
This type stub file was generated by pyright.
"""

from dataclasses import dataclass
from typing import Optional
from .common import PathOrStr

@dataclass
class Meta:
    """
    Any resource that is downloaded to - or extracted in - the cache directory will
    have a meta JSON file written next to it, which corresponds to an instance
    of this class.

    In older versions of AllenNLP, this meta document just had two fields: 'url' and
    'etag'. The 'url' field is now the more general 'resource' field, but these old
    meta files are still compatible when a `Meta` is instantiated with the `.from_path()`
    class method.
    """

    resource: str
    cached_path: str
    creation_time: float
    size: int = ...
    etag: Optional[str] = ...
    extraction_dir: bool = ...
    @classmethod
    def new(
        cls,
        resource: PathOrStr,
        cached_path: PathOrStr,
        *,
        etag: Optional[str] = ...,
        extraction_dir: bool = ...
    ) -> Meta: ...
    def to_file(self) -> None: ...
    @classmethod
    def from_path(cls, path: PathOrStr) -> Meta: ...
    @staticmethod
    def get_resource_size(path: PathOrStr) -> int:
        """
        Get the size of a file or directory.
        """
        ...