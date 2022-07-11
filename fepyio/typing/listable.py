from typing import TypeVar, Union

T = TypeVar("T")
Listable = Union[T, list[T]]

# See: https://github.com/python/mypy/issues/10242
Tupleable = Union[T, tuple[T, ...]]  # type: ignore
