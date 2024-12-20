"""
This type stub file was generated by pyright.
"""

import tarfile
from pathlib import Path
from typing import Optional, Tuple
from .common import PathOrStr

def resource_to_filename(resource: PathOrStr, etag: Optional[str] = ...) -> str:
    """
    Convert a ``resource`` into a hashed filename in a repeatable way.
    If ``etag`` is specified, append its hash to the resources', delimited
    by a period.

    THis is essentially the inverse of :func:`filename_to_url()`.
    """
    ...

def filename_to_url(
    filename: str, cache_dir: Optional[PathOrStr] = ...
) -> Tuple[str, Optional[str]]:
    """
    Return the URL and etag (which may be ``None``) stored for ``filename``.
    Raises :exc:`FileNotFoundError` if ``filename`` or its stored metadata do not exist.

    This is essentially the inverse of :func:`resource_to_filename()`.
    """
    ...

def find_latest_cached(
    url: str, cache_dir: Optional[PathOrStr] = ..., verbose: bool = ...
) -> Optional[Path]:
    """
    Get the path to the latest cached version of a given resource.
    """
    ...

def check_tarfile(tar_file: tarfile.TarFile):  # -> None:
    """Tar files can contain files outside of the extraction directory, or symlinks that point
    outside the extraction directory. We also don't want any block devices fifos, or other
    weird file types extracted. This checks for those issues and throws an exception if there
    is a problem."""
    ...

def is_url_or_existing_file(url_or_filename: PathOrStr) -> bool:
    """
    Given something that might be a URL or local path,
    determine if it's actually a url or the path to an existing file.
    """
    ...
