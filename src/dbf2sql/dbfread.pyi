# Type stubs for dbfread library
from collections import OrderedDict
from typing import Any, Iterator, List, Optional

class Field:
    name: str
    type: str
    length: int
    decimal_count: int

class DBF:
    def __init__(
        self,
        filename: str,
        encoding: Optional[str] = None,
        char_decode_errors: str = "strict",
        **kwargs: Any,
    ) -> None: ...
    def __enter__(self) -> "DBF": ...
    def __exit__(self, *args: Any) -> None: ...
    def __iter__(self) -> Iterator[OrderedDict[str, Any]]: ...
    def __len__(self) -> int: ...
    @property
    def fields(self) -> List[Field]: ...
    @property
    def encoding(self) -> Optional[str]: ...
