"""
This type stub file was generated by pyright.
"""

import io
from typing import Optional
from .scheme_client import SchemeClient

"""
Cloudflare R2.
"""

class R2Client(SchemeClient):
    recoverable_errors = ...
    scheme = ...
    def __init__(self, resource: str) -> None: ...
    def get_etag(self) -> Optional[str]: ...
    def get_size(self) -> Optional[int]: ...
    def get_resource(self, temp_file: io.BufferedWriter) -> None: ...
    def get_bytes_range(self, index: int, length: int) -> bytes: ...