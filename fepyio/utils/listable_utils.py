from typing import Callable, Optional, TypeVar, Union

# If we run this as main, the import fails
try:
    from fepyio.typing.listable import Listable, Tupleable
except ImportError:
    import sys
    from os.path import abspath, dirname, join

    # Add 'fepyio/typing/' to sys path
    sys.path.append(join(dirname(dirname(abspath(__file__))), "typing"))
    from listable import Listable, Tupleable  # type: ignore


T = TypeVar("T")


def listable_map(func: Callable, value: Optional[Listable], none_pass: bool = True):
    """Like map(), but for listables.

    Parameters
    ----------
    func : callable
        Function to apply to listable.
    value : Listable
        Listable to have function applied to.
    none_pass : bool, default=True
        If True and `value` is None, return None instead of passing `value` to `func`.
    """
    if value is None and none_pass:
        return None
    if isinstance(value, list):
        return list(map(func, value))

    return func(value)


def tupleable_map(func: Callable, value: Optional[Tupleable], none_pass: bool = True):
    """Like map(), but for tupleables.

    Parameters
    ----------
    func : callable
        Function to apply to tupleable.
    value : Tupleable
        Tupleable to have function applied to.
    none_pass : bool, default=True
        If True and `value` is None, return None instead of passing `value` to `func`.
    """
    if value is None and none_pass:
        return None
    if isinstance(value, tuple):
        return tuple(map(func, value))

    return func(value)


def unlist(listable: Union[T, list[T], tuple[T]]) -> Union[T, list[T], tuple[T]]:
    """Convert a list or tuple of length 1 to a single item, otherwise pass.

    Examples
    --------
    >>> unlist([1, 2, 3])
    [1, 2, 3]
    >>> unlist([1])
    1
    >>> unlist((1, 2, 3))
    (1, 2, 3)
    >>> unlist((1,))
    1
    >>> unlist(1)
    1
    """
    if isinstance(listable, (list, tuple)) and len(listable) == 1:
        return listable[0]
    else:
        return listable


if __name__ == "__main__":
    import doctest

    doctest.testmod()
